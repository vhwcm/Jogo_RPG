import uuid
import math
import concurrent.futures
from typing import Dict, Any, List, Optional, Union, Tuple
from engine.db.schema import init_db, get_connection
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore
from engine.providers.base import BaseLLMProvider
from engine.providers.factory import LLMFactory
from engine.memory.context_builder import ContextBuilder
from engine.memory.importance import calculate_importance
from engine.memory.summarizer import CampaignSummarizer
from engine.domain.models import KingdomStatus, TurnResponse, CampaignInfo, Item, Task, ImperioAliado, GameAction, MapNode, MapEdge, PeriodicEvent, EvaluationResult
from engine.domain.evaluator import ActionEvaluator
from engine.domain.formula_evaluator import calculate_event_effect
from engine.utils import generate_fallback_embedding
import config

GAME_MASTER_SYSTEM_INSTRUCTION = """
VOCÊ É O CONSELHEIRO REAL E GAME MASTER EM UM RPG DE ESTRATÉGIA MEDIEVAL/FANTASIA.
SUA MISSÃO É NARRAR EVENTOS, GERENCIAR OS STATUS DO REINO E EVOLUIR A HISTÓRIA.

### REGRAS DE FORMATAÇÃO (OBRIGATÓRIO)
Sua resposta deve ser APENAS um JSON válido seguindo exatamente este esquema:
{
  "aventura": "Texto narrativo épico (descreva o cenário, o conflito e apresente SEMPRE 3 opções numeradas de ação ao final em linhas separadas).",
  "clima": "aventura | calmo | frenetico | harmonia | desenvolvimento | desespero (Escolha obrigatoriamente a opção que melhor se alinha ao tom e ambiente narrativo do contexto atual)",
  "opcoes": [
    {
      "texto": "1. Primeira opção de ação",
      "impacto": { "dinheiro": -500, "poder_militar": 0 }
    },
    {
      "texto": "2. Segunda opção de ação",
      "impacto": { "dinheiro": -300, "poder_militar": 200 }
    },
    {
      "texto": "3. Terceira opção de ação (ação com resultado incerto ou combate)",
      "impacto": { "dinheiro": null, "poder_militar": null }
    }
  ],
  "status_reino": {
    "nome_reino": "Nome do Reino (String)",
    "imperador": "Nome do Jogador (String)",
    "dinheiro": 5000 (Inteiro, sem pontos),
    "populacao": 10000 (Inteiro, sem pontos),
    "religião": "Nome da Religião (String)",
    "poder_militar": 1000 (Inteiro),
    "felicidade": "70%" (String com %)
  },
  "actions": [
    {
      "action_type": "add_item | remove_item | add_structure | remove_structure | add_kingdom_asset | remove_kingdom_asset | create_task | update_task | create_periodic_event | update_periodic_event | remove_periodic_event | add_ally | update_ally | add_map_node | update_map_node | remove_map_node | connect_map_nodes | disconnect_map_nodes",
      "payload": { ... }
    }
  ]
}

### SISTEMA DE ACTIONS SUPORTADAS
Sempre que eventos da história concederem itens, criaturas ou artefatos, ou quando o soberano construir/estabelecer estruturas e postos do reino, ou iniciar/atualizar tarefas de longo prazo, ou criar/atualizar eventos periódicos e tributos recorrentes, ou firmar/mudar relações diplomáticas, ou descobrir novos territórios/biomas no mapa, emita itens na lista "actions":
1. add_item / add_structure / add_kingdom_asset:
   payload: {"id": "id_unico_str", "nome": "Nome do Item/Estrutura/Criatura", "categoria": "estrutura|santuario|posto_avancado|fortificacao|monumento|criatura|artefato|recurso|equipamento|outro", "descricao": "...", "atributos": {"chave": "valor"}}
2. remove_item / remove_structure / remove_kingdom_asset:
   payload: {"id": "id_do_item_ou_estrutura"}
3. create_task:
   payload: {"id": "id_da_task", "titulo": "Título da Missão", "descricao": "...", "status": "em_andamento|concluida|falhou|cancelada", "progresso": 0_a_100, "dia_inicio": 1, "dias_estimados": 30, "objetivo_esperado": "...", "is_incidente_dinamico": true_ou_false}
4. update_task:
   payload: {"id": "id_da_task", "status": "em_andamento|concluida|falhou|cancelada", "progresso": 0_a_100, "descricao": "..."}
5. create_periodic_event:
   payload: {"id": "id_do_evento", "titulo": "Tributo do Império Vizinho", "descricao": "...", "intervalo_dias": 45, "proximo_disparo_dia": 45, "efeito": {"dinheiro": 500}, "status": "ativo"}
6. update_periodic_event:
   payload: {"id": "id_do_evento", "status": "ativo|pausado|cancelado", "proximo_disparo_dia": 90}
7. remove_periodic_event:
   payload: {"id": "id_do_evento"}
8. add_ally:
   payload: {"id": "id_do_aliado", "nome": "Nome do Reino", "rei": "Nome do Soberano", "raca": "Humano|Elfo|Anão|Orc|Centauro|Demônio|Djinn|Dragão|Elemental|Fauno|Gnomo|Goblin|Leprechaun|Mago|Morto Vivo|Rinoceronte|Sereia|Trol|Vampiro", "populacao": 25000, "poder_militar": 3000, "relacionamento": -100_a_100, "status_diplomatico": "hostil|neutro|amigavel|aliado|vassalo", "historico_notas": "..."}
9. update_ally:
   payload: {"id": "id_do_aliado", "raca": "...", "relacionamento": -100_a_100, "status_diplomatico": "...", "historico_notas": "..."}
10. add_map_node:
   payload: {"id": "id_do_node", "label": "Nome do Ponto no Mapa", "node_type": "bioma|tropa|reino_vizinho|estrutura|santuario|fortificacao|mina|porto|ruina|vila", "emoji": "🌲|⚔️|👑|🏛️|✨|🛡️|⛏️|⚓|🏚️|🌾", "status": "ativo|descoberto|hostil|em_marcha", "metadata": {"tropas": 150, "dono": "Reino", "perigo": "Baixo"}, "connect_to": "id_do_node_pai_opcional", "edge_type": "estrada|fronteira|rota"}
11. update_map_node:
   payload: {"id": "id_do_node", "status": "...", "metadata": { ... }}
12. remove_map_node:
   payload: {"id": "id_do_node"}
13. connect_map_nodes:
   payload: {"source_node_id": "id_origem", "target_node_id": "id_destino", "edge_type": "estrada|fronteira|rota", "descricao": "..."}
14. disconnect_map_nodes:
   payload: {"source_node_id": "id_origem", "target_node_id": "id_destino"}

### REGRAS CRÍTICAS DE JOGO
1. **Religião Inicial:** Todo reino SEMPRE começa SEM religião oficial ("Nenhuma"). No Turno 1 (início da campanha), a PRIMEIRA pergunta/decisão apresentada ao Imperador DEVE ser obrigatoriamente a escolha ou definição da religião/doutrina do reino.
2. **Respeito aos Status do Árbitro:** Os deltas de dinheiro e poder militar calculados pelo árbitro de regras DEVEM ser respeitados no status_reino.
3. **Não-Imediatismo de Quests e Construções:** NUNCA conclua tarefas ou construções de longo prazo no mesmo turno em que foram iniciadas. Narre a partida das tropas, o início da escavação ou a preparação dos operários, cadastrando a task com o prazo estimado em dias.
4. **Clima Musical:** Defina o campo 'clima' dinamicamente conforme a atmosfera da cena.
5. **Tom Majestic:** Use linguagem formal e imersiva ("Vossa Majestade", "Sua Graça").
6. **Sem Emojis no Texto:** Mantenha a narrativa literária, elegante e imersiva. NÃO inclua emojis no texto narrativo.
7. **Opções e Prévias OBRIGATÓRIAS:** Você DEVE sempre incluir o campo 'opcoes' como uma lista com exatamente 3 objetos. Cada objeto possui 'texto' e 'impacto' com 'dinheiro' e 'poder_militar'.
8. **Actions Modulares:** Emita ações na chave 'actions' quando itens forem obtidos/perdidos, missões iniciadas/atualizadas, eventos periódicos configurados ou elementos do mapa forem descobertos/alterados.
9. **Sistema de Raças & Criação de Novos Impérios Inimigos / Vizinhos:**
   - O universo do jogo possui 19 raças canônicas: Humano, Elfo, Anão, Orc, Centauro, Demônio, Djinn, Dragão, Elemental, Fauno, Gnomo, Goblin, Leprechaun, Mago, Morto Vivo, Rinoceronte, Sereia, Trol, Vampiro.
   - O reino do jogador possui sua raça informada no contexto. Respeite suas características e cultura.
   - Ao introduzir, gerar ou interagir com um NOVO império inimigo, reino rival, vizinho ou facção externa (na narrativa ou via action 'add_ally'), você DEVE OBRIGATORIAMENTE escolher uma das raças canônicas disponíveis e preencher o campo 'raca' no payload da action 'add_ally'.
10. **Grafo e Mapa do Reino:** O reino do jogador e sua capital ('node_capital') já residem centralizados no mapa (x=0, y=0). NUNCA emita 'add_ally' para o próprio reino do jogador e NUNCA emita 'add_map_node' com node_type 'reino_vizinho' ou 'capital' para o reino ou capital do jogador.
"""

class GameEngine:
    def __init__(self, db_path: str = "", provider_name: Optional[str] = None):
        self.db_path = db_path or config.DB_PATH
        self.conn = init_db(self.db_path)
        self.repo = Repository(self.conn)
        self.vector_store = VectorStore(self.conn)
        self._provider = LLMFactory.get_provider(provider_name)
        self.evaluator = ActionEvaluator(self._provider)
        self.context_builder = ContextBuilder(self.repo, self.vector_store, self._provider)
        self.summarizer = CampaignSummarizer(self._provider)
        self.short_term_memories: Dict[str, List[Dict[str, str]]] = {}
        self._bg_executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

    @property
    def provider(self) -> BaseLLMProvider:
        return self._provider

    @provider.setter
    def provider(self, val: BaseLLMProvider):
        self._provider = val
        if hasattr(self, "evaluator") and self.evaluator:
            self.evaluator.provider = val
        if hasattr(self, "context_builder") and self.context_builder:
            self.context_builder.provider = val
        if hasattr(self, "summarizer") and self.summarizer:
            self.summarizer.provider = val

    def _get_short_term_memory(self, campaign_id: str) -> List[Dict[str, str]]:
        if campaign_id not in self.short_term_memories:
            recent_mems = self.vector_store.get_recent_memories(campaign_id, limit=10)
            mem_list = []
            for m in reversed(recent_mems):
                mem_list.append({"user": f"Turno {m['turn_number']}", "narrative": m["content"]})
            self.short_term_memories[campaign_id] = mem_list
        return self.short_term_memories[campaign_id]

    def create_campaign(
        self,
        campaign_name: str,
        ruler_name: str,
        kingdom_name: str,
        race: str,
        campaign_id: Optional[str] = None
    ) -> TurnResponse:
        campaign_id = campaign_id or str(uuid.uuid4())[:8]
        self.repo.create_campaign(campaign_id, campaign_name)
        self.short_term_memories[campaign_id] = []

        cap_id = "node_capital"
        forest_id = "node_floresta_ancestral"
        mount_id = "node_montanhas_ferro"
        plains_id = "node_campos_dourados"

        self.repo.upsert_map_node(
            node_id=cap_id,
            campaign_id=campaign_id,
            label=f"Capital {kingdom_name}",
            node_type="capital",
            emoji="🏰",
            x=0.0,
            y=0.0,
            status="ativo",
            size="mega",
            metadata={"dono": kingdom_name, "tipo": "Capital", "tropas": 500, "perigo": "Nenhum"}
        )
        self.repo.upsert_map_node(
            node_id=forest_id,
            campaign_id=campaign_id,
            label="Floresta Ancestral",
            node_type="bioma",
            emoji="🌲",
            x=0.0,
            y=-180.0,
            status="descoberto",
            size="grande",
            metadata={"tipo": "Floresta", "perigo": "Baixo", "recursos": "Madeira e Ervas"}
        )
        self.repo.upsert_map_node(
            node_id=mount_id,
            campaign_id=campaign_id,
            label="Montanhas de Ferro",
            node_type="bioma",
            emoji="⛰️",
            x=-190.0,
            y=110.0,
            status="descoberto",
            size="grande",
            metadata={"tipo": "Montanhas", "perigo": "Médio", "recursos": "Minério de Ferro"}
        )
        self.repo.upsert_map_node(
            node_id=plains_id,
            campaign_id=campaign_id,
            label="Campos Dourados",
            node_type="bioma",
            emoji="🌾",
            x=190.0,
            y=110.0,
            status="descoberto",
            size="grande",
            metadata={"tipo": "Planície Fértil", "perigo": "Nenhum", "recursos": "Alimento"}
        )
        self.repo.upsert_map_edge(
            edge_id="edge_cap_forest",
            campaign_id=campaign_id,
            source_node_id=cap_id,
            target_node_id=forest_id,
            edge_type="estrada",
            descricao="Estrada Real do Norte"
        )
        self.repo.upsert_map_edge(
            edge_id="edge_cap_mount",
            campaign_id=campaign_id,
            source_node_id=cap_id,
            target_node_id=mount_id,
            edge_type="estrada",
            descricao="Trilha dos Mineradores"
        )
        self.repo.upsert_map_edge(
            edge_id="edge_cap_plains",
            campaign_id=campaign_id,
            source_node_id=cap_id,
            target_node_id=plains_id,
            edge_type="estrada",
            descricao="Rota Comercial Agrícola"
        )
        neighbor_id = "node_reino_vizinho_solaria"
        self.repo.upsert_map_node(
            node_id=neighbor_id,
            campaign_id=campaign_id,
            label="Reino de Solária",
            node_type="reino_vizinho",
            emoji="👑",
            x=240.0,
            y=-140.0,
            status="ativo",
            size="mega",
            metadata={
                "rei": "Rainha Elis",
                "raca": "Elfo",
                "populacao": "25.000",
                "poder_militar": "2.500",
                "relacionamento": 50,
                "status_diplomatico": "neutro",
                "dono": "Reino de Solária",
                "detalhes": "Império Élfico vizinho com forte tradição diplomática e comercial."
            }
        )
        self.repo.upsert_map_edge(
            edge_id="edge_cap_solaria",
            campaign_id=campaign_id,
            source_node_id=cap_id,
            target_node_id=neighbor_id,
            edge_type="neutro",
            descricao="Tratado de Não-Agressão com Solária"
        )
        self.repo.upsert_periodic_event(
            event_id=f"recolhimento_impostos_{campaign_id}",
            campaign_id=campaign_id,
            titulo="Recolhimento de Impostos",
            intervalo_dias=30,
            proximo_disparo_dia=30,
            descricao="Arrecadação periódica de tributos reais baseada na população e no índice de felicidade do reino.",
            ultimo_disparo_dia=0,
            efeito={
                "tipo": "formula",
                "recurso": "dinheiro",
                "formula": "(populacao * 0.05) * (felicidade / 100)",
                "aliquota": 0.05,
                "descricao_calculo": "5% da população ajustado pela felicidade"
            },
            status="ativo",
            criado_no_turno=1
        )

        initial_user_prompt = (
            f"INÍCIO DE CAMPANHA: Criar reino '{kingdom_name}' de raça '{race}', governado pelo Imperador(a) '{ruler_name}'. "
            f"O reino começa sem religião oficial ('Nenhuma'). A PRIMEIRA pergunta/decisão apresentada ao Imperador "
            f"DEVE ser obrigatoriamente a definição da religião do reino (apresente 3 opções para o Imperador escolher a fé do reino)."
        )
        
        context = self.context_builder.build_prompt_context(campaign_id, initial_user_prompt, [])
        
        response_json = self.provider.generate_json(
            prompt=context,
            system_instruction=GAME_MASTER_SYSTEM_INSTRUCTION,
            temperature=0.4
        )

        turn_resp = self._process_turn_response(
            campaign_id,
            turn_number=1,
            ruler_name=ruler_name,
            kingdom_name=kingdom_name,
            race=race,
            user_action=initial_user_prompt,
            response_json=response_json
        )
        return turn_resp

    def execute_turn(self, campaign_id: str, player_action: str) -> TurnResponse:
        latest_state = self.repo.get_latest_world_state(campaign_id)
        if not latest_state:
            raise ValueError(f"Campanha '{campaign_id}' não encontrada ou sem estado inicial.")

        current_turn = latest_state["turn_number"] + 1
        ruler_name = latest_state["ruler_name"]
        kingdom_name = latest_state["kingdom_name"]
        race = latest_state["race"]

        st_memory = self._get_short_term_memory(campaign_id)
        previous_opcoes = latest_state.get("raw_state", {}).get("opcoes", [])
        if not previous_opcoes:
            previous_opcoes = self._extract_opcoes(latest_state.get("raw_state", {}), latest_state.get("raw_state", {}).get("aventura", ""))

        active_tasks = self.repo.get_campaign_tasks(campaign_id)
        active_periodic = self.repo.get_periodic_events(campaign_id)

        evaluation = self.evaluator.evaluate_action(
            campaign_id=campaign_id,
            action_text=player_action,
            previous_opcoes=previous_opcoes,
            current_world_state=latest_state,
            active_tasks=active_tasks,
            periodic_events=active_periodic
        )

        context = self.context_builder.build_prompt_context(campaign_id, player_action, st_memory, evaluation)

        response_json = self.provider.generate_json(
            prompt=context,
            system_instruction=GAME_MASTER_SYSTEM_INSTRUCTION,
            temperature=0.4
        )

        turn_resp = self._process_turn_response(
            campaign_id,
            turn_number=current_turn,
            ruler_name=ruler_name,
            kingdom_name=kingdom_name,
            race=race,
            user_action=player_action,
            response_json=response_json,
            evaluation_result=evaluation
        )
        return turn_resp

    def _infer_node_size(self, node_type: str, explicit_size: Optional[str] = None) -> str:
        if explicit_size and str(explicit_size).lower() in ["mega", "grande", "medio", "pequeno", "micro"]:
            return str(explicit_size).lower()
        nt = (node_type or "estrutura").lower()
        if nt in ["capital", "reino_vizinho", "imperio", "reino"]:
            return "mega"
        if nt in ["fortificacao", "exercito", "bioma", "floresta", "montanha", "cidade", "cidadela"]:
            return "grande"
        if nt in ["santuario", "estatua", "obra", "monumento", "totem", "altar", "ruina", "caverna", "rumor", "marco"]:
            return "pequeno"
        return "medio"

    def _is_placeable_asset(self, categoria: str, nome: str = "") -> bool:
        cat = (categoria or "").lower()
        nom = (nome or "").lower()
        placeable_cats = {
            "estrutura", "santuario", "obra", "monumento", "estatua",
            "fortificacao", "posto_avancado", "mina", "porto", "vila",
            "templo", "torre", "altar", "ruina", "fazenda", "quartel"
        }
        if cat in placeable_cats:
            return True
        keywords = [
            "santuario", "santuário", "estátua", "estatua", "obra",
            "monumento", "torre", "templo", "mina", "porto", "posto",
            "forte", "fortaleza", "altar", "totem", "fazenda", "oficina",
            "castelo", "muralha", "quarte", "cidadela"
        ]
        return any(k in nom for k in keywords)

    def _calculate_orbital_position(self, campaign_id: str, node_type: str, category: str = "") -> Tuple[float, float]:
        existing_nodes = self.repo.get_map_nodes(campaign_id)
        nt = (node_type or category or "estrutura").lower()
        is_orbital = nt in ["santuario", "estatua", "obra", "monumento", "totem", "altar", "templo", "posto_avancado", "torre"]
        
        if is_orbital:
            orbital_nodes = [
                n for n in existing_nodes 
                if n.get("id") != "node_capital" and math.hypot(float(n.get("x", 0.0)), float(n.get("y", 0.0))) <= 210.0
            ]
            idx = len(orbital_nodes)
            if idx < 6:
                radius = 95.0
                slots = 6
                angle = (idx * (2 * math.pi / slots)) + 0.25
            elif idx < 14:
                radius = 140.0
                slots = 8
                angle = ((idx - 6) * (2 * math.pi / slots)) + 0.45
            else:
                radius = 185.0
                slots = 12
                angle = ((idx - 14) * (2 * math.pi / slots)) + 0.15
            x = round(radius * math.cos(angle), 1)
            y = round(radius * math.sin(angle), 1)
            return float(x), float(y)
        else:
            count = len(existing_nodes)
            angle = (count * 0.897) + 0.3
            radius = 160.0 + ((count // 6) * 110.0)
            x = round(radius * math.cos(angle), 1)
            y = round(radius * math.sin(angle), 1)
            return float(x), float(y)

    def _is_player_kingdom_or_capital(self, text: str, kingdom_name: str, ruler_name: str = "") -> bool:
        if not text:
            return False
        t = str(text).strip().lower()
        k = (kingdom_name or "").strip().lower()
        r = (ruler_name or "").strip().lower()
        
        if t in ["node_capital", "capital", "capital_node"]:
            return True
        if k:
            if t == k:
                return True
            clean_t = t.replace("(", "").replace(")", "").strip()
            if clean_t in [k, f"capital {k}", f"{k} capital", f"capital de {k}", f"capital do {k}", f"capital da {k}", f"reino {k}", f"reino de {k}", f"reino do {k}", f"reino da {k}"]:
                return True
            t_normalized = t.replace("_", " ")
            if t_normalized in [k, f"capital {k}", f"{k} capital", f"node capital", f"node {k}"]:
                return True
            if t in [f"capital_{k}", f"node_{k}", f"node_capital_{k}"]:
                return True
        if r and (t == r or t in [f"rei {r}", f"rainha {r}", f"soberano {r}", f"imperador {r}"]):
            return True
        return False

    def _cleanup_duplicate_capital_nodes(self, campaign_id: str):
        latest_ws = self.repo.get_latest_world_state(campaign_id)
        kingdom_name = latest_ws.get("kingdom_name", "") if latest_ws else ""
        ruler_name = latest_ws.get("ruler_name", "") if latest_ws else ""
        
        nodes = self.repo.get_map_nodes(campaign_id)
        for n in nodes:
            nid = n.get("id")
            ntype = str(n.get("node_type", "")).lower()
            nlabel = n.get("label", "")
            if nid != "node_capital":
                if ntype == "capital" or self._is_player_kingdom_or_capital(nid, kingdom_name, ruler_name) or (ntype == "reino_vizinho" and self._is_player_kingdom_or_capital(nlabel, kingdom_name, ruler_name)):
                    self.repo.delete_map_node(nid, campaign_id)
        
        allies = self.repo.get_campaign_allies(campaign_id)
        for a in allies:
            aid = a.get("id")
            aname = a.get("nome", "")
            if self._is_player_kingdom_or_capital(aid, kingdom_name, ruler_name) or self._is_player_kingdom_or_capital(aname, kingdom_name, ruler_name):
                self.repo.delete_campaign_ally(aid, campaign_id)

    def apply_actions(self, campaign_id: str, actions: List[GameAction], turn_number: int, current_day: int = 1):
        latest_ws = self.repo.get_latest_world_state(campaign_id)
        kingdom_name = latest_ws.get("kingdom_name", "") if latest_ws else ""
        ruler_name = latest_ws.get("ruler_name", "") if latest_ws else ""

        for act in actions:
            action_type = act.action_type
            payload = act.payload or {}

            if action_type in ["add_item", "add_structure", "add_kingdom_asset"]:
                item_id = payload.get("id") or f"asset_{turn_number}_{str(uuid.uuid4())[:6]}"
                nome = payload.get("nome", "Ativo do Reino")
                default_cat = "estrutura" if "structure" in action_type else "outro"
                categoria = payload.get("categoria", default_cat)
                descricao = payload.get("descricao", "")
                atributos = payload.get("atributos", {})
                if not isinstance(atributos, dict):
                    atributos = {}

                is_placeable = bool(payload.get("posicionavel_no_mapa", False)) or bool(atributos.get("posicionavel_no_mapa", False)) or self._is_placeable_asset(categoria, nome)
                atributos["posicionavel_no_mapa"] = is_placeable
                if "tamanho_no" not in atributos:
                    node_type_infer = categoria if categoria in ["santuario", "fortificacao", "estrutura", "monumento", "estatua"] else "estrutura"
                    atributos["tamanho_no"] = self._infer_node_size(node_type_infer, payload.get("tamanho_no") or payload.get("size"))

                adquirido_no_turno = payload.get("adquirido_no_turno", turn_number)

                should_place = bool(payload.get("posicionar_no_mapa", False)) or (payload.get("x") is not None and payload.get("y") is not None)
                if should_place:
                    node_id = f"node_{item_id}"
                    node_type = payload.get("node_type", categoria if categoria in ["santuario", "fortificacao", "monumento", "estatua", "mina", "porto", "vila"] else "estrutura")
                    node_size = atributos.get("tamanho_no", "medio")
                    default_emojis = {
                        "capital": "🏰", "bioma": "🌲", "floresta": "🌲", "montanha": "⛰️",
                        "mina": "⛏️", "vila": "🌾", "fazenda": "🌾", "tropa": "⚔️",
                        "exercito": "⚔️", "patrulha": "🛡️", "reino_vizinho": "👑", "aliado": "👑",
                        "estrutura": "🏛️", "fortificacao": "🛡️", "posto_avancado": "🏹",
                        "santuario": "✨", "templo": "⛪", "porto": "⚓", "mar": "🌊",
                        "ruina": "🏚️", "caverna": "🕳️", "monumento": "🗿", "estatua": "🗿"
                    }
                    emoji = payload.get("emoji") or default_emojis.get(node_type.lower(), "🏛️")
                    px = payload.get("x")
                    py = payload.get("y")
                    if px is None or py is None:
                        px, py = self._calculate_orbital_position(campaign_id, node_type, categoria)
                    
                    self.repo.upsert_map_node(
                        node_id=node_id,
                        campaign_id=campaign_id,
                        label=nome,
                        node_type=node_type,
                        emoji=emoji,
                        x=float(px),
                        y=float(py),
                        status="ativo",
                        size=node_size,
                        metadata={"asset_id": item_id, "categoria": categoria, "dono": "Reino"}
                    )
                    if payload.get("connect_to_capital", True):
                        self.repo.upsert_map_edge(
                            edge_id=f"edge_cap_{node_id}",
                            campaign_id=campaign_id,
                            source_node_id="node_capital",
                            target_node_id=node_id,
                            edge_type="rota",
                            descricao=f"Acesso a {nome}"
                        )
                    atributos["no_mapa"] = True
                    atributos["map_node_id"] = node_id

                self.repo.upsert_campaign_item(
                    item_id=item_id,
                    campaign_id=campaign_id,
                    nome=nome,
                    categoria=categoria,
                    descricao=descricao,
                    atributos=atributos,
                    adquirido_no_turno=adquirido_no_turno
                )

            elif action_type in ["remove_item", "remove_structure", "remove_kingdom_asset"]:
                item_id = payload.get("id") or payload.get("nome")
                if item_id:
                    items = self.repo.get_campaign_items(campaign_id)
                    matched = [i for i in items if i["id"] == str(item_id) or i["nome"] == str(item_id)]
                    if matched:
                        node_id = matched[0].get("atributos", {}).get("map_node_id")
                        if node_id:
                            self.repo.delete_map_node(node_id, campaign_id)
                    self.repo.delete_campaign_item(str(item_id), campaign_id)

            elif action_type == "create_task":
                task_id = payload.get("id") or f"task_{turn_number}_{str(uuid.uuid4())[:6]}"
                titulo = payload.get("titulo", "Nova Tarefa")
                descricao = payload.get("descricao", "")
                status = payload.get("status", "em_andamento")
                progresso = payload.get("progresso", 0)
                duracao_estimada = payload.get("duracao_estimada")
                objetivo_esperado = payload.get("objetivo_esperado")
                is_incidente = payload.get("is_incidente_dinamico", False) or payload.get("is_incidente", False)
                dia_inicio = payload.get("dia_inicio") or current_day
                dias_estimados = payload.get("dias_estimados") or 0
                criada_no_turno = payload.get("criada_no_turno", turn_number)
                self.repo.upsert_campaign_task(
                    task_id=task_id,
                    campaign_id=campaign_id,
                    titulo=titulo,
                    descricao=descricao,
                    status=status,
                    progresso=progresso,
                    duracao_estimada=duracao_estimada,
                    objetivo_esperado=objetivo_esperado,
                    is_incidente=is_incidente,
                    dia_inicio=dia_inicio,
                    dias_estimados=dias_estimados,
                    criada_no_turno=criada_no_turno
                )

            elif action_type == "update_task":
                task_id = payload.get("id") or payload.get("titulo")
                if task_id:
                    existing_tasks = self.repo.get_campaign_tasks(campaign_id)
                    matched = [t for t in existing_tasks if t["id"] == str(task_id) or t["titulo"] == str(task_id)]
                    if matched:
                        target = matched[0]
                        self.repo.upsert_campaign_task(
                            task_id=target["id"],
                            campaign_id=campaign_id,
                            titulo=payload.get("titulo", target["titulo"]),
                            descricao=payload.get("descricao", target.get("descricao", "")),
                            status=payload.get("status", target.get("status", "em_andamento")),
                            progresso=payload.get("progresso", target.get("progresso")),
                            duracao_estimada=payload.get("duracao_estimada", target.get("duracao_estimada")),
                            objetivo_esperado=payload.get("objetivo_esperado", target.get("objetivo_esperado")),
                            is_incidente=payload.get("is_incidente_dinamico", target.get("is_incidente_dinamico", False)),
                            dia_inicio=payload.get("dia_inicio", target.get("dia_inicio", 1)),
                            dias_estimados=payload.get("dias_estimados", target.get("dias_estimados", 0)),
                            criada_no_turno=target.get("criada_no_turno", turn_number)
                        )

            elif action_type == "create_periodic_event":
                raw_id = payload.get("id")
                titulo = payload.get("titulo", "Novo Evento Periódico")
                existing_pe = self.repo.get_periodic_events(campaign_id)
                matched = [e for e in existing_pe if (raw_id and e["id"] == str(raw_id)) or e["titulo"].lower() == titulo.lower() or ("imposto" in titulo.lower() and "imposto" in e["titulo"].lower())]

                if matched:
                    target = matched[0]
                    event_id = target["id"]
                    old_efeito = target.get("efeito", {})
                    new_efeito = payload.get("efeito", {})
                    if isinstance(old_efeito, dict) and "formula" in old_efeito and "formula" not in new_efeito:
                        efeito = {**old_efeito, **new_efeito}
                    else:
                        efeito = new_efeito
                    intervalo = int(payload.get("intervalo_dias", target.get("intervalo_dias", 30)))
                    proximo = int(payload.get("proximo_disparo_dia") or target.get("proximo_disparo_dia", current_day + intervalo))
                    descricao = payload.get("descricao", target.get("descricao", ""))
                    status_pe = payload.get("status", target.get("status", "ativo"))
                    criado_turno = target.get("criado_no_turno", turn_number)
                else:
                    event_id = raw_id or f"pe_{turn_number}_{str(uuid.uuid4())[:6]}"
                    intervalo = int(payload.get("intervalo_dias", 30))
                    proximo = int(payload.get("proximo_disparo_dia") or (current_day + intervalo))
                    descricao = payload.get("descricao", "")
                    efeito = payload.get("efeito", {})
                    status_pe = payload.get("status", "ativo")
                    criado_turno = turn_number

                self.repo.upsert_periodic_event(
                    event_id=event_id,
                    campaign_id=campaign_id,
                    titulo=titulo,
                    intervalo_dias=intervalo,
                    proximo_disparo_dia=proximo,
                    descricao=descricao,
                    ultimo_disparo_dia=0,
                    efeito=efeito,
                    status=status_pe,
                    criado_no_turno=criado_turno
                )

            elif action_type == "update_periodic_event":
                event_id = payload.get("id") or payload.get("titulo")
                if event_id:
                    existing_pe = self.repo.get_periodic_events(campaign_id)
                    matched = [e for e in existing_pe if e["id"] == str(event_id) or e["titulo"].lower() == str(event_id).lower() or ("imposto" in str(event_id).lower() and "imposto" in e["titulo"].lower())]
                    if matched:
                        target = matched[0]
                        old_efeito = target.get("efeito", {})
                        new_efeito = payload.get("efeito", {})
                        if isinstance(old_efeito, dict) and "formula" in old_efeito and "formula" not in new_efeito:
                            efeito = {**old_efeito, **new_efeito}
                        else:
                            efeito = new_efeito
                        self.repo.upsert_periodic_event(
                            event_id=target["id"],
                            campaign_id=campaign_id,
                            titulo=payload.get("titulo", target["titulo"]),
                            intervalo_dias=int(payload.get("intervalo_dias", target["intervalo_dias"])),
                            proximo_disparo_dia=int(payload.get("proximo_disparo_dia", target["proximo_disparo_dia"])),
                            descricao=payload.get("descricao", target.get("descricao", "")),
                            ultimo_disparo_dia=int(payload.get("ultimo_disparo_dia", target.get("ultimo_disparo_dia", 0))),
                            efeito=efeito,
                            status=payload.get("status", target.get("status", "ativo")),
                            criado_no_turno=target.get("criado_no_turno", turn_number)
                        )

            elif action_type in ["remove_periodic_event", "delete_periodic_event"]:
                event_id = payload.get("id") or payload.get("titulo")
                if event_id:
                    self.repo.delete_periodic_event(str(event_id), campaign_id)

            elif action_type == "add_ally":
                ally_id = payload.get("id") or f"ally_{turn_number}_{str(uuid.uuid4())[:6]}"
                nome = payload.get("nome", "Reino Desconhecido")
                if self._is_player_kingdom_or_capital(nome, kingdom_name, ruler_name) or self._is_player_kingdom_or_capital(ally_id, kingdom_name, ruler_name):
                    continue
                rei = payload.get("rei", "Desconhecido")
                raca = payload.get("raca") or payload.get("race", "Humano")
                populacao = payload.get("populacao", "10000")
                poder_militar = payload.get("poder_militar", "1000")
                relacionamento = payload.get("relacionamento", 50)
                status_diplomatico = payload.get("status_diplomatico", "neutro")
                historico_notas = payload.get("historico_notas")
                self.repo.upsert_campaign_ally(
                    ally_id=ally_id,
                    campaign_id=campaign_id,
                    nome=nome,
                    rei=rei,
                    raca=raca,
                    populacao=populacao,
                    poder_militar=poder_militar,
                    relacionamento=relacionamento,
                    status_diplomatico=status_diplomatico,
                    historico_notas=historico_notas
                )
                ally_node_id = f"node_{ally_id}"
                edge_map = {"aliado": "alianca", "amigavel": "alianca", "neutro": "neutro", "tensao": "tensao", "hostil": "guerra", "vassalo": "alianca"}
                edge_type = edge_map.get(str(status_diplomatico).lower(), "neutro")
                all_nodes = self.repo.get_map_nodes(campaign_id)
                angle = (len(all_nodes) * 1.3) % 6.28
                node_x = float(payload.get("x", math.cos(angle) * 260.0))
                node_y = float(payload.get("y", math.sin(angle) * 260.0))
                self.repo.upsert_map_node(
                    node_id=ally_node_id,
                    campaign_id=campaign_id,
                    label=nome,
                    node_type="reino_vizinho",
                    emoji="👑",
                    x=node_x,
                    y=node_y,
                    status="ativo",
                    metadata={
                        "rei": rei,
                        "raca": raca,
                        "populacao": populacao,
                        "poder_militar": poder_militar,
                        "relacionamento": relacionamento,
                        "status_diplomatico": status_diplomatico,
                        "dono": nome,
                        "detalhes": historico_notas or f"Reino governado por {rei} ({raca})"
                    }
                )
                self.repo.upsert_map_edge(
                    edge_id=f"edge_cap_{ally_node_id}",
                    campaign_id=campaign_id,
                    source_node_id="node_capital",
                    target_node_id=ally_node_id,
                    edge_type=edge_type,
                    descricao=f"Relação Diplomática com {nome}"
                )

            elif action_type == "update_ally":
                ally_id = payload.get("id") or payload.get("nome")
                if ally_id:
                    if self._is_player_kingdom_or_capital(str(ally_id), kingdom_name, ruler_name):
                        continue
                    new_nome = payload.get("nome", "")
                    if new_nome and self._is_player_kingdom_or_capital(new_nome, kingdom_name, ruler_name):
                        continue
                    existing_allies = self.repo.get_campaign_allies(campaign_id)
                    matched = [a for a in existing_allies if a["id"] == str(ally_id) or a["nome"] == str(ally_id)]
                    if matched:
                        target = matched[0]
                        new_rel = payload.get("relacionamento", target.get("relacionamento", 50))
                        new_stat = payload.get("status_diplomatico", target.get("status_diplomatico", "neutro"))
                        new_raca = payload.get("raca") or payload.get("race") or target.get("raca", "Humano")
                        new_rei = payload.get("rei", target["rei"])
                        new_pop = payload.get("populacao", target.get("populacao", "10000"))
                        new_mil = payload.get("poder_militar", target.get("poder_militar", "1000"))
                        new_hist = payload.get("historico_notas", target.get("historico_notas"))
                        new_nome = payload.get("nome", target["nome"])
                        self.repo.upsert_campaign_ally(
                            ally_id=target["id"],
                            campaign_id=campaign_id,
                            nome=new_nome,
                            rei=new_rei,
                            raca=new_raca,
                            populacao=new_pop,
                            poder_militar=new_mil,
                            relacionamento=new_rel,
                            status_diplomatico=new_stat,
                            historico_notas=new_hist
                        )
                        ally_node_id = f"node_{target['id']}"
                        existing_nodes = self.repo.get_map_nodes(campaign_id)
                        matching_node = next((n for n in existing_nodes if n["id"] == ally_node_id or n["label"] == target["nome"]), None)
                        if matching_node:
                            cur_meta = matching_node.get("metadata", {})
                            cur_meta.update({
                                "rei": new_rei,
                                "raca": new_raca,
                                "populacao": new_pop,
                                "poder_militar": new_mil,
                                "relacionamento": new_rel,
                                "status_diplomatico": new_stat,
                                "dono": new_nome,
                                "detalhes": new_hist or cur_meta.get("detalhes", "")
                            })
                            self.repo.upsert_map_node(
                                node_id=matching_node["id"],
                                campaign_id=campaign_id,
                                label=new_nome,
                                node_type="reino_vizinho",
                                emoji="👑",
                                x=matching_node.get("x", 240.0),
                                y=matching_node.get("y", -140.0),
                                status=matching_node.get("status", "ativo"),
                                metadata=cur_meta
                            )
                            edge_map = {"aliado": "alianca", "amigavel": "alianca", "neutro": "neutro", "tensao": "tensao", "hostil": "guerra", "vassalo": "alianca"}
                            new_edge_type = edge_map.get(str(new_stat).lower(), "neutro")
                            self.repo.upsert_map_edge(
                                edge_id=f"edge_cap_{matching_node['id']}",
                                campaign_id=campaign_id,
                                source_node_id="node_capital",
                                target_node_id=matching_node["id"],
                                edge_type=new_edge_type,
                                descricao=f"Relação Diplomática com {new_nome}"
                            )

            elif action_type == "add_map_node":
                node_id = payload.get("id") or f"node_{turn_number}_{str(uuid.uuid4())[:6]}"
                label = payload.get("label") or payload.get("nome", "Ponto Estratégico")
                node_type = payload.get("node_type", "estrutura")
                
                is_capital_target = (
                    str(node_id) == "node_capital" or 
                    str(node_type).lower() == "capital" or 
                    self._is_player_kingdom_or_capital(node_id, kingdom_name, ruler_name) or 
                    self._is_player_kingdom_or_capital(label, kingdom_name, ruler_name)
                )

                if is_capital_target:
                    status_node = payload.get("status", "ativo")
                    metadata = payload.get("metadata", {})
                    if not isinstance(metadata, dict):
                        metadata = {}
                    existing_nodes = self.repo.get_map_nodes(campaign_id)
                    existing_cap = next((n for n in existing_nodes if n["id"] == "node_capital"), None)
                    cap_meta = existing_cap.get("metadata", {}) if existing_cap else {}
                    cap_meta.update(metadata)
                    self.repo.upsert_map_node(
                        node_id="node_capital",
                        campaign_id=campaign_id,
                        label=f"Capital {kingdom_name}" if kingdom_name else "Capital Imperial",
                        node_type="capital",
                        emoji="🏰",
                        x=0.0,
                        y=0.0,
                        status=status_node or "ativo",
                        size="mega",
                        metadata=cap_meta
                    )
                    continue

                node_size = self._infer_node_size(node_type, payload.get("size") or payload.get("tamanho_no"))
                
                default_emojis = {
                    "capital": "🏰", "bioma": "🌲", "floresta": "🌲", "montanha": "⛰️",
                    "mina": "⛏️", "vila": "🌾", "fazenda": "🌾", "tropa": "⚔️",
                    "exercito": "⚔️", "patrulha": "🛡️", "reino_vizinho": "👑", "aliado": "👑",
                    "estrutura": "🏛️", "fortificacao": "🛡️", "posto_avancado": "🏹",
                    "santuario": "✨", "templo": "⛪", "porto": "⚓", "mar": "🌊",
                    "ruina": "🏚️", "caverna": "🕳️", "monumento": "🗿", "estatua": "🗿"
                }
                emoji = payload.get("emoji") or default_emojis.get(node_type.lower(), "📍")
                
                x = payload.get("x")
                y = payload.get("y")
                if x is None or y is None:
                    x, y = self._calculate_orbital_position(campaign_id, node_type, payload.get("categoria", ""))

                status_node = payload.get("status", "ativo")
                metadata = payload.get("metadata", {})
                if not isinstance(metadata, dict):
                    metadata = {}
                
                self.repo.upsert_map_node(
                    node_id=node_id,
                    campaign_id=campaign_id,
                    label=label,
                    node_type=node_type,
                    emoji=emoji,
                    x=float(x),
                    y=float(y),
                    status=status_node,
                    size=node_size,
                    metadata=metadata
                )

                connect_to = payload.get("connect_to")
                edge_type = payload.get("edge_type", "estrada")
                if connect_to:
                    edge_id = f"edge_{node_id}_{connect_to}"
                    self.repo.upsert_map_edge(
                        edge_id=edge_id,
                        campaign_id=campaign_id,
                        source_node_id=node_id,
                        target_node_id=str(connect_to),
                        edge_type=edge_type,
                        descricao=payload.get("edge_desc", "")
                    )

            elif action_type == "update_map_node":
                node_id = payload.get("id") or payload.get("label")
                if node_id:
                    is_capital_target = (
                        str(node_id) == "node_capital" or 
                        self._is_player_kingdom_or_capital(node_id, kingdom_name, ruler_name) or 
                        self._is_player_kingdom_or_capital(payload.get("label", ""), kingdom_name, ruler_name)
                    )
                    if is_capital_target:
                        existing_nodes = self.repo.get_map_nodes(campaign_id)
                        existing_cap = next((n for n in existing_nodes if n["id"] == "node_capital"), None)
                        cap_meta = existing_cap.get("metadata", {}) if existing_cap else {}
                        if "metadata" in payload and isinstance(payload["metadata"], dict):
                            cap_meta.update(payload["metadata"])
                        self.repo.upsert_map_node(
                            node_id="node_capital",
                            campaign_id=campaign_id,
                            label=f"Capital {kingdom_name}" if kingdom_name else "Capital Imperial",
                            node_type="capital",
                            emoji="🏰",
                            x=0.0,
                            y=0.0,
                            status=payload.get("status", existing_cap.get("status", "ativo") if existing_cap else "ativo"),
                            size="mega",
                            metadata=cap_meta
                        )
                        continue

                    existing_nodes = self.repo.get_map_nodes(campaign_id)
                    matched = [n for n in existing_nodes if n["id"] == str(node_id) or n["label"] == str(node_id)]
                    if matched:
                        target = matched[0]
                        new_meta = target.get("metadata", {})
                        if "metadata" in payload and isinstance(payload["metadata"], dict):
                            new_meta.update(payload["metadata"])
                        
                        target_nt = payload.get("node_type", target.get("node_type", "estrutura"))
                        target_size = self._infer_node_size(target_nt, payload.get("size") or target.get("size"))
                        self.repo.upsert_map_node(
                            node_id=target["id"],
                            campaign_id=campaign_id,
                            label=payload.get("label", target["label"]),
                            node_type=target_nt,
                            emoji=payload.get("emoji", target.get("emoji", "📍")),
                            x=float(payload.get("x", target.get("x", 0.0))),
                            y=float(payload.get("y", target.get("y", 0.0))),
                            status=payload.get("status", target.get("status", "ativo")),
                            size=target_size,
                            metadata=new_meta
                        )

            elif action_type == "remove_map_node":
                node_id = payload.get("id") or payload.get("label")
                if node_id:
                    self.repo.delete_map_node(str(node_id), campaign_id)

            elif action_type in ["connect_map_nodes", "add_map_edge"]:
                source = payload.get("source_node_id") or payload.get("source")
                target = payload.get("target_node_id") or payload.get("target")
                if source and target:
                    edge_id = payload.get("id") or f"edge_{source}_{target}"
                    edge_type = payload.get("edge_type", "estrada")
                    desc = payload.get("descricao", "")
                    self.repo.upsert_map_edge(
                        edge_id=edge_id,
                        campaign_id=campaign_id,
                        source_node_id=str(source),
                        target_node_id=str(target),
                        edge_type=edge_type,
                        descricao=desc
                    )

            elif action_type in ["disconnect_map_nodes", "remove_map_edge"]:
                edge_id = payload.get("id")
                if edge_id:
                    self.repo.delete_map_edge(str(edge_id), campaign_id)
                else:
                    source = payload.get("source_node_id") or payload.get("source")
                    target = payload.get("target_node_id") or payload.get("target")
                    if source and target:
                        self.repo.delete_map_edge_between(campaign_id, str(source), str(target))

            elif action_type == "place_asset_on_map":
                asset_id = payload.get("asset_id") or payload.get("id") or payload.get("nome")
                if asset_id:
                    self.place_asset_on_map(
                        campaign_id=campaign_id,
                        asset_id=str(asset_id),
                        x=payload.get("x"),
                        y=payload.get("y"),
                        node_type=payload.get("node_type"),
                        size=payload.get("size") or payload.get("tamanho_no"),
                        connect_to_capital=payload.get("connect_to_capital", True)
                    )

            elif action_type == "unplace_asset_from_map":
                asset_id = payload.get("asset_id") or payload.get("id") or payload.get("nome")
                if asset_id:
                    self.unplace_asset_from_map(campaign_id=campaign_id, asset_id=str(asset_id))

    def _process_turn_response(
        self,
        campaign_id: str,
        turn_number: int,
        ruler_name: str,
        kingdom_name: str,
        race: str,
        user_action: str,
        response_json: Dict[str, Any],
        evaluation_result: Optional[EvaluationResult] = None
    ) -> TurnResponse:
        narrative = response_json.get("aventura", "O destino se desenrola diante de vossos olhos...")
        status_dict = response_json.get("status_reino", {})

        latest_ws = self.repo.get_latest_world_state(campaign_id) if turn_number > 1 else None
        prev_day = latest_ws.get("current_day", 1) if latest_ws else 1
        days_passed = evaluation_result.dias_passados if evaluation_result else (1 if turn_number > 1 else 0)
        current_day = prev_day + days_passed if turn_number > 1 else 1

        pop_val = status_dict.get("populacao") or status_dict.get("população") or status_dict.get("population") or 10000
        try:
            pop_int = int(str(pop_val).replace(".", "").replace(",", ""))
        except (ValueError, TypeError):
            pop_int = 10000

        periodic_gold_delta = 0
        periodic_mil_delta = 0
        triggered_events_to_process = []

        if evaluation_result and evaluation_result.eventos_periodicos_disparados:
            triggered_events_to_process = evaluation_result.eventos_periodicos_disparados
        elif turn_number > 1 and latest_ws:
            triggered_events_to_process = self.repo.get_due_periodic_events(campaign_id, current_day)

        if triggered_events_to_process:
            for ev in triggered_events_to_process:
                ev_id = ev.get("id")
                intervalo = max(1, int(ev.get("intervalo_dias", 30)))
                next_disp = current_day + intervalo
                calc_res = ev.get("efeito_calculado") or calculate_event_effect(ev.get("efeito", {}), {
                    "populacao": pop_int,
                    "felicidade": status_dict.get("felicidade", latest_ws.get("happiness", "70%") if latest_ws else "70%"),
                    "dinheiro": latest_ws.get("gold", 5000) if latest_ws else 5000,
                    "poder_militar": latest_ws.get("military", 1000) if latest_ws else 1000,
                    "dia_atual": current_day
                })
                periodic_gold_delta += calc_res.get("dinheiro", 0) + calc_res.get("ouro", 0) + calc_res.get("gold", 0)
                periodic_mil_delta += calc_res.get("poder_militar", 0) + calc_res.get("military", 0)

                self.repo.upsert_periodic_event(
                    event_id=ev_id,
                    campaign_id=campaign_id,
                    titulo=ev.get("titulo", "Evento Periódico"),
                    intervalo_dias=intervalo,
                    proximo_disparo_dia=next_disp,
                    descricao=ev.get("descricao", ""),
                    ultimo_disparo_dia=current_day,
                    efeito=ev.get("efeito", {}),
                    status=ev.get("status", "ativo"),
                    criado_no_turno=ev.get("criado_no_turno", 1)
                )

        if latest_ws:
            delta_action_gold = evaluation_result.delta_dinheiro if (evaluation_result and evaluation_result.delta_dinheiro is not None) else 0
            final_gold = max(0, latest_ws.get("gold", 5000) + delta_action_gold + periodic_gold_delta)

            delta_action_mil = evaluation_result.delta_poder_militar if (evaluation_result and evaluation_result.delta_poder_militar is not None) else 0
            final_mil = max(0, latest_ws.get("military", 1000) + delta_action_mil + periodic_mil_delta)
        else:
            final_gold = int(status_dict.get("dinheiro", 5000)) + periodic_gold_delta
            final_mil = int(status_dict.get("poder_militar", 1000)) + periodic_mil_delta

        status = KingdomStatus(
            nome_reino=status_dict.get("nome_reino", kingdom_name),
            imperador=status_dict.get("imperador", ruler_name),
            dinheiro=final_gold,
            populacao=pop_int,
            religião=status_dict.get("religião", "Nenhuma"),
            poder_militar=final_mil,
            felicidade=str(status_dict.get("felicidade", "70%")),
            dia_atual=current_day,
            dias_passados=days_passed if turn_number > 1 else 0
        )

        response_json["user_action"] = user_action
        self.repo.touch_campaign(campaign_id)
        self.repo.save_world_state(
            campaign_id=campaign_id,
            turn_number=turn_number,
            kingdom_name=status.nome_reino,
            ruler_name=status.imperador,
            race=race,
            gold=status.dinheiro,
            population=status.populacao,
            military=status.poder_militar,
            happiness=status.felicidade,
            religion=status.religião,
            current_day=current_day,
            raw_state_json=response_json
        )

        memory_text = f"Turno {turn_number}: Jogador ordenou '{user_action}'. Consequência: {narrative[:300]}"
        importance = calculate_importance(memory_text)
        fallback_emb = generate_fallback_embedding(memory_text)

        mem_id = self.vector_store.add_memory(
            campaign_id=campaign_id,
            turn_number=turn_number,
            content=memory_text,
            importance=importance,
            event_type="turn",
            embedding=fallback_emb
        )

        def _bg_async_task(db_path_val, camp_id_val, turn_num_val, mem_id_val, mem_text_val, provider_inst, summarizer_inst):
            try:
                real_emb = provider_inst.generate_embedding(mem_text_val)
                if real_emb:
                    conn_bg = get_connection(db_path_val)
                    vstore_bg = VectorStore(conn_bg)
                    vstore_bg.update_memory_embedding(mem_id_val, real_emb)
                    if turn_num_val % config.SUMMARY_INTERVAL_TURNS == 0:
                        repo_bg = Repository(conn_bg)
                        recents = vstore_bg.get_recent_memories(camp_id_val, limit=config.SUMMARY_INTERVAL_TURNS)
                        camp = repo_bg.get_campaign(camp_id_val) or {}
                        prev_summary = camp.get("summary", "")
                        new_summary = summarizer_inst.summarize_turns(prev_summary, recents)
                        repo_bg.update_campaign_summary(camp_id_val, new_summary)
                    conn_bg.close()
            except Exception:
                pass

        self._bg_executor.submit(
            _bg_async_task,
            self.db_path,
            campaign_id,
            turn_number,
            mem_id,
            memory_text,
            self.provider,
            self.summarizer
        )

        st_mem = self._get_short_term_memory(campaign_id)
        st_mem.append({"user": user_action, "narrative": narrative})
        if len(st_mem) > 10:
            st_mem.pop(0)

        raw_actions = response_json.get("actions", [])
        parsed_actions: List[GameAction] = []
        if isinstance(raw_actions, list):
            for act in raw_actions:
                if isinstance(act, dict) and "action_type" in act:
                    parsed_actions.append(GameAction(
                        action_type=act["action_type"],
                        payload=act.get("payload", {})
                    ))

        if parsed_actions:
            self.apply_actions(campaign_id, parsed_actions, turn_number, current_day)

        if "personagens" in response_json and isinstance(response_json["personagens"], list):
            for idx, c in enumerate(response_json["personagens"]):
                if isinstance(c, dict) and "nome" in c:
                    cid = c.get("id") or f"npc_{turn_number}_{idx}"
                    self.repo.upsert_character(
                        character_id=cid,
                        campaign_id=campaign_id,
                        name=c["nome"],
                        role=c.get("papel", "NPC"),
                        location=c.get("local", "Reino"),
                        is_alive=c.get("vivo", True),
                        relationship=c.get("lealdade", 0)
                    )

        if "quests" in response_json and isinstance(response_json["quests"], list):
            for idx, q in enumerate(response_json["quests"]):
                if isinstance(q, dict) and "titulo" in q:
                    qid = q.get("id") or f"quest_{turn_number}_{idx}"
                    self.repo.upsert_quest(
                        quest_id=qid,
                        campaign_id=campaign_id,
                        title=q["titulo"],
                        description=q.get("descricao", ""),
                        status=q.get("status", "active"),
                        objective=q.get("objetivo", "")
                    )

        if "itens" in response_json and isinstance(response_json["itens"], list):
            for idx, item in enumerate(response_json["itens"]):
                if isinstance(item, dict) and "nome" in item:
                    iid = item.get("id") or f"item_{turn_number}_{idx}"
                    self.repo.upsert_item(
                        item_id=iid,
                        campaign_id=campaign_id,
                        name=item["nome"],
                        owner=item.get("dono", "player"),
                        quantity=item.get("quantidade", 1),
                        properties=item.get("propriedades", {})
                    )

        raw_clima = response_json.get("clima") or response_json.get("tema") or response_json.get("trilha_sonora") or ""
        clima = self._infer_clima(raw_clima, narrative)
        opcoes = self._extract_opcoes(response_json, narrative)

        return TurnResponse(
            campaign_id=campaign_id,
            aventura=narrative,
            status_reino=status,
            clima=clima,
            opcoes=opcoes,
            actions=parsed_actions,
            raw_json=response_json
        )

    def get_campaign_state_details(self, campaign_id: str) -> Dict[str, Any]:
        self._cleanup_duplicate_capital_nodes(campaign_id)
        return {
            "items": self.repo.get_campaign_items(campaign_id),
            "tasks": self.repo.get_campaign_tasks(campaign_id),
            "periodic_events": self.repo.get_periodic_events(campaign_id),
            "allies": self.repo.get_campaign_allies(campaign_id),
            "map_nodes": self.repo.get_map_nodes(campaign_id),
            "map_edges": self.repo.get_map_edges(campaign_id)
        }

    def estimate_action_impact(self, campaign_id: str, action_text: str) -> Dict[str, Any]:
        latest_ws = self.repo.get_latest_world_state(campaign_id)
        if not latest_ws:
            return {"dinheiro": None, "poder_militar": None, "populacao": None, "dias_passados": 1, "tipo_execucao": "imediata", "viabilidade": True, "explicacao": ""}

        prev_opcoes = latest_ws.get("raw_state", {}).get("opcoes", [])
        if not prev_opcoes:
            prev_opcoes = self._extract_opcoes(latest_ws.get("raw_state", {}), latest_ws.get("raw_state", {}).get("aventura", ""))

        active_tasks = self.repo.get_campaign_tasks(campaign_id)
        periodic_events = self.repo.get_periodic_events(campaign_id)

        eval_res = self.evaluator.evaluate_action(
            campaign_id=campaign_id,
            action_text=action_text,
            previous_opcoes=prev_opcoes,
            current_world_state=latest_ws,
            active_tasks=active_tasks,
            periodic_events=periodic_events
        )

        return {
            "dinheiro": eval_res.delta_dinheiro,
            "poder_militar": eval_res.delta_poder_militar,
            "populacao": eval_res.delta_populacao,
            "dias_passados": eval_res.dias_passados,
            "tipo_execucao": eval_res.tipo_execucao,
            "viabilidade": eval_res.viabilidade,
            "explicacao": eval_res.motivo_inviabilidade or eval_res.intencao_detectada
        }

    def _extract_opcoes(self, response_json: Dict[str, Any], narrative: str) -> List[Any]:
        raw_opcoes = response_json.get("opcoes")
        if isinstance(raw_opcoes, list) and len(raw_opcoes) > 0:
            cleaned = []
            for opt in raw_opcoes:
                if isinstance(opt, dict) and "texto" in opt:
                    cleaned.append(opt)
                elif isinstance(opt, str) and opt.strip():
                    cleaned.append(opt.strip())
            if len(cleaned) > 0:
                return cleaned

        import re
        lines = narrative.split("\n")
        line_opcoes = [l.strip() for l in lines if re.match(r"^\s*(\d+[\.\)]|\*\*?\d+[\.\)]\*\*?)\s+", l)]
        if line_opcoes:
            return line_opcoes

        inline_matches = re.findall(r"(?:^|\s)(\d+[\.\)]\s+[\s\S]+?)(?=(?:\s+\d+[\.\)]|$))", narrative)
        if inline_matches:
            return [m.strip() for m in inline_matches]

        return []

    def _infer_clima(self, raw_clima: str, narrative: str) -> str:
        valid_climas = {"aventura", "calmo", "frenetico", "harmonia", "desenvolvimento", "desespero"}
        if raw_clima and isinstance(raw_clima, str):
            c_clean = raw_clima.strip().lower()
            if c_clean in valid_climas:
                return c_clean
            for v in valid_climas:
                if v in c_clean:
                    return v

        text = narrative.lower()
        if any(k in text for k in ["guerra", "batalha", "combate", "ataque", "exército", "sangue", "inimigo", "invasão"]):
            return "frenetico"
        if any(k in text for k in ["crise", "desastre", "fome", "morte", "ruína", "peste", "perigo", "caos", "traição"]):
            return "desespero"
        if any(k in text for k in ["festa", "celebração", "paz", "alegria", "harmonia", "aliança", "vitória", "casamento"]):
            return "harmonia"
        if any(k in text for k in ["construção", "obras", "reforma", "mina", "comércio", "moedas", "impostos", "expansão", "evoluir"]):
            return "desenvolvimento"
        if any(k in text for k in ["diplomacia", "conselho", "tranquilo", "meditação", "tratado", "silêncio", "acordo"]):
            return "calmo"
        return "aventura"

    def rollback_turn(self, campaign_id: str, target_turn: int) -> TurnResponse:
        target_ws = self.repo.get_world_state_at_turn(campaign_id, target_turn)
        if not target_ws:
            raise ValueError(f"Turno {target_turn} não encontrado para a campanha '{campaign_id}'.")

        self.repo.delete_world_states_after_turn(campaign_id, target_turn)
        self.repo.delete_memories_after_turn(campaign_id, target_turn)

        if campaign_id in self.short_term_memories:
            del self.short_term_memories[campaign_id]

        status = KingdomStatus(
            nome_reino=target_ws["kingdom_name"],
            imperador=target_ws["ruler_name"],
            dinheiro=target_ws["gold"],
            populacao=target_ws.get("population", 10000) or 10000,
            religião=target_ws["religion"],
            poder_militar=target_ws["military"],
            felicidade=target_ws["happiness"]
        )
        raw_json = target_ws.get("raw_state") or {}
        if isinstance(raw_json, str):
            import json
            try:
                raw_json = json.loads(raw_json)
            except Exception:
                raw_json = {}
        narrative = raw_json.get("aventura", f"Retornado ao Turno {target_turn}.")
        raw_clima = raw_json.get("clima") or raw_json.get("tema") or raw_json.get("trilha_sonora") or ""
        clima = self._infer_clima(raw_clima, narrative)
        opcoes = self._extract_opcoes(raw_json, narrative)

        return TurnResponse(
            aventura=narrative,
            status_reino=status,
            clima=clima,
            opcoes=opcoes,
            actions=[],
            raw_json=raw_json
        )

    def delete_campaign(self, campaign_id: str) -> bool:
        if campaign_id in self.short_term_memories:
            del self.short_term_memories[campaign_id]
        return self.repo.delete_campaign(campaign_id)

    def get_campaign_history(self, campaign_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_world_state_history(campaign_id)

    def get_campaign_entities(self, campaign_id: str) -> Dict[str, Any]:
        return {
            "characters": self.repo.get_characters(campaign_id),
            "quests": self.repo.get_quests(campaign_id),
            "items": self.repo.get_items(campaign_id),
            "locations": self.repo.get_locations(campaign_id),
            "campaign_items": self.repo.get_campaign_items(campaign_id),
            "campaign_tasks": self.repo.get_campaign_tasks(campaign_id),
            "periodic_events": self.repo.get_periodic_events(campaign_id),
            "campaign_allies": self.repo.get_campaign_allies(campaign_id),
            "map_nodes": self.repo.get_map_nodes(campaign_id),
            "map_edges": self.repo.get_map_edges(campaign_id)
        }

    def export_campaign(self, campaign_id: str) -> Dict[str, Any]:
        camp = self.repo.get_campaign(campaign_id)
        if not camp:
            raise ValueError(f"Campanha '{campaign_id}' não encontrada.")

        history = self.repo.get_world_state_history(campaign_id)
        entities = self.get_campaign_entities(campaign_id)
        memories = self.vector_store.get_recent_memories(campaign_id, limit=100)

        return {
            "version": "2.0.0",
            "campaign": camp,
            "world_states": history,
            "entities": entities,
            "memories": memories
        }

    def import_campaign(self, campaign_data: Dict[str, Any]) -> str:
        camp_meta = campaign_data.get("campaign")
        if not camp_meta or "name" not in camp_meta:
            raise ValueError("Payload de importação inválido: dados da campanha ausentes.")

        campaign_id = camp_meta.get("id") or str(uuid.uuid4())[:8]
        self.repo.delete_campaign(campaign_id)
        self.repo.create_campaign(campaign_id, camp_meta["name"])
        if camp_meta.get("summary"):
            self.repo.update_campaign_summary(campaign_id, camp_meta["summary"])

        for ws in campaign_data.get("world_states", []):
            self.repo.save_world_state(
                campaign_id=campaign_id,
                turn_number=ws["turn_number"],
                kingdom_name=ws["kingdom_name"],
                ruler_name=ws["ruler_name"],
                race=ws["race"],
                gold=ws["gold"],
                population=ws.get("population", 10000),
                military=ws["military"],
                happiness=ws["happiness"],
                religion=ws["religion"],
                current_day=ws.get("current_day", 1),
                raw_state_json=ws.get("raw_state", {})
            )

        entities = campaign_data.get("entities", {})
        for char in entities.get("characters", []):
            self.repo.upsert_character(
                character_id=char["id"],
                campaign_id=campaign_id,
                name=char["name"],
                role=char.get("role", "NPC"),
                location=char.get("location", "Valdrin"),
                is_alive=char.get("is_alive", True),
                relationship=char.get("relationship_with_player", 0),
                knowledge=char.get("knowledge", [])
            )
        for quest in entities.get("quests", []):
            self.repo.upsert_quest(
                quest_id=quest["id"],
                campaign_id=campaign_id,
                title=quest["title"],
                description=quest.get("description", ""),
                status=quest.get("status", "active"),
                objective=quest.get("objective", "")
            )
        for item in entities.get("items", []):
            self.repo.upsert_item(
                item_id=item["id"],
                campaign_id=campaign_id,
                name=item["name"],
                owner=item.get("owner", "player"),
                quantity=item.get("quantity", 1),
                properties=item.get("properties", {})
            )
        for loc in entities.get("locations", []):
            self.repo.upsert_location(
                location_id=loc["id"],
                campaign_id=campaign_id,
                name=loc["name"],
                description=loc.get("description", ""),
                control_faction=loc.get("control_faction", "Player")
            )

        for ci in entities.get("campaign_items", []):
            self.repo.upsert_campaign_item(
                item_id=ci["id"],
                campaign_id=campaign_id,
                nome=ci["nome"],
                categoria=ci.get("categoria", "outro"),
                descricao=ci.get("descricao", ""),
                atributos=ci.get("atributos", {}),
                adquirido_no_turno=ci.get("adquirido_no_turno", 1)
            )
        for ct in entities.get("campaign_tasks", []):
            self.repo.upsert_campaign_task(
                task_id=ct["id"],
                campaign_id=campaign_id,
                titulo=ct["titulo"],
                descricao=ct.get("descricao", ""),
                status=ct.get("status", "em_andamento"),
                progresso=ct.get("progresso"),
                duracao_estimada=ct.get("duracao_estimada"),
                objetivo_esperado=ct.get("objetivo_esperado"),
                is_incidente=ct.get("is_incidente_dinamico", False) or ct.get("is_incidente", False),
                dia_inicio=ct.get("dia_inicio", 1),
                dias_estimados=ct.get("dias_estimados", 0),
                criada_no_turno=ct.get("criada_no_turno", 1)
            )
        for pe in entities.get("periodic_events", []):
            self.repo.upsert_periodic_event(
                event_id=pe["id"],
                campaign_id=campaign_id,
                titulo=pe["titulo"],
                intervalo_dias=pe.get("intervalo_dias", 30),
                proximo_disparo_dia=pe.get("proximo_disparo_dia", 30),
                descricao=pe.get("descricao", ""),
                ultimo_disparo_dia=pe.get("ultimo_disparo_dia", 0),
                efeito=pe.get("efeito", {}),
                status=pe.get("status", "ativo"),
                criado_no_turno=pe.get("criado_no_turno", 1)
            )
        for ca in entities.get("campaign_allies", []):
            self.repo.upsert_campaign_ally(
                ally_id=ca["id"],
                campaign_id=campaign_id,
                nome=ca["nome"],
                rei=ca["rei"],
                populacao=ca.get("populacao", "10000"),
                poder_militar=ca.get("poder_militar", "1000"),
                relacionamento=ca.get("relacionamento", 50),
                status_diplomatico=ca.get("status_diplomatico", "neutro"),
                historico_notas=ca.get("historico_notas")
            )
        for mn in entities.get("map_nodes", []):
            self.repo.upsert_map_node(
                node_id=mn["id"],
                campaign_id=campaign_id,
                label=mn["label"],
                node_type=mn.get("node_type", "estrutura"),
                emoji=mn.get("emoji", "📍"),
                x=float(mn.get("x", 0.0)),
                y=float(mn.get("y", 0.0)),
                status=mn.get("status", "ativo"),
                size=mn.get("size") or self._infer_node_size(mn.get("node_type", "estrutura")),
                metadata=mn.get("metadata", {})
            )
        for me in entities.get("map_edges", []):
            self.repo.upsert_map_edge(
                edge_id=me["id"],
                campaign_id=campaign_id,
                source_node_id=me["source_node_id"],
                target_node_id=me["target_node_id"],
                edge_type=me.get("edge_type", "estrada"),
                descricao=me.get("descricao", "")
            )

        for mem in campaign_data.get("memories", []):
            self.vector_store.add_memory(
                campaign_id=campaign_id,
                turn_number=mem["turn_number"],
                content=mem["content"],
                importance=mem.get("importance", 0.5),
                event_type=mem.get("event_type", "turn"),
                embedding=mem.get("embedding", [])
            )

        return campaign_id

    def place_asset_on_map(
        self,
        campaign_id: str,
        asset_id: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
        node_type: Optional[str] = None,
        size: Optional[str] = None,
        connect_to_capital: bool = True
    ) -> Dict[str, Any]:
        items = self.repo.get_campaign_items(campaign_id)
        matched = [i for i in items if i["id"] == str(asset_id) or i["nome"] == str(asset_id)]
        if not matched:
            raise ValueError(f"Ativo {asset_id} não encontrado na campanha {campaign_id}")
        target = matched[0]
        cat = target.get("categoria", "estrutura")
        nome = target.get("nome", "Ativo")
        attrs = target.get("atributos", {})
        
        if not node_type:
            nom_lower = nome.lower()
            if "santuario" in nom_lower or "santuário" in nom_lower or cat == "santuario":
                target_nt = "santuario"
            elif "estatua" in nom_lower or "estátua" in nom_lower or "monumento" in nom_lower or cat in ["estatua", "monumento"]:
                target_nt = "estatua"
            elif "obra" in nom_lower or cat == "obra":
                target_nt = "obra"
            elif "fort" in nom_lower or "muralha" in nom_lower or cat == "fortificacao":
                target_nt = "fortificacao"
            elif cat in ["santuario", "fortificacao", "monumento", "estatua", "mina", "porto", "vila", "bioma"]:
                target_nt = cat
            else:
                target_nt = "estrutura"
        else:
            target_nt = node_type

        target_size = self._infer_node_size(target_nt, size or attrs.get("tamanho_no"))
        
        default_emojis = {
            "capital": "🏰", "bioma": "🌲", "floresta": "🌲", "montanha": "⛰️",
            "mina": "⛏️", "vila": "🌾", "fazenda": "🌾", "tropa": "⚔️",
            "exercito": "⚔️", "patrulha": "🛡️", "reino_vizinho": "👑", "aliado": "👑",
            "estrutura": "🏛️", "fortificacao": "🛡️", "posto_avancado": "🏹",
            "santuario": "✨", "templo": "⛪", "porto": "⚓", "mar": "🌊",
            "ruina": "🏚️", "caverna": "🕳️", "monumento": "🗿", "estatua": "🗿"
        }
        emoji = default_emojis.get(target_nt.lower(), "🏛️")
        
        if x is None or y is None:
            x, y = self._calculate_orbital_position(campaign_id, target_nt, cat)

        node_id = attrs.get("map_node_id") or f"node_{target['id']}"
        self.repo.upsert_map_node(
            node_id=node_id,
            campaign_id=campaign_id,
            label=nome,
            node_type=target_nt,
            emoji=emoji,
            x=float(x),
            y=float(y),
            status="ativo",
            size=target_size,
            metadata={"asset_id": target["id"], "categoria": cat, "dono": "Reino"}
        )
        if connect_to_capital:
            self.repo.upsert_map_edge(
                edge_id=f"edge_cap_{node_id}",
                campaign_id=campaign_id,
                source_node_id="node_capital",
                target_node_id=node_id,
                edge_type="rota",
                descricao=f"Acesso a {nome}"
            )
        self.repo.link_item_to_map_node(target["id"], campaign_id, node_id)
        return {
            "node_id": node_id,
            "label": nome,
            "node_type": target_nt,
            "size": target_size,
            "x": float(x),
            "y": float(y)
        }

    def unplace_asset_from_map(self, campaign_id: str, asset_id: str) -> bool:
        return self.repo.unlink_item_from_map_node(str(asset_id), campaign_id)

    def get_campaign_info(self, campaign_id: str) -> Optional[CampaignInfo]:
        camp = self.repo.get_campaign(campaign_id)
        if not camp:
            return None

        self.repo.touch_campaign(campaign_id)
        latest_ws = self.repo.get_latest_world_state(campaign_id)
        status = None
        turn_num = 0
        if latest_ws:
            turn_num = latest_ws["turn_number"]
            status = KingdomStatus(
                nome_reino=latest_ws["kingdom_name"],
                imperador=latest_ws["ruler_name"],
                dinheiro=latest_ws["gold"],
                populacao=latest_ws.get("population", 10000) or 10000,
                religião=latest_ws["religion"],
                poder_militar=latest_ws["military"],
                felicidade=latest_ws["happiness"]
            )

        race_val = latest_ws.get("race", "Humano") if latest_ws else "Humano"
        return CampaignInfo(
            campaign_id=campaign_id,
            name=camp["name"],
            turn_number=turn_num,
            summary=camp.get("summary", ""),
            race=race_val,
            latest_status=status
        )

    def list_campaigns(self) -> List[Dict[str, Any]]:
        return self.repo.list_campaigns()
