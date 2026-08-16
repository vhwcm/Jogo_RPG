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
    criada_no_turno: int = 1

@dataclass
class ImperioAliado:
    id: str
    nome: str
    rei: str
    populacao: Union[int, str]
    poder_militar: Union[int, str]
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
