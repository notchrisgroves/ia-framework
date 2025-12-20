# Architecture Security Standards

**Progressive context file - Load when validating architecture against industry standards**

This document covers industry standards, frameworks, and best practices for secure architecture design.

---

## Primary Standards

### NIST SP 800-160 Vol. 1 - Systems Security Engineering

**URL:** https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final

**Coverage:** Comprehensive security engineering framework for trustworthy secure systems

**Key Sections:**
- **Chapter 2:** Systems security engineering fundamentals
- **Chapter 3:** Systems security engineering process (32 tasks across 12 processes)
- **Section 3.4.3:** Threat modeling and vulnerability identification
- **Appendix D:** Security design principles

**Security Design Principles (Appendix D):**
1. **Least Privilege** - Minimal permissions necessary
2. **Fail-Safe Defaults** - Deny by default, allow explicitly
3. **Economy of Mechanism** - Keep design simple
4. **Complete Mediation** - Check every access
5. **Open Design** - Security not dependent on secrecy of design
6. **Separation of Privilege** - Multiple conditions for access
7. **Least Common Mechanism** - Minimize shared resources
8. **Psychological Acceptability** - Easy to use correctly
9. **Defense in Depth** - Layered security controls
10. **Modularity** - Isolated components with defined interfaces

**Application:** Primary framework for ALL architecture security evaluations

---

### OWASP ASVS (Application Security Verification Standard)

**URL:** https://owasp.org/www-project-application-security-verification-standard/

**Current Version:** ASVS 4.0.3 (2021)

**Coverage:** Security requirements for application architectures across 3 verification levels

**Verification Levels:**
- **Level 1 (L1)** - Basic security (all applications, automated testing)
- **Level 2 (L2)** - Standard security (most applications, manual + automated)
- **Level 3 (L3)** - High assurance (critical applications, deep manual review)

**Relevant Architecture Chapters:**

**V1: Architecture, Design and Threat Modeling**
- 1.1 Secure Software Development Lifecycle
- 1.2 Authentication Architecture
- 1.3 Session Management Architecture
- 1.4 Access Control Architecture
- 1.5 Input and Output Architecture
- 1.6 Cryptographic Architecture
- 1.7 Errors, Logging and Auditing Architecture
- 1.8 Data Protection
- 1.9 Communications Architecture
- 1.10 Malicious Software
- 1.11 Business Logic Architecture
- 1.12 Secure File Upload Architecture
- 1.13 API Architecture
- 1.14 Configuration Architecture

**V2: Authentication**
- 2.1 Password Security
- 2.2 General Authenticator Requirements
- 2.5 Credential Recovery
- 2.7 Out of Band Verifier (MFA)
- 2.8 One Time Verifier (OTP, hardware tokens)

**V3: Session Management**
- 3.1 Fundamental Session Management
- 3.2 Session Binding
- 3.3 Session Logout and Timeout
- 3.4 Cookie-based Session Management
- 3.5 Token-based Session Management

**V4: Access Control**
- 4.1 General Access Control Design
- 4.2 Operation Level Access Control
- 4.3 Other Access Control Considerations

**V6: Stored Cryptography**
- 6.1 Data Classification
- 6.2 Algorithms
- 6.4 Secret Management

**V9: Communication**
- 9.1 Client Communication Security
- 9.2 Server Communication Security

**Application:** Security control verification, requirement mapping, compliance validation

---

### CSA Security Guidance for Cloud Computing

**URL:** https://cloudsecurityalliance.org/research/guidance/

**Current Version:** v5.0 (2022)

**Coverage:** Cloud architecture security best practices across 14 domains

**Key Domains for Architecture Review:**

**Domain 1: Cloud Computing Concepts and Architectures**
- Shared responsibility model (IaaS/PaaS/SaaS boundaries)
- Multi-tenancy isolation
- Cloud deployment models (public/private/hybrid/community)

**Domain 2: Governance and Enterprise Risk Management**
- Cloud governance framework
- Risk assessment for cloud architectures

**Domain 3: Legal and Compliance**
- Data sovereignty
- Jurisdiction-specific requirements

**Domain 4: Compliance and Audit**
- Cloud audit framework
- Compliance validation

**Domain 6: Management Plane and Business Continuity**
- Management API security
- Business continuity planning

**Domain 7: Infrastructure Security**
- Network security (VPC, security groups, NACLs)
- Compute security (container, VM isolation)
- Storage security (encryption at rest)

**Domain 8: Virtualization and Containers**
- Hypervisor security
- Container orchestration (Kubernetes security)

**Domain 11: Data Security and Encryption**
- Encryption architecture (KMS, HSM)
- Key management lifecycle

**Domain 12: Identity, Entitlement, and Access Management**
- Cloud IAM architecture
- Federation (SAML, OAuth, OIDC)

**Domain 13: Security as a Service**
- Cloud-native security services

**Domain 14: Related Technologies**
- Serverless security
- IoT security

**Application:** Cloud-specific architecture reviews (AWS, Azure, GCP)

---

### SABSA (Sherwood Applied Business Security Architecture)

**URL:** https://sabsa.org/

**Coverage:** Enterprise security architecture framework (business-driven, risk-based)

**SABSA Matrix (6x6):**
- **Rows:** Contextual (business), Conceptual (architect), Logical (designer), Physical (builder), Component (tradesman), Operational (facility manager)
- **Columns:** Assets, Motivation, Process, People, Location, Time

**Key Concepts:**
- **Business-driven security** - Security objectives aligned to business goals
- **Risk-based architecture** - Threat and risk inform design
- **Layered architecture** - Strategic, tactical, operational layers

**Lifecycle:**
- Strategy & Planning → Design → Implementation → Management & Operations

**Application:** Enterprise architecture reviews, business alignment validation

---

## Supporting Standards

### NIST Cybersecurity Framework (CSF)

**URL:** https://www.nist.gov/cyberframework

**Current Version:** CSF 2.0 (2024)

**Coverage:** Security control mapping across 5 functions

**5 Functions:**
1. **Identify** - Asset management, risk assessment
2. **Protect** - Access control, data security, protective technology
3. **Detect** - Anomaly detection, security monitoring
4. **Respond** - Incident response, communication
5. **Recover** - Recovery planning, improvements

**Application:** Security control mapping, compliance reporting

---

### NIST SP 800-207 - Zero Trust Architecture

**URL:** https://csrc.nist.gov/publications/detail/sp/800-207/final

**Coverage:** Zero trust principles and deployment models

**7 Tenets of Zero Trust:**
1. All data sources and computing services are resources
2. All communication is secured (encrypt all traffic)
3. Access granted per-session (continuous verification)
4. Access determined by dynamic policy (context-aware)
5. Enterprise monitors and measures integrity (continuous monitoring)
6. All resource authentication and authorization are dynamic (re-evaluate constantly)
7. Enterprise collects information to improve security posture (telemetry)

**ZTA Deployment Models:**
- Device agent/gateway-based
- Enclave gateway-based
- Resource portal-based

**Application:** Zero trust architecture validation

---

### MITRE ATT&CK Enterprise Framework

**URL:** https://attack.mitre.org/matrices/enterprise/

**Coverage:** Adversary tactics, techniques, and procedures (TTPs)

**14 Tactics:** Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact

**Application:** Threat-informed architecture design, detection coverage validation

**See:** `methodologies/threat-modeling.md` for ATT&CK-based threat modeling

---

### CIS Controls v8

**URL:** https://www.cisecurity.org/controls/v8

**Coverage:** 18 prioritized security controls across 3 implementation groups

**Implementation Groups:**
- **IG1** - Basic cyber hygiene (small organizations, limited resources)
- **IG2** - Standard security (medium organizations, dedicated security)
- **IG3** - High security (large organizations, mature security programs)

**Relevant Controls for Architecture:**
- **Control 1:** Inventory and Control of Enterprise Assets
- **Control 3:** Data Protection
- **Control 4:** Secure Configuration of Enterprise Assets
- **Control 5:** Account Management
- **Control 6:** Access Control Management
- **Control 8:** Audit Log Management
- **Control 9:** Email and Web Browser Protections
- **Control 12:** Network Infrastructure Management
- **Control 13:** Network Monitoring and Defense

**Application:** Control implementation validation, security baseline

---

### ISO 27001:2022 - Information Security Management

**URL:** https://www.iso.org/standard/27001

**Coverage:** ISMS requirements and security controls (Annex A)

**Annex A Controls (93 controls across 4 themes):**
1. **Organizational (37)** - Policies, asset management, access control, supplier security
2. **People (8)** - Awareness, training, disciplinary process
3. **Physical (14)** - Secure areas, equipment security, environmental controls
4. **Technological (34)** - Cryptography, operations security, network security, secure development

**Relevant Architecture Controls:**
- **A.8.1** - User endpoint devices (secure configuration)
- **A.8.2** - Privileged access rights (least privilege)
- **A.8.3** - Information access restriction (access control)
- **A.8.9** - Configuration management (baseline hardening)
- **A.8.20** - Networks security (segmentation, monitoring)
- **A.8.21** - Security of network services (secure protocols)
- **A.8.24** - Use of cryptography (encryption architecture)

**Application:** ISMS compliance validation

---

### PCI DSS 4.0 - Payment Card Industry Data Security Standard

**URL:** https://www.pcisecuritystandards.org/document_library/

**Coverage:** Security requirements for payment card data protection

**12 Requirements (6 goals):**

**Goal 1: Secure Network**
- Req 1: Install and maintain network security controls (firewalls, segmentation)
- Req 2: Apply secure configurations to all system components

**Goal 2: Protect Account Data**
- Req 3: Protect stored account data (encryption at rest)
- Req 4: Protect cardholder data with strong cryptography during transmission

**Goal 3: Vulnerability Management**
- Req 5: Protect all systems and networks from malicious software
- Req 6: Develop and maintain secure systems and software

**Goal 4: Strong Access Control**
- Req 7: Restrict access to system components and cardholder data by business need to know
- Req 8: Identify users and authenticate access to system components
- Req 9: Restrict physical access to cardholder data

**Goal 5: Monitor and Test Networks**
- Req 10: Log and monitor all access to system components and cardholder data
- Req 11: Test security of systems and networks regularly

**Goal 6: Information Security Policy**
- Req 12: Support information security with organizational policies and programs

**Application:** Payment architecture reviews, cardholder data environment (CDE) validation

---

### HIPAA Security Rule - Healthcare Architecture

**URL:** https://www.hhs.gov/hipaa/for-professionals/security/

**Coverage:** PHI (Protected Health Information) security requirements

**3 Safeguard Categories:**

**Administrative Safeguards**
- Security management process
- Risk analysis and management
- Workforce security

**Physical Safeguards**
- Facility access controls
- Workstation security
- Device and media controls

**Technical Safeguards (Architecture Focus)**
- Access control (unique user IDs, emergency access)
- Audit controls (logging and monitoring)
- Integrity controls (data integrity verification)
- Transmission security (encryption in transit)

**Application:** Healthcare architecture reviews, PHI protection validation

---

## Architecture Patterns

### Secure Architecture Patterns

**1. Zero Trust Architecture**
- Verify explicitly (never trust, always verify)
- Least privilege access (JIT/JEA)
- Assume breach (minimize blast radius)

**2. Defense-in-Depth**
- Multiple security layers (network, host, application, data)
- Independent controls (bypass one ≠ bypass all)
- Fail-secure design

**3. Secure by Default**
- Deny-by-default (whitelist, not blacklist)
- Minimal attack surface (disable unnecessary services)
- Secure defaults (strong crypto, no default passwords)

**4. Separation of Duties**
- Multi-person approval for critical operations
- Role segregation (dev ≠ prod access)
- Privileged access management (PAM)

**5. Encryption Architecture**
- Encryption at rest (database, file storage, backups)
- Encryption in transit (TLS 1.2+, mTLS for service-to-service)
- Key management (HSM, KMS, key rotation)

**6. Secure API Design**
- Authentication (OAuth 2.0, API keys, JWT)
- Authorization (RBAC, ABAC, scopes)
- Rate limiting and throttling
- Input validation and output encoding

**7. Network Segmentation**
- DMZ (demilitarized zone)
- Micro-segmentation (east-west traffic controls)
- Security zones (public, internal, restricted, management)

**8. Secure Logging and Monitoring**
- Centralized logging (SIEM)
- Tamper-evident logs (write-once storage)
- Real-time alerting (anomaly detection)

**See:** `reference/patterns.md` for detailed pattern documentation

---

## Anti-Patterns (Security Mistakes)

**1. Monolithic Authentication**
- Single authentication point for all systems
- No MFA, weak password policies
- **Fix:** Federated identity, SSO with MFA, risk-based auth

**2. Client-Side Security**
- Security logic in client code (JavaScript, mobile apps)
- Trust client input without validation
- **Fix:** Server-side validation, never trust client

**3. Hardcoded Secrets**
- Credentials in code, config files committed to Git
- **Fix:** Secrets management (Vault, AWS Secrets Manager)

**4. Missing Rate Limiting**
- No throttling on authentication, APIs
- Vulnerable to brute force, DDoS
- **Fix:** Rate limiting, CAPTCHA, exponential backoff

**5. Insufficient Logging**
- No audit trail for security events
- Missing logs for authentication, authorization, data access
- **Fix:** Comprehensive security logging, SIEM integration

**6. Trust Boundary Violations**
- Internal network implicitly trusted
- No authentication between microservices
- **Fix:** Zero trust, mTLS for service-to-service, continuous verification

**7. Insecure Direct Object References (IDOR)**
- Direct database IDs in URLs (e.g., `/user/1234`)
- No authorization checks
- **Fix:** Indirect references, authorization checks, UUIDs

**8. Missing Security Headers**
- No HSTS, CSP, X-Frame-Options
- **Fix:** Implement security headers (OWASP Secure Headers)

**See:** `reference/patterns.md` for complete anti-pattern documentation

---

## Compliance Mapping

| Standard | Primary Focus | Architecture Areas |
|---|---|---|
| **NIST SP 800-160** | Systems security engineering | All architecture reviews |
| **OWASP ASVS** | Application security | Web/mobile/API architectures |
| **CSA Guidance** | Cloud security | AWS/Azure/GCP architectures |
| **SABSA** | Enterprise security | Enterprise architecture |
| **NIST CSF** | Security controls | Control mapping, reporting |
| **NIST SP 800-207** | Zero trust | Zero trust validation |
| **MITRE ATT&CK** | Threat intelligence | Threat-informed design |
| **CIS Controls v8** | Security baseline | Control implementation |
| **ISO 27001** | ISMS | Compliance validation |
| **PCI DSS 4.0** | Payment security | Payment architectures |
| **HIPAA Security Rule** | Healthcare security | Healthcare architectures |

---

## Standards Selection Guide

**Q: Which standards should I reference for this architecture review?**

**Default (All Reviews):**
- NIST SP 800-160 (systems security engineering)
- OWASP ASVS (if application architecture)
- Defense-in-depth principles

**Add if Cloud:**
- CSA Cloud Security Guidance
- Cloud provider security best practices (AWS Well-Architected, Azure Security Benchmark, GCP Security Foundations)

**Add if Regulated:**
- PCI DSS (payment card data)
- HIPAA Security Rule (healthcare PHI)
- GDPR (EU personal data)
- SOC 2 (service organization controls)

**Add if High-Risk:**
- NIST SP 800-207 (zero trust)
- MITRE ATT&CK (threat-informed design)
- CIS Controls v8 (hardening baseline)

**Add if Enterprise:**
- SABSA (business-driven architecture)
- ISO 27001 (ISMS compliance)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Primary Standards:** NIST SP 800-160, OWASP ASVS, CSA, SABSA
