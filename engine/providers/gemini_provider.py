import json
from typing import List, Dict, Any, Optional
from engine.providers.base import BaseLLMProvider
from engine.utils import generate_fallback_embedding
import config

GENERIC_FLASH_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
]

EMBEDDING_CANDIDATES = [
    "text-embedding-004",
    "embedding-001",
    "models/text-embedding-004",
    "models/embedding-001",
]

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str = "", model_name: str = ""):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model_name or config.GEMINI_MODEL
        self.embedding_model = config.GEMINI_EMBEDDING_MODEL
        self._genai_genai = None
        self._legacy_genai = None
        self._tested_and_working = False

        if self.api_key:
            # 1. Initialize Client SDK
            try:
                from google import genai
                self._genai_genai = genai.Client(api_key=self.api_key)
            except Exception:
                try:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=self.api_key)
                    self._legacy_genai = legacy_genai
                except Exception:
                    pass

    def _ensure_initialized(self):
        if not self._tested_and_working and self.is_available():
            self.discover_and_test_models()

    @property
    def name(self) -> str:
        return "gemini"

    def is_available(self) -> bool:
        return bool(self.api_key and (self._genai_genai is not None or self._legacy_genai is not None))

    def discover_and_test_models(self):
        """
        Lists all available models from Gemini API, selects the newest generation and embedding models,
        and executes probe requests to verify live connectivity.
        """
        discovered_gen_models = []
        discovered_emb_models = []

        # List models via available SDK
        try:
            if self._genai_genai:
                all_models = list(self._genai_genai.models.list())
                for m in all_models:
                    m_name = getattr(m, "name", str(m))
                    clean_name = m_name.replace("models/", "")
                    if "gemini" in clean_name.lower():
                        discovered_gen_models.append(clean_name)
                    elif "embed" in clean_name.lower():
                        discovered_emb_models.append(clean_name)

            elif self._legacy_genai:
                all_models = list(self._legacy_genai.list_models())
                for m in all_models:
                    m_name = getattr(m, "name", str(m))
                    methods = getattr(m, "supported_generation_methods", [])
                    if "generateContent" in methods:
                        discovered_gen_models.append(m_name)
                    if "embedContent" in methods:
                        discovered_emb_models.append(m_name)
        except Exception as e:
            print(f"[Gemini Discovery] Warning: ListModels query failed ({e}). Using candidate list.")

        # Build candidate test order
        gen_candidates = []
        if self.model_name:
            gen_candidates.append(self.model_name)
        gen_candidates.extend([m for m in discovered_gen_models if m not in gen_candidates])
        gen_candidates.extend([m for m in GENERIC_FLASH_CANDIDATES if m not in gen_candidates])

        emb_candidates = []
        if self.embedding_model:
            emb_candidates.append(self.embedding_model)
        emb_candidates.extend([m for m in discovered_emb_models if m not in emb_candidates])
        emb_candidates.extend([m for m in EMBEDDING_CANDIDATES if m not in emb_candidates])

        # Probe Generation Model
        active_gen_model = None
        for candidate in gen_candidates:
            try:
                res = self._probe_generate_text(candidate, "Diga 'OK'")
                if res:
                    active_gen_model = candidate
                    print(f"✅ [Gemini] Modelo de geração validado com sucesso: '{active_gen_model}'")
                    break
            except Exception as e:
                pass

        if active_gen_model:
            self.model_name = active_gen_model
            self._tested_and_working = True
        else:
            print("⚠️ [Gemini] Nenhum modelo de geração respondeu ao teste de probe.")

        # Probe Embedding Model
        active_emb_model = None
        for candidate in emb_candidates:
            try:
                emb = self._probe_generate_embedding(candidate, "Teste de vetor")
                if emb and len(emb) > 0:
                    active_emb_model = candidate
                    print(f"✅ [Gemini] Modelo de embeddings validado com sucesso: '{active_emb_model}'")
                    break
            except Exception:
                pass

        if active_emb_model:
            self.embedding_model = active_emb_model

    def _probe_generate_text(self, model_name: str, prompt: str) -> str:
        if self._genai_genai:
            response = self._genai_genai.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text or ""
        elif self._legacy_genai:
            model = self._legacy_genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            return response.text or ""
        return ""

    def _probe_generate_embedding(self, model_name: str, text: str) -> List[float]:
        if self._genai_genai:
            response = self._genai_genai.models.embed_content(
                model=model_name,
                contents=text
            )
            if hasattr(response, "embedding") and hasattr(response.embedding, "values"):
                return list(response.embedding.values)
            elif hasattr(response, "embeddings") and response.embeddings:
                return list(response.embeddings[0].values)
        elif self._legacy_genai:
            res = self._legacy_genai.embed_content(
                model=model_name if model_name.startswith("models/") else f"models/{model_name}",
                content=text
            )
            if "embedding" in res:
                return res["embedding"]
        return []

    def generate_text(self, prompt: str, system_instruction: str = "", temperature: float = 0.5) -> str:
        if not self.is_available():
            raise RuntimeError("Gemini API Key is not configured or client initialization failed.")

        self._ensure_initialized()
        try:
            if self._genai_genai:
                from google.genai import types
                config_obj = types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system_instruction if system_instruction else None
                )
                response = self._genai_genai.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config_obj
                )
                return response.text or ""

            elif self._legacy_genai:
                model = self._legacy_genai.GenerativeModel(
                    model_name=self.model_name if self.model_name.startswith("models/") else f"models/{self.model_name}",
                    system_instruction=system_instruction if system_instruction else None,
                    generation_config={"temperature": temperature}
                )
                response = model.generate_content(prompt)
                return response.text or ""
        except Exception as e:
            # Fallback to retry with other candidate models
            print(f"Warning: Gemini generate_text failed with model '{self.model_name}' ({e}). Re-probing...")
            for candidate in GENERIC_FLASH_CANDIDATES:
                if candidate != self.model_name:
                    try:
                        res = self._probe_generate_text(candidate, prompt)
                        if res:
                            self.model_name = candidate
                            return res
                    except Exception:
                        pass
            raise e

    def generate_json(self, prompt: str, system_instruction: str = "", temperature: float = 0.4) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Gemini API Key is not configured.")

        self._ensure_initialized()
        try:
            if self._genai_genai:
                from google.genai import types
                config_obj = types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json",
                    system_instruction=system_instruction if system_instruction else None
                )
                response = self._genai_genai.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config_obj
                )
                text = response.text or "{}"
                return json.loads(text)

            elif self._legacy_genai:
                model = self._legacy_genai.GenerativeModel(
                    model_name=self.model_name if self.model_name.startswith("models/") else f"models/{self.model_name}",
                    system_instruction=system_instruction if system_instruction else None,
                    generation_config={
                        "temperature": temperature,
                        "response_mime_type": "application/json"
                    }
                )
                response = model.generate_content(prompt)
                text = response.text or "{}"
                return json.loads(text)
        except Exception as e:
            print(f"Warning: Gemini generate_json failed with model '{self.model_name}' ({e}). Re-probing...")
            for candidate in GENERIC_FLASH_CANDIDATES:
                if candidate != self.model_name:
                    try:
                        sys_prompt = (system_instruction + "\nRespond in JSON.").strip()
                        raw = self._probe_generate_text(candidate, prompt + "\nRespond in JSON format.")
                        if raw:
                            # Try parsing JSON or clean formatting
                            clean_json = raw.strip()
                            if clean_json.startswith("```"):
                                clean_json = clean_json.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                            parsed = json.loads(clean_json)
                            self.model_name = candidate
                            return parsed
                    except Exception:
                        pass
            raise e

    def generate_embedding(self, text: str) -> List[float]:
        if not self.is_available():
            return generate_fallback_embedding(text)

        try:
            emb = self._probe_generate_embedding(self.embedding_model, text)
            if emb:
                return emb
        except Exception as e:
            for cand in EMBEDDING_CANDIDATES:
                try:
                    emb = self._probe_generate_embedding(cand, text)
                    if emb:
                        self.embedding_model = cand
                        return emb
                except Exception:
                    pass

        return generate_fallback_embedding(text)
