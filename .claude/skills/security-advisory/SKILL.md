---
name: security-advisory
description: Cybersecurity advisory with 3 modes - formal risk assessments using structured 22-question methodology, ad-hoc security guidance, and multi-framework policy generation. Consultation-focused (no hands-on testing).
---

# Security Advisory Skill

**Auto-loaded when `security` agent invoked with advisory task**

Unified cybersecurity advisory with 3 modes: Risk Assessment (formal 22-question structured), Ad-Hoc Advisory (general security guidance), and Policy Generation (multi-framework policy development).

**Core Philosophy:** Hands-off approach. Consultation and guidance, not hands-on testing. Framework-based analysis (NIST CSF, ISO 27001, SOC 2).

---

## 🚨 Critical Rules

**Before providing ANY advisory:**

1. **Library Exploration** - ALWAYS explore `resources/library/` for relevant frameworks, benchmarks, methodologies based on topic
2. **Framework-Based Analysis** - Use NIST CSF, ISO 27001, SOC 2, PCI DSS as appropriate
3. **No Hands-On Testing** - Advisory only, delegate to security-testing for hands-on work
4. **Formal vs Ad-Hoc Detection** - Route to appropriate workflow based on request type
5. **Context Loading** - Read CLAUDE.md → SKILL.md before starting
6. **Fast Mode Default** - No checkpoints unless Deep Mode explicitly requested

**Quality Standards = Advisory Credibility** - See `reference/advisory-standards.md`

---

## 📚 Library Exploration (CRITICAL)

**BEFORE providing guidance, dynamically explore for relevant context:**

```
resources/library/                    ← Frameworks, standards, benchmarks
├── benchmarks/                       (CIS controls, hardening guides)
├── books/                            (security methodology books)
├── frameworks/                       (NIST, OWASP, PCI-DSS, HIPAA, GDPR, MITRE)
├── repositories/                     (OWASP cheatsheets, ASVS, WSTG, OSCAL)
└── threat-intelligence/              (threat data and research)
```

**Dynamic Discovery Workflow:**
1. Identify topic/compliance keywords from user request
2. Explore with Glob: `resources/library/**/*{keyword}*` (NOT hardcoded paths)
3. Read discovered materials relevant to the question
4. Cite specific framework sections/control numbers in response

**Example explorations:**
- HIPAA question → `Glob: resources/library/**/*hipaa*`
- Docker security → `Glob: resources/library/**/*docker*` OR `**/*container*`
- Incident response → `Glob: resources/library/**/*800-61*` OR `**/*incident*`

**Never hardcode specific file paths** - always discover dynamically

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Sonnet (risk assessment, advisory analysis)
**Upgrade to Opus:** Strategic security decisions, complex risk modeling, novel threat scenarios
**Research:** Perplexity Sonar-Pro for industry threat research, regulatory updates

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## Decision Tree: Advisory Mode Selection

**Level 1: What TYPE of advisory?**

### Mode 1: Risk Assessment (Formal Structured)

**Detection Keywords:**
- User: "risk assessment", "security assessment", "security posture assessment"
- "22 questions", "structured assessment", "compliance assessment"
- "deliverables", "assessment report", "120-day plan"
- Request mentions formal engagement

**Decision Path:** Risk Assessment → 22-Question Methodology → `workflows/risk-assessment.md`

**Workflow Phases:**
1. COLLECT (gather context via 22-question framework)
2. ANALYZE (identify gaps against compliance frameworks)
3. DELIVER (executive summary, risk register, remediation roadmap)

**Characteristics:**
- Formal engagement with deliverables
- 22-question structured methodology
- Compliance framework mapping (NIST CSF, ISO 27001, SOC 2)
- 3 deliverables: Executive Summary, Risk Register, 120-Day Remediation Plan
- 2-4 hours typical duration
- Fast Mode (no checkpoints)

**Workflow:** `workflows/risk-assessment.md`

**Output:** `output/engagements/risk-assessments/{client}-{YYYY-MM}/`

---

### Mode 2: Ad-Hoc Advisory (General Guidance)

**Detection Keywords:**
- User: "how do I...", "best practices for...", "what's the best way to..."
- "threat intelligence", "security guidance", "recommendation"
- "compliance question", "policy advice"
- Quick questions without formal engagement

**Decision Path:** Ad-Hoc Advisory → General Guidance → `workflows/ad-hoc-advisory.md`

**Workflow Steps:**
1. Understand question and context
2. Provide framework-based guidance (NIST CSF, OWASP, CIS)
3. Include references and best practices
4. Document session for continuity

**Characteristics:**
- Conversational response (not formal deliverable)
- Framework-based guidance
- Quick turnaround (15-30 minutes)
- Session documentation for continuity
- Fast Mode (no checkpoints)

**Workflow:** `workflows/ad-hoc-advisory.md`

**Output:** Session documentation only

---

### Mode 3: Policy Generation (Multi-Framework)

**Detection Keywords:**
- User: "generate policies", "create policies", "policy development"
- "security policy", "compliance policies", "policy templates"
- "policy generation", "multi-framework policy"
- Request for organization-specific security policies

**Decision Path:** Policy Generation → Framework Selection → `workflows/policy-generation-workflow.md`

**Workflow Phases:**
1. IDENTIFY (applicable compliance frameworks based on industry/requirements)
2. ANALYZE (required policies based on framework mapping)
3. CUSTOMIZE (collect organization variables, intelligent defaults)
4. GENERATE (policies with multi-framework citations)
5. VALIDATE (completeness against framework requirements)

**Characteristics:**
- Multi-framework policy development (NIST CSF, ISO 27001, PCI DSS, HIPAA, GDPR, SOC 2)
- 25+ policy templates with intelligent defaults
- Framework-specific citations in each policy
- Organization size-based customization
- Industry-specific customizations
- 2-4 hours for complete policy suite

**Workflow:** `workflows/policy-generation-workflow.md`

**Templates:** `templates/policies/` (25 policy templates)

**Output:** `output/engagements/policy-generation/{client}-{YYYY-MM}/`

---

## Routing Decision Matrix

| User Request | Mode | Command | Deliverables | Duration |
|--------------|------|---------|--------------|----------|
| "Conduct formal security assessment for our org" | Risk Assessment | `/risk-assessment` | 6 files | 2-4 hours |
| "How do I secure Docker containers?" | Ad-Hoc Advisory | `/security-advice` | Session doc | 15-45 min |
| "22-question security posture review" | Risk Assessment | `/risk-assessment` | 6 files | 2-4 hours |
| "What are NIST CSF best practices for X?" | Ad-Hoc Advisory | `/security-advice` | Session doc | 15-45 min |
| "Generate security policies for our organization" | Policy Generation | `/policy` | Policy suite | 2-4 hours |
| "Create policies for HIPAA/PCI DSS compliance" | Policy Generation | `/policy` | Policy suite | 2-4 hours |

---

## Workflow: Risk Assessment (3 Phases)

**COLLECT → ANALYZE → DELIVER**

### Phase 1: COLLECT (22-Question Framework)

**Structured Questioning:**

**Section 1: Organizational Context (5 questions)**
1. Industry and regulatory requirements
2. Organization size and structure
3. Critical assets and data
4. Current compliance frameworks
5. Risk tolerance and business objectives

**Section 2: Technical Posture (8 questions)**
6. Network architecture and segmentation
7. Endpoint security controls
8. Authentication and access management
9. Encryption standards
10. Patch management processes
11. Backup and recovery capabilities
12. Security monitoring and logging
13. Incident response capabilities

**Section 3: Governance (5 questions)**
14. Security policies and procedures
15. Security awareness training
16. Third-party risk management
17. Vendor security requirements
18. Security budget and resources

**Section 4: Compliance (4 questions)**
19. Regulatory requirements (HIPAA, PCI DSS, GDPR)
20. Audit history and findings
21. Compliance gaps identified
22. Remediation timelines

---

**OSINT Industry Research (Between Phases 1-2):**

After collecting client information, delegate industry threat intelligence research:

```markdown
Load osint-research skill for industry threat landscape research.

**Caller:** security-advisory
**Mode:** fast (30-45 min for risk assessment Phase 2)

**Research Plan:**
- Industry threat landscape
- Regulatory requirements
- Recent breach trends in industry
- Competitor security posture
- Compliance framework documentation

**Output:** output/engagements/advisory/{client}/02-research/intelligence-summary.md

osint-research executes WebSearch + industry reports for compliance context.
```

**Result:** Industry-specific threat intelligence ready for framework mapping

---

### Phase 2: ANALYZE

**Framework Mapping:**
- Map current state to NIST CSF (Identify, Protect, Detect, Respond, Recover)
- Identify gaps against ISO 27001 controls
- Assess SOC 2 readiness (if applicable)
- Map to industry-specific compliance (HIPAA, PCI DSS, GDPR)

**Risk Scoring:**
- Critical: Major gaps with high business impact
- High: Significant gaps with moderate impact
- Medium: Process improvements needed
- Low: Best practice enhancements

---

### Phase 3: DELIVER

**Deliverables (3 files):**

1. **Executive Summary**
   - Current security posture assessment
   - Critical findings (top 3-5)
   - Overall risk rating
   - Strategic recommendations

2. **Risk Register**
   - All findings with risk ratings
   - Business impact analysis
   - Compliance framework mapping
   - Evidence references

3. **120-Day Remediation Plan**
   - Month 1: Critical fixes (high-impact, quick wins)
   - Month 2-3: High-priority projects
   - Month 4: Process improvements
   - Resource requirements and timeline

**See:** `workflows/risk-assessment.md` for complete 22-question methodology

---

## Workflow: Ad-Hoc Advisory

**UNDERSTAND → GUIDE → DOCUMENT**

### Step 1: UNDERSTAND

**Context Gathering:**
- What is the specific question?
- What framework/standard applies? (NIST CSF, OWASP, CIS)
- Industry context (healthcare, financial, technology)
- Current state and constraints

---

### Step 2: GUIDE

**Framework-Based Guidance:**
- Reference applicable framework (NIST CSF, ISO 27001, OWASP)
- Provide best practices with citations
- Include practical implementation steps
- Identify potential pitfalls

**Example Response Structure:**
```
Question: How do I secure Docker containers?

Framework Reference: CIS Docker Benchmark
Best Practices:
1. Use official images with verified publishers
2. Implement least privilege (non-root users)
3. Enable Docker Content Trust (image signing)
4. Scan images for vulnerabilities (Trivy, Clair)
5. Apply resource limits (CPU, memory)

References:
- CIS Docker Benchmark v1.6.0
- NIST SP 800-190 (Application Container Security)
```

---

### Step 3: DOCUMENT

**Session Documentation:**
- Question asked
- Guidance provided
- Framework references
- Follow-up items (if any)

**See:** `workflows/ad-hoc-advisory.md` for complete approach

---

## When to Use Security Advisory vs Other Skills

**✅ Use security-advisory for:**
- Formal risk assessments (22-question structured)
- Security posture evaluations
- Compliance framework guidance (NIST CSF, ISO 27001, SOC 2)
- Policy and process recommendations
- Strategic security guidance
- Quick security best practices questions

**❌ Use security-testing instead for:**
- Hands-on penetration testing
- Vulnerability scanning
- Network segmentation testing
- Exploitation and proof-of-concept
- Technical security testing

**❌ Use legal instead for:**
- Compliance review (HIPAA, PCI DSS, GDPR legal requirements)
- Risk assessment (legal risks, CFAA compliance)
- Contract review (scope agreements, NDAs)

---

## Compliance Frameworks

**Primary Frameworks:**
- **NIST Cybersecurity Framework (CSF)** - Identify, Protect, Detect, Respond, Recover
- **ISO 27001/27002** - Information security management
- **SOC 2** - Service organization controls (Trust Services Criteria)
- **CIS Controls** - 18 critical security controls
- **OWASP** - Web application security (Top 10, ASVS)

**Industry-Specific:**
- **HIPAA** - Healthcare data security
- **PCI DSS** - Payment card data security
- **GDPR** - European data protection
- **CCPA** - California consumer privacy

**See:** `reference/frameworks.md` for complete framework mappings

---

## Fast Mode vs Deep Mode

**Fast Mode (Default - 90% of advisory work):**
- Single-session work (2-4 hours for risk assessment, 15-30 min for ad-hoc)
- No checkpoints during assessment
- Track deliverables only (executive summary, risk register, remediation plan)
- Direct execution → verified output

**Deep Mode (Opt-in - 10% of advisory work):**
- Multi-week security program development (2+ weeks)
- SESSION-STATE.md tracking for multi-session continuity
- Checkpoints after major milestones
- Triggered by: User explicitly requests "--deep", "comprehensive security program"

**See:** `docs/streamlining-methodology.md` for complete guidance

---

## Output Structure

**Risk Assessment:**
```
output/engagements/risk-assessments/{client}-{YYYY-MM}/
   README.md                          (Engagement overview)
   01-executive-summary.md            (C-level summary)
   02-risk-register.md                (All findings with risk ratings)
   03-remediation-plan-120-day.md     (Month 1, 2-3, 4 priorities)
   supporting/
      22-question-responses.md        (Raw data collected)
      framework-mapping.md            (NIST CSF, ISO 27001 mapping)
```

**Ad-Hoc Advisory:**
- Session documentation only (no formal deliverables)

---

## Tools

| Tool | Purpose | Location |
|------|---------|----------|
| WebSearch | Framework research | Native |
| WebFetch | Deep content extraction | Native |
| Read | Framework documentation | Native |

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `advisory-standards.md` | Quality standards for advisory work |
| `frameworks.md` | NIST CSF, ISO 27001, SOC 2, CIS Controls |
| `22-question-methodology.md` | Complete 22-question framework |

---

## Integration Points

**Security Testing Integration:**
- Risk assessment identifies testing priorities
- Recommendations may include penetration testing
- Delegate hands-on testing to security-testing skill

**Legal Integration:**
- Compliance requirements (HIPAA, PCI DSS, GDPR)
- Risk assessment with legal context
- Contract review for security requirements

**Infrastructure Operations Integration:**
- Infrastructure hardening recommendations
- Docker security guidance
- Zero-trust architecture design

---

## Common Scenarios

**Formal Risk Assessment:** "Conduct security assessment for our healthcare organization"
→ Risk Assessment → 22 questions → 3 deliverables → 2-4 hours

**Ad-Hoc Guidance:** "How do I secure API endpoints?"
→ Ad-Hoc Advisory → OWASP guidance → Session doc → 15-30 min

**Compliance Assessment:** "Are we SOC 2 ready?"
→ Risk Assessment → SOC 2 focus → 3 deliverables → 2-4 hours

**Quick Question:** "What are NIST CSF best practices for incident response?"
→ Ad-Hoc Advisory → NIST CSF reference → Session doc → 15-30 min

---

## Version History

**v2.0 (2025-12-11)** - Fresh framework rebuild
- Decision tree router (Risk Assessment vs Ad-Hoc Advisory)
- 22-question structured methodology
- Progressive disclosure architecture
- Fast Mode default (no checkpoints)

---

**Version:** 2.0
**Last Updated:** 2025-12-11
**Status:** Decision tree router with framework-based analysis
