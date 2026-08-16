import re
from typing import List, Dict, Any, Optional
from engine.providers.base import BaseLLMProvider
from engine.providers.gemini_provider import GeminiProvider
from engine.providers.grok_provider import GrokProvider
from engine.providers.openai_provider import OpenAIProvider
from engine.providers.ollama_provider import OllamaProvider
from engine.utils import generate_fallback_embedding
import config

class MockFallbackProvider(BaseLLMProvider):
    @property
    def name(self) -> str:
        return "mock_fallback"

    def is_available(self) -> bool:
        return True

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        return "Os oráculos vislumbram o destino em silêncio. (Modo Offline / Simulador Narrativo Ativo)"

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        if "ÁRBITRO DE REGRAS" in system_instruction or "ORDEM DO JOGADOR:" in prompt:
            user_order = prompt.split("ORDEM DO JOGADOR:")[-1] if "ORDEM DO JOGADOR:" in prompt else prompt
            opts = []
            if "1" in user_order:
                opts.append(1)
            if "2" in user_order:
                opts.append(2)
            if "3" in user_order:
                opts.append(3)
            return {
                "intencao_detectada": "Ordem executada",
                "opcoes_selecionadas": opts,
                "delta_dinheiro": None,
                "delta_poder_militar": None,
                "delta_populacao": None,
                "delta_felicidade": None,
                "dias_passados": 7,
                "tipo_execucao": "imediata",
                "viabilidade": True,
                "motivo_inviabilidade": "",
                "diretrizes_narrador": "Executar a ordem com precisão.",
                "tarefas_atualizadas": []
            }

        kingdom_match = re.search(r"reino\s+['\"]([^'\"]+)['\"]", prompt, re.IGNORECASE)
        if not kingdom_match:
            kingdom_match = re.search(r"Reino:\s*([^\n\r]+)", prompt)
        if not kingdom_match:
            kingdom_match = re.search(r"reino\s+([A-Za-z0-9_ ]+)", prompt, re.IGNORECASE)
        kingdom_name = kingdom_match.group(1).strip() if kingdom_match else "Valdrin"

        ruler_match = re.search(r"Imperador(?:\(a\))?\s+['\"]([^'\"]+)['\"]", prompt, re.IGNORECASE)
        if not ruler_match:
            ruler_match = re.search(r"Imperador(?:\(a\))?:\s*([^\n\r]+)", prompt)
        ruler_name = ruler_match.group(1).strip() if ruler_match else "Arthur"

        rel_match = re.search(r"Religi[aã]o Oficial:\s*([^\n\r]+)", prompt, re.IGNORECASE)
        curr_rel = rel_match.group(1).strip() if rel_match else "Nenhuma"

        gold_match = re.search(r"Tesouro Real(?:\s*\(Ouro\))?:\s*([0-9\.,]+)", prompt, re.IGNORECASE)
        gold = int(re.sub(r"[^\d]", "", gold_match.group(1))) if gold_match else 5000

        pop_match = re.search(r"Popula[cç][aã]o(?:\s*do Reino)?:\s*([0-9\.,]+)", prompt, re.IGNORECASE)
        pop = int(re.sub(r"[^\d]", "", pop_match.group(1))) if pop_match else 10000

        mil_match = re.search(r"Poder Militar:\s*([0-9\.,]+)", prompt, re.IGNORECASE)
        mil = int(re.sub(r"[^\d]", "", mil_match.group(1))) if mil_match else 1000

        fel_match = re.search(r"Felicidade(?:\s*do Povo)?:\s*([0-9]+)%", prompt, re.IGNORECASE)
        fel = int(fel_match.group(1)) if fel_match else 70

        turn_match = re.search(r"Turno Atual:\s*([0-9]+)", prompt, re.IGNORECASE)
        turn = int(turn_match.group(1)) if turn_match else 1

        if "=== AÇÃO ATUAL DO JOGADOR ===" in prompt:
            user_action = prompt.split("=== AÇÃO ATUAL DO JOGADOR ===")[-1].strip()
        else:
            action_match = re.search(r"AÇÃO DO JOGADOR.*?:\s*(.+)", prompt, re.IGNORECASE)
            user_action = action_match.group(1).strip() if action_match else ""

        is_first_turn = "INÍCIO DE CAMPANHA" in user_action or curr_rel.lower() in ["nenhuma", "none", ""]
        actions = []

        if is_first_turn and "INÍCIO DE CAMPANHA" in user_action:
            aventura_text = (
                f"Saudações, Vossa Majestade {ruler_name}. O reino de {kingdom_name} recém-fundado ainda não possui uma fé oficial. "
                "Como primeiro ato de vosso reinado, qual doutrina espiritual devemos adotar para guiar nosso povo?\n"
                "1. Fundar a Ordem da Luz Divina para unificar a fé e abençoar nossas tropas\n"
                "2. Adorar os Antigos Deuses da Natureza e dos Elementos em comunhão com a terra\n"
                "3. Manter o Reino laico, investindo na Razão, Guildas de Comércio e Filosofia"
            )
            opcoes = [
                "1. Fundar a Ordem da Luz Divina para unificar a fé",
                "2. Adorar os Antigos Deuses da Natureza e dos Elementos",
                "3. Manter o Reino laico, investindo na Razão e Comércio"
            ]
            new_rel = "Nenhuma"
        elif is_first_turn:
            if "1" in user_action or "luz divina" in user_action.lower():
                new_rel = "Ordem da Luz Divina"
                gold -= 300
                mil += 150
                fel = min(100, fel + 10)
                aventura_text = (
                    f"Vossa Majestade proclamou a Ordem da Luz Divina como a fé suprema de {kingdom_name}! "
                    "Capelas foram erguidas e paladinos sagrados juraram lealdade à coroa. "
                    "Contudo, mensageiros relatam que comerciantes de reinos vizinhos e lordes florestais solicitam audiência urgente.\n"
                    "1. Convocar embaixadores élficos de Sylvandor para propor um tratado de não-agressão\n"
                    "2. Enviar batedores militares para mapear as Montanhas de Ferro em busca de minérios\n"
                    "3. Financiar um grande festival para celebrar a nova fé e alegrar o povo"
                )
                opcoes = [
                    "1. Convocar embaixadores de Sylvandor para tratado diplomático",
                    "2. Enviar batedores para mapear as Montanhas de Ferro",
                    "3. Financiar um grande festival real para celebrar a fé"
                ]
                actions.append({
                    "action_type": "add_item",
                    "payload": {
                        "id": "item_amuleto_luz",
                        "nome": "Amuleto da Luz Solar",
                        "categoria": "artefato",
                        "descricao": "Relíquia sagrada abençoada pela nova fé que fortalece o moral das tropas.",
                        "atributos": {"moral": "+15", "fe": "Sagrada"}
                    }
                })
                actions.append({
                    "action_type": "create_task",
                    "payload": {
                        "id": "quest_catedral_luz",
                        "titulo": "Construção da Grande Catedral",
                        "descricao": "Edificar o monumento sagrado da Ordem da Luz Divina na capital.",
                        "progresso": 25,
                        "duracao_estimada": "3 turnos",
                        "objetivo_esperado": "Consolidar a fé e aumentar a influência cultural.",
                        "is_incidente_dinamico": False
                    }
                })
            elif "2" in user_action or "natureza" in user_action.lower() or "antigos" in user_action.lower():
                new_rel = "Antigos Deuses da Natureza"
                pop += 500
                fel = min(100, fel + 15)
                gold -= 100
                aventura_text = (
                    f"A bênção dos Antigos Deuses da Natureza envolveu as terras de {kingdom_name}! "
                    "As colheitas floresceram com vigor impressionante e espíritos da floresta se aproximaram em paz. "
                    "Entretanto, feras selvagens foram avistadas na fronteira oriental.\n"
                    "1. Domesticar e recrutar Ursos de Guerra Ancestrais para a guarda real\n"
                    "2. Estabelecer entrepostos comerciais nas clareiras sagradas\n"
                    "3. Organizar uma expedição druídica para investigar as ruínas antigas"
                )
                opcoes = [
                    "1. Domesticar Ursos de Guerra Ancestrais para a guarda real",
                    "2. Estabelecer entrepostos comerciais nas clareiras sagradas",
                    "3. Organizar expedição druídica para investigar ruínas antigas"
                ]
                actions.append({
                    "action_type": "add_item",
                    "payload": {
                        "id": "item_semente_ancestral",
                        "nome": "Semente da Árvore da Vida",
                        "categoria": "artefato",
                        "descricao": "Broto sagrado que acelera o crescimento agrícola e cura enfermos.",
                        "atributos": {"fertilidade": "+20%", "vitalidade": "+10"}
                    }
                })
                actions.append({
                    "action_type": "create_task",
                    "payload": {
                        "id": "quest_circulo_druidas",
                        "titulo": "Comunhão com os Guardiões da Floresta",
                        "descricao": "Expandir o círculo sagrado de druidas e proteger as fronteiras naturais.",
                        "progresso": 30,
                        "duracao_estimada": "2 turnos",
                        "objetivo_esperado": "Obter apoio militar dos espíritos florestais.",
                        "is_incidente_dinamico": False
                    }
                })
            else:
                new_rel = "Reino Laico (Razão e Ciência)"
                gold += 600
                mil += 100
                fel = min(100, fel + 5)
                aventura_text = (
                    f"O reino de {kingdom_name} adotou a Razão, as Guildas e a Ciência como seus pilares! "
                    "Novos mercados foram abertos, atraindo artesãos, financistas e inventores talentosos. "
                    "Engenheiros reais apresentam seus primeiros projetos de expansão.\n"
                    "1. Construir uma grande oficina mecânica para criar trabucos e armaduras aprimoradas\n"
                    "2. Enviar caravanas comerciais para o Império de Ouroboros\n"
                    "3. Abrir a Academia Real de Arquitetura e Estratégia Militar"
                )
                opcoes = [
                    "1. Construir grande oficina mecânica para engenharia bélica",
                    "2. Enviar caravanas comerciais para o Império de Ouroboros",
                    "3. Fundar a Academia Real de Arquitetura e Estratégia"
                ]
                actions.append({
                    "action_type": "add_item",
                    "payload": {
                        "id": "item_grimorio_engenharia",
                        "nome": "Tratado de Engenharia Bélica",
                        "categoria": "equipamento",
                        "descricao": "Manual de táticas e mecânica avançada de fortificação.",
                        "atributos": {"defesa": "+15", "eficiencia": "+20%"}
                    }
                })
                actions.append({
                    "action_type": "create_task",
                    "payload": {
                        "id": "quest_academia_ciencias",
                        "titulo": "Fundação da Academia Real",
                        "descricao": "Construção de laboratórios e bibliotecas para pesquisa de novas tecnologias.",
                        "progresso": 20,
                        "duracao_estimada": "4 turnos",
                        "objetivo_esperado": "Desenvolver armaduras e métodos agrícolas avançados.",
                        "is_incidente_dinamico": False
                    }
                })
        else:
            new_rel = curr_rel
            action_lower = user_action.lower()
            if "posto" in action_lower or "avançado" in action_lower or "avancado" in action_lower or "santuario" in action_lower or "santuário" in action_lower or "constru" in action_lower or "fortaleza" in action_lower or "muralha" in action_lower:
                gold -= 350
                mil += 180
                fel = min(100, fel + 6)
                is_santuario = "santuario" in action_lower or "santuário" in action_lower
                is_posto = "posto" in action_lower or "avançado" in action_lower or "avancado" in action_lower
                
                if is_santuario:
                    nome_asset = "Santuário Sagrado das Montanhas"
                    cat_asset = "santuario"
                    desc_asset = "Local de contemplação espiritual e oração erguido por decreto do soberano."
                    attr_asset = {"fe": "+20", "harmonia": "+15"}
                elif is_posto:
                    nome_asset = "Posto Avançado do Norte"
                    cat_asset = "posto_avancado"
                    desc_asset = "Guarnição fortificada estabelecida na fronteira norte para patrulha e vigia."
                    attr_asset = {"defesa_fronteira": "+30", "vigilancia": "+25"}
                else:
                    nome_asset = "Fortificação da Fronteira"
                    cat_asset = "estrutura"
                    desc_asset = "Estrutura defensiva construída para salvaguardar o território do reino."
                    attr_asset = {"resistencia": "+25", "defesa": "+20"}

                aventura_text = (
                    f"A ordem de edificação em {kingdom_name} foi executada com precisão magistral! "
                    f"O {nome_asset} foi concluído e já fortalece as defesas e a glória de nossas terras. "
                    "Os batedores e operários agora aguardam vossas próximas diretrizes estratégicas.\n"
                    "1. Guarnecer a nova estrutura com tropas de arqueiros veteranos\n"
                    "2. Estabelecer entrepostos de comércio ao redor da construção\n"
                    "3. Expandir as patrulhas e mapear as regiões adjacentes"
                )
                opcoes = [
                    "1. Guarnecer a nova estrutura com tropas veteranas",
                    "2. Estabelecer entrepostos de comércio locais",
                    "3. Expandir patrulhas para regiões adjacentes"
                ]
                actions.append({
                    "action_type": "add_structure",
                    "payload": {
                        "id": f"asset_{cat_asset}_{turn}",
                        "nome": nome_asset,
                        "categoria": cat_asset,
                        "descricao": desc_asset,
                        "atributos": attr_asset
                    }
                })
            elif "diplomacia" in action_lower or "embaixador" in action_lower or "tratado" in action_lower or "aliad" in action_lower or "1" in action_lower:
                gold += 400
                pop += 300
                fel = min(100, fel + 5)
                aventura_text = (
                    f"As negociações diplomáticas de {kingdom_name} foram coroadas de glória! "
                    "O Reino Élfico de Sylvandor aceitou uma aliança militar e comercial vantajosa. "
                    "Caravanas de especiarias e arqueiros de elite chegaram à capital.\n"
                    "1. Organizar guarda de fronteira conjunta com arqueiros de Sylvandor\n"
                    "2. Abrir rota de comércio de pedras preciosas com os elfos\n"
                    "3. Construir fortalezas de vigia para proteger os comboios de suprimentos"
                )
                opcoes = [
                    "1. Estabelecer guarda de fronteira com arqueiros aliados",
                    "2. Abrir rota de comércio de pedras preciosas",
                    "3. Construir fortalezas de vigia na rota comercial"
                ]
                actions.append({
                    "action_type": "add_ally",
                    "payload": {
                        "id": "reino_sylvandor",
                        "nome": "Reino de Sylvandor",
                        "rei": "Arquidruida Thalor",
                        "raca": "Elfo",
                        "relacionamento": 75,
                        "status_diplomatico": "aliado",
                        "poder_militar": 2400,
                        "populacao": 18000,
                        "historico_notas": "Aliança formal selada após tratado de paz e comércio."
                    }
                })
                actions.append({
                    "action_type": "add_item",
                    "payload": {
                        "id": "item_arco_elfico",
                        "nome": "Arco Lunar de Sylvandor",
                        "categoria": "equipamento",
                        "descricao": "Arco forjado em madeira estelar concedido pela guarda real de Sylvandor.",
                        "atributos": {"ataque_distancia": "+25", "precisao": "+30%"}
                    }
                })
            elif "militar" in action_lower or "batedores" in action_lower or "urso" in action_lower or "guerra" in action_lower or "oficina" in action_lower or "2" in action_lower:
                mil += 250
                gold -= 200
                fel = max(10, fel - 2)
                aventura_text = (
                    f"O poderio militar de {kingdom_name} expandiu-se com bravura! "
                    "Nossos generais reportam que as patrulhas dominaram postos estratégicos e repeliram bandos de salteadores. "
                    "No entanto, mineradores encontraram um portal selado nas profundezas de uma caverna.\n"
                    "1. Enviar guardas de elite para deslacrar e explorar o portal arcano\n"
                    "2. Fortificar a entrada da caverna com muralhas e catapultas\n"
                    "3. Convocar sábios e alquimistas para decifrar as runas antigas"
                )
                opcoes = [
                    "1. Enviar guardas de elite para explorar o portal arcano",
                    "2. Fortificar a caverna com muralhas e catapultas",
                    "3. Convocar sábios e alquimistas para decifrar as runas"
                ]
                actions.append({
                    "action_type": "create_task",
                    "payload": {
                        "id": "incidente_portal_arcano",
                        "titulo": "Investigação do Portal Subterrâneo",
                        "descricao": "Forças arcanas desconhecidas emitem pulsos de energia nas minas.",
                        "progresso": 15,
                        "duracao_estimada": "2 turnos",
                        "objetivo_esperado": "Evitar invasão planar ou obter tesouros arcanos.",
                        "is_incidente_dinamico": True
                    }
                })
            else:
                gold += 500
                fel = min(100, fel + 8)
                pop += 200
                aventura_text = (
                    f"As medidas de prosperidade de Vossa Majestade encheram as praças de {kingdom_name} de júbilo! "
                    "O comércio está pujante, os artesãos prosperam e a moral do povo nunca esteve tão alta. "
                    "Guildas mercantis propõem novos investimentos de longo prazo.\n"
                    "1. Expandir o porto e construir navios de exploração marítima\n"
                    "2. Reduzir impostos das famílias rurais para impulsionar a agricultura\n"
                    "3. Treinar novos cavaleiros blindados para a guarda de honra"
                )
                opcoes = [
                    "1. Expandir o porto e construir navios de exploração",
                    "2. Reduzir impostos rurais para acelerar o crescimento populacional",
                    "3. Treinar cavaleiros blindados para a guarda de honra"
                ]
                actions.append({
                    "action_type": "add_item",
                    "payload": {
                        "id": "item_tesouro_guildas",
                        "nome": "Cálice de Ouro das Guildas",
                        "categoria": "artefato",
                        "descricao": "Símbolo de riqueza e prosperidade concedido pelos mercadores do reino.",
                        "atributos": {"renda_passiva": "+50 ouro/turno"}
                    }
                })

        return {
            "aventura": aventura_text,
            "opcoes": opcoes,
            "status_reino": {
                "nome_reino": kingdom_name,
                "imperador": ruler_name,
                "dinheiro": max(0, gold),
                "populacao": max(100, pop),
                "religião": new_rel,
                "poder_militar": max(50, mil),
                "felicidade": f"{fel}%"
            },
            "actions": actions
        }

    def generate_embedding(self, text: str) -> List[float]:
        return generate_fallback_embedding(text)


class FallbackLLMProvider(BaseLLMProvider):
    def __init__(self, primary: BaseLLMProvider, fallbacks: List[BaseLLMProvider]):
        self.primary = primary
        self.fallbacks = fallbacks

    @property
    def name(self) -> str:
        return f"{self.primary.name}_with_fallbacks"

    def is_available(self) -> bool:
        if self.primary.is_available():
            return True
        return any(f.is_available() for f in self.fallbacks)

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_text(prompt, system_instruction, temperature)
                except Exception as e:
                    print(f"Warning: Provider '{provider.name}' failed generate_text ({e}). Trying next fallback...")
        return MockFallbackProvider().generate_text(prompt, system_instruction, temperature)

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_json(prompt, system_instruction, temperature)
                except Exception as e:
                    print(f"Warning: Provider '{provider.name}' failed generate_json ({e}). Trying next fallback...")
        return MockFallbackProvider().generate_json(prompt, system_instruction, temperature)

    def generate_embedding(self, text: str) -> List[float]:
        candidates = [self.primary] + self.fallbacks
        for provider in candidates:
            if provider.is_available():
                try:
                    return provider.generate_embedding(text)
                except Exception as e:
                    pass
        return MockFallbackProvider().generate_embedding(text)


class LLMFactory:
    @staticmethod
    def get_provider(preferred_name: Optional[str] = None) -> BaseLLMProvider:
        provider_name = (preferred_name or config.DEFAULT_PROVIDER).lower()
        
        providers_map = {
            "gemini": GeminiProvider(),
            "grok": GrokProvider(),
            "openai": OpenAIProvider(),
            "ollama": OllamaProvider(),
            "mock_fallback": MockFallbackProvider(),
        }
        
        primary = providers_map.get(provider_name, GeminiProvider())
        fallbacks = [p for name, p in providers_map.items() if name != provider_name]
        if "mock_fallback" not in [p.name for p in fallbacks] and primary.name != "mock_fallback":
            fallbacks.append(MockFallbackProvider())
        
        return FallbackLLMProvider(primary, fallbacks)
