# Benchmark Standards Reference

**Authoritative compliance frameworks for automated script generation**

---

## CIS Benchmarks

**URL:** https://www.cisecurity.org/cis-benchmarks/

**Coverage:** 100+ platform-specific hardening guides

**Structure:**
- **Level 1:** Essential baseline, minimal service disruption
- **Level 2:** Defense-in-depth, may impact functionality

**Common Platforms:**
- Linux: Ubuntu, RHEL, Debian, CentOS, Amazon Linux
- Windows: Windows Server 2019/2022, Windows 10/11
- Cloud: AWS, Azure, GCP
- Databases: MySQL, PostgreSQL, Oracle, SQL Server
- Applications: Docker, Kubernetes, Apache, nginx

**Control Format:**
```
Control ID: X.Y.Z
Title: [Control description]
Profile Applicability: Level 1/2
Description: [Rationale]
Audit: [Commands to check compliance]
Remediation: [Commands to fix non-compliance]
Impact: [Potential service disruption]
Default Value: [Out-of-box configuration]
References: [CVE IDs, vendor docs]
```

---

## DISA STIGs

**URL:** https://public.cyber.mil/stigs/

**Coverage:** DoD security configuration standards

**Severity Categories:**
- **CAT I (Critical):** Immediate exploitation, data loss
- **CAT II (Medium):** Potential exploitation
- **CAT III (Low):** Limited impact

**Common Systems:**
- Operating Systems: RHEL, Windows Server, Ubuntu
- Applications: Apache, IIS, Oracle, SQL Server
- Network: Cisco IOS, Juniper, Palo Alto

**Control Format (STIG ID):**
```
Vuln ID: V-XXXXXX
STIG ID: [System]-XX-XXXXXX
Rule ID: SV-XXXXXX
Severity: CAT I/II/III
Rule Title: [Control description]
Discussion: [Threat explanation]
Check Text: [Manual verification steps]
Fix Text: [Remediation procedure]
CCI: [DoD Control Correlation Identifier]
```

---

## PCI DSS v4.0

**URL:** https://www.pcisecuritystandards.org/

**Requirements (12 categories):**
1. Install and maintain network security controls
2. Apply secure configurations
3. Protect stored account data
4. Protect cardholder data with strong cryptography
5. Protect all systems from malware
6. Develop and maintain secure systems
7. Restrict access to cardholder data
8. Identify users and authenticate access
9. Restrict physical access to cardholder data
10. Log and monitor all access
11. Test security systems regularly
12. Support information security with policies

**Automation Scope:**
- Req 2: Secure configurations (automated validation)
- Req 8: Authentication controls (password policies)
- Req 10: Logging (audit log configuration)

---

## HIPAA Security Rule

**URL:** https://www.hhs.gov/hipaa/for-professionals/security/

**Safeguard Categories:**
- **Administrative (164.308):** Policies, training, risk analysis
- **Physical (164.310):** Facility access, workstation security
- **Technical (164.312):** Access controls, audit controls, encryption

**Automation Focus:**
- Access controls (unique user IDs, automatic logoff)
- Audit controls (audit logging enabled)
- Integrity controls (data validation)
- Transmission security (encryption in transit)

---

## NIST SP 800-53 Rev. 5

**URL:** https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

**Control Families (20 categories):**
- AC (Access Control)
- AU (Audit and Accountability)
- CM (Configuration Management)
- IA (Identification and Authentication)
- SC (System and Communications Protection)

**Automation Examples:**
- AC-2: Account Management (automated user provisioning)
- AU-2: Audit Events (logging configuration)
- CM-6: Configuration Settings (baseline enforcement)

---

## CIS Controls v8

**URL:** https://www.cisecurity.org/controls/v8

**Implementation Groups:**
- **IG1:** Essential cyber hygiene (small organizations)
- **IG2:** Enterprise security (mid-size organizations)
- **IG3:** Advanced security (large organizations)

**18 Controls:**
1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets
5. Account Management
6. Access Control Management
...18. Penetration Testing

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Standards:** CIS, DISA STIG, PCI DSS v4.0, HIPAA, NIST SP 800-53 Rev. 5, CIS Controls v8
