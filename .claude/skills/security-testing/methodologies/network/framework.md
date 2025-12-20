
## Methodology Overview

Network penetration testing assesses the security of network infrastructure, systems, and services by simulating real-world attack scenarios using the MITRE ATT&CK Enterprise framework as the tactical baseline.

---

## MITRE ATT&CK Enterprise Matrix Integration

**Discovery:** `Glob: resources/library/**/*mitre*` or `**/*attack*`
**Coverage:** Complete enterprise tactics, techniques, and procedures

### 14 Tactics (Attack Lifecycle)

1. **Reconnaissance** (TA0043) - Gather information for targeting
2. **Resource Development** (TA0042) - Establish resources for operations
3. **Initial Access** (TA0001) - Gain foothold in network
4. **Execution** (TA0002) - Run malicious code
5. **Persistence** (TA0003) - Maintain access
6. **Privilege Escalation** (TA0004) - Gain higher-level permissions
7. **Defense Evasion** (TA0005) - Avoid detection
8. **Credential Access** (TA0006) - Steal credentials
9. **Discovery** (TA0007) - Explore environment
10. **Lateral Movement** (TA0008) - Move through network
11. **Collection** (TA0009) - Gather data of interest
12. **Command and Control** (TA0011) - Communicate with compromised systems
13. **Exfiltration** (TA0010) - Steal data
14. **Impact** (TA0040) - Disrupt/destroy systems

---

## NIST SP 800-115 Testing Phases

**Reference:** https://csrc.nist.gov/publications/detail/sp/800-115/final (use WebFetch)
**Pages:** 80 (split into 10-page chunks)

### Phase 1: Planning
- Define scope and objectives
- Identify target systems and networks
- Establish rules of engagement
- Obtain necessary approvals

### Phase 2: Discovery (Reconnaissance)
- **Active Scanning:** Port scanning, service enumeration
- **Passive Scanning:** Traffic monitoring, OSINT
- **Network Mapping:** Topology discovery, subnet identification
- **Service Identification:** Banner grabbing, version detection

### Phase 3: Attack (Exploitation)
- **Vulnerability Exploitation:** Known CVEs, misconfigurations
- **Password Attacks:** Brute force, password spraying, credential stuffing
- **Social Engineering:** Phishing, pretexting (if in scope)
- **Privilege Escalation:** Local/domain privilege escalation

### Phase 4: Reporting
- Document findings with evidence
- Map to MITRE ATT&CK techniques
- Provide remediation recommendations
- Include executive summary

---

## Network Testing Scope Categories

### Internal Network Penetration Testing

**Objective:** Assess security from inside the network perimeter

**Common Targets:**
- Internal servers (file, database, application)
- Workstations and endpoints
- Network devices (switches, routers, firewalls)
- Internal applications and services
- Active Directory infrastructure
- Wireless networks (if applicable)

**Key Testing Areas:**
- Lateral movement paths
- Domain privilege escalation
- Network segmentation effectiveness
- Sensitive data exposure
- Credential harvesting opportunities

---

### External Network Penetration Testing

**Objective:** Assess security from internet perspective

**Common Targets:**
- Public-facing web servers
- Email servers (SMTP, IMAP, POP3)
- VPN endpoints
- DNS servers
- FTP/SFTP servers
- Remote access services (RDP, SSH)
- Cloud infrastructure endpoints

**Key Testing Areas:**
- External attack surface
- Internet-exposed vulnerabilities
- Remote code execution opportunities
- Authentication bypass
- Information disclosure

---

### Cloud Network Penetration Testing

**Objective:** Assess cloud infrastructure security

**Common Targets:**
- Cloud virtual networks (AWS VPC, Azure VNet, GCP VPC)
- Cloud instances/VMs
- Container orchestration (Kubernetes, ECS, AKS)
- Serverless functions (Lambda, Azure Functions)
- Cloud databases (RDS, CosmosDB, CloudSQL)
- Cloud storage (S3, Blob Storage, Cloud Storage)

**Key Testing Areas:**
- Misconfigurations (security groups, IAM)
- Metadata service abuse
- Cloud-native vulnerabilities
- Cross-account access
- Network segmentation in cloud

---

## MITRE ATT&CK Technique Categories

### Initial Access Techniques (Examples)

**T1133: External Remote Services**
- Test VPN authentication bypass
- Exploit RDP/SSH vulnerabilities
- Weak authentication on remote services

**T1190: Exploit Public-Facing Application**
- Web application vulnerabilities
- SQL injection, RCE
- Unpatched CVEs

**T1566: Phishing** (if social engineering in scope)
- Spear phishing attachments
- Phishing links
- Credential harvesting

**T1078: Valid Accounts**
- Credential stuffing
- Password spraying
- Default credentials

---

### Privilege Escalation Techniques (Examples)

**T1068: Exploitation for Privilege Escalation**
- Kernel exploits
- Sudo misconfigurations
- SUID binaries

**T1078: Valid Accounts**
- Compromised admin credentials
- Service account abuse

**T1543: Create or Modify System Process**
- Windows service manipulation
- Systemd service abuse

---

### Lateral Movement Techniques (Examples)

**T1021: Remote Services**
- RDP lateral movement
- SSH lateral movement
- WinRM/PSRemoting
- SMB/CIFS exploitation

**T1550: Use Alternate Authentication Material**
- Pass-the-Hash
- Pass-the-Ticket
- Kerberos exploitation

**T1570: Lateral Tool Transfer**
- Internal pivoting
- Proxy chains
- Port forwarding

---

### Credential Access Techniques (Examples)

**T1003: OS Credential Dumping**
- LSASS dumping
- SAM database extraction
- /etc/shadow extraction
- Cached credentials

**T1110: Brute Force**
- Password spraying
- Credential stuffing
- Dictionary attacks

**T1555: Credentials from Password Stores**
- Browser credential theft
- Password manager exploitation
- KeePass, LastPass attacks

---

## Testing Methodology Structure

### EXPLORE Phase
1. **Scope Review**
   - Read SCOPE.md engagement requirements
   - Identify network ranges, IP addresses
   - Understand out-of-scope items
   - Clarify testing window and rules

2. **Initial Reconnaissance**
   - Passive OSINT (DNS, WHOIS, Shodan)
   - Active scanning (Nmap, Masscan)
   - Service enumeration
   - Network mapping

3. **MITRE ATT&CK Mapping**
   - Map discovered services to potential techniques
   - Identify likely attack paths
   - Reference framework for technique details

### PLAN Phase
1. **Prioritize Targets**
   - Critical systems identified
   - High-value targets (domain controllers, databases)
   - Easy wins (known vulnerabilities)

2. **Tool Inventory Check** (CRITICAL)
   - Review `/servers` for available tools
   - Check for: Nmap, Metasploit, Impacket, Responder, Bloodhound, etc.
   - Identify missing tools needed for testing
   - Request deployment if gaps exist

3. **Attack Path Planning**
   - Initial access methods
   - Privilege escalation paths
   - Lateral movement routes
   - Credential access opportunities

4. **Test Plan Generation**
   - Map to MITRE ATT&CK techniques
   - Document testing approach per target
   - Include success criteria
   - Get user approval before proceeding

### CODE Phase (Execution)
1. **Initial Access**
   - Execute planned attack vectors
   - Document successful techniques
   - Map to MITRE ATT&CK IDs

2. **Post-Exploitation**
   - Enumerate compromised systems
   - Escalate privileges where possible
   - Harvest credentials
   - Identify lateral movement opportunities

3. **Lateral Movement**
   - Pivot to additional systems
   - Test network segmentation
   - Document access paths

4. **Objective Achievement**
   - Reach testing goals (domain admin, sensitive data, etc.)
   - Document evidence (screenshots, command output)
   - Map all techniques used to MITRE ATT&CK

### COMMIT Phase (Reporting)
1. **Findings Documentation**
   - Executive summary
   - Technical findings with MITRE ATT&CK mapping
   - Evidence (screenshots, logs, exploit code)
   - Attack path diagrams

2. **Remediation Recommendations**
   - Prioritized by risk (critical to low)
   - Specific remediation steps
   - Defense-in-depth suggestions
   - Long-term security improvements

3. **MITRE ATT&CK Integration**
   - Map all successful techniques to ATT&CK IDs
   - Include detection recommendations per technique
   - Reference ATT&CK for defensive controls

---

## Common Network Vulnerabilities

### Network Services
- **Unpatched Services:** Known CVEs in SSH, RDP, SMB, FTP
- **Weak Authentication:** Default credentials, weak passwords
- **Misconfigured Services:** Anonymous FTP, SMB null sessions
- **Outdated Protocols:** SMBv1, TLS 1.0/1.1, SSLv3

### Windows Domain Environment
- **Kerberoasting:** Service account password extraction
- **AS-REP Roasting:** Accounts without Kerberos pre-auth
- **NTLM Relay:** SMB/HTTP NTLM relay attacks
- **Unconstrained Delegation:** Privilege escalation via delegation
- **Zerologon (CVE-2020-1472):** Domain controller exploitation
- **PrintNightmare (CVE-2021-34527):** Print spooler RCE

### Linux/Unix Systems
- **Sudo Misconfigurations:** NOPASSWD, command injection
- **SUID Binaries:** Privilege escalation via SUID
- **Kernel Exploits:** DirtyCow, others based on version
- **Cron Job Abuse:** Writable cron scripts
- **Docker Misconfigurations:** Exposed Docker socket

### Network Infrastructure
- **Default Credentials:** Routers, switches, firewalls
- **SNMP Community Strings:** Public/private exposure
- **Telnet Enabled:** Unencrypted management
- **Weak VPN Configs:** Outdated ciphers, no MFA

---

## Reference Resources

### Local Resources (Dynamic Discovery)

**MITRE ATT&CK:** `Glob: resources/library/**/*mitre*` or `**/*attack*`

**Books:** `Glob: resources/library/books/**/*`
- Network/Red Team: `**/*rtfm*` or `**/*red-team*` or `**/*hacking*` or `**/*python*`

### Web Resources

**MITRE ATT&CK:**
- Website: https://attack.mitre.org/

**NIST SP 800-115:**
- Website: https://csrc.nist.gov/publications/detail/sp/800-115/final
- Guide: Technical Guide to Information Security Testing and Assessment

---

**Created:** 2025-12-01
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Version:** 1.0
