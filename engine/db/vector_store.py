import json
import math
import sqlite3
from typing import List, Dict, Any, Optional

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    
    if HAS_NUMPY:
        a = np.array(v1, dtype=float)
        b = np.array(v2, dtype=float)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
    else:
        # Pure Python fallback calculation (zero external dependencies)
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

class VectorStore:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_memory(
        self,
        campaign_id: str,
        turn_number: int,
        content: str,
        importance: float,
        event_type: str = "event",
        characters: Optional[List[str]] = None,
        location: str = "",
        embedding: Optional[List[float]] = None
    ) -> int:
        chars_json = json.dumps(characters or [])
        emb_json = json.dumps(embedding or [])
        
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO memories (campaign_id, turn_number, content, importance, event_type, characters_json, location, embedding_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (campaign_id, turn_number, content, importance, event_type, chars_json, location, emb_json)
        )
        self.conn.commit()
        return cursor.lastrowid

    def update_memory_embedding(self, memory_id: int, embedding: List[float]):
        emb_json = json.dumps(embedding or [])
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE memories SET embedding_json = ? WHERE id = ?",
            (emb_json, memory_id)
        )
        self.conn.commit()

    def search_memories(
        self,
        campaign_id: str,
        query_embedding: Optional[List[float]] = None,
        top_k: int = 5,
        importance_min: float = 0.0,
        character_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM memories WHERE campaign_id = ? AND importance >= ?"
        params = [campaign_id, importance_min]
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            mem_dict = dict(row)
            mem_dict["characters"] = json.loads(mem_dict.get("characters_json") or "[]")
            emb = json.loads(mem_dict.get("embedding_json") or "[]")
            mem_dict["embedding"] = emb
            
            if character_filter:
                chars = [c.lower() for c in mem_dict["characters"]]
                if character_filter.lower() not in chars:
                    continue
            
            score = mem_dict["importance"]
            if query_embedding and emb:
                sim = cosine_similarity(query_embedding, emb)
                score = (0.7 * sim) + (0.3 * mem_dict["importance"])
            
            mem_dict["similarity_score"] = score
            memories.append(mem_dict)
            
        memories.sort(key=lambda m: m["similarity_score"], reverse=True)
        return memories[:top_k]

    def get_recent_memories(self, campaign_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM memories WHERE campaign_id = ? ORDER BY turn_number DESC LIMIT ?",
            (campaign_id, limit)
        )
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["characters"] = json.loads(d.get("characters_json") or "[]")
            result.append(d)
        return result
