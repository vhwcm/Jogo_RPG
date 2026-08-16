import pytest
from engine.domain.models import Item, Task, ImperioAliado, GameAction, TurnResponse, KingdomStatus
from engine.domain.state_manager import GameEngine
from engine.db.schema import init_db
from engine.db.repository import Repository
from fastapi.testclient import TestClient
from server.app import app, engine
from engine.providers.factory import LLMFactory

@pytest.fixture
def test_engine(tmp_path):
    db_file = tmp_path / "test_actions_rpg.db"
    eng = GameEngine(db_path=str(db_file), provider_name="mock_fallback")
    yield eng
    eng.conn.close()

def test_models_instantiation():
    item = Item(
        id="item_1",
        nome="Espada Flamejante",
        categoria="equipamento",
        descricao="Uma espada forjada no fogo sagrado",
        atributos={"ataque": 50, "elemento": "fogo"},
        adquirido_no_turno=2
    )
    assert item.id == "item_1"
    assert item.nome == "Espada Flamejante"
    assert item.categoria == "equipamento"
    assert item.atributos["ataque"] == 50
    assert item.adquirido_no_turno == 2

    task = Task(
        id="task_1",
        titulo="Explorar Ruínas",
        descricao="Mapear as ruínas do templo antigo",
        status="em_andamento",
        progresso=25,
        duracao_estimada="2 turnos",
        objetivo_esperado="Encontrar relíquia",
        is_incidente_dinamico=False,
        criada_no_turno=1
    )
    assert task.id == "task_1"
    assert task.status == "em_andamento"
    assert task.progresso == 25
    assert task.is_incidente_dinamico is False

    ally = ImperioAliado(
        id="ally_1",
        nome="Reino dos Elfos de Sylva",
        rei="Elrond",
        populacao=25000,
        poder_militar=3500,
        relacionamento=75,
        status_diplomatico="amigavel",
        historico_notas="Tratado comercial firmado no turno 1"
    )
    assert ally.id == "ally_1"
    assert ally.relacionamento == 75
    assert ally.status_diplomatico == "amigavel"

    action = GameAction(
        action_type="add_item",
        payload={"id": "item_1", "nome": "Espada Flamejante"}
    )
    assert action.action_type == "add_item"
    assert action.payload["id"] == "item_1"

    status = KingdomStatus()
    turn_resp = TurnResponse(
        aventura="Texto de teste",
        status_reino=status,
        actions=[action]
    )
    assert len(turn_resp.actions) == 1
    assert turn_resp.actions[0].action_type == "add_item"

def test_repository_actions_crud(tmp_path):
    db_file = tmp_path / "test_repo_crud.db"
    conn = init_db(str(db_file))
    repo = Repository(conn)
    repo.create_campaign("camp1", "Campanha Teste")

    repo.upsert_campaign_item(
        item_id="it_1",
        campaign_id="camp1",
        nome="Dragão Ancião",
        categoria="criatura",
        descricao="Criatura alada ancestral",
        atributos={"poder_fogo": 90, "elemento": "fogo"},
        adquirido_no_turno=1
    )
    items = repo.get_campaign_items("camp1")
    assert len(items) == 1
    assert items[0]["nome"] == "Dragão Ancião"
    assert items[0]["categoria"] == "criatura"
    assert items[0]["atributos"]["poder_fogo"] == 90

    repo.upsert_campaign_task(
        task_id="tk_1",
        campaign_id="camp1",
        titulo="Construção da Grande Muralha",
        descricao="Fortificar as defesas",
        status="em_andamento",
        progresso=50,
        duracao_estimada="3 turnos",
        objetivo_esperado="Defesa impenetrável",
        is_incidente=False,
        criada_no_turno=1
    )
    tasks = repo.get_campaign_tasks("camp1")
    assert len(tasks) == 1
    assert tasks[0]["titulo"] == "Construção da Grande Muralha"
    assert tasks[0]["progresso"] == 50

    repo.upsert_campaign_ally(
        ally_id="al_1",
        campaign_id="camp1",
        nome="Ducado de Ferro",
        rei="Grom",
        populacao=12000,
        poder_militar=4000,
        relacionamento=60,
        status_diplomatico="aliado",
        historico_notas="Aliança defensiva"
    )
    allies = repo.get_campaign_allies("camp1")
    assert len(allies) == 1
    assert allies[0]["nome"] == "Ducado de Ferro"
    assert allies[0]["relacionamento"] == 60

    repo.delete_campaign_item("it_1", "camp1")
    assert len(repo.get_campaign_items("camp1")) == 0

    repo.delete_campaign_task("tk_1", "camp1")
    assert len(repo.get_campaign_tasks("camp1")) == 0

    repo.delete_campaign_ally("al_1", "camp1")
    assert len(repo.get_campaign_allies("camp1")) == 0
    conn.close()

def test_engine_apply_actions(test_engine):
    turn1 = test_engine.create_campaign("Reino Modular", "Arthur", "Valdrin", "Humano")
    camp_id = test_engine.list_campaigns()[0]["id"]

    actions = [
        GameAction(
            action_type="add_item",
            payload={
                "id": "dragao_1",
                "nome": "Dragão Guardião",
                "categoria": "criatura",
                "descricao": "Um jovem dragão domesticado",
                "atributos": {"forca": 100}
            }
        ),
        GameAction(
            action_type="create_task",
            payload={
                "id": "missao_1",
                "titulo": "Exploração do Norte",
                "descricao": "Mapear montanhas",
                "status": "em_andamento",
                "progresso": 10,
                "duracao_estimada": "4 turnos",
                "objetivo_esperado": "Encontrar minério",
                "is_incidente_dinamico": False
            }
        ),
        GameAction(
            action_type="add_ally",
            payload={
                "id": "imperio_elfos",
                "nome": "Império de Sylva",
                "rei": "Thranduil",
                "populacao": 30000,
                "poder_militar": 5000,
                "relacionamento": 80,
                "status_diplomatico": "aliado",
                "historico_notas": "Tratado de paz"
            }
        )
    ]

    test_engine.apply_actions(camp_id, actions, turn_number=2)

    details = test_engine.get_campaign_state_details(camp_id)
    assert len(details["items"]) == 1
    assert details["items"][0]["nome"] == "Dragão Guardião"
    assert len(details["tasks"]) == 1
    assert details["tasks"][0]["titulo"] == "Exploração do Norte"
    assert len(details["allies"]) == 1
    assert details["allies"][0]["nome"] == "Império de Sylva"

    update_actions = [
        GameAction(
            action_type="update_task",
            payload={
                "id": "missao_1",
                "status": "concluida",
                "progresso": 100
            }
        ),
        GameAction(
            action_type="update_ally",
            payload={
                "id": "imperio_elfos",
                "relacionamento": 95,
                "status_diplomatico": "aliado"
            }
        ),
        GameAction(
            action_type="remove_item",
            payload={"id": "dragao_1"}
        )
    ]

    test_engine.apply_actions(camp_id, update_actions, turn_number=3)

    updated_details = test_engine.get_campaign_state_details(camp_id)
    assert len(updated_details["items"]) == 0
    assert updated_details["tasks"][0]["status"] == "concluida"
    assert updated_details["tasks"][0]["progresso"] == 100
    assert updated_details["allies"][0]["relacionamento"] == 95

def test_api_state_details_and_turn_actions():
    client = TestClient(app)
    engine.provider = LLMFactory.get_provider("mock_fallback")

    resp = client.post("/api/campaigns", json={
        "campaign_name": "API Modular Campaign",
        "ruler_name": "Valerius",
        "kingdom_name": "Valyria",
        "race": "Elfo",
        "provider": "mock_fallback"
    })
    assert resp.status_code == 200
    camps = client.get("/api/campaigns").json()
    camp_id = [c for c in camps if c["name"] == "API Modular Campaign"][0]["id"]

    details_resp = client.get(f"/api/campaign/{camp_id}/state-details")
    assert details_resp.status_code == 200
    data = details_resp.json()
    assert "items" in data
    assert "tasks" in data
    assert "allies" in data

    alias_resp = client.get(f"/api/campaigns/{camp_id}/state-details")
    assert alias_resp.status_code == 200

def test_engine_apply_structures_and_assets(test_engine):
    test_engine.create_campaign("Reino das Estruturas", "Arthur", "Valdrin", "Humano")
    camp_id = test_engine.list_campaigns()[0]["id"]

    actions = [
        GameAction(
            action_type="add_structure",
            payload={
                "id": "posto_norte_1",
                "nome": "Posto Avançado do Norte",
                "categoria": "posto_avancado",
                "descricao": "Guarnição militar de vigilância nas montanhas geladas",
                "atributos": {"defesa": "+30", "vigilancia": "+20"}
            }
        ),
        GameAction(
            action_type="add_kingdom_asset",
            payload={
                "id": "santuario_luz_1",
                "nome": "Santuário da Chama Sagrada",
                "categoria": "santuario",
                "descricao": "Templo erguido para abençoar o reino e os fiéis",
                "atributos": {"fe": "+25", "cura": "+15"}
            }
        )
    ]

    test_engine.apply_actions(camp_id, actions, turn_number=2)

    details = test_engine.get_campaign_state_details(camp_id)
    items = details["items"]
    assert len(items) == 2
    
    posto = [i for i in items if i["id"] == "posto_norte_1"][0]
    assert posto["nome"] == "Posto Avançado do Norte"
    assert posto["categoria"] == "posto_avancado"
    assert posto["atributos"]["defesa"] == "+30"

    santuario = [i for i in items if i["id"] == "santuario_luz_1"][0]
    assert santuario["nome"] == "Santuário da Chama Sagrada"
    assert santuario["categoria"] == "santuario"
    assert santuario["atributos"]["fe"] == "+25"

    remove_actions = [
        GameAction(
            action_type="remove_structure",
            payload={"id": "posto_norte_1"}
        )
    ]
    test_engine.apply_actions(camp_id, remove_actions, turn_number=3)

    updated_details = test_engine.get_campaign_state_details(camp_id)
    assert len(updated_details["items"]) == 1
    assert updated_details["items"][0]["id"] == "santuario_luz_1"

def test_mock_fallback_building_orders(test_engine):
    test_engine.create_campaign("Reino de Teste", "Arthur", "Valdrin", "Humano")
    camp_id = test_engine.list_campaigns()[0]["id"]

    test_engine.execute_turn(camp_id, "1. Escolher Ordem da Luz Divina")
    turn_resp = test_engine.execute_turn(camp_id, "Construir um posto avançado no reino do norte")

    assert any(a.action_type in ["add_structure", "add_item", "add_kingdom_asset"] for a in turn_resp.actions)
    details = test_engine.get_campaign_state_details(camp_id)
    assert any("posto" in i["nome"].lower() or i["categoria"] == "posto_avancado" for i in details["items"])

