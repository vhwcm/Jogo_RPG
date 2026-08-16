import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from engine.domain.state_manager import GameEngine
from engine.providers.factory import LLMFactory
from server.dto import (
    CreateCampaignRequest,
    TurnRequest,
    TurnResponseDTO,
    KingdomStatusDTO,
    CampaignSummaryDTO,
    RollbackRequest,
    ImportCampaignRequest,
    EstimateActionRequest,
    GameActionDTO,
    StateDetailsDTO,
    PlaceAssetRequest
)

app = FastAPI(title="AI RPG Game Server API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GameEngine()

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "provider": engine.provider.name,
        "available": engine.provider.is_available(),
        "has_api_key": config.is_any_api_key_configured()
    }

@app.post("/api/campaigns", response_model=TurnResponseDTO)
def create_campaign(req: CreateCampaignRequest):
    try:
        if req.provider:
            engine.provider = LLMFactory.get_provider(req.provider)
        turn = engine.create_campaign(
            campaign_name=req.campaign_name,
            ruler_name=req.ruler_name,
            kingdom_name=req.kingdom_name,
            race=req.race
        )
        actions_dto = [GameActionDTO(action_type=a.action_type, payload=a.payload) for a in turn.actions]
        return TurnResponseDTO(
            campaign_id=turn.campaign_id,
            aventura=turn.aventura,
            clima=turn.clima,
            opcoes=turn.opcoes,
            status_reino=KingdomStatusDTO(**turn.status_reino.__dict__),
            actions=actions_dto,
            raw_json=turn.raw_json
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns")
def list_campaigns():
    return engine.list_campaigns()

@app.get("/api/campaigns/{campaign_id}")
def get_campaign_info(campaign_id: str):
    info = engine.get_campaign_info(campaign_id)
    if not info:
        raise HTTPException(status_code=404, detail="Campaign not found")
    status_dto = KingdomStatusDTO(**info.latest_status.__dict__) if info.latest_status else None
    return {
        "campaign_id": info.campaign_id,
        "name": info.name,
        "turn_number": info.turn_number,
        "summary": info.summary,
        "race": info.race,
        "status": status_dto
    }

@app.delete("/api/campaigns/{campaign_id}")
def delete_campaign(campaign_id: str):
    deleted = engine.delete_campaign(campaign_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"status": "success", "message": f"Campanha {campaign_id} removida com sucesso."}

@app.get("/api/campaigns/{campaign_id}/history")
def get_campaign_history(campaign_id: str):
    history = engine.get_campaign_history(campaign_id)
    return {"campaign_id": campaign_id, "history": history}

@app.get("/api/campaigns/{campaign_id}/entities")
def get_campaign_entities(campaign_id: str):
    return engine.get_campaign_entities(campaign_id)

@app.get("/api/campaign/{campaign_id}/state-details")
@app.get("/api/campaigns/{campaign_id}/state-details")
def get_campaign_state_details(campaign_id: str):
    return engine.get_campaign_state_details(campaign_id)

@app.post("/api/campaigns/{campaign_id}/rollback", response_model=TurnResponseDTO)
def rollback_campaign(campaign_id: str, req: RollbackRequest):
    try:
        turn = engine.rollback_turn(campaign_id, req.target_turn)
        actions_dto = [GameActionDTO(action_type=a.action_type, payload=a.payload) for a in turn.actions]
        return TurnResponseDTO(
            aventura=turn.aventura,
            clima=turn.clima,
            opcoes=turn.opcoes,
            status_reino=KingdomStatusDTO(**turn.status_reino.__dict__),
            actions=actions_dto,
            raw_json=turn.raw_json
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns/{campaign_id}/export")
def export_campaign(campaign_id: str):
    try:
        return engine.export_campaign(campaign_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@app.post("/api/campaigns/import")
def import_campaign(req: ImportCampaignRequest):
    try:
        cid = engine.import_campaign(req.campaign_data)
        return {"status": "success", "campaign_id": cid}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/campaigns/{campaign_id}/estimate_action")
def estimate_action(campaign_id: str, req: EstimateActionRequest):
    try:
        return engine.estimate_action_impact(campaign_id, req.action_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/turn", response_model=TurnResponseDTO)
def execute_turn(req: TurnRequest):
    try:
        turn = engine.execute_turn(req.campaign_id, req.player_action)
        actions_dto = [GameActionDTO(action_type=a.action_type, payload=a.payload) for a in turn.actions]
        return TurnResponseDTO(
            campaign_id=req.campaign_id,
            aventura=turn.aventura,
            clima=turn.clima,
            opcoes=turn.opcoes,
            status_reino=KingdomStatusDTO(**turn.status_reino.__dict__),
            actions=actions_dto,
            raw_json=turn.raw_json
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/campaigns/{campaign_id}/assets/{asset_id}/place_on_map")
def place_asset_on_map(campaign_id: str, asset_id: str, req: PlaceAssetRequest):
    try:
        result = engine.place_asset_on_map(
            campaign_id=campaign_id,
            asset_id=asset_id,
            x=req.x,
            y=req.y,
            node_type=req.node_type,
            size=req.size,
            connect_to_capital=req.connect_to_capital
        )
        return {"status": "success", "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/campaigns/{campaign_id}/assets/{asset_id}/unplace_from_map")
def unplace_asset_from_map(campaign_id: str, asset_id: str):
    try:
        success = engine.unplace_asset_from_map(campaign_id, asset_id)
        return {"status": "success", "unplaced": success}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/memories/{campaign_id}")
def get_memories(campaign_id: str, limit: int = 5):
    return engine.vector_store.get_recent_memories(campaign_id, limit=limit)

web_dir = Path(__file__).resolve().parent.parent / "web"
if web_dir.exists():
    app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="web")
