import os
import pytest
from engine.db.schema import init_db
from engine.db.repository import Repository

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_rpg.db"
    conn = init_db(str(db_file))
    yield conn
    conn.close()

def test_db_schema_creation(temp_db):
    cursor = temp_db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "campaigns" in tables
    assert "world_state" in tables
    assert "characters" in tables
    assert "quests" in tables
    assert "memories" in tables

def test_repository_campaign_crud(temp_db):
    repo = Repository(temp_db)
    camp = repo.create_campaign("c1", "Campanha Teste")
    assert camp["id"] == "c1"
    assert camp["name"] == "Campanha Teste"

    retrieved = repo.get_campaign("c1")
    assert retrieved is not None
    assert retrieved["name"] == "Campanha Teste"

    all_camps = repo.list_campaigns()
    assert len(all_camps) == 1

def test_repository_world_state(temp_db):
    repo = Repository(temp_db)
    repo.create_campaign("c1", "Campanha Teste")
    
    ws = repo.save_world_state(
        campaign_id="c1",
        turn_number=1,
        kingdom_name="Valdrin",
        ruler_name="Arthur",
        race="Humano",
        gold=6000,
        military=1500,
        happiness="80%",
        religion="Luz",
        population=12500
    )
    assert ws["gold"] == 6000
    assert ws["population"] == 12500
    
    latest = repo.get_latest_world_state("c1")
    assert latest is not None
    assert latest["turn_number"] == 1
    assert latest["kingdom_name"] == "Valdrin"
    assert latest["ruler_name"] == "Arthur"
    assert latest["population"] == 12500

def test_repository_characters_and_quests(temp_db):
    repo = Repository(temp_db)
    repo.create_campaign("c1", "Campanha Teste")
    
    repo.upsert_character("npc_1", "c1", "Marcus", role="Guarda Capitão", location="Portão", relationship=15)
    chars = repo.get_characters("c1")
    assert len(chars) == 1
    assert chars[0]["name"] == "Marcus"
    assert chars[0]["relationship_with_player"] == 15

    repo.upsert_quest("q1", "c1", "Procurar Princesa", "A princesa desapareceu", status="active")
    quests = repo.get_quests("c1")
    assert len(quests) == 1
    assert quests[0]["title"] == "Procurar Princesa"
