import os
import sys
import site
from pathlib import Path

# Ensure user site-packages are in sys.path
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

BASE_DIR = Path(__file__).resolve().parent

# Try importing python-dotenv or parse .env manually
env_file = BASE_DIR / ".env"

if not env_file.exists():
    # Create default template .env file if missing
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(
                "# AI RPG Game - Configuração de Chaves de API\n"
                "# Insira a sua chave em um dos provedores abaixo:\n\n"
                "# 1. Google Gemini (Recomendado): https://aistudio.google.com/app/apikey\n"
                "GEMINI_API_KEY=\n\n"
                "# 2. xAI Grok API: https://console.x.ai/\n"
                "GROK_API_KEY=\n\n"
                "# 3. OpenAI API: https://platform.openai.com/api-keys\n"
                "OPENAI_API_KEY=\n\n"
                "# Provedor padrão: gemini, grok, openai ou ollama\n"
                "DEFAULT_LLM_PROVIDER=gemini\n"
            )
    except Exception:
        pass

if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip("'\""))

# Database & Storage Settings
DB_PATH = os.getenv("RPG_DB_PATH", str(BASE_DIR / "data" / "rpg_game.db"))

# LLM Providers Configuration
DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Model Names
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")

GROK_MODEL = os.getenv("GROK_MODEL", "grok-2-latest")
GROK_BASE_URL = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Memory / RAG Settings
TOP_K_MEMORIES = int(os.getenv("TOP_K_MEMORIES", "5"))
IMPORTANCE_THRESHOLD = float(os.getenv("IMPORTANCE_THRESHOLD", "0.2"))
SUMMARY_INTERVAL_TURNS = int(os.getenv("SUMMARY_INTERVAL_TURNS", "10"))

# Server Settings
WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))

def is_any_api_key_configured() -> bool:
    return bool(GEMINI_API_KEY.strip() or GROK_API_KEY.strip() or OPENAI_API_KEY.strip())
