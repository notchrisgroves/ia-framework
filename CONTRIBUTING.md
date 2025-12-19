# Contributing to IA Framework

Thank you for your interest in contributing to the Intelligence Adjacent Framework!

## Quick Start

1. Fork the repository
2. Clone your fork
3. Run the installer: `./setup/install.sh` or `.\setup\install.ps1`
4. Make your changes
5. Run validation: `python .claude/tools/validation/framework-health-check.py`
6. Submit a pull request

## Code Standards

### Agent Files (`agents/*.md`)
- Must be **<150 lines** (enforced by pre-commit hook)
- Follow template in `.claude/library/templates/AGENT-TEMPLATE.md`

### Skill Files (`skills/*/SKILL.md`)
- Must be **<500 lines**
- Follow progressive disclosure pattern

### Command Files (`commands/*.md`)
- YAML frontmatter with `name` and `description`
- Include: Quick Start, When to Use, Workflow sections

### Documentation
- No hardcoded counts (use "multiple" or "various")
- Keep paths relative where possible

## Pull Request Checklist

- [ ] Ran `framework-health-check.py`
- [ ] No hardcoded credentials
- [ ] Documentation updated (if needed)
- [ ] Follows existing patterns

## What We're Looking For

**High Priority:**
- Bug fixes
- Documentation improvements
- New generic skills
- Validation improvements

**Medium Priority:**
- New hooks
- Template improvements
- Cross-platform fixes

## Questions?

Open an issue for discussion before starting major work.

---

**Thank you for contributing!**
