import pytest
from fastapi.testclient import TestClient
from server.app import app, engine
from engine.providers.factory import LLMFactory

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_mock_provider():
    engine.provider = LLMFactory.get_provider("mock_fallback")

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_api_campaign_creation_and_turn():
    # 1. Create Campaign
    payload = {
        "campaign_name": "API Test Kingdom",
        "ruler_name": "Kaelen",
        "kingdom_name": "Aethelgard",
        "race": "Humano",
        "provider": "mock_fallback"
    }
    resp = client.post("/api/campaigns", json=payload)
    if resp.status_code != 200:
        print("API Error Response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "aventura" in data
    assert "status_reino" in data
    assert "opcoes" in data
    assert isinstance(data["opcoes"], list)

    # 2. List Campaigns
    list_resp = client.get("/api/campaigns")
    assert list_resp.status_code == 200
    camps = list_resp.json()
    target_camp = [c for c in camps if c["name"] == "API Test Kingdom"][0]
    cid = target_camp["id"]

    # 3. Execute Turn
    turn_payload = {
        "campaign_id": cid,
        "player_action": "Enviar diplomatas para a cidade vizinha."
    }
    t_resp = client.post("/api/turn", json=turn_payload)
    assert t_resp.status_code == 200
    t_data = t_resp.json()
    assert "aventura" in t_data
    assert "opcoes" in t_data

    # 4. Get Memories
    mem_resp = client.get(f"/api/memories/{cid}")
    assert mem_resp.status_code == 200
    mems = mem_resp.json()
    assert isinstance(mems, list)

def test_api_state_management():
    # 1. Create Campaign
    payload = {
        "campaign_name": "State Management Kingdom",
        "ruler_name": "Aurelius",
        "kingdom_name": "Aurelia",
        "race": "Humano",
        "provider": "mock_fallback"
    }
    resp = client.post("/api/campaigns", json=payload)
    assert resp.status_code == 200
    camps = client.get("/api/campaigns").json()
    target_camp = [c for c in camps if c["name"] == "State Management Kingdom"][0]
    cid = target_camp["id"]

    # 2. Execute turn 2 & 3
    client.post("/api/turn", json={"campaign_id": cid, "player_action": "Treinar exército"})
    client.post("/api/turn", json={"campaign_id": cid, "player_action": "Coletar impostos"})

    # 3. Check history
    hist_resp = client.get(f"/api/campaigns/{cid}/history")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data["history"]) == 3

    # 4. Check entities
    ent_resp = client.get(f"/api/campaigns/{cid}/entities")
    assert ent_resp.status_code == 200
    assert "characters" in ent_resp.json()

    # 5. Rollback to Turn 1
    rb_resp = client.post(f"/api/campaigns/{cid}/rollback", json={"target_turn": 1})
    assert rb_resp.status_code == 200
    info_resp = client.get(f"/api/campaigns/{cid}")
    assert info_resp.json()["turn_number"] == 1

    # 6. Export Campaign
    exp_resp = client.get(f"/api/campaigns/{cid}/export")
    assert exp_resp.status_code == 200
    save_data = exp_resp.json()

    # 7. Delete Campaign
    del_resp = client.delete(f"/api/campaigns/{cid}")
    assert del_resp.status_code == 200

    # 8. Import Campaign
    imp_resp = client.post("/api/campaigns/import", json={"campaign_data": save_data})
    assert imp_resp.status_code == 200
    imported_cid = imp_resp.json()["campaign_id"]
    assert imported_cid == cid

