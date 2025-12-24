#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Powered Tweet Generator for Blog Posts

Uses Grok via OpenRouter to generate engagement-focused tweets
following the HOOK → VALUE → CTA formula.

Based on viral tweet research:
- Pattern interrupt hooks (1.7 second decision)
- Tension/problem statement
- Insight/solution reveal
- Proof/numbers for credibility
- Clear CTA with link

References:
- https://impressifyx.com/post/oTbWwAleTO_N
- https://buildsolo.io/twitter-thread-template/
"""

import sys
import io
import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load .env from framework root
def load_env():
    env_path = Path(__file__).parents[2] / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"\''))

load_env()

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment. Check ~/.claude/.env")

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Use Grok for creative content
MODEL = "x-ai/grok-4-fast"


def generate_tweet(
    title: str,
    excerpt: str,
    content: str,
    url: str,
    content_type: str = "technical"
) -> Dict:
    """
    Generate an engagement-focused tweet for a blog post.

    Args:
        title: Blog post title
        excerpt: Post excerpt/summary
        content: Full post content (for context)
        url: Published URL
        content_type: "technical", "career", "personal", "framework"

    Returns:
        Dict with:
        - tweet: Main tweet text
        - thread_hooks: 3-5 thread expansion ideas
        - alt_hooks: 2-3 alternative opening hooks
    """

    # Truncate content for context (keep under token limits)
    content_preview = content[:4000] if len(content) > 4000 else content

    system_prompt = """You write viral tweets for a technical blog about AI, cybersecurity, and career development.

EXAMPLE FORMAT:
```
Most security advice is backwards.

You're told to patch everything, monitor everything, document everything. But with limited resources? That's a recipe for burnout and gaps.

This 12-week GRC roadmap prioritizes what actually matters—using free NIST/ISO frameworks to build enterprise-grade security on a startup budget.

https://example.com/post-slug/
#Cybersecurity #GRC #SmallBusiness #Security
```

HOOK FORMULAS (pick one):
1. Contrarian: "Most advice about X is wrong/backwards."
2. Statistic: "73% of developers miss this..."
3. Problem+Promise: "Struggling with X? Here's what works."
4. Story hook: "I tried X for 6 months. Here's what happened."
5. Pattern Interrupt: Start with unexpected statement

RULES:
- NO emojis ever
- NO "Here's the thing" or AI clichés
- Be specific - numbers beat vague claims
- Short punchy sentences, not walls of text
- URL on its own line
- 3-4 relevant hashtags on the NEXT line below URL"""

    user_prompt = f"""Write ONE tweet promoting this blog post:

TITLE: {title}
EXCERPT: {excerpt}
URL: {url}

Follow the EXAMPLE FORMAT exactly:
1. Hook line (contrarian, statistic, or pattern interrupt)
2. Blank line
3. Value paragraph (2-3 punchy sentences)
4. Blank line
5. CTA sentence introducing the link
6. Blank line
7. URL on its own line
8. 3-4 hashtags on the next line

Output ONLY the tweet text. No explanations, no markdown code blocks."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,  # Higher for creative content
        "max_tokens": 2000
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()

        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = result.get("usage", {})

        # Clean up the response - just the tweet text
        tweet = content.strip()

        return {
            "tweet": tweet,
            "model": MODEL,
            "tokens": usage.get("total_tokens", 0)
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timeout (60s exceeded)"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def format_tweet_file(result: Dict, url: str) -> str:
    """Format the result into tweet.md - just the tweet text, nothing else."""
    tweet = result.get("tweet", "").strip()

    # Clean up any residual formatting from the model
    # Remove markdown artifacts, quotes, or explanatory text
    tweet = tweet.strip('`"\'')

    # If model included explanatory text, try to extract just the tweet
    if "===" in tweet or "Tweet:" in tweet:
        lines = tweet.split('\n')
        tweet = '\n'.join(l for l in lines if l.strip() and not l.startswith('===') and not l.startswith('Tweet:'))

    return tweet.strip()


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_tweet.py <draft.md> [url]")
        print("\nReads draft.md, extracts title/excerpt, generates tweet.")
        print("If url not provided, uses placeholder.")
        sys.exit(1)

    draft_path = Path(sys.argv[1])
    url = sys.argv[2] if len(sys.argv) > 2 else "https://notchrisgroves.com/post-slug/"

    if not draft_path.exists():
        print(f"[!] File not found: {draft_path}")
        sys.exit(1)

    # Read and parse draft
    content = draft_path.read_text(encoding='utf-8')

    # Extract frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            body = parts[2]

            # Simple YAML parsing
            title = ""
            excerpt = ""
            for line in frontmatter_text.split("\n"):
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("excerpt:"):
                    excerpt = line.split(":", 1)[1].strip().strip('"\'')
        else:
            title = "Untitled"
            excerpt = ""
            body = content
    else:
        title = "Untitled"
        excerpt = ""
        body = content

    print(f"Generating tweet for: {title}")
    print(f"URL: {url}")
    print()

    result = generate_tweet(
        title=title,
        excerpt=excerpt,
        content=body,
        url=url,
        content_type="technical"
    )

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)

    # Save to tweet.md in same directory as draft
    tweet_path = draft_path.parent / "tweet.md"
    tweet_content = format_tweet_file(result, url)
    tweet_path.write_text(tweet_content, encoding='utf-8')

    print("=== GENERATED TWEET ===")
    print(result["tweet"])
    print()
    print(f"Saved to: {tweet_path}")
    print(f"Tokens used: {result.get('tokens', 0)}")
