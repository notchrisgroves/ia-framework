# Framework Tool Catalog

**Auto-generated tool inventory for agent awareness**

**Last Updated:** 2025-12-17

**Purpose:** This catalog provides agents with awareness of ALL available tools across the framework - both framework-core utilities and skill-specific tools.

**Usage:**
- Agents read this during startup for tool awareness
- Reference tools using relative paths: `tools/...` or `skills/*/scripts/...`
- Skill-specific scripts are automatically loaded with skill context

---

## 1. Framework-Core Tools (Available to ALL Agents)

These tools are in `tools/` and available to ALL agents regardless of skill context.

### Multi-Model AI Integration

**openrouter/**: Dynamic model fetching and multi-model orchestration
- Path: `tools/openrouter/`
- Files: `fetch-models.ts`, `README.md`
- Purpose: Dynamic model list fetching, OpenRouter API integration
- Models supported: Haiku (routing/templates), Sonnet (complex), Grok (verification), Perplexity (research)

**context7/**: Library documentation API integration
- Path: `tools/context7/`
- Files: `context7.ts`, `README.md`
- Purpose: Fetch up-to-date library documentation for Python, JavaScript, TypeScript packages
- Use cases: Import statement generation, API usage examples, version-specific docs

---

## 2. Skill-Specific Scripts (Loaded with Skill Context)

These scripts are colocated with their respective skills in `skills/{skill}/scripts/`.

**Agent Awareness:**
- When an agent loads a skill (via SKILL.md), it gains context about that skill's scripts
- Scripts are referenced using skill-relative paths
- Better discoverability and logical cohesion

### security-testing Skill

**Description:** Unified security testing with 3 modes - penetration testing (exploitation), vulnerability scanning (detection only), and network segmentation testing

- **hackerone**: `skills/security-testing/scripts/hackerone/` (HackerOne API integration)
- **security**: `skills/security-testing/scripts/security/` (Audit logging, remediation tools)

### writer Skill

**Description:** Content creation for Intelligence Adjacent - blog posts, newsletters, documentation, and social media

- **blog-workflow.ts**: `skills/writer/scripts/blog-workflow.ts` (Blog post management - init, publish, draft, archive, tweet, image-prompt)
- **ghost-admin.ts**: `skills/writer/scripts/ghost-admin.ts` (Ghost Admin API integration - posts, pages, members)
- **publish-weekly-digest.ts**: `skills/writer/scripts/publish-weekly-digest.ts` (Automated newsletter generation and publishing)

### infrastructure-ops Skill

**Description:** VPS management, Docker networking, zero-trust access (Twingate), security hardening, and infrastructure automation

- **git**: `skills/infrastructure-ops/scripts/git/` (Git automation utilities)
- **infrastructure**: `skills/infrastructure-ops/scripts/infrastructure/` (VPS deployment tools)

---

## 3. VPS Servers (Remote Security Tools via Docker)

These servers are deployed on VPS infrastructure and accessed via SSH + Docker exec. They follow the on-demand container model.

### Playwright Server

**Description:** Headless browser automation for security assessments - screenshot capture, PDF generation, HAR recording, and authenticated browsing

- **playwright.py**: `servers/playwright/wrappers/playwright.py`
  - `screenshot()` - Capture screenshot (full page, element, or viewport)
  - `pdf()` - Generate PDF of page (Chromium only)
  - `har()` - Record HAR (HTTP Archive) for traffic analysis
  - `batch_screenshot()` - Batch capture from URL list

**Use Cases:**
- Evidence collection during penetration tests
- Document vulnerable configurations
- Capture before/after exploitation states
- HAR recording for API discovery
- Authenticated browsing with cookies/basic auth

**Deployment Status:** Ready for deployment (infrastructure-ops agent will deploy)

---

## 4. Tool Organization Standard

**Framework-core tools:** `tools/` (general utilities for ALL agents)
**Skill-specific scripts:** `skills/{skill}/scripts/` (colocated with skills)
**VPS wrappers:** `servers/` (remote security tools via Docker - not yet migrated)

**When to create a new tool:**
1. Check this catalog first - tool may already exist
2. Determine scope: Framework-wide (tools/) or Skill-specific (skills/*/scripts/)
3. Follow template standards in `library/templates/`
4. Update this catalog after creation

---

## 5. Tool Discovery Protocol

**BEFORE delegating to ANY agent OR creating ANY new tool:**

1. **Check Tool Catalog** - Read this file for existing tools
2. **Search Skill Scripts** - Use Glob for `skills/*/scripts/**`
3. **Verify Tool Exists** - Read tool file to confirm it does what's needed
4. **Decision:**
   - Tool exists + you can use it → **Use it directly (don't delegate)**
   - Tool exists + agent-specific context needed → Delegate with tool reference
   - Tool missing → Create new tool OR delegate if agent should own it

**Violations:**
- ❌ Delegating without checking tool availability first
- ❌ Creating duplicate tools
- ❌ Asking "should I create a script?" when one already exists

---

## 6. Templates

**Tool creation templates available:**
- `library/templates/TOOL-TEMPLATE-PYTHON.py` - Python tool template
- `library/templates/TOOL-TEMPLATE-TYPESCRIPT.ts` - TypeScript tool template

**See:** `docs/CREDENTIAL-HANDLING-ENFORCEMENT.md` for credential management standards

---

**Version:** 1.1 (Added writer skill tools)
**Last Updated:** 2025-12-17
**Framework:** Intelligence Adjacent (IA)
