# Framework-to-Policy Requirement Mapping
## Intelligent Policy Generation Matrix

**Purpose:** This document maps regulatory frameworks and compliance standards to required security policies, enabling intelligent policy generation that satisfies multiple frameworks with minimal duplication.

**Last Updated:** 2025-10-22
**Version:** 1.0

---

## Framework Coverage

This mapping covers the following frameworks:
- **NIST Cybersecurity Framework (CSF) 2.0**
- **ISO/IEC 27001:2022**
- **CIS Controls v8.1**
- **PCI DSS v4.0.1**
- **HIPAA Security Rule**
- **GLBA (Gramm-Leach-Bliley Act)**
- **SOC 2 (Trust Services Criteria)**
- **NIST SP 800-53 Rev. 5**
- **NIST SP 800-171 Rev. 2** (CUI/CMMC)
- **GDPR** (Data Protection)
- **CCPA/CPRA** (California Privacy)
- **OWASP ASVS 5.0**

---

## Policy Requirement Matrix

### Legend
- ✅ **Required** - Framework explicitly requires this policy
- 🟡 **Recommended** - Framework strongly recommends or implies need
- 🔵 **Optional** - Framework mentions but doesn't mandate
- ⚪ **Not Applicable** - Framework doesn't address this area

---

## Core Governance Policies

### 1. Information Security Policy (Master Policy)

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.PO-1, GV.OC-1, GV.OC-2 |
| ISO 27001:2022 | ✅ Required | Clause 5.2, A.5.1 |
| CIS Controls v8.1 | ✅ Required | Control 1.1, 1.2 (Governance) |
| PCI DSS v4.0.1 | ✅ Required | Req 12.1, 12.2 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(1)(i) |
| GLBA | ✅ Required | Safeguards Rule §314.3 |
| SOC 2 | ✅ Required | CC1.2, CC1.3 |
| NIST 800-53 | ✅ Required | PL-1, PM-1 |
| GDPR | 🟡 Recommended | Art. 24, 32 |
| CCPA/CPRA | 🟡 Recommended | §1798.100(b) |

**Primary Responsibility:** Chief Information Security Officer (CISO) or equivalent
**Update Frequency:** Annual or upon significant organizational change
**Approval Authority:** Board of Directors / Executive Committee

---

### 2. Risk Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.RM-1, GV.RM-2, ID.RA-1 through ID.RA-10 |
| ISO 27001:2022 | ✅ Required | Clause 6.1, A.5.7 |
| CIS Controls v8.1 | ✅ Required | Control 1.5, 4.1, 4.7 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.3 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(1)(ii)(A) |
| GLBA | ✅ Required | Safeguards Rule §314.4(b) |
| SOC 2 | ✅ Required | CC3.2, CC9.1 |
| NIST 800-53 | ✅ Required | RA-1 through RA-10, PM-9 |
| NIST 800-171 | ✅ Required | 3.11.1, 3.11.2 |

**Primary Responsibility:** Chief Risk Officer (CRO) or CISO
**Update Frequency:** Annual minimum, continuous risk assessment
**Key Components:** Risk appetite statement, risk register, risk treatment plans

---

### 3. Access Control / Identity Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.AA-1 through PR.AA-6, PR.AC-1 through PR.AC-7 |
| ISO 27001:2022 | ✅ Required | A.5.15, A.5.16, A.5.17, A.5.18, A.8.2, A.8.3 |
| CIS Controls v8.1 | ✅ Required | Control 5, 6 |
| PCI DSS v4.0.1 | ✅ Required | Req 7, 8 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(3), §164.308(a)(4), §164.312(a)(1) |
| GLBA | ✅ Required | Safeguards Rule §314.4(c) |
| SOC 2 | ✅ Required | CC6.1, CC6.2, CC6.3 |
| NIST 800-53 | ✅ Required | AC-1 through AC-25, IA-1 through IA-12 |
| NIST 800-171 | ✅ Required | 3.1.1 through 3.1.22, 3.5.1 through 3.5.11 |
| GDPR | ✅ Required | Art. 32(1)(b) |

**Primary Responsibility:** Identity & Access Management (IAM) Director
**Key Subpolicies:** Password standards, MFA requirements, role-based access control (RBAC)
**Critical Controls:** Least privilege, separation of duties, regular access reviews

---

### 4. Incident Response Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | RS.MA-1 through RS.MA-5, RS.CO-1 through RS.CO-5, RS.AN-1 through RS.AN-5, RS.MI-1 through RS.MI-3, RC.RP-1, RC.CO-1 through RC.CO-4 |
| ISO 27001:2022 | ✅ Required | A.5.24 through A.5.28 |
| CIS Controls v8.1 | ✅ Required | Control 17 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.10 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(6) |
| GLBA | 🟡 Recommended | Incident Response component of Safeguards |
| SOC 2 | ✅ Required | CC7.3, CC7.4, CC7.5 |
| NIST 800-53 | ✅ Required | IR-1 through IR-10, SI-1 through SI-23 |
| NIST 800-171 | ✅ Required | 3.6.1, 3.6.2, 3.6.3 |
| GDPR | ✅ Required | Art. 33, 34 (Breach Notification) |
| CCPA/CPRA | 🟡 Recommended | Breach notification requirements |

**Primary Responsibility:** Incident Response Manager / SOC Manager
**24/7 Requirement:** Many frameworks require continuous monitoring and response capability
**Key Components:** Detection, containment, eradication, recovery, lessons learned

---

### 5. Data Classification & Protection Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.DS-1 through PR.DS-11, ID.AM-5 |
| ISO 27001:2022 | ✅ Required | A.5.10, A.5.12, A.5.13, A.8.10 through A.8.13 |
| CIS Controls v8.1 | ✅ Required | Control 3, 13 |
| PCI DSS v4.0.1 | ✅ Required | Req 3 (Cardholder Data), Req 9 (Physical Access) |
| HIPAA Security Rule | ✅ Required | §164.308(a)(1), §164.312(a)(2), §164.312(e) |
| GLBA | ✅ Required | Safeguards Rule §314.4(c) |
| SOC 2 | ✅ Required | CC6.6, CC6.7 |
| NIST 800-53 | ✅ Required | MP-1 through MP-8, SC-28 |
| NIST 800-171 | ✅ Required | 3.13.11, 3.13.16 |
| GDPR | ✅ Required | Art. 5, 25, 32 |
| CCPA/CPRA | ✅ Required | §1798.100, §1798.150 |

**Primary Responsibility:** Chief Data Officer (CDO) or Data Protection Officer (DPO)
**Critical Requirement:** Data inventory and classification scheme (Public, Internal, Confidential, Restricted)
**Key Controls:** Encryption at rest/in transit, DLP, data retention/disposal

---

### 6. Business Continuity & Disaster Recovery Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | RC.RP-1, RC.CO-1 through RC.CO-4, GV.SC-6 |
| ISO 27001:2022 | ✅ Required | A.5.29, A.5.30, A.8.14 |
| CIS Controls v8.1 | 🟡 Recommended | Control 11.4, 11.5 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.3.4 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(7) |
| GLBA | 🟡 Recommended | Business continuity component |
| SOC 2 | ✅ Required | A1.2, A1.3 (Availability criteria) |
| NIST 800-53 | ✅ Required | CP-1 through CP-13 |
| NIST 800-171 | 🟡 Recommended | Business continuity guidance |

**Primary Responsibility:** Business Continuity Manager / Disaster Recovery Coordinator
**Critical Metrics:** RTO (Recovery Time Objective), RPO (Recovery Point Objective)
**Testing Requirement:** Most frameworks require annual testing minimum

---

## Technical Security Policies

### 7. Network Security Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.AC-4, PR.AC-5, PR.PT-3, PR.PT-4, DE.CM-1 |
| ISO 27001:2022 | ✅ Required | A.8.20 through A.8.23 |
| CIS Controls v8.1 | ✅ Required | Control 4, 12, 13 |
| PCI DSS v4.0.1 | ✅ Required | Req 1, 2, 11 |
| HIPAA Security Rule | ✅ Required | §164.312(a)(1), §164.312(e) |
| GLBA | ✅ Required | Safeguards Rule network security |
| SOC 2 | ✅ Required | CC6.6, CC6.7, CC7.2 |
| NIST 800-53 | ✅ Required | AC-4, SC-7, SC-8 |
| NIST 800-171 | ✅ Required | 3.1.3, 3.13.1 through 3.13.8 |

**Primary Responsibility:** Network Security Engineer / Network Operations Manager
**Key Components:** Firewall standards, network segmentation, IDS/IPS, VPN
**Critical Controls:** Default deny, network monitoring, secure remote access

---

### 8. Encryption Standard / Cryptographic Controls Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.DS-1, PR.DS-2, PR.DS-5 |
| ISO 27001:2022 | ✅ Required | A.8.24 |
| CIS Controls v8.1 | ✅ Required | Control 3.11, 13.6 |
| PCI DSS v4.0.1 | ✅ Required | Req 3.5, 4.2 |
| HIPAA Security Rule | ✅ Required | §164.312(a)(2)(iv), §164.312(e)(2)(ii) |
| GLBA | ✅ Required | Safeguards Rule encryption requirement |
| SOC 2 | ✅ Required | CC6.7 |
| NIST 800-53 | ✅ Required | SC-12, SC-13, SC-28 |
| NIST 800-171 | ✅ Required | 3.13.11, 3.13.16 |
| GDPR | ✅ Required | Art. 32(1)(a) |

**Primary Responsibility:** Cryptography Officer / Security Architect
**Key Standards:** Approved algorithms (AES-256, RSA-2048+), key management lifecycle
**Critical Requirement:** Key rotation, secure key storage (HSM/KMS)

---

### 9. Vulnerability Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | ID.RA-3, ID.RA-9, PR.IP-12, DE.CM-4, DE.CM-8 |
| ISO 27001:2022 | ✅ Required | A.8.8 |
| CIS Controls v8.1 | ✅ Required | Control 7 |
| PCI DSS v4.0.1 | ✅ Required | Req 6.3, 11.3 |
| HIPAA Security Rule | 🟡 Recommended | §164.308(a)(8) |
| SOC 2 | ✅ Required | CC7.1, CC7.2 |
| NIST 800-53 | ✅ Required | RA-3, RA-5, SI-2 |
| NIST 800-171 | ✅ Required | 3.11.2, 3.14.1 |

**Primary Responsibility:** Vulnerability Management Lead / Security Operations
**SLA Requirements:** Critical (24-48 hrs), High (7-14 days), Medium (30 days), Low (90 days)
**Key Activities:** Continuous scanning, patch management, vulnerability assessments

---

### 10. Logging & Monitoring Policy (Audit Log Management)

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | DE.CM-1 through DE.CM-9, PR.PT-1 |
| ISO 27001:2022 | ✅ Required | A.8.15, A.8.16 |
| CIS Controls v8.1 | ✅ Required | Control 8 |
| PCI DSS v4.0.1 | ✅ Required | Req 10 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(1)(ii)(D), §164.312(b) |
| GLBA | ✅ Required | Safeguards Rule monitoring |
| SOC 2 | ✅ Required | CC7.2, CC8.1 |
| NIST 800-53 | ✅ Required | AU-1 through AU-16 |
| NIST 800-171 | ✅ Required | 3.3.1 through 3.3.9 |
| GDPR | 🟡 Recommended | Art. 32(1)(d) |

**Primary Responsibility:** Security Operations Center (SOC) Manager
**Retention Requirements:** Varies by framework (90 days to 7 years)
**Critical Requirement:** SIEM for centralized log aggregation and correlation

---

### 11. Configuration Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.IP-1, ID.AM-2 |
| ISO 27001:2022 | ✅ Required | A.8.9, A.8.32 |
| CIS Controls v8.1 | ✅ Required | Control 4 |
| PCI DSS v4.0.1 | ✅ Required | Req 2 |
| HIPAA Security Rule | 🟡 Recommended | Configuration baseline |
| SOC 2 | ✅ Required | CC6.6, CC8.1 |
| NIST 800-53 | ✅ Required | CM-1 through CM-14 |
| NIST 800-171 | ✅ Required | 3.4.1 through 3.4.9 |

**Primary Responsibility:** Configuration Manager / IT Operations
**Key Standards:** CIS Benchmarks, DISA STIGs, vendor hardening guides
**Critical Process:** Change control, configuration baseline, drift detection

---

### 12. Mobile Device Management (MDM) Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.AC-1, PR.DS-3 |
| ISO 27001:2022 | ✅ Required | A.6.7, A.8.5 |
| CIS Controls v8.1 | ✅ Required | Control 2.7, 5.6 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.8.3 (if accessing CDE) |
| HIPAA Security Rule | ✅ Required | §164.310(d)(1) (if accessing ePHI) |
| GLBA | 🟡 Recommended | Mobile device security |
| SOC 2 | 🟡 Recommended | Mobile endpoint security |
| NIST 800-53 | ✅ Required | AC-19, AC-20 |
| NIST 800-171 | ✅ Required | 3.1.18, 3.1.19 |

**Primary Responsibility:** Endpoint Security Manager / Mobile Device Administrator
**Key Controls:** Encryption, remote wipe, app whitelisting, containerization
**BYOD Consideration:** Separate policy or addendum for personal device usage

---

### 13. Privileged Access Management (PAM) Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.AA-5, PR.AA-6, PR.AC-4 |
| ISO 27001:2022 | ✅ Required | A.8.2, A.8.3 |
| CIS Controls v8.1 | ✅ Required | Control 5.4, 6.8 |
| PCI DSS v4.0.1 | ✅ Required | Req 7.2, 8.2 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(3)(ii)(A) |
| SOC 2 | ✅ Required | CC6.2, CC6.3 |
| NIST 800-53 | ✅ Required | AC-6, IA-2(1) through IA-2(12) |
| NIST 800-171 | ✅ Required | 3.1.5, 3.1.6 |

**Primary Responsibility:** Privileged Access Manager / IAM Director
**Key Controls:** Just-in-time (JIT) access, session recording, approval workflows
**Critical Requirement:** Dedicated PAM platform (CyberArk, BeyondTrust, etc.)

---

### 14. Cloud Security Policy / Cloud Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.SC-1, GV.SC-3, ID.AM-4 |
| ISO 27001:2022 | ✅ Required | A.5.23 (Cloud services) |
| CIS Controls v8.1 | ✅ Required | Control 15 (Service Provider Management) |
| PCI DSS v4.0.1 | ✅ Required | Req 12.8 (Service Providers) |
| HIPAA Security Rule | ✅ Required | §164.308(b) (Business Associate) |
| SOC 2 | ✅ Required | CC9.2 (Subservice Organizations) |
| NIST 800-53 | ✅ Required | SA-9, SA-10 |
| NIST 800-171 | 🟡 Recommended | Cloud-specific guidance |
| GDPR | ✅ Required | Art. 28 (Processors) |

**Primary Responsibility:** Cloud Security Architect / Cloud Operations Manager
**Key Frameworks:** CSA STAR, FedRAMP for government
**Critical Controls:** CSPM, CASB, cloud-native security (CNAPP)

---

## Operational Policies

### 15. Third-Party Risk Management (TPRM) / Vendor Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.SC-1 through GV.SC-10, ID.AM-4 |
| ISO 27001:2022 | ✅ Required | A.5.19 through A.5.23, A.8.30 |
| CIS Controls v8.1 | ✅ Required | Control 15 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.8, 12.9 |
| HIPAA Security Rule | ✅ Required | §164.308(b)(1), §164.314(a) |
| GLBA | ✅ Required | Safeguards Rule §314.4(d) |
| SOC 2 | ✅ Required | CC9.2 |
| NIST 800-53 | ✅ Required | SA-9, SR-1 through SR-12 |
| NIST 800-171 | ✅ Required | 3.14.1, 3.14.2 |
| GDPR | ✅ Required | Art. 28 (Processor agreements) |

**Primary Responsibility:** Third-Party Risk Manager / Vendor Management Office
**Key Process:** Due diligence, continuous monitoring, SLA management, right to audit
**Critical Requirement:** Vendor risk assessment questionnaire, security addendums

---

### 16. Asset Management Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | ID.AM-1 through ID.AM-7, GV.OC-4 |
| ISO 27001:2022 | ✅ Required | A.5.9, A.5.10, A.5.11 |
| CIS Controls v8.1 | ✅ Required | Control 1, 2 |
| PCI DSS v4.0.1 | 🟡 Recommended | Asset inventory supporting CDE scoping |
| HIPAA Security Rule | 🟡 Recommended | ePHI system inventory |
| SOC 2 | 🟡 Recommended | Asset inventory for security |
| NIST 800-53 | ✅ Required | CM-8, PM-5 |
| NIST 800-171 | ✅ Required | 3.4.1 |

**Primary Responsibility:** IT Asset Manager / CMDB Administrator
**Key Requirement:** CMDB (Configuration Management Database) or asset inventory tool
**Scope:** Hardware, software, data, services, people

---

### 17. Physical Security Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | 🟡 Recommended | PR.AC-2, PR.DS-5 |
| ISO 27001:2022 | ✅ Required | A.7.1 through A.7.14 |
| CIS Controls v8.1 | 🟡 Recommended | Physical access to facilities |
| PCI DSS v4.0.1 | ✅ Required | Req 9 |
| HIPAA Security Rule | ✅ Required | §164.310 (Physical Safeguards) |
| GLBA | 🟡 Recommended | Physical security component |
| SOC 2 | ✅ Required | CC6.4 (Physical access) |
| NIST 800-53 | ✅ Required | PE-1 through PE-23 |
| NIST 800-171 | ✅ Required | 3.10.1 through 3.10.6 |

**Primary Responsibility:** Facilities Manager / Physical Security Manager
**Key Controls:** Badge access, visitor management, CCTV, environmental monitoring
**Sensitive Areas:** Data centers, server rooms, network closets

---

### 18. Security Awareness Training Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.AT-1, GV.AT-2, PR.AT-1 |
| ISO 27001:2022 | ✅ Required | A.6.3 |
| CIS Controls v8.1 | ✅ Required | Control 14 |
| PCI DSS v4.0.1 | ✅ Required | Req 12.6 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(5) |
| GLBA | ✅ Required | Safeguards Rule training |
| SOC 2 | ✅ Required | CC1.4 |
| NIST 800-53 | ✅ Required | AT-1 through AT-6 |
| NIST 800-171 | ✅ Required | 3.2.1, 3.2.2 |
| GDPR | 🟡 Recommended | Training on data protection |

**Primary Responsibility:** Security Awareness Program Manager / Training Manager
**Frequency:** Annual minimum, new hire onboarding, role-based training
**Key Topics:** Phishing, social engineering, password hygiene, data handling

---

### 19. Acceptable Use Policy (AUP)

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | 🟡 Recommended | GV.PO-2, PR.AT-1 |
| ISO 27001:2022 | ✅ Required | A.6.2, A.8.23 |
| CIS Controls v8.1 | 🟡 Recommended | User behavior expectations |
| PCI DSS v4.0.1 | 🟡 Recommended | Supporting access control policies |
| HIPAA Security Rule | 🟡 Recommended | Workforce security |
| SOC 2 | 🟡 Recommended | User responsibilities |
| NIST 800-53 | 🟡 Recommended | PL-4, PS-6 |

**Primary Responsibility:** Human Resources / IT Director
**Key Restrictions:** Personal use, prohibited activities, monitoring notice
**Legal Requirement:** Signed acknowledgment by all users

---

### 20. Password Standard / Authentication Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | PR.AA-1, PR.AA-2 |
| ISO 27001:2022 | ✅ Required | A.5.17, A.5.18 |
| CIS Controls v8.1 | ✅ Required | Control 6 (MFA) |
| PCI DSS v4.0.1 | ✅ Required | Req 8.3, 8.4, 8.5 |
| HIPAA Security Rule | ✅ Required | §164.308(a)(5)(ii)(D) |
| GLBA | ✅ Required | Multi-factor authentication |
| SOC 2 | ✅ Required | CC6.1 |
| NIST 800-53 | ✅ Required | IA-5 |
| NIST 800-171 | ✅ Required | 3.5.7 through 3.5.10 |

**Primary Responsibility:** Identity & Access Management (IAM) Team
**Modern Standard:** Passwordless (FIDO2), MFA required for privileged access
**Complexity:** Follow NIST SP 800-63B (length over complexity)

---

## Industry-Specific Policies

### 21. Privacy Management Policy (GDPR/CCPA)

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| GDPR | ✅ Required | Art. 5, 6, 24, 25, 32 |
| CCPA/CPRA | ✅ Required | §1798.100 through §1798.199 |
| HIPAA Privacy Rule | ✅ Required | 45 CFR Part 160, Subparts A and E |
| ISO 27001:2022 | 🟡 Recommended | A.5.34 (Privacy) |
| SOC 2 | 🟡 Recommended | Privacy criteria (if applicable) |
| NIST Privacy Framework | ✅ Required | Core functions and categories |

**Primary Responsibility:** Data Protection Officer (DPO) / Privacy Officer
**Key Requirements:** Data subject rights, consent management, privacy impact assessments
**Geographic Scope:** EU/EEA (GDPR), California (CCPA), other state laws

---

### 22. AI Governance Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST AI RMF | ✅ Required | GOVERN, MAP, MEASURE, MANAGE functions |
| ISO 42001 | ✅ Required | AI management system requirements |
| NIST CSF 2.0 | 🟡 Recommended | GV.SC (AI as third-party service) |
| EU AI Act | ✅ Required | High-risk AI system requirements |
| GDPR | ✅ Required | Art. 22 (Automated decision-making) |

**Primary Responsibility:** Chief AI Officer / Chief Data Officer
**Key Controls:** Model validation, bias testing, explainability, human oversight
**Emerging Requirement:** Becoming mandatory for organizations using AI/ML

---

### 23. Database Security Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| PCI DSS v4.0.1 | ✅ Required | Req 3, 8 (Database access) |
| HIPAA Security Rule | ✅ Required | §164.312(a), §164.312(e) |
| ISO 27001:2022 | 🟡 Recommended | A.8.10 (Deletion of information) |
| SOC 2 | 🟡 Recommended | Database access controls |
| NIST 800-53 | 🟡 Recommended | SC-28 (Protection at rest) |

**Primary Responsibility:** Database Administrator (DBA) / Data Security Team
**Key Controls:** Encryption, access logging, query monitoring, data masking
**High-Risk Data:** Cardholder data, ePHI, PII

---

### 24. Email Security Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| ISO 27001:2022 | 🟡 Recommended | A.8.5 (Secure authentication) |
| CIS Controls v8.1 | 🟡 Recommended | Control 9.1 (Email protections) |
| PCI DSS v4.0.1 | 🟡 Recommended | Email with cardholder data |
| NIST 800-53 | 🟡 Recommended | SI-8 (Spam protection) |

**Primary Responsibility:** Email Administrator / Messaging Security Team
**Key Controls:** SPF, DKIM, DMARC, anti-phishing, email encryption
**Critical Requirement:** Email gateway security (SEG/ICES)

---

### 25. Internet Usage Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| ISO 27001:2022 | 🟡 Recommended | A.6.2 (Mobile devices) |
| CIS Controls v8.1 | 🟡 Recommended | Web filtering and monitoring |
| PCI DSS v4.0.1 | 🟡 Recommended | Internet access from CDE |

**Primary Responsibility:** IT Security / Network Operations
**Key Controls:** Web filtering, acceptable use, monitoring notice
**Legal Consideration:** User acknowledgment of monitoring

---

### 26. Equipment Disposal / Data Sanitization Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| ISO 27001:2022 | ✅ Required | A.8.10 (Deletion of information) |
| PCI DSS v4.0.1 | ✅ Required | Req 9.8 |
| HIPAA Security Rule | ✅ Required | §164.310(d)(2) |
| NIST 800-53 | ✅ Required | MP-6 |
| NIST 800-171 | ✅ Required | 3.8.3 |
| GDPR | 🟡 Recommended | Right to erasure support |

**Primary Responsibility:** IT Asset Management / Facilities
**Key Standards:** NIST SP 800-88 (Media Sanitization)
**Methods:** Degaussing, cryptographic erasure, physical destruction

---

### 27. Software Management / Secure Software Development Policy

| Framework | Requirement Level | Specific Citations |
|-----------|-------------------|-------------------|
| NIST CSF 2.0 | ✅ Required | GV.SC-4, PR.DS-6 |
| ISO 27001:2022 | ✅ Required | A.8.25 through A.8.32 |
| CIS Controls v8.1 | ✅ Required | Control 16, 18 |
| PCI DSS v4.0.1 | ✅ Required | Req 6 |
| NIST 800-53 | ✅ Required | SA-1 through SA-22 |
| NIST 800-171 | ✅ Required | 3.14.1 through 3.14.7 |
| OWASP ASVS 5.0 | ✅ Required | All verification requirements |

**Primary Responsibility:** Director of Engineering / Application Security Manager
**Key Standards:** OWASP Top 10, SANS Top 25, secure SDLC
**Critical Controls:** SAST, DAST, SCA, code review, security testing

---

## Policy Generation Priority by Industry

### Financial Services (Credit Unions, Banks, Fintech)
**Mandatory Frameworks:** PCI DSS, GLBA, FFIEC, SOC 2, NIST CSF
**Critical Policies (Tier 1):**
1. Information Security Policy
2. Risk Management Policy
3. Access Control / Identity Management
4. Incident Response Policy
5. Data Classification & Protection
6. Third-Party Risk Management
7. Network Security Policy
8. Encryption Standard
9. Logging & Monitoring
10. Vulnerability Management

---

### Healthcare (Hospitals, Clinics, Health Tech)
**Mandatory Frameworks:** HIPAA, HITECH, SOC 2, NIST CSF
**Critical Policies (Tier 1):**
1. Information Security Policy
2. Risk Management Policy
3. Access Control / Identity Management
4. Incident Response Policy
5. Data Classification & Protection (ePHI)
6. Privacy Management Policy
7. Business Continuity & Disaster Recovery
8. Physical Security Policy
9. Third-Party Risk Management (Business Associates)
10. Encryption Standard

---

### Technology / SaaS
**Mandatory Frameworks:** SOC 2, ISO 27001, GDPR (if EU customers), NIST CSF
**Critical Policies (Tier 1):**
1. Information Security Policy
2. Risk Management Policy
3. Access Control / Identity Management
4. Incident Response Policy
5. Secure Software Development
6. Cloud Security Policy
7. Data Classification & Protection
8. Third-Party Risk Management
9. Vulnerability Management
10. Configuration Management

---

### Government Contractors / Defense
**Mandatory Frameworks:** NIST 800-171, CMMC, FedRAMP, NIST 800-53
**Critical Policies (Tier 1):**
1. Information Security Policy
2. Risk Management Policy
3. Access Control / Identity Management
4. Incident Response Policy
5. Data Classification & Protection (CUI)
6. Configuration Management
7. Network Security Policy
8. Physical Security Policy
9. Privileged Access Management
10. Mobile Device Management

---

### Retail / E-commerce
**Mandatory Frameworks:** PCI DSS, GDPR/CCPA (if applicable), NIST CSF
**Critical Policies (Tier 1):**
1. Information Security Policy
2. Risk Management Policy
3. Access Control / Identity Management
4. Incident Response Policy
5. Data Classification & Protection
6. Network Security Policy (PCI focus)
7. Third-Party Risk Management
8. Encryption Standard
9. Vulnerability Management
10. Privacy Management Policy

---

## Policy Overlap Analysis

### High Overlap Policies (Satisfy 8+ Frameworks)
These policies provide maximum ROI by satisfying multiple framework requirements:

1. **Access Control / Identity Management** - 10 frameworks
2. **Incident Response Policy** - 10 frameworks
3. **Data Classification & Protection** - 10 frameworks
4. **Risk Management Policy** - 9 frameworks
5. **Information Security Policy** - 10 frameworks
6. **Third-Party Risk Management** - 10 frameworks
7. **Logging & Monitoring** - 9 frameworks

**Recommendation:** Prioritize these policies first for organizations pursuing multiple certifications.

---

### Medium Overlap Policies (Satisfy 5-7 Frameworks)
Secondary priority policies:

1. **Network Security Policy** - 9 frameworks
2. **Encryption Standard** - 9 frameworks
3. **Vulnerability Management** - 7 frameworks
4. **Configuration Management** - 8 frameworks
5. **Business Continuity & Disaster Recovery** - 7 frameworks
6. **Security Awareness Training** - 9 frameworks

---

### Specialized Policies (Satisfy 1-4 Frameworks)
Industry or framework-specific:

1. **Privacy Management Policy** - GDPR, CCPA, HIPAA specific
2. **AI Governance Policy** - AI-focused organizations
3. **Database Security Policy** - PCI DSS, HIPAA specific
4. **Physical Security Policy** - HIPAA, PCI DSS, ISO specific
5. **Email Security Policy** - Optional/best practice

---

## Usage Guidelines

### For Policy Generation Workflow:
1. **Identify applicable frameworks** based on industry and business requirements
2. **Determine required policies** using the requirement matrix above
3. **Prioritize high-overlap policies** to satisfy multiple frameworks efficiently
4. **Customize policy templates** with organization-specific details
5. **Map framework requirements** into each policy's compliance section
6. **Assign responsibility** based on organizational structure
7. **Validate completeness** against each framework's checklist

### For Multi-Framework Compliance:
- Use the "Framework Compliance Mapping" section in each policy template
- Cite specific requirement numbers for each applicable framework
- Ensure policy controls satisfy the most stringent framework requirement
- Maintain a master compliance matrix showing policy-to-framework coverage

---

**Last Updated:** 2025-10-22
**Maintained By:** Kali / Cybersecurity Advisory Skill
**Next Review:** Quarterly or upon framework updates
