#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context7 REST API wrapper package - Library documentation access

Token-efficient access to Context7 library documentation with:
- Field filtering (85% reduction in minimal mode)
- Smart caching (1 hour TTL)
- Progressive disclosure (minimal/standard/full modes)
- Top-N limiting (configurable results)

Usage:
    from servers.context7 import search_libraries, get_library_docs

    # Search for libraries
    result = search_libraries("requests", detail_level="minimal", limit=3)

    # Get documentation for a specific library
    docs = get_library_docs("vercel/next.js", topic="ssr", detail_level="minimal")

API Endpoints:
    - GET /search?query={term} - Search for libraries
    - GET /{org}/{library}?type=txt&topic={topic}&tokens={limit} - Get docs
"""

from .docs import search_libraries, get_library_docs

__all__ = ["search_libraries", "get_library_docs"]
