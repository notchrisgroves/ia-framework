#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qa_review_blog_post wrapper - Specialized Blog Post Peer Review

Automated peer review for blog posts using OpenRouter models.

Optimization strategies:
- Field filtering: 80% reduction (structured review format)
- Pre-aggregation: Extract issues, rating, recommendations
- Smart model selection: Technical vs general content
- File storage: Full review saved for audit trail
"""

import sys
import io
import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables. Check ~/.claude/.env")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model selection - use dynamic selection from OpenRouter API
# Import from tools/research/openrouter for latest model discovery
try:
    sys.path.insert(0, str(Path(__file__).parents[1] / 'tools' / 'research' / 'openrouter'))
    from fetch_models import get_latest_model
    TECHNICAL_MODEL = get_latest_model("x-ai", prefer_keywords=["code"]) or "x-ai/grok-code-fast-1"
    GENERAL_MODEL = get_latest_model("x-ai") or "x-ai/grok-4-fast"
except Exception:
    # Fallback to defaults if dynamic selection fails
    TECHNICAL_MODEL = "x-ai/grok-code-fast-1"
    GENERAL_MODEL = "x-ai/grok-4-fast"


def qa_review_blog_post(
    content: str,
    content_type: str = "auto",
    detail_level: str = "standard",
    engagement_dir: Optional[str] = None
) -> Dict:
    """
    Perform automated peer review of blog post content.

    Args:
        content: Blog post content (markdown format)
        content_type: "technical", "general", or "auto" (default: auto-detect)
        detail_level: "minimal" (~200 tokens), "standard" (~800 tokens, default), "full" (all data)
        engagement_dir: Optional directory for output files

    Returns:
        Dict with:
        - summary: Structured review findings
        - outputFile: Path to full review
        - message: Human-readable summary
        - model: Model used for review

    Token efficiency:
    - Minimal mode: ~200 tokens (85% reduction)
    - Standard mode: ~800 tokens (40% reduction)
    - Full mode: Use outputFile path instead

    Review includes:
    1. Technical accuracy (claims, code examples, methodology)
    2. Readability (structure, clarity, flow)
    3. Link validity (conceptual checks)
    4. Completeness (missing context, caveats)
    5. Overall rating (1-5)
    6. Specific issues and recommendations
    """

    # Auto-detect content type
    if content_type == "auto":
        technical_keywords = ["code", "security", "vulnerability", "exploit", "smart contract",
                             "python", "javascript", "solidity", "sql", "api", "encryption"]
        content_lower = content.lower()
        is_technical = any(keyword in content_lower for keyword in technical_keywords)
        content_type = "technical" if is_technical else "general"

    # Select model based on content type
    model = TECHNICAL_MODEL if content_type == "technical" else GENERAL_MODEL

    # Determine output location
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"qa-review-{timestamp}.json"

    if engagement_dir:
        output_dir = Path(engagement_dir)
    else:
        session_date = datetime.now().strftime("%Y-%m-%d")
        output_dir = Path.home() / ".claude" / "sessions" / session_date / "qa-reviews"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    # Construct review prompt
    system_prompt = """You are a technical peer reviewer for a professional blog focused on cybersecurity, AI, and system building (Intelligence Adjacent framework).

Your review should assess:
1. Technical Accuracy - Are claims correct? Any misleading statements? Code examples valid?
2. Readability - Is it clear, well-structured, and engaging?
3. Link Validity - Do mentioned resources exist? (conceptual check)
4. Completeness - Missing important context or caveats?

Provide:
- Overall rating (1-5, where 5 is publication-ready)
- Specific issues found (categorized by severity: critical, major, minor)
- Recommended corrections
- What's done well

Be thorough but constructive. Focus on accuracy and clarity."""

    user_prompt = f"""Review this blog post draft:

{content}

Provide a structured review with:
1. Overall Rating (1-5)
2. Technical Accuracy Issues
3. Readability Issues
4. Link Validity Issues
5. Completeness Issues
6. Recommended Corrections (prioritized)
7. What's Done Well"""

    # Prepare API request
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
        "temperature": 0.3,  # Lower temperature for more consistent reviews
        "max_tokens": 4096
    }

    try:
        # Execute API call
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        full_response = response.json()

        # Save full response to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(full_response, f, indent=2)

        # Parse review content
        review_content = full_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = full_response.get("usage", {})

        # Extract structured information (basic parsing)
        issues = extract_issues(review_content)
        rating = extract_rating(review_content)
        recommendations = extract_recommendations(review_content)

        # Build summary based on detail level
        if detail_level == "minimal":
            summary = {
                "rating": rating,
                "issueCount": len(issues),
                "criticalIssues": [i for i in issues if i.get("severity") == "critical"],
                "topRecommendations": recommendations[:3] if recommendations else [],
                "reviewPreview": review_content[:500] + "..." if len(review_content) > 500 else review_content
            }
        elif detail_level == "standard":
            summary = {
                "rating": rating,
                "issues": issues,
                "recommendations": recommendations,
                "reviewContent": review_content,
                "tokens": {
                    "prompt": usage.get("prompt_tokens", 0),
                    "completion": usage.get("completion_tokens", 0),
                    "total": usage.get("total_tokens", 0)
                }
            }
        else:  # full
            summary = {
                "message": f"Full review in {output_file}",
                "rating": rating,
                "issueCount": len(issues),
                "tokens": usage
            }

        # Generate human-readable message
        message = f"[+] QA Review complete (model: {model})\n"
        message += f"    Rating: {rating}/5\n"
        message += f"    Issues found: {len(issues)}\n"
        message += f"    Critical: {len([i for i in issues if i.get('severity') == 'critical'])}\n"
        message += f"    Major: {len([i for i in issues if i.get('severity') == 'major'])}\n"
        message += f"    Minor: {len([i for i in issues if i.get('severity') == 'minor'])}\n"
        message += f"    Tokens used: {usage.get('total_tokens', 0)}\n"
        message += f"    Full review: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message,
            "model": model,
            "contentType": content_type
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout (120s exceeded)",
            "outputFile": str(output_file),
            "model": model
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error: {e.response.status_code} - {e.response.text}",
            "outputFile": str(output_file),
            "model": model
        }
    except Exception as e:
        return {
            "error": str(e),
            "outputFile": str(output_file),
            "model": model
        }


def extract_rating(review_content: str) -> int:
    """Extract overall rating (1-5) from review content."""
    import re
    # Look for patterns like "Rating: 3/5" or "Overall rating: 3/5"
    patterns = [
        r"rating[:\s]+(\d)/5",
        r"overall[:\s]+(\d)/5",
        r"score[:\s]+(\d)/5"
    ]

    for pattern in patterns:
        match = re.search(pattern, review_content, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return 0  # Unknown rating


def extract_issues(review_content: str) -> List[Dict]:
    """Extract issues from review content with basic categorization."""
    issues = []

    # Simple keyword-based extraction
    critical_keywords = ["critical", "severe", "major flaw", "incorrect", "wrong", "misleading"]
    major_keywords = ["major", "significant", "important", "should fix"]
    minor_keywords = ["minor", "small", "consider", "suggest"]

    # Split by lines and look for issue indicators
    lines = review_content.split('\n')
    current_issue = None

    for line in lines:
        line_lower = line.lower()

        # Detect issue severity
        severity = "minor"
        if any(kw in line_lower for kw in critical_keywords):
            severity = "critical"
        elif any(kw in line_lower for kw in major_keywords):
            severity = "major"

        # Look for bullet points or numbered lists (common in reviews)
        if line.strip().startswith(('-', '*', '•')) or (len(line) > 0 and line[0].isdigit() and '.' in line[:3]):
            issue_text = line.strip().lstrip('-*•0123456789. ')
            if len(issue_text) > 10:  # Meaningful issue
                issues.append({
                    "severity": severity,
                    "description": issue_text[:200]  # Limit length
                })

    return issues


def extract_recommendations(review_content: str) -> List[str]:
    """Extract recommendations from review content."""
    recommendations = []

    # Look for recommendation sections
    lines = review_content.split('\n')
    in_recommendations = False

    for line in lines:
        line_lower = line.lower()

        # Detect recommendation section
        if 'recommendation' in line_lower or 'suggested' in line_lower or 'should' in line_lower:
            in_recommendations = True

        # Extract recommendation items
        if in_recommendations:
            if line.strip().startswith(('-', '*', '•')) or (len(line) > 0 and line[0].isdigit() and '.' in line[:3]):
                rec_text = line.strip().lstrip('-*•0123456789. ')
                if len(rec_text) > 10:
                    recommendations.append(rec_text[:300])  # Limit length

    return recommendations[:10]  # Top 10 recommendations


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qa_review.py <markdown_file> [content_type] [detail_level]")
        print("\nContent types: technical, general, auto (default: auto)")
        print("Detail levels: minimal, standard (default), full")
        print("\nExample: python qa_review.py draft.md technical standard")
        sys.exit(1)

    markdown_file = sys.argv[1]
    content_type = sys.argv[2] if len(sys.argv) > 2 else "auto"
    detail_level = sys.argv[3] if len(sys.argv) > 3 else "standard"

    # Read markdown file
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[!] Error reading file: {e}")
        sys.exit(1)

    result = qa_review_blog_post(content, content_type=content_type, detail_level=detail_level)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
        print(f"\nRating: {result['summary'].get('rating', 'N/A')}/5")

        if detail_level == "standard" and "reviewContent" in result['summary']:
            print(f"\nFull Review:\n{result['summary']['reviewContent']}")
