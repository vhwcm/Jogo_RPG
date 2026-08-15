from typing import List, Dict, Any
from engine.providers.base import BaseLLMProvider

SUMMARIZER_PROMPT = """
ATUE COMO O CRONISTA REAL DO REINO.
Sua missão é resumir o histórico de eventos da campanha em um registro conciso de 1 a 2 parágrafos densos.
Mantenha os principais conflitos, mortes, alianças, descobertas e o estado atual das quests.
Ignorar detalhes banais (compras simples, saudações repetidas).
"""

class CampaignSummarizer:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    def summarize_turns(self, previous_summary: str, recent_memories: List[Dict[str, Any]]) -> str:
        events_text = "\n".join([f"- Turno {m.get('turn_number')}: {m.get('content')}" for m in recent_memories])
        prompt = f"""
RESUMO DA CAMPANHA ATÉ AGORA:
{previous_summary if previous_summary else '(Início da Campanha)'}

NOVOS EVENTOS RECENTES:
{events_text}

Por favor, gere um resumo atualizado e unificado da campanha:
"""
        return self.provider.generate_text(prompt, system_instruction=SUMMARIZER_PROMPT, temperature=0.3).strip()
