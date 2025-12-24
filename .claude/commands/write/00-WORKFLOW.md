# Content Workflow - Prompt Chain Orchestrator

**5 phases with mandatory gates. Each phase MUST complete before the next.**

---

## Phase Overview

```
Phase 1: RESEARCH → Gate: sources.txt exists with 10+ sources
Phase 2: DRAFT → Gate: draft.md exists with valid frontmatter
Phase 3: QA → Gate: rating = 5/5 in qa-review.json (may take multiple iterations)
Phase 4: VISUALS → Gate: hero.png exists
Phase 5: PUBLISH → Gate: Ghost URL returned + tweet.txt exists
```

---

## Execution Flow

### BEFORE Starting Any Phase

1. **Identify current phase** by checking blog/YYYY-MM-DD-{slug}/ folder contents
2. **Load the appropriate prompt** from `commands/write/prompts/`
3. **Execute ONLY that phase** - do not skip ahead
4. **Show checkpoint output** to user after completion
5. **Verify gate** before proceeding to next phase

---

## Phase Detection Logic

```
IF sources.txt NOT EXISTS → Load 01-RESEARCH.md
ELSE IF draft.md NOT EXISTS → Load 02-DRAFT.md
ELSE IF qa-review.json NOT EXISTS OR rating < 5 → Load 03-QA.md
ELSE IF hero.png NOT EXISTS → Load 04-VISUALS.md
ELSE IF Ghost NOT published OR tweet.txt NOT EXISTS → Load 05-PUBLISH.md
ELSE → Workflow complete
```

---

## Prompt Files

| Phase | File | Gate |
|-------|------|------|
| 1 | `prompts/01-RESEARCH.md` | sources.txt with 10+ entries |
| 2 | `prompts/02-DRAFT.md` | draft.md with valid frontmatter |
| 3 | `prompts/03-QA.md` | qa-review.json with rating = 5/5 |
| 4 | `prompts/04-VISUALS.md` | hero.png exists |
| 5 | `prompts/05-PUBLISH.md` | Ghost URL + tweet.txt |

---

## Output Directory

**ALL files go to:** `blog/YYYY-MM-DD-{slug}/`

**Files stay in place** - never move between folders.

---

## Metadata Tracking

Each phase updates `metadata.json`:

```json
{
  "slug": "YYYY-MM-DD-title",
  "phase": "research|draft|qa|visuals|published",
  "created": "2025-12-20T...",
  "updated": "2025-12-20T...",
  "sources_count": 12,
  "word_count": 1847,
  "qa_rating": 4.5,
  "ghost": {
    "id": "abc123",
    "url": "https://...",
    "status": "published"
  }
}
```

---

## Agent Routing

```
Task(subagent_type="writer", prompt="Execute /write Phase X...")
```

**Agent loads:**
1. `agents/writer.md`
2. `skills/writer/SKILL.md`
3. Phase-specific prompt from `commands/write/prompts/`

---

## Critical Rules

1. **NEVER skip phases** - Execute in order 1→2→3→4→5
2. **NEVER proceed without gate verification** - Each phase has a hard gate
3. **ALWAYS show checkpoint output** - User must see phase completion
4. **Files stay in blog/YYYY-MM-DD-{slug}/** - Never move
5. **metadata.json tracks progress** - Update after each phase

---

**Framework:** Intelligence Adjacent v1.0.0
