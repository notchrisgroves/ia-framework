# Security Code Review Standards

**Progressive context file - Load when validating code against industry standards**

This document covers industry standards, frameworks, and best practices for security code reviews.

---

## Primary Standards

### OWASP Code Review Guide v2.0

**URL:** https://owasp.org/www-project-code-review-guide/

**Coverage:** Comprehensive security code review methodology

**Key Sections:**
- **Chapter 3:** Methodology and techniques (manual review, automated analysis)
- **Chapter 4:** Common vulnerability patterns (injection, XSS, auth, crypto)
- **Chapter 5:** Language-specific guidance (Java, .NET, PHP, Python, Ruby)
- **Chapter 7:** Review frameworks and checklists

**Application:** Primary framework for ALL security code reviews

**Key Principles:**
1. **Context is king** - Understand application architecture before reviewing code
2. **Risk-based approach** - Focus on high-risk areas (auth, data access, crypto)
3. **Defense in depth** - Look for layered security controls
4. **Automation + Manual** - Use SAST tools but manual review required for logic flaws

---

### CWE (Common Weakness Enumeration)

**URL:** https://cwe.mitre.org/

**Coverage:** Comprehensive list of software security weaknesses

**CWE Top 25 Most Dangerous (2023):**

1. **CWE-787** - Out-of-bounds Write
2. **CWE-79** - Cross-Site Scripting (XSS)
3. **CWE-89** - SQL Injection
4. **CWE-20** - Improper Input Validation
5. **CWE-125** - Out-of-bounds Read
6. **CWE-78** - OS Command Injection
7. **CWE-416** - Use After Free
8. **CWE-22** - Path Traversal
9. **CWE-352** - CSRF
10. **CWE-434** - Unrestricted File Upload
11. **CWE-476** - NULL Pointer Dereference
12. **CWE-502** - Deserialization of Untrusted Data
13. **CWE-190** - Integer Overflow
14. **CWE-287** - Improper Authentication
15. **CWE-798** - Hardcoded Credentials
16. **CWE-862** - Missing Authorization
17. **CWE-77** - Command Injection
18. **CWE-306** - Missing Authentication
19. **CWE-119** - Buffer Overflow
20. **CWE-276** - Incorrect Default Permissions
21. **CWE-918** - SSRF
22. **CWE-362** - Race Condition
23. **CWE-400** - Uncontrolled Resource Consumption
24. **CWE-611** - XXE
25. **CWE-94** - Code Injection

**Application:** All vulnerability findings MUST map to CWE IDs

---

### SEI CERT Coding Standards

**URL:** https://wiki.sei.cmu.edu/confluence/display/seccode

**Coverage:** Language-specific secure coding rules

**Supported Languages:**
- C Coding Standard
- C++ Coding Standard
- Java Coding Guidelines
- Perl Coding Standard
- Android Secure Coding Standard

**Key Areas:**
- **Input Validation (IDS)** - Validate all untrusted data
- **Declarations (DCL)** - Proper variable/function declarations
- **Expressions (EXP)** - Safe expression evaluation
- **Integers (INT)** - Integer overflow/underflow prevention
- **Strings (STR)** - Safe string handling
- **Memory Management (MEM)** - Proper allocation/deallocation
- **File I/O (FIO)** - Secure file operations
- **Environment (ENV)** - Secure environment interaction
- **Concurrency (CON)** - Thread-safe code

**Application:** Apply language-specific rules during code review

---

### NIST SP 800-218 - Secure Software Development Framework (SSDF)

**URL:** https://csrc.nist.gov/publications/detail/sp/800-218/final

**Coverage:** Secure software development lifecycle practices

**4 Practice Groups:**

**PO (Prepare the Organization):**
- PO.1: Define security requirements
- PO.2: Implement security roles
- PO.3: Implement security training
- PO.4: Define security standards
- PO.5: Manage security risks

**PS (Protect the Software):**
- PS.1: Secure development environment
- PS.2: Secure code repository
- PS.3: Code review requirements

**PW (Produce Well-Secured Software):**
- PW.1: Design for security
- PW.2: Review design
- PW.3: Verify third-party components
- PW.4: Reuse existing secure components
- PW.5: Create source code securely
- PW.6: Configure securely
- PW.7: Review code
- PW.8: Test security
- PW.9: Configure build process

**RV (Respond to Vulnerabilities):**
- RV.1: Identify vulnerabilities
- RV.2: Assess vulnerabilities
- RV.3: Remediate vulnerabilities

**Application:** Validate secure development practices during code review

---

### OWASP ASVS (Application Security Verification Standard)

**URL:** https://owasp.org/www-project-application-security-verification-standard/

**Coverage:** Security requirements for application code

**Relevant Sections for Code Review:**

**V1: Architecture, Design and Threat Modeling**
- V1.1: Secure SDLC
- V1.2: Authentication Architecture
- V1.4: Access Control Architecture
- V1.6: Cryptographic Architecture

**V2: Authentication**
- V2.1: Password Security
- V2.2: General Authenticator Requirements
- V2.5: Credential Recovery
- V2.7: Out of Band Verifier

**V3: Session Management**
- V3.1: Fundamental Session Management
- V3.2: Session Binding
- V3.3: Session Logout and Timeout
- V3.4: Cookie-based Session Management

**V4: Access Control**
- V4.1: General Access Control Design
- V4.2: Operation Level Access Control
- V4.3: Other Access Control Considerations

**V5: Validation, Sanitization and Encoding**
- V5.1: Input Validation
- V5.2: Sanitization and Sandboxing
- V5.3: Output Encoding and Injection Prevention
- V5.4: Memory, String, and Unmanaged Code
- V5.5: Deserialization Prevention

**V6: Stored Cryptography**
- V6.1: Data Classification
- V6.2: Algorithms
- V6.3: Random Values
- V6.4: Secret Management

**V7: Error Handling and Logging**
- V7.1: Log Content
- V7.2: Log Processing
- V7.3: Log Protection
- V7.4: Error Handling

**V8: Data Protection**
- V8.1: General Data Protection
- V8.2: Client-side Data Protection
- V8.3: Sensitive Private Data

**V9: Communication**
- V9.1: Client Communication Security
- V9.2: Server Communication Security

**V10: Malicious Code**
- V10.1: Code Integrity
- V10.2: Malicious Code Search
- V10.3: Application Integrity

**Application:** Map code review findings to ASVS requirements

---

## Supporting Standards

### SANS Top 25 Programming Errors

**URL:** https://www.sans.org/top25-software-errors/

**3 Categories:**

**Insecure Interaction:**
1. Improper Neutralization (Injection)
2. Improper Input Validation
3. Improper Encoding/Escaping
4. Cross-Site Scripting
5. SQL Injection
6. OS Command Injection
7. CSRF
8. Path Traversal

**Risky Resource Management:**
9. Buffer Overflow
10. Uncontrolled Resource Consumption
11. Unrestricted Upload
12. Missing Authentication
13. Missing Authorization
14. Incorrect Authorization
15. Hardcoded Credentials
16. Missing Encryption
17. Inadequate Encryption Strength

**Porous Defenses:**
18. Incorrect Permission Assignment
19. Use of Broken Crypto
20. Insufficient Verification of Data Authenticity
21. Improper Certificate Validation
22. Use of Hard-coded Cryptographic Key
23. Missing or Incorrect Authorization
24. Server-Side Request Forgery (SSRF)
25. Improper Restriction of XML External Entity Reference (XXE)

**Application:** Review checklist development

---

### PCI DSS 4.0 - Secure Coding Requirements

**Requirement 6.2: Secure Development**

**6.2.1:** Bespoke software developed securely
- Input validation
- Error handling
- Secure cryptographic storage
- Secure communications
- Avoid common vulnerabilities (OWASP Top 10)

**6.2.2:** Software development personnel trained in secure coding

**6.2.3:** Code review before release to production
- Manual or automated review
- Performed by someone other than original author
- Ensure code changes reviewed

**6.2.4:** Software engineering techniques to prevent/mitigate common attacks
- Input validation
- Output encoding
- Parameterized queries
- Memory-safe languages
- Strong cryptography

**Application:** PCI DSS compliance validation for payment applications

---

### NIST SP 800-53 - Security Controls

**Relevant Controls for Code Review:**

**SA-11: Developer Security Testing and Evaluation**
- Static code analysis
- Dynamic code analysis
- Penetration testing
- Code review

**SA-15: Development Process, Standards, and Tools**
- Secure coding standards
- Code review requirements
- Security testing

**SI-10: Information Input Validation**
- Syntax validation
- Semantic validation
- Prevent code injection

**Application:** Federal compliance validation

---

## Language-Specific Standards

### Python - PEP 8 + Security

**Security-Relevant PEPs:**
- **PEP 506** - Adding secrets module (use instead of random)
- **PEP 578** - Runtime Audit Hooks

**Common Security Issues:**
- Pickle deserialization (never use with untrusted data)
- SQL injection (use parameterized queries, not f-strings)
- Command injection (avoid os.system, use subprocess with list args)
- Path traversal (validate paths, use os.path.abspath)
- Eval/exec with user input (never)

**Secure Libraries:**
- **cryptography** (not PyCrypto)
- **bcrypt/argon2** for password hashing
- **secrets** for random tokens

**See:** `reference/language-specific.md` (Python section)

---

### JavaScript/Node.js - Security Standards

**ESLint Security Plugins:**
- **eslint-plugin-security** - Detects security issues
- **eslint-plugin-no-unsanitized** - Prevents XSS

**Common Security Issues:**
- XSS (sanitize output, use CSP)
- Prototype pollution (validate object keys)
- Command injection (child_process with user input)
- Path traversal (validate file paths)
- SQL injection (use parameterized queries)
- Missing rate limiting
- Missing security headers

**Secure Libraries:**
- **helmet** (security headers)
- **express-rate-limit** (rate limiting)
- **validator** (input validation)
- **dompurify** (XSS prevention)

**See:** `reference/language-specific.md` (JavaScript section)

---

### Java - SEI CERT + OWASP

**SEI CERT Java Coding Standard:**
- **IDS** - Input Validation and Data Sanitization
- **FIO** - File I/O
- **SER** - Serialization
- **SEC** - Security

**Common Security Issues:**
- SQL injection (use PreparedStatement)
- XXE (disable external entities)
- Deserialization (never deserialize untrusted data)
- Path traversal (validate paths)
- LDAP injection (escape input)
- Weak random (use SecureRandom)
- Hardcoded credentials

**Secure Libraries:**
- **OWASP ESAPI** - Security API
- **Spring Security** - Auth framework
- **Apache Shiro** - Auth framework

**See:** `reference/language-specific.md` (Java section)

---

### C/C++ - SEI CERT + MISRA

**SEI CERT C/C++ Coding Standards:**
- **STR** - Strings (bounds checking)
- **MEM** - Memory Management (leaks, buffer overflows)
- **INT** - Integers (overflow/underflow)
- **FIO** - File I/O
- **CON** - Concurrency

**Common Security Issues:**
- Buffer overflow (use strncpy, snprintf, bounds checking)
- Format string vulnerabilities (never printf(user_input))
- Integer overflow (check arithmetic)
- Use after free
- NULL pointer dereference
- Race conditions

**Secure Practices:**
- Use memory-safe functions (strncpy vs strcpy)
- Bounds checking on all array access
- Initialize all variables
- Check return values
- Use static analysis tools (Coverity, PVS-Studio)

**See:** `reference/language-specific.md` (C/C++ section)

---

## CVSS v3.1 Scoring Guide

**Base Metrics:**

**Attack Vector (AV):**
- **Network (N):** Remotely exploitable
- **Adjacent (A):** Adjacent network access
- **Local (L):** Local access required
- **Physical (P):** Physical access required

**Attack Complexity (AC):**
- **Low (L):** No special conditions
- **High (H):** Specific conditions required

**Privileges Required (PR):**
- **None (N):** No authentication
- **Low (L):** Basic user privileges
- **High (H):** Admin/elevated privileges

**User Interaction (UI):**
- **None (N):** No interaction required
- **Required (R):** User must take action

**Scope (S):**
- **Unchanged (U):** Impact limited to vulnerable component
- **Changed (C):** Impact beyond vulnerable component

**Impact (C/I/A):**
- **None (N):** No impact
- **Low (L):** Limited impact
- **High (H):** Total compromise

**Severity Ranges:**
- **Critical:** 9.0-10.0 (immediate action)
- **High:** 7.0-8.9 (urgent action)
- **Medium:** 4.0-6.9 (planned remediation)
- **Low:** 0.1-3.9 (informational)

**Calculator:** https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator

---

## Standards Selection Guide

**Q: Which standards should I reference for this code review?**

**Default (All Reviews):**
- OWASP Code Review Guide (methodology)
- CWE classifications (vulnerability naming)
- CVSS v3.1 scoring (severity)

**Add if Language-Specific:**
- SEI CERT C/C++ (for C/C++ code)
- SEI CERT Java (for Java code)
- Language-specific security guides (see `reference/language-specific.md`)

**Add if Compliance Required:**
- PCI DSS Requirement 6.2 (payment applications)
- NIST SP 800-53 SA-11 (federal systems)
- NIST SP 800-218 SSDF (all federal software)

**Add if Application Security Focus:**
- OWASP ASVS (security requirements mapping)
- SANS Top 25 (checklist development)

---

**Version:** 2.0
**Last Updated:** 2025-12-02
**Primary Standards:** OWASP Code Review Guide, CWE, SEI CERT, NIST SP 800-218
