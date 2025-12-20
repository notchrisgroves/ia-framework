"""
Framework Paths - Centralized path management for IA Framework

This module provides portable path resolution for all framework components.
All tools and scripts should import paths from here rather than hardcoding.

Usage:
    from tools.framework_paths import FRAMEWORK_DIR, SKILLS_DIR, get_output_path

Environment Variables:
    IA_FRAMEWORK_DIR - Override default framework location (default: ~/.claude)
"""

import os
from pathlib import Path
from typing import Optional


def _get_framework_root() -> Path:
    """
    Determine framework root directory.

    Resolution order:
    1. IA_FRAMEWORK_DIR environment variable (if set)
    2. ~/.claude (default)
    """
    env_dir = os.getenv("IA_FRAMEWORK_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    # Default: ~/.claude
    return Path.home() / ".claude"


# =============================================================================
# CORE DIRECTORIES
# =============================================================================

FRAMEWORK_DIR = _get_framework_root()
"""Root framework directory (~/.claude or IA_FRAMEWORK_DIR)"""

# Primary structure
AGENTS_DIR = FRAMEWORK_DIR / "agents"
SKILLS_DIR = FRAMEWORK_DIR / "skills"
COMMANDS_DIR = FRAMEWORK_DIR / "commands"
TOOLS_DIR = FRAMEWORK_DIR / "tools"
HOOKS_DIR = FRAMEWORK_DIR / "hooks"
DOCS_DIR = FRAMEWORK_DIR / "docs"
LIBRARY_DIR = FRAMEWORK_DIR / "library"
SERVERS_DIR = FRAMEWORK_DIR / "servers"

# Resources
RESOURCES_DIR = FRAMEWORK_DIR / "resources"
RESOURCES_LIBRARY_DIR = RESOURCES_DIR / "library"
BENCHMARKS_DIR = RESOURCES_LIBRARY_DIR / "benchmarks"
FRAMEWORKS_DIR = RESOURCES_LIBRARY_DIR / "frameworks"
REPOSITORIES_DIR = RESOURCES_LIBRARY_DIR / "repositories"
THREAT_INTEL_DIR = RESOURCES_LIBRARY_DIR / "threat-intelligence"
BOOKS_DIR = RESOURCES_LIBRARY_DIR / "books"

# User-generated content (gitignored)
OUTPUT_DIR = FRAMEWORK_DIR / "output"
SESSIONS_DIR = FRAMEWORK_DIR / "sessions"
PLANS_DIR = FRAMEWORK_DIR / "plans"
INPUT_DIR = FRAMEWORK_DIR / "input"

# Blog content
BLOG_DIR = FRAMEWORK_DIR / "blog"
BLOG_PAGES_DIR = BLOG_DIR / "pages"
BLOG_POSTS_DIR = BLOG_DIR / "posts"


# =============================================================================
# CORE FILES
# =============================================================================

CLAUDE_MD = FRAMEWORK_DIR / "CLAUDE.md"
SETTINGS_JSON = FRAMEWORK_DIR / "settings.json"
ENV_FILE = FRAMEWORK_DIR / ".env"
ENV_EXAMPLE = FRAMEWORK_DIR / ".env.example"
MANIFEST_FILE = FRAMEWORK_DIR / ".framework-manifest.yaml"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_skill_path(skill_name: str) -> Path:
    """Get path to a skill directory."""
    return SKILLS_DIR / skill_name


def get_skill_file(skill_name: str, filename: str = "SKILL.md") -> Path:
    """Get path to a specific file within a skill."""
    return SKILLS_DIR / skill_name / filename


def get_agent_path(agent_name: str) -> Path:
    """Get path to an agent file."""
    return AGENTS_DIR / f"{agent_name}.md"


def get_command_path(command_name: str) -> Path:
    """Get path to a command file."""
    return COMMANDS_DIR / f"{command_name}.md"


def get_output_path(category: str, *subpaths: str) -> Path:
    """
    Get path within output directory.

    Args:
        category: Top-level category (engagements, blog, career, etc.)
        subpaths: Additional path components

    Returns:
        Full path, creating directories if needed

    Example:
        get_output_path("engagements", "pentests", "acme-2025-01")
        → ~/.claude/output/engagements/pentests/acme-2025-01/
    """
    path = OUTPUT_DIR / category
    for subpath in subpaths:
        path = path / subpath
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_session_path(session_name: str) -> Path:
    """Get path for a session state file."""
    if not session_name.endswith(".md"):
        session_name = f"{session_name}.md"
    return SESSIONS_DIR / session_name


def get_resource_path(category: str, *subpaths: str) -> Path:
    """
    Get path within resources library.

    Args:
        category: Resource category (benchmarks, frameworks, repositories, etc.)
        subpaths: Additional path components

    Example:
        get_resource_path("frameworks", "nist", "sp800")
        → ~/.claude/resources/library/frameworks/nist/sp800/
    """
    path = RESOURCES_LIBRARY_DIR / category
    for subpath in subpaths:
        path = path / subpath
    return path


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, creating if needed."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_framework_configured() -> bool:
    """Check if framework is properly configured."""
    return CLAUDE_MD.exists() and SKILLS_DIR.exists()


def get_relative_path(absolute_path: Path) -> Path:
    """Convert absolute path to framework-relative path."""
    try:
        return absolute_path.relative_to(FRAMEWORK_DIR)
    except ValueError:
        return absolute_path


def resolve_framework_path(relative_path: str) -> Path:
    """Resolve a framework-relative path to absolute."""
    return FRAMEWORK_DIR / relative_path


# =============================================================================
# CONFIGURATION STATUS
# =============================================================================

def get_configuration_summary() -> dict:
    """Get summary of framework configuration for diagnostics."""
    return {
        "framework_dir": str(FRAMEWORK_DIR),
        "configured": is_framework_configured(),
        "env_override": os.getenv("IA_FRAMEWORK_DIR") is not None,
        "directories": {
            "agents": AGENTS_DIR.exists(),
            "skills": SKILLS_DIR.exists(),
            "commands": COMMANDS_DIR.exists(),
            "tools": TOOLS_DIR.exists(),
            "hooks": HOOKS_DIR.exists(),
            "resources": RESOURCES_DIR.exists(),
            "output": OUTPUT_DIR.exists(),
            "sessions": SESSIONS_DIR.exists(),
        },
        "files": {
            "CLAUDE.md": CLAUDE_MD.exists(),
            "settings.json": SETTINGS_JSON.exists(),
            ".env": ENV_FILE.exists(),
            ".framework-manifest.yaml": MANIFEST_FILE.exists(),
        }
    }


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    """Print configuration summary when run directly."""
    import json

    print("IA Framework Paths Configuration")
    print("=" * 50)
    print(f"Framework Directory: {FRAMEWORK_DIR}")
    print(f"Configured: {is_framework_configured()}")
    print()

    summary = get_configuration_summary()
    print("Directories:")
    for name, exists in summary["directories"].items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {name}")

    print("\nFiles:")
    for name, exists in summary["files"].items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {name}")

    print("\nPath Examples:")
    print(f"  Skill: {get_skill_path('security-testing')}")
    print(f"  Agent: {get_agent_path('security')}")
    print(f"  Output: {get_output_path('engagements', 'pentests')}")
