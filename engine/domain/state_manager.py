import uuid
from typing import Dict, Any, List, Optional
from engine.db.schema import init_db
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore
from engine.providers.base import BaseLLMProvider
from engine.providers.factory import LLMFactory
from engine.memory.context_builder import ContextBuilder
from engine.memory.importance import calculate_importance
from engine.memory.summarizer import CampaignSummarizer
from engine.domain.models import KingdomStatus, TurnResponse, CampaignInfo
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
  }
}

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
  }
}

Exemplo 2 (Turno de Decisão Estratégica):
{
  "aventura": "Sábia decisão, Vossa Majestade. Ao rejeitar o dogma em favor da Razão, Aurelia estabelece as fundações de uma nova era iluminada. As universidades começam a ser planejadas e os eruditos celebram vossa prudência.\\n\\nO que deseja fazer agora para fortalecer o reino de Aurelia?\\n1. Ordenar a construção da Grande Academia de Ciências para acelerar o progresso tecnológico.\\n2. Construir Centro de Treinamento Militar para fortalecer os guardas de fronteira.\\n3. Enviar exploradores para mapear as Terras Desconhecidas.",
  "clima": "desenvolvimento",
  "opcoes": [
    {
      "texto": "1. Ordenar a construção da Grande Academia de Ciências para acelerar o progresso tecnológico.",
      "impacto": { "dinheiro": -500, "poder_militar": 0 }
    },
    {
      "texto": "2. Construir Centro de Treinamento Militar para fortalecer os guardas de fronteira.",
      "impacto": { "dinheiro": -400, "poder_militar": 200 }
    },
    {
      "texto": "3. Enviar exploradores para mapear as Terras Desconhecidas.",
      "impacto": { "dinheiro": null, "poder_militar": null }
    }
  ],
  "status_reino": {
    "nome_reino": "Aurelia",
    "imperador": "Arthur",
    "dinheiro": 4500,
    "populacao": 10200,
    "religião": "Estado Laico",
    "poder_militar": 1200,
    "felicidade": "75%"
  }
}

### REGRAS DE JOGO
1. **Religião Inicial:** Todo reino SEMPRE começa SEM religião oficial ("Nenhuma"). No Turno 1 (início da campanha), a PRIMEIRA pergunta/decisão apresentada ao Imperador DEVE ser obrigatoriamente a escolha ou definição da religião/doutrina do reino.
2. **Consequências Lógicas:** As escolhas do usuário devem alterar os números no próximo turno.
3. **Clima Musical:** Defina o campo 'clima' dinamicamente conforme a atmosfera da cena.
4. **Tom Majestic:** Use linguagem formal e imersiva ("Vossa Majestade", "Sua Graça").
5. **Sem Emojis no Texto:** Mantenha a narrativa literária, elegante e imersiva. NÃO inclua emojis no texto narrativo.
6. **Opções e Prévias OBRIGATÓRIAS:** Você DEVE sempre incluir o campo 'opcoes' como uma lista com exatamente 3 objetos. Cada objeto possui 'texto' e 'impacto' com 'dinheiro' (inteiro indicando variação ex: -500, 200 ou null se incerto) e 'poder_militar' (inteiro indicando variação ex: 200, -100 ou null se incerto em combates).
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
        # Isolated short-term memory per campaign_id
        self.short_term_memories: Dict[str, List[Dict[str, str]]] = {}

    def _get_short_term_memory(self, campaign_id: str) -> List[Dict[str, str]]:
        if campaign_id not in self.short_term_memories:
            # Reconstruct from recent vector store memories if available
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

        # Initial turn prompt
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

        # Build Context with RAG & Short-Term
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

        # 1. Save Structured World State to SQLite3
        response_json["user_action"] = user_action
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

        # 2. Add turn to Episodic Vector RAG Memory
        memory_text = f"Turno {turn_number}: Jogador ordenou '{user_action}'. Consequência: {narrative[:300]}"
        importance = calculate_importance(memory_text)
        embedding = self.provider.generate_embedding(memory_text)

        self.vector_store.add_memory(
            campaign_id=campaign_id,
            turn_number=turn_number,
            content=memory_text,
            importance=importance,
            event_type="turn",
            embedding=embedding
        )

        # 3. Short term memory management (per campaign)
        st_mem = self._get_short_term_memory(campaign_id)
        st_mem.append({"user": user_action, "narrative": narrative})
        if len(st_mem) > 10:
            st_mem.pop(0)

        # 4. Optional entity updates from LLM JSON response
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

        # 5. Periodic Chapter Summarizer
        if turn_number % config.SUMMARY_INTERVAL_TURNS == 0:
            try:
                recents = self.vector_store.get_recent_memories(campaign_id, limit=config.SUMMARY_INTERVAL_TURNS)
                camp = self.repo.get_campaign(campaign_id) or {}
                prev_summary = camp.get("summary", "")
                new_summary = self.summarizer.summarize_turns(prev_summary, recents)
                self.repo.update_campaign_summary(campaign_id, new_summary)
            except Exception as e:
                print(f"Warning: Campaign summarizer failed ({e})")

        raw_clima = response_json.get("clima") or response_json.get("tema") or response_json.get("trilha_sonora") or ""
        clima = self._infer_clima(raw_clima, narrative)
        opcoes = self._extract_opcoes(response_json, narrative)

        return TurnResponse(
            aventura=narrative,
            status_reino=status,
            clima=clima,
            opcoes=opcoes,
            raw_json=response_json
        )

    def estimate_action_impact(self, campaign_id: str, action_text: str) -> Dict[str, Any]:
        """Estimate the expected cost/gain for a custom free-text action before execution."""
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
        """Rollback campaign state to a specific turn number."""
        target_ws = self.repo.get_world_state_at_turn(campaign_id, target_turn)
        if not target_ws:
            raise ValueError(f"Turno {target_turn} não encontrado para a campanha '{campaign_id}'.")

        # Trim states and RAG memories after target_turn
        self.repo.delete_world_states_after_turn(campaign_id, target_turn)
        self.repo.delete_memories_after_turn(campaign_id, target_turn)

        # Reset short-term memory for this campaign
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
            raw_json=raw_json
        )

    def delete_campaign(self, campaign_id: str) -> bool:
        """Completely delete a campaign and all related states."""
        if campaign_id in self.short_term_memories:
            del self.short_term_memories[campaign_id]
        return self.repo.delete_campaign(campaign_id)

    def get_campaign_history(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get step-by-step history of world states across turns."""
        return self.repo.get_world_state_history(campaign_id)

    def get_campaign_entities(self, campaign_id: str) -> Dict[str, Any]:
        """Get all registered game entities (characters, quests, items, locations)."""
        return {
            "characters": self.repo.get_characters(campaign_id),
            "quests": self.repo.get_quests(campaign_id),
            "items": self.repo.get_items(campaign_id),
            "locations": self.repo.get_locations(campaign_id)
        }

    def export_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Export full campaign savegame payload to JSON-serializable dict."""
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
        """Import full campaign savegame payload from JSON dict."""
        camp_meta = campaign_data.get("campaign")
        if not camp_meta or "name" not in camp_meta:
            raise ValueError("Payload de importação inválido: dados da campanha ausentes.")

        campaign_id = camp_meta.get("id") or str(uuid.uuid4())[:8]
        # Clean existing if present
        self.repo.delete_campaign(campaign_id)
        self.repo.create_campaign(campaign_id, camp_meta["name"])
        if camp_meta.get("summary"):
            self.repo.update_campaign_summary(campaign_id, camp_meta["summary"])

        # Import world states
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

        # Import entities
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

        # Import memories
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

