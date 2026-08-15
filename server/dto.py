try:
    from pydantic import BaseModel
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__

from typing import List, Dict, Any, Optional

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

class TurnResponseDTO(BaseModel):
    aventura: str
    clima: Optional[str] = "aventura"
    opcoes: Optional[List[Any]] = []
    status_reino: KingdomStatusDTO
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


