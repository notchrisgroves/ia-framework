# Security Configuration Standards Reference

**Authoritative standards for infrastructure hardening validation**

---

## CIS Benchmarks

**Organization:** Center for Internet Security (CIS)

**URL:** https://www.cisecurity.org/cis-benchmarks/

**Description:** Consensus-developed secure configuration guidelines for 100+ technologies

### Coverage

**Operating Systems:**
- Linux: Ubuntu, RHEL, Debian, CentOS, Amazon Linux, SUSE, Oracle Linux
- Windows: Windows 10, Windows 11, Windows Server 2016/2019/2022
- Unix: Solaris, AIX, HP-UX
- macOS: macOS 10.15+, macOS 11+, macOS 12+

**Cloud Platforms:**
- AWS: AWS Foundations Benchmark (200+ controls)
- Azure: Azure Foundations Benchmark (150+ controls)
- Google Cloud: GCP Foundations Benchmark (120+ controls)
- Oracle Cloud: Oracle Cloud Infrastructure Benchmark

**Containers & Orchestration:**
- Docker: CIS Docker Benchmark (100+ controls)
- Kubernetes: CIS Kubernetes Benchmark (200+ controls)
- OpenShift: CIS Red Hat OpenShift Container Platform Benchmark

**Databases:**
- MySQL: CIS MySQL Benchmark
- PostgreSQL: CIS PostgreSQL Benchmark
- MongoDB: CIS MongoDB Benchmark
- Oracle Database: CIS Oracle Database Benchmark
- Microsoft SQL Server: CIS SQL Server Benchmark

**Web Servers:**
- Apache HTTP Server: CIS Apache Benchmark
- nginx: CIS nginx Benchmark
- Microsoft IIS: CIS IIS Benchmark
- Apache Tomcat: CIS Tomcat Benchmark

**Network Devices:**
- Cisco IOS: CIS Cisco IOS Benchmark
- Palo Alto Networks: CIS Palo Alto Firewall Benchmark
- Fortinet FortiGate: CIS FortiGate Benchmark
- Juniper: CIS Juniper Benchmark

### Benchmark Structure

**Profile Levels:**
- **Level 1:** Essential baseline hardening (minimal service/functionality disruption)
- **Level 2:** Defense-in-depth hardening (may reduce functionality, assumes dedicated admin)

**Control Format:**
```
Control ID: X.Y.Z (e.g., 5.2.1)
Title: [Control description]
Profile Applicability: Level 1 Server | Level 2 Workstation
Description: [Rationale for control]
Rationale Statement: [Security benefit]
Audit: [Command(s) to check compliance]
Remediation: [Command(s) or procedure to fix]
Impact: [Potential service disruption or functionality loss]
Default Value: [Out-of-box configuration]
References: [CVE IDs, NIST SP 800-53 controls, vendor documentation]
CIS Controls: [Mapping to CIS Controls v8]
```

**Example (CIS Ubuntu 22.04 Benchmark):**
```
5.2.1 Ensure permissions on /etc/ssh/sshd_config are configured (Automated)

Profile Applicability: Level 1 - Server

Description:
The /etc/ssh/sshd_config file contains configuration specifications for sshd.
Incorrect permissions could expose the file to unauthorized access.

Audit:
# stat /etc/ssh/sshd_config
Access: (0600/-rw-------) Uid: (0/root) Gid: (0/root)

Remediation:
# chown root:root /etc/ssh/sshd_config
# chmod 0600 /etc/ssh/sshd_config

Impact: None

Default Value: Access: (0644/-rw-r--r--) Uid: (0/root) Gid: (0/root)
```

### Automation Support

**Automated Tools:**
- **OpenSCAP:** Linux CIS benchmark scanning
- **CIS-CAT Pro:** Commercial tool for CIS benchmark assessment
- **AWS Security Hub:** CIS AWS Foundations automated checks
- **Azure Security Center:** CIS Azure Foundations automated checks
- **Docker Bench:** CIS Docker Benchmark automated checks
- **kube-bench:** CIS Kubernetes Benchmark automated checks

---

## DISA STIGs

**Organization:** Defense Information Systems Agency (DISA)

**URL:** https://public.cyber.mil/stigs/

**Description:** Security Technical Implementation Guides (STIGs) for DoD systems

### Coverage

**Operating Systems:**
- Red Hat Enterprise Linux (RHEL) 7, 8, 9
- Ubuntu 18.04, 20.04, 22.04 LTS
- Windows Server 2016, 2019, 2022
- Windows 10, Windows 11
- Solaris 10, 11

**Applications:**
- Apache HTTP Server 2.4
- Microsoft IIS 10.0
- Oracle Database 12c, 19c
- Microsoft SQL Server 2016, 2019
- PostgreSQL 9.x

**Network Devices:**
- Cisco IOS Router
- Cisco IOS Switch
- Palo Alto NGFW
- F5 BIG-IP LTM
- Juniper SRX

**Virtualization:**
- VMware vSphere 6.x, 7.x
- Microsoft Hyper-V 2016, 2019

### STIG Structure

**Severity Categories:**
- **CAT I (High):** Immediate threat, direct exploitation possible, data loss risk
- **CAT II (Medium):** Potential threat, indirect exploitation, system compromise risk
- **CAT III (Low):** Limited threat, minimal impact, best practice deviation

**Control Format:**
```
Vuln ID: V-XXXXXX (unique vulnerability identifier)
STIG ID: [System]-XX-XXXXXX (e.g., RHEL-08-010010)
Rule ID: SV-XXXXXX (STIG Viewer ID)
Severity: CAT I | CAT II | CAT III
Group Title: [Control category]
Rule Title: [Specific control description]
Discussion: [Detailed explanation of threat]
Check Text: [Manual verification procedure]
Fix Text: [Remediation procedure]
CCI: [Control Correlation Identifier - maps to NIST SP 800-53]
```

**Example (RHEL 8 STIG):**
```
Vuln ID: V-230221
STIG ID: RHEL-08-010010
Rule ID: SV-230221r627750_rule
Severity: CAT II

Rule Title:
RHEL 8 must be a vendor-supported release.

Discussion:
An operating system release is considered "supported" if the vendor continues to
provide security patches for the product. Running an unsupported release may result
in system compromise.

Check Text:
Verify the version of the operating system:
# cat /etc/redhat-release
Red Hat Enterprise Linux release 8.4 (Ootpa)

If the release is not supported by the vendor, this is a finding.

Fix Text:
Upgrade to a supported version of RHEL 8.

CCI: CCI-000366 (NIST SP 800-53 Rev 4: CM-6 b)
```

### Automation Support

**Automated Tools:**
- **OpenSCAP:** DISA STIG SCAP content scanning
- **SCAP Compliance Checker (SCC):** DISA official tool
- **Nessus:** STIG compliance auditing
- **Ansible:** DISA STIG remediation playbooks (Red Hat, Lockdown Enterprise)

---

## NSA/CISA Security Guides

**Organizations:** National Security Agency (NSA) + Cybersecurity and Infrastructure Security Agency (CISA)

**NSA URL:** https://www.nsa.gov/Press-Room/Cybersecurity-Advisories-Guidance/

**CISA URL:** https://www.cisa.gov/cybersecurity-best-practices

**Description:** Government-endorsed hardening guides for critical infrastructure

### Notable Guides

**Kubernetes Hardening Guide (NSA/CISA):**
- URL: https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF
- Coverage: Pod security, network policies, RBAC, secrets management, audit logging
- Application: Kubernetes cluster hardening (government + private sector)

**VMware ESXi Hardening Guide (NSA):**
- URL: https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/3183719/
- Coverage: ESXi host hardening, vCenter security, network isolation, logging
- Application: VMware infrastructure hardening

**Active Directory Security (NSA):**
- URL: https://media.defense.gov/2023/Apr/19/2003203233/-1/-1/0/CSI_LIMITING_ADVERSARY_LATERAL_MOVEMENT_IN_MICROSOFT_AD.PDF
- Coverage: Tiered administration, credential protection, logging, attack detection
- Application: Microsoft Active Directory hardening

**Network Infrastructure Security (CISA):**
- URL: https://www.cisa.gov/sites/default/files/publications/Network_Infrastructure_Security_Guide_508.pdf
- Coverage: Router/switch hardening, network segmentation, monitoring
- Application: Network device hardening (Cisco, Juniper, Palo Alto)

---

## Mozilla SSL Configuration Generator

**Organization:** Mozilla Foundation

**URL:** https://ssl-config.mozilla.org/

**Description:** Best practice TLS/SSL configurations for web servers

### Configuration Profiles

**Modern (Recommended):**
- TLS 1.3 only
- Strong cipher suites (AEAD only: AES-GCM, ChaCha20-Poly1305)
- No legacy client support
- Application: New deployments, modern browsers only

**Intermediate (Balanced):**
- TLS 1.2 + TLS 1.3
- Strong + some compatible cipher suites
- Support for legacy clients (5+ years old)
- Application: Most production deployments

**Old (Legacy):**
- TLS 1.0 + TLS 1.1 + TLS 1.2 + TLS 1.3
- All cipher suites (including weak ciphers)
- Support for very old clients (10+ years old)
- Application: Legacy compatibility requirements only

### Supported Web Servers

- Apache HTTP Server
- nginx
- Microsoft IIS
- HAProxy
- AWS ELB
- Caddy
- Lighttpd

**Example (nginx - Intermediate):**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:MozSSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000" always;
```

---

## NIST Standards

**Organization:** National Institute of Standards and Technology (NIST)

**URL:** https://csrc.nist.gov/publications

### NIST SP 800-123 - Guide to General Server Security

**URL:** https://csrc.nist.gov/publications/detail/sp/800-123/final

**Coverage:** Server baseline security (installation, patching, hardening, monitoring)

**Key Sections:**
- Server security principles
- Installation and deployment
- Secure configuration
- Patch management
- Monitoring and logging

**Application:** Foundation for server hardening programs

### NIST SP 800-70 Rev. 4 - Security Configuration Checklists

**URL:** https://csrc.nist.gov/publications/detail/sp/800-70/rev-4/final

**Coverage:** Methodology for creating and using security configuration checklists

**Key Sections:**
- Checklist development process
- Checklist content requirements (narrative, procedural, template)
- Checklist testing and validation
- SCAP (Security Content Automation Protocol) integration
- National Checklist Program (NCP)

**Application:** Creating custom security baselines

### NIST SP 800-53 Rev. 5 - Security and Privacy Controls

**URL:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

**Coverage:** Comprehensive control catalog (20 families)

**Configuration-Related Control Families:**
- **AC (Access Control):** User accounts, least privilege, remote access
- **CM (Configuration Management):** Baseline configurations, change control
- **IA (Identification and Authentication):** Authentication mechanisms, MFA
- **SC (System and Communications Protection):** Encryption, network security

**Application:** Mapping CIS/STIG controls to NIST framework

---

## Additional Standards

### ISO/IEC 27001/27002

**URL:** https://www.iso.org/isoiec-27001-information-security.html

**Coverage:** Information security management system (ISMS) controls

**Configuration-Related Controls:**
- A.8: Asset Management (inventory, classification)
- A.9: Access Control (user access, privileged accounts)
- A.12: Operations Security (logging, vulnerability management)
- A.13: Communications Security (network security, encryption)

### PCI DSS v4.0

**URL:** https://www.pcisecuritystandards.org/

**Coverage:** Payment Card Industry Data Security Standard

**Configuration-Related Requirements:**
- Requirement 1: Install and maintain network security controls
- Requirement 2: Apply secure configurations to all system components
- Requirement 8: Identify users and authenticate access to system components
- Requirement 10: Log and monitor all access to system components

### HIPAA Security Rule

**URL:** https://www.hhs.gov/hipaa/for-professionals/security/

**Coverage:** Health Insurance Portability and Accountability Act - Technical Safeguards

**Configuration-Related Safeguards:**
- 164.312(a)(1): Access Control (unique user IDs, encryption, automatic logoff)
- 164.312(b): Audit Controls (hardware/software mechanisms to record activity)
- 164.312(c): Integrity Controls (data validation)
- 164.312(d): Person or Entity Authentication (verify identity before access)
- 164.312(e): Transmission Security (encryption for ePHI in transit)

---

## Vendor-Specific Hardening Guides

### Red Hat Enterprise Linux (RHEL)

**URL:** https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/

**Coverage:** RHEL-specific hardening (SELinux, firewalld, FIPS mode)

### Microsoft Windows Server

**URL:** https://learn.microsoft.com/en-us/windows-server/security/security-and-assurance

**Coverage:** Windows Server security baselines, Group Policy hardening

### AWS Well-Architected Framework - Security Pillar

**URL:** https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html

**Coverage:** AWS security best practices (IAM, encryption, network isolation)

### Azure Security Baseline

**URL:** https://learn.microsoft.com/en-us/security/benchmark/azure/

**Coverage:** Azure-specific security controls and configurations

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Standards:** CIS Benchmarks, DISA STIGs, NSA/CISA Guides, Mozilla SSL, NIST (SP 800-123, SP 800-70, SP 800-53)
