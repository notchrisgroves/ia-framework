---
type: workflow
name: architecture-review
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Architecture Review Workflow

**Complete 3-phase workflow for architecture security reviews**

This document covers the end-to-end process for conducting architecture security reviews.

---

## Workflow Overview

**Total Time:** 6-10 hours for comprehensive architecture review

**3 Phases:**
1. **Threat Modeling** (2-3 hours) - Identify threats and attack vectors
2. **Design Validation** (2-3 hours) - Review secure patterns and controls
3. **Defense-in-Depth Analysis** (2-4 hours) - Evaluate layered security

**Output:** Architecture review report with threat model, findings, recommendations

---

## Prerequisites

### Required Materials

**Architecture Documentation:**
- System architecture diagrams (logical and physical)
- Network topology diagrams
- Data flow diagrams (DFD)
- Component interaction diagrams
- Trust boundary documentation

**Technical Specifications:**
- Technology stack (languages, frameworks, databases)
- API specifications (OpenAPI/Swagger)
- Authentication/authorization design
- Data classification and handling
- Infrastructure-as-Code (Terraform, CloudFormation, ARM templates)

**Business Context:**
- Sensitivity of data (PII, PHI, financial, IP)
- Threat actor interest (nation-state, cybercrime, insider)
- Compliance requirements (PCI DSS, HIPAA, GDPR, SOC 2)
- Risk tolerance (high/medium/low)

**Optional (Helpful):**
- Previous security assessments
- Penetration test reports
- Incident history
- Security policies and standards

---

## Phase 1: Threat Modeling (2-3 hours)

**Objective:** Identify threats, attack vectors, and security weaknesses

### Step 1.1: Decompose Architecture (30 min)

**Actions:**
1. **Identify trust boundaries**
   - External (Internet → DMZ)
   - Internal (DMZ → Internal network)
   - Privileged (Internal → Database, management interfaces)

2. **Map data flows**
   - Input sources (user input, APIs, file uploads)
   - Processing locations (web tier, app tier, background jobs)
   - Storage locations (databases, file systems, caches)
   - Output destinations (user responses, APIs, logs)

3. **Document assets**
   - Data assets (PII, credentials, financial data, IP)
   - Service assets (authentication, payment processing, core business logic)
   - Infrastructure assets (servers, databases, load balancers)

4. **Identify entry points**
   - Public-facing (web pages, REST APIs, GraphQL endpoints)
   - Internal (admin interfaces, internal APIs, message queues)
   - External integrations (third-party APIs, webhooks, OAuth)

**Checkpoint:** Architecture decomposition documented (trust boundaries, data flows, assets, entry points)

---

### Step 1.2: Apply Threat Modeling Methodology (45-90 min)

**Choose methodology based on context:**
- **STRIDE** - Default for most reviews (comprehensive, systematic)
- **PASTA** - Risk-driven reviews with business impact analysis
- **Attack Trees** - Complex attack path analysis
- **MITRE ATT&CK** - Threat actor-informed design

**See:** `methodologies/threat-modeling.md` for complete methodology details

**STRIDE Process (Default):**

1. **Spoofing** - Identify authentication weaknesses
   - Missing MFA, weak password policies, session hijacking risks

2. **Tampering** - Identify data integrity weaknesses
   - Man-in-the-middle, database tampering, code injection

3. **Repudiation** - Identify logging/audit gaps
   - Missing authentication logs, no data access logs

4. **Information Disclosure** - Identify confidentiality weaknesses
   - Unencrypted data, verbose error messages, credential exposure

5. **Denial of Service** - Identify availability weaknesses
   - No rate limiting, resource exhaustion, single points of failure

6. **Elevation of Privilege** - Identify authorization weaknesses
   - Missing authorization checks, IDOR, privilege escalation paths

**Checkpoint:** Threat modeling completed (STRIDE categories documented, threats identified)

---

### Step 1.3: Document Threats (30 min)

**Threat Register Format:**

| Threat ID | Category | Severity | Description | Affected Components | Existing Mitigations | Recommended Mitigations |
|---|---|---|---|---|---|---|
| T-001 | Spoofing | High | No MFA on admin accounts → credential compromise | Admin portal | Password auth only | Implement MFA (TOTP, WebAuthn) |
| T-002 | Tampering | Medium | Database connection not encrypted → MITM | App → DB | None | Enable TLS for DB connections |
| T-003 | Info Disclosure | Critical | API returns full user objects → PII leakage | REST API | None | Implement response filtering (only required fields) |

**Severity Ratings:**
- **Critical** - Immediate exploitation, severe impact (data breach, full compromise)
- **High** - Exploitable with moderate effort, significant impact (privilege escalation, PII access)
- **Medium** - Requires specific conditions, moderate impact (information disclosure, DoS)
- **Low** - Difficult to exploit, minimal impact (verbose errors, metadata leakage)

**Optional: DREAD Scoring** (for prioritization):
- **D**amage (1-10): How bad would an attack be?
- **R**eproducibility (1-10): How easy to reproduce?
- **E**xploitability (1-10): How much effort to launch attack?
- **A**ffected Users (1-10): How many users impacted?
- **D**iscoverability (1-10): How easy to find vulnerability?
- **Total:** Sum / 5 = Risk score (1-10)

**Checkpoint:** Threat register created with severity ratings

---

### Step 1.4: Create Threat Model Diagram (30 min)

**Diagram Requirements:**
- Architecture diagram with threat annotations
- Trust boundaries highlighted (color-coded)
- Attack vectors marked (arrows with labels)
- Data flow security controls (encryption, validation, auth)

**Tools:**
- draw.io, Lucidchart, Microsoft Threat Modeling Tool
- Or: Annotated screenshots/diagrams in Markdown

**Checkpoint:** Threat model diagram created

---

### 🔒 CHECKPOINT: Phase 1 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 1: Threat Modeling - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Threats Identified:** [N threats]
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

**Methodology Used:** STRIDE

**Files Created:**
- `threat-register.md`
- `threat-model-diagram.png`

**Next Action:** Phase 2 - Design Validation
```

**⚠️ DO NOT PROCEED without completing threat modeling**

---

## Phase 2: Design Validation (2-3 hours)

**Objective:** Validate secure design patterns and security controls

### Step 2.1: Review Authentication Architecture (30 min)

**Validation Checklist:**

**✅ Strong Authentication:**
- [ ] Multi-factor authentication (MFA) enforced for admin accounts
- [ ] Password policies (12+ chars, complexity, rotation)
- [ ] Account lockout after failed attempts (5-10 attempts)
- [ ] Rate limiting on authentication endpoints

**✅ Secure Session Management:**
- [ ] Session tokens cryptographically random (256+ bits)
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)
- [ ] Session timeout (15-30 min idle, 8-12 hours absolute)
- [ ] Token invalidation on logout

**✅ Password Storage:**
- [ ] Strong password hashing (Argon2id, bcrypt, scrypt)
- [ ] Salt per password (no shared salt)
- [ ] No reversible encryption for passwords

**Standards:** OWASP ASVS V2 (Authentication), NIST SP 800-63B

**Findings:** Document weaknesses in findings register

---

### Step 2.2: Review Authorization Architecture (30 min)

**Validation Checklist:**

**✅ Access Control:**
- [ ] Authorization checks on every request (not just authentication)
- [ ] RBAC or ABAC implemented (role-based or attribute-based)
- [ ] Least privilege (users have minimum necessary permissions)
- [ ] No IDOR vulnerabilities (authorization checks per resource)

**✅ Privilege Separation:**
- [ ] Admin functions separated from user functions
- [ ] API keys with scoped permissions (not admin-level keys)
- [ ] Service accounts with minimal permissions

**✅ Enforcement:**
- [ ] Server-side authorization (never trust client)
- [ ] Consistent enforcement (all endpoints, all methods)

**Standards:** OWASP ASVS V4 (Access Control)

**Findings:** Document weaknesses in findings register

---

### Step 2.3: Review Cryptography Architecture (30 min)

**Validation Checklist:**

**✅ Encryption at Rest:**
- [ ] Database encryption (TDE or column-level)
- [ ] File storage encryption (S3 SSE, Azure Storage encryption)
- [ ] Backup encryption
- [ ] Sensitive config encrypted (secrets, API keys)

**✅ Encryption in Transit:**
- [ ] TLS 1.2+ for all external communication (deprecate TLS 1.0/1.1)
- [ ] mTLS for service-to-service communication
- [ ] HTTPS enforced (no HTTP fallback, HSTS header)
- [ ] Certificate validation (no self-signed in production)

**✅ Key Management:**
- [ ] Key management service (AWS KMS, Azure Key Vault, Vault)
- [ ] Key rotation (90 days or less)
- [ ] Separate keys per environment (dev ≠ prod)
- [ ] HSM for high-value keys (optional, FIPS 140-2 Level 3+)

**✅ Crypto Standards:**
- [ ] AES-256-GCM for symmetric encryption (authenticated encryption)
- [ ] RSA-2048+ or ECDSA P-256+ for asymmetric
- [ ] SHA-256 or SHA-3 for hashing (NOT MD5, SHA-1)
- [ ] Argon2id/bcrypt/scrypt for passwords (NOT PBKDF2 with low iterations)

**Standards:** NIST SP 800-175B (Cryptography), OWASP Cryptographic Storage

**Findings:** Document weaknesses in findings register

---

### Step 2.4: Review Data Protection (30 min)

**Validation Checklist:**

**✅ Data Classification:**
- [ ] Data classified (public, internal, confidential, restricted)
- [ ] Handling procedures per classification
- [ ] PII/PHI identified and protected

**✅ Input Validation:**
- [ ] Whitelist validation (allow known good, reject rest)
- [ ] Type checking (string, int, email, UUID)
- [ ] Length limits (prevent buffer overflow, DoS)
- [ ] SQL injection prevention (parameterized queries, ORMs)
- [ ] XSS prevention (output encoding, CSP headers)

**✅ Output Encoding:**
- [ ] HTML entity encoding for user-generated content
- [ ] JSON responses with correct Content-Type
- [ ] Error messages sanitized (no stack traces, sensitive data)

**✅ Data Minimization:**
- [ ] Collect only necessary data
- [ ] Retention policies (delete old data)
- [ ] Data masking in non-production (anonymize PII/PHI)

**Standards:** OWASP ASVS V5 (Validation), OWASP ASVS V8 (Data Protection)

**Findings:** Document weaknesses in findings register

---

### Step 2.5: Review API Security (30 min)

**Validation Checklist:**

**✅ Authentication & Authorization:**
- [ ] API authentication (OAuth 2.0, API keys, JWT)
- [ ] Token expiration (short-lived access tokens, refresh tokens)
- [ ] Scoped permissions (granular OAuth scopes)

**✅ Rate Limiting:**
- [ ] Per-user rate limits (100-1000 requests/min)
- [ ] Per-IP rate limits
- [ ] Endpoint-specific limits (lower for expensive operations)

**✅ Input Validation:**
- [ ] Schema validation (OpenAPI, JSON Schema)
- [ ] Type validation
- [ ] Request size limits (prevent DoS)

**✅ Security Headers:**
- [ ] `Strict-Transport-Security` (HSTS)
- [ ] `Content-Security-Policy` (CSP)
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY`

**Standards:** OWASP API Security Top 10, OWASP ASVS V13 (API)

**Findings:** Document weaknesses in findings register

---

### Step 2.6: Review Secure Design Patterns (30 min)

**Patterns to Validate:**

**✅ Secure by Default:**
- [ ] Deny-by-default (whitelist, not blacklist)
- [ ] Minimal attack surface (unnecessary services disabled)
- [ ] Secure defaults (strong crypto, no default passwords)

**✅ Fail-Secure:**
- [ ] Failure defaults to deny (not grant access)
- [ ] Graceful degradation (maintain security during failures)

**✅ Separation of Duties:**
- [ ] Multi-person approval for critical operations
- [ ] Role segregation (dev ≠ prod access)

**See:** `reference/patterns.md` for complete pattern documentation

**Findings:** Document pattern violations in findings register

---

### 🔒 CHECKPOINT: Phase 2 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 2: Design Validation - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Areas Reviewed:**
- Authentication architecture
- Authorization architecture
- Cryptography architecture
- Data protection
- API security
- Secure design patterns

**Findings Identified:** [N findings]
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

**Files Created:**
- `findings-register.md`
- `design-review-notes.md`

**Next Action:** Phase 3 - Defense-in-Depth Analysis
```

---

## Phase 3: Defense-in-Depth Analysis (2-4 hours)

**Objective:** Evaluate layered security controls and identify single points of failure

### Step 3.1: Map Security Layers (45 min)

**Identify security controls at each layer:**

**Layer 1: Physical**
- Data center security (if on-premises)
- Device security (endpoint protection)

**Layer 2: Network**
- Firewalls (external, internal, host-based)
- IDS/IPS (intrusion detection/prevention)
- Network segmentation (DMZ, VLANs, security groups)
- DDoS protection (CloudFlare, AWS Shield)

**Layer 3: Host**
- OS hardening (CIS benchmarks, DISA STIGs)
- Antivirus/EDR (endpoint detection and response)
- Patch management (automated patching, vulnerability management)

**Layer 4: Application**
- Input validation and output encoding
- Authentication and authorization
- Session management
- WAF (Web Application Firewall)

**Layer 5: Data**
- Encryption at rest
- Encryption in transit
- Access controls (database permissions, file ACLs)
- Data loss prevention (DLP)

**Checkpoint:** Security layers documented

---

### Step 3.2: Identify Single Points of Failure (45 min)

**SPOF Analysis:**

**Questions to ask:**
1. If [component] is compromised, what else is at risk?
2. Can an attacker bypass [control] to access [asset]?
3. What happens if [layer] fails (authentication bypass, network breach)?

**Common SPOFs:**
- **Monolithic authentication** - Single password for all systems
- **No network segmentation** - Flat network (compromise one → access all)
- **No encryption** - Data readable if network breached
- **Single admin account** - No separation of duties
- **No backup authentication** - MFA failure = locked out
- **No redundancy** - Single server, single database

**Validation:**
- [ ] No single control failure = total compromise
- [ ] Multiple independent security layers
- [ ] Redundancy for critical controls (failover, backup)

**Checkpoint:** SPOFs identified

---

### Step 3.3: Evaluate Network Segmentation (45 min)

**Segmentation Analysis:**

**✅ DMZ Architecture:**
- [ ] External firewall (Internet → DMZ)
- [ ] Internal firewall (DMZ → Internal)
- [ ] DMZ hosts minimal (web servers, reverse proxies only)
- [ ] No direct database access from DMZ

**✅ Micro-segmentation:**
- [ ] Security groups per application/service
- [ ] East-west traffic controls (lateral movement prevention)
- [ ] Least privilege network access (only required ports/protocols)

**✅ Security Zones:**
- [ ] Public zone (Internet-facing)
- [ ] Internal zone (corporate network)
- [ ] Restricted zone (sensitive data - databases, PII)
- [ ] Management zone (admin interfaces, jump boxes)

**Standards:** NIST SP 800-125B (Network Segmentation), PCI DSS Req 1

**Findings:** Document segmentation gaps

---

### Step 3.4: Evaluate Monitoring and Detection (45 min)

**Monitoring Validation:**

**✅ Centralized Logging:**
- [ ] SIEM integration (Splunk, Elastic, Sentinel)
- [ ] Log aggregation from all systems
- [ ] Retention (90 days minimum)
- [ ] Tamper-evident logs (write-once storage)

**✅ What's Logged:**
- [ ] Authentication events (login success/failure, MFA, password changes)
- [ ] Authorization events (access granted/denied, privilege escalation)
- [ ] Data access (database queries, file access, especially PII/PHI)
- [ ] Configuration changes (firewall rules, IAM policies)
- [ ] Security events (IDS/IPS alerts, malware detections)

**✅ Real-Time Alerting:**
- [ ] Anomaly detection (UEBA)
- [ ] Threshold alerts (5+ failed logins in 10 min)
- [ ] Correlation rules (SIEM correlation)
- [ ] Incident response integration (PagerDuty, Slack)

**Standards:** NIST SP 800-92 (Log Management), PCI DSS Req 10

**Findings:** Document monitoring gaps

---

### Step 3.5: Validate Fail-Safe Mechanisms (30 min)

**Fail-Safe Validation:**

**Questions to ask:**
1. What happens if authentication service fails?
2. What happens if rate limiting fails?
3. What happens if firewall rules fail to load?
4. What happens if encryption key is unavailable?

**✅ Fail-Secure Design:**
- [ ] Authentication failure → deny access (not grant)
- [ ] Authorization failure → deny access
- [ ] Firewall failure → block traffic (fail-closed)
- [ ] Crypto failure → refuse to process (not store plaintext)

**✅ Graceful Degradation:**
- [ ] Backup authentication (secondary MFA method)
- [ ] Read-only mode (if write operations fail)
- [ ] Circuit breaker (prevent cascade failures)

**Checkpoint:** Fail-safe mechanisms validated

---

### Step 3.6: Create Defense-in-Depth Report (60 min)

**Report Structure:**

**1. Executive Summary**
- Architecture overview
- Security posture (strong/adequate/weak)
- Critical findings (top 3-5)
- Recommendations summary

**2. Defense-in-Depth Analysis**
- Security layers mapped
- Single points of failure identified
- Network segmentation evaluation
- Monitoring and detection assessment
- Fail-safe mechanism validation

**3. Findings Register**
- All findings with severity ratings
- Affected components
- Existing mitigations
- Recommended mitigations
- Standards references (NIST, OWASP, CSA)

**4. Recommendations Roadmap**
- Prioritized list of improvements
- Implementation effort estimates (hours/days)
- Risk reduction impact (high/medium/low)
- Quick wins (low effort, high impact)

**5. Standards Compliance**
- NIST SP 800-160 compliance
- OWASP ASVS verification level
- Regulatory compliance (PCI DSS, HIPAA, if applicable)

**See:** `templates/review-report.md` for complete template

**Checkpoint:** Defense-in-depth report completed

---

### 🔒 CHECKPOINT: Phase 3 Complete

**Update multi-session tracking in `sessions/:**
```markdown
## Phase 3: Defense-in-Depth Analysis - COMPLETE

**Completion:** [YYYY-MM-DD HH:MM]

**Analysis Completed:**
- Security layers mapped
- Single points of failure identified
- Network segmentation evaluated
- Monitoring and detection assessed
- Fail-safe mechanisms validated

**Files Created:**
- `defense-in-depth-report.md`
- `findings-register.md` (updated)
- `recommendations-roadmap.md`

**Next Action:** N/A - Architecture review complete
```

---

## Final Deliverables

**Required outputs:**
1. **Threat Register** - All threats with STRIDE categories, severity ratings
2. **Threat Model Diagram** - Architecture with threat annotations
3. **Findings Register** - All security weaknesses with recommendations
4. **Defense-in-Depth Report** - Complete analysis with standards references
5. **Recommendations Roadmap** - Prioritized improvements with effort estimates
6. **Executive Summary** - High-level overview for stakeholders

**Output Directory:**
```
output/engagements/architecture-reviews/[client]-[YYYY-MM]/
   SCOPE.md
   README.md
   01-discovery/
      architecture-diagrams/
      technical-specs/
   02-threat-modeling/
      threat-register.md
      threat-model-diagram.png
      STRIDE-analysis.md
   03-findings/
      findings-register.md
      design-review-notes.md
   04-compliance/
      NIST-800-160-compliance.md
      OWASP-ASVS-compliance.md
   05-reporting/
      defense-in-depth-report.md
      recommendations-roadmap.md
      executive-summary.md
```

---

## Common Mistakes to Avoid

**❌ Skipping threat modeling**
- Never approve architecture without threat identification

**❌ Generic recommendations**
- Bad: "Implement encryption"
- Good: "Enable TLS 1.2+ for DB connections (currently plaintext) → Implement AWS RDS encryption in transit"

**❌ No prioritization**
- Use severity ratings (Critical/High/Medium/Low)
- Consider business impact, exploitability

**❌ Missing standards references**
- Always cite NIST, OWASP, CSA guidance
- Maintains professional credibility

**❌ No checkpoint documentation**
- Update session file after each phase
- Essential for multi-session reviews

---

## Time Estimates

| Phase | Standard Review | Comprehensive Review |
|---|---|---|
| **Phase 1: Threat Modeling** | 2 hours | 3-4 hours |
| **Phase 2: Design Validation** | 2 hours | 3 hours |
| **Phase 3: Defense-in-Depth** | 2 hours | 4 hours |
| **Total** | **6 hours** | **10-11 hours** |

**Factors affecting time:**
- Architecture complexity (simple web app vs distributed microservices)
- Documentation quality (complete diagrams vs incomplete)
- Threat modeling methodology (STRIDE vs PASTA)
- Compliance requirements (basic vs PCI DSS/HIPAA)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Framework:** NIST SP 800-160, STRIDE, Defense-in-Depth
