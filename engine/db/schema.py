import sqlite3
import os
from pathlib import Path

CREATE_CAMPAIGNS_TABLE = """
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        conn.execute(CREATE_CAMPAIGNS_TABLE)
        conn.execute(CREATE_WORLD_STATE_TABLE)
        conn.execute(CREATE_CHARACTERS_TABLE)
        conn.execute(CREATE_QUESTS_TABLE)
        conn.execute(CREATE_ITEMS_TABLE)
        conn.execute(CREATE_LOCATIONS_TABLE)
        conn.execute(CREATE_MEMORIES_TABLE)

        # Migration check for population column in existing databases
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(world_state);")
        columns = [row[1] for row in cursor.fetchall()]
        if columns and "population" not in columns:
            conn.execute("ALTER TABLE world_state ADD COLUMN population INTEGER DEFAULT 10000;")
    return conn
