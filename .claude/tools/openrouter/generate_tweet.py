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

    system_prompt = """You are a social media strategist for a technical blog about AI frameworks, cybersecurity, and career development. The brand voice is:

VOICE PRINCIPLES:
- Professional but accessible (smart colleagues over coffee)
- Humble - show expertise through analysis, not claims
- Action-oriented - challenge readers to take action
- Direct and specific - real measurements, not marketing

TWEET STRUCTURE (HOOK → VALUE → CTA):
1. HOOK (first line): Pattern interrupt. Contrarian take, surprising data, bold claim, or provocative question. This is everything - users decide in 1.7 seconds.
2. TENSION (1-2 lines): The problem or pain point. What's broken? What do people get wrong?
3. INSIGHT (1-2 lines): What you discovered/built. The non-obvious finding.
4. PROOF (optional): Specific numbers, before/after, concrete outcomes.
5. CTA: Link + engagement invitation.

EFFECTIVE HOOK FORMULAS:
- Contrarian: "Most people think [X]. They're wrong."
- Data drop: "[Surprising statistic]. Here's what that means."
- Story: "I spent [time] doing [thing]. Here's what I learned."
- Question: "[Provocative question]?"
- Hot take: "Unpopular opinion: [bold statement]"

RULES:
- NO emojis (brand standard)
- NO AI clichés ("Here's the thing...", "But here's what nobody talks about...")
- NO corporate buzzwords ("leverage", "synergy", "paradigm shift")
- NO humble-bragging ("Having mastered X over 20 years...")
- BE specific - real numbers > vague claims
- SHORT sentences. Whitespace matters.
- Under 280 chars for main hook line ideally
- INCLUDE 2-4 relevant hashtags at the end (e.g., #AI #Cybersecurity #DevOps #LLM #MCP)"""

    user_prompt = f"""Generate a compelling tweet for this blog post:

TITLE: {title}

EXCERPT: {excerpt}

CONTENT PREVIEW:
{content_preview}

URL: {url}

CONTENT TYPE: {content_type}

Generate:
1. MAIN TWEET: Full tweet with HOOK → VALUE → CTA structure. Include the URL at the end.

2. THREAD HOOKS: 3-5 potential thread expansion topics (one line each). These are ideas for turning the tweet into a thread if it performs well.

3. ALT HOOKS: 2-3 alternative opening hooks using different formulas (contrarian, data, question, etc.)

Format your response as:

=== MAIN TWEET ===
[Full tweet here]

=== THREAD HOOKS ===
1. [Topic 1]
2. [Topic 2]
...

=== ALT HOOKS ===
1. [Alternative hook 1]
2. [Alternative hook 2]
..."""

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

        # Parse the structured response
        parsed = parse_tweet_response(content)

        return {
            "tweet": parsed.get("main_tweet", ""),
            "thread_hooks": parsed.get("thread_hooks", []),
            "alt_hooks": parsed.get("alt_hooks", []),
            "raw_response": content,
            "model": MODEL,
            "tokens": usage.get("total_tokens", 0)
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timeout (60s exceeded)"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}


def parse_tweet_response(content: str) -> Dict:
    """Parse the structured tweet response from Grok."""
    result = {
        "main_tweet": "",
        "thread_hooks": [],
        "alt_hooks": []
    }

    sections = content.split("===")

    current_section = None
    for section in sections:
        section = section.strip()

        if "MAIN TWEET" in section:
            current_section = "main"
        elif "THREAD HOOKS" in section or "THREAD" in section:
            current_section = "thread"
        elif "ALT HOOKS" in section or "ALTERNATIVE" in section:
            current_section = "alt"
        elif current_section == "main":
            result["main_tweet"] = section.strip()
        elif current_section == "thread":
            lines = [l.strip() for l in section.split("\n") if l.strip()]
            for line in lines:
                # Remove numbering
                clean = line.lstrip("0123456789.-) ").strip()
                if clean and len(clean) > 10:
                    result["thread_hooks"].append(clean)
        elif current_section == "alt":
            lines = [l.strip() for l in section.split("\n") if l.strip()]
            for line in lines:
                clean = line.lstrip("0123456789.-) ").strip()
                if clean and len(clean) > 10:
                    result["alt_hooks"].append(clean)

    return result


def format_tweet_file(result: Dict, url: str) -> str:
    """Format the result into tweet.md content with copyable code block."""
    output = []

    # Header
    output.append("# Tweet")
    output.append("")
    output.append("Copy the content below:")
    output.append("")

    # Main tweet in code block for easy copying
    output.append("```")
    output.append(result.get("tweet", ""))
    output.append("```")
    output.append("")

    # Thread potential
    output.append("## Thread Potential")
    output.append("")
    for i, hook in enumerate(result.get("thread_hooks", [])[:5], 1):
        output.append(f"{i}. {hook}")
    output.append("")

    # Alternative hooks
    output.append("## Alternative Hooks")
    output.append("")
    for i, hook in enumerate(result.get("alt_hooks", [])[:3], 1):
        output.append(f"{i}. {hook}")
    output.append("")

    # Metadata
    output.append("---")
    output.append("")
    output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append(f"**Model:** {result.get('model', 'unknown')}")
    output.append(f"**Tokens:** {result.get('tokens', 0)}")

    return "\n".join(output)


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
