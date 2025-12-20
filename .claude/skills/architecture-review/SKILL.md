---
name: architecture-review
description: System design security analysis with STRIDE/PASTA threat modeling, NIST SP 800-160/OWASP ASVS validation, secure architecture patterns, and defense-in-depth validation. Use for threat modeling, zero trust design, network segmentation review, and cloud architecture security.
---

# Architecture Review Skill

**Auto-loaded when `security` agent invoked for architecture security**

Specialized in STRIDE/PASTA threat modeling, NIST SP 800-160/OWASP ASVS validation, secure architecture patterns, and zero trust design.

**Core Philosophy:** Threat modeling is mandatory. All reviews must include STRIDE/PASTA/ATT&CK analysis. Defense-in-depth validation ensures layered security. Standards-based recommendations (NIST/OWASP/CSA) maintain professional credibility.

---

## 🚀 Quick Access

**Slash Command:** `/arch-review`

Architecture security review with threat modeling (STRIDE, PASTA, Attack Trees) and defense-in-depth validation.

**See:** `commands/arch-review.md` for complete workflow

---

## 🚨 Critical Rules

**Before starting any architecture review:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md
2. **Threat Modeling Required** - All reviews MUST include threat modeling (STRIDE, PASTA, or ATT&CK-based) - never skip threat identification phase
3. **Checkpoint After Review Phase** - Update session file after major phases (threat modeling, design validation, defense-in-depth analysis) with threats identified and weaknesses found
4. **Defense-in-Depth Validation** - All architectures MUST be evaluated for layered security controls (never approve single-point-of-failure designs)
5. **Standards-Based Recommendations** - All recommendations MUST reference NIST 800-160, OWASP ASVS, or CSA guidance (never provide unsupported design opinions)

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ architecture components reviewed, refresh rules.

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Opus (complex threat modeling, architecture security design, attack path analysis)
**Downgrade to Sonnet:** Standard threat model validation, known pattern identification
**Downgrade to Haiku:** Simple architecture questions, standards lookups

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## When to Use

✅ **Use architecture-review for:**
- Threat modeling (STRIDE, PASTA, MITRE ATT&CK, Attack Trees)
- Secure design pattern validation (Zero Trust, Defense-in-Depth, Secure by Default)
- Defense-in-depth analysis (layered security, SPOF identification)
- Compliance validation (NIST, OWASP, CSA, PCI DSS, HIPAA)
- Architecture diagram security annotations
- Network segmentation review
- API security architecture
- Cloud architecture security (AWS, Azure, GCP)
- Zero Trust Architecture (ZTA) design
- Microservices security
- Infrastructure-as-Code security review

❌ **Don't use if:**
- Source code vulnerability analysis → Use `/code-review` (code-review skill)
- System configuration hardening → Use `/secure-config` (secure-config skill)
- Dependency vulnerability scanning → Use `/dependency-audit` (dependency-audit skill)
- Active penetration testing → Use `/pentest` (security-testing skill)

---

## Prerequisites

**For Architecture Review:**
- System architecture diagrams (logical and physical)
- Network topology and data flow diagrams
- Technology stack specifications
- API specifications (OpenAPI/Swagger)
- Infrastructure-as-Code (Terraform, CloudFormation)
- Business context (data sensitivity, compliance requirements, threat actors)

**Optional (Helpful):**
- Previous security assessments
- Penetration test reports
- Incident history
- Security policies and standards

---

## Workflow: 3-Phase Architecture Review

**Total Duration:** 6-10 hours for comprehensive architecture review

### Phase 1: Threat Modeling (2-3 hours)

**Goal:** Decompose architecture, apply STRIDE/PASTA, identify threats and attack vectors, document threat register

**Actions:**
1. Decompose architecture (trust boundaries, data flows, assets, entry points)
2. Apply threat modeling methodology (STRIDE, PASTA, Attack Trees, or MITRE ATT&CK)
3. Identify threats for each component
4. Document attack vectors and scenarios
5. Assess threat severity and likelihood

**Threat Modeling Methodologies:**

**STRIDE** - Default for most reviews (comprehensive, systematic)
- Spoofing (authentication bypass)
- Tampering (data modification)
- Repudiation (denial of actions)
- Information Disclosure (data leakage)
- Denial of Service (availability impact)
- Elevation of Privilege (authorization bypass)

**PASTA** - Risk-driven reviews with business impact analysis (7 stages)
**Attack Trees** - Complex attack path analysis (visual modeling)
**MITRE ATT&CK** - Threat actor-informed design

**Deliverables:**
- `01-threat-modeling/threat-register.md`
- `01-threat-modeling/attack-scenarios.md`
- `01-threat-modeling/STRIDE-analysis.md`

**Checkpoint:** Threat modeling completed, threat register created

**Load for this phase:**
```
Read skills/architecture-review/methodologies/threat-modeling.md
# Focus on: STRIDE/PASTA/Attack Trees methodology, threat identification
```

---

### Phase 2: Design Validation (2-3 hours)

**Goal:** Review authentication, authorization, cryptography, data protection, API security, secure design patterns

**Actions:**
1. Validate authentication mechanisms (MFA, SSO, session management)
2. Review authorization models (RBAC, ABAC, least privilege)
3. Assess cryptography (TLS, encryption at rest, key management)
4. Evaluate data protection (PII handling, data classification, sanitization)
5. Review API security (authentication, rate limiting, input validation)
6. Identify secure design patterns vs anti-patterns

**Secure Patterns:**
- Zero Trust (never trust, always verify)
- Defense-in-Depth (layered security)
- Secure by Default (secure defaults)
- Separation of Duties (role segregation)
- Encryption Architecture (data protection)
- Secure API Design (API Gateway, OAuth 2.0)
- Network Segmentation (DMZ, micro-segmentation)
- Secure Logging (audit trails, tamper-proof)

**Anti-Patterns:**
- Monolithic Authentication (single auth point)
- Client-Side Security (trusting client)
- Hardcoded Secrets (credentials in code)
- Missing Rate Limiting (DoS vulnerability)
- Insufficient Logging (blind spots)
- Trust Boundary Violations (improper segmentation)
- IDOR (Insecure Direct Object References)
- Missing Security Headers (XSS, clickjacking)

**Deliverables:**
- `02-design-validation/findings-register.md`
- `02-design-validation/secure-patterns-analysis.md`
- `02-design-validation/anti-patterns-detected.md`

**Checkpoint:** Design validation completed, findings documented

**Load for this phase:**
```
Read skills/architecture-review/reference/patterns.md
# Focus on: Secure patterns, anti-patterns, pattern validation

Read skills/architecture-review/reference/standards.md
# Focus on: NIST 800-160, OWASP ASVS, CSA guidance
```

---

### Phase 3: Defense-in-Depth Analysis (2-4 hours)

**Goal:** Map security layers, identify single points of failure, evaluate network segmentation, validate monitoring and fail-safe mechanisms

**Actions:**
1. Map security layers (perimeter, network, host, application, data)
2. Identify single points of failure (SPOF)
3. Evaluate network segmentation (zones, VLANs, micro-segmentation)
4. Validate monitoring and logging (SIEM, detection coverage)
5. Assess fail-safe mechanisms (circuit breakers, rate limits, graceful degradation)
6. Review incident response capabilities

**Defense-in-Depth Layers:**
- **Layer 1: Perimeter** - Firewall, IDS/IPS, WAF, DDoS protection
- **Layer 2: Network** - Segmentation, VLANs, micro-segmentation, Zero Trust
- **Layer 3: Host** - EDR, host firewall, hardening, patching
- **Layer 4: Application** - WAF, API Gateway, authentication, authorization, input validation
- **Layer 5: Data** - Encryption at rest/transit, DLP, access controls, tokenization

**Deliverables:**
- `03-defense-in-depth/security-layers.md`
- `03-defense-in-depth/spof-analysis.md`
- `03-defense-in-depth/segmentation-review.md`
- `03-defense-in-depth/monitoring-coverage.md`

**Final deliverable:**
- `ARCHITECTURE-REVIEW-REPORT.md` (comprehensive report with executive summary, findings, recommendations, standards mapping)

**Checkpoint:** All phases completed, final report delivered

**Load for this phase:**
```
Read skills/architecture-review/reference/standards.md
# Focus on: Defense-in-depth principles, NIST zero trust, CSA cloud security
```

---

## Industry Standards

**Primary Frameworks:**
- **NIST SP 800-160** - Systems Security Engineering (all reviews)
- **OWASP ASVS** - Application Security Verification Standard (application architectures)
- **CSA Cloud Security** - Cloud Architectures (AWS, Azure, GCP)
- **NIST SP 800-207** - Zero Trust Architecture

**Compliance Standards:**
- **PCI DSS** - Payment card data
- **HIPAA** - Healthcare data
- **GDPR** - EU personal data
- **SOC 2** - Service organizations
- **ISO 27001** - Information security management
- **SABSA** - Enterprise security architecture

**Complete reference:** `reference/standards.md`

---

## Output Structure

```
output/engagements/architecture-reviews/{client}-{YYYY-MM}/
├── SCOPE.md                          (Review scope and objectives)
├── 01-threat-modeling/
│   ├── threat-register.md            (All threats identified)
│   ├── attack-scenarios.md           (Attack path analysis)
│   └── STRIDE-analysis.md            (STRIDE methodology output)
├── 02-design-validation/
│   ├── findings-register.md          (Security weaknesses)
│   ├── secure-patterns-analysis.md   (Patterns validated)
│   └── anti-patterns-detected.md     (Anti-patterns found)
├── 03-defense-in-depth/
│   ├── security-layers.md            (Layered security mapping)
│   ├── spof-analysis.md              (Single points of failure)
│   ├── segmentation-review.md        (Network segmentation)
│   └── monitoring-coverage.md        (Detection capabilities)
├── diagrams/
│   ├── architecture-annotated.png    (Annotated with threats)
│   ├── threat-model.png              (Threat model visualization)
│   └── attack-trees.png              (Attack tree diagrams)
└── ARCHITECTURE-REVIEW-REPORT.md     (Final deliverable)
```

**Multi-session tracking:** `sessions/YYYY-MM-DD-project-name.md`

---

## Progressive Context Loading

**Core Context (Always Loaded):**
- This SKILL.md file

**Extended Context (Load as Needed):**

**Threat Modeling:**
- `methodologies/threat-modeling.md` - STRIDE, PASTA, Attack Trees, MITRE ATT&CK-based threat modeling

**Standards and Compliance:**
- `reference/standards.md` - NIST SP 800-160, OWASP ASVS, CSA Cloud Security, SABSA, Zero Trust, PCI DSS, HIPAA, ISO 27001, GDPR

**Architecture Patterns:**
- `reference/patterns.md` - Secure patterns (Zero Trust, Defense-in-Depth, Secure by Default, etc.) and anti-patterns (Monolithic Auth, Client-Side Security, Hardcoded Secrets, etc.)

**Scope Decision Helper:**
- `reference/scope-decision-helper.md` - Decision tree for architecture vs code vs config vs testing

**Output Structure:**
- `reference/output-structure.md` - Directory structure, file naming, diagram formats, compliance outputs

**Workflow:**
- `workflows/architecture-review.md` - Complete 3-phase workflow with detailed steps

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ architecture components reviewed OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for architecture review:
- Context loaded (CLAUDE.md + SKILL.md)
- Threat modeling complete (STRIDE/PASTA/ATT&CK)
- Checkpoints maintained (phases, threats, weaknesses documented)
- Defense-in-depth validated (layered controls verified)
- Standards-based recommendations (NIST/OWASP/CSA citations)
```

---

## Threat Modeling Selection Guide

**Use STRIDE when:**
- Standard architecture review
- Systematic threat identification needed
- Component-level analysis required
- Time: 2-3 hours

**Use PASTA when:**
- Risk-driven review required
- Business impact analysis needed
- Compliance-focused review
- Time: 3-4 hours

**Use Attack Trees when:**
- Complex attack path analysis
- Visual modeling required
- Multiple attack vectors
- Time: 2-3 hours

**Use MITRE ATT&CK when:**
- Threat actor-informed design
- Specific adversary targeting
- Defensive architecture planning
- Time: 2-3 hours

---

## Quality Checks (Pre-Delivery)

**All architecture reviews must include:**
- ✅ Threat model completed (STRIDE/PASTA/ATT&CK)
- ✅ Threat register with all threats documented
- ✅ Design validation with findings (authentication, authorization, cryptography, data protection, API security)
- ✅ Defense-in-depth analysis (layered security mapped, SPOFs identified)
- ✅ Standards-based recommendations (NIST 800-160, OWASP ASVS, or CSA cited)
- ✅ Annotated architecture diagrams (threats and controls visualized)
- ✅ Executive summary (high-level findings for stakeholders)
- ✅ Technical report (detailed findings with remediation guidance)

---

**Version:** 2.0
**Last Updated:** 2025-12-12
**Model:** Claude Sonnet 4.5
**Framework:** STRIDE + PASTA + NIST SP 800-160 + OWASP ASVS + CSA + Zero Trust
**Pattern:** Progressive context loading with 3-phase workflow
