
## Plan Information

**Plan ID:** [YYYY-MM-DD-PLAN-XXX]
**Created:** [YYYY-MM-DD HH:MM UTC]
**Engagement Type:** [Penetration Test | Vulnerability Assessment | Bug Bounty | Red Team]
**Testing Mode:** [Director (production) | Mentor (learning) | Demo (validation)]

**Prepared By:** [Tester name]
**Approved By:** [Client contact]
**Approval Date:** [YYYY-MM-DD] ← REQUIRED BEFORE EXECUTION

---

## Scope Summary

### In-Scope Assets

**From SCOPE.md:**
[Brief summary of what will be tested - reference full scope document]

**Asset Breakdown:**
- **Web Applications:** [X applications]
- **APIs:** [X endpoints]
- **Mobile Apps:** [X apps]
- **Network Hosts:** [X hosts/networks]
- **Cloud Infrastructure:** [X accounts/subscriptions]

**Testing Constraints:**
- Testing window: [Dates/times]
- Rate limits: [Max requests per minute]
- Excluded functions: [DoS, destructive tests, etc.]

**Emergency Contact:** [Name, phone] - If testing causes issues

---

## Tool Inventory Check ✓

**CRITICAL STEP:** Verified `/servers` and local tools BEFORE generating this plan.

### Available Tools

**Web/API Testing:**
- ✅ Burp Suite Professional [Version X.Y]
- ✅ OWASP ZAP
- ✅ Nuclei
- ✅ SQLMap
- ✅ ffuf

**Network Testing:**
- ✅ Nmap [Version]
- ✅ Metasploit Framework [Version]
- ✅ Bloodhound
- ✅ Responder
- ❌ Impacket - NEED TO INSTALL

**Mobile Testing:**
- ✅ Frida [Version]
- ✅ Objection
- ✅ MobSF
- ❌ APKTool - NEED TO INSTALL

**Cloud Security:**
- ✅ ScoutSuite [Version]
- ✅ Prowler
- ❌ Pacu - NEED TO INSTALL

**Missing Tools Action:**
- [ ] Request deployment of Impacket via `/servers`
- [ ] Install APKTool locally
- [ ] Request Pacu deployment or use alternative

**Plan Adjusted Based on Available Tools:**
[Note any tests that cannot be performed due to missing tools]

---

## Testing Approach by Domain

### Domain: [Network | Web/API | Mobile | Web3 | AI/LLM | Cloud]

**Methodology:** [Framework baseline - e.g., MITRE ATT&CK, OWASP Top 10, etc.]

**Framework Location:** `../methodologies/[domain]/framework.md`

**Testing Structure:** EXPLORE-PLAN-CODE-COMMIT

---

## Detailed Test Plan

### Phase 1: EXPLORE (Already Complete)

**Completed Activities:**
- ✅ Read SCOPE.md
- ✅ Reconnaissance complete
- ✅ Attack surface mapped
- ✅ Tool inventory verified
- ✅ Framework baseline selected

**Key Findings from EXPLORE:**
- [Finding 1: e.g., Discovered 15 web applications]
- [Finding 2: e.g., Identified external API endpoints]
- [Finding 3: e.g., AWS infrastructure in scope]

---

### Phase 2: PLAN (This Document)

**Purpose:** Generate scope-driven test plan and get approval

**Status:** ⏳ Awaiting approval

---

### Phase 3: CODE (Execution Plan)

**CRITICAL:** Do NOT execute until this plan is approved.

---

## Test Cases by Asset

### Asset 1: [Application Name / URL]

**Asset Type:** [Web Application | API | Mobile App | Network | Cloud]
**URL/Location:** [https://example.com or IP address]
**Framework:** [OWASP Top 10 + API Top 10 | MITRE ATT&CK | MASVS | etc.]

#### Test Case 1.1: Authentication Testing

**Objective:** Test authentication mechanisms for bypass vulnerabilities

**Framework Mapping:**
- OWASP A07:2021 - Identification and Authentication Failures
- OWASP API2:2023 - Broken Authentication

**Tests to Perform:**
1. **Username Enumeration**
   - Test login error messages for user existence disclosure
   - Tools: Burp Intruder, manual testing
   - Expected Result: Generic error messages

2. **Password Policy Testing**
   - Test password complexity requirements
   - Test account lockout mechanisms
   - Tools: Manual testing
   - Expected Result: Strong password policy enforced

3. **Session Management**
   - Test session token entropy
   - Test session fixation vulnerabilities
   - Test session timeout
   - Tools: Burp Suite, manual testing
   - Expected Result: Secure session handling

4. **Multi-Factor Authentication**
   - Test MFA bypass techniques
   - Test MFA implementation
   - Tools: Manual testing
   - Expected Result: MFA properly enforced

**Evidence to Collect:**
- Screenshots of authentication flow
- Session tokens for analysis
- Error messages

**Time Estimate:** 2-3 hours

---

#### Test Case 1.2: Authorization Testing

**Objective:** Test for Broken Access Control (IDOR, BOLA, BFLA)

**Framework Mapping:**
- OWASP A01:2021 - Broken Access Control
- OWASP API1:2023 - BOLA (Broken Object Level Authorization)
- OWASP API5:2023 - BFLA (Broken Function Level Authorization)

**Tests to Perform:**
1. **IDOR (Insecure Direct Object References)**
   - Test user ID manipulation in URLs/APIs
   - Test access to other users' resources
   - Tools: Burp Suite, manual parameter manipulation
   - Expected Result: Proper authorization checks prevent access

2. **Horizontal Privilege Escalation**
   - Test accessing data of users at same privilege level
   - Tools: Burp Suite, multiple test accounts
   - Expected Result: Users cannot access each other's data

3. **Vertical Privilege Escalation**
   - Test accessing admin functions as regular user
   - Test role manipulation
   - Tools: Burp Suite, JWT manipulation
   - Expected Result: Admin functions properly protected

4. **Path Traversal**
   - Test file access via ../../../ manipulation
   - Tools: Manual testing, Burp Suite
   - Expected Result: Proper input validation prevents traversal

**Evidence to Collect:**
- Successful IDOR exploitation screenshots
- Requests/responses showing unauthorized access
- Proof of privilege escalation

**Time Estimate:** 3-4 hours

---

#### Test Case 1.3: Injection Testing

**Objective:** Test for injection vulnerabilities (SQL, NoSQL, Command, XSS)

**Framework Mapping:**
- OWASP A03:2021 - Injection

**Tests to Perform:**
1. **SQL Injection**
   - Test all input points for SQLi
   - Test in-band, blind, and time-based injection
   - Tools: SQLMap, Burp Suite, manual testing
   - Expected Result: Parameterized queries prevent injection

2. **NoSQL Injection**
   - Test NoSQL queries for injection (if MongoDB/etc used)
   - Tools: Burp Suite, NoSQLMap
   - Expected Result: Proper input sanitization

3. **Command Injection**
   - Test OS command injection in user inputs
   - Tools: Manual testing, Burp Suite
   - Expected Result: No command execution possible

4. **Cross-Site Scripting (XSS)**
   - Test reflected XSS
   - Test stored XSS
   - Test DOM-based XSS
   - Tools: Burp Suite, manual testing
   - Expected Result: Proper output encoding prevents XSS

**Evidence to Collect:**
- Injection payloads that succeeded
- Database outputs from SQLi
- XSS alert screenshots

**Time Estimate:** 4-5 hours

---

#### Test Case 1.4: Business Logic Testing

**Objective:** Test application-specific business logic for flaws

**Framework Mapping:**
- OWASP A04:2021 - Insecure Design

**Tests to Perform:**
1. **Workflow Bypass**
   - Test skipping payment steps
   - Test accessing restricted states
   - Tools: Manual testing, Burp Suite
   - Expected Result: Workflow enforced server-side

2. **Race Conditions**
   - Test simultaneous transactions
   - Test coupon/discount abuse
   - Tools: Burp Turbo Intruder
   - Expected Result: Proper transaction locking

3. **Price Manipulation**
   - Test modifying prices in requests
   - Test negative quantities
   - Tools: Burp Suite, manual testing
   - Expected Result: Server-side validation prevents manipulation

4. **Rate Limiting Bypass**
   - Test API rate limits
   - Test brute force protection
   - Tools: ffuf, Burp Intruder
   - Expected Result: Rate limiting enforced

**Evidence to Collect:**
- Screenshots of business logic bypass
- Requests showing manipulation
- Proof of race condition exploitation

**Time Estimate:** 3-4 hours

---

[Continue for all assets and test cases...]

---

### Asset 2: [Second Application/System]

[Same structure as Asset 1]

---

### Asset 3: [Third Application/System]

[Same structure as Asset 1]

---

## Network Penetration Testing Plan (if applicable)

### Network Scope

**IP Ranges:**
- [10.0.1.0/24] - Internal network
- [192.168.1.0/24] - DMZ

**Methodology:** MITRE ATT&CK Enterprise Framework

### Test Case N.1: Reconnaissance

**Objective:** Map network topology and identify live hosts

**ATT&CK Mapping:**
- TA0043 - Reconnaissance

**Tests:**
1. **Port Scanning**
   - Scan all in-scope IPs for open ports
   - Tools: Nmap, Masscan
   - Command: `nmap -sS -p- -T4 10.0.1.0/24`

2. **Service Enumeration**
   - Identify services and versions
   - Tools: Nmap service detection
   - Command: `nmap -sV -sC -p [ports] [targets]`

**Evidence:** Nmap scan results

**Time Estimate:** 2-3 hours

---

### Test Case N.2: Initial Access

**Objective:** Gain initial foothold on network

**ATT&CK Mapping:**
- TA0001 - Initial Access

**Tests:**
1. **Exploit Public-Facing Services**
   - Test for unpatched vulnerabilities in discovered services
   - Tools: Metasploit, Searchsploit, Nuclei
   - Focus: Web servers, SSH, RDP, SMB

2. **Valid Accounts**
   - Test default credentials on discovered services
   - Test password spraying (if authorized)
   - Tools: Hydra, CrackMapExec

**Evidence:** Screenshots of successful exploitation

**Time Estimate:** 4-6 hours

---

### Test Case N.3: Privilege Escalation

**Objective:** Escalate privileges on compromised systems

**ATT&CK Mapping:**
- TA0004 - Privilege Escalation

**Tests:**
1. **Windows Privilege Escalation**
   - Test for kernel exploits
   - Test for service misconfigurations
   - Tools: PowerUp, WinPEAS

2. **Linux Privilege Escalation**
   - Test sudo misconfigurations
   - Test SUID binaries
   - Tools: LinPEAS, linux-exploit-suggester

**Evidence:** Proof of root/SYSTEM access

**Time Estimate:** 3-4 hours

---

### Test Case N.4: Lateral Movement

**Objective:** Move through network to reach high-value targets

**ATT&CK Mapping:**
- TA0008 - Lateral Movement

**Tests:**
1. **Pass-the-Hash**
   - Test credential reuse across systems
   - Tools: Impacket, CrackMapExec

2. **Remote Services**
   - Test RDP/SSH access with compromised credentials
   - Tools: Native clients, xfreerdp

**Evidence:** Access to additional systems

**Time Estimate:** 3-4 hours

---

[Continue for all network testing phases...]

---

## Mobile Application Testing Plan (if applicable)

### Mobile Scope

**Applications:**
- [App Name] - Android [Version]
- [App Name] - iOS [Version]

**Methodology:** OWASP MASTG + MASVS

### Test Case M.1: Data Storage Testing

**Objective:** Identify insecure data storage

**MASVS Mapping:**
- MASVS-STORAGE

**Tests:**
1. **SharedPreferences / NSUserDefaults**
   - Extract local storage files
   - Check for sensitive data in plaintext
   - Tools: adb, Frida, Objection

2. **SQLite Databases**
   - Extract and analyze databases
   - Check for unencrypted sensitive data
   - Tools: sqlite3, DB Browser

**Evidence:** Screenshots of sensitive data found

**Time Estimate:** 2-3 hours

---

### Test Case M.2: Network Communication Testing

**Objective:** Test SSL/TLS implementation and certificate pinning

**MASVS Mapping:**
- MASVS-NETWORK

**Tests:**
1. **SSL Pinning Bypass**
   - Attempt to bypass certificate pinning
   - Tools: Frida, Objection, SSL Kill Switch
   - Expected Result: Pinning properly implemented

2. **Cleartext Traffic**
   - Check for unencrypted HTTP traffic
   - Tools: Burp Suite, mitmproxy
   - Expected Result: All traffic encrypted

**Evidence:** Burp Suite traffic capture

**Time Estimate:** 2-3 hours

---

[Continue for all mobile testing areas...]

---

## Cloud Security Testing Plan (if applicable)

### Cloud Scope

**Provider:** [AWS | Azure | GCP | Multi-cloud]
**Account/Subscription:** [Production account]

**Methodology:** Cloud Security Best Practices + CIS Benchmarks

### Test Case C.1: IAM Security

**Objective:** Assess identity and access management

**Tests:**
1. **Overly Permissive Policies**
   - Scan for wildcard permissions
   - Identify AdministratorAccess usage
   - Tools: ScoutSuite, Prowler

2. **MFA Enforcement**
   - Check MFA status for privileged accounts
   - Tools: AWS CLI, ScoutSuite

**Evidence:** ScoutSuite report

**Time Estimate:** 2-3 hours

---

### Test Case C.2: Data Exposure

**Objective:** Identify publicly accessible data

**Tests:**
1. **Public S3 Buckets**
   - Scan for public read/write access
   - Tools: ScoutSuite, aws-cli

2. **Unencrypted Storage**
   - Check encryption at rest settings
   - Tools: ScoutSuite, manual review

**Evidence:** List of public/unencrypted resources

**Time Estimate:** 2-3 hours

---

[Continue for all cloud testing areas...]

---

## Timeline & Resource Allocation

### Estimated Timeline

**Total Estimated Hours:** [XX hours]

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Web App Testing | 15-20 hours | None |
| API Testing | 10-15 hours | None |
| Network Testing | 12-16 hours | Requires internal access |
| Mobile Testing | 10-12 hours | App binaries needed |
| Cloud Testing | 8-10 hours | AWS credentials needed |
| Reporting | 8-10 hours | All testing complete |

**Project Timeline:**
- **Week 1:** Web/API testing
- **Week 2:** Network/Mobile/Cloud testing
- **Week 3:** Reporting and remediation guidance

### Resource Allocation

**Testing Team:**
- [Lead Tester]: Web/API/reporting
- [Tester 2]: Network/infrastructure
- [Tester 3]: Mobile/cloud

---

## Success Criteria

**Deliverables:**
- [ ] All test cases executed
- [ ] Findings documented with evidence
- [ ] Remediation guidance provided
- [ ] Final report delivered

**Quality Standards:**
- [ ] 100% accuracy (no fabricated results)
- [ ] Reproducible PoCs for all findings
- [ ] Clear remediation steps for each finding
- [ ] Professional PTES-compliant report

---

## Risk Assessment

### Testing Risks

**Potential Issues:**
1. **Service Disruption Risk:** [Low | Medium | High]
   - Mitigation: Test in off-hours, use rate limiting

2. **Data Corruption Risk:** [Low | Medium | High]
   - Mitigation: Read-only tests where possible, backup verification

3. **Account Lockout Risk:** [Low | Medium | High]
   - Mitigation: Coordinate with IT, test accounts provisioned

**Rollback Plan:**
- Emergency contact available: [Name, phone]
- Testing can be paused at any time
- Destructive tests require explicit approval

---

## Approval

**This test plan requires approval before execution begins.**

**Approved By:**
- **Name:** [Client contact name]
- **Title:** [Title]
- **Date:** [YYYY-MM-DD]
- **Signature:** [Digital or physical signature]

**Modifications:**
- Any changes to this plan require re-approval
- Scope creep must be documented and approved

---

## Post-Testing

**After CODE Phase:**
- [ ] Findings documented (using FINDING-TEMPLATE.md)
- [ ] Evidence collected and organized
- [ ] Fix proposals generated (using FIX-PROPOSAL-TEMPLATE.md)
- [ ] Final report compiled (using PENTEST-REPORT-TEMPLATE.md)

**Verification Testing:**
- [ ] Re-test after fixes applied
- [ ] Confirm all findings remediated
- [ ] Document remediation status

---

**Plan Status:** [Draft | Awaiting Approval | Approved | In Progress | Complete]

**Last Updated:** [YYYY-MM-DD HH:MM UTC]

**Version:** [1.0]
