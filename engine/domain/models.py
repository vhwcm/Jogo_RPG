from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union

@dataclass
class Item:
    id: str
    nome: str
    categoria: str
    descricao: str
    atributos: Dict[str, Any] = field(default_factory=dict)
    adquirido_no_turno: int = 1

@dataclass
class Task:
    id: str
    titulo: str
    descricao: str
    status: str = "em_andamento"
    progresso: Optional[int] = None
    duracao_estimada: Optional[str] = None
    objetivo_esperado: Optional[str] = None
    is_incidente_dinamico: bool = False
    dia_inicio: int = 1
    dias_estimados: int = 0
    criada_no_turno: int = 1

@dataclass
class PeriodicEvent:
    id: str
    campaign_id: str
    titulo: str
    intervalo_dias: int
    proximo_disparo_dia: int
    descricao: str = ""
    ultimo_disparo_dia: int = 0
    efeito: Dict[str, Any] = field(default_factory=dict)
    status: str = "ativo"
    criado_no_turno: int = 1

AVAILABLE_RACES: List[str] = [
    "Humano",
    "Elfo",
    "Anão",
    "Orc",
    "Centauro",
    "Demônio",
    "Djinn",
    "Dragão",
    "Elemental",
    "Fauno",
    "Gnomo",
    "Goblin",
    "Leprechaun",
    "Mago",
    "Morto Vivo",
    "Rinoceronte",
    "Sereia",
    "Trol",
    "Vampiro"
]

@dataclass
class ImperioAliado:
    id: str
    nome: str
    rei: str
    populacao: Union[int, str]
    poder_militar: Union[int, str]
    raca: str = "Humano"
    relacionamento: int = 50
    status_diplomatico: str = "neutro"
    historico_notas: Optional[str] = None

@dataclass
class MapNode:
    id: str
    label: str
    node_type: str = "estrutura"
    emoji: str = "📍"
    x: float = 0.0
    y: float = 0.0
    status: str = "ativo"
    size: str = "medio"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MapEdge:
    id: str
    source_node_id: str
    target_node_id: str
    edge_type: str = "estrada"
    descricao: str = ""

@dataclass
class GameAction:
    action_type: str
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KingdomStatus:
    nome_reino: str = "Reino de Valdrin"
    imperador: str = "Majestade"
    dinheiro: int = 5000
    populacao: int = 10000
    religião: str = "Nenhuma"
    poder_militar: int = 1000
    felicidade: str = "70%"
    dia_atual: int = 1
    dias_passados: int = 0

@dataclass
class ImpactoPrevisto:
    dinheiro: Optional[int] = None
    poder_militar: Optional[int] = None
    populacao: Optional[int] = None

@dataclass
class OpcaoDecisao:
    texto: str
    impacto: Optional[ImpactoPrevisto] = None

@dataclass
class EvaluationResult:
    intencao_detectada: str
    opcoes_selecionadas: List[int] = field(default_factory=list)
    delta_dinheiro: Optional[int] = None
    delta_poder_militar: Optional[int] = None
    delta_populacao: Optional[int] = None
    delta_felicidade: Optional[int] = None
    dias_passados: int = 1
    tipo_execucao: str = "imediata"
    dias_duracao_tarefa: Optional[int] = None
    viabilidade: bool = True
    motivo_inviabilidade: str = ""
    diretrizes_narrador: str = ""
    eventos_periodicos_disparados: List[Dict[str, Any]] = field(default_factory=list)
    tarefas_atualizadas: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class TurnResponse:
    aventura: str
    status_reino: KingdomStatus
    clima: str = "aventura"
    opcoes: List[Any] = field(default_factory=list)
    actions: List[GameAction] = field(default_factory=list)
    raw_json: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CampaignInfo:
    campaign_id: str
    name: str
    turn_number: int
    summary: str = ""
    race: str = "Humano"
    latest_status: Optional[KingdomStatus] = None
