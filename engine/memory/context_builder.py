from typing import List, Dict, Any, Optional
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore
from engine.providers.base import BaseLLMProvider
from engine.domain.models import EvaluationResult, AVAILABLE_RACES

class ContextBuilder:
    def __init__(self, repo: Repository, vector_store: VectorStore, provider: BaseLLMProvider):
        self.repo = repo
        self.vector_store = vector_store
        self.provider = provider

    def build_prompt_context(
        self,
        campaign_id: str,
        user_input: str,
        short_term_history: List[Dict[str, str]],
        evaluation_result: Optional[EvaluationResult] = None
    ) -> str:
        world_state = self.repo.get_latest_world_state(campaign_id) or {}
        characters = self.repo.get_characters(campaign_id)
        quests = self.repo.get_quests(campaign_id)
        campaign = self.repo.get_campaign(campaign_id) or {}

        items = self.repo.get_campaign_items(campaign_id)
        tasks = self.repo.get_campaign_tasks(campaign_id)
        allies = self.repo.get_campaign_allies(campaign_id)
        periodic_events = self.repo.get_periodic_events(campaign_id)

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

        current_day = world_state.get("current_day", 1)
        days_passed = evaluation_result.dias_passados if evaluation_result else 1
        new_day = current_day + days_passed

        player_race = world_state.get("race", "Humano")

        lines.append("=== CALENDÁRIO E TEMPO DO REINO ===")
        lines.append(f"Dia Atual: {current_day} -> Novo Dia: {new_day} (+{days_passed} dias transcorridos nesta ação)")
        lines.append("")

        lines.append("=== ESTADO ESTRUTURADO DO MUNDO ===")
        lines.append(f"Reino: {world_state.get('kingdom_name', 'N/A')}")
        lines.append(f"Imperador: {world_state.get('ruler_name', 'N/A')} (Raça: {player_race})")
        lines.append(f"Recursos Atuais: Ouro={world_state.get('gold', 5000)} | População={world_state.get('population', 10000)} | Poder Militar={world_state.get('military', 1000)} | Felicidade={world_state.get('happiness', '70%')}")
        lines.append(f"Religião Oficial: {world_state.get('religion', 'Nenhuma')}")
        lines.append("")

        lines.append("=== LORE & SISTEMA DE RAÇAS DO UNIVERSO ===")
        lines.append(f"Raça do Soberano / Reino Atual: {player_race}")
        lines.append(f"Todas as Raças Disponíveis no Mundo: {', '.join(AVAILABLE_RACES)}")
        lines.append("Diretriz de Criação de Impérios / Reinos Inimigos ou Vizinhos: Ao introduzir, narrar ou registrar um novo império estrangeiro, facção rival ou aliado (via narrativa ou action 'add_ally'), atribua OBRIGATORIAMENTE uma das raças disponíveis acima e especifique sua raça na narrativa e no payload do aliado. O reino do próprio jogador ('node_capital') nunca é um aliado nem reino vizinho; nunca emita 'add_ally' ou nó de reino vizinho para o próprio reino.")
        lines.append("")

        if evaluation_result:
            lines.append("=== DIRETRIZES OBRIGATÓRIAS DO ÁRBITRO DE REGRAS ===")
            lines.append(f"Intenção Reconhecida: {evaluation_result.intencao_detectada}")
            if evaluation_result.opcoes_selecionadas:
                lines.append(f"Opções Selecionadas: {evaluation_result.opcoes_selecionadas}")
            lines.append(f"Variação Exata de Recursos a Aplicar em status_reino: Delta Ouro={evaluation_result.delta_dinheiro}, Delta Militar={evaluation_result.delta_poder_militar}")
            lines.append(f"Tipo de Execução: {evaluation_result.tipo_execucao.upper()}")
            if evaluation_result.tipo_execucao == "longo_prazo":
                lines.append(f"REGRA INVIOLÁVEL: Esta é uma missão/tarefa de longo prazo ({evaluation_result.dias_duracao_tarefa or 'vários'} dias). Narre apenas o envio, mobilização ou início da obra. NÃO conclua o objetivo no mesmo turno. Crie ou atualize a task correspondente.")
            if evaluation_result.eventos_periodicos_disparados:
                lines.append("EVENTOS PERIÓDICOS DISPARADOS:")
                for ev in evaluation_result.eventos_periodicos_disparados:
                    lines.append(f"- Evento '{ev.get('titulo')}': {ev.get('descricao', '')} (Efeito: {ev.get('efeito')})")
            if evaluation_result.diretrizes_narrador:
                lines.append(f"Instruções Específicas: {evaluation_result.diretrizes_narrador}")
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
                dur = f" | Estimativa: {tk['dias_estimados']} dias" if tk.get('dias_estimados') else ""
                lines.append(f"- [{tk['status'].upper()}]{inc} {tk['titulo']} (ID: {tk['id']}) | Progresso: {prog}{dur} (Iniciado no Dia {tk.get('dia_inicio', 1)}) - {tk.get('descricao', '')}")
            lines.append("")

        if periodic_events:
            lines.append("=== EVENTOS PERIÓDICOS E CRONOGRAMA DO REINO ===")
            for pe in periodic_events:
                lines.append(f"- [{pe['status'].upper()}] {pe['titulo']}: Intervalo de {pe['intervalo_dias']} dias | Próximo Disparo: Dia {pe['proximo_disparo_dia']} | Efeito: {pe.get('efeito')}")
            lines.append("")

        if allies:
            lines.append("=== IMPÉRIOS E DIPLOMACIA (ALIADOS/RIVAIS) ===")
            for al in allies:
                lines.append(f"- {al['nome']} (Soberano: {al['rei']} | Raça: {al.get('raca', 'Humano')}) | Status: {al['status_diplomatico']} | Relação: {al['relacionamento']}/100 | Poder Militar: {al.get('poder_militar', 'N/A')} | População: {al.get('populacao', 'N/A')}")
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
