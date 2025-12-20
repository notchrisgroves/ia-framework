---
name: threat-intel
description: Threat intelligence gathering using MITRE ATT&CK, CVE research with NIST NVD/CISA KEV verification, and threat actor profiling for vulnerability prioritization and threat landscape analysis. Use for CVE details, exploit data, attack campaign analysis, and industry-specific threats.
---

# Threat Intelligence Skill

**Auto-loaded when `security` agent invoked for threat intelligence and CVE research**

Specialized in CVE research with NIST NVD/CISA KEV integration, threat actor profiling, attack campaign analysis, and ATT&CK technique mapping with detection/mitigation guidance.

**Core Philosophy:** ATT&CK mapping required. All threat intelligence must map to MITRE ATT&CK tactics/techniques. CVE verification from NVD is mandatory. CISA KEV prioritization ensures focus on real-world threats.

---

## 🚀 Quick Access

**Slash Command:** `/threat-intel`

Threat intelligence research with CVE analysis, threat actor profiling, and MITRE ATT&CK mapping.

**See:** `commands/threat-intel.md` for complete workflow

---

## 🚨 Critical Rules

**Before starting any threat intelligence work:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md
2. **MITRE ATT&CK Mapping Required** - All threat intelligence must map to ATT&CK tactics/techniques (ensures standardized threat communication)
3. **Checkpoint After Intelligence Phase** - Update session file after major phases (CVE research, threat landscape, ATT&CK mapping) with CVEs researched and techniques identified
4. **CVE Verification from NVD** - All CVE intelligence must be verified against NIST NVD, not secondary sources only (ensures accurate vulnerability data)
5. **CISA KEV Prioritization** - Always check CISA KEV catalog for active exploitation (focuses on real-world threats)

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ CVEs researched, refresh rules.

---

## Model Selection

**Reference:** `library/model-selection-matrix.md` for complete task-to-model mapping

**Default:** Latest Sonnet (threat analysis, CVE research, ATT&CK mapping, technical reports)
**Downgrade to Haiku:** Simple CVE lookups, CISA KEV checks
**Upgrade to Opus:** Novel threat pattern analysis, strategic threat landscape assessment
**Research:** Perplexity Sonar-Pro for real-time threat intelligence, latest CVE data

**Dynamic Selection:** `tools/research/openrouter/fetch_models.py` for latest versions

---

## When to Use

✅ **Use threat-intel for:**
- CVE details, CVSS scores, CISA KEV status
- MITRE ATT&CK mapping and technique analysis
- Exploit/IOC data, detection rules (Sigma, YARA)
- Threat actor TACTICS (what they do, how they do it)
- Vulnerability prioritization and patch management
- Attack campaign analysis (timeline, malware, IOCs)
- Industry-specific threats (sector analysis, peer incidents)
- Emerging threats (zero-days, novel techniques, supply chain)

❌ **Don't use if:**
- Company/person background checks → Use `osint-research` skill
- Competitive intelligence, general investigations → Use `osint-research` skill
- Pre-engagement reconnaissance (general context) → Use `osint-research` skill
- Threat actor CONTEXT (who they are, history, motivations) → Use `osint-research` skill

**Overlap (Threat Actors):**
- Contextual (who, why, history) → osint-research
- Tactical (what, how, detection) → threat-intel

---

## Operational Modes

### 1. CVE Research

**8-step vulnerability analysis process**

**Process:**
1. Query NIST NVD for CVE details
2. Calculate CVSS v3.1 scores (base, temporal, environmental)
3. Check CISA KEV catalog for active exploitation
4. Review EPSS probability scores
5. Map to CWE weakness categories
6. Identify affected products and versions
7. Research proof-of-concept availability
8. Document mitigation and patch status

**Deliverables:** CVE intelligence report, exploitability assessment, patch guidance, detection recommendations

**Time:** 15-30 minutes per CVE (standard), 45-60 minutes (deep analysis)

**Methodology:** `methodologies/cve-research.md`

### 2. Threat Landscape Analysis

**Comprehensive threat actor and campaign analysis**

**Coverage:**
- Threat actor profiling (attribution, motivations, TTPs)
- Attack campaign analysis (timeline, malware, IOCs)
- Industry-specific threats (sector analysis, peer incidents)
- Emerging threats (zero-days, novel techniques, supply chain)

**Deliverables:** Threat actor profiles, campaign timelines, industry reports, IOC lists

**Time:** 2-4 hours per engagement

**Methodology:** `methodologies/threat-landscape.md`

### 3. MITRE ATT&CK Mapping

**Standardized technique identification and defensive mapping**

**Process:**
- Map observed behavior to ATT&CK techniques
- Identify tactic progression (Initial Access → Exfiltration)
- Document detection methods (Sigma, YARA, SIEM queries)
- Add mitigation guidance per technique
- Generate ATT&CK Navigator layers (JSON)

**Deliverables:** Technique mappings, Navigator layers, detection rules, mitigation recommendations

**Time:** 1-2 hours (10-20 techniques), 4-6 hours (full incident reconstruction)

**Methodology:** `methodologies/attck-mapping.md`

---

## Workflow: 5-Phase Intelligence Process

**Total Duration:** 6-10 hours for comprehensive threat intelligence engagement

### Phase 1: Intelligence Requirements (30 min)

**Goal:** Define objectives, identify target systems, determine threat actor interest, set research scope

**Deliverables:**
- Objectives and scope documented

**Checkpoint:** Requirements documented

### Phase 2: CVE Research (1-2 hours)

**Goal:** Query NIST NVD, check CISA KEV, research proof-of-concept availability, document patches

**Deliverables:**
- CVE intelligence reports
- Vulnerability prioritization matrix

**Checkpoint:** CVEs researched, KEV status documented, files created

### Phase 3: Threat Landscape Analysis (2-4 hours)

**Goal:** Research attack campaigns, profile threat actors, analyze industry threats, identify emerging vulnerabilities

**Deliverables:**
- Threat actor profiles
- Campaign analysis
- Industry threat reports

**Checkpoint:** Threat landscape documented, actors profiled, files created

### Phase 4: ATT&CK Mapping (1-2 hours)

**Goal:** Map to tactics/techniques, generate Navigator layers, provide detection/mitigation guidance

**Deliverables:**
- Technique mappings
- ATT&CK Navigator JSON
- Detection rules

**Checkpoint:** ATT&CK mapping completed, detection rules created, files created

### Phase 5: Reporting (1-2 hours)

**Goal:** Executive summary, detailed reports, remediation roadmap

**Deliverables:**
- Executive summary
- Technical report
- Remediation roadmap

**Final Checkpoint:** All reports completed, quality assurance passed

---

## Industry Standards

**Primary frameworks:**

- **MITRE ATT&CK** - Adversary behavior framework (tactics, techniques, mitigations)
- **NIST NVD** - National Vulnerability Database (authoritative CVE source)
- **FIRST CVSS v3.1** - Common Vulnerability Scoring System (severity assessment)
- **CISA KEV** - Known Exploited Vulnerabilities catalog (active exploitation tracking)

**Supporting standards:**
- **MITRE CWE** - Common Weakness Enumeration (vulnerability classification)
- **EPSS** - Exploit Prediction Scoring System (exploitability probability)
- **OWASP Top 10** - Web application threat prioritization
- **SANS ISC** - Real-time threat intelligence

**Prioritization Formula:**
```
Priority = (CVSS × 0.4) + (EPSS × 100 × 0.3) + (KEV Status × 10 × 0.3)
```

**Complete reference:** `reference/standards.md`

---

## Research Depth Levels

**Three engagement depths:**

1. **Standard CVE Research** (15-30 min per CVE)
   - Quick lookups for patch decisions
   - NVD + KEV status + CVSS scoring
   - Basic mitigation guidance

2. **Comprehensive Threat Intelligence** (2-4 hours)
   - Full analysis with ATT&CK mapping
   - Threat actor profiling
   - Detection rule development
   - Industry context

3. **Strategic Intelligence** (8-16 hours)
   - Industry landscape analysis
   - Long-term forecasting
   - Executive reporting
   - Annual planning support

**Selection guide:**
- Standard: Daily monitoring, patch decisions
- Comprehensive: Incident response, penetration testing
- Strategic: Annual planning, board reporting

**Complete descriptions:** `reference/research-depth.md`

---

## Output Structure

```
output/engagements/threat-intel/{client}-{YYYY-MM}/
├── 01-cve-research/          (CVE intelligence reports)
├── 02-threat-landscape/      (Threat actor profiles, campaigns)
├── 03-attck-mapping/         (Technique mappings, Navigator layers)
├── 04-iocs/                  (Indicators: CSV, JSON, STIX)
└── 05-reporting/             (Executive summary, final reports)
```

**Integration Formats:**
- STIX 2.1 bundles for TIP platforms
- CSV for SIEM import
- JSON for automation
- Markdown for documentation

**Multi-session tracking:** `sessions/YYYY-MM-DD-project-name.md`

---

## VPS Tool Integration

**cvemap (Kali Pentest Container):**

```python
from servers.kali_pentest.cvemap import cvemap

# Search CVEs by product
result = cvemap.search(
    query="apache struts",
    severity="critical,high",
    limit=20
)
```

**Returns:** CVE IDs, CVSS scores, descriptions, references

**Complete integration:** `reference/vps-tools.md`

---

## CVE Verification Process

**All CVE intelligence must be verified:**

1. **Query NIST NVD:** https://nvd.nist.gov/vuln/search
2. **Verify CVE exists:** CVE-YYYY-##### format, published date
3. **Calculate CVSS v3.1:** Base Score (0.0-10.0)
4. **Check CISA KEV:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog
5. **Review EPSS:** https://www.first.org/epss/ (exploit prediction scoring)
6. **Map to CWE:** Common Weakness Enumeration ID
7. **Search exploits:** Exploit-DB, Metasploit, GitHub
8. **Document patches:** Vendor advisories, patch availability, workarounds

**Never rely on secondary sources only** - always verify against NIST NVD.

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ CVEs researched OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for threat intelligence:
- Context loaded (CLAUDE.md + SKILL.md)
- ATT&CK mapped (tactics/techniques identified)
- Checkpoints maintained (CVEs, ATT&CK, reports documented)
- CVEs verified (NVD validation for all vulnerabilities)
- KEV prioritized (CISA catalog checked for active exploitation)
```

---

## Safety Guardrails

**Citation Requirements:**
- Cite NIST NVD, CISA KEV, vendor advisories
- Include CVE IDs and publication dates
- Link to authoritative sources
- Document research timestamps

**Accuracy:**
- Verify CVE details with multiple sources
- Validate CVSS scores with FIRST calculator
- Cross-check exploitation status
- Clearly mark unconfirmed intelligence

**Scope:**
- Focus on publicly available intelligence
- Avoid speculative attribution
- Follow responsible disclosure for new findings
- Respect confidentiality of client-specific intelligence

---

## Quality Checks (Pre-Delivery)

**Standard CVE research:**
- ✅ CVE intelligence reports (one per CVE)
- ✅ Vulnerability prioritization matrix

**Comprehensive threat intelligence:**
- ✅ Threat actor profiles
- ✅ ATT&CK Navigator layers (JSON)
- ✅ Detection rules (Sigma/YARA)
- ✅ Executive summary and technical report

**All engagements:**
- ✅ All CVEs verified against NIST NVD (not secondary sources)
- ✅ CISA KEV status checked for all CVEs
- ✅ MITRE ATT&CK mapping included (tactics/techniques documented)
- ✅ Detection guidance provided (Sigma, YARA, SIEM queries)
- ✅ Prioritization scores calculated (CVSS + EPSS + KEV)

---

## Progressive Context Loading

**Core Context (Always Loaded):**
- This SKILL.md file

**Extended Context (Load as Needed):**
- `workflows/threat-intelligence.md` - Complete 5-phase workflow
- `methodologies/cve-research.md` - 8-step CVE research process
- `methodologies/threat-landscape.md` - Threat actor and campaign analysis
- `methodologies/attck-mapping.md` - MITRE ATT&CK mapping process
- `templates/cve-research-report.md` - CVE intelligence report template
- `reference/standards.md` - MITRE ATT&CK, NVD, CVSS, CISA KEV, EPSS, CWE frameworks
- `reference/scope-decision-helper.md` - When to use threat-intel vs osint-research
- `reference/output-structure.md` - Directory organization
- `reference/vps-tools.md` - cvemap VPS tool integration
- `reference/research-depth.md` - Research depth levels and time estimates

---

**Version:** 2.0
**Last Updated:** 2025-12-12
**Model:** Claude Sonnet 4.5 (primary), Claude Haiku 4.5 (simple lookups)
**Framework:** MITRE ATT&CK + NIST NVD + CISA KEV + FIRST CVSSv3.1
**Pattern:** Progressive context loading with 5-phase workflow
