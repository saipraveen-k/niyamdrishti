"""
AI Provider abstraction.
Swap providers without rewriting business logic.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    async def extract_structured(
        self,
        text: str,
        schema: Type[BaseModel],
        system_prompt: str,
        model: Optional[str] = None,
    ) -> BaseModel:
        """Extract structured data from text using the given Pydantic schema."""
        ...

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
    ) -> str:
        """Generate a chat response."""
        ...

    @abstractmethod
    async def translate(
        self,
        text: str,
        target_language: str,
        context: Optional[str] = None,
    ) -> str:
        """Translate text to target language (en|te|hi)."""
        ...
