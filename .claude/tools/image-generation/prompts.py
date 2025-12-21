#!/usr/bin/env python3
"""
Smart Prompt Generation for FLUX Image Generation

Provides content analysis and variety in image prompts based on topic detection.
FALLBACK ONLY - For best results, create a custom hero-prompt.txt file.

BRAND STYLE REQUIREMENTS (MANDATORY):
All hero images MUST include:
- "90s anime style with detailed linework" - Core art style
- "cyberpunk aesthetic" - Neon lighting, tech atmosphere
- Deep purple and electric blue (or similar neon palette)
- "Dramatic lighting" with atmospheric fog

See: skills/writer/reference/BRAND-GUIDE.md for examples

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
            "deep purple and electric blue with neon accents",
            "cyan and magenta cyberpunk glow",
            "amber and teal contrasting neon",
            "electric green matrix-style with purple highlights",
            "neon pink and blue synthwave"
        ],
        "scenes": [
            "floating hexagonal modules orbiting a central figure in a void",
            "massive glowing terminal with cascading data streams",
            "library of floating knowledge containers in darkness",
            "switchboard operator routing glowing data to personas",
            "architect orchestrating interconnected systems"
        ],
        "moods": ["mysterious", "powerful", "orchestrated", "vast", "illuminated"]
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
    "90s anime style with detailed linework, cyberpunk aesthetic, dramatic lighting",
    "90s anime style, cyberpunk neon aesthetic, atmospheric fog and dramatic shadows",
    "detailed anime illustration, cyberpunk setting, dramatic lighting illuminating fog",
    "90s anime style with detailed character expressions, cyberpunk neon glow",
    "anime style with detailed linework, cyberpunk aesthetic, dramatic atmospheric lighting",
]

COMPOSITIONS: List[str] = [
    "dramatic wide shot with lone figure",
    "medium shot with glowing elements as focal point",
    "cinematic composition with depth layers",
    "atmospheric scene with fog and neon lighting",
    "dynamic composition with cascading light",
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

    Creates stylized atmospheric visuals - NOT diagrams or charts.
    Explicitly avoids text/words in the image.

    Args:
        title: Blog post title
        content: Optional draft content

    Returns:
        Complete prompt for hero image generation
    """
    topic = analyze_topic(title, content)

    # Map topics to visual concepts (NOT the title text)
    TOPIC_CONCEPTS = {
        "security": "cybersecurity operations and digital defense systems",
        "ai": "artificial intelligence and neural network visualization",
        "infrastructure": "modern server infrastructure and cloud systems",
        "framework": "modular software architecture with interconnected components",
        "career": "professional achievement and career growth",
        "general": "futuristic technology workspace"
    }

    concept = TOPIC_CONCEPTS.get(topic, TOPIC_CONCEPTS["general"])

    # Build prompt with explicit no-text instruction
    base_prompt = build_prompt(concept, topic=topic)

    # Add no-text constraint
    return f"{base_prompt}\nNo text, no words, no letters, no labels. Pure visual art only."


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
