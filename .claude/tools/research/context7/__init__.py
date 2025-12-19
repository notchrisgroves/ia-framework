"""
Context7 REST API Wrapper

Token-efficient library documentation access through Context7.
Provides search, documentation retrieval, and smart caching.

Usage:
    from tools.context7 import search_libraries, get_library_docs

    # Search for libraries
    results = search_libraries("react", detail_level="minimal", limit=3)
    print(results["message"])

    # Get documentation for a specific library
    docs = get_library_docs("vercel/next.js", topic="ssr", detail_level="minimal")
    print(docs["message"])

API: https://context7.com/api/v1/
"""

from .docs import search_libraries, get_library_docs

__all__ = ["search_libraries", "get_library_docs"]

__version__ = "1.0.0"
