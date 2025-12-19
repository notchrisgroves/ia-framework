# Enforcement Methodology - Framework Standard

**Created:** 2025-12-14
**Status:** Baseline standard for all framework enforcement
**Purpose:** Ensure consistent, testable behavior across all framework components

---

## Core Principle

**"If it's important enough to document, it's important enough to enforce automatically."**

Every critical rule MUST have:
1. **Enforcement mechanism** (hook, pre-commit, validation tool)
2. **Test suite** (proves it works)
3. **Clear error messages** (tells user how to fix)
4. **Documentation** (explains why it exists)

**No more:** Documentation that says "you should do X" without enforcement
**Instead:** Hooks/validators that PREVENT wrong behavior automatically

---

## The Pattern (Proven Dec 14, 2025)

### Example: Session Management Enforcement

**Problem:** Agents create duplicate tracking files (STATUS.md, COMPLETE.md, AUDIT.md), violating single source of truth

**Solution Implemented:**

1. **Hook Enforcement** (`hooks/enforce-session-boundary.py`)
   - PostToolUse hook monitors for task completion
   - Suggests /clear + checkpoint workflow
   - Reminds: "Do NOT create duplicate tracking files"
   - Tested: ✅ Works correctly

2. **Pre-Commit Enforcement** (`hooks/pre-commit/prevent-duplicate-tracking.sh`)
   - Blocks commits with STATUS.md, COMPLETE.md, AUDIT.md in root
   - Blocks duplicate session files (same project, same date)
   - Warns if >5 session files for same project
   - Tested: ✅ Blocks violations, allows valid files

3. **Template Enforcement** (`library/templates/SESSION-STATE-TEMPLATE.md`)
   - EXPLICIT "HOW TO RESUME" instructions at top
   - Master Plan Reference section (what files to load)
   - Enforcement Reminders section (what NOT to do)
   - Tested: ✅ Clear, unambiguous instructions

4. **Documentation** (`hooks/README.md`)
   - Explains all hooks and what they enforce
   - Provides testing examples
   - References best practices

**Result:** Impossible to violate the rule without ignoring explicit errors

---

## Enforcement Hierarchy

### Level 1: Prevention (Strongest)
**Pre-commit hooks** - Block violations before they enter git history
- Example: `prevent-duplicate-tracking.sh`
- Use for: File naming, structure violations, credential leaks

### Level 2: Detection (Strong)
**PostToolUse hooks** - Catch violations immediately after they happen
- Example: `enforce-session-boundary.py`
- Use for: Workflow violations, quality gates, task completion

### Level 3: Guidance (Moderate)
**Templates with explicit instructions** - Tell user exactly what to do
- Example: SESSION-STATE-TEMPLATE.md with "HOW TO RESUME" section
- Use for: Complex workflows, multi-step processes

### Level 4: Documentation (Weakest)
**README files and docs** - Explain the "why" behind rules
- Example: `hooks/README.md`
- Use for: Context, rationale, references

**Never rely on Level 4 alone!** Always combine with Levels 1-3.

---

## Testing Requirements

**ALL enforcement mechanisms MUST be tested before deployment:**

```bash
# 1. Create test case that violates rule
# 2. Run enforcement mechanism
# 3. Verify it blocks/warns/guides correctly
# 4. Clean up test artifacts
```

**Example test suite:**
```bash
# Test 1: Hook detects completed tasks
echo '{"name":"TodoWrite","input":{"todos":[...]}}' | python hooks/enforce-session-boundary.py

# Test 2: Pre-commit blocks duplicate files
echo "# Test" > STATUS.md
git add STATUS.md
bash hooks/pre-commit/prevent-duplicate-tracking.sh
# Expected: Exit 1 (blocked)

# Test 3: Pre-commit allows valid files
echo "# Session" > sessions/2025-12-14-test.md
git add sessions/2025-12-14-test.md
bash hooks/pre-commit/prevent-duplicate-tracking.sh
# Expected: Exit 0 (allowed)
```

**Document test results in implementation notes.**

---

## Where to Apply This Pattern

### ✅ Already Implemented
- Session management (duplicate file prevention)
- Command frontmatter (official fields only)
- README validation (no hardcoded counts)
- **Hardcoded count prevention (ALL documentation files)** - 2025-12-17
  - Hook: `hooks/pre-commit/prevent-hardcoded-counts.sh`
  - Tool: `tools/validation/detect-hardcoded-counts.py`
  - Blocks: Component counts, category counts, ratio counts, total counts
  - Scope: All .md/.yml/.yaml files (excluding sessions/, plans/, output/)
  - Tested: ✅ Detects violations, skips false positives (examples, docs)

### 🔄 Needs Implementation

**1. Skills Decision Tree Validation**
- Problem: Skills have complex decision trees, need consistent routing
- Enforcement needed:
  - Pre-commit: Validate decision tree syntax
  - PostToolUse: Verify correct skill was invoked for task type
  - Evals: Test that decision trees route correctly

**2. Agent Format Validation**
- Problem: Agents must stay <150 lines
- Enforcement needed:
  - Pre-commit: Block agents >150 lines (already exists?)
  - Template: Explicit structure requirements
  - Evals: Test agent loads correct skill context

**3. File Location Standards**
- Problem: Files created in wrong locations (root vs docs/ vs sessions/)
- Enforcement needed:
  - PostToolUse: Detect file writes, suggest correct location
  - Pre-commit: Warn if files in wrong directory
  - Template: FILE-LOCATION-STANDARDS.md loaded on-demand

**4. Command Parameter Validation**
- Problem: Slash commands need specific inputs
- Enforcement needed:
  - UserPromptSubmit: Validate command syntax before execution
  - Template: Show required vs optional parameters
  - Evals: Test commands with various inputs

**5. Tool Discovery Protocol**
- Problem: Tools get duplicated instead of discovered
- Enforcement needed:
  - PreToolUse: Check TOOL-CATALOG.md before creating tools
  - PostToolUse: Warn if duplicate tool created
  - Evals: Test tool discovery workflow

---

## Claude Code 2025 Features to Use

Based on research of official 2025 features:

### **1. Evaluations (Official Testing Framework)**
**What:** Systematic testing of agent/skill behavior
**Use for:**
- Testing decision tree routing in skills
- Validating agent context loading
- Ensuring commands work with various inputs
**Reference:** [Using the Evaluation Tool](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)

### **2. Quality Gates (Automated Validation)**
**What:** /workflow:ship validates gates before PR creation
**Use for:**
- Running formatters, lints, unit tests automatically
- Enforcing standards consistently
- Preventing problems before production
**Reference:** [Quality Gates in Claude Skills](https://claude-plugins.dev/skills/@phrazzld/claude-config/quality-gates)

### **3. Memory Tool (Persistent Context)**
**What:** Claude remembers project details across sessions
**Use for:**
- Persistent context without manual session files?
- Automatic recall of decisions and tasks
**Note:** May replace our manual SESSION-STATE.md files
**Reference:** [Enabling Autonomous Work](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)

### **4. Checkpoints (Auto-Save State)**
**What:** Automatically saves code + conversation state before changes
**Use for:**
- /rewind to previous state (code + context)
- May replace manual session checkpointing
**Reference:** [Claude Code Checkpoints](https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/)

### **5. Background Tasks (Long-Running Processes)**
**What:** Keep dev servers, tests running without blocking
**Use for:**
- Running test suites in background
- Continuous validation during development
**Reference:** [Claude Code 2.0 Features](https://skywork.ai/blog/claude-code-2-0-checkpoints-subagents-autonomous-coding/)

---

## Action Items

### Immediate (This Session)
- [x] Document enforcement methodology (this file)
- [ ] Investigate if Memory Tool + Checkpoints replace SESSION-STATE.md
- [ ] Test built-in /rewind vs our session management

### Next Session
- [ ] Create evaluation suite for skills decision trees
- [ ] Implement quality gates for framework validation
- [ ] Set up background task for continuous testing
- [ ] Migrate to built-in Memory/Checkpoints if better than SESSION-STATE.md

### Long Term
- [ ] Apply enforcement pattern to all 5 identified areas
- [ ] Create eval suites for each major component
- [ ] Document testing standards
- [ ] Train on using quality gates consistently

---

## Critical Note

**THIS METHODOLOGY MUST BE APPLIED TO:**
- Skills with detailed decision workflows
- Agent context loading
- Command parameter handling
- File location enforcement
- Tool discovery protocol
- ANY new component added to framework

**Testing is NOT optional.** Every enforcement mechanism MUST be tested before considering it complete.

---

## References

**Claude Code Official:**
- [Evaluation Tool](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)
- [Agent Skills Guide](https://devtoolhub.com/agent-skills-guide-claude/)
- [Quality Gates](https://claude-plugins.dev/skills/@phrazzld/claude-config/quality-gates)

**Best Practices:**
- [Eval-Driven Development](https://fireworks.ai/blog/eval-driven-development-with-claude-code)
- [Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks)
- [Autonomous Workflows](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)

---

**Last Updated:** 2025-12-14
**Framework:** Intelligence Adjacent (IA) v4.0
**Status:** Baseline standard for all future enforcement
