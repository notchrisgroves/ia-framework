# Secure Architecture Patterns and Anti-Patterns

**Progressive context file - Load when analyzing architecture patterns**

This document covers secure architecture patterns (best practices) and anti-patterns (common mistakes).

---

## Secure Architecture Patterns

### 1. Zero Trust Architecture

**Principle:** Never trust, always verify

**Key Components:**
- **Identity-centric security** - User/device identity as control plane
- **Least privilege access** - JIT (Just-In-Time), JEA (Just-Enough-Access)
- **Micro-segmentation** - Granular network controls
- **Continuous verification** - Re-authenticate, re-authorize per session
- **Assume breach** - Minimize blast radius, contain lateral movement

**Implementation:**
- Identity provider (Okta, Azure AD, Auth0)
- Policy engine (OPA, Cedar, custom)
- Policy enforcement point (API gateway, service mesh)
- Encrypted communication (mTLS)
- Telemetry and analytics (SIEM, UEBA)

**Standards:** NIST SP 800-207

**When to use:** Modern architectures, cloud-native, high-security environments

---

### 2. Defense-in-Depth (Layered Security)

**Principle:** Multiple independent security layers

**Layers:**
1. **Physical** - Data center security, device protection
2. **Network** - Firewalls, IDS/IPS, segmentation
3. **Host** - OS hardening, antivirus, EDR
4. **Application** - Input validation, authentication, authorization
5. **Data** - Encryption at rest, access controls

**Key Characteristics:**
- Independent controls (bypass one ≠ bypass all)
- Fail-secure design (failure defaults to deny)
- No single point of failure

**Implementation Example (Web Application):**
```
Internet → WAF → Load Balancer → Firewall → Web Tier → App Tier → Database Tier
         ↓        ↓              ↓          ↓           ↓            ↓
       DDoS     TLS Term     IDS/IPS    Auth/AuthZ  Logic/Valid  Encryption
```

**Standards:** NIST SP 800-160 (Appendix D: Defense in Depth)

**When to use:** ALL architectures (foundational principle)

---

### 3. Secure by Default

**Principle:** Security enabled out-of-the-box, minimal configuration required

**Key Practices:**
- **Deny-by-default** - Whitelist (allow known good) vs blacklist (block known bad)
- **Minimal attack surface** - Disable unnecessary services, close unused ports
- **Secure defaults** - Strong crypto (TLS 1.2+, AES-256), no default credentials
- **Fail-secure** - Failure mode denies access (not grants)

**Implementation:**
- **Firewall rules:** Default deny, explicit allow
- **API authentication:** Reject unauthenticated by default
- **Database access:** Least privilege accounts, no default passwords
- **File permissions:** Restrictive by default (750, 640)

**Anti-Example:**
- MongoDB with no authentication (pre-3.0 default)
- Elasticsearch publicly accessible (default bind to 0.0.0.0)
- Admin interfaces on default ports (8080, 8443) without authentication

**Standards:** OWASP ASVS V1.1 (Secure SDLC), CIS Controls

**When to use:** ALL architectures, especially products/SaaS

---

### 4. Separation of Duties (SoD)

**Principle:** Divide critical functions among multiple people/systems

**Key Practices:**
- **Multi-person approval** - Critical operations require 2+ approvals (4-eyes principle)
- **Role segregation** - Dev ≠ prod access, read ≠ write
- **Privileged access management (PAM)** - Separate admin accounts, time-limited access
- **Break-glass procedures** - Emergency access with full audit trail

**Implementation:**
- **Code deployment:** Developer commits → CI/CD → Approval → Production
- **Financial transactions:** Initiator ≠ Approver
- **Data access:** Read-only analysts, write-only ETL, DBA with full access
- **AWS IAM:** Separate roles for dev, ops, security, billing

**Standards:** NIST SP 800-53 AC-5 (Separation of Duties)

**When to use:** High-value systems, financial systems, regulated environments

---

### 5. Encryption Architecture

**Principle:** Protect data confidentiality and integrity with cryptography

**Encryption Types:**

**A. Encryption at Rest**
- Database encryption (TDE - Transparent Data Encryption)
- File system encryption (LUKS, BitLocker, FileVault)
- Object storage encryption (S3 SSE, Azure Storage encryption)
- Backup encryption (encrypted archives)

**B. Encryption in Transit**
- TLS 1.2+ for HTTPS (deprecate TLS 1.0/1.1)
- mTLS (mutual TLS) for service-to-service communication
- VPN for remote access (WireGuard, IPsec, OpenVPN)
- Encrypted messaging (Signal Protocol, E2EE)

**C. Encryption at Use (Advanced)**
- Homomorphic encryption (compute on encrypted data)
- Confidential computing (TEE - Trusted Execution Environments like Intel SGX, AMD SEV)

**Key Management:**
- **HSM (Hardware Security Module)** - FIPS 140-2 Level 3+ for high-value keys
- **KMS (Key Management Service)** - AWS KMS, Azure Key Vault, GCP Cloud KMS
- **Key rotation** - Automatic periodic rotation (90 days recommended)
- **Key hierarchy** - Master key → Data encryption keys (envelope encryption)

**Crypto Standards:**
- **Symmetric:** AES-256-GCM (authenticated encryption)
- **Asymmetric:** RSA-2048+ or ECDSA P-256+
- **Hashing:** SHA-256, SHA-3
- **Password hashing:** Argon2id, bcrypt, scrypt (NOT MD5, SHA-1)
- **TLS:** TLS 1.2 minimum, TLS 1.3 preferred

**Standards:** NIST SP 800-175B (Cryptography), OWASP Cryptographic Storage Cheat Sheet

**When to use:** ALL systems handling sensitive data

---

### 6. Secure API Design

**Principle:** APIs are the attack surface of modern applications

**Key Practices:**

**A. Authentication**
- **OAuth 2.0** - Authorization framework (access tokens, refresh tokens)
- **API Keys** - Simple authentication (rotate regularly, use HTTPS only)
- **JWT (JSON Web Tokens)** - Stateless authentication (verify signature, check expiration)
- **mTLS** - Certificate-based authentication (service-to-service)

**B. Authorization**
- **RBAC (Role-Based Access Control)** - Permissions based on roles
- **ABAC (Attribute-Based Access Control)** - Context-aware authorization
- **OAuth scopes** - Granular permissions (read:users, write:posts)

**C. Rate Limiting**
- Per-user limits (100 requests/min/user)
- Per-IP limits (1000 requests/min/IP)
- Endpoint-specific limits (10 auth attempts/hour)
- Exponential backoff (429 Too Many Requests)

**D. Input Validation**
- Whitelist validation (allow known good, reject everything else)
- Schema validation (OpenAPI, JSON Schema)
- Type checking (string, int, email, UUID)
- Length limits (prevent buffer overflow, DoS)

**E. Output Encoding**
- Prevent XSS (HTML entity encoding, CSP headers)
- JSON responses (correct Content-Type: application/json)
- Error messages (no sensitive data, stack traces in dev only)

**F. API Security Headers**
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy` (CSP)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`

**Standards:** OWASP API Security Top 10, OWASP ASVS V13 (API)

**When to use:** ALL API architectures (REST, GraphQL, gRPC)

---

### 7. Network Segmentation

**Principle:** Isolate network zones to contain breaches

**Segmentation Strategies:**

**A. DMZ (Demilitarized Zone)**
- External firewall (Internet → DMZ)
- Internal firewall (DMZ → Internal)
- DMZ hosts: Web servers, reverse proxies, mail servers
- Internal hosts: Application servers, databases

**B. Micro-segmentation**
- Segment by application, service, or data classification
- East-west traffic controls (lateral movement prevention)
- Software-defined networking (SDN), security groups

**C. Security Zones**
- **Public zone** - Internet-facing (web servers, CDN)
- **Internal zone** - Corporate network (workstations, file servers)
- **Restricted zone** - Sensitive data (databases, PII, financial)
- **Management zone** - Admin interfaces (jump boxes, bastions)

**Implementation:**
- **Physical:** VLANs, separate subnets
- **Cloud:** VPC (AWS), VNet (Azure), VPC (GCP)
- **Security groups:** Stateful firewall rules (allow only necessary traffic)
- **NACLs (Network ACLs):** Stateless firewall (subnet-level)

**Standards:** NIST SP 800-125B (Network Segmentation), PCI DSS Req 1 (Network Security Controls)

**When to use:** ALL network architectures, especially PCI DSS/HIPAA

---

### 8. Secure Logging and Monitoring

**Principle:** Detect security incidents through comprehensive logging

**Key Practices:**

**A. Centralized Logging**
- **SIEM (Security Information and Event Management)** - Splunk, Elastic, Sentinel
- **Log aggregation** - Collect from all systems (servers, apps, network devices)
- **Retention** - 90 days minimum (regulatory requirements may require longer)

**B. What to Log**
- **Authentication events** - Login success/failure, MFA, password changes
- **Authorization events** - Access granted/denied, privilege escalation
- **Data access** - Database queries (especially PII/PHI), file access
- **Configuration changes** - Firewall rules, IAM policies, system configs
- **Security events** - IDS/IPS alerts, malware detections, anomalies

**C. Tamper-Evident Logs**
- **Write-once storage** - S3 Object Lock, Azure Immutable Blob
- **Cryptographic signatures** - Sign log entries (detect tampering)
- **Separate log storage** - Logs in separate account/subscription

**D. Real-Time Alerting**
- **Anomaly detection** - ML-based (UEBA - User and Entity Behavior Analytics)
- **Threshold alerts** - Failed login attempts (5+ in 10 min)
- **Correlation rules** - Multiple indicators (SIEM correlation)

**E. Log Security**
- **Encryption in transit** - TLS for log shipping
- **Encryption at rest** - Encrypted log storage
- **Access control** - Least privilege (security team only)
- **No sensitive data** - Sanitize passwords, tokens, PII

**Standards:** NIST SP 800-92 (Log Management), OWASP Logging Cheat Sheet, PCI DSS Req 10

**When to use:** ALL production systems

---

## Anti-Patterns (Common Security Mistakes)

### 1. Monolithic Authentication

**Problem:** Single authentication point for all systems, no defense-in-depth

**Symptoms:**
- One password for all applications
- No MFA
- Weak password policies (6 chars, no complexity)
- No password rotation

**Risks:**
- Credential stuffing attacks
- Phishing effectiveness
- Lateral movement after compromise

**Fix:**
- **Federated identity** - SSO (Single Sign-On) with centralized IDP
- **MFA (Multi-Factor Authentication)** - TOTP, WebAuthn, push notifications
- **Risk-based authentication** - Context-aware (location, device, behavior)
- **Strong password policies** - 12+ chars, complexity, rotation
- **Passwordless** - WebAuthn, FIDO2, passkeys

**Standards:** OWASP ASVS V2 (Authentication), NIST SP 800-63B (Digital Identity)

---

### 2. Client-Side Security

**Problem:** Security logic in client code (JavaScript, mobile apps), trust client input

**Symptoms:**
- Validation only in JavaScript (no server-side validation)
- Authorization checks in mobile app code
- Sensitive data in client code (API keys, secrets)
- Trust HTTP headers (X-Forwarded-For, Referer)

**Risks:**
- Bypass validation (modify client code, intercept requests)
- Privilege escalation (modify authorization checks)
- Credential exposure (decompile mobile apps)

**Fix:**
- **Server-side validation** - Validate all input server-side
- **Server-side authorization** - Never trust client authorization
- **Secrets management** - Backend-only secrets, use API gateways
- **Verify, don't trust** - Don't trust client headers, IP addresses

**Standards:** OWASP Top 10 (A04:2021 - Insecure Design)

---

### 3. Hardcoded Secrets

**Problem:** Credentials in code, config files committed to Git

**Symptoms:**
- Database passwords in application.properties
- API keys in source code
- Credentials in Dockerfiles
- .env files committed to Git

**Risks:**
- Credential exposure (public GitHub repos)
- Insider threats (developers with access)
- Credential sprawl (same password everywhere)

**Fix:**
- **Secrets management** - Vault, AWS Secrets Manager, Azure Key Vault
- **Environment variables** - Load from secure source at runtime
- **Secret scanning** - GitGuardian, TruffleHog, git-secrets
- **Rotate secrets** - Regular rotation, especially after exposure

**Standards:** OWASP Top 10 (A07:2021 - Identification and Authentication Failures)

---

### 4. Missing Rate Limiting

**Problem:** No throttling on authentication, APIs, critical endpoints

**Symptoms:**
- No rate limits on /login, /api endpoints
- No CAPTCHA on authentication
- No exponential backoff
- No account lockout after failed attempts

**Risks:**
- Brute force attacks (password guessing)
- Credential stuffing (leaked password lists)
- DDoS (resource exhaustion)
- Abuse (scraping, spam)

**Fix:**
- **Rate limiting** - Per-user, per-IP, per-endpoint
- **CAPTCHA** - After N failed attempts (reCAPTCHA v3)
- **Exponential backoff** - 1s, 2s, 4s, 8s delays
- **Account lockout** - Temporary lockout after 5-10 failed attempts
- **WAF (Web Application Firewall)** - CloudFlare, AWS WAF, Akamai

**Standards:** OWASP ASVS V2.2 (General Authenticator Security)

---

### 5. Insufficient Logging

**Problem:** No audit trail for security events, missing logs

**Symptoms:**
- No authentication logs (who logged in?)
- No authorization logs (who accessed what?)
- No data access logs (who queried PII?)
- No configuration change logs (who changed firewall rules?)

**Risks:**
- Cannot detect breaches (no visibility)
- Cannot investigate incidents (no evidence)
- Compliance failures (PCI DSS, HIPAA require logging)
- Insider threats undetected

**Fix:**
- **Comprehensive logging** - Auth, authz, data access, config changes
- **SIEM integration** - Centralized logging and alerting
- **Retention** - 90 days minimum (regulatory requirements)
- **Tamper-evident** - Write-once storage, cryptographic signatures

**Standards:** NIST SP 800-92 (Log Management), PCI DSS Req 10, OWASP Logging

---

### 6. Trust Boundary Violations

**Problem:** Internal network implicitly trusted, no authentication between services

**Symptoms:**
- "Flat network" (all systems in one VLAN)
- No authentication between microservices
- Internal APIs without authentication
- Trust based on IP address or network location

**Risks:**
- Lateral movement (compromise one system → access all)
- Insider threats (malicious employee)
- Supply chain attacks (compromised dependency)

**Fix:**
- **Zero trust** - Never trust, always verify
- **mTLS** - Certificate-based authentication for service-to-service
- **Network segmentation** - Micro-segmentation, security groups
- **API gateway** - Centralized authentication/authorization

**Standards:** NIST SP 800-207 (Zero Trust Architecture)

---

### 7. Insecure Direct Object References (IDOR)

**Problem:** Direct database IDs in URLs, no authorization checks

**Symptoms:**
- URLs like `/user/1234`, `/invoice/5678`
- No authorization check (can access any ID)
- Sequential IDs (enumerate /user/1, /user/2, /user/3...)

**Risks:**
- Unauthorized data access (view other users' data)
- Privilege escalation (modify other users' data)
- Data leakage (enumerate all records)

**Fix:**
- **Indirect references** - Session-specific mappings (user sees "invoice 1", server maps to UUID)
- **Authorization checks** - Verify user can access resource
- **UUIDs** - Non-sequential identifiers (prevent enumeration)
- **Context-aware authz** - Check ownership (this user owns this resource)

**Standards:** OWASP Top 10 (A01:2021 - Broken Access Control)

---

### 8. Missing Security Headers

**Problem:** No HTTP security headers, vulnerable to client-side attacks

**Symptoms:**
- No `Strict-Transport-Security` (HSTS)
- No `Content-Security-Policy` (CSP)
- No `X-Frame-Options`
- No `X-Content-Type-Options`

**Risks:**
- XSS (Cross-Site Scripting)
- Clickjacking
- MIME-type sniffing
- Downgrade attacks (HTTPS → HTTP)

**Fix:**
- **HSTS** - `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- **CSP** - `Content-Security-Policy: default-src 'self'`
- **X-Frame-Options** - `X-Frame-Options: DENY`
- **X-Content-Type-Options** - `X-Content-Type-Options: nosniff`

**Standards:** OWASP Secure Headers Project, Mozilla Observatory

---

## Pattern Selection Guide

**Q: Which patterns should I recommend for this architecture?**

**Default (All Architectures):**
- Defense-in-Depth
- Secure by Default
- Encryption Architecture (at rest + in transit)
- Secure Logging and Monitoring

**Add if Modern/Cloud:**
- Zero Trust Architecture
- Secure API Design
- Network Segmentation (micro-segmentation)

**Add if High-Security:**
- Separation of Duties
- Multi-Factor Authentication
- Privileged Access Management

**Add if Regulated (PCI DSS/HIPAA):**
- Network Segmentation (DMZ, security zones)
- Encryption Architecture (all data encrypted)
- Comprehensive Logging (audit trail for compliance)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Standards:** NIST SP 800-160, OWASP ASVS, OWASP Top 10
