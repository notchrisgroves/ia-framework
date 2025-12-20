---
type: documentation
title: README Maintenance Rules
classification: public
version: 2.0
last_updated: 2025-12-14
---

# README.md Maintenance Rules - MANDATORY ENFORCEMENT

**Purpose:** Define what README is (and is NOT) to prevent scope creep and maintenance debt

**Status:** ✅ Active Enforcement
**Validation:** Pre-commit hook + manual review
**Framework:** Intelligence Adjacent (IA)

---

## README Constitutional Principles

**README is the FRONT DOOR to the project:**
- First impression for new users
- Quick understanding of what/why/how
- Gateway to deeper documentation
- STABLE, not frequently changing

**README is NOT:**
- ❌ Project management tracker
- ❌ Session progress log
- ❌ Complete manual
- ❌ Architecture deep-dive
- ❌ Development guide
- ❌ Changelog

---

## Rule 0: The Six Sacred Questions

**README must answer EXACTLY these questions (and no more):**

1. **What is this?** (2-3 sentences)
2. **Why should I care?** (5-7 key features)
3. **How do I install it?** (Quick setup steps)
4. **How do I use it?** (1-2 basic examples)
5. **Where can I learn more?** (Links to docs)
6. **How do I contribute?** (Link to CONTRIBUTING.md)

**Everything else belongs elsewhere.**

---

## MANDATORY Rules (ZERO TOLERANCE)

### Rule 1: No Session Tracking

**FORBIDDEN:**
```markdown
❌ ## Current Status
❌ **Phase 1: Foundation (In Progress)** ✅
❌ - [x] Folder structure created
❌ - [ ] Initial commit
```

**WHY:** Session state is temporary, changes frequently, creates git noise

**CORRECT LOCATION:** `sessions/YYYY-MM-DD-project-name.md`

**ALLOWED:**
```markdown
✅ **Status:** Active Development
✅ **Version:** 1.0.0
```

Simple badge/tag only, no detailed progress tracking.

---

### Rule 2: No Dated References

**FORBIDDEN:**
```markdown
❌ See `docs/2025-12-11-FRAMEWORK-REBUILD-PLAN.md`
❌ "As of December 2024..."
❌ "Phase 1 complete (2025-12-13)"
❌ References to "parent framework"
```

**WHY:** Dated docs are session-specific and rot quickly

**CORRECT:**
```markdown
✅ See `docs/architecture.md`
✅ See `CHANGELOG.md` for version history
```

Use permanent doc paths only.

---

### Rule 3: No Hardcoded Counts

**FORBIDDEN:**
```markdown
❌ "4 Specialized Agents"
❌ "18 Skills available"
❌ "27 Slash Commands"
❌ "(each <150 lines)"
```

**WHY:** Counts change constantly, create maintenance debt across files

**CORRECT:**
```markdown
✅ "Specialized Agents - Security, Writer, Advisor, Legal"
✅ "Modular skills with progressive context loading"
✅ "Comprehensive command suite"
```

**See:** `docs/README-MAINTENANCE-DESIGN.md` for approved patterns

---

### Rule 4: No Detailed Architecture

**FORBIDDEN:**
```markdown
❌ Complete architecture principles section (>50 lines)
❌ Detailed hierarchical context loading explanation
❌ Complete folder structure enumeration
❌ Evaluation-driven development methodology
```

**WHY:** Architecture details belong in dedicated docs, not README

**CORRECT:**
```markdown
✅ **Progressive Context Loading** - CLAUDE.md (<250 lines) → skills/*.md (<500 lines) → reference/ (on-demand)

See `docs/architecture.md` for complete details.
```

**High-level summary (2-3 sentences) + link only.**

---

### Rule 5: No Development Guides

**FORBIDDEN:**
```markdown
❌ Complete coding best practices section
❌ Detailed validation tool usage
❌ Pre-commit hook setup instructions
❌ Component creation step-by-step guides
```

**WHY:** Development process belongs in CONTRIBUTING.md

**CORRECT:**
```markdown
✅ ## Contributing

See `CONTRIBUTING.md` for development guidelines, coding standards, and validation tools.
```

**Single link only.**

---

### Rule 6: Folder Structure - High-Level Only

**FORBIDDEN:**
```markdown
❌ Complete directory tree with all subdirectories
❌ Detailed file-by-file enumeration
❌ More than 2 levels of nesting shown
```

**WHY:** Detailed structure changes frequently, creates maintenance burden

**CORRECT:**
```markdown
✅ ia-framework/
   ├── CLAUDE.md          # Navigation layer
   ├── agents/            # Specialized agents
   ├── skills/            # Modular capabilities
   ├── commands/          # Slash commands
   └── docs/              # Documentation
```

**Top 2 levels max.** Link to `docs/directory-structure.md` for details.

---

### Rule 7: No Content Duplication

**FORBIDDEN:**
- Duplicating CLAUDE.md content
- Duplicating docs/ content
- Duplicating agent/skill descriptions
- Copying installation steps from other files

**WHY:** Creates synchronization burden, content drift

**CORRECT:**
- README has unique, concise content
- Links to authoritative sources
- Single source of truth for each topic

---

## Standard README Structure (MANDATORY)

```markdown
# Project Name
Brief tagline

---

## What is This?
2-3 sentences describing the project

---

## Features
- 5-7 key capabilities
- Bullet point format
- Focus on user benefits

---

## Installation
Quick setup steps (copy-paste ready)

---

## Quick Start
1-2 basic usage examples

---

## Documentation
Links to deeper docs with brief descriptions

---

## Contributing
Link to CONTRIBUTING.md

---

## License
License information

---

**Version:** X.Y.Z
**Status:** [Development/Stable/etc]
**Framework:** Intelligence Adjacent (IA)
```

**Total length:** ~150-250 lines maximum

---

## README Update Protocol

**BEFORE editing README.md:**

1. **Read this rules file** (`docs/README-MAINTENANCE-RULES.md`)
2. **Ask these questions:**
   - Is this session-specific? → `sessions/`
   - Is this architecture detail? → `docs/architecture.md`
   - Is this development process? → `CONTRIBUTING.md`
   - Will this change frequently? → Wrong location
   - Does this duplicate existing content? → Link instead
3. **Check validation:** `python tools/validation/validate-readme.py`

**Allowed updates:**
- Installation steps (if setup process changes)
- Quick Start examples (if basic usage changes)
- Feature list (if major capabilities added)
- Documentation links (if docs reorganized)

**Forbidden updates:**
- Session progress tracking
- Work-in-progress status
- Temporary notes
- Detailed process documentation

---

## What Goes Where (Quick Reference)

| Content Type | Location | Why |
|---|---|---|
| Session progress | `sessions/YYYY-MM-DD-*.md` | Temporary state |
| Architecture details | `docs/architecture.md` | Too detailed |
| Development process | `CONTRIBUTING.md` | Developer-focused |
| Coding standards | `CONTRIBUTING.md` | Development rules |
| Directory structure | `docs/directory-structure.md` | Changes frequently |
| Component creation | `library/templates/` | How-to guides |
| Version history | `CHANGELOG.md` | Historical record |
| Dated session docs | `sessions/` or `docs/history/` | Time-specific |

---

## Validation Enforcement

**Pre-commit hook checks:**
```bash
python tools/validation/validate-readme.py --strict
```

**Blocks commits with:**
- Hardcoded counts (`\d+ (skills|agents|commands)`)
- File size references (`\d+GB`, `\d+MB`)
- Progress indicators (`\d+% complete`)
- Phase/status markers (detected via patterns)

**Manual review checklist:**
- [ ] No session tracking
- [ ] No dated references
- [ ] No detailed architecture (>3 sentences)
- [ ] No development guides
- [ ] Folder structure ≤2 levels
- [ ] No content duplication
- [ ] Total length <250 lines

---

## Common Violations & Fixes

### Violation 1: Session Progress Tracking

**Wrong:**
```markdown
## Current Status
**Phase 1: Foundation (In Progress)**
- [x] Folder structure
- [ ] Initial commit
```

**Right:**
```markdown
**Status:** Active Development
**Version:** 1.0.0
```

**Move detailed progress to:** `sessions/2025-12-14-framework-rebuild.md`

---

### Violation 2: Dated Documentation References

**Wrong:**
```markdown
See `docs/2025-12-11-FRAMEWORK-REBUILD-PLAN.md` in parent framework
```

**Right:**
```markdown
See `docs/architecture.md` for framework design
```

**Move dated docs to:** `docs/history/` or `sessions/`

---

### Violation 3: Over-Detailed Architecture

**Wrong:**
```markdown
## Architecture Principles

### Hierarchical Context Loading
[50+ lines of detailed explanation]

### Progressive Disclosure
[30+ lines of methodology]

### Evaluation-Driven Development
[40+ lines of process]
```

**Right:**
```markdown
## Architecture

**Progressive Context Loading** - CLAUDE.md (<250 lines) → skills/*.md (<500 lines) → reference/ (on-demand)

See `docs/architecture.md` for complete design principles.
```

**Move details to:** `docs/architecture.md`

---

### Violation 4: Development Process Documentation

**Wrong:**
```markdown
## Development

### Creating Components
[Complete step-by-step guide]

### Validation Tools
[Detailed tool usage]

### Pre-Commit Hooks
[Setup instructions]
```

**Right:**
```markdown
## Contributing

See `CONTRIBUTING.md` for development guidelines, coding standards, and validation tools.
```

**Move details to:** `CONTRIBUTING.md`

---

## README Anti-Patterns (Hall of Shame)

**These patterns indicate README scope creep:**

1. **"Current Status" sections** → Session tracking
2. **Dated file references** → Will rot
3. **Complete directory trees** → Too detailed
4. **Step-by-step how-tos** → Wrong location
5. **Hardcoded counts** → Maintenance debt
6. **Architecture deep-dives** → Wrong audience
7. **Change logs inline** → Use CHANGELOG.md
8. **Multiple "See also" sections** → Link once

**If you see these, README needs restructuring.**

---

## Enforcement

**AUTOMATED ENFORCEMENT (Active):**

1. **Pre-Commit Hook** (`.git/hooks/pre-commit`):
   - **BLOCKS commits** that violate documentation standards
   - Validates ALL documentation files (README.md, CLAUDE.md, agents/CLAUDE.md, skills/CLAUDE.md, commands/CLAUDE.md)
   - Checks all 7 constitutional rules
   - Exit code 1 = Commit blocked, must fix violations

2. **Documentation Validator** (`tools/validation/validate-documentation.py`):
   - Comprehensive validation of 7 constitutional rules
   - Pattern matching for violations
   - Context-aware (allows examples, version numbers, etc.)
   - Staged-only mode for pre-commit hooks

3. **README Validator** (`tools/validation/validate-readme.py`):
   - Legacy validator (hardcoded counts only)
   - Still runs for backward compatibility
   - Will be replaced by documentation validator

**MANUAL ENFORCEMENT:**
- Content guardian: `library/prompts/content-guardian.md` (writer agent loads)
- Review checklist before commits

**How It Works:**
1. Developer edits documentation file
2. Runs `git commit`
3. Pre-commit hook executes automatically
4. Validator scans staged files for violations
5. **If violations found:** Commit BLOCKED with clear error messages
6. **If clean:** Commit allowed

**Testing Enforcement:**
```bash
# Test validator directly
python tools/validation/validate-documentation.py

# Test on specific file
python tools/validation/validate-documentation.py --file README.md

# Test pre-commit hook (add violation, try to commit)
echo "We have 4 agents" >> CLAUDE.md
git add CLAUDE.md
git commit -m "Test"  # BLOCKED by hook
```

**Bypassing (NOT RECOMMENDED):**
```bash
git commit --no-verify  # Skip all hooks
```

**This is TRUE enforcement - technical barriers, not just documentation.**

---

## Related Documentation

- `docs/README-MAINTENANCE-DESIGN.md` - Why these rules exist
- `library/prompts/content-guardian.md` - Writer agent enforcement
- `tools/validation/validate-readme.py` - Automated validation
- `CONTRIBUTING.md` - Development process (to be created)

---

## Version History

**v2.0 (2025-12-14):**
- Complete rewrite with constitutional rules
- Added "no session tracking" rule
- Added "no dated references" rule
- Clarified scope and boundaries
- Added enforcement mechanisms

**v1.0 (2025-11-23):**
- Initial rules for hardcoded counts only

---

**These rules are MANDATORY and NON-NEGOTIABLE.**

**README is a front door, not a filing cabinet.**

**Status:** ✅ Active Enforcement
**Framework:** Intelligence Adjacent (IA)
