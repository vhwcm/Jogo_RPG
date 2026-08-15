from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

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
    raw_json: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CampaignInfo:
    campaign_id: str
    name: str
    turn_number: int
    summary: str = ""
    race: str = "Humano"
    latest_status: Optional[KingdomStatus] = None

