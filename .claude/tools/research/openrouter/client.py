#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenRouter API Client for Multi-Model LLM Access

Unified interface to query AI models through OpenRouter with dynamic model selection.
Uses fetch_models.py for discovering latest models instead of hardcoded IDs.

Usage:
    from tools.openrouter import OpenRouterClient, get_latest_model

    # Get latest Grok model dynamically
    grok_model = get_latest_model("x-ai")

    # Query with dynamic model
    client = OpenRouterClient()
    result = client.query_model(
        model=grok_model,
        prompt="Verify case law citation for Smith v. Jones",
        temperature=0.2
    )

API: https://openrouter.ai/api/v1/chat/completions
Author: Intelligence Adjacent
Version: 2.0.0
Last Updated: 2025-12-11
"""

import sys
import io
import os
import json
import time
from pathlib import Path
from typing import Dict, Optional, Any

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
# OpenRouter Client Class
# =============================================================================

class OpenRouterClient:
    """Client for OpenRouter API with retry logic and error handling"""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 120):
        """
        Initialize OpenRouter client

        Args:
            api_key: OpenRouter API key (defaults to .env)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or OPENROUTER_API_KEY
        self.timeout = timeout
        self.session_requests = 0
        self.session_cost = 0.0

    def query_model(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: int = 2
    ) -> Dict[str, Any]:
        """
        Query a model through OpenRouter

        Args:
            model: Model ID (e.g., 'x-ai/grok-4-fast', 'anthropic/claude-3.5-sonnet')
            prompt: User prompt/query
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum response tokens
            system_prompt: Optional system prompt
            retry_count: Number of retries on failure
            retry_delay: Delay between retries (seconds)

        Returns:
            dict: {
                'content': str,         # Response content
                'model': str,           # Model used
                'tokens': int,          # Tokens used
                'cost': float,          # Estimated cost
                'duration': float,      # Response time (seconds)
                'success': bool         # Request succeeded
            }

        Example:
            >>> client = OpenRouterClient()
            >>> result = client.query_model(
            ...     model="x-ai/grok-4-fast",
            ...     prompt="Explain quantum computing",
            ...     temperature=0.3
            ... )
            >>> print(result['content'])
        """
        # Build request payload
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://intelligence-adjacent.com",
            "X-Title": "IA Framework"
        }

        # Retry loop
        for attempt in range(retry_count):
            try:
                start_time = time.time()

                if HTTP_CLIENT == 'requests':
                    response = requests.post(
                        self.BASE_URL,
                        headers=headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    data = response.json()
                else:
                    req = urllib.request.Request(
                        self.BASE_URL,
                        data=json.dumps(payload).encode('utf-8'),
                        headers=headers,
                        method='POST'
                    )
                    with urllib.request.urlopen(req, timeout=self.timeout) as response:
                        data = json.loads(response.read().decode('utf-8'))

                duration = time.time() - start_time

                # Parse response
                content = data['choices'][0]['message']['content']
                usage = data.get('usage', {})
                tokens = usage.get('total_tokens', 0)

                # Estimate cost
                cost = self._estimate_cost(model, tokens)

                # Update session metrics
                self.session_requests += 1
                self.session_cost += cost

                return {
                    'content': content,
                    'model': model,
                    'tokens': tokens,
                    'cost': cost,
                    'duration': duration,
                    'success': True,
                    'usage': usage
                }

            except Exception as e:
                error_details = str(e)
                if HTTP_CLIENT == 'requests' and hasattr(e, 'response') and e.response is not None:
                    try:
                        error_body = e.response.json()
                        error_details = f"{e} | Response: {json.dumps(error_body, indent=2)}"
                    except:
                        try:
                            error_details = f"{e} | Response text: {e.response.text[:200]}"
                        except:
                            pass

                if attempt < retry_count - 1:
                    if __name__ == "__main__":
                        print(f"[!] Attempt {attempt + 1}/{retry_count} failed: {error_details}")
                        print(f"[*] Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    return {
                        'content': '',
                        'model': model,
                        'tokens': 0,
                        'cost': 0.0,
                        'duration': 0.0,
                        'success': False,
                        'error': error_details
                    }

    def _estimate_cost(self, model: str, tokens: int) -> float:
        """
        Estimate API cost based on model and tokens

        Rough estimates (per 1M tokens):
        - Grok: $5 / 1M tokens
        - Claude Sonnet: $3 / 1M tokens
        - GPT-4: $10 / 1M tokens
        """
        cost_per_million = {
            'grok': 5.0,
            'claude': 3.0,
            'gpt-4': 10.0,
            'gpt-3': 0.5
        }

        for key, price in cost_per_million.items():
            if key in model.lower():
                return (tokens / 1_000_000) * price

        # Default fallback
        return (tokens / 1_000_000) * 4.0

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        return {
            'requests': self.session_requests,
            'cost': round(self.session_cost, 4)
        }


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """Test CLI for OpenRouter client"""
    import argparse
    from .fetch_models import get_latest_model

    parser = argparse.ArgumentParser(description='OpenRouter API Client')
    parser.add_argument('--provider', required=True, help='Provider (e.g., x-ai, anthropic)')
    parser.add_argument('--prompt', required=True, help='Prompt to send')
    parser.add_argument('--temperature', type=float, default=0.3, help='Sampling temperature')
    parser.add_argument('--max-tokens', type=int, default=2000, help='Max response tokens')
    parser.add_argument('--keywords', nargs='+', help='Prefer models with keywords')

    args = parser.parse_args()

    # Get latest model dynamically
    print(f"[*] Finding latest {args.provider} model...")
    model_id = get_latest_model(args.provider, prefer_keywords=args.keywords)

    if not model_id:
        print(f"[!] No models found for provider: {args.provider}")
        sys.exit(1)

    print(f"[*] Using model: {model_id}")
    print(f"[*] Prompt: {args.prompt[:100]}...")

    # Query model
    client = OpenRouterClient()
    result = client.query_model(
        model=model_id,
        prompt=args.prompt,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )

    if result['success']:
        print(f"\n[+] Response received")
        print(f"[+] Model: {result['model']}")
        print(f"[+] Tokens: {result['tokens']}")
        print(f"[+] Cost: ${result['cost']:.4f}")
        print(f"[+] Duration: {result['duration']:.2f}s")
        print(f"\n{'-'*60}")
        print(result['content'])
        print(f"{'-'*60}\n")
    else:
        print(f"[!] Query failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


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
