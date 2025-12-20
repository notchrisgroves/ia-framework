# MITRE ATT&CK Mapping Methodology

**Standardized technique identification and defensive mapping**

---

## ATT&CK Mapping Process

### Step 1: Identify Observed Behavior

**Sources:**
- Security incident logs
- Penetration testing findings
- Malware analysis reports
- Threat intelligence reports
- SIEM alerts and detections

**Behavioral Data:**
- What actions were taken (files created, commands executed, network connections)
- How access was gained (exploit, credential theft, social engineering)
- What persistence mechanisms were used
- What data was accessed or exfiltrated

---

### Step 2: Map to ATT&CK Tactics

**14 ATT&CK Tactics (Adversary Objectives):**
1. Reconnaissance - Gather information about target
2. Resource Development - Establish resources for operations
3. Initial Access - Get into target network
4. Execution - Run malicious code
5. Persistence - Maintain foothold
6. Privilege Escalation - Gain higher-level permissions
7. Defense Evasion - Avoid detection
8. Credential Access - Steal account credentials
9. Discovery - Explore environment
10. Lateral Movement - Move through environment
11. Collection - Gather data of interest
12. Command and Control - Communicate with compromised systems
13. Exfiltration - Steal data
14. Impact - Manipulate, interrupt, or destroy systems

**Tactic Progression Example:**
Initial Access (T1190: Exploit Public-Facing Application) → Execution (T1059: Command and Scripting Interpreter) → Persistence (T1053: Scheduled Task) → Credential Access (T1003: OS Credential Dumping) → Lateral Movement (T1021: Remote Services) → Exfiltration (T1041: Exfiltration Over C2 Channel)

---

### Step 3: Map to ATT&CK Techniques and Sub-Techniques

**Technique Identification:**
- Match observed behavior to specific technique
- Document sub-technique when applicable
- Link to procedure examples from threat actor groups
- Add custom notes for unique variations

**Example Mapping:**
```
Tactic: Initial Access
Technique: T1190 - Exploit Public-Facing Application
Sub-Technique: N/A (no sub-techniques)
Procedure: Exploited CVE-2024-12345 in Apache Struts
Threat Actor: APT41 (known to use this technique)
```

**ATT&CK Matrix Reference:**
- Enterprise ATT&CK: https://attack.mitre.org/matrices/enterprise/
- Technique Database: https://attack.mitre.org/techniques/enterprise/

---

### Step 4: Add Detection Methods

**Detection Guidance:**
For each technique, document:
- Data sources required (process monitoring, network traffic, file monitoring)
- Detection logic (Sigma rules, YARA rules, log queries)
- SIEM queries (Splunk, Elastic, Sentinel)
- EDR detection capabilities

**Example:**
```
Technique: T1003.001 - LSASS Memory Dumping
Detection:
- Data Source: Process Monitoring, File Monitoring
- Sigma Rule: proc_access_win_lsass_dump.yml
- SIEM Query: process.name:"lsass.exe" AND event.code:"10" AND source.process.name:*
- EDR: Alert on MiniDumpWriteDump API calls to lsass.exe
```

---

### Step 5: Document Mitigation Strategies

**Mitigation Guidance:**
For each technique, recommend:
- Preventive controls (disable unnecessary services, patch vulnerabilities)
- Detective controls (logging, monitoring, alerting)
- Corrective controls (incident response procedures)
- Reference official ATT&CK mitigations

**Example:**
```
Technique: T1190 - Exploit Public-Facing Application
Mitigations:
- M1048: Application Isolation and Sandboxing (limit blast radius)
- M1030: Network Segmentation (isolate public-facing apps)
- M1026: Privileged Account Management (minimize service account privileges)
- M1016: Vulnerability Scanning (regular scanning and patching)
- Custom: Deploy WAF with virtual patching for zero-day exposure
```

---

### Step 6: Generate ATT&CK Navigator Layers

**Navigator Layer Creation:**
- Use ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/
- Create JSON layer file with observed techniques
- Color-code by severity or detection coverage
- Export for sharing and visualization

**Layer Types:**
- Red Team Layer - Techniques used during penetration test
- Blue Team Layer - Detection coverage heatmap
- Threat Actor Layer - Known TTPs for specific APT group
- Incident Response Layer - Techniques observed during incident

**JSON Layer Format:**
```json
{
  "name": "Observed Techniques - Client Pentest 2024-12",
  "versions": {
    "attack": "14",
    "navigator": "4.9.1",
    "layer": "4.4"
  },
  "domain": "enterprise-attack",
  "techniques": [
    {
      "techniqueID": "T1190",
      "tactic": "initial-access",
      "color": "#ff6666",
      "comment": "Exploited CVE-2024-12345",
      "enabled": true,
      "score": 9.8
    }
  ]
}
```

---

## Use Cases

1. **Penetration Testing → ATT&CK Mapping**
   - Map pentest findings to techniques
   - Demonstrate attack path to client
   - Provide detection and mitigation guidance

2. **Security Incident Post-Mortem**
   - Reconstruct adversary TTP timeline
   - Identify detection gaps
   - Improve defensive posture

3. **Threat Hunt Hypothesis Development**
   - Select high-risk techniques based on threat intelligence
   - Build hunt queries for each technique
   - Validate detection coverage

4. **Security Control Gap Analysis**
   - Map existing detections to ATT&CK
   - Identify uncovered techniques
   - Prioritize control investments

---

## Deliverables

**ATT&CK Mapping Report includes:**
1. **Technique Inventory** (table with tactic, technique, sub-technique, procedure)
2. **ATT&CK Navigator Layer** (JSON file for visualization)
3. **Detection Guidance** (Sigma rules, SIEM queries, EDR configurations)
4. **Mitigation Recommendations** (prioritized control improvements)
5. **Threat Actor Linkage** (which APT groups use these techniques)

**Time Estimate:**
- Simple mapping (5-10 techniques): 30-45 minutes
- Comprehensive mapping (20-30 techniques): 2-3 hours
- Full incident reconstruction: 4-6 hours

---

**Related:**
- `methodologies/cve-research.md` - CVE research methodology
- `methodologies/threat-landscape.md` - Threat landscape analysis
- `reference/standards.md` - MITRE ATT&CK framework details
- `workflows/threat-intelligence.md` - Complete workflow
