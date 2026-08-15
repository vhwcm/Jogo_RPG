import json
from typing import List, Dict, Any
from engine.providers.base import BaseLLMProvider
from engine.utils import generate_fallback_embedding
import config

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str = "", model_name: str = ""):
        self.base_url = base_url or config.OLLAMA_BASE_URL
        self.model_name = model_name or config.OLLAMA_MODEL

    @property
    def name(self) -> str:
        return "ollama"

    def is_available(self) -> bool:
        if not HAS_HTTPX:
            return False
        try:
            with httpx.Client(timeout=2.0) as client:
                r = client.get(f"{self.base_url}/api/version")
                return r.status_code == 200
        except Exception:
            return False

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        if not HAS_HTTPX:
            raise RuntimeError("httpx package is required for Ollama provider.")
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_instruction,
            "options": {"temperature": temperature},
            "stream": False
        }
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(f"{self.base_url}/api/generate", json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "")

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        if not HAS_HTTPX:
            raise RuntimeError("httpx package is required for Ollama provider.")
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_instruction,
            "format": "json",
            "options": {"temperature": temperature},
            "stream": False
        }
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(f"{self.base_url}/api/generate", json=payload)
            resp.raise_for_status()
            text = resp.json().get("response", "{}")
            return json.loads(text)

    def generate_embedding(self, text: str) -> List[float]:
        if HAS_HTTPX:
            try:
                payload = {"model": self.model_name, "prompt": text}
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(f"{self.base_url}/api/embeddings", json=payload)
                    if resp.status_code == 200:
                        return resp.json().get("embedding", [])
            except Exception:
                pass

        return generate_fallback_embedding(text)
