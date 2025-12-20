---
type: template
name: threat-model
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Threat Model - [System Name]

**System:** [System/Application Name]
**Date:** [YYYY-MM-DD]
**Threat Modeling Lead:** [Your Name]
**Methodology:** STRIDE
**Review Status:** [Draft / Review / Final]

---

## System Overview

### System Description

[Brief description of the system, its purpose, and key functionality]

**Business Context:**
- **Sensitivity of Data:** [Public / Internal / Confidential / Restricted]
- **Regulatory Requirements:** [PCI DSS / HIPAA / GDPR / SOC 2 / None]
- **Threat Actor Interest:** [Nation-State / Cybercrime / Insider / Hacktivist / Low]
- **Risk Tolerance:** [High / Medium / Low]

### Technology Stack

- **Frontend:** [Technologies]
- **Backend:** [Technologies]
- **Database:** [Technologies]
- **Infrastructure:** [Cloud/On-Premises/Hybrid]
- **Authentication:** [OAuth 2.0 / SAML / Custom / etc.]
- **APIs:** [REST / GraphQL / gRPC / etc.]

---

## Architecture Decomposition

### Trust Boundaries

**Trust Boundary 1: External (Internet → DMZ)**
- **Description:** Public internet users accessing the system
- **Security Controls:** WAF, DDoS protection, rate limiting, TLS
- **Entry Points:** Web application, REST API, GraphQL endpoint

**Trust Boundary 2: Internal (DMZ → Internal Network)**
- **Description:** Internal systems accessing backend services
- **Security Controls:** Internal firewall, VPN, authentication
- **Entry Points:** Admin portal, internal APIs, database access

**Trust Boundary 3: Privileged (Internal → Sensitive Data)**
- **Description:** Privileged access to sensitive data and systems
- **Security Controls:** MFA, privileged access management, audit logging
- **Entry Points:** Database, key management, admin functions

### Data Flows

| Flow ID | Source | Destination | Data Type | Security Controls | Threats |
|---|---|---|---|---|---|
| DF-001 | User Browser | Web Server | User credentials | HTTPS (TLS 1.2+) | MITM, credential theft |
| DF-002 | Web Server | App Server | Session token | Internal TLS | Session hijacking, tampering |
| DF-003 | App Server | Database | SQL queries | TLS, parameterized queries | SQL injection, data breach |
| DF-004 | App Server | External API | API requests | HTTPS, OAuth 2.0 | Token theft, API abuse |

### Assets

**High-Value Assets:**

| Asset ID | Asset Name | Type | Classification | Owner | Threat Actors Interested |
|---|---|---|---|---|---|
| A-001 | Customer PII Database | Data | Confidential | Data Team | Cybercrime, Nation-State |
| A-002 | Authentication Service | Service | Critical | Security Team | All threat actors |
| A-003 | Payment Processing Module | Service | Restricted | Finance Team | Cybercrime |
| A-004 | API Keys / Secrets | Data | Restricted | Security Team | All threat actors |

**Medium-Value Assets:**
- [Asset name, type, classification]

**Low-Value Assets:**
- [Asset name, type, classification]

### Entry Points

| Entry Point ID | Entry Point | Type | Authentication | Authorization | Rate Limiting | Threats |
|---|---|---|---|---|---|---|
| EP-001 | /login | Web UI | Username/Password | N/A (public) | Yes (10/min) | Brute force, credential stuffing |
| EP-002 | /api/users | REST API | OAuth 2.0 | RBAC | Yes (100/min) | Unauthorized access, data breach |
| EP-003 | /admin | Web UI | Username/Password + MFA | Admin role | Yes (5/min) | Privilege escalation |
| EP-004 | /webhook | REST API | API Key | Scope-based | Yes (1000/min) | API abuse, DoS |

---

## STRIDE Threat Analysis

### Spoofing (Identity Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| S-001 | Attacker impersonates user via stolen credentials | Authentication service, user sessions | High | Password authentication | Implement MFA (TOTP, WebAuthn) | 8.0 |
| S-002 | Session token theft via XSS | Web application, session management | Medium | HttpOnly cookies | Implement CSP headers, output encoding | 6.0 |
| S-003 | API key stolen from client code | Mobile app, REST API | High | API key authentication | Move API key to backend, use OAuth 2.0 | 7.5 |

### Tampering (Data Integrity Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| T-001 | MITM attack on database connection | App server → Database | Critical | None | Enable TLS for database connections | 9.0 |
| T-002 | SQL injection via user input | REST API, database | High | None | Implement parameterized queries, input validation | 8.5 |
| T-003 | Request tampering via proxy | REST API | Medium | HTTPS | Implement request signing (HMAC) | 5.5 |

### Repudiation (Logging/Audit Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| R-001 | User denies account changes | User management, audit logging | Medium | Basic logging | Implement comprehensive audit logging (who, what, when, where) | 5.0 |
| R-002 | No audit trail for admin actions | Admin portal | High | None | Implement admin action logging with tamper-evident storage | 7.0 |
| R-003 | Missing data access logs | Database, PII access | High | None | Implement database query logging for PII tables | 7.5 |

### Information Disclosure (Confidentiality Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| I-001 | API returns full user objects including PII | REST API | Critical | None | Implement response filtering (only required fields) | 9.0 |
| I-002 | Database backups not encrypted | Backup system | High | None | Enable backup encryption (AES-256) | 8.0 |
| I-003 | Verbose error messages expose stack traces | Web application, API | Low | None | Sanitize error messages (generic errors in production) | 3.0 |
| I-004 | No encryption at rest for PII | Database | Critical | None | Enable TDE (Transparent Data Encryption) | 9.5 |

### Denial of Service (Availability Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| D-001 | No rate limiting on authentication endpoint | /login endpoint | High | None | Implement rate limiting (10 attempts/min/IP) | 7.0 |
| D-002 | Resource exhaustion via large file uploads | File upload API | Medium | None | Implement file size limits (10MB), virus scanning | 6.0 |
| D-003 | Single database instance (no failover) | Database | High | None | Implement database replication (primary + replica) | 7.5 |

### Elevation of Privilege (Authorization Threats)

| Threat ID | Description | Affected Components | Severity | Existing Mitigations | Recommended Mitigations | Risk Score |
|---|---|---|---|---|---|---|
| E-001 | IDOR allows access to other users' data | REST API (/api/users/{id}) | Critical | None | Implement authorization checks (verify ownership) | 9.0 |
| E-002 | No authorization checks on admin endpoints | Admin API | Critical | None | Implement role-based authorization (admin role required) | 9.5 |
| E-003 | Privilege escalation via parameter tampering | User management | High | None | Server-side role validation (never trust client input) | 8.0 |

---

## Threat Prioritization

### Critical Threats (Immediate Action Required)

1. **T-001** - MITM on database connection (9.0) → Enable database TLS
2. **I-001** - API leaks PII (9.0) → Implement response filtering
3. **I-004** - No encryption at rest for PII (9.5) → Enable TDE
4. **E-001** - IDOR vulnerability (9.0) → Add authorization checks
5. **E-002** - No admin authorization (9.5) → Implement RBAC

### High Threats (Implement Within 30 Days)

6. **S-001** - No MFA on user accounts (8.0) → Implement MFA
7. **T-002** - SQL injection risk (8.5) → Parameterized queries
8. **I-002** - Unencrypted backups (8.0) → Enable backup encryption
9. **E-003** - Privilege escalation (8.0) → Server-side role validation
10. **S-003** - API key in client code (7.5) → Move to backend, use OAuth

### Medium Threats (Implement Within 90 Days)

11. **S-002** - Session token theft (6.0) → CSP headers, output encoding
12. **R-002** - Missing admin audit logs (7.0) → Admin action logging
13. **R-003** - Missing PII access logs (7.5) → Database query logging
14. **D-001** - No rate limiting on auth (7.0) → Rate limiting implementation
15. **D-003** - No database failover (7.5) → Database replication

### Low Threats (Implement When Resources Available)

16. **T-003** - Request tampering (5.5) → Request signing
17. **R-001** - Basic logging only (5.0) → Comprehensive audit logging
18. **D-002** - File upload DoS (6.0) → File size limits
19. **I-003** - Verbose errors (3.0) → Error sanitization

---

## Threat Model Diagram

[Include architecture diagram with threat annotations]

**Diagram Components:**
- Trust boundaries (color-coded: red = external, yellow = internal, green = privileged)
- Attack vectors (arrows with threat IDs)
- Data flows with security controls
- Assets (highlighted with classification)

**See:** `threat-model-diagram.png` for visual representation

---

## Mitigations Summary

### Authentication & Authorization

**Current State:** Basic password authentication, no MFA, missing authorization checks

**Recommended Mitigations:**
1. Implement MFA (TOTP, WebAuthn) for all accounts - **Priority: High**
2. Implement RBAC (Role-Based Access Control) - **Priority: Critical**
3. Add authorization checks on all endpoints - **Priority: Critical**
4. Implement account lockout after 5 failed attempts - **Priority: Medium**

**Standards:** OWASP ASVS V2 (Authentication), V4 (Access Control)

### Cryptography

**Current State:** HTTPS for external traffic, no database encryption, no backup encryption

**Recommended Mitigations:**
1. Enable TLS for database connections - **Priority: Critical**
2. Enable TDE (Transparent Data Encryption) for databases - **Priority: Critical**
3. Enable backup encryption (AES-256) - **Priority: High**
4. Implement key management service (AWS KMS, Azure Key Vault) - **Priority: High**

**Standards:** NIST SP 800-175B (Cryptography), OWASP Cryptographic Storage

### Input Validation & Data Protection

**Current State:** Minimal input validation, no parameterized queries

**Recommended Mitigations:**
1. Implement parameterized queries (prevent SQL injection) - **Priority: High**
2. Implement whitelist input validation - **Priority: High**
3. Implement response filtering (prevent PII leakage) - **Priority: Critical**
4. Implement output encoding (prevent XSS) - **Priority: Medium**

**Standards:** OWASP ASVS V5 (Validation), V8 (Data Protection)

### Logging & Monitoring

**Current State:** Basic application logs, no security event logging

**Recommended Mitigations:**
1. Implement comprehensive security logging (auth, authz, data access) - **Priority: High**
2. Implement admin action audit logging - **Priority: High**
3. Integrate with SIEM for real-time alerting - **Priority: Medium**
4. Implement tamper-evident log storage - **Priority: Medium**

**Standards:** NIST SP 800-92 (Log Management), PCI DSS Req 10

### Network Security

**Current State:** Basic firewall, no network segmentation, no IDS/IPS

**Recommended Mitigations:**
1. Implement network segmentation (DMZ, internal, restricted zones) - **Priority: Medium**
2. Implement IDS/IPS for threat detection - **Priority: Low**
3. Implement WAF (Web Application Firewall) - **Priority: Medium**
4. Implement DDoS protection - **Priority: Low**

**Standards:** NIST SP 800-125B (Network Segmentation), PCI DSS Req 1

---

## Assumptions and Constraints

### Assumptions

1. [Assumption 1 - e.g., "Internal network is not fully trusted"]
2. [Assumption 2 - e.g., "Threat actors have moderate resources (cybercrime groups)"]
3. [Assumption 3 - e.g., "Data breach would result in significant financial/reputational damage"]

### Constraints

1. [Constraint 1 - e.g., "Limited security budget ($50k annual)"]
2. [Constraint 2 - e.g., "Must maintain < 100ms API response time"]
3. [Constraint 3 - e.g., "Compliance deadline in 90 days"]

### Out of Scope

1. [Out of scope item 1 - e.g., "Third-party vendor security assessments"]
2. [Out of scope item 2 - e.g., "Physical security controls"]
3. [Out of scope item 3 - e.g., "Social engineering attacks"]

---

## Review and Approval

| Role | Name | Date | Signature |
|---|---|---|---|
| **Threat Modeling Lead** | [Name] | [YYYY-MM-DD] | [Signature] |
| **Security Architect** | [Name] | [YYYY-MM-DD] | [Signature] |
| **Development Lead** | [Name] | [YYYY-MM-DD] | [Signature] |
| **Product Owner** | [Name] | [YYYY-MM-DD] | [Signature] |

---

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Name] | Initial threat model |
| 1.1 | [YYYY-MM-DD] | [Name] | Updated after architecture changes |

---

## References

- **STRIDE Methodology:** https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- **NIST SP 800-160 Vol. 1:** https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final
- **OWASP ASVS:** https://owasp.org/www-project-application-security-verification-standard/
- **MITRE ATT&CK:** https://attack.mitre.org/

---

**Document Classification:** Confidential - Internal Use Only
**Next Review Date:** [YYYY-MM-DD] (recommended annual review)
