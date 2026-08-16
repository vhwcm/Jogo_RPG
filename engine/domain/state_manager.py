import uuid
import math
import concurrent.futures
from typing import Dict, Any, List, Optional, Union
from engine.db.schema import init_db, get_connection
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore
from engine.providers.base import BaseLLMProvider
from engine.providers.factory import LLMFactory
from engine.memory.context_builder import ContextBuilder
from engine.memory.importance import calculate_importance
from engine.memory.summarizer import CampaignSummarizer
from engine.domain.models import KingdomStatus, TurnResponse, CampaignInfo, Item, Task, ImperioAliado, GameAction, MapNode, MapEdge
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
      "action_type": "add_item | remove_item | add_structure | remove_structure | add_kingdom_asset | remove_kingdom_asset | create_task | update_task | add_ally | update_ally | add_map_node | update_map_node | remove_map_node | connect_map_nodes | disconnect_map_nodes",
      "payload": { ... }
    }
  ]
}

### SISTEMA DE ACTIONS SUPORTADAS
Sempre que eventos da história concederem itens, criaturas ou artefatos, ou quando o soberano construir/estabelecer estruturas e postos do reino (ex: posto avançado, santuário, quartel, muralha, mina, monumento), ou iniciar/atualizar tarefas de longo prazo, ou firmar/mudar relações diplomáticas, ou descobrir novos territórios/biomas no mapa, ou mobilizar tropas/rotas no mapa tático, emita itens na lista "actions":
1. add_item / add_structure / add_kingdom_asset:
   payload: {"id": "id_unico_str", "nome": "Nome do Item/Estrutura/Criatura", "categoria": "estrutura|santuario|posto_avancado|fortificacao|monumento|criatura|artefato|recurso|equipamento|outro", "descricao": "...", "atributos": {"chave": "valor"}}
2. remove_item / remove_structure / remove_kingdom_asset:
   payload: {"id": "id_do_item_ou_estrutura"}
3. create_task:
   payload: {"id": "id_da_task", "titulo": "Título da Missão", "descricao": "...", "status": "em_andamento|concluida|falhou|cancelada", "progresso": 0_a_100, "duracao_estimada": "3 turnos", "objetivo_esperado": "...", "is_incidente_dinamico": true_ou_false}
4. update_task:
   payload: {"id": "id_da_task", "status": "em_andamento|concluida|falhou|cancelada", "progresso": 0_a_100, "descricao": "..."}
5. add_ally:
   payload: {"id": "id_do_aliado", "nome": "Nome do Reino", "rei": "Nome do Soberano", "populacao": 25000, "poder_militar": 3000, "relacionamento": 50_a_100, "status_diplomatico": "hostil|neutro|amigavel|aliado|vassalo", "historico_notas": "..."}
6. update_ally:
   payload: {"id": "id_do_aliado", "relacionamento": -100_a_100, "status_diplomatico": "...", "historico_notas": "..."}
7. add_map_node:
   payload: {"id": "id_do_node", "label": "Nome do Ponto no Mapa", "node_type": "bioma|tropa|reino_vizinho|estrutura|santuario|fortificacao|mina|porto|ruina|vila", "emoji": "🌲|⚔️|👑|🏛️|✨|🛡️|⛏️|⚓|🏚️|🌾", "status": "ativo|descoberto|hostil|em_marcha", "metadata": {"tropas": 150, "dono": "Reino", "perigo": "Baixo"}, "connect_to": "id_do_node_pai_opcional", "edge_type": "estrada|fronteira|rota"}
8. update_map_node:
   payload: {"id": "id_do_node", "status": "...", "metadata": { ... }}
9. remove_map_node:
   payload: {"id": "id_do_node"}
10. connect_map_nodes:
   payload: {"source_node_id": "id_origem", "target_node_id": "id_destino", "edge_type": "estrada|fronteira|rota", "descricao": "..."}
11. disconnect_map_nodes:
   payload: {"source_node_id": "id_origem", "target_node_id": "id_destino"}

### EXEMPLOS DE FORMATO DE RESPOSTA (SMALL SHOTS / FEW-SHOT)
Exemplo 1 (Turno Inicial - Escolha de Religião):
{
  "aventura": "Saudações, Vossa Majestade. O Reino de Aurelia foi fundado com glória, porém o povo aguarda vossa palavra sobre a fé que guiará nossas terras.\\n\\nComo deseja definir o destino espiritual de Aurelia?\\n1. Declarar o Reino como um Estado Laico pautado na Ciência e na Razão.\\n2. Adotar a Fé dos Antigos Deuses da Natureza como religião oficial.\\n3. Instituir o Culto da Chama Sagrada como a verdadeira e única fé do reino.",
  "clima": "desenvolvimento",
  "opcoes": [
    {
      "texto": "1. Declarar o Reino como um Estado Laico pautado na Ciência e na Razão.",
      "impacto": { "dinheiro": 0, "poder_militar": 0 }
    },
    {
      "texto": "2. Adotar a Fé dos Antigos Deuses da Natureza como religião oficial.",
      "impacto": { "dinheiro": 0, "poder_militar": 0 }
    },
    {
      "texto": "3. Instituir o Culto da Chama Sagrada como a verdadeira e única fé do reino.",
      "impacto": { "dinheiro": 0, "poder_militar": 0 }
    }
  ],
  "status_reino": {
    "nome_reino": "Aurelia",
    "imperador": "Arthur",
    "dinheiro": 5000,
    "populacao": 10000,
    "religião": "Nenhuma",
    "poder_militar": 1000,
    "felicidade": "70%"
  },
  "actions": []
}

Exemplo 2 (Turno com Recompensas, Ações e Atualização de Mapa):
{
  "aventura": "Vossos batedores retornaram da expedição ao leste e mapearam a misteriosa Floresta dos Sussurros, além de despacharem uma guarnição militar para patrulhar a fronteira.\\n\\nQual vossa próxima ordem?\\n1. Estabelecer um posto avançado de observação na floresta.\\n2. Expandir o comércio com as vilas locais.\\n3. Recuar as tropas para a capital.",
  "clima": "aventura",
  "opcoes": [
    {
      "texto": "1. Estabelecer um posto avançado de observação na floresta.",
      "impacto": { "dinheiro": -400, "poder_militar": 100 }
    },
    {
      "texto": "2. Expandir o comércio com as vilas locais.",
      "impacto": { "dinheiro": 250, "poder_militar": 0 }
    },
    {
      "texto": "3. Recuar as tropas para a capital.",
      "impacto": { "dinheiro": 0, "poder_militar": 0 }
    }
  ],
  "status_reino": {
    "nome_reino": "Aurelia",
    "imperador": "Arthur",
    "dinheiro": 4600,
    "populacao": 10100,
    "religião": "Estado Laico",
    "poder_militar": 1100,
    "felicidade": "75%"
  },
  "actions": [
    {
      "action_type": "add_map_node",
      "payload": {
        "id": "node_floresta_sussurros",
        "label": "Floresta dos Sussurros",
        "node_type": "bioma",
        "emoji": "🌲",
        "status": "descoberto",
        "metadata": { "perigo": "Médio", "recursos": "Madeira Rara" },
        "connect_to": "node_capital",
        "edge_type": "estrada"
      }
    },
    {
      "action_type": "add_map_node",
      "payload": {
        "id": "node_patrulha_leste",
        "label": "1ª Legião em Patrulha",
        "node_type": "tropa",
        "emoji": "⚔️",
        "status": "em_marcha",
        "metadata": { "tropas": 200, "comandante": "Capitão Gareth" },
        "connect_to": "node_floresta_sussurros",
        "edge_type": "rota"
      }
    }
  ]
}

### REGRAS DE JOGO
1. **Religião Inicial:** Todo reino SEMPRE começa SEM religião oficial ("Nenhuma"). No Turno 1 (início da campanha), a PRIMEIRA pergunta/decisão apresentada ao Imperador DEVE ser obrigatoriamente a escolha ou definição da religião/doutrina do reino.
2. **Consequências Lógicas:** As escolhas do usuário devem alterar os números no próximo turno.
3. **Clima Musical:** Defina o campo 'clima' dinamicamente conforme a atmosfera da cena.
4. **Tom Majestic:** Use linguagem formal e imersiva ("Vossa Majestade", "Sua Graça").
5. **Sem Emojis no Texto:** Mantenha a narrativa literária, elegante e imersiva. NÃO inclua emojis no texto narrativo.
6. **Opções e Prévias OBRIGATÓRIAS:** Você DEVE sempre incluir o campo 'opcoes' como uma lista com exatamente 3 objetos. Cada objeto possui 'texto' e 'impacto' com 'dinheiro' (inteiro indicando variação ex: -500, 200 ou null se incerto) e 'poder_militar' (inteiro indicando variação ex: 200, -100 ou null se incerto em combates).
7. **Actions Modulares:** Emita ações na chave 'actions' quando itens forem obtidos/perdidos, missões iniciadas/atualizadas, aliados adicionados/modificados ou elementos do mapa forem descobertos/alterados.
"""

class GameEngine:
    def __init__(self, db_path: str = "", provider_name: Optional[str] = None):
        self.db_path = db_path or config.DB_PATH
        self.conn = init_db(self.db_path)
        self.repo = Repository(self.conn)
        self.vector_store = VectorStore(self.conn)
        self.provider = LLMFactory.get_provider(provider_name)
        self.context_builder = ContextBuilder(self.repo, self.vector_store, self.provider)
        self.summarizer = CampaignSummarizer(self.provider)
        self.short_term_memories: Dict[str, List[Dict[str, str]]] = {}
        self._bg_executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

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
        race: str
    ) -> TurnResponse:
        campaign_id = str(uuid.uuid4())[:8]
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

        context = self.context_builder.build_prompt_context(campaign_id, player_action, st_memory)

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
            response_json=response_json
        )
        return turn_resp

    def apply_actions(self, campaign_id: str, actions: List[GameAction], turn_number: int):
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
                adquirido_no_turno = payload.get("adquirido_no_turno", turn_number)
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
                    self.repo.delete_campaign_item(str(item_id), campaign_id)

            elif action_type == "create_task":
                task_id = payload.get("id") or f"task_{turn_number}_{str(uuid.uuid4())[:6]}"
                titulo = payload.get("titulo", "Nova Tarefa")
                descricao = payload.get("descricao", "")
                status = payload.get("status", "em_andamento")
                progresso = payload.get("progresso")
                duracao_estimada = payload.get("duracao_estimada")
                objetivo_esperado = payload.get("objetivo_esperado")
                is_incidente = payload.get("is_incidente_dinamico", False) or payload.get("is_incidente", False)
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
                            criada_no_turno=target.get("criada_no_turno", turn_number)
                        )

            elif action_type == "add_ally":
                ally_id = payload.get("id") or f"ally_{turn_number}_{str(uuid.uuid4())[:6]}"
                nome = payload.get("nome", "Reino Desconhecido")
                rei = payload.get("rei", "Desconhecido")
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
                    populacao=populacao,
                    poder_militar=poder_militar,
                    relacionamento=relacionamento,
                    status_diplomatico=status_diplomatico,
                    historico_notas=historico_notas
                )

            elif action_type == "update_ally":
                ally_id = payload.get("id") or payload.get("nome")
                if ally_id:
                    existing_allies = self.repo.get_campaign_allies(campaign_id)
                    matched = [a for a in existing_allies if a["id"] == str(ally_id) or a["nome"] == str(ally_id)]
                    if matched:
                        target = matched[0]
                        self.repo.upsert_campaign_ally(
                            ally_id=target["id"],
                            campaign_id=campaign_id,
                            nome=payload.get("nome", target["nome"]),
                            rei=payload.get("rei", target["rei"]),
                            populacao=payload.get("populacao", target.get("populacao", "10000")),
                            poder_militar=payload.get("poder_militar", target.get("poder_militar", "1000")),
                            relacionamento=payload.get("relacionamento", target.get("relacionamento", 50)),
                            status_diplomatico=payload.get("status_diplomatico", target.get("status_diplomatico", "neutro")),
                            historico_notas=payload.get("historico_notas", target.get("historico_notas"))
                        )

            elif action_type == "add_map_node":
                node_id = payload.get("id") or f"node_{turn_number}_{str(uuid.uuid4())[:6]}"
                label = payload.get("label") or payload.get("nome", "Ponto Estratégico")
                node_type = payload.get("node_type", "estrutura")
                
                default_emojis = {
                    "capital": "🏰", "bioma": "🌲", "floresta": "🌲", "montanha": "⛰️",
                    "mina": "⛏️", "vila": "🌾", "fazenda": "🌾", "tropa": "⚔️",
                    "exercito": "⚔️", "patrulha": "🛡️", "reino_vizinho": "👑", "aliado": "👑",
                    "estrutura": "🏛️", "fortificacao": "🛡️", "posto_avancado": "🏹",
                    "santuario": "✨", "templo": "⛪", "porto": "⚓", "mar": "🌊",
                    "ruina": "🏚️", "caverna": "🕳️"
                }
                emoji = payload.get("emoji") or default_emojis.get(node_type.lower(), "📍")
                
                x = payload.get("x")
                y = payload.get("y")
                if x is None or y is None:
                    existing_nodes = self.repo.get_map_nodes(campaign_id)
                    count = len(existing_nodes)
                    angle = (count * 0.897) + 0.3
                    radius = 160.0 + ((count // 6) * 110.0)
                    x = round(radius * math.cos(angle), 1)
                    y = round(radius * math.sin(angle), 1)

                status_node = payload.get("status", "ativo")
                metadata = payload.get("metadata", {})
                if not isinstance(metadata, dict):
                    metadata = {"detalhes": str(metadata)}

                self.repo.upsert_map_node(
                    node_id=node_id,
                    campaign_id=campaign_id,
                    label=label,
                    node_type=node_type,
                    emoji=emoji,
                    x=float(x),
                    y=float(y),
                    status=status_node,
                    metadata=metadata
                )

                connect_to = payload.get("connect_to") or payload.get("parent_node_id")
                if connect_to:
                    edge_id = f"edge_{node_id}_{connect_to}_{str(uuid.uuid4())[:4]}"
                    edge_type = payload.get("edge_type", "estrada")
                    desc = payload.get("edge_desc", payload.get("descricao", "Rota Conectada"))
                    self.repo.upsert_map_edge(
                        edge_id=edge_id,
                        campaign_id=campaign_id,
                        source_node_id=str(connect_to),
                        target_node_id=str(node_id),
                        edge_type=edge_type,
                        descricao=desc
                    )

            elif action_type == "update_map_node":
                node_id = payload.get("id") or payload.get("label")
                if node_id:
                    existing_nodes = self.repo.get_map_nodes(campaign_id)
                    matched = [n for n in existing_nodes if n["id"] == str(node_id) or n["label"] == str(node_id)]
                    if matched:
                        target = matched[0]
                        updated_metadata = {**target.get("metadata", {}), **payload.get("metadata", {})}
                        self.repo.upsert_map_node(
                            node_id=target["id"],
                            campaign_id=campaign_id,
                            label=payload.get("label", target["label"]),
                            node_type=payload.get("node_type", target.get("node_type", "estrutura")),
                            emoji=payload.get("emoji", target.get("emoji", "📍")),
                            x=float(payload.get("x", target["x"])),
                            y=float(payload.get("y", target["y"])),
                            status=payload.get("status", target.get("status", "ativo")),
                            metadata=updated_metadata
                        )

            elif action_type == "remove_map_node":
                node_id = payload.get("id") or payload.get("label")
                if node_id:
                    self.repo.delete_map_node(str(node_id), campaign_id)

            elif action_type in ["connect_map_nodes", "add_map_edge"]:
                source = payload.get("source_node_id") or payload.get("source")
                target = payload.get("target_node_id") or payload.get("target")
                if source and target:
                    edge_id = payload.get("id") or f"edge_{source}_{target}_{str(uuid.uuid4())[:4]}"
                    edge_type = payload.get("edge_type", "estrada")
                    descricao = payload.get("descricao", "")
                    self.repo.upsert_map_edge(
                        edge_id=edge_id,
                        campaign_id=campaign_id,
                        source_node_id=str(source),
                        target_node_id=str(target),
                        edge_type=edge_type,
                        descricao=descricao
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

    def _process_turn_response(
        self,
        campaign_id: str,
        turn_number: int,
        ruler_name: str,
        kingdom_name: str,
        race: str,
        user_action: str,
        response_json: Dict[str, Any]
    ) -> TurnResponse:
        narrative = response_json.get("aventura", "O destino se desenrola diante de vossos olhos...")
        status_dict = response_json.get("status_reino", {})

        pop_val = status_dict.get("populacao") or status_dict.get("população") or status_dict.get("population") or 10000
        try:
            pop_int = int(str(pop_val).replace(".", "").replace(",", ""))
        except (ValueError, TypeError):
            pop_int = 10000

        status = KingdomStatus(
            nome_reino=status_dict.get("nome_reino", kingdom_name),
            imperador=status_dict.get("imperador", ruler_name),
            dinheiro=int(status_dict.get("dinheiro", 5000)),
            populacao=pop_int,
            religião=status_dict.get("religião", "Nenhuma"),
            poder_militar=int(status_dict.get("poder_militar", 1000)),
            felicidade=str(status_dict.get("felicidade", "70%"))
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
            self.apply_actions(campaign_id, parsed_actions, turn_number)

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
            aventura=narrative,
            status_reino=status,
            clima=clima,
            opcoes=opcoes,
            actions=parsed_actions,
            raw_json=response_json
        )

    def get_campaign_state_details(self, campaign_id: str) -> Dict[str, Any]:
        return {
            "items": self.repo.get_campaign_items(campaign_id),
            "tasks": self.repo.get_campaign_tasks(campaign_id),
            "allies": self.repo.get_campaign_allies(campaign_id),
            "map_nodes": self.repo.get_map_nodes(campaign_id),
            "map_edges": self.repo.get_map_edges(campaign_id)
        }

    def estimate_action_impact(self, campaign_id: str, action_text: str) -> Dict[str, Any]:
        latest_ws = self.repo.get_latest_world_state(campaign_id)
        current_gold = latest_ws["gold"] if latest_ws else 5000
        current_military = latest_ws["military"] if latest_ws else 1000

        prompt = f"""Dada a seguinte ação pretendida pelo imperador: "{action_text}"
Status atual do reino: Dinheiro = {current_gold}, Poder Militar = {current_military}.
Estime os custos ou ganhos DIRETOS e PREVISÍVEIS desta ação em dinheiro e poder militar.
Se a ação for incerta (ex: combate, sorte, expedição de risco), coloque null.
Sua resposta deve ser APENAS um JSON válido no formato:
{{
  "dinheiro": -500 ou 200 ou null,
  "poder_militar": 100 ou -50 ou null,
  "explicacao": "Breve justificativa de 1 frase."
}}"""
        try:
            res = self.provider.generate_json(
                prompt=prompt,
                system_instruction="Você é um assistente de cálculo de custos econômicos e militares para RPG.",
                temperature=0.2
            )
            return {
                "dinheiro": res.get("dinheiro"),
                "poder_militar": res.get("poder_militar"),
                "explicacao": res.get("explicacao", "")
            }
        except Exception:
            return {"dinheiro": None, "poder_militar": None, "explicacao": ""}

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
                criada_no_turno=ct.get("criada_no_turno", 1)
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
                x=mn.get("x", 0.0),
                y=mn.get("y", 0.0),
                status=mn.get("status", "ativo"),
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
