# 🏰 Domain: Kingdom State & Decisions

## Purpose
Gerenciar o estado determinístico dos recursos do reino e o modelo de impacto de decisões a cada turno.

---

## Entities & Models (`engine/domain/models.py`)

```python
@dataclass
class KingdomStatus:
    nome_reino: str
    imperador: str
    dinheiro: int
    populacao: int
    religião: str
    poder_militar: int
    felicidade: str

@dataclass
class ImpactoPrevisto:
    dinheiro: Optional[int]
    poder_militar: Optional[int]

@dataclass
class OpcaoDecisao:
    texto: str
    impacto: Optional[ImpactoPrevisto]

@dataclass
class TurnResponse:
    aventura: str
    clima: str
    opcoes: List[OpcaoDecisao]
    status_reino: KingdomStatus
    turno_atual: int
    personagens_novos: Optional[List[Dict[str, Any]]] = None
    quests_novas: Optional[List[Dict[str, Any]]] = None
```

---

## Business Rules

1. **Métricas Estruturadas**:
   - `dinheiro`: Saldo monetário em tesouro real (inteiro).
   - `populacao`: Quantidade de cidadãos (inteiro sanitizado, sem pontos/vírgulas no parse).
   - `poder_militar`: Capacidade bélica do exército (inteiro).
   - `felicidade`: Humor geral da população, sempre com formato percentual (ex: `"70%"`).
   - `religião`: Fé patrona do reino (definida no Turno 1).

2. **Opções e Estimativas de Impacto**:
   - Cada turno gera 3 opções enumeradas recomendadas pelo Game Master.
   - Opcionalmente, cada opção traz previsões numéricas de ganho ou perda de recursos (`dinheiro`, `poder_militar`). Valores desconhecidos são representados por `null`.
   - O jogador também tem a liberdade de enviar uma ação em texto livre (`free-text action`).

3. **Clima Emocional (`clima`)**:
   - Classificação do tom do turno: `aventura`, `calmo`, `desenvolvimento`, `frenetico`, `desespero`, `harmonia`.
   - Caso o LLM gere um clima inválido ou omita o campo, o `GameEngine._infer_clima()` realiza inferência por palavras-chave na narrativa.

---

## Related Code
- `engine/domain/models.py`: Modelos `KingdomStatus`, `OpcaoDecisao`, `TurnResponse`.
- `engine/domain/state_manager.py`: `_process_turn_response`, `_infer_clima`, `execute_turn`.
- `engine/db/repository.py`: `save_world_state`, `get_latest_world_state`, `get_history`.
