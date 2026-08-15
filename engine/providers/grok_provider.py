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

class GrokProvider(BaseLLMProvider):
    def __init__(self, api_key: str = "", base_url: str = "", model_name: str = ""):
        self.api_key = api_key or config.GROK_API_KEY
        self.base_url = base_url or config.GROK_BASE_URL
        self.model_name = model_name or config.GROK_MODEL

    @property
    def name(self) -> str:
        return "grok"

    def is_available(self) -> bool:
        return bool(self.api_key and HAS_HTTPX)

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        if not self.is_available():
            raise RuntimeError("Grok API key is not configured or httpx package is missing.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Grok API key is not configured or httpx package is missing.")

        json_sys_instruction = (system_instruction + "\nIMPORTANT: You MUST respond ONLY with valid JSON.").strip()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = [
            {"role": "system", "content": json_sys_instruction},
            {"role": "user", "content": prompt}
        ]

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return json.loads(text)

    def generate_embedding(self, text: str) -> List[float]:
        return generate_fallback_embedding(text)
