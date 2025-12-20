#!/usr/bin/env python3
"""
FLUX Image Generator via OpenRouter API

Generates images using Black Forest Labs FLUX models with dynamic model selection.
Integrates with blog workflow for automatic hero image generation.

Usage:
    # Simple prompt
    python generate_image.py "cyberpunk cityscape at night" -o output.png

    # Blog hero (analyzes content for style)
    python generate_image.py --hero blog/2025-12-19-post-title

    # Check API and model availability
    python generate_image.py --check

    # Analyze title for topic detection
    python generate_image.py --analyze "Zero Trust Network Security"

Dependencies:
    - requests (pip install requests)
    - python-dotenv (pip install python-dotenv)

API: OpenRouter (https://openrouter.ai/api/v1/chat/completions)
Model: Black Forest Labs FLUX (dynamically selected via fetch_models.py)

Author: Intelligence Adjacent Framework
Version: 1.0.0
"""

import argparse
import base64
import json
import os
import sys
import io
from pathlib import Path
from typing import Optional, Dict, Any

# UTF-8 for Windows - only set if not already wrapped
if sys.platform == 'win32' and not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =============================================================================
# Dependencies
# =============================================================================

try:
    import requests
except ImportError:
    print("[ERROR] requests not installed. Run: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Add parent paths for imports
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR / 'research' / 'openrouter'))

try:
    from fetch_models import get_latest_model, list_models, OPENROUTER_API_KEY
except ImportError:
    # Fallback credential loading
    def load_api_key() -> str:
        if load_dotenv:
            env_path = Path(__file__).parents[2] / '.env'
            load_dotenv(env_path)
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            env_file = Path(__file__).parents[2] / '.env'
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENROUTER_API_KEY='):
                            return line.split('=', 1)[1].strip()
            raise ValueError("OPENROUTER_API_KEY not found")
        return api_key

    OPENROUTER_API_KEY = load_api_key()
    get_latest_model = None
    list_models = None

# Import prompt utilities
try:
    from prompts import build_prompt, analyze_topic, build_hero_prompt
except ImportError:
    # Inline fallback
    def analyze_topic(title: str, content: str = None) -> str:
        return "general"

    def build_prompt(subject: str, **kwargs) -> str:
        return f"{subject}. Professional digital art, detailed, atmospheric lighting."

    def build_hero_prompt(title: str, content: str = None) -> str:
        return build_prompt(title)


# =============================================================================
# ANSI Colors
# =============================================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'


def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")


def log_ok(msg: str):
    print(f"{Colors.GREEN}[OK]{Colors.END} {msg}")


def log_warn(msg: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {msg}")


def log_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")


# =============================================================================
# FLUX Image Generator
# =============================================================================

class FluxImageGenerator:
    """
    Generate images using FLUX models via OpenRouter API.

    Features:
        - Dynamic model selection (always uses latest FLUX)
        - Content-aware prompt generation
        - Style variety based on topic detection
        - Base64 PNG output

    Example:
        generator = FluxImageGenerator()
        success = generator.generate("cyberpunk cityscape", "output.png")
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    FALLBACK_MODEL = "black-forest-labs/flux.2-max"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize generator with API key."""
        self.api_key = api_key or OPENROUTER_API_KEY
        self._model_cache = None

    def get_flux_model(self) -> str:
        """
        Get latest FLUX model from OpenRouter API.

        Uses dynamic model discovery via fetch_models.py.
        Falls back to hardcoded model if discovery unavailable.

        Returns:
            Model ID string (e.g., "black-forest-labs/flux.2-max")
        """
        if self._model_cache:
            return self._model_cache

        # Try dynamic model discovery
        if get_latest_model:
            try:
                # Get latest black-forest-labs model with FLUX/image keywords
                model = get_latest_model(
                    "black-forest-labs",
                    prefer_keywords=["flux", "max"]
                )
                if model:
                    self._model_cache = model
                    return model

                # Fallback: search all models
                if list_models:
                    all_models = list_models()
                    for m in all_models:
                        model_id = m.get('id', '').lower()
                        if 'flux' in model_id and 'black-forest' in model_id:
                            self._model_cache = m['id']
                            return m['id']
            except Exception as e:
                log_warn(f"Model discovery failed: {e}")

        # Last resort fallback
        self._model_cache = self.FALLBACK_MODEL
        return self.FALLBACK_MODEL

    def generate(
        self,
        prompt: str,
        output_path: str,
        timeout: int = 180
    ) -> bool:
        """
        Generate image from prompt and save to file.

        Args:
            prompt: Text prompt for image generation
            output_path: Path to save PNG output
            timeout: Request timeout in seconds

        Returns:
            True if successful, False otherwise
        """
        model = self.get_flux_model()
        log_info(f"Using model: {model}")
        log_info(f"Prompt: {prompt[:100]}...")

        try:
            response = requests.post(
                self.API_URL,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://intelligence-adjacent.com',
                    'X-Title': 'IA Framework'
                },
                json={
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}]
                },
                timeout=timeout
            )

            if response.status_code != 200:
                error_data = response.json()
                log_error(f"API error: {error_data.get('error', {}).get('message', 'Unknown')}")
                return False

            data = response.json()
            return self._save_image(data, output_path, prompt)

        except requests.Timeout:
            log_error(f"Request timed out after {timeout}s")
            return False
        except Exception as e:
            log_error(f"Generation failed: {e}")
            return False

    def _save_image(self, data: Dict[str, Any], output_path: str, prompt: str) -> bool:
        """Extract and save image from API response."""
        try:
            choices = data.get('choices', [])
            if not choices:
                log_error("No choices in response")
                return False

            msg = choices[0].get('message', {})
            images = msg.get('images', [])

            if not images:
                log_error("No images in response")
                log_info(f"Response keys: {list(msg.keys())}")
                return False

            # Extract base64 image
            img_url = images[0].get('image_url', {}).get('url', '')
            if not img_url.startswith('data:image'):
                log_error("Invalid image URL format")
                return False

            # Decode and save
            b64_data = img_url.split(',')[1]
            img_bytes = base64.b64decode(b64_data)

            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(img_bytes)

            log_ok(f"Saved: {output_path} ({len(img_bytes):,} bytes)")

            # Save prompt alongside image
            prompt_file = output.with_suffix('.txt')
            prompt_file.write_text(f"PROMPT:\n{prompt}\n\nMODEL:\n{self.get_flux_model()}")
            log_ok(f"Saved prompt: {prompt_file}")

            return True

        except Exception as e:
            log_error(f"Failed to save image: {e}")
            return False

    def generate_hero(self, slug: str, blog_dir: str = "blog") -> bool:
        """
        Generate hero image for a blog post.

        Analyzes draft content for topic detection and generates
        appropriately styled hero image.

        Args:
            slug: Blog post slug (e.g., "2025-12-19-post-title")
            blog_dir: Base blog directory

        Returns:
            True if successful
        """
        post_dir = Path(blog_dir) / slug
        draft_file = post_dir / "draft.md"
        output_path = post_dir / "hero.png"

        if not draft_file.exists():
            log_error(f"Draft not found: {draft_file}")
            return False

        # Read draft for content analysis
        content = draft_file.read_text(encoding='utf-8')

        # Extract title from frontmatter
        title = slug  # Default to slug
        if content.startswith('---'):
            try:
                end = content.index('---', 3)
                frontmatter = content[3:end]
                for line in frontmatter.split('\n'):
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"\'')
                        break
            except:
                pass

        log_info(f"Generating hero for: {title}")

        # Build prompt with content analysis
        prompt = build_hero_prompt(title, content)
        log_info(f"Detected topic: {analyze_topic(title, content)}")

        return self.generate(prompt, str(output_path))

    def check(self) -> bool:
        """Check API connectivity and model availability."""
        print("Checking FLUX image generation...")

        # Check API key
        if not self.api_key:
            log_error("OPENROUTER_API_KEY not set")
            return False
        log_ok(f"API key loaded: {self.api_key[:20]}...")

        # Check model discovery
        model = self.get_flux_model()
        log_ok(f"FLUX model: {model}")

        # Quick API test (don't actually generate)
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={'Authorization': f'Bearer {self.api_key}'},
                timeout=10
            )
            if response.status_code == 200:
                log_ok("OpenRouter API accessible")
            else:
                log_warn(f"API returned status {response.status_code}")
        except Exception as e:
            log_error(f"API check failed: {e}")
            return False

        return True


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate images using FLUX via OpenRouter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "cyberpunk cityscape at night" -o image.png
  %(prog)s --hero blog/2025-12-19-post-title
  %(prog)s --analyze "Zero Trust Network Security"
  %(prog)s --check
        """
    )

    parser.add_argument('prompt', nargs='?', help='Text prompt for image generation')
    parser.add_argument('-o', '--output', default='output.png', help='Output file path')
    parser.add_argument('--hero', metavar='SLUG', help='Generate hero for blog post slug')
    parser.add_argument('--blog-dir', default='blog', help='Blog directory (default: blog)')
    parser.add_argument('--analyze', metavar='TITLE', help='Analyze title for topic detection')
    parser.add_argument('--check', action='store_true', help='Check API and model availability')
    parser.add_argument('--timeout', type=int, default=180, help='Request timeout in seconds')

    args = parser.parse_args()

    generator = FluxImageGenerator()

    # Check mode
    if args.check:
        success = generator.check()
        sys.exit(0 if success else 1)

    # Analyze mode
    if args.analyze:
        topic = analyze_topic(args.analyze)
        prompt = build_hero_prompt(args.analyze)
        print(f"\nTitle: {args.analyze}")
        print(f"Detected topic: {topic}")
        print(f"\nGenerated prompt:\n{prompt}")
        sys.exit(0)

    # Hero generation mode
    if args.hero:
        success = generator.generate_hero(args.hero, args.blog_dir)
        sys.exit(0 if success else 1)

    # Standard prompt mode
    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    success = generator.generate(args.prompt, args.output, timeout=args.timeout)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
