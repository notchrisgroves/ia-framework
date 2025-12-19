#!/usr/bin/env python3
"""
Level 1 Hook: Load agent and skill context when Task tool is invoked

Trigger: PreToolUse when tool_name == 'Task'
Purpose: Load agent.md + SKILL.md + tool catalog + MODEL ROUTING for specialized agent work
Output: Agent prompt, skill context, tool catalog, and model guidance wrapped in <system-reminder>
"""
import json
import sys
import io
from pathlib import Path

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Agent to skill mapping
AGENT_SKILL_MAP = {
    "security": [
        "security-testing",      # Pentesting, vuln scan, segmentation
        "architecture-review",   # Threat modeling, security architecture
        "code-review",           # Security code analysis
        "dependency-audit",      # Supply chain security
        "threat-intel",          # CVE research, threat landscape
        "secure-config",         # CIS/STIG hardening validation
        "benchmark-generation",  # Compliance script generation
        "security-advisory",     # Risk assessment, ad-hoc guidance
    ],
    "writer": ["writer"],
    "advisor": ["career", "osint-research", "qa-review"],
    "legal": ["legal"],
}

# Model routing trigger keywords (from library/model-selection-matrix.md)
MODEL_TRIGGERS = {
    "opus": [
        "design plan", "test plan", "methodology", "approach design",
        "stuck", "blocked", "hitting wall", "can't figure", "not finding",
        "novel", "complex", "architecture", "strategic", "multi-factor",
        "ultrathink", "think deeply", "comprehensive analysis"
    ],
    "grok": [
        "qa review", "second opinion", "what am i missing", "challenge assumptions",
        "adversarial", "blind spots", "verify findings", "double check"
    ],
    "grok-code": [
        "why is this vulnerable", "explain why", "reasoning traces",
        "understand why", "root cause", "how does this exploit"
    ],
    "perplexity": [
        "osint", "research", "investigate", "intelligence gathering",
        "industry context", "threat landscape", "current events"
    ],
    "haiku": [
        "validate", "checklist", "verify compliance", "format check",
        "quick validation", "scope check", "simple task"
    ]
}


def detect_model_escalation(prompt_text):
    """
    Detect model escalation triggers from prompt text.

    Returns:
        Tuple of (recommended_model, trigger_matched, reason)
    """
    prompt_lower = prompt_text.lower()

    # Check each model's triggers in priority order
    # Opus first (for planning/stuck), then specialized models
    for model, triggers in MODEL_TRIGGERS.items():
        for trigger in triggers:
            if trigger in prompt_lower:
                return model, trigger, get_model_reason(model)

    # Default to sonnet if no triggers matched
    return "sonnet", None, "Default execution model"


def get_model_reason(model):
    """Get human-readable reason for model selection."""
    reasons = {
        "opus": "Complex reasoning needed (planning, stuck, novel problem)",
        "grok": "Adversarial QA review (challenge assumptions, find gaps)",
        "grok-code": "WHY explanation needed (reasoning traces for vulnerabilities)",
        "perplexity": "Research with citations (OSINT, threat landscape)",
        "haiku": "Fast validation (checklists, format checks)",
        "sonnet": "Default execution (known patterns, standard workflows)"
    }
    return reasons.get(model, "Unknown model")


def load_agent_context(subagent_type):
    """
    Load agent prompt file.

    Args:
        subagent_type: Agent name (e.g., "security", "writer")

    Returns:
        Tuple of (agent_content, error_message)
    """
    agent_file = Path(f"agents/{subagent_type}.md")

    if not agent_file.exists():
        return None, f"WARNING: Agent file not found: agents/{subagent_type}.md"

    try:
        content = agent_file.read_text(encoding='utf-8')
        return content, None
    except Exception as e:
        return None, f"ERROR reading agent file: {e}"


def load_skill_context(skill_name):
    """
    Load skill SKILL.md file.

    Args:
        skill_name: Skill name (e.g., "security-testing", "writer")

    Returns:
        Tuple of (skill_content, error_message)
    """
    skill_file = Path(f"skills/{skill_name}/SKILL.md")

    if not skill_file.exists():
        return None, f"WARNING: Skill file not found: skills/{skill_name}/SKILL.md"

    try:
        content = skill_file.read_text(encoding='utf-8')
        return content, None
    except Exception as e:
        return None, f"ERROR reading skill file: {e}"


def load_tool_catalog():
    """
    Load tool catalog for reference.

    Returns:
        Tuple of (catalog_content, error_message)
    """
    catalog_file = Path("library/catalogs/TOOL-CATALOG.md")

    if not catalog_file.exists():
        return None, "WARNING: Tool catalog not found: library/catalogs/TOOL-CATALOG.md"

    try:
        content = catalog_file.read_text(encoding='utf-8')
        return content, None
    except Exception as e:
        return None, f"ERROR reading tool catalog: {e}"


def detect_primary_skill(subagent_type, prompt_text):
    """
    Detect which skill to load for agents with multiple skills.

    For security agent, detect which skill based on prompt keywords:
    - architecture-review: architecture, threat model, design review
    - code-review: code review, security code, vulnerability code
    - dependency-audit: dependency, supply chain, sbom, package
    - threat-intel: cve, threat intel, mitre, attack
    - secure-config: hardening, cis, stig, baseline
    - benchmark-generation: benchmark, compliance script, automation
    - security-advisory: risk assessment, advisory, guidance
    - security-testing: pentest, scan, segmentation (default)

    For advisor agent, detect which skill based on prompt keywords:
    - career: career, resume, interview, job, mentorship
    - osint-research: osint, research, investigate, intelligence
    - qa-review: review, qa, quality, verification

    Args:
        subagent_type: Agent name
        prompt_text: Task prompt text

    Returns:
        Primary skill name (string)
    """
    prompt_lower = prompt_text.lower()

    # Security agent - detect skill from keywords
    if subagent_type == "security":
        # Architecture review
        if any(kw in prompt_lower for kw in ["architecture", "threat model", "design review", "arch-review"]):
            return "architecture-review"
        # Code review
        if any(kw in prompt_lower for kw in ["code review", "code-review", "security code", "source code"]):
            return "code-review"
        # Dependency audit
        if any(kw in prompt_lower for kw in ["dependency", "supply chain", "sbom", "package audit"]):
            return "dependency-audit"
        # Threat intel
        if any(kw in prompt_lower for kw in ["cve", "threat intel", "threat-intel", "mitre", "attack pattern"]):
            return "threat-intel"
        # Secure config
        if any(kw in prompt_lower for kw in ["hardening", "cis benchmark", "stig", "baseline", "secure-config"]):
            return "secure-config"
        # Benchmark generation
        if any(kw in prompt_lower for kw in ["benchmark", "compliance script", "benchmark-gen"]):
            return "benchmark-generation"
        # Security advisory
        if any(kw in prompt_lower for kw in ["risk assessment", "advisory", "security guidance", "risk-assessment"]):
            return "security-advisory"
        # Default to security-testing (pentest, vuln scan, segmentation)
        return "security-testing"

    # Advisor agent - detect skill from keywords
    if subagent_type == "advisor":
        osint_keywords = ["osint", "research", "investigate", "intelligence", "gather information"]
        qa_keywords = ["review", "qa", "quality", "verify", "verification", "check quality"]
        career_keywords = ["career", "resume", "interview", "job", "mentorship", "coaching"]

        # Check OSINT first
        if any(keyword in prompt_lower for keyword in osint_keywords):
            return "osint-research"

        # Then QA
        if any(keyword in prompt_lower for keyword in qa_keywords):
            return "qa-review"

        # Default to career development
        return "career"

    # Single-skill agents (writer, legal)
    return AGENT_SKILL_MAP[subagent_type][0]


def main():
    """Load agent, skill, and tool catalog when Task tool is invoked."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Extract subagent_type from tool parameters
        parameters = data.get("parameters", {})
        subagent_type = parameters.get("subagent_type", "")
        prompt_text = parameters.get("prompt", "")

        if not subagent_type:
            print("WARNING: No subagent_type in Task parameters", file=sys.stderr)
            sys.exit(0)

        # Check if this is a known agent
        if subagent_type not in AGENT_SKILL_MAP:
            print(f"WARNING: Unknown subagent_type: {subagent_type}", file=sys.stderr)
            sys.exit(0)

        # Load agent prompt
        agent_content, agent_error = load_agent_context(subagent_type)
        if agent_error:
            print(agent_error, file=sys.stderr)
            sys.exit(1)

        # Detect primary skill (for multi-skill agents like advisor)
        primary_skill = detect_primary_skill(subagent_type, prompt_text)

        # Load skill context
        skill_content, skill_error = load_skill_context(primary_skill)
        if skill_error:
            print(skill_error, file=sys.stderr)
            # Continue with agent only (don't fail completely)

        # Load tool catalog
        tool_catalog, catalog_error = load_tool_catalog()
        if catalog_error:
            print(catalog_error, file=sys.stderr)
            # Continue without tool catalog (don't fail completely)

        # Detect model escalation from prompt
        recommended_model, trigger, reason = detect_model_escalation(prompt_text)

        # Build output with all loaded context
        output_parts = ["<system-reminder type=\"agent-context\">"]

        # MODEL ROUTING GUIDANCE (injected first for visibility)
        output_parts.append("=== MODEL ROUTING ===")
        output_parts.append(f"Recommended Model: {recommended_model.upper()}")
        output_parts.append(f"Reason: {reason}")
        if trigger:
            output_parts.append(f"Trigger Detected: \"{trigger}\"")
        output_parts.append("")
        output_parts.append("If this recommendation doesn't match the task, you may override.")
        output_parts.append("Reference: library/model-selection-matrix.md")
        output_parts.append("")

        # Agent prompt
        output_parts.append("=== AGENT PROMPT ===")
        output_parts.append(agent_content)
        output_parts.append("")

        # Skill context (if loaded)
        if skill_content:
            output_parts.append(f"=== SKILL CONTEXT: {primary_skill} ===")
            output_parts.append(skill_content)
            output_parts.append("")

        # Tool catalog (if loaded)
        if tool_catalog:
            output_parts.append("=== TOOL CATALOG ===")
            output_parts.append(tool_catalog)
            output_parts.append("")

        output_parts.append("</system-reminder>")

        # Output to stdout (auto-injected into conversation)
        print("\n".join(output_parts))
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR in load-agent-skill-context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
