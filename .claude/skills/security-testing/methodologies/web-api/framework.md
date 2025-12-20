
## Methodology Overview

Web application and API security testing identifies vulnerabilities in web-based applications and their APIs by systematically testing against OWASP security standards and industry best practices.

---

## OWASP Framework Integration

### OWASP Top 10 (Web Application Vulnerabilities)

**Discovery:** `Glob: resources/library/**/*owasp-top10*`

**Top 10 Vulnerabilities (2021):**

1. **A01:2021 - Broken Access Control**
   - Vertical privilege escalation
   - Horizontal privilege escalation
   - IDOR (Insecure Direct Object References)
   - Missing function-level access control

2. **A02:2021 - Cryptographic Failures**
   - Sensitive data transmitted in clear text
   - Weak/outdated cryptographic algorithms
   - Missing encryption at rest
   - Improper key management

3. **A03:2021 - Injection**
   - SQL injection (SQLi)
   - NoSQL injection
   - Command injection (OS command injection)
   - LDAP injection
   - XML injection

4. **A04:2021 - Insecure Design**
   - Missing security controls
   - Inadequate threat modeling
   - Insecure design patterns
   - Business logic flaws

5. **A05:2021 - Security Misconfiguration**
   - Default credentials
   - Unnecessary features enabled
   - Error messages revealing stack traces
   - Missing security headers
   - Outdated/unpatched software

6. **A06:2021 - Vulnerable and Outdated Components**
   - Using components with known vulnerabilities
   - Unpatched dependencies
   - Outdated libraries/frameworks
   - Unsupported software versions

7. **A07:2021 - Identification and Authentication Failures**
   - Weak password requirements
   - Credential stuffing vulnerabilities
   - Session fixation
   - Missing MFA
   - Predictable session IDs

8. **A08:2021 - Software and Data Integrity Failures**
   - Insecure deserialization
   - CI/CD pipeline compromise
   - Auto-update without integrity verification
   - Unsigned or unvalidated updates

9. **A09:2021 - Security Logging and Monitoring Failures**
   - Insufficient logging
   - Logs not monitored
   - Lack of alerting
   - Insufficient audit trails

10. **A10:2021 - Server-Side Request Forgery (SSRF)**
    - Internal network access via SSRF
    - Cloud metadata access
    - Port scanning via SSRF
    - Bypassing network controls

---

### OWASP API Security Top 10

**Discovery:** `Glob: resources/library/**/*owasp*api*` or `**/*api-security*`
**Size:** 367 files, 277.9k tokens

**API-Specific Vulnerabilities:**

1. **API1:2023 - Broken Object Level Authorization (BOLA)**
   - Access to objects belonging to other users
   - Manipulation of IDs in API requests
   - Missing or improper authorization checks

2. **API2:2023 - Broken Authentication**
   - Weak API key generation
   - Missing rate limiting on authentication
   - JWT vulnerabilities (weak signing, none algorithm)
   - Token leakage in URLs/logs

3. **API3:2023 - Broken Object Property Level Authorization**
   - Mass assignment vulnerabilities
   - Excessive data exposure
   - Missing property-level access controls

4. **API4:2023 - Unrestricted Resource Consumption**
   - Missing rate limiting
   - Resource exhaustion attacks
   - Expensive operations without limits
   - Lack of pagination

5. **API5:2023 - Broken Function Level Authorization (BFLA)**
   - Accessing admin functions as regular user
   - Missing role-based access controls
   - Predictable endpoint naming

6. **API6:2023 - Unrestricted Access to Sensitive Business Flows**
   - Automated abuse of legitimate functions
   - Business logic bypass
   - Missing anti-automation controls

7. **API7:2023 - Server Side Request Forgery (SSRF)**
   - Forcing API to make requests to internal resources
   - Cloud metadata service access
   - Internal port scanning

8. **API8:2023 - Security Misconfiguration**
   - Verbose error messages
   - Missing security headers (CORS, CSP)
   - Unnecessary HTTP methods enabled
   - Default configurations

9. **API9:2023 - Improper Inventory Management**
   - Undocumented API endpoints
   - Old API versions still accessible
   - Shadow APIs
   - Zombie APIs

10. **API10:2023 - Unsafe Consumption of APIs**
    - Trusting third-party APIs without validation
    - Following redirects without verification
    - Insufficient data validation from external APIs

---

### OWASP Application Security Verification Standard (ASVS)

**Discovery:** `Glob: resources/library/**/*asvs*`
**Purpose:** Security requirements and testing levels

**Verification Levels:**

- **Level 1:** Basic security verification (automated testing)
- **Level 2:** Standard security verification (manual + automated)
- **Level 3:** Advanced security verification (comprehensive testing)

**Covers 14 Categories:**
1. Architecture, Design and Threat Modeling
2. Authentication
3. Session Management
4. Access Control
5. Validation, Sanitization and Encoding
6. Stored Cryptography
7. Error Handling and Logging
8. Data Protection
9. Communication
10. Malicious Code
11. Business Logic
12. Files and Resources
13. API and Web Service
14. Configuration

---

### OWASP Web Security Testing Guide (WSTG)

**Discovery:** `Glob: resources/library/**/*wstg*`
**Purpose:** Comprehensive web testing methodology

**Testing Categories:**
- Information Gathering
- Configuration and Deployment Management Testing
- Identity Management Testing
- Authentication Testing
- Authorization Testing
- Session Management Testing
- Input Validation Testing
- Error Handling Testing
- Cryptography Testing
- Business Logic Testing
- Client-Side Testing

---

## Testing Methodology Structure

### EXPLORE Phase

1. **Scope Review**
   - Read SCOPE.md for target applications/APIs
   - Identify in-scope domains, subdomains, endpoints
   - Understand authentication requirements
   - Note out-of-scope items and rate limiting

2. **Application Reconnaissance**
   - Manual browsing and functionality mapping
   - Technology stack identification (Wappalyzer, Burp)
   - API endpoint discovery (Swagger/OpenAPI docs, traffic analysis)
   - Authentication mechanism analysis
   - Input point enumeration

3. **OWASP Vulnerability Mapping**
   - Map application features to OWASP Top 10
   - Identify potential API vulnerabilities
   - Review ASVS requirements applicable to app
   - Prioritize high-risk areas

### PLAN Phase

1. **Vulnerability Prioritization**
   - High-risk features (authentication, payment, admin)
   - Complex business logic
   - Data-sensitive operations
   - Public-facing endpoints

2. **Tool Inventory Check** (CRITICAL)
   - Review `/servers` for available tools
   - Check for: Burp Suite, OWASP ZAP, SQLMap, Nuclei, ffuf, etc.
   - Identify missing tools
   - Request deployment if needed

3. **Test Plan Generation**
   - Map OWASP Top 10 to specific tests
   - Document API testing approach per endpoint
   - Include both automated and manual tests
   - Plan for authentication bypass, authorization, injection, etc.
   - Get user approval before testing

### CODE Phase (Testing)

1. **Automated Scanning**
   - OWASP ZAP/Burp Suite active scan
   - Nuclei template scanning
   - SQLMap for SQL injection
   - Document findings

2. **Manual Testing**
   - **Authentication Testing**
     - Credential stuffing, brute force
     - Session management flaws
     - JWT vulnerabilities
     - OAuth misconfiguration

   - **Authorization Testing**
     - BOLA/IDOR testing
     - Privilege escalation (vertical/horizontal)
     - BFLA (accessing admin functions)
     - Missing function-level access control

   - **Injection Testing**
     - SQL injection (in-band, blind, time-based)
     - NoSQL injection
     - Command injection
     - Template injection
     - XML/XXE injection

   - **Business Logic Testing**
     - Payment manipulation
     - Workflow bypass
     - Race conditions
     - Parameter tampering

   - **API-Specific Testing**
     - Mass assignment
     - Rate limit bypass
     - Excessive data exposure
     - GraphQL vulnerabilities (introspection, batching)
     - API versioning issues

3. **Evidence Collection**
   - Screenshots of successful exploits
   - Request/response pairs from Burp
   - Proof-of-concept code
   - Map findings to OWASP categories

### COMMIT Phase (Reporting)

1. **Findings Documentation**
   - Executive summary
   - Technical findings mapped to OWASP categories
   - Severity ratings (Critical, High, Medium, Low)
   - Evidence (screenshots, PoC)
   - CVSS scores where applicable

2. **Remediation Recommendations**
   - Specific code fixes
   - Configuration changes
   - Security header recommendations
   - Input validation patterns
   - Reference OWASP Cheat Sheets

3. **OWASP Integration**
   - Map all findings to OWASP Top 10 / API Top 10
   - Include ASVS control references
   - Link to relevant WSTG sections

---

## Common Web/API Vulnerabilities

### Authentication & Session Management
- **Weak Password Policy:** No complexity requirements
- **Missing MFA:** Single-factor authentication only
- **Session Fixation:** Session ID not regenerated after login
- **Predictable Session Tokens:** Sequential or weak randomness
- **JWT Issues:** None algorithm, weak secrets, lack of expiration

### Authorization
- **IDOR:** User can access other users' data via ID manipulation
- **Missing Function-Level Access Control:** Regular user accessing admin endpoints
- **Path Traversal:** Access to unauthorized files via ../ manipulation
- **CORS Misconfiguration:** Overly permissive CORS allowing credential theft

### Injection Vulnerabilities
- **SQL Injection:** Union-based, Boolean-based, Time-based blind SQLi
- **Command Injection:** OS command execution via unsanitized input
- **NoSQL Injection:** MongoDB, CouchDB injection attacks
- **LDAP Injection:** Authentication bypass via LDAP
- **SSTI (Server-Side Template Injection):** RCE via template engines
- **XXE (XML External Entity):** XML parser vulnerabilities

### Business Logic
- **Race Conditions:** Multiple simultaneous requests causing logic bypass
- **Price Manipulation:** Negative quantities, decimal manipulation
- **Workflow Bypass:** Skipping payment steps
- **Insufficient Process Validation:** Missing state checks

### API-Specific
- **Mass Assignment:** Modifying protected fields via API
- **Excessive Data Exposure:** API returning unnecessary sensitive data
- **Lack of Rate Limiting:** Brute force, resource exhaustion
- **GraphQL Issues:** Introspection enabled, deep nesting, batching attacks

### Information Disclosure
- **Verbose Error Messages:** Stack traces, database errors
- **Source Code Disclosure:** .git, .svn, backup files exposed
- **Directory Listing:** Enabled on web server
- **API Documentation Exposure:** Swagger UI publicly accessible

---

## Testing Tools

**Web Application Scanners:**
- Burp Suite Professional (comprehensive)
- OWASP ZAP (free alternative)
- Nuclei (template-based scanning)
- Nikto (web server scanner)

**Injection Testing:**
- SQLMap (SQL injection)
- NoSQLMap (NoSQL injection)
- Commix (command injection)

**API Testing:**
- Postman (API testing and collection)
- Insomnia (REST/GraphQL client)
- ffuf (fuzzing and discovery)
- Arjun (parameter discovery)

**Directory/File Discovery:**
- Gobuster
- ffuf
- Feroxbuster
- Dirsearch

**Subdomain Enumeration:**
- Subfinder
- Amass
- Assetfinder

---

## Reference Resources

### Local Resources (Dynamic Discovery)

**OWASP:** `Glob: resources/library/**/*owasp*`
- Top 10: `**/*top10*`
- ASVS: `**/*asvs*`
- WSTG: `**/*wstg*`
- Cheat Sheets: `**/*cheatsheet*`

**Books:** `Glob: resources/library/books/**/*`
- Web/API testing: `**/*bug-bounty*` or `**/*api*` or `**/*web*`

### Web Resources

**OWASP:**
- Top 10: https://owasp.org/Top10/
- API Security Top 10: https://owasp.org/API-Security/
- ASVS: https://owasp.org/www-project-application-security-verification-standard/
- WSTG: https://owasp.org/www-project-web-security-testing-guide/

---

**Created:** 2025-12-01
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Version:** 1.0
