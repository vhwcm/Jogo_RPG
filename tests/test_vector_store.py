import pytest
from engine.db.schema import init_db
from engine.db.repository import Repository
from engine.db.vector_store import VectorStore, cosine_similarity

@pytest.fixture
def vector_db(tmp_path):
    db_file = tmp_path / "test_vector.db"
    conn = init_db(str(db_file))
    repo = Repository(conn)
    repo.create_campaign("c1", "Campanha Teste")
    yield conn
    conn.close()

def test_cosine_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]
    assert pytest.approx(cosine_similarity(v1, v2), 0.001) == 1.0
    assert pytest.approx(cosine_similarity(v1, v3), 0.001) == 0.0

def test_vector_store_add_and_search(vector_db):
    vs = VectorStore(vector_db)
    vs.add_memory("c1", turn_number=1, content="Jogador roubou o cavalo de Marcus", importance=0.8, characters=["Marcus"], embedding=[1.0, 0.5, 0.0])
    vs.add_memory("c1", turn_number=2, content="Jogador comprou uma maçã", importance=0.1, characters=[], embedding=[0.0, 0.1, 0.9])

    memories = vs.search_memories("c1", query_embedding=[1.0, 0.5, 0.0], top_k=2)
    assert len(memories) == 2
    assert memories[0]["content"] == "Jogador roubou o cavalo de Marcus"
    assert memories[0]["similarity_score"] > memories[1]["similarity_score"]

def test_vector_store_character_filter(vector_db):
    vs = VectorStore(vector_db)
    vs.add_memory("c1", turn_number=1, content="Jogador falou com Marcus", importance=0.5, characters=["Marcus"])
    vs.add_memory("c1", turn_number=2, content="Jogador falou com Princesa", importance=0.5, characters=["Princesa"])

    memories = vs.search_memories("c1", character_filter="Marcus")
    assert len(memories) == 1
    assert "Marcus" in memories[0]["characters"]
