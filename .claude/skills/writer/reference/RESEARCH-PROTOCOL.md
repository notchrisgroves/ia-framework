# Research Protocol

**Multi-source OSINT research methodology for Intelligence Adjacent content**

**Minimum Standard:** 10+ sources for ANY published content
**Quality Standard:** Diverse, authoritative, verifiable sources

---

## Research Philosophy

**Evidence-Based:** All claims backed by verifiable sources
**Multi-Perspective:** Diverse sources prevent echo chamber
**Primary Focus:** Original sources over aggregators
**Adversarial Validation:** Use Grok to challenge assumptions

---

## Source Priority Matrix

**Use sources in this priority order:**

### Tier 1: Primary Sources (Highest Authority)

**Official Documentation:**
- Vendor security advisories
- CVE/NVD databases (MITRE, NIST)
- Official product documentation
- RFC specifications
- Academic papers (peer-reviewed)

**Direct Analysis:**
- GitHub repositories (code review)
- Library documentation via Context7
- Security tool outputs (Burp, Nmap, etc.)
- Direct testing/experimentation

**Why Tier 1:**
- Most authoritative
- Direct from source
- Verifiable and reproducible
- No intermediary interpretation

### Tier 2: Expert Sources (High Authority)

**Security Research:**
- KrebsOnSecurity
- Dark Reading
- BleepingComputer
- Schneier on Security
- Talos Intelligence

**Technical Blogs:**
- Company engineering blogs (Cloudflare, Netflix, Shopify)
- Security researchers (personal blogs with track record)
- SANS Internet Storm Center

**Why Tier 2:**
- Expert analysis
- Industry credibility
- Original research/insights
- Track record of accuracy

### Tier 3: Community Sources (Medium Authority)

**Technical Communities:**
- Stack Overflow (validated answers)
- Reddit r/netsec, r/AskNetsec (upvoted, verified)
- HackerNews discussions
- GitHub issue discussions

**Standards Organizations:**
- OWASP documentation
- CIS Benchmarks
- NIST frameworks

**Why Tier 3:**
- Community validation
- Practical real-world insights
- Multiple perspectives
- Less formal but useful

### Tier 4: AI/Model Sources (Validation Only)

**Multi-Model Research:**
- Grok (adversarial perspective, challenges assumptions)
- GPT-4 (structured analysis, comprehensive synthesis)
- Claude (technical accuracy, code review)
- Perplexity (sourced research with citations)

**Why Tier 4:**
- Requires verification (not authoritative alone)
- Useful for synthesis and perspective
- Must cite original sources, not AI output
- Good for adversarial validation

**NEVER cite:** "According to ChatGPT..." (cite the PRIMARY source AI referenced)

---

## Research Methodologies by Content Type

### Deep Research (4-6 hours, Tier 1 content)

**Use for:** Trending topics, original research, exclusive insights

**Process:**
1. **Primary source gathering (2-3 hours)**
   - Official advisories, CVEs, vendor docs
   - Code analysis (GitHub, Context7)
   - Direct testing/experimentation

2. **Expert analysis (1-2 hours)**
   - Security researcher blogs
   - Company engineering posts
   - Technical deep dives

3. **Community validation (30-60 min)**
   - HackerNews discussions
   - Reddit technical communities
   - GitHub issues/PRs

4. **Multi-model synthesis (1 hour)**
   - Grok: Challenge assumptions, find gaps
   - GPT-4: Comprehensive synthesis
   - Claude: Technical accuracy check

**Output:**
- 15-20 sources
- Primary sources dominant (60%+)
- Original insights from analysis
- Multi-perspective validation

### Standard Research (2-4 hours, Tier 2 content)

**Use for:** Analysis posts, expert synthesis, practical guides

**Process:**
1. **Primary sources (1-2 hours)**
   - Official docs, CVEs
   - Code examples via Context7

2. **Expert sources (1 hour)**
   - Industry blogs
   - Security research

3. **Multi-model validation (30-60 min)**
   - Grok for adversarial check
   - GPT-4 for synthesis

**Output:**
- 10-12 sources
- Mix of primary (40%) and expert (60%)
- Practical application focus

### Quick Research (1-2 hours, Tier 3 content)

**Use for:** How-to guides, tool overviews

**Process:**
1. **Official documentation (30-60 min)**
   - Tool/library official docs
   - Quick CVE check if relevant

2. **Community sources (30 min)**
   - Stack Overflow best practices
   - GitHub examples

3. **Validation (15-30 min)**
   - Quick multi-model check

**Output:**
- 8-10 sources
- Focused on single tool/technique
- Beginner-friendly

---

## Research Tools & Access

### Context7

**Use for:** Code examples, library documentation

**Best for:**
- Official library/framework documentation
- Code implementation examples
- API reference details
- Technical specifications

**Limitation:** May not have latest versions, always verify currency

### OpenRouter (Multi-Model)

**Grok:**
- Adversarial perspective
- Challenges common assumptions
- Finds gaps in logic
- Contrarian validation

**GPT-4:**
- Comprehensive structured research
- Synthesis of multiple sources
- Deep technical analysis
- Pattern recognition

**Claude:**
- Technical accuracy
- Code review and analysis
- Security-focused insights
- Careful reasoning

**Process:**
1. Research question to all 3 models
2. Compare responses for discrepancies
3. Use disagreements to identify areas needing deeper research
4. Cite PRIMARY sources, not model outputs

### WebSearch (Native Claude)

**Use for:**
- Recent news and developments
- Official documentation sites
- Security advisories
- Industry analysis

**Search strategies:**
- Specific: `"CVE-2025-1234" site:nvd.nist.gov`
- Vendor: `site:vendor.com "security advisory"`
- Recent: Add year `security topic 2025`

### Manual OSINT

**Direct investigation:**
- CVE databases (NVD, MITRE)
- GitHub repository analysis
- Burp/Nmap scan results (for security content)
- Direct tool testing

---

## Source Documentation Standards

### During Research

**Track ALL sources in sources.txt:**
```
# Primary Sources
- [CVE-2025-1234](https://nvd.nist.gov/...) - SQL injection vulnerability
- [Vendor Advisory](https://vendor.com/...) - Patch information
- [GitHub Issue #123](https://github.com/...) - Community discussion

# Expert Analysis
- [KrebsOnSecurity](https://krebsonsecurity.com/...) - Impact analysis
- [Cloudflare Blog](https://blog.cloudflare.com/...) - Technical deep dive

# Community Validation
- [HackerNews Discussion](https://news.ycombinator.com/...) - Practitioner insights
- [Reddit r/netsec](https://reddit.com/r/netsec/...) - Community perspective

# Multi-Model Research
Primary sources verified via: Grok (adversarial), GPT-4 (comprehensive), Claude (technical)
```

### In Published Content

**Sources section (at end of post):**
```markdown
## Sources

- [CVE-2025-1234 - NVD Database](https://nvd.nist.gov/...) - Official vulnerability details
- [Vendor Security Advisory](https://vendor.com/...) - Patch and remediation
- [Krebs on Security Analysis](https://krebsonsecurity.com/...) - Impact assessment
- [GitHub Repository](https://github.com/user/repo) - Implementation code
```

**Format:**
- Link text descriptive
- URL accessible (public, not paywalled without note)
- Brief description of what source provides
- In order of importance/relevance

---

## Research Quality Checks

### Source Validation

**Before using ANY source, verify:**
- [ ] Authoritative (known expert/organization)
- [ ] Current (within 6-12 months for security topics)
- [ ] Verifiable (claims can be reproduced)
- [ ] Accessible (public URL or reproducible)
- [ ] Relevant (directly supports claim being made)

### Red Flags

**Avoid sources with:**
- ❌ No author attribution
- ❌ Excessive ads/spam
- ❌ Uncited claims (no sources)
- ❌ Clickbait headlines
- ❌ Obvious bias without disclosure
- ❌ Outdated information (years old for tech topics)

### Citation Standards

**Cite when:**
- Making factual claims
- Providing statistics/data
- Referencing vulnerabilities
- Describing techniques
- Including code examples

**DON'T cite:**
- Common knowledge (TCP uses port 80 for HTTP)
- Your own testing results (describe methodology instead)
- AI model outputs (cite primary source AI referenced)

---

## Multi-Model Research Protocol

### Step 1: Initial Research (All 3 Models)

**Prompt template:**
```
Research [topic] with focus on [specific aspect].

Requirements:
- Technical accuracy
- Recent developments (2024-2025)
- Primary sources
- Security implications

Cite all sources.
```

**Run in parallel:** Grok + GPT-4 + Claude

### Step 2: Compare & Identify Gaps

**Look for:**
- Discrepancies (signals need for deeper research)
- Gaps (one model found something others missed)
- Consensus (validates findings)
- Contradictions (require primary source verification)

### Step 3: Adversarial Validation (Grok Focus)

**Prompt:**
```
Challenge these findings:
[List consensus findings]

What are we missing?
What assumptions are wrong?
What's the contrarian view?
```

### Step 4: Primary Source Verification

**For each claim:**
- Find primary source (official docs, CVE, vendor advisory)
- Verify claim accuracy
- Note any differences from model outputs
- Cite primary source, NOT model

---

## Research Output Files

### Organized Research Directory

```
output/blog/research/{slug}/
├── research-notes.md        # Complete research notes with findings
├── sources.txt              # All sources with descriptions
├── key-insights.md          # Original analysis and insights
├── model-outputs/           # Multi-model research (for reference)
│   ├── grok-response.md
│   ├── gpt4-response.md
│   └── claude-response.md
└── evidence/                # Screenshots, data, experiments
    ├── screenshot-1.png
    └── test-results.txt
```

### research-notes.md Template

```markdown
# Research Notes: [Topic]

## Research Question
[What we're investigating]

## Key Findings
1. [Finding with source]
2. [Finding with source]

## Primary Sources
- [Source 1] - [Key information]
- [Source 2] - [Key information]

## Expert Analysis
- [Source 3] - [Expert perspective]

## Community Insights
- [Source 4] - [Practitioner experience]

## Original Analysis
[Your synthesis and insights]

## Gaps & Questions
- [Areas needing more research]
- [Unresolved questions]

## Sources Summary
Total: 12 sources (6 primary, 4 expert, 2 community)
```

---

## Common Research Mistakes

### Mistake 1: Echo Chamber Research

**Problem:** All sources say same thing (no diversity)
**Solution:** Seek contrarian views, use Grok for adversarial perspective

### Mistake 2: Recency Bias

**Problem:** Only use latest sources, miss important historical context
**Solution:** Include foundational sources (RFCs, academic papers, original research)

### Mistake 3: Authority Worship

**Problem:** Trust "expert" without verification
**Solution:** Verify claims with primary sources, even from experts

### Mistake 4: AI Over-Reliance

**Problem:** Cite "ChatGPT says..." or "According to Claude..."
**Solution:** Use AI for research direction, ALWAYS cite primary sources

### Mistake 5: Insufficient Breadth

**Problem:** 2-3 sources for complex topic
**Solution:** Minimum 10 sources, 15+ for deep research

---

## Quality Metrics

**Minimum standards before publishing:**
- [ ] 10+ sources documented in sources.txt
- [ ] Primary sources verifying key claims
- [ ] Multi-model validation completed
- [ ] All claims traceable to sources
- [ ] Sources properly cited in post
- [ ] Adversarial perspective considered (Grok)
- [ ] No AI model citations (only primary sources)

---

## Research Ethics

**Always:**
- ✅ Cite sources properly
- ✅ Link to original when possible
- ✅ Credit researchers/authors
- ✅ Note when behind paywall
- ✅ Disclose conflicts of interest

**Never:**
- ❌ Plagiarize (cite and quote)
- ❌ Misrepresent sources
- ❌ Cherry-pick to support narrative
- ❌ Cite inaccessible sources without note
- ❌ Present speculation as fact

---

**Research is the foundation of quality content. No shortcuts.**

---

**See Also:**
- `workflows/blog-content.md` - Complete blog workflow
- `CONTENT-STANDARDS.md` - Quality requirements
- `library/prompts/content-guardian.md` - Enforcement protocol
