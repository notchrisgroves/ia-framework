
## Submission Information

**Program:** [Company Name Bug Bounty Program]
**Asset:** [URL / App / API endpoint]
**Severity:** [Critical | High | Medium | Low | None]
**Weakness:** [CWE-XXX: Description]
**CVSS Score:** [X.X] ([Link to calculator if provided])

---

## Summary

[One clear sentence describing the vulnerability]

**Example:**
> "An SQL injection vulnerability in the /api/user/search endpoint allows unauthenticated attackers to extract the entire user database including password hashes."

---

## Description

### What is the vulnerability?

[2-3 sentences explaining the technical flaw]

### Where is it located?

**Affected Component:**
- **URL:** [Exact URL or endpoint]
- **Parameter:** [Vulnerable parameter name]
- **Method:** [GET | POST | PUT | DELETE]
- **Version:** [If applicable]

### Why is this a security issue?

[Explain the impact - what can an attacker do with this?]

---

## Steps to Reproduce

**CRITICAL:** Steps must be 100% reproducible. Test multiple times before submitting.

**Prerequisites:**
- [Account type required: none, free account, premium account]
- [Tools needed: browser, Burp Suite, curl, etc.]

**Step-by-Step:**

1. [Exact step 1]
   ```
   [Command or action if applicable]
   ```

2. [Exact step 2]
   ```
   [Command or action]
   ```

3. [Exact step 3]
   ```
   [Command or action]
   ```

4. **Observe:** [What happens - the vulnerability is triggered]

**Expected Result:** [What should happen normally]

**Actual Result:** [What actually happens - demonstrates the vulnerability]

---

## Proof of Concept

### HTTP Request (if applicable)

```http
POST /api/user/search HTTP/1.1
Host: vulnerable-site.com
Content-Type: application/json
Cookie: session=abc123

{
  "query": "admin' OR '1'='1"
}
```

### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "users": [
    {"id": 1, "username": "admin", "email": "admin@site.com", "password_hash": "..."},
    {"id": 2, "username": "user1", "email": "user1@site.com", "password_hash": "..."},
    [...]
  ]
}
```

### Screenshots

[Attach screenshots showing]:
1. **Before exploitation** - Normal behavior
2. **During exploitation** - Malicious input
3. **After exploitation** - Impact demonstrated

**Screenshot Guidelines:**
- Blur/redact sensitive data (real user emails, PII)
- Show full context (URL bar, request/response)
- High quality, readable

### Video (if complex)

[Link to unlisted YouTube/Vimeo video demonstrating exploitation]
- Keep video < 5 minutes
- Narrate steps clearly
- Show terminal/browser clearly

---

## Impact

### What can an attacker achieve?

[Describe realistic attack scenarios]

**Primary Impact:**
- [Impact 1: e.g., Access to all user data]
- [Impact 2: e.g., Account takeover for any user]

**Secondary Impact:**
- [Impact 3: e.g., Potential for privilege escalation]
- [Impact 4: e.g., Reputation damage]

### Affected Users

- [All users | Authenticated users | Specific subset]
- **Scale:** [Number of potentially affected users/accounts]

### Business Impact

- **Data at Risk:** [PII | Financial | Credentials | etc.]
- **Compliance:** [GDPR | PCI DSS | HIPAA violations]
- **Reputation:** [Public disclosure risk, customer trust]

---

## Severity Justification

**My Assessment:** [Critical | High | Medium | Low]

**Reasoning:**
- **Exploitability:** [Easy with basic tools | Requires specific conditions | Difficult]
- **Impact:** [Complete compromise | Significant data exposure | Limited exposure]
- **Scope:** [Affects all users | Affects authenticated users | Affects specific subset]
- **Attack Complexity:** [Low | Medium | High]

**CVSS v3.1 Vector:**
```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
Score: X.X (High)
```

---

## Suggested Fix

[Provide remediation guidance - helps triage team]

**Short-Term Mitigation:**
```
[Quick workaround they can apply immediately]
```

**Long-Term Fix:**
```
[Recommended secure implementation]
Example:
- Use parameterized queries instead of string concatenation
- Implement input validation with whitelist approach
- Add rate limiting to prevent brute force
```

**Reference:**
- [OWASP Cheat Sheet link]
- [CWE Mitigation guide]

---

## Supporting Material

**References:**
- [Similar disclosed vulnerabilities]
- [OWASP Testing Guide section]
- [CWE entry]
- [Research papers or blog posts explaining the attack]

**Tools Used:**
- [Tool 1: Version]
- [Tool 2: Version]

---

## Disclosure Timeline

**Discovery Date:** [YYYY-MM-DD]
**Submission Date:** [YYYY-MM-DD]
**Test Environment:** [Production | Staging | Reported as noted]

---

## Additional Notes

[Any additional context that helps with validation]

**Important:**
- [Note if this could chain with other vulnerabilities]
- [Note if you found similar issues elsewhere in the application]
- [Note any concerns about testing (e.g., "I stopped testing to avoid data corruption")]

---

## Triage Checklist (Self-Review Before Submitting)

Before clicking "Submit," verify:

- [ ] **Reproducible:** I tested this 3+ times successfully
- [ ] **Clear Steps:** Anyone can follow my reproduction steps
- [ ] **Evidence:** I provided screenshots/requests/responses
- [ ] **Accurate:** All information is 100% factual (no speculation)
- [ ] **In-Scope:** Asset is listed in program scope
- [ ] **Not a Duplicate:** I searched for similar reports first
- [ ] **Respectful:** Professional tone, no threats/demands
- [ ] **Complete:** All sections filled out
- [ ] **Redacted:** Removed any real PII/sensitive data from evidence
- [ ] **Rules Followed:** I followed the program's testing rules

---

## Submission Tips

**DO:**
- ✅ Be clear and concise
- ✅ Provide complete reproduction steps
- ✅ Include evidence (screenshots, logs, requests)
- ✅ Explain the impact in business terms
- ✅ Suggest fixes (shows expertise)
- ✅ Be patient with triage team
- ✅ Respond promptly to questions

**DON'T:**
- ❌ Speculate or guess about impact
- ❌ Test beyond what's needed to prove vulnerability
- ❌ Submit vague reports hoping for a bounty
- ❌ Be rude or demanding
- ❌ Threaten public disclosure
- ❌ Submit duplicates
- ❌ Test out-of-scope assets

---

## Platform-Specific Notes

### HackerOne

**Severity Scale:** None | Low | Medium | High | Critical

**Fields Required:**
- Title
- Vulnerability Type (CWE)
- Description
- Steps to Reproduce
- Impact
- Severity

**Markdown Supported:** Yes (use code blocks, headers, lists)

### Bugcrowd

**Severity Scale:** P1 (Critical) | P2 (High) | P3 (Medium) | P4 (Low) | P5 (Info)

**Fields Required:**
- Title
- Description
- Proof of Concept
- Impact
- Priority

**Markdown Supported:** Yes

### Intigriti

**Severity Scale:** Critical | High | Medium | Low | Info

**Fields Required:**
- Description
- Reproduction Steps
- Impact
- Remediation

**Markdown Supported:** Yes

### YesWeHack

**Severity Scale:** Critical | High | Medium | Low | Info

**Fields Required:**
- Summary
- Technical Environment
- Reproduction
- Impact
- Remédiation (Remediation)

**Markdown Supported:** Limited

---

## Example Submission (Complete)

**Program:** Acme Corp Bug Bounty
**Asset:** https://app.acme.com
**Severity:** High
**Weakness:** CWE-89: SQL Injection

### Summary

SQL injection in the user search API endpoint allows authenticated users to extract sensitive data from the database.

### Description

The `/api/v1/users/search` endpoint is vulnerable to SQL injection due to insufficient input sanitization. The `query` parameter is directly concatenated into a SQL statement without proper escaping or parameterization.

**Affected Component:**
- **URL:** https://app.acme.com/api/v1/users/search
- **Parameter:** `query` (POST body)
- **Method:** POST
- **Authentication:** Required (free account)

An attacker can exploit this vulnerability to extract database contents, including user credentials, PII, and other sensitive data.

### Steps to Reproduce

1. Create a free account at https://app.acme.com/signup
2. Log in and navigate to the user search feature
3. Open Burp Suite and intercept the search request
4. Modify the `query` parameter to: `admin' OR '1'='1' --`
5. Forward the request

**Expected:** Should return only users matching "admin"
**Actual:** Returns all users in the database due to SQL injection

### Proof of Concept

**Request:**
```http
POST /api/v1/users/search HTTP/1.1
Host: app.acme.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "query": "admin' OR '1'='1' --"
}
```

**Response:**
```json
{
  "success": true,
  "count": 1247,
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@acme.com",
      "created_at": "2020-01-15"
    },
    {
      "id": 2,
      "username": "user_001",
      "email": "user001@example.com",
      "created_at": "2020-02-20"
    },
    [... 1245 more users ...]
  ]
}
```

[Screenshot showing full response with 1247 users returned]

### Impact

An authenticated attacker can:
1. Extract the entire user database (1200+ users)
2. Access emails and usernames for account enumeration
3. Potentially extract password hashes with UNION-based injection
4. Escalate to RCE if database user has elevated privileges

**Affected Users:** All 1200+ registered users
**Data at Risk:** PII, account information, potential credential exposure
**Compliance Impact:** GDPR Article 32 violation (inadequate security measures)

### Severity Justification

**Assessment:** High

- **Exploitability:** Easy - requires only free account and Burp Suite
- **Impact:** High - complete user database exposure
- **Scope:** All users affected
- **Attack Complexity:** Low

**CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N**
**Score: 6.5 (Medium) - Recommend High due to scale**

### Suggested Fix

**Immediate Mitigation:**
- Implement WAF rule to block common SQL injection patterns
- Add rate limiting to the endpoint

**Long-Term Fix:**
```python
# VULNERABLE CODE (before)
query = f"SELECT * FROM users WHERE username LIKE '%{user_input}%'"

# SECURE CODE (after)
query = "SELECT * FROM users WHERE username LIKE %s"
cursor.execute(query, (f"%{user_input}%",))
```

Use parameterized queries throughout the application.

**Reference:**
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

### Supporting Material

- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- OWASP A03:2021 Injection: https://owasp.org/Top10/A03_2021-Injection/

### Disclosure Timeline

- **Discovery:** 2025-12-01
- **Submission:** 2025-12-01

---

**Submission Complete** ✓

---

**Note:** This template follows industry best practices for responsible vulnerability disclosure. Always follow the program's rules and code of conduct.
