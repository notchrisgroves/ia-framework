#!/usr/bin/env python3
"""
Image Generation Tools

FLUX image generation via OpenRouter API with dynamic model selection.

Usage:
    from tools.image_generation import FluxImageGenerator

    generator = FluxImageGenerator()
    generator.generate("cyberpunk cityscape", "output.png")

See generate-image.py for CLI usage.
"""

from .generate_image import FluxImageGenerator
from .prompts import build_prompt, analyze_topic, TOPIC_STYLES

__all__ = [
    'FluxImageGenerator',
    'build_prompt',
    'analyze_topic',
    'TOPIC_STYLES',
]
