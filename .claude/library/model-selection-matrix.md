# Model Selection Matrix

**Purpose:** Task-to-model mapping for optimal cost, speed, and quality trade-offs

**Dynamic Selection:** All model references use `tools/research/openrouter/fetch_models.py` for latest versions

---

## Quick Reference

| Task Type | Model | Provider | Why |
|-----------|-------|----------|-----|
| File operations, templates | Haiku | Anthropic | Fastest, cheapest, sufficient |
| Day-to-day coding | Sonnet | Anthropic | Balanced performance/cost |
| Novel problems, architecture | Opus | Anthropic | Frontier reasoning |
| Agentic coding workflows | Grok Code | xAI | Reasoning traces visible |
| Adversarial review | Grok 3 | xAI | Challenge assumptions |
| Deep research, tool calling | Grok 4.1 Fast | xAI | 2M context, citations |
| OSINT, real-time research | Perplexity Sonar | Perplexity | Current events, citations |

---

## Model Profiles

### Anthropic: Claude Haiku 4.5

**Strengths:**
- Fastest response time
- Most cost-efficient
- Near-frontier intelligence (matches Sonnet 4 on many tasks)
- Extended thinking capability
- Excellent for sub-agents and parallel execution

**Best For:**
- File organization and folder creation
- Template application
- Format validation and linting
- Routing decisions
- Checklist execution
- Simple transformations
- High-volume operations
- Sub-agents in multi-agent workflows

**Not For:**
- Novel problem solving
- Complex architecture decisions
- Deep reasoning chains

**Cost:** $ (cheapest)
**Speed:** ⚡⚡⚡ (fastest)
**Context:** 200K tokens

---

### Anthropic: Claude Sonnet 4.5

**Strengths:**
- State-of-the-art coding (72.7% SWE-bench)
- Autonomous codebase navigation
- Strong tool orchestration
- Extended context (1M tokens)
- Balanced capability/efficiency

**Best For:**
- Day-to-day code writing
- Standard workflows and agents
- Documentation writing
- Code reviews (medium complexity)
- Analysis tasks
- Research synthesis
- Multi-context workflows
- Most skill/agent work

**Not For:**
- Extremely complex novel problems
- When speed is critical (use Haiku)
- When deep reasoning needed (use Opus)

**Cost:** $$ (moderate)
**Speed:** ⚡⚡ (fast)
**Context:** 1M tokens

---

### Anthropic: Claude Opus 4.5

**Strengths:**
- Frontier reasoning model
- Long-horizon tasks (hours of continuous operation)
- Complex software engineering
- Multimodal capabilities
- Improved robustness to prompt injection

**Best For:**
- Novel problem solving
- Complex architecture decisions
- Deep security analysis
- Multi-file refactoring
- Strategic planning
- Autonomous research
- Extended thinking tasks
- Multi-step planning

**Not For:**
- Simple operations (wasteful)
- High-volume tasks (expensive)
- When speed matters

**Cost:** $$$$ (most expensive)
**Speed:** ⚡ (slower)
**Context:** 200K tokens

**Usage Pattern:** Use sparingly for tasks that genuinely need frontier reasoning

---

### xAI: Grok Code Fast 1

**Strengths:**
- Speedy agentic coding
- Reasoning traces visible in response
- Economical for coding tasks
- Developer can steer workflows

**Best For:**
- Code generation with reasoning
- Security code review (explains WHY code is vulnerable)
- Debugging with explanation
- Technical problem solving
- When reasoning trace visibility needed
- Agentic coding workflows
- Educational code reviews

**Not For:**
- Non-coding tasks
- When reasoning traces not needed
- Simple format checks (use Haiku)

**Cost:** $$ (moderate)
**Speed:** ⚡⚡ (fast)
**Context:** 256K tokens

---

### xAI: Grok 4.1 Fast

**Strengths:**
- Best agentic tool calling
- 2M context window (largest)
- Excels at customer support simulation
- Deep research capabilities
- Can enable/disable reasoning

**Best For:**
- Deep research tasks
- Agentic workflows with many tool calls
- Customer support scenarios
- Large context requirements
- Real-world use cases

**Not For:**
- Simple tasks (overkill)
- When cost matters

**Cost:** $$ (moderate)
**Speed:** ⚡⚡ (fast)
**Context:** 2M tokens

---

### xAI: Grok 3 / Grok 3 Mini

**Strengths:**
- Thinking before responding
- Raw thinking traces accessible
- Logic-based reasoning
- Contrarian perspectives

**Best For:**
- Adversarial review (QA)
- Challenge assumptions
- Logic validation
- Detect hallucinations
- Contrarian perspectives

**Not For:**
- Coding (use Grok Code)
- Research (use Grok 4.1 or Perplexity)

**Cost:** $ (cheap)
**Speed:** ⚡⚡⚡ (fast)
**Context:** 131K tokens

---

### Perplexity: Sonar-Pro

**Strengths:**
- Real-time web search
- Automatic citations
- Current events knowledge
- Up-to-date information

**Best For:**
- OSINT research
- Current events analysis
- Citation-heavy work
- Real-time data needs
- Market research

**Not For:**
- Coding tasks
- Tasks not requiring real-time data
- Deep reasoning without web access

**Cost:** $$ (moderate)
**Speed:** ⚡⚡ (fast, depends on search)
**Context:** Varies

---

## Information Retrieval Tools

Tools for documentation lookup and web research. Choose based on content type.

### Context7

**Purpose:** Programming library/framework documentation
**Wrapper:** `tools/context7/` (REST API)
**Functions:** `search_libraries()`, `get_library_docs()`

**Best For:**
- Library API references (requests, fastapi, react, next.js)
- Code examples from official documentation
- Version-specific docs (e.g., `/vercel/next.js/v15.0.0`)
- Fast-moving frameworks (Next.js, React, Tailwind, Zod)

**Key Value:** Prevents LLM hallucination of outdated APIs

**Not For:**
- Security frameworks (NIST, CIS, OWASP)
- Real-time news/events
- General web research

**Cost:** $ (cheapest - API call only)
**Token Efficiency:** 85-97% reduction with minimal mode

---

### Information Retrieval Decision Tree

```
Need external information?
  ↓
Is it library/framework documentation?
  ├─ YES → Context7 (cheapest, prevents hallucination)
  └─ NO → Continue
      ↓
Do you have a specific URL?
  ├─ YES → WebFetch
  └─ NO → Continue
      ↓
Need real-time data or news?
  ├─ YES → WebSearch (current events)
  └─ NO → Continue
      ↓
Need citations or deep OSINT?
  ├─ YES → Perplexity Sonar-Pro
  └─ NO → Continue
      ↓
Need 2M+ context or agentic tools?
  ├─ YES → Grok 4.1 Fast
  └─ NO → WebSearch (general)
```

### Tool Comparison

| Tool | Use Case | Cost | Best For |
|------|----------|------|----------|
| Context7 | Library docs | $ | Code examples, API references |
| WebFetch | Specific URL | $ | Known webpage analysis |
| WebSearch | Web queries | $$ | Current events, general info |
| Perplexity | Deep OSINT | $$ | Citations, research |
| Grok 4.1 | Large context | $$ | Tool calling, 2M+ docs |

---

## Task-Based Selection Guide

### File Operations
**Model:** Haiku 4.5
**Why:** Fast, cheap, more than sufficient

**Examples:**
- Create folder structure
- Organize files
- Apply templates
- Format code

---

### Coding - Standard
**Model:** Sonnet 4.5
**Why:** Best coding performance, balanced cost

**Examples:**
- Write new functions
- Refactor code
- Fix bugs
- Code reviews

**Upgrade to Opus when:**
- Novel architecture needed
- Multi-file complex refactoring
- Strategic design decisions

**Downgrade to Haiku when:**
- Template code
- Simple transformations
- Format fixes

---

### Coding - With Reasoning Traces
**Model:** Grok Code Fast 1
**Why:** Visible reasoning, helps understand decisions

**Examples:**
- Security code review (shows WHY vulnerable)
- Complex debugging
- Learning-focused coding
- When explanation needed
- Agentic coding workflows
- Vulnerability analysis with reasoning

---

### Analysis - Security
**Model:** Sonnet 4.5 (standard) → Opus 4.5 (novel)
**Why:** Sonnet for known patterns, Opus for novel threats

**Examples:**
- Standard vuln assessment → Sonnet
- Novel attack research → Opus
- Threat modeling (complex) → Opus
- Code security review → Sonnet

---

### Research - OSINT
**Model:** Perplexity Sonar-Pro (primary) + Grok 4.1 Fast (secondary)
**Why:** Perplexity for citations, Grok for depth

**Examples:**
- Company research
- Threat intelligence
- Market analysis
- Competitor analysis

**Pattern:** Dual-source (Perplexity + Grok) for cross-validation

---

### QA Review
**Model:** Haiku 4.5 (structured) + Grok 3 (adversarial)
**Why:** Haiku fast for checklists, Grok for challenges

**Examples:**
- Report validation → Haiku (completeness) + Grok (assumptions)
- Code review → Haiku (standards) + Grok (logic holes)
- Documentation → Haiku (format) + Grok (clarity)

---

### Writing - Content
**Model:** Sonnet 4.5 (drafting) + Perplexity (research)
**Why:** Sonnet for quality writing, Perplexity for research

**Examples:**
- Blog posts: Perplexity (research) → Sonnet (write)
- Documentation: Sonnet (write)
- Reports: Sonnet (write) + Haiku (QA)

---

### Architecture & Planning
**Model:** Opus 4.5
**Why:** Needs frontier reasoning, strategic thinking

**Examples:**
- System architecture design
- Technology stack decisions
- Security architecture
- Long-term planning

**Cost Justification:** One-time decisions with long-term impact

---

## Cost Optimization Strategies

### 1. Right-Size by Default
- **Default to Sonnet** for uncertain tasks
- **Upgrade to Opus** only when needed
- **Downgrade to Haiku** for simple operations

### 2. Multi-Model Workflows
- Use Haiku for routing/triage
- Use Sonnet for main work
- Use Opus for complex decisions
- Example: Haiku routes task → Sonnet executes → Opus for novel issues

### 3. Parallel Sub-Agents
- Spawn multiple Haiku instances for parallel work
- Cheaper than one Sonnet doing sequential work
- Use for embarrassingly parallel tasks

### 4. Research Dual-Source
- Perplexity for breadth (citations)
- Grok for depth (analysis)
- Cross-validate findings

---

## Model Selection Decision Tree

```
START
  ↓
Is task novel/complex?
  ├─ YES → Opus 4.5
  └─ NO → Continue
      ↓
Does task need real-time web data?
  ├─ YES → Perplexity Sonar-Pro
  └─ NO → Continue
      ↓
Is this adversarial/challenging task?
  ├─ YES → Grok 3
  └─ NO → Continue
      ↓
Does task need coding with reasoning traces?
  ├─ YES → Grok Code Fast 1
  └─ NO → Continue
      ↓
Is task simple/template/formatting?
  ├─ YES → Haiku 4.5
  └─ NO → Sonnet 4.5 (default)
```

---

## Skill-Specific Recommendations

### security-testing
- **Recon:** Perplexity (OSINT)
- **Testing:** Sonnet (standard) / Opus (novel)
- **Reporting:** Sonnet (write) + Haiku (QA)

### writer
- **Research:** Perplexity (depth research)
- **Drafting:** Sonnet (write)
- **QA:** Haiku (structured) + Grok 3 (adversarial)

### code-review
- **Format Checks:** Haiku (fast validation)
- **Security Review:** Grok Code Fast 1 (reasoning traces explain WHY vulnerable)
- **Logic Review:** Sonnet (complexity analysis)
- **Architecture:** Opus (design patterns)

**Why Grok Code for security:** Visible reasoning traces show step-by-step vulnerability explanation - helps understand attack vectors and remediation logic

### architecture-review
- **Threat Modeling:** Opus (complex reasoning)
- **Standards Validation:** Haiku (checklist)
- **Report Writing:** Sonnet (documentation)

### osint-research
- **Fast Mode:** Perplexity only
- **Deep Mode:** Perplexity + Grok 4.1 Fast (cross-validation)

### qa-review
- **Structured Review:** Haiku (checklists, standards)
- **Adversarial Review:** Grok 3 (challenge assumptions)
- **Cross-Validation:** Human (conflicts)

---

## Implementation

**Dynamic Selection:**
```python
from tools.research.openrouter import get_latest_model

# Get latest model by provider
haiku = get_latest_model("anthropic", prefer_keywords=["haiku"])
sonnet = get_latest_model("anthropic", prefer_keywords=["sonnet"])
opus = get_latest_model("anthropic", prefer_keywords=["opus"])
grok_code = get_latest_model("x-ai", prefer_keywords=["code"])
grok = get_latest_model("x-ai")
perplexity = get_latest_model("perplexity", prefer_keywords=["sonar"])
```

**In Skills/Agents:**
```markdown
## Model Selection

**Default:** Latest Sonnet
**Upgrade to Opus when:** Novel problem, complex architecture, strategic planning
**Downgrade to Haiku when:** Templates, formatting, routing, checklists
```

---

**Version:** 1.1
**Last Updated:** 2025-12-19
**Dynamic Selection:** OpenRouter API via `tools/research/openrouter/fetch_models.py`
**Information Retrieval:** Context7 (library docs) + WebSearch/Perplexity (research)
