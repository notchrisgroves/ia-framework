# Scope Decision Helper: threat-intel vs osint-research

**When to use threat-intel skill vs osint-research skill**

---

## ✅ When to Use threat-intel

Use this skill when you need:

### Structured Threat Data
- CVE research and vulnerability intelligence
- MITRE ATT&CK mapping and technique analysis
- IOC enrichment and indicator analysis
- CISA KEV tracking and active exploitation monitoring
- Exploit availability research (PoC, Metasploit modules)
- CVSS scoring and vulnerability prioritization

### Tactical Intelligence
- Threat actor TACTICS and TTPs (what they do, how they do it)
- Attack campaign technical analysis
- Detection rule development (Sigma, YARA)
- Mitigation strategies for specific techniques
- Defensive security posture improvement

### Technical Depth
- When you need NVD-verified CVE details
- When EPSS scores and exploitability matter
- When you're prioritizing patch management
- When building threat hunt hypotheses

---

## ❌ When to Use osint-research Instead

**Don't use threat-intel for:**
- Non-security research → Use `/osint-research`
- Company/person background checks → Use `/osint-research`
- Competitive intelligence → Use `/osint-research`
- General investigations → Use `/osint-research`
- Pre-engagement reconnaissance (general context) → Use `/osint-research`
- Threat actor CONTEXTUAL information (who they are, history, motivations) → Use `/osint-research`

---

## 🔀 Decision Tree

### Question 1: Is this security/threat-focused?

**NO** → Use osint-research ✅
**YES** → Continue to Question 2

### Question 2: Do you need...

**ANY of these? → threat-intel ✅**
- CVE details?
- MITRE ATT&CK mapping?
- Exploit/IOC data?
- CISA alerts?
- Threat actor TACTICS (how they operate)?

**OR these? → osint-research ✅**
- Person/company background?
- Competitive intelligence?
- General investigation?
- Threat actor CONTEXT (who they are, why they attack)?

---

## Examples

### Use threat-intel ✅

**CVE Research:**
- "Research CVE-2024-1234 for patch priority"
- "Check if CVE-2024-5678 is in CISA KEV catalog"
- "What's the CVSS score for CVE-2024-9999?"
- "Is there a public exploit for CVE-2024-1111?"

**ATT&CK Mapping:**
- "Map ransomware attack to MITRE ATT&CK"
- "What ATT&CK techniques does APT28 use?"
- "Create ATT&CK Navigator layer for this pentest"
- "What detection rules exist for T1003 (credential dumping)?"

**Tactical Threat Actor Intelligence:**
- "Research LockBit's specific TTPs and detection methods"
- "What MITRE ATT&CK techniques does FIN7 use?"
- "How does APT29 maintain persistence?"
- "What tools and malware does Lazarus Group deploy?"

**Vulnerability Prioritization:**
- "Which critical CVEs should we patch first?"
- "Current threats to finance sector (need CVEs/IOCs)"
- "What vulnerabilities are actively exploited right now?"
- "EPSS scores for our critical asset CVEs"

---

### Use osint-research ✅

**General Background:**
- "Research LockBit's history and motivations"
- "Who is behind APT41?"
- "Background on ransomware group REvil"
- "History of FIN7 cybercrime operations"

**Non-Security Research:**
- "Company background check for Acme Corp"
- "Investigate person John Smith from LinkedIn"
- "Competitive intelligence on CompetitorXYZ"
- "General threat landscape overview for finance sector"

**Pre-Engagement Reconnaissance:**
- "General OSINT on target company for pentest scoping"
- "Company structure and subsidiaries research"
- "Technology stack identification (general, no CVEs)"
- "Public data exposure assessment"

---

## Overlap Area: Threat Actors

**When researching threat actors, choose based on WHAT you need:**

### Contextual Information → osint-research ✅
- Who they are (attribution, affiliation)
- Why they attack (motivations, objectives)
- History (past operations, timeline)
- Organizational structure
- Funding sources
- Geopolitical context

### Tactical Information → threat-intel ✅
- What they do (attack types, targets)
- How they operate (TTPs, techniques)
- What tools they use (malware, exploits)
- Detection methods (Sigma rules, IOCs)
- Mitigation strategies (defensive controls)
- MITRE ATT&CK mapping

---

## Quick Reference Table

| Need | threat-intel | osint-research |
|------|--------------|----------------|
| CVE details | ✅ | ❌ |
| CVSS scores | ✅ | ❌ |
| CISA KEV status | ✅ | ❌ |
| Exploit availability | ✅ | ❌ |
| MITRE ATT&CK mapping | ✅ | ❌ |
| IOC enrichment | ✅ | ❌ |
| Detection rules (Sigma, YARA) | ✅ | ❌ |
| Threat actor TTPs | ✅ | ❌ |
| Threat actor background | ❌ | ✅ |
| Company research | ❌ | ✅ |
| Person investigation | ❌ | ✅ |
| Competitive intelligence | ❌ | ✅ |
| General investigation | ❌ | ✅ |

---

## Still Unsure?

**Default Rules:**
1. If it involves CVEs, exploits, or MITRE ATT&CK → threat-intel
2. If it's about people, companies, or general context → osint-research
3. For threat actors: Contextual = osint-research, Tactical = threat-intel
4. When in doubt, ask: "Do I need technical security data or general information?"

---

**See Also:**
- `skills/osint-research/SKILL.md` - General OSINT research capabilities
- `skills/threat-intel/SKILL.md` - Threat intelligence capabilities
- `reference/standards.md` - Threat intelligence frameworks
