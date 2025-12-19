"""
OpenRouter API Client Package

Multi-model LLM access through OpenRouter with dynamic model discovery.
No hardcoded model IDs - always fetches latest available models.

Usage:
    from tools.openrouter import OpenRouterClient, get_latest_model, list_models

    # Get latest Grok model
    grok_model = get_latest_model("x-ai")

    # Query with dynamic model
    client = OpenRouterClient()
    result = client.query_model(
        model=grok_model,
        prompt="Your query here",
        temperature=0.3
    )

    # List all available models from a provider
    models = list_models(provider="x-ai")
"""

from .fetch_models import (
    list_models,
    get_latest_model,
    get_model_info,
    fetch_models_from_api
)

from .client import OpenRouterClient

__all__ = [
    'OpenRouterClient',
    'list_models',
    'get_latest_model',
    'get_model_info',
    'fetch_models_from_api'
]

__version__ = '2.0.0'
