# Scope Decision Helper: osint-research vs threat-intel

**When to use osint-research skill vs threat-intel skill**

---

## ✅ When to Use osint-research

Use this skill when you need:

### General Intelligence Gathering
- Research a person, company, or entity (non-security context)
- Competitive intelligence and market analysis
- Pre-engagement reconnaissance (general background)
- Due diligence and background investigations
- Threat actor CONTEXTUAL information (who they are, history, motivations, public reporting)

### Narrative Reports
- Comprehensive dossiers with multiple sources
- Intelligence briefs with strategic context
- Investigation reports with detailed background
- Research that requires synthesis and storytelling

### Dual-Source Verification
- When you need Claude WebSearch + Grok social intelligence
- Cross-validation of findings from multiple angles
- Social media sentiment analysis (X/Twitter via Grok)

---

## ❌ When to Use threat-intel Instead

**Don't use osint-research for:**
- CVE lookups and vulnerability research → Use `/threat-intel`
- MITRE ATT&CK mapping → Use `/threat-intel`
- Exploit availability research → Use `/threat-intel`
- IOC enrichment and threat data → Use `/threat-intel`
- CISA KEV tracking → Use `/threat-intel`
- Threat actor TACTICAL TTPs (what they do, how they do it, detection methods) → Use `/threat-intel`

---

## 🔀 Decision Tree

### Question 1: Is this security/threat-focused?

**NO** → Use osint-research ✅
**YES** → Continue to Question 2

### Question 2: Do you need structured threat data (CVE, MITRE, IOCs)?

**YES** → Use threat-intel ✅
**NO** → Continue to Question 3

### Question 3: Is it about a specific vulnerability or exploit?

**YES** → Use threat-intel ✅
**NO** → Use osint-research ✅

---

## Examples

### Use osint-research ✅

**General Research:**
- "Research competitor's product strategy"
- "Background check on potential hire"
- "Pre-pentest reconnaissance for Acme Corp" (general background, not CVE-specific)
- "What is Acme Corp's technology stack?"

**Threat Actor Context:**
- "Research threat actor LockBit's history and targets" (contextual: who, why, history)
- "What is APT28's organizational structure and funding?"
- "Who are the key members of FIN7 cybercrime group?"
- "What motivates Lazarus Group?"

**Competitive Intelligence:**
- "Market analysis for cybersecurity vendors"
- "Research competitor's pricing strategy"
- "Customer sentiment about CompanyXYZ"

**Pre-Employment:**
- "Research Acme Corp for job application"
- "Company culture at Tech Startup Inc."
- "Employee reviews and glassdoor sentiment"

---

### Use threat-intel ✅

**CVE Research:**
- "Research CVE-2024-1234"
- "Is CVE-2024-5678 in CISA KEV catalog?"
- "What's the CVSS score for this vulnerability?"

**ATT&CK Mapping:**
- "Map ransomware attack to MITRE ATT&CK"
- "What ATT&CK techniques does APT28 use?" (tactical: how they operate)
- "Create ATT&CK Navigator layer for this pentest"

**Threat Actor TTPs:**
- "Map LockBit's TTPs to MITRE ATT&CK" (tactical)
- "What tools and malware does Lazarus Group deploy?" (tactical)
- "How does APT29 maintain persistence?" (tactical)
- "What detection rules exist for FIN7 techniques?" (tactical)

**Vulnerability Intelligence:**
- "Which critical CVEs should we patch first?"
- "Current threats to finance sector (need CVEs/IOCs)"
- "What vulnerabilities are actively exploited right now?"

---

## Overlap Area: Threat Actors

**When researching threat actors, choose based on WHAT you need:**

### Contextual Information → osint-research ✅
- Who they are (attribution, affiliation, members)
- Why they attack (motivations, objectives, funding)
- History (past operations, timeline, evolution)
- Organizational structure and relationships
- Geopolitical context and state sponsorship

### Tactical Information → threat-intel ✅
- What they do (attack types, targets, campaigns)
- How they operate (TTPs, techniques, procedures)
- What tools they use (malware, exploits, infrastructure)
- Detection methods (Sigma rules, IOCs, YARA)
- Mitigation strategies (defensive controls, hardening)
- MITRE ATT&CK mapping and technique analysis

---

## Quick Reference Table

| Need | osint-research | threat-intel |
|------|----------------|--------------|
| Person/company background | ✅ | ❌ |
| Competitive intelligence | ✅ | ❌ |
| Pre-employment research | ✅ | ❌ |
| Pre-pentest reconnaissance (general) | ✅ | ❌ |
| Threat actor context (who/why/history) | ✅ | ❌ |
| Dual-source verification (Claude + Grok) | ✅ | ❌ |
| Social media sentiment | ✅ | ❌ |
| CVE details and CVSS scores | ❌ | ✅ |
| CISA KEV status | ❌ | ✅ |
| Exploit availability | ❌ | ✅ |
| MITRE ATT&CK mapping | ❌ | ✅ |
| IOC enrichment | ❌ | ✅ |
| Detection rules (Sigma, YARA) | ❌ | ✅ |
| Threat actor TTPs (what/how) | ❌ | ✅ |

---

## Still Unsure?

**Default Rules:**
1. If it involves CVEs, exploits, or MITRE ATT&CK → threat-intel
2. If it's about people, companies, or general context → osint-research
3. For threat actors: Contextual (who/why/history) = osint-research, Tactical (what/how/detection) = threat-intel
4. When in doubt, start with osint-research (broader scope). The agent will suggest threat-intel if structured security data is needed.

**Examples to Clarify:**

❓ "Research LockBit ransomware"
- If you want: History, motivations, organizational structure → osint-research ✅
- If you want: TTPs, malware analysis, ATT&CK mapping → threat-intel ✅

❓ "Current threats to healthcare sector"
- If you want: General threat landscape, news, trends → osint-research ✅
- If you want: Specific CVEs, IOCs, detection rules → threat-intel ✅

❓ "Research Acme Corp for pentest"
- If you want: Company background, tech stack, employees → osint-research ✅
- If you want: Known vulnerabilities, CVEs, exploits → threat-intel ✅

---

**See Also:**
- `skills/threat-intel/SKILL.md` - Threat intelligence capabilities
- `reference/intelligence-areas.md` - OSINT intelligence gathering areas
- `methodologies/dual-source-research.md` - Claude + Grok research methodology
