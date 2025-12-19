#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context7 Library Documentation Wrapper

Token-efficient access to library documentation through Context7 REST API.
Provides search, documentation retrieval, and smart caching.

Usage:
    from tools.context7 import search_libraries, get_library_docs

    # Search for libraries
    results = search_libraries("react", detail_level="minimal", limit=3)

    # Get documentation
    docs = get_library_docs("vercel/next.js", topic="ssr", detail_level="minimal")

API: https://context7.com/api/v1/
Author: Intelligence Adjacent
Version: 1.0.0
Last Updated: 2025-12-11
"""

import sys
import io
import json
import hashlib
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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
    raise ImportError("No HTTP client available. Install: pip install requests")

# =============================================================================
# Configuration
# =============================================================================
CACHE_DIR = Path(__file__).parents[2] / '.cache' / 'context7'
CACHE_TTL = 3600  # 1 hour (documentation rarely changes)
API_BASE_URL = "https://context7.com/api/v1"

# Load API key
def load_api_key() -> str:
    """Load Context7 API key from .env file"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parents[2] / '.env'
        load_dotenv(env_path)
        api_key = os.getenv("CONTEXT7_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass

    # Fallback to manual parsing
    env_file = Path(__file__).parents[2] / '.env'
    if not env_file.exists():
        raise FileNotFoundError(f".env file not found at {env_file}")

    with open(env_file, 'r', encoding='utf-8') as f:
        in_context7_section = False
        for line in f:
            stripped = line.strip()
            # Detect Context7 section
            if stripped == '# Context7':
                in_context7_section = True
            # Extract API_KEY from Context7 section
            elif in_context7_section and stripped.startswith('API_KEY='):
                return stripped.split('=', 1)[1].strip()
            # Exit Context7 section on next section header
            elif in_context7_section and stripped.startswith('#') and stripped != '# Context7':
                break

    raise ValueError("CONTEXT7_API_KEY not found in .env file")

API_KEY = load_api_key()

# =============================================================================
# Core Functions
# =============================================================================

def search_libraries(
    query: str,
    detail_level: str = "minimal",
    limit: int = 3,
    use_cache: bool = True
) -> Dict:
    """
    Search for libraries by name/keyword

    Args:
        query: Search term (e.g., "react", "requests")
        detail_level: "minimal" (top 3, ID only), "standard" (top 10 with metadata), "full" (all)
        limit: Max results in summary
        use_cache: Use cached results if available

    Returns:
        Dict with summary, outputFile, message

    Token efficiency:
        - Minimal: ~150 tokens (85% reduction)
        - Standard: ~500 tokens (50% reduction)
        - Full: Use outputFile path
    """
    # Check cache
    if use_cache:
        cached_result = check_cache(f"search_{query}")
        if cached_result:
            cached_result['cached'] = True
            return cached_result

    # Determine output location
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_name = query.replace("/", "_").replace(":", "_")
    filename = f"search-{safe_name}-{timestamp}.json"

    session_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(__file__).parents[2] / "sessions" / session_date / "context7"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    try:
        # Make API request
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(
            f"{API_BASE_URL}/search",
            params={"query": query},
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        full_response = response.json()

        # Save full response
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(full_response, f, indent=2)

        # Parse based on detail level
        if detail_level == "minimal":
            summary = extract_minimal_libraries(full_response, min(limit, 3))
        elif detail_level == "standard":
            summary = extract_standard_libraries(full_response, limit if limit > 3 else 10)
        else:  # full
            summary = full_response

        # Generate message
        message = format_library_message(summary, query, output_file)

        # Save to cache
        result = {"summary": summary, "outputFile": str(output_file), "message": message}
        if use_cache:
            save_to_cache(result, f"search_{query}")

        result['cached'] = False
        return result

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Library search failed: {str(e)}",
            "outputFile": str(output_file)
        }


def get_library_docs(
    library_path: str,
    topic: Optional[str] = None,
    tokens: int = 500,
    detail_level: str = "minimal",
    use_cache: bool = True
) -> Dict:
    """
    Get library documentation with token-efficient filtering

    Args:
        library_path: Library path (e.g., 'vercel/next.js', 'psf/requests')
        topic: Optional topic to focus on (e.g., 'authentication', 'ssr')
        tokens: Max tokens of documentation to retrieve
        detail_level: "minimal" (top 3 examples), "standard" (top 10), "full" (all)
        use_cache: Use cached results if available

    Returns:
        Dict with summary, outputFile, message

    Token efficiency:
        - Minimal: ~300 tokens (97% reduction)
        - Standard: ~800 tokens (92% reduction)
        - Full: Use outputFile path
    """
    # Check cache
    cache_key = f"docs_{library_path}_{topic}_{tokens}"
    if use_cache:
        cached_result = check_cache(cache_key)
        if cached_result:
            cached_result['cached'] = True
            return cached_result

    # Determine output location
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    safe_path = library_path.replace("/", "_")
    safe_topic = f"-{topic}" if topic else ""
    filename = f"{safe_path}{safe_topic}-{timestamp}.md"

    session_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(__file__).parents[2] / "sessions" / session_date / "context7"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    try:
        # Make API request
        headers = {"Authorization": f"Bearer {API_KEY}"}
        params = {
            "type": "txt",
            "tokens": tokens if detail_level == "full" else min(tokens, 1000)
        }
        if topic:
            params["topic"] = topic

        response = requests.get(
            f"{API_BASE_URL}/{library_path}",
            params=params,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        full_response = response.text

        # Save full response
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_response)

        # Parse based on detail level
        if detail_level == "minimal":
            summary = extract_minimal_examples(full_response, limit=3)
        elif detail_level == "standard":
            summary = extract_standard_examples(full_response, limit=10)
        else:  # full
            summary = {
                "message": f"Full documentation in {output_file}",
                "exampleCount": count_examples(full_response)
            }

        # Generate message
        message = format_docs_message(summary, library_path, topic, output_file)

        # Save to cache
        result = {"summary": summary, "outputFile": str(output_file), "message": message}
        if use_cache:
            save_to_cache(result, cache_key)

        result['cached'] = False
        return result

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Documentation retrieval failed: {str(e)}",
            "outputFile": str(output_file)
        }


# =============================================================================
# Helper Functions
# =============================================================================

def extract_minimal_libraries(response: Dict, limit: int) -> Dict:
    """Extract minimal library info (ID and name only) - 85% token reduction"""
    libraries = []

    if isinstance(response, dict) and 'results' in response:
        libs = response['results']
    elif isinstance(response, dict) and 'libraries' in response:
        libs = response['libraries']
    elif isinstance(response, list):
        libs = response
    else:
        libs = []

    for lib in libs[:limit]:
        libraries.append({
            "title": lib.get("title", lib.get("name", "Unknown")),
            "id": lib.get("id", lib.get("path", ""))
        })

    return {
        "total": len(libs) if isinstance(libs, list) else 0,
        "topMatches": libraries,
        "message": f"Found {len(libs)} matches, showing top {min(limit, len(libraries))}"
    }


def extract_standard_libraries(response: Dict, limit: int) -> Dict:
    """Extract standard library info with descriptions - 50% token reduction"""
    libraries = []

    if isinstance(response, dict) and 'results' in response:
        libs = response['results']
    elif isinstance(response, dict) and 'libraries' in response:
        libs = response['libraries']
    elif isinstance(response, list):
        libs = response
    else:
        libs = []

    for lib in libs[:limit]:
        libraries.append({
            "title": lib.get("title", lib.get("name", "Unknown")),
            "id": lib.get("id", lib.get("path", "")),
            "description": lib.get("description", ""),
            "trustScore": lib.get("trustScore", lib.get("trust_score", "N/A"))
        })

    return {
        "total": len(libs),
        "matches": libraries,
        "truncated": len(libs) > limit
    }


def extract_minimal_examples(doc_text: str, limit: int) -> Dict:
    """Extract minimal examples (title + code only) - 97% token reduction"""
    examples = []
    current_title = None
    current_code = []
    in_code_block = False

    for line in doc_text.split('\n'):
        if line.startswith('###'):
            if current_title and current_code:
                examples.append({
                    "title": current_title,
                    "code": '\n'.join(current_code)
                })
            current_title = line.replace('###', '').strip()
            current_code = []
            in_code_block = False
        elif line.startswith('```'):
            in_code_block = not in_code_block
        elif in_code_block:
            current_code.append(line)

    if current_title and current_code:
        examples.append({"title": current_title, "code": '\n'.join(current_code)})

    return {
        "exampleCount": len(examples),
        "topExamples": examples[:limit],
        "message": f"Extracted {len(examples)} examples, showing top {min(limit, len(examples))}"
    }


def extract_standard_examples(doc_text: str, limit: int) -> Dict:
    """Extract standard examples with context - 92% token reduction"""
    examples = []
    current_example = {}
    in_code_block = False

    for line in doc_text.split('\n'):
        if line.startswith('###'):
            if current_example:
                examples.append(current_example)
            current_example = {"title": line.replace('###', '').strip(), "description": "", "code": ""}
        elif line.startswith('```'):
            in_code_block = not in_code_block
        elif in_code_block and current_example:
            current_example["code"] += line + '\n'
        elif current_example and not in_code_block and line.strip():
            if not current_example["description"] and not line.startswith('-'):
                current_example["description"] = line.strip()

    if current_example:
        examples.append(current_example)

    return {
        "exampleCount": len(examples),
        "examples": examples[:limit],
        "truncated": len(examples) > limit
    }


def count_examples(doc_text: str) -> int:
    """Count total examples in documentation"""
    return doc_text.count('###')


def format_library_message(summary: Dict, query: str, output_file: Path) -> str:
    """Format human-readable message for library search"""
    if isinstance(summary, dict) and "topMatches" in summary:
        message = f"[+] Library search: {query}\n"
        message += f"    Total matches: {summary['total']}\n"
        message += f"    Top matches:\n"
        for lib in summary["topMatches"]:
            message += f"      - {lib['title']} ({lib['id']})\n"
        message += f"    Full results: {output_file}"
    else:
        message = f"[+] Found {summary.get('total', 0)} matches for '{query}'\n"
        message += f"    Full results: {output_file}"
    return message


def format_docs_message(summary: Dict, library_path: str, topic: Optional[str], output_file: Path) -> str:
    """Format human-readable message for documentation"""
    topic_str = f" (topic: {topic})" if topic else ""
    message = f"[+] Documentation for {library_path}{topic_str}\n"

    if "exampleCount" in summary:
        message += f"    Examples found: {summary['exampleCount']}\n"
        if "topExamples" in summary:
            message += f"    Showing top {len(summary['topExamples'])} examples\n"
    elif "examples" in summary:
        message += f"    Examples returned: {len(summary['examples'])}\n"

    message += f"    Full documentation: {output_file}"
    return message


def check_cache(cache_key: str) -> Optional[Dict]:
    """Check if cached result exists and is fresh"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{hashlib.md5(cache_key.encode()).hexdigest()}.json"

    if cache_file.exists():
        cache_age = time.time() - cache_file.stat().st_mtime
        if cache_age < CACHE_TTL:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None


def save_to_cache(data: Dict, cache_key: str):
    """Save result to cache"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{hashlib.md5(cache_key.encode()).hexdigest()}.json"
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI interface for Context7"""
    import argparse

    parser = argparse.ArgumentParser(description='Context7 Library Documentation')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for libraries')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--detail', default='minimal', choices=['minimal', 'standard', 'full'])
    search_parser.add_argument('--limit', type=int, default=3, help='Max results')

    # Get docs command
    docs_parser = subparsers.add_parser('get', help='Get library documentation')
    docs_parser.add_argument('library', help='Library path (e.g., vercel/next.js)')
    docs_parser.add_argument('--topic', help='Focus topic')
    docs_parser.add_argument('--tokens', type=int, default=500, help='Max tokens')
    docs_parser.add_argument('--detail', default='minimal', choices=['minimal', 'standard', 'full'])

    args = parser.parse_args()

    if args.command == 'search':
        result = search_libraries(args.query, detail_level=args.detail, limit=args.limit)
    elif args.command == 'get':
        result = get_library_docs(
            args.library,
            topic=args.topic,
            tokens=args.tokens,
            detail_level=args.detail
        )
    else:
        parser.print_help()
        sys.exit(1)

    if "error" in result:
        print(f"[!] Error: {result['error']}")
        sys.exit(1)
    else:
        print(result["message"])
        if result.get("cached"):
            print("    [Served from cache]")


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
