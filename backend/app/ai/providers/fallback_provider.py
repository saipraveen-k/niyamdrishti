"""
Fallback AI provider.
Tries the primary provider (Claude); on rate-limit or quota errors falls back to OpenAI.
"""

from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from app.ai.providers.base import AIProvider
from app.core.logging import get_logger

logger = get_logger(__name__)

# Anthropic HTTP status codes that signal quota / rate limit exhaustion
_ANTHROPIC_RATE_LIMIT_STATUSES = {429, 529}


def _is_anthropic_rate_limit(exc: Exception) -> bool:
    """Return True when the exception represents an Anthropic quota/rate-limit error."""
    try:
        import anthropic

        if isinstance(exc, anthropic.RateLimitError):
            return True
        if isinstance(exc, anthropic.APIStatusError):
            return exc.status_code in _ANTHROPIC_RATE_LIMIT_STATUSES
    except ImportError:
        pass
    return False


class FallbackProvider(AIProvider):
    """
    Wraps a primary and a fallback provider.
    If the primary raises a rate-limit / quota error, the call is transparently
    retried on the fallback provider.  All other errors propagate normally.
    """

    def __init__(self, primary: AIProvider, fallback: AIProvider):
        self.primary = primary
        self.fallback = fallback

    async def extract_structured(
        self,
        text: str,
        schema: Type[BaseModel],
        system_prompt: str,
        model: Optional[str] = None,
    ) -> BaseModel:
        try:
            return await self.primary.extract_structured(text, schema, system_prompt, model)
        except Exception as exc:
            if _is_anthropic_rate_limit(exc):
                logger.warning(
                    "ai_primary_rate_limited_falling_back",
                    operation="extract_structured",
                    error=str(exc),
                )
                return await self.fallback.extract_structured(text, schema, system_prompt, model)
            raise

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
    ) -> str:
        try:
            return await self.primary.chat(messages, system_prompt, model, temperature)
        except Exception as exc:
            if _is_anthropic_rate_limit(exc):
                logger.warning(
                    "ai_primary_rate_limited_falling_back",
                    operation="chat",
                    error=str(exc),
                )
                return await self.fallback.chat(messages, system_prompt, model, temperature)
            raise

    async def translate(
        self,
        text: str,
        target_language: str,
        context: Optional[str] = None,
    ) -> str:
        try:
            return await self.primary.translate(text, target_language, context)
        except Exception as exc:
            if _is_anthropic_rate_limit(exc):
                logger.warning(
                    "ai_primary_rate_limited_falling_back",
                    operation="translate",
                    error=str(exc),
                )
                return await self.fallback.translate(text, target_language, context)
            raise
