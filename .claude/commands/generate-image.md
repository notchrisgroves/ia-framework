---
name: generate-image
description: Generate images via FLUX.2 Max for blog posts, concepts, and visualizations
---

# /generate-image - AI Image Generation

Generate images using Black Forest Labs FLUX models via OpenRouter API with dynamic model selection and content-aware styling.

**Tool:** `tools/image-generation/generate_image.py`
**API:** OpenRouter (FLUX model dynamically selected via `fetch_models.py`)
**Output:** PNG images with varied styles based on content analysis

---

## Quick Start

```bash
# Generate image with prompt
/generate-image "cyberpunk security analyst at terminal" -o output/images/analyst.png

# Check API and model availability
/generate-image --check
```

**Note:** For blog post hero images, use the blog workflow (Stage 3: VISUAL ASSETS) which automatically generates topic-aware heroes from draft content.

---

## When to Use

**Use /generate-image when:**
- Generating standalone concept visualizations
- Creating one-off AI-generated images
- Testing prompts before blog workflow

**Don't use when:**
- Creating blog post hero images → use blog workflow (auto-generates from content)
- Need technical diagrams (flowcharts, sequences) → use diagram-generation skill
- Need screenshots or real UI captures
- Need precise architectural diagrams → use Mermaid

---

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `prompt` | Text prompt for generation | `"zero trust architecture"` |
| `-o, --output` | Output file path (required) | `-o output/images/image.png` |
| `--check` | Verify API connectivity | |
| `--timeout` | Request timeout seconds | `--timeout 300` |

**Internal options (used by blog workflow):**
| Option | Description |
|--------|-------------|
| `--hero SLUG` | Generate hero for blog post (analyzes content) |
| `--analyze TITLE` | Analyze title for topic detection (no generation) |

---

## Topic-Aware Styling

The generator analyzes content to determine appropriate visual style:

| Topic | Color Palettes | Scene Types |
|-------|---------------|-------------|
| **Security** | Red/black, green matrix, amber alerts | Command centers, terminals, shields |
| **AI/ML** | Purple/blue neural, gold/white clean | Neural networks, data flows, collaboration |
| **Infrastructure** | Orange/teal industrial, status lights | Server rooms, containers, networks |
| **Framework** | Multi-color modular, blue/gold | Building blocks, orbital systems |
| **Career** | Professional blue/gold, warm amber | Workstations, portfolios, achievements |

**Variety is intentional** - each generation selects randomly from appropriate pools to avoid repetitive visuals across posts.

---

## Blog Workflow Integration

Hero images are automatically generated during the blog publishing workflow:

```
RESEARCH → WRITING → VISUAL ASSETS → QA_REVIEW → PUBLISHING
                          ↓
              ┌──────────────────────┐
              │  1. Generate hero    │ (FLUX via OpenRouter)
              │  2. Export diagrams  │ (Mermaid if .mmd files exist)
              │  3. Process inline   │ (if markers present)
              └──────────────────────┘
```

**Automatic on publish:** If `hero.png` doesn't exist when publishing, it's generated automatically from draft content analysis.

**See:** `skills/writer/workflows/blog-content.md` Stage 2.5: VISUAL ASSETS

---

## Output Structure

```
# Specified via -o flag
output/images/my-image.png    # Generated image
output/images/my-image.txt    # Prompt used (for regeneration)
```

**Example:**
```bash
/generate-image "zero trust architecture" -o output/images/zero-trust.png
```

---

## CLI Usage

```bash
# Generate image
python tools/image-generation/generate_image.py "prompt" -o output/images/image.png

# API check
python tools/image-generation/generate_image.py --check
```

---

## Inline Image Markers (Future)

Add markers in draft.md for inline concept images:

```markdown
<!-- image: zero trust architecture with encrypted tunnels -->

The zero-trust model eliminates implicit trust...
```

These will be detected and generated during the VISUAL ASSETS stage.

---

## Relationship to Diagram Generation

| Need | Tool | When to Use |
|------|------|-------------|
| Hero image | `/generate-image` | Every blog post |
| Concept visualization | `/generate-image` | Abstract ideas, moods |
| Technical flowchart | `diagram-generation` | Processes, architectures |
| Sequence diagram | `diagram-generation` | API flows, interactions |
| Data charts | `diagram-generation` | Risk distribution, metrics |

**Both are processed in the same VISUAL ASSETS stage** of the blog workflow.

---

## Dynamic Model Selection

The tool uses `tools/research/openrouter/fetch_models.py` to dynamically select the latest FLUX model:

```python
model = get_latest_model("black-forest-labs", prefer_keywords=["flux", "max"])
```

This ensures the tool always uses the best available model without hardcoding model IDs that could become deprecated.

**Model cache:** 24-hour TTL, stored in `.cache/openrouter/models.json`

---

## Troubleshooting

**Issue: "OPENROUTER_API_KEY not found"**
- Add to `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`

**Issue: "No allowed providers available"**
- Check OpenRouter dashboard for provider status
- Run `/generate-image --check` to verify connectivity

**Issue: "Request timed out"**
- FLUX generation takes 30-120 seconds
- Use `--timeout 300` for larger images

**Issue: Repetitive styles**
- Working as designed - variety comes from random pool selection
- Each generation should produce different results

---

## Examples

```bash
# Concept visualization
/generate-image "human directing multiple AI agents in harmony" -o output/images/collab.png

# Security-themed image
/generate-image "zero trust network with encrypted tunnels" -o output/images/zero-trust.png

# Check API before generating
/generate-image --check
```

---

## Related

- `skills/diagram-generation/` - Mermaid/PlantUML diagram export
- `skills/writer/workflows/blog-content.md` - Full blog workflow
- `commands/blog-post.md` - Blog post creation command
- `tools/research/openrouter/` - Model discovery and API client

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
