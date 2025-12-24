# Phase 4: VISUALS

## 🚨 CRITICAL RULES

**Before starting this phase:**
1. **Verify Phase 3 Complete** - `qa-review.json` MUST exist with rating = 5/5
2. **Read draft.md** - Extract title for image generation
3. **Create hero-prompt.txt** - Write a CUSTOM prompt matching brand style (see Step 1b)

**You MUST:**
- **CREATE hero-prompt.txt FIRST** - With custom prompt matching brand style
- **EXECUTE the Python script** - This GENERATES a real PNG image file
- Use the EXACT Bash command specified below
- Wait for generation to complete (30-120 seconds)
- Verify `hero.png` exists in the blog folder after execution

**NEVER:**
- ❌ Just save a prompt file - you must GENERATE the actual image
- ❌ Use TypeScript image-prompt tool
- ❌ Skip hero image generation
- ❌ Proceed without verifying hero.png exists (check file size > 0)
- ❌ Use placeholder images
- ❌ Assume the image exists - RUN THE COMMAND
- ❌ Skip hero-prompt.txt and rely on auto-generated prompts

---

## Required Output Files

You MUST create in `blog/YYYY-MM-DD-{slug}/`:

- [ ] `hero.png` - Generated hero image via FLUX
- [ ] `hero.txt` - Prompt used (for regeneration)
- [ ] `metadata.json` - Updated with phase: "visuals", hero_generated: true

---

## Step 1: Verify QA Gate Passed

**Check qa-review.json:**
```json
{
  "ratings": {
    "overall": 5  // MUST be exactly 5/5
  },
  "gate_passed": true
}
```

**If rating < 5: STOP. Return to Phase 3. Iterate until 5/5.**

---

## Step 1b: Create hero-prompt.txt (REQUIRED)

🚨 **DO NOT SKIP THIS STEP** - Auto-generated prompts don't match brand style.

**Write a custom hero-prompt.txt in `blog/YYYY-MM-DD-{slug}/` with:**

### Brand Style Requirements (MANDATORY)

Every hero image MUST include these style elements:
- **"90s anime style with detailed linework"** - The core art style
- **"cyberpunk aesthetic"** - Neon colors, tech atmosphere
- **"Deep purple and electric blue"** (or similar neon color palette)
- **"Dramatic lighting"** with atmospheric fog

### Prompt Structure

```
[Specific visual scene description relating to the post topic]
[Color palette - neon colors like purple/blue/cyan/amber]
Cyberpunk aesthetic, 90s anime style with detailed linework.
Dramatic lighting [with atmospheric fog / illuminating shadows / etc.].
```

### Example Prompts (Reference Published Posts)

**IA Framework Architecture:**
```
A vast hierarchical library floating in a neon void - three distinct tiers of glowing knowledge. The top tier is a compact navigation console, the middle tier shows specialized agent personas in ornate frames, the bottom tier contains massive skill repositories pulsing with methodologies. A lone figure stands at the navigation console, pulling down only the context needed while the rest remains dormant. Deep purple and electric blue, cyberpunk aesthetic, 90s anime style with detailed linework. Dramatic lighting from the glowing tiers illuminating atmospheric fog.
```

**Agent Architecture:**
```
A vintage telephone switchboard operator in a cyberpunk setting, but instead of phone cables they're routing glowing data streams to specialized AI agents represented as distinct personas - a security guard with shields, a writer with flowing manuscripts, an advisor with star charts, a legal figure with balanced scales. The switchboard itself is a thin elegant console, emphasizing routing over complexity. Neon purple and teal, dramatic shadows, 90s anime style with detailed character expressions.
```

**Skills System:**
```
A vast library of floating skill modules, each one a glowing hexagonal container holding specialized knowledge - security shields, writing quills, legal scales, career compasses. They orbit around a central figure who pulls down only the modules needed, leaving the rest dormant in the darkness. Progressive disclosure visualized as layers of light revealing deeper expertise. Cyberpunk meets ancient library aesthetic, warm amber and cool cyan contrasts. 90s anime style.
```

### Tips for Good Prompts

- **Be specific** - Describe an actual scene, not just "security operations"
- **Include a figure** - A person interacting with the environment adds depth
- **Match the topic** - Visualize the post's core concept metaphorically
- **Use contrasts** - Light/dark, warm/cool colors, complexity/simplicity

---

## Step 2: Generate Hero Image (FLUX via OpenRouter)

**EXACT COMMAND - You MUST execute this via Bash tool:**
```bash
python tools/image-generation/generate_image.py --hero blog/YYYY-MM-DD-{slug}
```

🚨 **THIS IS A BASH COMMAND - RUN IT. DO NOT JUST WRITE IT DOWN.**

**What the script does when you run it:**
1. Reads draft.md and extracts title from frontmatter
2. Analyzes content for topic detection (security, AI, infrastructure, etc.)
3. Selects appropriate style from topic-specific pools:
   - **Security:** Red/black alerts, green matrix, command centers
   - **AI/ML:** Purple/blue neural, gold/white clean, collaboration
   - **Infrastructure:** Orange/teal industrial, server rooms
   - **Framework:** Multi-color modular, building blocks
4. Calls FLUX API via OpenRouter (30-120 seconds wait time)
5. Saves `hero.png` (the actual image) and `hero.txt` (prompt used)

**Output files created by the script:**
- `blog/YYYY-MM-DD-{slug}/hero.png` - **THE ACTUAL PNG IMAGE** (~1.7-2MB)
- `blog/YYYY-MM-DD-{slug}/hero.txt` - Prompt used for regeneration

---

## Step 3: Verify Image Generated

**Check file exists:**
```bash
ls -la blog/YYYY-MM-DD-{slug}/hero.png
```

**If generation failed:**
1. Check API connectivity: `python tools/image-generation/generate_image.py --check`
2. Retry generation
3. If still fails, use manual override with custom prompt

**Manual override (only if automatic fails):**
```bash
python tools/image-generation/generate_image.py "custom prompt describing topic" -o blog/YYYY-MM-DD-{slug}/hero.png
```

---

## Step 4: Export Diagrams (If Applicable)

**Only if `diagrams/` folder exists with .mmd files:**
```bash
python skills/diagram-generation/scripts/export-diagram.py blog/YYYY-MM-DD-{slug}/diagrams/*.mmd
```

**Output:** `diagrams/*.png` files

---

## ⛔ GATE (MANDATORY)

**Cannot proceed to Phase 5 (PUBLISH) unless:**
- [ ] `hero.png` exists and is > 0 bytes
- [ ] `hero.txt` exists with prompt used
- [ ] `metadata.json` updated with hero_generated: true

🚨 **If hero.png missing:** Retry generation. Do not proceed.

---

## Checkpoint Output

**Show user:**
```
✅ PHASE 4 COMPLETE: Visual Assets
Hero image: blog/YYYY-MM-DD-{slug}/hero.png
Topic detected: [security|ai|infrastructure|framework]
Prompt saved: hero.txt
Diagrams exported: [X] (if applicable)

Gate: PASSED ✓
→ Ready for Phase 5: PUBLISH
```

**If generation failed:**
```
⛔ PHASE 4 BLOCKED: Visual Assets
Error: [error message]
Retrying with: [command]
```

---

**Next Phase:** Load `prompts/05-PUBLISH.md`
