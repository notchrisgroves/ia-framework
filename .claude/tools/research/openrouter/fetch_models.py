#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenRouter Dynamic Model Discovery

Fetches available models from OpenRouter API dynamically (no hardcoded model IDs).
Provides caching, filtering, and model selection helpers.

Usage:
    from tools.openrouter import get_latest_model, list_models

    # Get latest Grok model
    grok_model = get_latest_model("x-ai")

    # Get latest Grok with "code" preference
    grok_code = get_latest_model("x-ai", prefer_keywords=["code"])

    # List all x-ai models
    models = list_models(provider="x-ai")

API: https://openrouter.ai/api/v1/models
Author: Intelligence Adjacent
Version: 1.0.0
Last Updated: 2025-12-11
"""

import sys
import io
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# =============================================================================
# UTF-8 Encoding for Windows
# =============================================================================
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =============================================================================
# HTTP Client
# =============================================================================
try:
    import requests
    HTTP_CLIENT = 'requests'
except ImportError:
    try:
        import urllib.request
        import urllib.error
        HTTP_CLIENT = 'urllib'
    except ImportError:
        raise ImportError("No HTTP client available. Install: pip install requests")

# =============================================================================
# Credential Loading
# =============================================================================
def load_api_key() -> str:
    """Load OpenRouter API key from .env file"""
    # Try dotenv first
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parents[2] / '.env'
        load_dotenv(env_path)
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass

    # Fallback to manual parsing
    env_file = Path(__file__).parents[2] / '.env'
    if not env_file.exists():
        raise FileNotFoundError(f".env file not found at {env_file}")

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('OPENROUTER_API_KEY='):
                return line.split('=', 1)[1].strip()

    raise ValueError("OPENROUTER_API_KEY not found in .env file")

OPENROUTER_API_KEY = load_api_key()

# =============================================================================
# Configuration
# =============================================================================
MODELS_API_URL = "https://openrouter.ai/api/v1/models"
CACHE_DIR = Path(__file__).parents[2] / '.cache' / 'openrouter'
CACHE_FILE = CACHE_DIR / 'models.json'
CACHE_TTL_HOURS = 24  # Refresh every 24 hours

# =============================================================================
# Core Functions
# =============================================================================

def fetch_models_from_api(api_key: Optional[str] = None, timeout: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch all available models from OpenRouter API

    Args:
        api_key: OpenRouter API key (defaults to .env)
        timeout: Request timeout in seconds

    Returns:
        List of model dictionaries
    """
    api_key = api_key or OPENROUTER_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        if HTTP_CLIENT == 'requests':
            response = requests.get(MODELS_API_URL, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
        else:
            req = urllib.request.Request(MODELS_API_URL, headers=headers, method='GET')
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode('utf-8'))

        models = data.get('data', [])
        if not models:
            raise ValueError("No models returned from OpenRouter API")

        return models

    except Exception as e:
        raise RuntimeError(f"Failed to fetch models from API: {e}")


def get_cached_models() -> Optional[List[Dict[str, Any]]]:
    """Get models from cache if available and not expired"""
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        cached_at = datetime.fromisoformat(cache_data.get('timestamp', ''))
        cache_age = datetime.now() - cached_at

        if cache_age > timedelta(hours=CACHE_TTL_HOURS):
            return None

        return cache_data.get('models', [])

    except Exception:
        return None


def save_models_to_cache(models: List[Dict[str, Any]]) -> None:
    """Save models to cache file"""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'models': models,
            'count': len(models)
        }
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        # Cache write failure shouldn't break functionality
        if __name__ == "__main__":
            print(f"[WARNING] Failed to save cache: {e}")


def list_models(
    provider: Optional[str] = None,
    use_cache: bool = True,
    force_refresh: bool = False
) -> List[Dict[str, Any]]:
    """
    List available models with optional filtering

    Args:
        provider: Filter by provider (e.g., "x-ai", "anthropic", "openai")
        use_cache: Use cached models if available
        force_refresh: Force refresh from API

    Returns:
        List of model dictionaries

    Example:
        >>> models = list_models(provider="x-ai")
        >>> for m in models:
        ...     print(m['id'], m['name'])
    """
    models = None

    # Try cache first unless force refresh
    if use_cache and not force_refresh:
        models = get_cached_models()
        if models and __name__ == "__main__":
            print(f"[*] Using cached models ({len(models)} models)")

    # Fetch from API if no cache or force refresh
    if models is None:
        if __name__ == "__main__":
            print(f"[*] Fetching models from OpenRouter API...")
        models = fetch_models_from_api()
        if models:
            save_models_to_cache(models)

    # Filter by provider if specified
    if provider:
        filtered = [m for m in models if m.get('id', '').startswith(provider + '/')]
        return filtered

    return models


def get_latest_model(
    provider: str,
    prefer_keywords: Optional[List[str]] = None,
    use_cache: bool = True
) -> Optional[str]:
    """
    Get the latest/best model ID for a given provider

    Args:
        provider: Provider prefix (e.g., "x-ai", "anthropic")
        prefer_keywords: Keywords to prioritize (e.g., ["fast", "code"])
        use_cache: Use cached models if available

    Returns:
        Model ID string or None if not found

    Examples:
        >>> get_latest_model("x-ai")
        'x-ai/grok-4.1-fast'
        >>> get_latest_model("x-ai", prefer_keywords=["code"])
        'x-ai/grok-code-fast-1'
        >>> get_latest_model("anthropic")
        'anthropic/claude-3.5-sonnet'
    """
    models = list_models(provider=provider, use_cache=use_cache)

    if not models:
        return None

    # If prefer_keywords specified, try to find matching model
    if prefer_keywords:
        for keyword in prefer_keywords:
            for model in models:
                model_id = model.get('id', '')
                if keyword.lower() in model_id.lower():
                    if __name__ == "__main__":
                        print(f"[+] Found model with keyword '{keyword}': {model_id}")
                    return model_id

    # Otherwise return first model (typically newest/primary)
    model_id = models[0].get('id')
    if __name__ == "__main__":
        print(f"[+] Using latest {provider} model: {model_id}")
    return model_id


def get_model_info(model_id: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific model

    Args:
        model_id: Full model ID (e.g., "x-ai/grok-4-fast")
        use_cache: Use cached models if available

    Returns:
        Model dictionary with details or None if not found
    """
    models = list_models(use_cache=use_cache)

    for model in models:
        if model.get('id') == model_id:
            return model

    return None


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI interface for model discovery"""
    import argparse

    parser = argparse.ArgumentParser(description='OpenRouter Model Discovery')
    parser.add_argument('--provider', '-p', help='Filter by provider (e.g., x-ai, anthropic)')
    parser.add_argument('--latest', '-l', action='store_true', help='Get latest model for provider')
    parser.add_argument('--info', '-i', metavar='MODEL_ID', help='Get info about specific model')
    parser.add_argument('--refresh', '-r', action='store_true', help='Force refresh cache')
    parser.add_argument('--keywords', '-k', nargs='+', help='Preferred keywords for --latest')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Get model info
    if args.info:
        info = get_model_info(args.info, use_cache=not args.refresh)
        if info:
            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print(f"\n[+] Model: {info.get('id')}")
                print(f"    Name: {info.get('name', 'N/A')}")
                print(f"    Context: {info.get('context_length', 'N/A')} tokens")
                if 'pricing' in info:
                    pricing = info['pricing']
                    print(f"    Pricing: ${pricing.get('prompt', 'N/A')} / ${pricing.get('completion', 'N/A')} per token")
        else:
            print(f"[!] Model not found: {args.info}")
        return

    # Get latest model for provider
    if args.latest:
        if not args.provider:
            print("[!] --latest requires --provider")
            sys.exit(1)

        model_id = get_latest_model(
            args.provider,
            prefer_keywords=args.keywords,
            use_cache=not args.refresh
        )

        if model_id:
            if args.json:
                print(json.dumps({"model_id": model_id}))
            else:
                print(f"\n[+] Latest {args.provider} model: {model_id}")
        else:
            print(f"[!] No models found for provider: {args.provider}")
        return

    # List models
    models = list_models(
        provider=args.provider,
        use_cache=not args.refresh
    )

    if args.json:
        print(json.dumps(models, indent=2))
    else:
        print(f"\n[+] Found {len(models)} models")
        if args.provider:
            print(f"    Provider: {args.provider}")
        print()

        for model in models[:20]:
            model_id = model.get('id', 'unknown')
            name = model.get('name', 'N/A')
            context = model.get('context_length', 'N/A')
            print(f"  • {model_id}")
            print(f"    {name} (context: {context} tokens)")

        if len(models) > 20:
            print(f"\n  ... and {len(models) - 20} more models")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
