from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider (e.g. 'gemini', 'grok', 'openai', 'ollama')."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if the provider is configured and credentials/servers are valid."""
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.5
    ) -> str:
        """Generate narrative or general text response."""
        pass

    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.4
    ) -> Dict[str, Any]:
        """Generate structured JSON response."""
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate float vector embedding for RAG memory search."""
        pass
