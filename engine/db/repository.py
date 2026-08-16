import json
import sqlite3
from typing import List, Dict, Any, Optional

class Repository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_campaign(self, campaign_id: str, name: str) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO campaigns (id, name, created_at, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (campaign_id, name)
        )
        self.conn.commit()
        return {"id": campaign_id, "name": name, "summary": ""}

    def touch_campaign(self, campaign_id: str):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE campaigns SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (campaign_id,))
        self.conn.commit()

    def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_campaigns(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.id, c.name, c.created_at, c.updated_at, c.summary,
                   w.kingdom_name, w.ruler_name, w.race, w.turn_number
            FROM campaigns c
            LEFT JOIN world_state w ON w.campaign_id = c.id
                 AND w.turn_number = (
                     SELECT MAX(ws.turn_number) FROM world_state ws WHERE ws.campaign_id = c.id
                 )
            ORDER BY c.updated_at DESC, c.created_at DESC, c.rowid DESC
        """)
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            if d.get("turn_number") is None:
                d["turn_number"] = 0
            result.append(d)
        return result

    def update_campaign_summary(self, campaign_id: str, summary: str):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE campaigns SET summary = ? WHERE id = ?", (summary, campaign_id))
        self.conn.commit()

    def delete_campaign(self, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def save_world_state(
        self,
        campaign_id: str,
        turn_number: int,
        kingdom_name: str,
        ruler_name: str,
        race: str,
        gold: int,
        military: int,
        happiness: str,
        religion: str,
        population: int = 10000,
        raw_state_json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        raw_json = json.dumps(raw_state_json or {})
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO world_state (campaign_id, turn_number, kingdom_name, ruler_name, race, gold, population, military, happiness, religion, raw_state_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (campaign_id, turn_number, kingdom_name, ruler_name, race, gold, population, military, happiness, religion, raw_json)
        )
        self.conn.commit()
        return {
            "campaign_id": campaign_id,
            "turn_number": turn_number,
            "kingdom_name": kingdom_name,
            "ruler_name": ruler_name,
            "race": race,
            "gold": gold,
            "population": population,
            "military": military,
            "happiness": happiness,
            "religion": religion,
            "raw_state": raw_state_json or {}
        }

    def get_latest_world_state(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM world_state WHERE campaign_id = ? ORDER BY turn_number DESC LIMIT 1",
            (campaign_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["raw_state"] = json.loads(res.get("raw_state_json") or "{}")
        return res

    def get_world_state_at_turn(self, campaign_id: str, turn_number: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM world_state WHERE campaign_id = ? AND turn_number = ?",
            (campaign_id, turn_number)
        )
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        res["raw_state"] = json.loads(res.get("raw_state_json") or "{}")
        return res

    def get_world_state_history(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM world_state WHERE campaign_id = ? ORDER BY turn_number ASC",
            (campaign_id,)
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            res = dict(row)
            res["raw_state"] = json.loads(res.get("raw_state_json") or "{}")
            result.append(res)
        return result

    def delete_world_states_after_turn(self, campaign_id: str, turn_number: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM world_state WHERE campaign_id = ? AND turn_number > ?",
            (campaign_id, turn_number)
        )
        self.conn.commit()

    def delete_memories_after_turn(self, campaign_id: str, turn_number: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM memories WHERE campaign_id = ? AND turn_number > ?",
            (campaign_id, turn_number)
        )
        self.conn.commit()

    def upsert_character(
        self,
        character_id: str,
        campaign_id: str,
        name: str,
        role: str = "NPC",
        location: str = "Valdrin",
        is_alive: bool = True,
        relationship: int = 0,
        knowledge: Optional[List[str]] = None
    ):
        cursor = self.conn.cursor()
        know_json = json.dumps(knowledge or [])
        cursor.execute(
            """
            INSERT INTO characters (id, campaign_id, name, role, location, is_alive, relationship_with_player, knowledge_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                role=excluded.role,
                location=excluded.location,
                is_alive=excluded.is_alive,
                relationship_with_player=excluded.relationship_with_player,
                knowledge_json=excluded.knowledge_json
            """,
            (character_id, campaign_id, name, role, location, 1 if is_alive else 0, relationship, know_json)
        )
        self.conn.commit()

    def get_characters(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE campaign_id = ?", (campaign_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["is_alive"] = bool(d["is_alive"])
            d["knowledge"] = json.loads(d.get("knowledge_json") or "[]")
            result.append(d)
        return result

    def delete_character(self, character_id: str, campaign_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM characters WHERE id = ? AND campaign_id = ?", (character_id, campaign_id))
        self.conn.commit()

    def upsert_quest(self, quest_id: str, campaign_id: str, title: str, description: str, status: str = "active", objective: str = ""):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO quests (id, campaign_id, title, description, status, objective)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                description=excluded.description,
                status=excluded.status,
                objective=excluded.objective
            """,
            (quest_id, campaign_id, title, description, status, objective)
        )
        self.conn.commit()

    def get_quests(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quests WHERE campaign_id = ?", (campaign_id,))
        return [dict(r) for r in cursor.fetchall()]

    def delete_quest(self, quest_id: str, campaign_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM quests WHERE id = ? AND campaign_id = ?", (quest_id, campaign_id))
        self.conn.commit()

    def upsert_item(self, item_id: str, campaign_id: str, name: str, owner: str = "player", quantity: int = 1, properties: Optional[Dict[str, Any]] = None):
        cursor = self.conn.cursor()
        props_json = json.dumps(properties or {})
        cursor.execute(
            """
            INSERT INTO items (id, campaign_id, name, owner, quantity, properties_json)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                owner=excluded.owner,
                quantity=excluded.quantity,
                properties_json=excluded.properties_json
            """,
            (item_id, campaign_id, name, owner, quantity, props_json)
        )
        self.conn.commit()

    def get_items(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items WHERE campaign_id = ?", (campaign_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["properties"] = json.loads(d.get("properties_json") or "{}")
            result.append(d)
        return result

    def delete_item(self, item_id: str, campaign_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ? AND campaign_id = ?", (item_id, campaign_id))
        self.conn.commit()

    def upsert_location(self, location_id: str, campaign_id: str, name: str, description: str = "", control_faction: str = "Player"):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO locations (id, campaign_id, name, description, control_faction)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                control_faction=excluded.control_faction
            """,
            (location_id, campaign_id, name, description, control_faction)
        )
        self.conn.commit()

    def get_locations(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM locations WHERE campaign_id = ?", (campaign_id,))
        return [dict(r) for r in cursor.fetchall()]

    def upsert_campaign_item(
        self,
        item_id: str,
        campaign_id: str,
        nome: str,
        categoria: str = "outro",
        descricao: str = "",
        atributos: Optional[Dict[str, Any]] = None,
        adquirido_no_turno: int = 1
    ):
        cursor = self.conn.cursor()
        attr_json = json.dumps(atributos or {})
        cursor.execute(
            """
            INSERT INTO campaign_items (id, campaign_id, nome, categoria, descricao, atributos_json, adquirido_no_turno)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nome=excluded.nome,
                categoria=excluded.categoria,
                descricao=excluded.descricao,
                atributos_json=excluded.atributos_json,
                adquirido_no_turno=excluded.adquirido_no_turno
            """,
            (item_id, campaign_id, nome, categoria, descricao, attr_json, adquirido_no_turno)
        )
        self.conn.commit()

    def get_campaign_items(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaign_items WHERE campaign_id = ? ORDER BY adquirido_no_turno ASC, id ASC", (campaign_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["atributos"] = json.loads(d.get("atributos_json") or "{}")
            result.append(d)
        return result

    def delete_campaign_item(self, item_id: str, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM campaign_items WHERE (id = ? OR nome = ?) AND campaign_id = ?", (item_id, item_id, campaign_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def upsert_campaign_task(
        self,
        task_id: str,
        campaign_id: str,
        titulo: str,
        descricao: str = "",
        status: str = "em_andamento",
        progresso: Optional[int] = None,
        duracao_estimada: Optional[str] = None,
        objetivo_esperado: Optional[str] = None,
        is_incidente: bool = False,
        criada_no_turno: int = 1
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO campaign_tasks (id, campaign_id, titulo, descricao, status, progresso, duracao_estimada, objetivo_esperado, is_incidente, criada_no_turno)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                titulo=excluded.titulo,
                descricao=excluded.descricao,
                status=excluded.status,
                progresso=excluded.progresso,
                duracao_estimada=excluded.duracao_estimada,
                objetivo_esperado=excluded.objetivo_esperado,
                is_incidente=excluded.is_incidente,
                criada_no_turno=excluded.criada_no_turno
            """,
            (task_id, campaign_id, titulo, descricao, status, progresso, duracao_estimada, objetivo_esperado, 1 if is_incidente else 0, criada_no_turno)
        )
        self.conn.commit()

    def get_campaign_tasks(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaign_tasks WHERE campaign_id = ? ORDER BY criada_no_turno ASC, id ASC", (campaign_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["is_incidente_dinamico"] = bool(d.get("is_incidente", 0))
            result.append(d)
        return result

    def delete_campaign_task(self, task_id: str, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM campaign_tasks WHERE (id = ? OR titulo = ?) AND campaign_id = ?", (task_id, task_id, campaign_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def upsert_campaign_ally(
        self,
        ally_id: str,
        campaign_id: str,
        nome: str,
        rei: str,
        populacao: Any = "10000",
        poder_militar: Any = "1000",
        relacionamento: int = 50,
        status_diplomatico: str = "neutro",
        historico_notas: Optional[str] = None
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO campaign_allies (id, campaign_id, nome, rei, populacao, poder_militar, relacionamento, status_diplomatico, historico_notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nome=excluded.nome,
                rei=excluded.rei,
                populacao=excluded.populacao,
                poder_militar=excluded.poder_militar,
                relacionamento=excluded.relacionamento,
                status_diplomatico=excluded.status_diplomatico,
                historico_notas=excluded.historico_notas
            """,
            (ally_id, campaign_id, nome, rei, str(populacao), str(poder_militar), int(relacionamento), status_diplomatico, historico_notas)
        )
        self.conn.commit()

    def get_campaign_allies(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaign_allies WHERE campaign_id = ? ORDER BY relacionamento DESC, nome ASC", (campaign_id,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

    def delete_campaign_ally(self, ally_id: str, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM campaign_allies WHERE (id = ? OR nome = ?) AND campaign_id = ?", (ally_id, ally_id, campaign_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def upsert_map_node(
        self,
        node_id: str,
        campaign_id: str,
        label: str,
        node_type: str = "estrutura",
        emoji: str = "📍",
        x: float = 0.0,
        y: float = 0.0,
        status: str = "ativo",
        metadata: Optional[Dict[str, Any]] = None
    ):
        cursor = self.conn.cursor()
        meta_json = json.dumps(metadata or {})
        cursor.execute(
            """
            INSERT INTO campaign_map_nodes (id, campaign_id, label, node_type, emoji, x, y, status, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id, campaign_id) DO UPDATE SET
                label=excluded.label,
                node_type=excluded.node_type,
                emoji=excluded.emoji,
                x=excluded.x,
                y=excluded.y,
                status=excluded.status,
                metadata_json=excluded.metadata_json
            """,
            (node_id, campaign_id, label, node_type, emoji, float(x), float(y), status, meta_json)
        )
        self.conn.commit()

    def get_map_nodes(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaign_map_nodes WHERE campaign_id = ? ORDER BY created_at ASC, id ASC", (campaign_id,))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["metadata"] = json.loads(d.get("metadata_json") or "{}")
            result.append(d)
        return result

    def delete_map_node(self, node_id: str, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM campaign_map_edges WHERE campaign_id = ? AND (source_node_id = ? OR target_node_id = ?)",
            (campaign_id, node_id, node_id)
        )
        cursor.execute("DELETE FROM campaign_map_nodes WHERE (id = ? OR label = ?) AND campaign_id = ?", (node_id, node_id, campaign_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def upsert_map_edge(
        self,
        edge_id: str,
        campaign_id: str,
        source_node_id: str,
        target_node_id: str,
        edge_type: str = "estrada",
        descricao: str = ""
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO campaign_map_edges (id, campaign_id, source_node_id, target_node_id, edge_type, descricao)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id, campaign_id) DO UPDATE SET
                source_node_id=excluded.source_node_id,
                target_node_id=excluded.target_node_id,
                edge_type=excluded.edge_type,
                descricao=excluded.descricao
            """,
            (edge_id, campaign_id, source_node_id, target_node_id, edge_type, descricao)
        )
        self.conn.commit()

    def get_map_edges(self, campaign_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaign_map_edges WHERE campaign_id = ? ORDER BY created_at ASC, id ASC", (campaign_id,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

    def delete_map_edge(self, edge_id: str, campaign_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM campaign_map_edges WHERE id = ? AND campaign_id = ?", (edge_id, campaign_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_map_edge_between(self, campaign_id: str, source_node_id: str, target_node_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            DELETE FROM campaign_map_edges 
            WHERE campaign_id = ? AND (
                (source_node_id = ? AND target_node_id = ?) OR 
                (source_node_id = ? AND target_node_id = ?)
            )
            """,
            (campaign_id, source_node_id, target_node_id, target_node_id, source_node_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
