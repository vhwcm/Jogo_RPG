import sqlite3
import os
from pathlib import Path

CREATE_CAMPAIGNS_TABLE = """
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary TEXT DEFAULT ''
);
"""

CREATE_WORLD_STATE_TABLE = """
CREATE TABLE IF NOT EXISTS world_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT NOT NULL,
    turn_number INTEGER NOT NULL,
    kingdom_name TEXT NOT NULL,
    ruler_name TEXT NOT NULL,
    race TEXT NOT NULL,
    gold INTEGER DEFAULT 5000,
    population INTEGER DEFAULT 10000,
    military INTEGER DEFAULT 1000,
    happiness TEXT DEFAULT '70%',
    religion TEXT DEFAULT 'Nenhuma',
    raw_state_json TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CHARACTERS_TABLE = """
CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'NPC',
    location TEXT DEFAULT 'Valdrin',
    is_alive INTEGER DEFAULT 1,
    relationship_with_player INTEGER DEFAULT 0,
    knowledge_json TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_QUESTS_TABLE = """
CREATE TABLE IF NOT EXISTS quests (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    status TEXT DEFAULT 'active',
    objective TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    name TEXT NOT NULL,
    owner TEXT DEFAULT 'player',
    quantity INTEGER DEFAULT 1,
    properties_json TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_LOCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS locations (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    control_faction TEXT DEFAULT 'Player',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_MEMORIES_TABLE = """
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT NOT NULL,
    turn_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    importance REAL DEFAULT 0.5,
    event_type TEXT DEFAULT 'event',
    characters_json TEXT DEFAULT '[]',
    location TEXT DEFAULT '',
    embedding_json TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CAMPAIGN_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_items (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    nome TEXT NOT NULL,
    categoria TEXT DEFAULT 'outro',
    descricao TEXT DEFAULT '',
    atributos_json TEXT DEFAULT '{}',
    adquirido_no_turno INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CAMPAIGN_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_tasks (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT DEFAULT '',
    status TEXT DEFAULT 'em_andamento',
    progresso INTEGER,
    duracao_estimada TEXT,
    objetivo_esperado TEXT,
    is_incidente INTEGER DEFAULT 0,
    dia_inicio INTEGER DEFAULT 1,
    dias_estimados INTEGER DEFAULT 0,
    criada_no_turno INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_PERIODIC_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS periodic_events (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT DEFAULT '',
    intervalo_dias INTEGER NOT NULL,
    ultimo_disparo_dia INTEGER DEFAULT 0,
    proximo_disparo_dia INTEGER NOT NULL,
    efeito_json TEXT DEFAULT '{}',
    status TEXT DEFAULT 'ativo',
    criado_no_turno INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CAMPAIGN_ALLIES_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_allies (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    nome TEXT NOT NULL,
    rei TEXT NOT NULL,
    raca TEXT DEFAULT 'Humano',
    populacao TEXT DEFAULT '10000',
    poder_militar TEXT DEFAULT '1000',
    relacionamento INTEGER DEFAULT 50,
    status_diplomatico TEXT DEFAULT 'neutro',
    historico_notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CAMPAIGN_MAP_NODES_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_map_nodes (
    id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    label TEXT NOT NULL,
    node_type TEXT DEFAULT 'estrutura',
    emoji TEXT DEFAULT '📍',
    x REAL DEFAULT 0.0,
    y REAL DEFAULT 0.0,
    status TEXT DEFAULT 'ativo',
    size TEXT DEFAULT 'medio',
    metadata_json TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, campaign_id),
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

CREATE_CAMPAIGN_MAP_EDGES_TABLE = """
CREATE TABLE IF NOT EXISTS campaign_map_edges (
    id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    source_node_id TEXT NOT NULL,
    target_node_id TEXT NOT NULL,
    edge_type TEXT DEFAULT 'estrada',
    descricao TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, campaign_id),
    FOREIGN KEY(campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);
"""

def get_connection(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def init_db(db_path: str) -> sqlite3.Connection:
    conn = get_connection(db_path)
    with conn:
        conn.execute(CREATE_CAMPAIGN_ALLIES_TABLE)
        conn.execute(CREATE_CAMPAIGNS_TABLE)
        conn.execute(CREATE_WORLD_STATE_TABLE)
        conn.execute(CREATE_CHARACTERS_TABLE)
        conn.execute(CREATE_QUESTS_TABLE)
        conn.execute(CREATE_ITEMS_TABLE)
        conn.execute(CREATE_LOCATIONS_TABLE)
        conn.execute(CREATE_MEMORIES_TABLE)
        conn.execute(CREATE_CAMPAIGN_ITEMS_TABLE)
        conn.execute(CREATE_CAMPAIGN_TASKS_TABLE)
        conn.execute(CREATE_PERIODIC_EVENTS_TABLE)
        conn.execute(CREATE_CAMPAIGN_MAP_NODES_TABLE)
        conn.execute(CREATE_CAMPAIGN_MAP_EDGES_TABLE)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(world_state);")
        columns = [row[1] for row in cursor.fetchall()]
        if columns and "population" not in columns:
            conn.execute("ALTER TABLE world_state ADD COLUMN population INTEGER DEFAULT 10000;")
        if columns and "current_day" not in columns:
            conn.execute("ALTER TABLE world_state ADD COLUMN current_day INTEGER DEFAULT 1;")

        cursor.execute("PRAGMA table_info(campaign_tasks);")
        task_columns = [row[1] for row in cursor.fetchall()]
        if task_columns and "dia_inicio" not in task_columns:
            conn.execute("ALTER TABLE campaign_tasks ADD COLUMN dia_inicio INTEGER DEFAULT 1;")
        if task_columns and "dias_estimados" not in task_columns:
            conn.execute("ALTER TABLE campaign_tasks ADD COLUMN dias_estimados INTEGER DEFAULT 0;")

        cursor.execute("PRAGMA table_info(campaign_allies);")
        ally_columns = [row[1] for row in cursor.fetchall()]
        if ally_columns and "raca" not in ally_columns:
            conn.execute("ALTER TABLE campaign_allies ADD COLUMN raca TEXT DEFAULT 'Humano';")

        cursor.execute("PRAGMA table_info(campaign_map_nodes);")
        node_columns = [row[1] for row in cursor.fetchall()]
        if node_columns and "size" not in node_columns:
            conn.execute("ALTER TABLE campaign_map_nodes ADD COLUMN size TEXT DEFAULT 'medio';")

        cursor.execute("PRAGMA table_info(campaigns);")
        camp_columns = [row[1] for row in cursor.fetchall()]
        if camp_columns and "updated_at" not in camp_columns:
            conn.execute("ALTER TABLE campaigns ADD COLUMN updated_at TIMESTAMP;")
            conn.execute("UPDATE campaigns SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE updated_at IS NULL;")
    return conn
