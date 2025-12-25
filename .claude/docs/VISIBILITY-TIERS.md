# Visibility Tier Classification System

**Purpose:** Automated classification of blog post visibility based on content type.

---

## Tier Definitions

| Tier | Ghost Setting | Who Sees It | Content Focus | Cost |
|------|---------------|-------------|---------------|------|
| `public` | Public | Everyone | Concepts, analysis, announcements | Free |
| `members` | Members | Lurker (free signup) | Methodology guides, infrastructure setup | Free |
| `paid` | Paid-members | Contributor + Fellow | Implementation deep dives, advanced tutorials | $5-20/mo |

---

## Membership Tiers (Ghost Portal)

| Tier | Cost | Benefits |
|------|------|----------|
| **Lurker** | Free | Public + methodology guides, infrastructure setup, security foundations |
| **Contributor** | $5/month | Everything in Lurker + implementation guides, deep dives, advanced workflows, priority email, early access |
| **Fellow** | $20/month | Everything in Contributor + direct implementation support, priority feature requests, influence content direction |

**Content Access:**
- **Public content** → Everyone
- **Members content** → Lurker, Contributor, Fellow
- **Paid content** → Contributor, Fellow only

**Value Ladder:**
- **Public**: Understand what the framework does and why
- **Lurker**: Learn how to use the framework effectively
- **Contributor**: Learn how to build, customize, and extend it
- **Fellow**: Get direct support and influence development

---

## Classification Decision Tree

```
IF title contains ["Deep Dive", "Building", "Creating", "Implementing",
                   "Extending", "Custom", "Internals", "Tutorial"]
   OR category == "implementation"
   → visibility: "paid"

ELSE IF title contains ["Guide", "Setup", "Hardening", "Methodology",
                        "Foundations", "Lab", "Professional", "Infrastructure"]
   OR category in ["security", "infrastructure"]
   → visibility: "members"

ELSE IF title contains ["Architecture", "Overview", "Introduction", "Analysis",
                        "Comparison", "Announcement", "Reality Check", "Companion"]
   OR category in ["commentary", "announcement", "framework", "tools"]
   → visibility: "public"

ELSE → visibility: "members" (safe default)
```

---

## Content Examples by Tier

### PUBLIC (What & Why)

- "The Complete IA Framework Architecture" - architecture overview
- "MCP Protocol: One Year Later" - industry analysis
- "Job Market 2025: Reality Check" - commentary
- "VPS Provider Comparison" - analysis/comparison
- "Obsidian as a Claude Code Companion" - tool introduction

### MEMBERS (How to Use)

- "VPS Hardening for Security Professionals" - methodology guide
- "Zero-Trust Security Lab Setup" - infrastructure setup
- "GRC Foundations" - methodology foundations
- "Professional Security Infrastructure" - infrastructure guide

### PAID (How to Build/Extend)

- "Skills System Deep Dive" - implementation internals
- "Building Your First Custom Skill" - implementation tutorial
- "Extending the Pentest Workflow" - customization guide
- "Creating a New Agent from Scratch" - implementation tutorial

---

## Override Mechanism

When a post doesn't fit the classification rules, use an override:

```yaml
---
title: "Skills System Deep Dive"
visibility: "public"
visibility_override: true
visibility_reason: "Launch promotion - free access for framework introduction"
---
```

**Valid override reasons:**
- Launch promotion / temporary free access
- Foundational content needed for paid tutorials
- Community request / accessibility consideration
- Cross-promotion with external publication

**Override requires:**
1. `visibility_override: true` in frontmatter
2. `visibility_reason: "..."` explaining the exception
3. Both fields present or QA will block

---

## Enforcement Points

| Phase | Check | Action |
|-------|-------|--------|
| DRAFT | Claude applies classification | Sets visibility in frontmatter |
| QA | Validate visibility matches rules | WARN if mismatch, require override |
| PUBLISH | Final verification | Block if mismatch without override |

---

## Grandfathering Existing Posts

Posts published before this system was implemented are **grandfathered**:

- Existing "Deep Dive" posts remain `public` (original classification)
- No retroactive changes required
- New posts follow classification rules

**Grandfathered posts (published as public, would now be paid):**
- 2025-12-20: Skills System Deep Dive
- 2025-12-20: Slash Commands Deep Dive
- 2025-12-20: Agent Architecture Deep Dive
- 2025-12-20: VPS Server Tools Deep Dive

---

## Ghost CMS Mapping

| Visibility | Ghost Setting | Access |
|------------|---------------|--------|
| `public` | Public | Everyone |
| `members` | Members only | Free + Paid subscribers |
| `paid` | Paid-members only | Paid subscribers only |

---

## Related Documentation

- `commands/write/prompts/02-DRAFT.md` - Classification rules in drafting
- `commands/write/prompts/03-QA.md` - Validation checks
- `skills/writer/SKILL.md` - Writer skill reference

---

**Version:** 1.0.0
**Last Updated:** 2025-12-24
**Framework:** Intelligence Adjacent (IA)
