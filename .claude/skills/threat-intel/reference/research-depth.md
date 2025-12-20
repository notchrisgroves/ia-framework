# Research Depth Levels

**Time estimates and scope for different threat intelligence engagements**

---

## 1. Standard CVE Research

**Duration:** 15-30 minutes per CVE

**Scope:**
- NIST NVD query for CVE metadata
- CISA KEV check for active exploitation
- Basic CVSS scoring (base score only)
- Patch availability check (vendor advisory)
- Basic mitigation guidance (patch or workaround)

**Deliverables:**
- CVE intelligence summary (1-2 pages)
- Patch recommendation
- Quick risk assessment

**Use Cases:**
- Rapid patch priority decisions
- Vulnerability triage
- Quick impact assessment
- Daily vulnerability monitoring

**Example:**
- User: "Is CVE-2024-12345 in CISA KEV?"
- Research: NVD query + KEV check + CVSS lookup
- Output: KEV status + CVSS score + patch link
- Time: 15 minutes

---

## 2. Comprehensive Threat Intelligence

**Duration:** 2-4 hours per topic

**Scope:**
- Multi-source CVE research (NVD + vendor + exploit databases)
- Threat actor profiling (1-2 actors)
- Attack campaign analysis (1-2 campaigns)
- MITRE ATT&CK mapping (10-20 techniques)
- IOC collection (IP, domain, hash indicators)
- Detection rule creation (Sigma, YARA)
- Detailed remediation roadmap

**Deliverables:**
- CVE intelligence report (5-10 pages per CVE)
- Threat actor profiles (5-10 pages each)
- ATT&CK Navigator layer (JSON)
- Detection rules (Sigma/YARA)
- Remediation roadmap (5-10 pages)

**Use Cases:**
- Incident response support
- Penetration test planning
- Threat hunt hypothesis development
- Security control gap analysis
- Post-breach forensics

**Example:**
- User: "Research APT28's recent campaigns and create ATT&CK mapping"
- Research: Threat actor profiling + campaign analysis + technique mapping
- Output: Actor profile + campaign timeline + ATT&CK layer + detection rules
- Time: 3-4 hours

---

## 3. Strategic Intelligence

**Duration:** 8-16 hours per engagement (may span multiple sessions)

**Scope:**
- Industry landscape analysis (finance, healthcare, government, etc.)
- Emerging threat identification (zero-days, novel techniques)
- Long-term trend analysis (quarterly/annual threat evolution)
- Risk quantification (probability × impact for organization)
- Compliance mapping (PCI DSS, HIPAA, SOC 2, ISO 27001)
- Executive briefing materials
- Multi-year threat forecast

**Deliverables:**
- Industry threat landscape report (20-50 pages)
- Emerging threats analysis (10-15 pages)
- Strategic risk assessment (15-20 pages)
- Executive briefing slides (10-15 slides)
- Compliance gap analysis (10-20 pages)
- 12-month threat forecast

**Use Cases:**
- Annual security strategy planning
- Board-level risk reporting
- Compliance audit support
- Security budget justification
- Threat modeling for new initiatives
- Mergers & acquisitions due diligence

**Example:**
- User: "Provide strategic threat intelligence for finance sector with 2025 forecast"
- Research: Industry analysis + emerging threats + trend analysis + risk quantification
- Output: Comprehensive report + executive briefing + compliance mapping + forecast
- Time: 12-16 hours (multi-session)

---

## Selecting Research Depth

### Quick Decision Matrix

| Scenario | Depth Level | Time |
|----------|-------------|------|
| Daily vulnerability monitoring | Standard | 15-30 min |
| Patch priority decision | Standard | 15-30 min |
| Single CVE deep dive | Comprehensive | 1-2 hours |
| Incident response | Comprehensive | 2-4 hours |
| Threat hunt planning | Comprehensive | 2-4 hours |
| Penetration test scoping | Comprehensive | 2-4 hours |
| Annual security strategy | Strategic | 8-16 hours |
| Board-level reporting | Strategic | 8-16 hours |
| Compliance audit | Strategic | 8-16 hours |

---

### Factors to Consider

**Use Standard CVE Research when:**
- Simple yes/no questions (Is it in KEV? Is there a patch?)
- Time-sensitive patch decisions
- Routine vulnerability management
- Single CVE without context needed

**Use Comprehensive Threat Intelligence when:**
- Incident investigation in progress
- Planning offensive security operations
- Developing threat hunt hypotheses
- Need detection rules and IOCs
- MITRE ATT&CK mapping required
- Multiple CVEs or threat actors involved

**Use Strategic Intelligence when:**
- Annual planning cycles
- Executive/board presentations
- Compliance framework requirements
- Long-term risk assessments
- Industry-wide threat analysis
- Multi-year forecasting needed

---

## Multi-Session Protocol

**For Strategic Intelligence (8-16+ hours):**

**Session 1 (2-3 hours):** Intelligence requirements + CVE research
- Define objectives and scope
- Research critical CVEs
- Create vulnerability prioritization matrix
- **Checkpoint:** Update `sessions/YYYY-MM-DD-project-name.md` (multi-session tracking)

**Session 2 (3-4 hours):** Threat landscape analysis
- Profile threat actors
- Analyze attack campaigns
- Document industry threats
- **Checkpoint:** Update `sessions/YYYY-MM-DD-project-name.md` (multi-session tracking)

**Session 3 (2-3 hours):** ATT&CK mapping + detection
- Map techniques to tactics
- Create Navigator layers
- Develop detection rules
- **Checkpoint:** Update `sessions/YYYY-MM-DD-project-name.md` (multi-session tracking)

**Session 4 (2-3 hours):** Reporting and presentation
- Executive summary
- Technical report
- Remediation roadmap
- Briefing slides
- **Final Checkpoint:** Close `sessions/YYYY-MM-DD-project-name.md` (multi-session tracking)

**See:** `docs/session-checkpoint-enforcement.md` for multi-session protocol

---

**Related:**
- `methodologies/cve-research.md` - CVE research methodology
- `methodologies/threat-landscape.md` - Threat landscape analysis
- `workflows/threat-intelligence.md` - Complete 5-phase workflow
- `docs/session-checkpoint-enforcement.md` - Multi-session checkpoints
