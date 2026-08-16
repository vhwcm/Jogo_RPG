try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default

from typing import List, Dict, Any, Optional, Union

class CreateCampaignRequest(BaseModel):
    campaign_name: str
    ruler_name: str
    kingdom_name: str
    race: str = "Humano"
    provider: Optional[str] = None

class TurnRequest(BaseModel):
    campaign_id: str
    player_action: str

class KingdomStatusDTO(BaseModel):
    nome_reino: str
    imperador: str
    dinheiro: int
    populacao: int = 10000
    religião: str
    poder_militar: int
    felicidade: str

class GameActionDTO(BaseModel):
    action_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)

class ItemDTO(BaseModel):
    id: str
    nome: str
    categoria: str
    descricao: str
    atributos: Dict[str, Any] = Field(default_factory=dict)
    adquirido_no_turno: int = 1

class TaskDTO(BaseModel):
    id: str
    titulo: str
    descricao: str
    status: str = "em_andamento"
    progresso: Optional[int] = None
    duracao_estimada: Optional[str] = None
    objetivo_esperado: Optional[str] = None
    is_incidente_dinamico: bool = False
    criada_no_turno: int = 1

class ImperioAliadoDTO(BaseModel):
    id: str
    nome: str
    rei: str
    populacao: Union[int, str]
    poder_militar: Union[int, str]
    relacionamento: int = 50
    status_diplomatico: str = "neutro"
    historico_notas: Optional[str] = None

class MapNodeDTO(BaseModel):
    id: str
    label: str
    node_type: str = "estrutura"
    emoji: str = "📍"
    x: float = 0.0
    y: float = 0.0
    status: str = "ativo"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MapEdgeDTO(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    edge_type: str = "estrada"
    descricao: str = ""

class StateDetailsDTO(BaseModel):
    items: List[Dict[str, Any]] = Field(default_factory=list)
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    allies: List[Dict[str, Any]] = Field(default_factory=list)
    map_nodes: List[Dict[str, Any]] = Field(default_factory=list)
    map_edges: List[Dict[str, Any]] = Field(default_factory=list)

class TurnResponseDTO(BaseModel):
    aventura: str
    clima: Optional[str] = "aventura"
    opcoes: Optional[List[Any]] = []
    status_reino: KingdomStatusDTO
    actions: Optional[List[GameActionDTO]] = []
    raw_json: Dict[str, Any]

class CampaignSummaryDTO(BaseModel):
    id: str
    name: str
    created_at: str
    summary: Optional[str] = ""

class RollbackRequest(BaseModel):
    target_turn: int

class ImportCampaignRequest(BaseModel):
    campaign_data: Dict[str, Any]

class EstimateActionRequest(BaseModel):
    action_text: str
