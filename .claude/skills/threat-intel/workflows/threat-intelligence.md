---
type: workflow
name: threat-intelligence
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Threat Intelligence Workflow

**Complete 5-phase threat intelligence research process**

---

## Workflow Overview

**5 sequential phases with checkpoints**

1. **Intelligence Requirements** (30 min) - Define objectives, scope, depth
2. **CVE Research** (1-2 hours) - Vulnerability intelligence gathering
3. **Threat Landscape Analysis** (2-4 hours) - Threat actors, campaigns, industry threats
4. **ATT&CK Mapping** (1-2 hours) - Technique identification, detection, mitigation
5. **Reporting** (1-2 hours) - Executive summary, technical reports, recommendations

**Total Time:** 6-10 hours for comprehensive threat intelligence engagement

---

## Phase 1: Intelligence Requirements

**Duration:** 30 minutes

### Objectives

1. **Define Intelligence Objectives**
   - What questions need answering? (What vulnerabilities exist? What threats target us? How do we detect X?)
   - Who is the audience? (CISO, security team, developers, board)
   - What decisions will this intelligence inform? (patch priority, detection investment, risk assessment)

2. **Identify Target Systems/Technologies**
   - Technology stack (OS, frameworks, applications, cloud services)
   - Critical assets (customer data, financial systems, intellectual property)
   - Attack surface (public-facing services, remote access, supply chain)

3. **Determine Threat Actor Interest**
   - Industry sector (finance, healthcare, government, etc.)
   - Geopolitical factors (nation-state interests, sanctions, conflicts)
   - Data value (PII, financial, trade secrets, credentials)
   - Historical targeting (have we been targeted before?)

4. **Set Research Scope and Depth**
   - Standard CVE Research (15-30 min per CVE) - Quick lookups for patch decisions
   - Comprehensive Threat Intelligence (6-10 hours) - Full landscape analysis
   - Strategic Intelligence (multi-week) - Industry trends, long-term threats

### Checkpoint

Update session file with:
- Intelligence objectives documented
- Target systems/technologies identified
- Threat actor interests assessed
- Research scope and depth determined
- Next action: Proceed to Phase 2 (CVE Research)

---

## Phase 2: CVE Research

**Duration:** 1-2 hours (varies by CVE count)

### Process

**For each CVE in scope:**

1. **Query NIST NVD for Vulnerabilities**
   - Search by CVE ID or product/vendor
   - Extract CVE metadata (title, description, dates, references)
   - Document affected products (CPE enumeration)

2. **Cross-Reference CISA KEV Catalog**
   - Check if CVE is in Known Exploited Vulnerabilities catalog
   - If IN KEV: Note due date and required action (HIGHEST PRIORITY)
   - If NOT IN KEV: No active exploitation confirmed (still monitor)

3. **Check EPSS Exploitability Scores**
   - Query EPSS API for probability score (0.0-1.0)
   - Note percentile ranking (e.g., 98th percentile = top 2%)
   - Interpretation: High EPSS (>0.5) = High exploitation likelihood

4. **Research Proof-of-Concept Availability**
   - Search Exploit-DB, GitHub, Packet Storm
   - Check Metasploit modules
   - Document PoC maturity (concept vs weaponized)

5. **Document Affected Versions and Patches**
   - Vendor security advisories
   - Fixed versions available
   - Patch release dates
   - Workarounds if patch unavailable

**Deliverables:**
- CVE intelligence reports (one per CVE)
- Vulnerability prioritization matrix (CVSS + EPSS + KEV status)
- Quick wins list (easy patches, high impact)

### Checkpoint

Update session file with:
- Phase 2 completion status + timestamp
- CVEs researched (count, IDs, CISA KEV status)
- CVE severity scores (Critical/High/Medium/Low counts)
- Files created (CVE reports, prioritization matrix)
- Next action: Proceed to Phase 3 (Threat Landscape Analysis) OR skip to Phase 4 if CVE-only research

---

## Phase 3: Threat Landscape Analysis

**Duration:** 2-4 hours

### Process

1. **Research Recent Attack Campaigns**
   - Identify campaigns targeting similar organizations
   - Campaign timelines and evolution
   - Malware families and tools used
   - IOCs (IP addresses, domains, file hashes)

2. **Profile Relevant Threat Actors**
   - Attribution (nation-state, cybercrime, hacktivist)
   - Motivations and objectives
   - Historical campaigns and targets
   - Known TTPs and toolsets

3. **Analyze Industry-Specific Threats**
   - Sector-specific attack patterns
   - Common vulnerability classes in industry
   - Regulatory and compliance impacts
   - Peer organization incidents (breach disclosures)

4. **Identify Emerging Vulnerabilities**
   - Zero-day vulnerabilities in the wild
   - Newly disclosed critical CVEs
   - Supply chain risks
   - Novel attack techniques

5. **Map to Organizational Risk**
   - Which threats apply to our environment?
   - What's the likelihood of targeting?
   - What's the potential impact?
   - Risk prioritization (likelihood × impact)

**Deliverables:**
- Threat actor profiles (5-10 pages each)
- Attack campaign analysis (10-20 pages)
- Industry threat landscape report (5-10 pages)
- Emerging threats summary (3-5 pages)

### Checkpoint

Update session file with:
- Phase 3 completion status + timestamp
- Threat actors profiled (count, names, attribution)
- Attack campaigns analyzed (count, names)
- Industry threats documented
- Files created (threat landscape report, actor profiles)
- Next action: Proceed to Phase 4 (ATT&CK Mapping)

---

## Phase 4: ATT&CK Mapping

**Duration:** 1-2 hours

### Process

1. **Map Findings to Tactics and Techniques**
   - Review CVEs, campaigns, threat actor TTPs
   - Identify ATT&CK tactics used (Initial Access, Execution, Persistence, etc.)
   - Map to specific techniques (T1190, T1059, T1053, etc.)
   - Document sub-techniques when applicable

2. **Document Sub-Techniques and Procedures**
   - Specific implementation details
   - Procedure examples from threat actors
   - Custom notes for unique variations

3. **Link to Threat Actor TTPs**
   - Which threat actors use these techniques?
   - Historical use in campaigns
   - Technique prevalence by actor type

4. **Generate ATT&CK Navigator Layers**
   - Create JSON layer file
   - Color-code by severity or detection coverage
   - Export for visualization and sharing

5. **Provide Detection and Mitigation Guidance**
   - Detection data sources (process, network, file monitoring)
   - SIEM queries and Sigma rules
   - EDR detection logic
   - Mitigation recommendations (M-codes)

**Deliverables:**
- Technique mappings table (tactic, technique, sub-technique, procedure)
- ATT&CK Navigator layer (JSON file)
- Detection rules (Sigma, YARA, SIEM queries)
- Mitigation recommendations (prioritized)

### Checkpoint

Update session file with:
- Phase 4 completion status + timestamp
- ATT&CK techniques mapped (count, technique IDs)
- Detection rules created (count, types)
- Files created (technique mappings, Navigator layer, detection rules)
- Next action: Proceed to Phase 5 (Reporting)

---

## Phase 5: Reporting

**Duration:** 1-2 hours

### Process

1. **Executive Summary with Key Threats**
   - Top 5-10 threats to organization
   - Risk assessment (likelihood × impact)
   - Strategic recommendations
   - Compliance implications

2. **Detailed CVE Intelligence Reports**
   - All CVE research consolidated
   - Prioritization matrix
   - Patch/mitigation guidance
   - Detection recommendations

3. **Threat Actor Profiles**
   - All profiled actors
   - TTPs and toolsets
   - Historical campaigns
   - Targeting likelihood

4. **ATT&CK Technique Mappings**
   - Technique inventory
   - Detection coverage heatmap
   - Mitigation priorities
   - Control gap analysis

5. **Prioritized Remediation Recommendations**
   - Quick wins (easy patches, high impact)
   - Short-term (0-30 days)
   - Medium-term (30-90 days)
   - Long-term (90+ days)

**Deliverables:**
- Executive summary (2-3 pages)
- Technical threat intelligence report (20-50 pages)
- CVE prioritization matrix (spreadsheet)
- Remediation roadmap (5-10 pages)

### Final Checkpoint

Update session file with:
- Phase 5 completion status + timestamp
- All reports completed (executive, technical, remediation)
- Files created (final deliverables list)
- Next action: N/A (threat intelligence complete)

---

## Output Directory Structure

```
output/engagements/threat-intel/{client}-{YYYY-MM}/
   README.md                          (Intelligence objectives)
   01-cve-research/
      CVE-2024-12345-analysis.md
      kev-catalog-review.md
      vulnerability-prioritization.md
   02-threat-landscape/
      threat-actor-profiles.md
      attack-campaigns.md
      industry-threats.md
   03-attck-mapping/
      technique-mappings.md
      navigator-layers/
         observed-techniques.json
      detection-rules/
   04-iocs/
      indicators.csv                 (IP, domain, hash indicators)
      yara-rules/
   05-reporting/
       executive-summary.md
       threat-intelligence-report.md
       remediation-roadmap.md
```

---

**Related:**
- `methodologies/cve-research.md` - CVE research process (Phase 2 details)
- `methodologies/threat-landscape.md` - Threat landscape analysis (Phase 3 details)
- `methodologies/attck-mapping.md` - ATT&CK mapping process (Phase 4 details)
- `reference/standards.md` - Threat intelligence frameworks
- `reference/output-structure.md` - Directory organization
