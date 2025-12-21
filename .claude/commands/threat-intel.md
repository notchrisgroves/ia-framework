---
name: threat-intel
description: Threat intelligence with CVE research and MITRE mapping
---

# /threat-intel - Threat Intelligence Research

Threat intelligence gathering using MITRE ATT&CK, CVE research, and CISA KEV for vulnerability prioritization and threat landscape analysis.

**Agent:** security
**Skill:** threat-intel
**Output:** `output/research/threat-intel/{topic}-{YYYY-MM}/`

---

## Quick Start

```
/threat-intel
```

Collects intelligence requirements → Performs threat research → Maps to MITRE ATT&CK → Generates tactical intelligence report

---

## When to Use

✅ **Use /threat-intel when:**
- Research specific CVEs and vulnerability impact
- Track threat actors and their TTPs
- Map attack patterns to MITRE ATT&CK framework
- Prioritize vulnerabilities using CISA KEV
- Analyze threat campaigns or malware families
- Build threat profiles for defensive planning
- Generate tactical intelligence for SOC/incident response

❌ **Don't use if:**
- Need general OSINT/contextual research → use `/osint`
- Need vulnerability scanning → use `/vuln-scan`
- Need penetration testing → use `/pentest`

---

## Workflow

1. **Context Collection** - Prompts gather intelligence requirements, focus area, output format
2. **Intelligence Gathering** - Research CVEs, threat actors, TTPs from authoritative sources
3. **Analysis & Mapping** - Map to MITRE ATT&CK, assess relevance, prioritize threats
4. **Output** - Generate intelligence report in `output/research/threat-intel/{topic}-{YYYY-MM}/`

**Estimated time:** 30-90 minutes

---

## Context Prompts

### Intelligence Type

**Question:** "What type of threat intelligence do you need?"

**Options:**
- **CVE Research** - Specific CVE analysis (impact, exploitability, patches)
- **Threat Actor Profile** - APT groups, cybercriminal orgs, TTPs, targets, motivations
- **Attack Campaign** - Attack campaigns, malware families, threat trends
- **Threat Landscape** - Broad analysis for industry, geography, or technology

**Default:** CVE Research

---

### Research Scope

**Question:** "How will you define the research scope?"

**Options:**
- **Specific CVE(s)** - Provide CVE IDs (e.g., CVE-2024-1234)
- **Technology/Product** - Threats for specific tech (e.g., "Microsoft Exchange")
- **Industry/Sector** - Threats targeting industry (e.g., "Healthcare", "Finance")
- **Threat Actor Name** - Specific APT group (e.g., "APT29", "Lazarus Group")

**Default:** Specific CVE(s)

---

### Intelligence Depth

**Question:** "How comprehensive should the intelligence be?"

**Options:**
- **Quick Brief** - Fast summary (15-30 min), key facts, basic mitigations
- **Standard Report** - Balanced analysis (45-60 min), comprehensive TTPs, MITRE mapping
- **Deep Analysis** - Exhaustive research (90-120 min), timeline reconstruction, detailed attribution

**Default:** Standard Report

---

### MITRE ATT&CK Mapping

**Question:** "Should findings be mapped to MITRE ATT&CK?"

**Options:**
- **Yes - Full Mapping** - Map all TTPs to tactics and techniques (include IDs, sub-techniques, mitigations)
- **Yes - Summary Only** - High-level tactic mapping without detailed techniques
- **No** - Skip MITRE mapping

**Default:** Yes - Full Mapping

---

### Output Format

**Question:** "What output format do you need?"

**Options:**
- **Markdown Report** - Human-readable markdown with sections, tables, links
- **Structured JSON** - Machine-readable JSON for SIEM/TIP/automation
- **Both** - Generate both markdown and JSON (recommended)

**Default:** Markdown Report

---

## Agent Routing

```typescript
Task({
  subagent_type: "security",
  model: "sonnet",
  prompt: `
Mode: threat-intelligence
Skill: threat-intel
Workflow: intelligence-gathering

Context:
- Intelligence Type: {cve-research|threat-actor|attack-campaign|threat-landscape}
- Scope: {cve-ids|technology|industry|threat-actor-name}
- Depth: {quick|standard|deep}
- MITRE Mapping: {full|summary|none}
- Output Format: {markdown|json|both}

Instructions:
Execute threat-intel SKILL.md workflow:
1. Research CVEs/threat actors/TTPs from authoritative sources
2. Map to MITRE ATT&CK framework
3. Assess relevance and prioritize threats
4. Generate intelligence report

Output: output/research/threat-intel/{topic}-{YYYY-MM}/
`
})
```

---

## Output Structure

```
output/research/threat-intel/{topic}-{YYYY-MM}/
├── INTELLIGENCE-SUMMARY.md
├── THREAT-REPORT.md
├── MITRE-MAPPING.md
├── RECOMMENDATIONS.md
├── SOURCES.md
├── data/
│   ├── threat-intel.json
│   ├── mitre-attack.json
│   └── indicators.json
└── evidence/
    ├── cve-details/
    ├── threat-actor-reports/
    └── screenshots/
```

**Deliverables:**

1. **Intelligence Summary** - Key findings, threat level, priority actions, timeline

2. **Threat Report** - Comprehensive analysis, threat actor TTPs, CVE details, attack patterns, IOCs, attribution

3. **MITRE Mapping** (if requested) - ATT&CK tactics/techniques, detection strategies, mitigations

4. **Recommendations** - Defensive mitigations prioritized, patch guidance, detection rules, response playbook

5. **Structured Data** (if JSON requested) - Machine-readable intelligence, STIX/TAXII compatible, IOC formats

---

## Metadata Tracking

**Create `metadata.json` at engagement start:**

```json
{
  "topic": "{topic}",
  "started_at": "YYYY-MM-DDTHH:MM:SS",
  "intel_type": "cve-research|threat-actor|attack-campaign|threat-landscape",
  "scope": "{cve-ids|technology|industry|threat-actor}",
  "depth": "quick|standard|deep",
  "mitre_mapping": "full|summary|none",
  "phase": "context|gathering|analysis|mapping|reporting|complete",
  "cves_analyzed": 0,
  "mitre_techniques": 0
}
```

---

## Examples

### CVE Research

```
/threat-intel
→ Type: CVE Research | Scope: CVE-2024-12345 | Depth: Standard | MITRE: Full

Result: CVE analysis with MITRE ATT&CK, remediation, IOCs (~45-60 min)
Output: output/research/threat-intel/cve-2024-12345-2025-12/
```

### APT Group Profile

```
/threat-intel
→ Type: Threat Actor | Scope: APT29 (Cozy Bear) | Depth: Deep | MITRE: Full

Result: APT profile with TTP analysis, IOCs, defensive strategy (~90-120 min)
Output: output/research/threat-intel/apt29-2025-12/
```

---

## Security & Legal

**Information Sharing:**
- Follow TLP (Traffic Light Protocol)
- Respect source attribution and sharing restrictions
- Comply with information sharing agreements
- Consider GDPR/privacy when sharing IOCs

**Responsible Disclosure:**
- Do not exploit vulnerabilities without authorization
- Follow responsible disclosure practices
- Report new vulnerabilities to vendors first
- Comply with bug bounty program rules

---

## References

**Frameworks:**
- MITRE ATT&CK: attack.mitre.org
- CISA KEV: cisa.gov/known-exploited-vulnerabilities
- NVD: nvd.nist.gov
- STIX/TAXII: oasis-open.org/committees/cti

**Intelligence Cycle:**
1. Planning & Direction (requirements)
2. Collection (sources)
3. Processing (normalization)
4. Analysis (synthesis)
5. Dissemination (reporting)
6. Feedback (iteration)

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
