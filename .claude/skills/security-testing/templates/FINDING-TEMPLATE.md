
## Finding Summary

**Finding ID:** [AUTO-GENERATE: YYYY-MM-DD-XXX or use tracker ID]
**Title:** [Clear, concise vulnerability title]
**Discovered:** [YYYY-MM-DD]
**Status:** [Open | In Progress | Remediated | Accepted Risk]
**Severity:** [Critical | High | Medium | Low | Informational]

**One-Line Summary:**
[Single sentence describing the vulnerability and impact]

---

## Target Information

**Application/System:** [Application name or system identifier]
**URL/Endpoint:** [Specific URL, API endpoint, or system location]
**IP Address:** [If applicable]
**Version:** [Application/software version tested]
**Component:** [Specific component, module, or feature affected]
**Environment:** [Production | Staging | Development | Test]

**Testing Context:**
- **Test Type:** [Penetration Test | Bug Bounty | Vulnerability Scan | Code Review]
- **Authorization:** [Authorized testing with written approval | Bug bounty program in-scope]
- **Test Date:** [YYYY-MM-DD]

---

## Vulnerability Classification

**Category:** [Choose primary category]
- OWASP Top 10: [A01-A10 if web/API]
- OWASP API Top 10: [API1-API10 if API-specific]
- OWASP Mobile: [MASVS-STORAGE, MASVS-CRYPTO, etc. if mobile]
- MITRE ATT&CK: [Technique ID if network/infrastructure]
- Immunefi Top 10: [V01-V10 if Web3/smart contract]
- CWE: [CWE-XXX if applicable]

**CVSS Score:** [X.X/10.0] ([Calculator link if available])

---

## Severity Assessment

**Severity: [Critical | High | Medium | Low | Informational]**

**Severity Justification:**
- **Exploitability:** [Easy | Moderate | Difficult | Very Difficult]
- **Impact:** [Critical | High | Medium | Low]
- **Affected Users:** [All users | Authenticated users | Administrators only | Specific subset]
- **Data at Risk:** [PII | Financial | Credentials | Application data | Configuration]
- **Business Impact:** [Service disruption | Data breach | Financial loss | Reputation damage | Compliance violation]

**Risk Rating Matrix:**
```
Likelihood: [High | Medium | Low]
Impact: [Critical | High | Medium | Low]
Risk = Likelihood × Impact = [SEVERITY]
```

---

## Detailed Description

### What is the Vulnerability?

[Clear technical description of the vulnerability. Explain WHAT is broken, WHY it's exploitable, and HOW it manifests.]

**Key Technical Details:**
- [Specific technical flaw]
- [Root cause analysis]
- [Why default security controls failed]

### Why Does This Matter?

[Business impact explanation. What can an attacker achieve? What data/systems are at risk?]

**Potential Attacker Goals:**
1. [Primary attacker objective]
2. [Secondary consequences]
3. [Worst-case scenario]

---

## Proof of Concept (PoC)

**CRITICAL RULES:**
- ✅ Include EXACT reproduction steps (step-by-step)
- ✅ Include actual evidence (screenshots, logs, HTTP requests/responses)
- ✅ 100% reproducible by anyone following these steps
- ❌ NO fabricated results
- ❌ NO assumptions or guesses
- ❌ NO "this probably works" statements

### Reproduction Steps

**Prerequisites:**
- [Tools required: Burp Suite, curl, browser, etc.]
- [Access level required: Unauthenticated, authenticated user, admin]
- [Test account credentials if needed]

**Step-by-Step Reproduction:**

1. **Step 1:** [Exact action]
   ```
   [Command, request, or action]
   ```
   **Expected:** [What should happen normally]
   **Actual:** [What actually happened]

2. **Step 2:** [Next action]
   ```
   [Command, request, or action]
   ```

3. **Step 3:** [Continue...]
   ```
   [Command, request, or action]
   ```

**Final Result:**
[Describe successful exploitation outcome]

### Evidence

**Request:**
```http
[Actual HTTP request if web/API]
POST /api/users/123/profile HTTP/1.1
Host: target.com
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 456,
  "role": "admin"
}
```

**Response:**
```http
[Actual HTTP response]
HTTP/1.1 200 OK
{
  "success": true,
  "message": "User 456 role updated to admin"
}
```

**Screenshots:**
- [Screenshot 1: Before exploitation]
- [Screenshot 2: During exploitation]
- [Screenshot 3: After exploitation showing impact]

**Logs/Output:**
```
[Relevant log entries or command output demonstrating vulnerability]
```

---

## Attack Scenarios

### Scenario 1: [Primary Attack Vector]

**Attacker Profile:** [External unauthenticated attacker | Authenticated user | Malicious insider]

**Attack Steps:**
1. [Attacker action 1]
2. [Attacker action 2]
3. [Attacker action 3]

**Outcome:**
[What attacker achieves]

**Impact:**
- [Business impact]
- [Data compromised]
- [Systems affected]

### Scenario 2: [Secondary Attack Vector or Chained Attack]

[If applicable, describe alternative attack paths or how this vulnerability chains with others]

---

## Impact Analysis

### Technical Impact

**Confidentiality:** [None | Low | Medium | High]
- [What data can be accessed]

**Integrity:** [None | Low | Medium | High]
- [What data/systems can be modified]

**Availability:** [None | Low | Medium | High]
- [What services can be disrupted]

### Business Impact

**Financial:**
- [Direct costs: data breach fines, incident response]
- [Indirect costs: reputation damage, customer churn]

**Compliance:**
- [GDPR | PCI DSS | HIPAA | SOC 2 violations]
- [Regulatory reporting requirements]

**Operational:**
- [Service downtime]
- [Customer impact]
- [Brand reputation]

---

## Root Cause Analysis

**Why Does This Vulnerability Exist?**

[Technical root cause - coding error, misconfiguration, design flaw, etc.]

**Contributing Factors:**
1. [Primary cause: e.g., Missing input validation]
2. [Secondary cause: e.g., Lack of server-side authorization checks]
3. [Underlying issue: e.g., Insufficient security testing in development]

**Security Control Failures:**
- [Which security controls should have prevented this?]
- [Why did those controls fail?]

---

## Remediation Guidance

### Immediate Workarounds (Stop Bleeding NOW)

**Option 1: [Quick mitigation - can be applied in minutes/hours]**
```
[Exact workaround steps or config changes]
```
**Impact:** [What this breaks, if anything]
**Risk Reduction:** [Reduces risk from X to Y]

**Option 2: [Alternative immediate mitigation]**
```
[Steps]
```

### Short-Term Fix (Code/Config Changes)

**Recommended Fix:**
```[language]
// BEFORE (vulnerable code)
[Show actual vulnerable code if available]

// AFTER (fixed code)
[Proposed secure implementation]
```

**Configuration Changes:**
```
[Exact config file changes needed]
```

**Implementation Steps:**
1. [Step 1 to apply fix]
2. [Step 2]
3. [Step 3]

**Testing After Fix:**
```
[How to verify fix works - re-run PoC, should fail]
```

### Long-Term Solutions (Architectural Improvements)

**Recommended Improvements:**
1. [Systemic improvement 1]
2. [Improvement 2]
3. [Improvement 3]

**Security Best Practices:**
- [Industry standard approach]
- [Reference OWASP Cheat Sheet / NIST guidance]

---

## Proposed Implementation (Ready to Apply)

**CRITICAL:** This section contains ACTUAL code/config changes ready for approval and implementation.

### Code Changes

**File:** `[path/to/file.ext]`

**Change:**
```diff
- [Line to remove or change]
+ [Line to add or replacement]
```

**Full Context:**
```[language]
[Show surrounding code for context]

// SECURE IMPLEMENTATION
[Complete fixed code block]
```

### Configuration Changes

**File:** `[config/file.conf]`

**Change:**
```diff
- setting = insecure_value
+ setting = secure_value
```

### Deployment Steps

1. **Backup:** Create backup of current code/config
2. **Apply:** Deploy changes to staging first
3. **Test:** Run verification tests (see Verification section)
4. **Deploy:** Roll out to production with rollback plan
5. **Monitor:** Watch for errors/issues for 24-48 hours

**Rollback Plan:**
```
[Steps to revert if fix causes issues]
```

---

## Verification & Testing

### How to Verify Fix is Effective

**Re-run Original PoC (Should FAIL):**
```
[Original exploit attempt]
Expected Result: [Should be blocked / return error]
```

**Positive Tests (Legitimate Use Still Works):**
1. [Test legitimate functionality still works]
2. [Ensure no regression]

**Negative Tests (Bypass Attempts Should Fail):**
1. [Try variant 1 of exploit - should fail]
2. [Try variant 2 of exploit - should fail]

### Verification Checklist

- [ ] Original PoC no longer works
- [ ] Legitimate functionality unaffected
- [ ] No new vulnerabilities introduced
- [ ] Security controls functioning as expected
- [ ] Logs capture blocked attempts
- [ ] No performance degradation

---

## References

**Framework Mappings:**
- OWASP: [Link to relevant OWASP resource]
- MITRE ATT&CK: [Technique link if applicable]
- CWE: [Link to CWE entry]

**Secure Coding Guidelines:**
- [OWASP Cheat Sheet link]
- [Language-specific security guide]
- [Framework security documentation]

**Similar Vulnerabilities:**
- [Link to similar disclosed vulnerabilities]
- [CVE references if applicable]

**Tools Used:**
- [Tool 1: Version X.Y]
- [Tool 2: Version X.Y]

---

## Timeline

- **Discovered:** [YYYY-MM-DD HH:MM UTC]
- **Reported:** [YYYY-MM-DD HH:MM UTC]
- **Acknowledged:** [YYYY-MM-DD HH:MM UTC]
- **Fix Proposed:** [YYYY-MM-DD HH:MM UTC]
- **Fix Applied:** [YYYY-MM-DD HH:MM UTC]
- **Verified:** [YYYY-MM-DD HH:MM UTC]
- **Status Changed to Remediated:** [YYYY-MM-DD HH:MM UTC]

---

## Credits

**Discovered By:** [Your name / team]
**Reported By:** [Your name / team]
**Remediation Assistance:** [If you implemented the fix]

---

## Notes

[Any additional context, limitations, or considerations]

---

**Finding Status: [OPEN]**

**Last Updated:** [YYYY-MM-DD HH:MM UTC]
