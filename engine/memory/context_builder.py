from typing import List, Dict, Any, Optional
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore
from engine.providers.base import BaseLLMProvider

class ContextBuilder:
    def __init__(self, repo: Repository, vector_store: VectorStore, provider: BaseLLMProvider):
        self.repo = repo
        self.vector_store = vector_store
        self.provider = provider

    def build_prompt_context(
        self,
        campaign_id: str,
        user_input: str,
        short_term_history: List[Dict[str, str]]
    ) -> str:
        # 1. Structured World State
        world_state = self.repo.get_latest_world_state(campaign_id) or {}
        characters = self.repo.get_characters(campaign_id)
        quests = self.repo.get_quests(campaign_id)
        campaign = self.repo.get_campaign(campaign_id) or {}

        # 2. RAG Semantic Retrieval for Long-Term Memory
        query_emb = self.provider.generate_embedding(user_input) if user_input else None
        rag_memories = self.vector_store.search_memories(
            campaign_id=campaign_id,
            query_embedding=query_emb,
            top_k=5,
            importance_min=0.2
        )

        # Build prompt sections
        lines = []

        lines.append("=== ESTADO ESTRUTURADO DO MUNDO ===")
        lines.append(f"Reino: {world_state.get('kingdom_name', 'N/A')}")
        lines.append(f"Imperador: {world_state.get('ruler_name', 'N/A')} (Raça: {world_state.get('race', 'Humano')})")
        lines.append(f"Recursos: Ouro={world_state.get('gold', 5000)} | População={world_state.get('population', 10000)} | Poder Militar={world_state.get('military', 1000)} | Felicidade={world_state.get('happiness', '70%')}")
        lines.append(f"Religião Oficial: {world_state.get('religion', 'Nenhuma')}")
        lines.append("")

        if characters:
            lines.append("=== PERSONAGENS & RECONHECIMENTO ===")
            for c in characters:
                status = "Vivo" if c["is_alive"] else "Morto"
                lines.append(f"- {c['name']} ({c['role']}) | Local: {c['location']} | Status: {status} | Relacionamento: {c['relationship_with_player']}")
            lines.append("")

        if quests:
            lines.append("=== QUESTS EM ANDAMENTO ===")
            for q in quests:
                lines.append(f"- [{q['status'].upper()}] {q['title']}: {q['description']}")
            lines.append("")

        if campaign.get("summary"):
            lines.append("=== RESUMO HISTÓRICO DA CAMPANHA ===")
            lines.append(campaign["summary"])
            lines.append("")

        if rag_memories:
            lines.append("=== MEMÓRIAS EPISÓDICAS RELEVANTES (RAG) ===")
            for m in rag_memories:
                lines.append(f"- [Turno {m['turn_number']}] (Importância {m['importance']:.2f}): {m['content']}")
            lines.append("")

        if short_term_history:
            lines.append("=== ÚLTIMAS INTERAÇÕES RECENTES ===")
            for item in short_term_history[-4:]:
                lines.append(f"Jogador: {item.get('user', '')}")
                lines.append(f"Narrador: {item.get('narrative', '')}")
            lines.append("")

        lines.append("=== AÇÃO ATUAL DO JOGADOR ===")
        lines.append(user_input)

        return "\n".join(lines)
