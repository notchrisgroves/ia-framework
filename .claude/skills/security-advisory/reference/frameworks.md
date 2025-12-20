# Security Frameworks Reference

**⚠️ ARCHITECTURE UPDATE:** Frameworks now use multi-location search pattern (2025-11-25)

---

## Multi-Location Search Pattern

**ALL workflows search these locations IN THIS ORDER:**

1. **PRIMARY: Skill Reference** (bundled public frameworks)
   - **Location:** `skills/security-advisory/reference/frameworks/`
   - **Contains:** NIST, CIS, OWASP, HIPAA, PCI-DSS, MITRE ATT&CK
   - **Version controlled:** YES
   - **Setup required:** NO (bundled with skill)

2. **SECONDARY: Professional Reference** (user-added private materials)
   - **Location:** `../../output/reference/`
   - **Contains:** Books, licensed standards (ISO full texts), COBIT, course materials
   - **Version controlled:** NO (see .gitignore)
   - **Setup required:** YES (user adds manually)

3. **FALLBACK: Web Research**
   - **Method:** WebSearch/WebFetch
   - **Requirement:** ALWAYS cite sources

**See:** `../reference/README.md` for complete architecture documentation

---

## PUBLIC Frameworks (Bundled with Skill)

**Location:** `skills/security-advisory/reference/frameworks/`

**Available Frameworks:**

### NIST Publications (Public Domain)
- **NIST Cybersecurity Framework (CSF) 2.0**
  - Functions: Identify, Protect, Detect, Respond, Recover, Govern
  - Use case: General business security posture assessment
  - Path: `reference/frameworks/nist/nist-csf-2.0.pdf`

- **NIST SP 800-53r5** - Security and Privacy Controls
  - Control families and baseline catalogs
  - Use case: Federal compliance, control selection
  - Path: `reference/frameworks/nist/nist-sp-800-53r5.pdf`

- **NIST SP 800-61r3** - Incident Response
  - Incident handling methodology and procedures
  - Use case: Incident response planning and execution
  - Path: `reference/frameworks/nist/nist-sp-800-61r3.pdf`

- **NIST SP 800-30r1** - Risk Assessment
  - Risk assessment methodology
  - Use case: Risk identification and analysis
  - Path: `reference/frameworks/nist/nist-sp-800-30r1.pdf`

### CIS Controls (Freely Available)
- **CIS Controls v8.1.2** (146 pages)
  - 18 security controls with implementation groups
  - Use case: Security baseline configuration
  - Path: `reference/frameworks/cis/cis-controls-v8.1.2.pdf`

### OWASP (Open Source)
- **OWASP ASVS 5.0** - Application Security Verification Standard
  - Web application security requirements
  - Use case: Secure development, application testing
  - Path: `reference/frameworks/owasp/owasp-asvs-5.0.pdf`

- **OWASP Top 10** - Critical security risks
  - Most critical web application security risks
  - Use case: Development guidance, vulnerability awareness
  - Path: `reference/frameworks/owasp/owasp-top-10.pdf`

- **OWASP Testing Guide**
  - Web application penetration testing methodology
  - Use case: Security testing procedures
  - Path: `reference/frameworks/owasp/owasp-testing-guide.pdf`

### HIPAA (Public Law)
- **HIPAA Security Rule** (45 CFR Part 164)
  - Administrative, physical, and technical safeguards
  - Use case: Healthcare compliance assessments
  - Path: `reference/frameworks/hipaa/security-rule.pdf`

### PCI-DSS (Freely Available)
- **PCI-DSS v4.0.1** (443 pages)
  - Payment card security requirements
  - Use case: Merchant compliance, payment processing
  - Path: `reference/frameworks/pci-dss/pci-dss-v4.0.1.pdf`

### MITRE (Public Knowledge Bases)
- **MITRE ATT&CK** - Adversary tactics and techniques
  - Threat modeling and detection engineering
  - Use case: Threat intelligence, security controls mapping
  - Path: `reference/standards/mitre-attack/`

---

## PRIVATE Materials (User-Added)

**Location:** `../../output/reference/`

**User must add manually:**

### ISO Standards (Licensed/Paid)
- **ISO 27001:2022** - Full standard (30 pages)
  - ISMS requirements and controls (Annex A)
  - **Note:** Summaries/excerpts OK in skill, full standard in ../../output/
  - User path: `../../output/reference/iso/iso-27001-2022.pdf`

- **ISO 27002:2022** - Security controls catalog
  - Implementation guidance for Annex A controls
  - User path: `../../output/reference/iso/iso-27002-2022.pdf`

### Books (Copyrighted)
- Security engineering and architecture books
- Penetration testing guides
- Compliance and audit references
- User path: `../../output/reference/books/`

### Proprietary Frameworks
- **COBIT** - ISACA membership required
- **TOGAF** - Open Group membership required
- User path: `../../output/reference/frameworks/`

---

## Framework Selection by Industry

**Workflows automatically load relevant frameworks:**

| Industry | Primary Frameworks | Secondary Frameworks |
|----------|-------------------|---------------------|
| Healthcare | HIPAA Security Rule, NIST 800-66 | ISO 27001, CIS Controls |
| Financial | FFIEC, PCI-DSS, SOX IT controls | NIST CSF, ISO 27001 |
| Retail/E-commerce | PCI-DSS, GDPR/CCPA | NIST CSF, CIS Controls |
| General Business | NIST CSF, CIS Controls | ISO 27001, OWASP |
| Technology/SaaS | SOC 2, ISO 27001 | NIST CSF, CIS Controls |

---

## Usage in Cybersecurity Advisory Workflows

**Phase 2: OSINT Research & Framework Loading**

1. **Identify industry** from client interview
2. **Search PRIMARY** location for public frameworks
3. **Search SECONDARY** location for user-added materials
4. **Fallback to web** if not found locally
5. **Extract controls** applicable to client
6. **Document in deliverables** with citations

**Example: Healthcare Client**

```markdown
1. Load: reference/frameworks/hipaa/security-rule.pdf
2. Check: ../../output/reference/books/hipaa-implementation-guide.pdf
3. WebSearch: Latest HHS guidance on cloud computing
4. Extract: Administrative, physical, technical safeguards
5. Map: HIPAA controls → policy templates
6. Cite: HIPAA Security Rule §164.308(a)(1)(i)
```

---

## Why This Architecture?

**Self-Contained Skills:**
- Share skill → frameworks included
- No manual setup → public frameworks bundled
- Portable → version controlled with skill

**Flexibility:**
- Add private materials → user's choice
- Not version controlled → respects licensing
- Automatic search → workflows find materials

**Similar Pattern:**
- Like benchmarks in `skills/secure-config/`
- Public CIS benchmarks bundled
- Custom benchmarks in ../../output/

---

## Citation Requirements

**ALWAYS cite framework sources:**

**Format:**
```
NIST Cybersecurity Framework v2.0 - Identify Function (ID.AM-1)
```

**Required Elements:**
- Framework name and version
- Section/control reference
- Quote or paraphrase
- Page number (for PDFs)

**Agent Instruction:** "ALWAYS reference the source document directly. NEVER rely on memory or uncited web sources."

---

## Update Schedule

**Framework Updates:**
- **NIST:** Check annually for new/revised publications
- **CIS:** Check quarterly for control updates
- **OWASP:** Check annually (especially Top 10)
- **PCI-DSS:** Check for version releases (currently v4.0.1)
- **HIPAA:** Check when regulations change
- **MITRE ATT&CK:** Check quarterly for new techniques

**Version Pinning:**
- Keep specific versions in filenames (e.g., `nist-csf-2.0.pdf`)
- Maintain legacy versions for historical assessments
- Document version changes in commit messages

---

## Additional Documentation

**Complete Architecture:**
- `../reference/README.md` - Reference materials architecture
- `../SKILL.md` - Complete skill documentation
- `../README.md` - Quick reference

**Related:**
- `README.md` - This directory's purpose and framework mappings
- `framework-policy-mapping.md` - Framework to policy mappings

---

**Last Updated:** 2025-11-25
**Architecture:** Multi-location search pattern (skill → professional → web)
