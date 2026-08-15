import pytest
from engine.domain.state_manager import GameEngine

@pytest.fixture
def test_engine(tmp_path):
    db_file = tmp_path / "test_domain_rpg.db"
    engine = GameEngine(db_path=str(db_file), provider_name="mock_fallback")
    yield engine
    engine.conn.close()

def test_game_engine_campaign_lifecycle(test_engine):
    # 1. Create campaign
    turn1 = test_engine.create_campaign(
        campaign_name="Reino dos Dragões",
        ruler_name="Valerius",
        kingdom_name="Valyria",
        race="Elfo"
    )
    assert turn1.aventura is not None
    assert turn1.status_reino is not None
    assert turn1.status_reino.populacao == 10000

    camps = test_engine.list_campaigns()
    assert len(camps) == 1
    camp_id = camps[0]["id"]

    # 2. Execute turn
    turn2 = test_engine.execute_turn(camp_id, "Fortalecer a guarda do castelo e treinar arqueiros.")
    assert turn2.aventura is not None
    assert turn2.status_reino is not None
    assert turn2.status_reino.populacao == 10000

    info = test_engine.get_campaign_info(camp_id)
    assert info is not None
    assert info.turn_number == 2
    assert info.latest_status.imperador is not None
    assert info.latest_status.populacao == 10000

def test_game_engine_rollback(test_engine):
    turn1 = test_engine.create_campaign("Reino do Norte", "Ned", "Winterfell", "Humano")
    camp_id = test_engine.list_campaigns()[0]["id"]
    
    turn2 = test_engine.execute_turn(camp_id, "Construir muralhas.")
    turn3 = test_engine.execute_turn(camp_id, "Recrutar soldados.")

    info = test_engine.get_campaign_info(camp_id)
    assert info.turn_number == 3

    # Rollback to Turn 1
    rolled = test_engine.rollback_turn(camp_id, 1)
    assert rolled.status_reino is not None

    info_after = test_engine.get_campaign_info(camp_id)
    assert info_after.turn_number == 1
    
    hist = test_engine.get_campaign_history(camp_id)
    assert len(hist) == 1

def test_game_engine_export_import(test_engine):
    turn1 = test_engine.create_campaign("Reino Solar", "Helios", "Solaria", "Elfo")
    camp_id = test_engine.list_campaigns()[0]["id"]
    test_engine.execute_turn(camp_id, "Organizar festival de verão.")

    exported = test_engine.export_campaign(camp_id)
    assert "version" in exported
    assert "campaign" in exported
    assert "world_states" in exported
    assert len(exported["world_states"]) == 2

    # Import with new ID
    imported_id = test_engine.import_campaign(exported)
    assert imported_id == camp_id

    info = test_engine.get_campaign_info(imported_id)
    assert info is not None
    assert info.turn_number == 2
    assert info.name == "Reino Solar"

def test_game_engine_memory_isolation(test_engine):
    t1 = test_engine.create_campaign("Campanha A", "Rei A", "Reino A", "Humano")
    cid_a = test_engine.list_campaigns()[0]["id"]
    
    t2 = test_engine.create_campaign("Campanha B", "Rei B", "Reino B", "Anão")
    cid_b = [c for c in test_engine.list_campaigns() if c["id"] != cid_a][0]["id"]

    test_engine.execute_turn(cid_a, "Ação exclusiva A")
    test_engine.execute_turn(cid_b, "Ação exclusiva B")

    mem_a = test_engine._get_short_term_memory(cid_a)
    mem_b = test_engine._get_short_term_memory(cid_b)

    assert any("exclusiva A" in m["user"] for m in mem_a)
    assert not any("exclusiva B" in m["user"] for m in mem_a)
    assert any("exclusiva B" in m["user"] for m in mem_b)

def test_game_engine_entities_and_delete(test_engine):
    t1 = test_engine.create_campaign("Reino da Floresta", "Silvanus", "Sylvan", "Elfo")
    cid = test_engine.list_campaigns()[0]["id"]

    test_engine.repo.upsert_character("npc1", cid, "Eldrin", role="Mago", relationship=20)
    test_engine.repo.upsert_quest("q1", cid, "Limpar floresta", "Derrotar aranhas")

    entities = test_engine.get_campaign_entities(cid)
    assert len(entities["characters"]) == 1
    assert entities["characters"][0]["name"] == "Eldrin"
    assert len(entities["quests"]) == 1
    assert entities["quests"][0]["title"] == "Limpar floresta"

    # Delete campaign
    deleted = test_engine.delete_campaign(cid)
    assert deleted is True
    assert test_engine.get_campaign_info(cid) is None


def test_game_engine_initial_religion_and_first_question(test_engine):
    turn1 = test_engine.create_campaign("Reino sem Fé", "Aethelred", "Wessex", "Humano")
    assert turn1.status_reino.religião == "Nenhuma"
    religion_keywords = ["fé", "doutrina", "religião", "luz divina", "laico", "sacerdotes", "crença", "culto", "deuses", "sagrado", "divino", "espiritual", "templo", "igreja", "filosofia", "panteão", "deus"]
    assert any(k in turn1.aventura.lower() for k in religion_keywords) or len(turn1.opcoes) >= 1

def test_clima_inference(test_engine):
    assert test_engine._infer_clima("frenetico", "Texto aleatorio") == "frenetico"
    assert test_engine._infer_clima("", "A grande batalha começou contra o exército inimigo!") == "frenetico"
    assert test_engine._infer_clima("", "A fome e a ruína se alastram pelo reino em meio ao caos.") == "desespero"
    assert test_engine._infer_clima("", "Celebramos a paz e a grande festa do reino.") == "harmonia"
    assert test_engine._infer_clima("", "Iniciamos a construção de novas obras e reformas.") == "desenvolvimento"
    assert test_engine._infer_clima("", "Os diplomatas reuniram-se em um conselho calmo.") == "calmo"
    assert test_engine._infer_clima("", "O bardo canta na taverna enquanto descansamos.") == "aventura"


def test_opcoes_extraction(test_engine):
    # Test JSON with explicit opcoes strings
    res1 = test_engine._extract_opcoes({"opcoes": ["1. A", "2. B", "3. C"]}, "texto")
    assert res1 == ["1. A", "2. B", "3. C"]

    # Test JSON with structured dict opcoes
    dict_opcoes = [
        {"texto": "1. Construir Igreja", "impacto": {"dinheiro": -500, "poder_militar": 0}},
        {"texto": "2. Centro de Treinamento", "impacto": {"dinheiro": -400, "poder_militar": 200}},
        {"texto": "3. Explorar", "impacto": {"dinheiro": None, "poder_militar": None}}
    ]
    res_dict = test_engine._extract_opcoes({"opcoes": dict_opcoes}, "texto")
    assert len(res_dict) == 3
    assert res_dict[0]["texto"] == "1. Construir Igreja"
    assert res_dict[0]["impacto"]["dinheiro"] == -500

    # Test line-by-line narrative extraction
    res2 = test_engine._extract_opcoes({}, "Aventura...\n1. Opcao Um\n2. Opcao Dois\n3. Opcao Tres")
    assert res2 == ["1. Opcao Um", "2. Opcao Dois", "3. Opcao Tres"]

    # Test inline narrative extraction
    inline_text = "O que deseja fazer? 1. Ordenar a construção. 2. Investir no exército. 3. Incentivos fiscais."
    res3 = test_engine._extract_opcoes({}, inline_text)
    assert len(res3) == 3
    assert res3[0].startswith("1.")
    assert res3[1].startswith("2.")
    assert res3[2].startswith("3.")

def test_estimate_action_impact(test_engine):
    turn1 = test_engine.create_campaign("Reino Teste", "Lider", "Valr", "Humano")
    camp_id = test_engine.list_campaigns()[0]["id"]

    est = test_engine.estimate_action_impact(camp_id, "Construir 2 quartéis para tropas")
    assert isinstance(est, dict)
    assert "dinheiro" in est
    assert "poder_militar" in est
    assert "explicacao" in est




