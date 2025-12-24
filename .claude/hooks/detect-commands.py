#!/usr/bin/env python3
"""
UserPromptSubmit Hook: Detect slash commands and suggest based on keywords

Trigger: UserPromptSubmit (every user message)
Purpose: Detect slash commands, suggest relevant commands based on keywords
Output: Slash command suggestions wrapped in <system-reminder> tags
"""
import json
import sys
import io
from pathlib import Path

# Ensure stdout uses UTF-8 encoding (Windows fix)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Keyword detection map (lowercase for case-insensitive matching)
KEYWORD_MAP = {
    "/job-analysis": [
        "job posting", "job description", "apply for", "career opportunity",
        "job application", "position", "hiring"
    ],
    "/resume-review": [
        "resume", "cv", "curriculum vitae", "optimize resume", "resume feedback"
    ],
    "/interview-prep": [
        "interview", "interview prep", "technical interview", "interview preparation"
    ],
    "/pentest": [
        "pentest", "penetration test", "penetration testing", "security test",
        "ethical hacking", "hack", "exploit"
    ],
    "/vuln-scan": [
        "vulnerability scan", "automated scan", "security scan", "vuln scan"
    ],
    "/write": [
        "blog post", "article", "write about", "publish", "blog content",
        "write a post", "create content"
    ],
    "/newsletter": [
        "newsletter", "weekly digest", "content digest", "email newsletter"
    ],
    "/risk-assessment": [
        "risk assessment", "compliance review", "security audit", "risk analysis"
    ],
    "/code-review": [
        "code review", "security review", "analyze code", "review code",
        "code analysis", "security code review"
    ],
    "/arch-review": [
        "architecture review", "threat model", "design security",
        "architecture security", "system design"
    ],
    "/tech-docs": [
        "documentation", "technical docs", "write docs", "create documentation"
    ],
}

# Command descriptions for suggestions
COMMAND_DESCRIPTIONS = {
    "/job-analysis": "Job posting analysis and application strategy",
    "/resume-review": "Comprehensive resume review and optimization",
    "/interview-prep": "Interview preparation for scheduled interviews",
    "/pentest": "Security testing with Director/Mentor/Demo modes",
    "/vuln-scan": "Automated vulnerability scanning",
    "/write": "Content creation (blog, docs, reports) with prompt-chained workflow",
    "/newsletter": "Automated weekly digest generation",
    "/risk-assessment": "Formal cybersecurity risk assessment",
    "/code-review": "Security-focused code review",
    "/arch-review": "Architecture security review with threat modeling",
    "/tech-docs": "Technical documentation with Diátaxis framework",
}


def detect_keywords(prompt_text):
    """
    Detect keywords in user prompt and return matching commands.

    Args:
        prompt_text: User's prompt text (string)

    Returns:
        List of matching command names (e.g., ["/pentest", "/vuln-scan"])
    """
    matches = []
    prompt_lower = prompt_text.lower()

    for command, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                if command not in matches:
                    matches.append(command)
                break

    return matches


def main():
    """Detect slash commands or suggest based on keywords."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Check if this is already a slash command
        if prompt.strip().startswith("/"):
            # User already typed a slash command - no suggestion needed
            sys.exit(0)

        # Detect keywords in prompt
        matching_commands = detect_keywords(prompt)

        if not matching_commands:
            # No matches - exit silently
            sys.exit(0)

        # Build suggestion output
        if len(matching_commands) == 1:
            command = matching_commands[0]
            description = COMMAND_DESCRIPTIONS.get(command, "No description available")
            output = f"""<system-reminder>
💡 Detected potential slash command based on keywords in user's message.

Suggested command: {command}
Description: {description}

To use: Type {command} to begin guided workflow
</system-reminder>"""
        else:
            # Multiple matches
            suggestions = []
            for cmd in matching_commands:
                desc = COMMAND_DESCRIPTIONS.get(cmd, "No description")
                suggestions.append(f"  • {cmd} - {desc}")

            output = f"""<system-reminder>
💡 Detected multiple potential slash commands based on keywords.

Suggested commands:
{chr(10).join(suggestions)}

To use: Type the command name to begin guided workflow
</system-reminder>"""

        print(output)
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Fail gracefully - don't block user prompt
        print(f"WARNING: Hook JSON parse error: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Fail gracefully - don't block user prompt
        print(f"WARNING: Hook error in detect-commands: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
