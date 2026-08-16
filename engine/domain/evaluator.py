import json
import re
from typing import Dict, Any, List, Optional
from engine.providers.base import BaseLLMProvider
from engine.domain.models import EvaluationResult
from engine.domain.formula_evaluator import calculate_event_effect

EVALUATOR_SYSTEM_INSTRUCTION = """VOCÊ É O ÁRBITRO DE REGRAS E AVALIADOR DE MECÂNICAS EM UM RPG DE ESTRATÉGIA.
SUA FUNÇÃO É DETERMINAR COM PRECISÃO MATEMÁTICA E LÓGICA O IMPACTO DE UMA AÇÃO DO JOGADOR.

### SUAS RESPONSABILIDADES:
1. **Identificar Escolhas Múltiplas:** Se o jogador disser "1 e 2", "opções 1 e 3", "quero a primeira e a segunda", identifique as opções selecionadas da lista anterior e COMBINE / SOME seus custos e ganhos.
2. **Cálculo Consolidado:**
   - Some os impactos em dinheiro, poder militar e população decorrentes EXCLUSIVAMENTE da ordem do jogador e das opções selecionadas.
   - NUNCA inclua no 'delta_dinheiro' ou 'delta_poder_militar' arrecadações de impostos ou tributos de eventos periódicos (esses são calculados automaticamente pelo motor de calendário).
   - Exemplo: Opção 1 custa -500 ouro, Opção 2 custa -300 ouro => delta_dinheiro = -800. Se a ação não tem custo nem opção com custo, delta_dinheiro = 0.
3. **Validação de Viabilidade:**
   - Verifique se o reino tem recursos suficientes para arcar com a soma dos custos.
   - Se o ouro atual for 600 e o custo total for -800, viabilidade = false.
4. **Passagem de Tempo em Dias (dias_passados):**
   - Estime quantos dias se passam no calendário do reino para executar esta ordem:
     - Decretos simples / audiências: 1 a 3 dias.
     - Pequenas obras / patrulhas locais: 5 a 15 dias.
     - Grandes construções / recrutamento em massa / expedições distantes: 20 a 60 dias.
5. **Classificação de Tipo de Execução:**
   - 'imediata': ações que se resolvem e produzem efeito no mesmo turno (ex: doar ouro, mudar imposto, responder embaixador).
   - 'longo_prazo': ações que exigem tempo, expedições, pesquisas ou construções (ex: explorar ruínas, erguer muralhas). Defina 'dias_duracao_tarefa'.
6. **Diretrizes para o Narrador:**
   - Instrua explicitamente o Game Master a NÃO concluir tarefas de longo prazo no mesmo turno, narrando apenas o início e mobilização.

### FORMATO OBRIGATÓRIO DE RESPOSTA (JSON):
{
  "intencao_detectada": "Descrição resumida da intenção do jogador",
  "opcoes_selecionadas": [1, 2],
  "delta_dinheiro": -800,
  "delta_poder_militar": 200,
  "delta_populacao": 0,
  "delta_felicidade": 5,
  "dias_passados": 10,
  "tipo_execucao": "longo_prazo",
  "dias_duracao_tarefa": 30,
  "viabilidade": true,
  "motivo_inviabilidade": "",
  "diretrizes_narrador": "Instruções estritas para o Narrador sobre como aplicar as consequências e narrar o evento.",
  "tarefas_atualizadas": [
    { "id": "task_id_ou_nome", "progresso_adicional": 25, "status": "em_andamento" }
  ]
}
"""

class ActionEvaluator:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    def evaluate_action(
        self,
        campaign_id: str,
        action_text: str,
        previous_opcoes: List[Any],
        current_world_state: Dict[str, Any],
        active_tasks: List[Dict[str, Any]],
        periodic_events: List[Dict[str, Any]]
    ) -> EvaluationResult:
        current_gold = current_world_state.get("gold", 5000)
        current_military = current_world_state.get("military", 1000)
        current_pop = current_world_state.get("population", 10000)
        current_day = current_world_state.get("current_day", 1)

        formatted_opcoes = []
        for idx, opt in enumerate(previous_opcoes):
            if isinstance(opt, dict):
                texto = opt.get("texto", f"Opção {idx+1}")
                impacto = opt.get("impacto", {})
                formatted_opcoes.append(f"- Opção {idx+1}: \"{texto}\" | Impacto: Ouro={impacto.get('dinheiro', 'N/A')}, Militar={impacto.get('poder_militar', 'N/A')}")
            else:
                formatted_opcoes.append(f"- Opção {idx+1}: \"{opt}\"")

        formatted_tasks = []
        for t in active_tasks:
            formatted_tasks.append(f"- Tarefa (ID: {t.get('id')}): {t.get('titulo')} | Progresso: {t.get('progresso', 0)}% | Dia Início: {t.get('dia_inicio', 1)} | Estimativa: {t.get('dias_estimados', 0)} dias")

        formatted_events = []
        for pe in periodic_events:
            formatted_events.append(f"- Evento Periódico: {pe.get('titulo')} | Intervalo: {pe.get('intervalo_dias')} dias | Próximo Disparo: Dia {pe.get('proximo_disparo_dia')}")

        prompt = f"""ESTADO ATUAL DO REINO (Dia {current_day}):
- Nome do Reino: {current_world_state.get('kingdom_name', 'N/A')}
- Imperador: {current_world_state.get('ruler_name', 'N/A')} (Raça: {current_world_state.get('race', 'Humano')})
- Ouro Disponível: {current_gold}
- Poder Militar: {current_military}
- População: {current_pop}

OPÇÕES OFERECIDAS ANTERIORMENTE:
{chr(10).join(formatted_opcoes) if formatted_opcoes else "Nenhuma opção estruturada"}

TAREFAS E MISSÕES EM ANDAMENTO:
{chr(10).join(formatted_tasks) if formatted_tasks else "Nenhuma tarefa em andamento"}

EVENTOS PERIÓDICOS ATIVOS:
{chr(10).join(formatted_events) if formatted_events else "Nenhum evento periódico"}

ORDEM DO JOGADOR:
"{action_text}"

Avalie a intenção, combine os custos se forem múltiplas opções, estime os dias transcorridos, classifique se é imediata ou longo prazo e emita o JSON de arbitragem.
IMPORTANTE: 'delta_dinheiro' e 'delta_poder_militar' devem refletir EXCLUSIVAMENTE o impacto direto da ordem do jogador ou das opções selecionadas (NÃO inclua tributos ou eventos periódicos)."""

        try:
            res_json = self.provider.generate_json(
                prompt=prompt,
                system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
                temperature=0.1
            )
            if not isinstance(res_json, dict):
                res_json = {}
        except Exception:
            res_json = {}

        selected_opts = res_json.get("opcoes_selecionadas") or self._heuristic_detect_options(action_text, previous_opcoes)
        delta_gold = res_json.get("delta_dinheiro")
        delta_mil = res_json.get("delta_poder_militar")
        delta_pop = res_json.get("delta_populacao")
        delta_hap = res_json.get("delta_felicidade")
        days_passed = res_json.get("dias_passados")
        exec_type = res_json.get("tipo_execucao", "imediata")
        task_duration = res_json.get("dias_duracao_tarefa")
        viability = res_json.get("viabilidade", True)
        unviability_reason = res_json.get("motivo_inviabilidade", "")
        narrator_guidance = res_json.get("diretrizes_narrador", "")

        if selected_opts:
            calculated_gold = 0
            calculated_mil = 0
            has_explicit_impact = False
            for opt_idx in selected_opts:
                if 1 <= opt_idx <= len(previous_opcoes):
                    opt_obj = previous_opcoes[opt_idx - 1]
                    if isinstance(opt_obj, dict) and "impacto" in opt_obj:
                        imp = opt_obj.get("impacto", {})
                        if isinstance(imp, dict):
                            g = imp.get("dinheiro")
                            m = imp.get("poder_militar")
                            if g is not None:
                                calculated_gold += int(g)
                                has_explicit_impact = True
                            if m is not None:
                                calculated_mil += int(m)
                                has_explicit_impact = True
            if has_explicit_impact:
                delta_gold = calculated_gold
                delta_mil = calculated_mil

        if days_passed is None or not isinstance(days_passed, int) or days_passed < 1:
            days_passed = 1 if exec_type == "imediata" else 7

        if delta_gold is not None and isinstance(delta_gold, (int, float)):
            if current_gold + delta_gold < 0:
                viability = False
                unviability_reason = f"Ouro insuficiente. Custo total necessário: {abs(delta_gold)}, mas o reino só possui {current_gold}."

        triggered_events = []
        target_day = current_day + days_passed
        for pe in periodic_events:
            if pe.get("status") == "ativo":
                next_trigger = pe.get("proximo_disparo_dia", 0)
                if next_trigger <= target_day:
                    ev_data = dict(pe)
                    ev_data["efeito_calculado"] = calculate_event_effect(pe.get("efeito", {}), {
                        "populacao": current_pop,
                        "felicidade": current_world_state.get("happiness", "70%"),
                        "dinheiro": current_gold,
                        "poder_militar": current_military,
                        "dia_atual": target_day
                    })
                    triggered_events.append(ev_data)

        if triggered_events:
            pe_gold = sum(e.get("efeito_calculado", {}).get("dinheiro", 0) + e.get("efeito_calculado", {}).get("ouro", 0) for e in triggered_events)
            pe_mil = sum(e.get("efeito_calculado", {}).get("poder_militar", 0) for e in triggered_events)
            if delta_gold is not None and isinstance(delta_gold, (int, float)) and pe_gold != 0:
                if delta_gold == pe_gold:
                    delta_gold = 0
                elif delta_gold > pe_gold:
                    delta_gold -= pe_gold
            if delta_mil is not None and isinstance(delta_mil, (int, float)) and pe_mil != 0:
                if delta_mil == pe_mil:
                    delta_mil = 0
                elif delta_mil > pe_mil:
                    delta_mil -= pe_mil

        return EvaluationResult(
            intencao_detectada=res_json.get("intencao_detectada", action_text),
            opcoes_selecionadas=selected_opts,
            delta_dinheiro=delta_gold,
            delta_poder_militar=delta_mil,
            delta_populacao=delta_pop,
            delta_felicidade=delta_hap,
            dias_passados=days_passed,
            tipo_execucao=exec_type,
            dias_duracao_tarefa=task_duration,
            viabilidade=viability,
            motivo_inviabilidade=unviability_reason,
            diretrizes_narrador=narrator_guidance,
            eventos_periodicos_disparados=triggered_events,
            tarefas_atualizadas=res_json.get("tarefas_atualizadas", [])
        )

    def _heuristic_detect_options(self, action_text: str, previous_opcoes: List[Any]) -> List[int]:
        selected = []
        low = action_text.lower()
        matches = re.findall(r"\b([1-9])\b", low)
        for m in matches:
            val = int(m)
            if val <= len(previous_opcoes) and val not in selected:
                selected.append(val)
        for idx, opt in enumerate(previous_opcoes, 1):
            if idx in selected:
                continue
            opt_text = (opt.get("texto", "") if isinstance(opt, dict) else str(opt)).lower()
            clean_opt = re.sub(r"^[0-9]+[\.\-\)\s]+", "", opt_text).strip()
            if clean_opt and (clean_opt in low or any(word in low for word in clean_opt.split() if len(word) > 4)):
                selected.append(idx)
        return sorted(selected)
