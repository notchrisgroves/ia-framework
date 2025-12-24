# Hero Image Generation

**Automatic generation via FLUX (OpenRouter) with topic-aware styling**

**Primary Method:** Automatic via `tools/image-generation/generate_image.py`
**Fallback:** Manual generation via Grok (legacy workflow below)

---

## Automatic Generation (Recommended)

### Quick Start

```bash
# Generate hero from blog post content analysis
python tools/image-generation/generate_image.py --hero blog/2025-12-19-post-title

# Check API connectivity
python tools/image-generation/generate_image.py --check

# Analyze title for topic detection (no generation)
python tools/image-generation/generate_image.py --analyze "Zero Trust Network Security"
```

### How It Works

1. **Reads draft.md** and extracts title from frontmatter
2. **Analyzes content** for topic detection using keyword matching
3. **Selects appropriate style** from topic-specific pools:
   - **Security:** Red/black alerts, green matrix, command centers
   - **AI/ML:** Purple/blue neural, gold/white clean, collaboration
   - **Infrastructure:** Orange/teal industrial, server rooms
   - **Framework:** Multi-color modular, building blocks
   - **Career:** Professional blue/gold, workstations
4. **Builds varied prompt** with random selection from pools (prevents repetition)
5. **Generates image** via FLUX API (30-120 seconds)
6. **Saves outputs:**
   - `hero.png` - Generated image (~1.7-2MB PNG)
   - `hero.txt` - Prompt used (for regeneration)

### Topic Detection

**Keywords analyzed (see `tools/image-generation/prompts.py`):**

| Topic | Keywords |
|-------|----------|
| Security | hack, pentest, vulnerability, breach, attack, defense, firewall, threat, zero trust |
| AI | model, neural, machine learning, llm, agent, claude, gpt, training, transformer |
| Infrastructure | server, docker, kubernetes, deploy, cloud, vps, container, devops, pipeline |
| Framework | architecture, system, design, pattern, workflow, skill, modular, structure |
| Career | job, resume, interview, professional, career, application, portfolio |

### Style Variety

**Each topic has pools of:**
- **Color palettes** - 5 options per topic (randomly selected)
- **Scene types** - 5 options per topic (randomly selected)
- **Moods** - 5 options per topic (randomly selected)
- **Techniques** - 6 global options (clean vector, cinematic, holographic, etc.)
- **Compositions** - 5 global options (wide, medium, close-up, orbital, diagonal)

**Variety is intentional** - Each generation produces different results to avoid repetitive visuals across posts.

### Manual Override

```bash
# Custom prompt (bypasses topic detection)
python tools/image-generation/generate_image.py "custom prompt here" -o blog/2025-12-19-title/hero.png

# Extended timeout for slow generation
python tools/image-generation/generate_image.py --hero blog/2025-12-19-title --timeout 300
```

### Regeneration

If you don't like the generated image:
1. Check `hero.txt` for the prompt used
2. Run generation again (random pool selection = different result)
3. Or use custom prompt for specific style

---

## Manual Generation (Fallback)

**Use when:** FLUX API unavailable, need specific style not in pools, prefer x.ai output

### Simple One-Liner Prompts

**Format:** `A cyberpunk anime illustration of [main subject/action], in a dark moody technical environment.`

**IMPORTANT:**
- Keep prompts SHORT and HIGH-LEVEL for variety
- Don't over-specify - let Grok interpret creatively
- **DO NOT include dimensions** (1280x720, 16:9, landscape, etc.) - dimensions are fixed

**Examples:**
- "Human collaborating with AI systems. Cyberpunk anime style."
- "Zero-trust network automation. Encrypted connections, no exposed ports. Cyberpunk anime."
- "Human orchestrating AI systems - collaboration not replacement. Determined mood."

### Manual Workflow

1. **Generate prompt** (or use output from `--analyze` flag)
2. **Paste into x.ai** image generation
3. **Download generated image**
4. **Save as:** `blog/{slug}/hero.png`
5. **Create alt text** for Ghost (under 191 chars)

### Alt Text (for Ghost)

**Format:** Condensed description under 191 characters
**Purpose:** Accessibility/SEO (invisible)

**Example:**
```
Human collaborating with AI systems, orchestration not replacement, determined mood, cyberpunk anime style
```

---

## Troubleshooting

**Issue: "OPENROUTER_API_KEY not found"**
- Add to `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`

**Issue: "No allowed providers available"**
- Check OpenRouter dashboard for provider status
- Run `python tools/image-generation/generate_image.py --check`

**Issue: Request timeout**
- FLUX generation takes 30-120 seconds
- Use `--timeout 300` for extended timeout

**Issue: Repetitive styles**
- Working as designed - variety comes from random pool selection
- Run generation again for different result
- Use custom prompt for specific style

---

## Related Files

**Tools:**
- `tools/image-generation/generate_image.py` - Core FLUX generator
- `tools/image-generation/prompts.py` - Topic detection and prompt building

**Commands:**
- `commands/generate-image.md` - Standalone image generation command
- `commands/write.md` - Full blog workflow with visual assets

**Workflows:**
- `workflows/blog-content.md` - Stage 3: VISUAL ASSETS

---

**Version:** 2.0 (Automatic FLUX generation)
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
