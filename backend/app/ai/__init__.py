"""
AI subsystem entry point.
Use get_ai_provider() to obtain the configured provider everywhere in the app.
"""

from app.ai.providers.base import AIProvider
from app.core.config import settings


def get_ai_provider() -> AIProvider:
    """
    Factory that returns the AI provider configured via AI_PROVIDER env var:

      openai                      – OpenAI only (default)
      anthropic                   – Anthropic (Claude) only
      anthropic_with_openai_fallback – Claude primary, falls back to OpenAI
                                       on rate-limit / quota errors
    """
    provider = settings.ai_provider

    if provider == "anthropic":
        from app.ai.providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider()

    if provider == "anthropic_with_openai_fallback":
        from app.ai.providers.anthropic_provider import AnthropicProvider
        from app.ai.providers.openai_provider import OpenAIProvider
        from app.ai.providers.fallback_provider import FallbackProvider
        return FallbackProvider(
            primary=AnthropicProvider(),
            fallback=OpenAIProvider(),
        )

    # default: openai
    from app.ai.providers.openai_provider import OpenAIProvider
    return OpenAIProvider()
