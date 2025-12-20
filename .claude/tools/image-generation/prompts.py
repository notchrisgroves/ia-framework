#!/usr/bin/env python3
"""
Smart Prompt Generation for FLUX Image Generation

Provides content analysis and variety in image prompts based on topic detection.
Prevents style lock-in by offering varied color palettes, scenes, and compositions.

Usage:
    from prompts import build_prompt, analyze_topic

    topic = analyze_topic("Zero Trust Network Security", draft_content)
    prompt = build_prompt("Zero trust architecture", topic=topic)

Author: Intelligence Adjacent Framework
"""

import random
from typing import Optional, List, Dict

# =============================================================================
# Topic Detection Keywords
# =============================================================================

TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "security": [
        "hack", "pentest", "vulnerability", "breach", "attack", "defense",
        "firewall", "intrusion", "malware", "exploit", "threat", "security",
        "penetration", "audit", "compliance", "risk", "zero trust", "encryption"
    ],
    "ai": [
        "model", "neural", "machine learning", "llm", "agent", "intelligence",
        "claude", "gpt", "training", "inference", "embedding", "transformer",
        "ai", "artificial", "cognitive", "autonomous"
    ],
    "infrastructure": [
        "server", "docker", "kubernetes", "deploy", "cloud", "vps",
        "container", "orchestration", "devops", "pipeline", "ci/cd",
        "network", "dns", "load balancer", "infrastructure"
    ],
    "framework": [
        "architecture", "system", "design", "pattern", "workflow", "skill",
        "agent", "hook", "command", "integration", "modular", "structure"
    ],
    "career": [
        "job", "resume", "interview", "professional", "career", "hire",
        "application", "recruiter", "linkedin", "portfolio"
    ],
}

# =============================================================================
# Style Variation Pools
# =============================================================================

TOPIC_STYLES: Dict[str, Dict[str, List[str]]] = {
    "security": {
        "palettes": [
            "red and black alert colors with amber warning accents",
            "electric green matrix-style on deep black",
            "cyan security shields with crimson threat indicators",
            "dark purple with red intrusion alerts",
            "orange and black warning scheme"
        ],
        "scenes": [
            "security operations center with threat dashboards",
            "terminal interface showing intrusion detection",
            "digital fortress with layered defenses",
            "network topology with encrypted pathways",
            "close-up of analyst reviewing threat data"
        ],
        "moods": ["intense", "vigilant", "focused", "defensive", "alert"]
    },
    "ai": {
        "palettes": [
            "purple and electric blue neural glow",
            "gold and white clean futuristic",
            "rainbow data streams on dark background",
            "teal and magenta synthetic intelligence",
            "silver and blue holographic"
        ],
        "scenes": [
            "abstract neural network with flowing data",
            "human-AI collaboration at holographic interface",
            "data visualization with interconnected nodes",
            "futuristic workspace with AI assistants",
            "portrait of human directing AI systems"
        ],
        "moods": ["innovative", "collaborative", "futuristic", "intelligent", "harmonious"]
    },
    "infrastructure": {
        "palettes": [
            "orange and teal industrial",
            "green status lights on dark gray",
            "blue network connections on black",
            "amber and steel industrial",
            "white and blue clean datacenter"
        ],
        "scenes": [
            "modern server room corridor with status lights",
            "container orchestration visualization",
            "cloud infrastructure diagram come to life",
            "network operations center",
            "deployment pipeline visualization"
        ],
        "moods": ["efficient", "reliable", "scalable", "organized", "professional"]
    },
    "framework": {
        "palettes": [
            "multi-color modular blocks",
            "blue and gold architectural",
            "green and purple component colors",
            "cyan interconnected elements",
            "warm amber with cool blue accents"
        ],
        "scenes": [
            "modular system with orbiting components",
            "architectural blueprint come to life",
            "interconnected building blocks",
            "workflow diagram as 3D environment",
            "system overview with labeled modules"
        ],
        "moods": ["structured", "elegant", "modular", "organized", "cohesive"]
    },
    "career": {
        "palettes": [
            "professional blue and gold",
            "warm amber and navy",
            "clean white with accent colors",
            "sophisticated gray and teal",
            "confident red and black"
        ],
        "scenes": [
            "professional at futuristic workstation",
            "digital portfolio showcase",
            "career path visualization",
            "networking in high-tech environment",
            "achievement milestone celebration"
        ],
        "moods": ["confident", "professional", "ambitious", "successful", "determined"]
    },
    "general": {
        "palettes": [
            "cyan and magenta neon on dark",
            "warm amber and cool blue contrast",
            "purple and gold elegant",
            "green and orange complementary",
            "red and teal vibrant"
        ],
        "scenes": [
            "futuristic command center",
            "abstract digital landscape",
            "cyberpunk cityscape at night",
            "holographic interface workspace",
            "data flow visualization"
        ],
        "moods": ["atmospheric", "dynamic", "immersive", "engaging", "striking"]
    }
}

TECHNIQUES: List[str] = [
    "detailed digital art with cinematic lighting",
    "clean vector-inspired illustration",
    "atmospheric with volumetric lighting",
    "holographic elements and wireframe overlays",
    "particle effects and data visualization",
    "anime-inspired with sharp details",
]

COMPOSITIONS: List[str] = [
    "wide establishing shot",
    "medium shot with clear focal point",
    "close-up portrait composition",
    "orbital/overview perspective",
    "dynamic diagonal composition",
]

# =============================================================================
# Analysis Functions
# =============================================================================

def analyze_topic(title: str, content: Optional[str] = None) -> str:
    """
    Detect primary topic from title and content.

    Args:
        title: Article/post title
        content: Optional full content text

    Returns:
        Topic key (security, ai, infrastructure, framework, career, general)
    """
    text = f"{title} {content or ''}".lower()

    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[topic] = score

    best_topic = max(scores, key=scores.get)
    return best_topic if scores[best_topic] > 0 else "general"


def build_prompt(
    subject: str,
    topic: Optional[str] = None,
    palette: Optional[str] = None,
    scene: Optional[str] = None,
    mood: Optional[str] = None,
    technique: Optional[str] = None,
    composition: Optional[str] = None
) -> str:
    """
    Build a varied image prompt with smart defaults.

    Args:
        subject: Main subject/concept to visualize
        topic: Topic category (auto-detected if None)
        palette: Color palette override
        scene: Scene type override
        mood: Mood/atmosphere override
        technique: Art technique override
        composition: Composition style override

    Returns:
        Complete prompt string for FLUX
    """
    # Default to general if no topic specified
    if topic is None or topic not in TOPIC_STYLES:
        topic = "general"

    style = TOPIC_STYLES[topic]

    # Select from pools if not specified
    palette = palette or random.choice(style["palettes"])
    scene = scene or random.choice(style["scenes"])
    mood = mood or random.choice(style["moods"])
    technique = technique or random.choice(TECHNIQUES)
    composition = composition or random.choice(COMPOSITIONS)

    # Build prompt
    prompt = f"""{subject}, depicted in a {scene} environment.
{palette} color scheme. {mood} atmosphere.
{composition}. {technique}.
Professional quality, highly detailed, atmospheric lighting."""

    return prompt.strip()


def build_hero_prompt(title: str, content: Optional[str] = None) -> str:
    """
    Build a hero image prompt from blog post title and content.

    Args:
        title: Blog post title
        content: Optional draft content

    Returns:
        Complete prompt for hero image generation
    """
    topic = analyze_topic(title, content)

    # Extract key concept from title
    # Remove common prefixes/suffixes
    concept = title
    for prefix in ["How to ", "Why ", "What is ", "The ", "A ", "An "]:
        if concept.startswith(prefix):
            concept = concept[len(prefix):]

    return build_prompt(concept, topic=topic)


# =============================================================================
# CLI Test
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        title = " ".join(sys.argv[1:])
        topic = analyze_topic(title)
        prompt = build_hero_prompt(title)
        print(f"Title: {title}")
        print(f"Detected topic: {topic}")
        print(f"\nGenerated prompt:\n{prompt}")
    else:
        # Demo with sample titles
        samples = [
            "Zero Trust Network Security Implementation",
            "Building AI Agents with Claude Code",
            "Docker Container Orchestration Best Practices",
            "Framework Architecture Deep Dive",
            "Career Development in Cybersecurity"
        ]

        for title in samples:
            topic = analyze_topic(title)
            prompt = build_hero_prompt(title)
            print(f"\n{'='*60}")
            print(f"Title: {title}")
            print(f"Topic: {topic}")
            print(f"Prompt: {prompt[:100]}...")
