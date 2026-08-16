import pytest
from engine.domain.models import MapNode, MapEdge, GameAction, KingdomStatus, TurnResponse
from engine.domain.state_manager import GameEngine
from engine.db.schema import init_db
from engine.db.repository import Repository
from fastapi.testclient import TestClient
from server.app import app

@pytest.fixture
def test_engine(tmp_path):
    db_file = tmp_path / "test_map_rpg.db"
    eng = GameEngine(db_path=str(db_file), provider_name="mock_fallback")
    yield eng
    eng.conn.close()

def test_map_models_instantiation():
    node = MapNode(
        id="node_1",
        label="Fortaleza do Norte",
        node_type="fortificacao",
        emoji="🛡️",
        x=120.5,
        y=-45.2,
        status="ativo",
        metadata={"tropas": 300, "nivel": 2}
    )
    assert node.id == "node_1"
    assert node.label == "Fortaleza do Norte"
    assert node.node_type == "fortificacao"
    assert node.emoji == "🛡️"
    assert node.x == 120.5
    assert node.y == -45.2
    assert node.status == "ativo"
    assert node.metadata["tropas"] == 300

    edge = MapEdge(
        id="edge_1",
        source_node_id="node_1",
        target_node_id="node_2",
        edge_type="estrada",
        descricao="Estrada Real"
    )
    assert edge.id == "edge_1"
    assert edge.source_node_id == "node_1"
    assert edge.target_node_id == "node_2"
    assert edge.edge_type == "estrada"
    assert edge.descricao == "Estrada Real"

def test_repository_map_nodes_and_edges(test_engine):
    repo = test_engine.repo
    cid = "test_camp_map"
    repo.create_campaign(cid, "Campanha do Mapa")

    repo.upsert_map_node(
        node_id="n1",
        campaign_id=cid,
        label="Capital Central",
        node_type="capital",
        emoji="🏰",
        x=0.0,
        y=0.0,
        status="ativo",
        metadata={"tropas": 1000}
    )
    repo.upsert_map_node(
        node_id="n2",
        campaign_id=cid,
        label="Mina Profunda",
        node_type="mina",
        emoji="⛏️",
        x=150.0,
        y=-80.0,
        status="descoberto",
        metadata={"recursos": "ouro"}
    )

    nodes = repo.get_map_nodes(cid)
    assert len(nodes) == 2
    assert nodes[0]["id"] == "n1"
    assert nodes[0]["metadata"]["tropas"] == 1000
    assert nodes[1]["id"] == "n2"
    assert nodes[1]["emoji"] == "⛏️"

    repo.upsert_map_edge(
        edge_id="e1",
        campaign_id=cid,
        source_node_id="n1",
        target_node_id="n2",
        edge_type="rota_comercial",
        descricao="Caminho dos Mineiros"
    )

    edges = repo.get_map_edges(cid)
    assert len(edges) == 1
    assert edges[0]["id"] == "e1"
    assert edges[0]["source_node_id"] == "n1"
    assert edges[0]["target_node_id"] == "n2"

    deleted_edge = repo.delete_map_edge("e1", cid)
    assert deleted_edge is True
    assert len(repo.get_map_edges(cid)) == 0

    repo.upsert_map_edge(
        edge_id="e2",
        campaign_id=cid,
        source_node_id="n1",
        target_node_id="n2",
        edge_type="estrada"
    )
    repo.delete_map_edge_between(cid, "n2", "n1")
    assert len(repo.get_map_edges(cid)) == 0

    repo.upsert_map_edge(
        edge_id="e3",
        campaign_id=cid,
        source_node_id="n1",
        target_node_id="n2",
        edge_type="fronteira"
    )
    repo.delete_map_node("n1", cid)
    assert len(repo.get_map_nodes(cid)) == 1
    assert len(repo.get_map_edges(cid)) == 0

def test_initial_campaign_creation_seeds_map(test_engine):
    turn = test_engine.create_campaign(
        campaign_name="Reino Imperial",
        ruler_name="Arthur",
        kingdom_name="Valoria",
        race="Humano"
    )
    camps = test_engine.list_campaigns()
    cid = camps[0]["id"]

    details = test_engine.get_campaign_state_details(cid)
    map_nodes = details["map_nodes"]
    map_edges = details["map_edges"]

    assert len(map_nodes) >= 4
    capital = next((n for n in map_nodes if n["id"] == "node_capital"), None)
    assert capital is not None
    assert capital["label"] == "Capital Valoria"
    assert capital["emoji"] == "🏰"
    assert capital["x"] == 0.0
    assert capital["y"] == 0.0

    forest = next((n for n in map_nodes if n["id"] == "node_floresta_ancestral"), None)
    assert forest is not None
    assert forest["emoji"] == "🌲"

    assert len(map_edges) >= 3

def test_apply_map_actions(test_engine):
    turn = test_engine.create_campaign(
        campaign_name="Guerra das Sombras",
        ruler_name="Elric",
        kingdom_name="Melnibone",
        race="Elfo"
    )
    cid = test_engine.list_campaigns()[0]["id"]

    actions = [
        GameAction(
            action_type="add_map_node",
            payload={
                "id": "node_acampamento_orcs",
                "label": "Acampamento Orc",
                "node_type": "tropa",
                "emoji": "⚔️",
                "status": "hostil",
                "metadata": {"tropas": 400, "perigo": "Alto"},
                "connect_to": "node_capital",
                "edge_type": "fronteira"
            }
        ),
        GameAction(
            action_type="add_map_node",
            payload={
                "label": "Ruínas do Templo Solar",
                "node_type": "ruina",
                "status": "descoberto",
                "metadata": {"reliquia": "Amuleto do Sol"}
            }
        )
    ]
    test_engine.apply_actions(cid, actions, turn_number=2)

    details = test_engine.get_campaign_state_details(cid)
    nodes = details["map_nodes"]
    edges = details["map_edges"]

    orc_node = next((n for n in nodes if n["id"] == "node_acampamento_orcs"), None)
    assert orc_node is not None
    assert orc_node["label"] == "Acampamento Orc"
    assert orc_node["status"] == "hostil"
    assert orc_node["metadata"]["tropas"] == 400

    ruin_node = next((n for n in nodes if "Ruínas do Templo Solar" in n["label"]), None)
    assert ruin_node is not None
    assert ruin_node["emoji"] == "🏚️"
    assert ruin_node["x"] != 0.0 or ruin_node["y"] != 0.0

    connected_edge = next((e for e in edges if e["target_node_id"] == "node_acampamento_orcs" or e["source_node_id"] == "node_acampamento_orcs"), None)
    assert connected_edge is not None
    assert connected_edge["edge_type"] == "fronteira"

    update_actions = [
        GameAction(
            action_type="update_map_node",
            payload={
                "id": "node_acampamento_orcs",
                "status": "pacificado",
                "metadata": {"tropas": 0, "perigo": "Nenhum"}
            }
        ),
        GameAction(
            action_type="connect_map_nodes",
            payload={
                "source_node_id": "node_floresta_ancestral",
                "target_node_id": ruin_node["id"],
                "edge_type": "rota",
                "descricao": "Trilha Escondida"
            }
        )
    ]
    test_engine.apply_actions(cid, update_actions, turn_number=3)

    details_after = test_engine.get_campaign_state_details(cid)
    updated_orc = next(n for n in details_after["map_nodes"] if n["id"] == "node_acampamento_orcs")
    assert updated_orc["status"] == "pacificado"
    assert updated_orc["metadata"]["tropas"] == 0

    trilha_edge = next(e for e in details_after["map_edges"] if e["source_node_id"] == "node_floresta_ancestral" and e["target_node_id"] == ruin_node["id"])
    assert trilha_edge["edge_type"] == "rota"
    assert trilha_edge["descricao"] == "Trilha Escondida"

    remove_actions = [
        GameAction(
            action_type="remove_map_node",
            payload={"id": "node_acampamento_orcs"}
        )
    ]
    test_engine.apply_actions(cid, remove_actions, turn_number=4)

    details_final = test_engine.get_campaign_state_details(cid)
    assert not any(n["id"] == "node_acampamento_orcs" for n in details_final["map_nodes"])
    assert not any(e["target_node_id"] == "node_acampamento_orcs" or e["source_node_id"] == "node_acampamento_orcs" for e in details_final["map_edges"])

def test_export_import_campaign_with_map(test_engine):
    test_engine.create_campaign("Império Solar", "Helios", "Solaria", "Humano")
    cid = test_engine.list_campaigns()[0]["id"]

    exported = test_engine.export_campaign(cid)
    assert "map_nodes" in exported["entities"]
    assert "map_edges" in exported["entities"]
    assert len(exported["entities"]["map_nodes"]) >= 4

    test_engine.delete_campaign(cid)
    imported_cid = test_engine.import_campaign(exported)

    details = test_engine.get_campaign_state_details(imported_cid)
    assert len(details["map_nodes"]) >= 4
    assert len(details["map_edges"]) >= 3

def test_api_state_details_and_turn():
    client = TestClient(app)

    create_resp = client.post("/api/campaigns", json={
        "campaign_name": "Campanha Teste API Mapa Unica",
        "ruler_name": "Rei Arthur",
        "kingdom_name": "Camelot",
        "race": "Humano",
        "provider": "mock_fallback"
    })
    assert create_resp.status_code == 200

    camps_resp = client.get("/api/campaigns")
    camps = camps_resp.json()
    matched = [c for c in camps if c["name"] == "Campanha Teste API Mapa Unica"]
    assert len(matched) > 0
    cid = matched[0]["id"]

    details_resp = client.get(f"/api/campaigns/{cid}/state-details")
    assert details_resp.status_code == 200
    data = details_resp.json()
    assert "map_nodes" in data
    assert "map_edges" in data
    assert len(data["map_nodes"]) >= 4
