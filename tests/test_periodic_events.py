import pytest
from engine.db.schema import init_db
from engine.db.repository import Repository
from engine.domain.state_manager import GameEngine
from engine.domain.models import GameAction

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_periodic.db"
    conn = init_db(str(db_file))
    yield conn, str(db_file)
    conn.close()

def test_periodic_events_crud(temp_db):
    conn, _ = temp_db
    repo = Repository(conn)
    repo.create_campaign("c_pe", "Reino Temporal")

    repo.upsert_periodic_event(
        event_id="pe_1",
        campaign_id="c_pe",
        titulo="Tributo Anual",
        intervalo_dias=365,
        proximo_disparo_dia=365,
        descricao="Pagamento de tributo",
        efeito={"dinheiro": 1000}
    )

    events = repo.get_periodic_events("c_pe")
    assert len(events) == 1
    assert events[0]["titulo"] == "Tributo Anual"
    assert events[0]["intervalo_dias"] == 365
    assert events[0]["proximo_disparo_dia"] == 365
    assert events[0]["efeito"]["dinheiro"] == 1000

    due_before = repo.get_due_periodic_events("c_pe", current_day=100)
    assert len(due_before) == 0

    due_after = repo.get_due_periodic_events("c_pe", current_day=370)
    assert len(due_after) == 1
    assert due_after[0]["id"] == "pe_1"

    deleted = repo.delete_periodic_event("pe_1", "c_pe")
    assert deleted is True
    assert len(repo.get_periodic_events("c_pe")) == 0

def test_campaign_tasks_with_temporal_fields(temp_db):
    conn, _ = temp_db
    repo = Repository(conn)
    repo.create_campaign("c_tk", "Reino Tasks")

    repo.upsert_campaign_task(
        task_id="t_exploracao",
        campaign_id="c_tk",
        titulo="Explorar Floresta Ancestral",
        descricao="Batedores enviados para o norte",
        status="em_andamento",
        progresso=0,
        dia_inicio=15,
        dias_estimados=45,
        criada_no_turno=2
    )

    tasks = repo.get_campaign_tasks("c_tk")
    assert len(tasks) == 1
    assert tasks[0]["dia_inicio"] == 15
    assert tasks[0]["dias_estimados"] == 45
    assert tasks[0]["status"] == "em_andamento"

def test_game_engine_turn_flow_and_days_progression(temp_db):
    _, db_path = temp_db
    engine = GameEngine(db_path=db_path, provider_name="mock")

    turn1 = engine.create_campaign(
        campaign_name="Campanha Temporal",
        ruler_name="Valerius",
        kingdom_name="Aethelgard",
        race="Humano"
    )

    assert turn1.status_reino.dia_atual == 1
    assert turn1.status_reino.dias_passados == 0
    cid = engine.list_campaigns()[0]["id"]

    turn2 = engine.execute_turn(cid, "quero fazer 1 e 2")
    assert turn2.status_reino.dia_atual > 1
    assert turn2.status_reino.dias_passados >= 1

    state_details = engine.get_campaign_state_details(cid)
    assert "periodic_events" in state_details

def test_tax_collection_event_created_on_campaign_start(temp_db):
    _, db_path = temp_db
    engine = GameEngine(db_path=db_path, provider_name="mock")

    turn1 = engine.create_campaign(
        campaign_name="Campanha de Impostos",
        ruler_name="Aurelius",
        kingdom_name="Imperium",
        race="Humano"
    )
    cid = engine.list_campaigns()[0]["id"]
    events = engine.repo.get_periodic_events(cid)
    tax_event = next((e for e in events if e["id"] == "recolhimento_impostos" or "Impostos" in e["titulo"]), None)

    assert tax_event is not None
    assert tax_event["titulo"] == "Recolhimento de Impostos"
    assert tax_event["intervalo_dias"] == 30
    assert tax_event["proximo_disparo_dia"] == 30
    assert tax_event["status"] == "ativo"
    assert "formula" in tax_event["efeito"]
    assert "(populacao * 0.05) * (felicidade / 100)" in tax_event["efeito"]["formula"]

def test_tax_collection_event_triggers_and_adds_gold(temp_db):
    _, db_path = temp_db
    engine = GameEngine(db_path=db_path, provider_name="mock")

    engine.create_campaign(
        campaign_name="Campanha de Impostos Recorrente",
        ruler_name="Aurelius",
        kingdom_name="Imperium",
        race="Humano"
    )
    cid = engine.list_campaigns()[0]["id"]

    engine.repo.save_world_state(
        campaign_id=cid,
        turn_number=1,
        kingdom_name="Imperium",
        ruler_name="Aurelius",
        race="Humano",
        gold=5000,
        population=10000,
        military=1000,
        happiness="70%",
        religion="Nenhuma",
        current_day=29,
        raw_state_json={"opcoes": [{"texto": "1. Patrulhar", "impacto": {"dinheiro": 0, "poder_militar": 0}}]}
    )

    turn2 = engine.execute_turn(cid, "patrulhar as fronteiras")
    assert turn2.status_reino.dia_atual >= 30
    expected_tax = int(round((10000 * 0.05) * 0.70))
    assert expected_tax == 350
    assert turn2.status_reino.dinheiro == 5000 + expected_tax

    updated_events = engine.repo.get_periodic_events(cid)
    tax_event = next((e for e in updated_events if "recolhimento_impostos" in e["id"] or "Impostos" in e["titulo"]), None)
    assert tax_event["ultimo_disparo_dia"] == turn2.status_reino.dia_atual
    assert tax_event["proximo_disparo_dia"] >= 60

def test_tax_rate_modification_and_dynamic_calculation(temp_db):
    _, db_path = temp_db
    engine = GameEngine(db_path=db_path, provider_name="mock")

    engine.create_campaign(
        campaign_name="Campanha Reforma Tributaria",
        ruler_name="Aurelius",
        kingdom_name="Imperium",
        race="Humano"
    )
    cid = engine.list_campaigns()[0]["id"]

    engine.apply_actions(
        campaign_id=cid,
        actions=[
            GameAction(
                action_type="update_periodic_event",
                payload={
                    "id": "recolhimento_impostos",
                    "efeito": {
                        "tipo": "formula",
                        "recurso": "dinheiro",
                        "formula": "(populacao * 0.08) * (felicidade / 100)",
                        "aliquota": 0.08
                    }
                }
            )
        ],
        turn_number=1,
        current_day=1
    )

    events = engine.repo.get_periodic_events(cid)
    tax_event = next((e for e in events if "recolhimento_impostos" in e["id"] or "Impostos" in e["titulo"]), None)
    assert tax_event["efeito"]["formula"] == "(populacao * 0.08) * (felicidade / 100)"

    engine.repo.save_world_state(
        campaign_id=cid,
        turn_number=1,
        kingdom_name="Imperium",
        ruler_name="Aurelius",
        race="Humano",
        gold=5000,
        population=10000,
        military=1000,
        happiness="70%",
        religion="Nenhuma",
        current_day=29,
        raw_state_json={"opcoes": [{"texto": "1. Patrulhar", "impacto": {"dinheiro": 0, "poder_militar": 0}}]}
    )

    turn2 = engine.execute_turn(cid, "patrulhar as fronteiras")
    expected_new_tax = int(round((10000 * 0.08) * 0.70))
    assert expected_new_tax == 560
    assert turn2.status_reino.dinheiro == 5000 + expected_new_tax
