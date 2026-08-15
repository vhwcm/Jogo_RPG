import json
from typing import List, Dict, Any
from engine.providers.base import BaseLLMProvider
from engine.utils import generate_fallback_embedding
import config

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str = "", model_name: str = ""):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model_name = model_name or config.OPENAI_MODEL
        self.embedding_model = config.OPENAI_EMBEDDING_MODEL
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except Exception:
                pass

    @property
    def name(self) -> str:
        return "openai"

    def is_available(self) -> bool:
        return bool(self.api_key and self._client is not None)

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        if not self.is_available():
            raise RuntimeError("OpenAI API Key is not configured.")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content or ""

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("OpenAI API Key is not configured.")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        text = response.choices[0].message.content or "{}"
        return json.loads(text)

    def generate_embedding(self, text: str) -> List[float]:
        if not self.is_available():
            return generate_fallback_embedding(text)

        try:
            res = self._client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return res.data[0].embedding
        except Exception as e:
            print(f"Warning: OpenAI embedding generation failed ({e}). Using fallback.")
            return generate_fallback_embedding(text)
