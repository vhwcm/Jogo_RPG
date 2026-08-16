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
        world_state = self.repo.get_latest_world_state(campaign_id) or {}
        characters = self.repo.get_characters(campaign_id)
        quests = self.repo.get_quests(campaign_id)
        campaign = self.repo.get_campaign(campaign_id) or {}

        items = self.repo.get_campaign_items(campaign_id)
        tasks = self.repo.get_campaign_tasks(campaign_id)
        allies = self.repo.get_campaign_allies(campaign_id)

        rag_memories = []
        recent_mems = self.vector_store.get_recent_memories(campaign_id, limit=1)
        if recent_mems and user_input:
            query_emb = self.provider.generate_embedding(user_input)
            rag_memories = self.vector_store.search_memories(
                campaign_id=campaign_id,
                query_embedding=query_emb,
                top_k=5,
                importance_min=0.2
            )

        lines = []

        lines.append("=== ESTADO ESTRUTURADO DO MUNDO ===")
        lines.append(f"Reino: {world_state.get('kingdom_name', 'N/A')}")
        lines.append(f"Imperador: {world_state.get('ruler_name', 'N/A')} (Raça: {world_state.get('race', 'Humano')})")
        lines.append(f"Recursos: Ouro={world_state.get('gold', 5000)} | População={world_state.get('population', 10000)} | Poder Militar={world_state.get('military', 1000)} | Felicidade={world_state.get('happiness', '70%')}")
        lines.append(f"Religião Oficial: {world_state.get('religion', 'Nenhuma')}")
        lines.append("")

        if items:
            lines.append("=== ESTRUTURAS, CONSTRUÇÕES & ATIVOS DO REINO (PATRIMÔNIO/ITENS/CRIATURAS) ===")
            for it in items:
                attr_str = ", ".join(f"{k}: {v}" for k, v in it.get("atributos", {}).items())
                attr_fmt = f" | Atributos: [{attr_str}]" if attr_str else ""
                lines.append(f"- [{it['categoria'].upper()}] {it['nome']} (ID: {it['id']}): {it.get('descricao', '')}{attr_fmt}")
            lines.append("")

        if tasks:
            lines.append("=== TAREFAS ATIVAS & INCIDENTES (TASKS) ===")
            for tk in tasks:
                prog = f"{tk['progresso']}%" if tk.get('progresso') is not None else "N/A"
                inc = " [INCIDENTE DINÂMICO]" if tk.get('is_incidente_dinamico') else ""
                dur = f" | Duração: {tk['duracao_estimada']}" if tk.get('duracao_estimada') else ""
                lines.append(f"- [{tk['status'].upper()}]{inc} {tk['titulo']} (ID: {tk['id']}) | Progresso: {prog}{dur} - {tk.get('descricao', '')}")
            lines.append("")

        if allies:
            lines.append("=== IMPÉRIOS E DIPLOMACIA (ALIADOS/RIVAIS) ===")
            for al in allies:
                lines.append(f"- {al['nome']} (Rei: {al['rei']}) | Status: {al['status_diplomatico']} | Relação: {al['relacionamento']}/100 | Poder Militar: {al.get('poder_militar', 'N/A')} | População: {al.get('populacao', 'N/A')}")
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
