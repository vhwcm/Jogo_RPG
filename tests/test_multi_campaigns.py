import pytest
from engine.db.schema import init_db
from engine.db.repository import Repository
from engine.domain.state_manager import GameEngine
from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

@pytest.fixture
def temp_repo(tmp_path):
    db_file = tmp_path / "test_multi_rpg.db"
    conn = init_db(str(db_file))
    repo = Repository(conn)
    yield repo
    conn.close()

def test_list_campaigns_enriched_metadata(temp_repo):
    # 1. Create two campaigns
    temp_repo.create_campaign("c1", "Reino dos Elfos")
    temp_repo.create_campaign("c2", "Reino dos Anões")

    # 2. Add world states
    temp_repo.save_world_state(
        campaign_id="c1",
        turn_number=1,
        kingdom_name="Lothlórien",
        ruler_name="Elrond",
        race="Elfo",
        gold=7000,
        military=1200,
        happiness="85%",
        religion="Natureza"
    )
    temp_repo.save_world_state(
        campaign_id="c2",
        turn_number=1,
        kingdom_name="Erebor",
        ruler_name="Thorin",
        race="Anão",
        gold=9000,
        military=3000,
        happiness="75%",
        religion="Forja"
    )
    temp_repo.save_world_state(
        campaign_id="c2",
        turn_number=2,
        kingdom_name="Erebor",
        ruler_name="Thorin",
        race="Anão",
        gold=8500,
        military=2800,
        happiness="78%",
        religion="Forja"
    )

    # 3. List campaigns and check enriched metadata
    camps = temp_repo.list_campaigns()
    assert len(camps) == 2

    c2_data = [c for c in camps if c["id"] == "c2"][0]
    assert c2_data["kingdom_name"] == "Erebor"
    assert c2_data["ruler_name"] == "Thorin"
    assert c2_data["race"] == "Anão"
    assert c2_data["turn_number"] == 2

    c1_data = [c for c in camps if c["id"] == "c1"][0]
    assert c1_data["kingdom_name"] == "Lothlórien"
    assert c1_data["ruler_name"] == "Elrond"
    assert c1_data["race"] == "Elfo"
    assert c1_data["turn_number"] == 1

def test_api_multi_campaign_switching_and_history():
    # 1. Create Campaign A
    payload_a = {
        "campaign_name": "Aventura A",
        "ruler_name": "Rei A",
        "kingdom_name": "Reino A",
        "race": "Humano",
        "provider": "mock_fallback"
    }
    resp_a = client.post("/api/campaigns", json=payload_a)
    assert resp_a.status_code == 200

    # 2. Create Campaign B
    payload_b = {
        "campaign_name": "Aventura B",
        "ruler_name": "Rei B",
        "kingdom_name": "Reino B",
        "race": "Elfo",
        "provider": "mock_fallback"
    }
    resp_b = client.post("/api/campaigns", json=payload_b)
    assert resp_b.status_code == 200

    # 3. Verify listing contains both with details
    list_resp = client.get("/api/campaigns")
    assert list_resp.status_code == 200
    camps = list_resp.json()
    assert len(camps) >= 2

    camp_a = [c for c in camps if c["name"] == "Aventura A"][0]
    camp_b = [c for c in camps if c["name"] == "Aventura B"][0]

    assert camp_a["kingdom_name"] == "Reino A"
    assert camp_b["kingdom_name"] == "Reino B"

    # 4. Execute turn on Campaign A
    t_resp = client.post("/api/turn", json={"campaign_id": camp_a["id"], "player_action": "Expandir fronteiras"})
    assert t_resp.status_code == 200

    # 5. Get history of Campaign A and check user_action is present
    hist_resp = client.get(f"/api/campaigns/{camp_a['id']}/history")
    assert hist_resp.status_code == 200
    history = hist_resp.json()["history"]
    assert len(history) == 2
    assert history[1]["raw_state"]["user_action"] == "Expandir fronteiras"

    # 6. Delete Campaign A and confirm Campaign B remains
    del_resp = client.delete(f"/api/campaigns/{camp_a['id']}")
    assert del_resp.status_code == 200

    camps_after = client.get("/api/campaigns").json()
    ids_after = [c["id"] for c in camps_after]
    assert camp_a["id"] not in ids_after
    assert camp_b["id"] in ids_after

def test_api_campaign_open_updates_timestamp_and_order():
    resp_x = client.post("/api/campaigns", json={
        "campaign_name": "Aventura X",
        "ruler_name": "Rei X",
        "kingdom_name": "Reino X",
        "race": "Humano",
        "provider": "mock_fallback"
    })
    assert resp_x.status_code == 200

    resp_y = client.post("/api/campaigns", json={
        "campaign_name": "Aventura Y",
        "ruler_name": "Rei Y",
        "kingdom_name": "Reino Y",
        "race": "Anão",
        "provider": "mock_fallback"
    })
    assert resp_y.status_code == 200

    camps = client.get("/api/campaigns").json()
    camp_x = [c for c in camps if c["name"] == "Aventura X"][0]
    camp_y = [c for c in camps if c["name"] == "Aventura Y"][0]

    assert camps[0]["id"] == camp_y["id"]

    import time
    time.sleep(1)

    info_x_resp = client.get(f"/api/campaigns/{camp_x['id']}")
    assert info_x_resp.status_code == 200

    camps_reordered = client.get("/api/campaigns").json()
    assert camps_reordered[0]["id"] == camp_x["id"]

    client.delete(f"/api/campaigns/{camp_x['id']}")
    client.delete(f"/api/campaigns/{camp_y['id']}")
