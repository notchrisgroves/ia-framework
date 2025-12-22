#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grok Adversarial QA Review for Blog Posts

IMPORTANT: This script ONLY calls Grok via OpenRouter.
Sonnet structured review should be done by Claude Code natively (no API cost).

Workflow:
1. Claude Code (Sonnet) does structured review → saves to qa-sonnet.json
2. This script calls Grok for adversarial review
3. Results combined into final qa-review.json

Usage:
    python dual_qa_review.py <draft.md> [sonnet_review.json]

If sonnet_review.json provided, combines with Grok review.
Otherwise, returns Grok-only review.
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
    raise ValueError("OPENROUTER_API_KEY not found. Check ~/.claude/.env")

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Only Grok via OpenRouter - Sonnet done natively by Claude Code
GROK_MODEL = "x-ai/grok-4-fast"


def call_openrouter(model: str, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> Dict:
    """Call OpenRouter API with specified model."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = result.get("usage", {})

        return {
            "content": content,
            "tokens": usage.get("total_tokens", 0),
            "model": model
        }
    except Exception as e:
        return {"error": str(e), "model": model}


def get_sonnet_review_prompt() -> str:
    """Return the prompt for Claude Code to do Sonnet structured review natively."""
    return """Perform structured QA review against these criteria:

1. COMPLETENESS - All claims backed by evidence/citations, code examples present, sources section exists
2. TECHNICAL ACCURACY - Claims factually correct, statistics have inline citations, no hallucinated references
3. STRUCTURE & CLARITY - Strong hook in opening, clear H2/H3 hierarchy, practical takeaways
4. STYLE COMPLIANCE - No AI clichés, no corporate buzzwords, professional tone, no hardcoded counts
5. CITATION VALIDATION - Inline links for key statistics, sources section at end

Rate each 1-5, provide OVERALL RATING [1-5], and list specific issues with line references."""


def grok_review(content: str, title: str) -> Dict:
    """Phase 2: Grok adversarial challenge review."""

    system_prompt = """You are an adversarial reviewer challenging a blog post. Your job is to find:

1. OVERSTATEMENTS
- Claims that exceed the evidence
- Statistics without sources
- "All", "every", "always" claims that may be false

2. LOGICAL GAPS
- Missing steps in reasoning
- Unsupported conclusions
- Correlation claimed as causation

3. HALLUCINATION DETECTION
- Fabricated statistics
- Non-existent CVEs or references
- Made-up tool names or features

4. MISSING CONTEXT
- Edge cases not addressed
- Counterarguments ignored
- Important caveats missing

5. EVIDENCE SUFFICIENCY
- Claims need more proof
- Screenshots/examples missing
- Sources too weak for claims made

Be skeptical but fair. Challenge assumptions. Surface potential issues."""

    user_prompt = f"""Challenge this blog post:

TITLE: {title}

CONTENT:
{content[:8000]}

Provide adversarial review:

## OVERSTATEMENTS: X found
- [Claim that exceeds evidence]

## LOGICAL GAPS: X found
- [Missing reasoning steps]

## POTENTIAL HALLUCINATIONS: X found
- [Statistics/references to verify]

## MISSING CONTEXT: X found
- [Important omissions]

## EVIDENCE SUFFICIENCY: X weak claims
- [Claims needing more proof]

## CONFIDENCE RATING: [1-5]
1 = Major concerns, likely inaccurate
2 = Multiple issues to address
3 = Some concerns, mostly sound
4 = Minor challenges only
5 = High confidence, well-supported

## KEY CHALLENGES
[Top 3 things author should address]"""

    print("  Calling Grok for adversarial review...")
    result = call_openrouter(GROK_MODEL, system_prompt, user_prompt)

    if "error" in result:
        print(f"  ❌ Grok error: {result['error']}")
    else:
        print(f"  ✅ Grok review complete ({result['tokens']} tokens)")

    return result


def extract_rating(content: str) -> int:
    """Extract numeric rating from review content."""
    import re
    patterns = [
        r"(?:OVERALL|CONFIDENCE)\s*RATING:\s*(\d)",
        r"Rating:\s*(\d)/5",
        r"\[(\d)\]"
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def cross_validate(sonnet_rating: int, grok_result: Dict) -> Dict:
    """Cross-validate Sonnet (native) and Grok (OpenRouter) results."""

    grok_rating = extract_rating(grok_result.get("content", "")) if "content" in grok_result else 0

    # Average the ratings
    if sonnet_rating > 0 and grok_rating > 0:
        avg_rating = (sonnet_rating + grok_rating) / 2
    elif sonnet_rating > 0:
        avg_rating = sonnet_rating
    elif grok_rating > 0:
        avg_rating = grok_rating
    else:
        avg_rating = 0

    # Calculate agreement level
    if sonnet_rating > 0 and grok_rating > 0:
        diff = abs(sonnet_rating - grok_rating)
        if diff <= 1:
            agreement = "high"
        elif diff <= 2:
            agreement = "medium"
        else:
            agreement = "low"
    else:
        agreement = "partial"

    # Determine gate pass (need rating >= 4)
    gate_passed = avg_rating >= 4.0

    return {
        "sonnet_rating": sonnet_rating,
        "grok_rating": grok_rating,
        "average_rating": round(avg_rating, 2),
        "agreement": agreement,
        "gate_passed": gate_passed
    }


def generate_qa_report(sonnet_review: Optional[Dict], grok_result: Dict, cross_val: Dict, title: str) -> Dict:
    """Generate final QA review JSON."""

    return {
        "reviewed_at": datetime.now().isoformat(),
        "title": title,
        "reviewers": ["sonnet", "grok"],
        "models": {
            "sonnet": "claude-sonnet-4 (native)",
            "grok": GROK_MODEL
        },
        "ratings": {
            "sonnet": cross_val["sonnet_rating"],
            "grok": cross_val["grok_rating"],
            "average": cross_val["average_rating"],
            "agreement": cross_val["agreement"]
        },
        "sonnet_review": sonnet_review.get("content", "Not provided") if sonnet_review else "Done natively by Claude Code",
        "grok_review": grok_result.get("content", "Error: No review generated"),
        "tokens_used": {
            "sonnet": 0,  # Native - no API cost
            "grok": grok_result.get("tokens", 0),
            "total": grok_result.get("tokens", 0)
        },
        "gate_passed": cross_val["gate_passed"],
        "errors": {
            "sonnet": None,
            "grok": grok_result.get("error")
        }
    }


def run_grok_review(draft_path: Path, sonnet_rating: int = 0, sonnet_review_path: Optional[Path] = None) -> Dict:
    """Run Grok adversarial review via OpenRouter.

    Sonnet review should be done natively by Claude Code before calling this.
    Pass sonnet_rating from native review for cross-validation.
    """

    print(f"\n{'='*60}")
    print("GROK ADVERSARIAL QA REVIEW")
    print(f"{'='*60}\n")

    # Read draft
    content = draft_path.read_text(encoding='utf-8')

    # Extract title from frontmatter
    title = "Untitled"
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].split("\n"):
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"\'')
                    break

    print(f"Post: {title}")
    print(f"Draft: {draft_path}")
    print(f"Sonnet Rating (native): {sonnet_rating}/5\n")

    # Load Sonnet review if provided
    sonnet_review = None
    if sonnet_review_path and sonnet_review_path.exists():
        with open(sonnet_review_path, 'r', encoding='utf-8') as f:
            sonnet_review = json.load(f)
            if "rating" in sonnet_review:
                sonnet_rating = sonnet_review["rating"]

    # Call Grok for adversarial review
    print("Calling Grok for adversarial review...")
    grok_result = grok_review(content, title)

    # Cross-validation
    print("\nCross-Validation")
    cross_val = cross_validate(sonnet_rating, grok_result)

    # Generate report
    report = generate_qa_report(sonnet_review, grok_result, cross_val, title)

    # Determine output location
    output_path = draft_path.parent / "qa-review.json"

    # Save report
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print("QA REVIEW SUMMARY")
    print(f"{'='*60}")
    print(f"  Sonnet Rating (native): {cross_val['sonnet_rating']}/5")
    print(f"  Grok Rating (OpenRouter): {cross_val['grok_rating']}/5")
    print(f"  Average:      {cross_val['average_rating']}/5")
    print(f"  Agreement:    {cross_val['agreement']}")
    print(f"  Gate Passed:  {'✅ YES' if cross_val['gate_passed'] else '❌ NO (needs >= 4.0)'}")
    print(f"\n  Grok Tokens: {report['tokens_used']['grok']}")
    print(f"  Saved to: {output_path}")
    print(f"{'='*60}\n")

    return report


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dual_qa_review.py <draft.md> [sonnet_rating]")
        print("\nRuns Grok adversarial review via OpenRouter.")
        print("Sonnet structured review should be done natively by Claude Code first.")
        print("\nArguments:")
        print("  draft.md      Path to the blog post draft")
        print("  sonnet_rating Optional Sonnet rating (1-5) from native review")
        print("\nExample:")
        print("  python dual_qa_review.py blog/2025-12-20-post/draft.md 4")
        sys.exit(1)

    draft_path = Path(sys.argv[1])
    sonnet_rating = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    if not draft_path.exists():
        print(f"[!] File not found: {draft_path}")
        sys.exit(1)

    result = run_grok_review(draft_path, sonnet_rating)

    if not result["gate_passed"]:
        print("⚠️  QA gate failed. Review feedback and revise before publishing.")
        sys.exit(1)
    else:
        print("✅ QA gate passed. Ready for visuals and publishing.")
        sys.exit(0)
