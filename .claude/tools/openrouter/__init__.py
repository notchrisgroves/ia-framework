"""
OpenRouter API Wrappers - Code API Pattern

Token-efficient wrappers for OpenRouter LLM models:
- chat: General text generation
- qa_review: Specialized blog post peer review
"""

from .chat import openrouter_chat
from .qa_review import qa_review_blog_post

__all__ = [
    'openrouter_chat',
    'qa_review_blog_post'
]
