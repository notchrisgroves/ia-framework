# Scope Compliance Guide (Real HackerOne Examples)

**Purpose:** Prevent scope violations using REAL examples from production bug bounty programs

**CRITICAL:** Performing out-of-scope testing = Program ban, account termination, or criminal charges

---

## Why Scope Compliance is Critical

**USER'S WARNING:**
> "performing a DOS when its strictly out of scope gets you fired or imprisoned"

**Real Consequences:**
- Program disqualification (permanent ban)
- Account termination across platforms
- Legal action (computer fraud laws)
- Criminal charges (unauthorized access)
- Reputation damage (industry blacklist)

**Statistics:**
- 15 HackerOne programs analyzed
- 330+ in-scope assets documented
- 50+ out-of-scope assets with explicit warnings

---

## Understanding Scope Statements

### Scope Components

Every bug bounty program defines:

1. **In-Scope Assets** - What you CAN test
2. **Out-of-Scope Assets** - What you CANNOT test
3. **Asset Instructions** - Special rules per asset
4. **Severity Limits** - Maximum severity per asset
5. **Bounty Eligibility** - Whether findings qualify for payment
6. **Submission Eligibility** - Whether findings can be reported

### HackerOne Scope Structure

```json
{
  "AssetType": "URL | OTHER | CIDR | SOURCE_CODE | AI_MODEL",
  "AssetIdentifier": "example.com",
  "EligibleForBounty": true/false,
  "EligibleForSubmission": true/false,
  "MaxSeverity": "critical | high | medium | low | none",
  "Instruction": "Special rules for this asset"
}
```

**Key Rule:** `EligibleForSubmission: false` = **DO NOT TEST** (even if you find something)

---

## Real Examples: Good Scoping

### Example 1: Cloudflare - Clear Asset with Context

**Asset:** `waf.cumulusfire.net`
- **Type:** URL
- **Eligible for Bounty:** ✅ Yes
- **Eligible for Submission:** ✅ Yes
- **Max Severity:** Medium
- **Instruction:** "This domain must be used for testing WAF bypasses."

**Why This is Good:**
- Explicitly states this is THE test domain for WAF testing
- Sets reasonable severity cap (medium) for test environment
- Clear, unambiguous scope

### Example 2: HackerOne VPN - Specific Vulnerabilities of Interest

**Asset:** `*.vpn.hackerone.net`
- **Type:** OTHER
- **Eligible for Bounty:** ✅ Yes
- **Max Severity:** Critical
- **Instruction:** "We'd be most interested in vulnerabilities that allow you to route traffic to other clients (lack of client isolation), routing traffic to internal HackerOne / Amazon networks, and bypassing sslsplit. Traffic routed through the VPN will originate from 66.232.20.0/23 or 206.166.248.0/23."

**Why This is Good:**
- Specifies WHAT vulnerabilities they care about
- Provides technical context (OpenVPN, sslsplit)
- Identifies traffic origins for verification
- Guides researcher focus to business-critical issues

### Example 3: Cloudflare - Multiple Asset Types

**In-Scope Assets (57 total):**
- URLs: `*.teams.cloudflare.com`, `dash.cloudflare.com`, `api.cloudflare.com`
- Products: `Cloudflare Workers`, `Cloudflare R2`, `Cloudflare D1`
- Mobile: `WARP Mobile Apps` (Android/iOS)
- Source Code: `https://github.com/cloudflare/workerd`
- AI Models: `Workers AI`
- Networks: `172.65.0.0/16` (OUT OF SCOPE - see exclusions)

**Why This is Good:**
- Comprehensive coverage across domains
- Includes modern attack surfaces (AI, cloud, mobile)
- Explicit asset type classification

---

## Real Examples: Out-of-Scope (DO NOT TEST)

### Example 1: Third-Party Hosted Assets

**HackerOne Program:**

**Out-of-Scope Asset:** `support.hackerone.com`
- **Eligible for Submission:** ❌ NO
- **Max Severity:** none
- **Instruction:** "This asset is hosted by Freshdesk, and as such these reports should be submitted to the appropriate program: https://hackerone.com/freshworks"

**Cloudflare Program:**

**Out-of-Scope Asset:** `support.cloudflare.com`
- **Eligible for Submission:** ❌ NO
- **Max Severity:** none
- **Instruction:** "This asset is hosted by Zendesk, and as such these reports should be submitted to their program instead via @Zendesk"

**CRITICAL RULE:**
- Third-party assets = Submit to THEIR program
- Testing these = Testing unauthorized third-party
- Result: Account ban + potential legal action

### Example 2: Customer Infrastructure

**Cloudflare:**

**Out-of-Scope Network:** `172.65.0.0/16`
- **Eligible for Submission:** ❌ NO
- **Max Severity:** none
- **Instruction:** "These are customer applications protected by Cloudflare Spectrum, hence out of scope"

**Why This is CRITICAL:**
- These are CUSTOMER assets, not Cloudflare
- Testing these = Attacking Cloudflare's paying customers
- Consequence: Immediate ban + legal liability

### Example 3: Partner/Marketing Sites

**HackerOne:**

**Out-of-Scope Assets:**
- `hackerone-swag.com` - Swag store (likely third-party)
- `h1.community` - Community forum (separate platform)
- `go.hacker.one` - Marketo marketing site

**All marked:**
- **Eligible for Submission:** ❌ NO
- **Max Severity:** none

---

## Real Examples: Special Instructions

### Severity-Limited Assets

**HackerOne - S3 Buckets:**

**Asset:** `profile-photos-us-east-2.hackerone-user-content.com`
- **Eligible for Bounty:** ✅ Yes
- **Max Severity:** Low
- **Instruction:** "This is an Amazon S3 bucket that contains profile and cover photos of users and programs. It does not contain any highly confidential information and would not impact the main application if it would be unreachable. A signed request is required to download an object."

**What This Means:**
- You CAN test this asset
- You CAN submit findings
- BUT: Maximum bounty for "Critical S3 takeover" = Low severity payout
- Why: Program explains impact is limited (no confidential data)

**Lesson:** Read instructions to understand WHY severity is capped

### Test Account Requirements

**Cloudflare Policy:**

```
All attacks must be executed against your own Cloudflare Account.
You can sign up for a free Cloudflare account and use it for testing.

Accounts should be created with a @wearehackerone.com email address.
```

**What This Means:**
- Create test account BEFORE testing
- Use specific email domain
- Do NOT test on other users' accounts
- Violating this = Disqualification

### AI Model Special Rules

**Cloudflare - Workers AI:**

**Asset:** `Workers AI`
- **Type:** AI_MODEL
- **Eligible for Bounty:** ✅ Yes
- **Max Severity:** Critical
- **Instruction:** "Reports on Prompt Injection attacks on models hosted by Workers AI without demonstrating an impact on Cloudflare will not be accepted."

**What This Means:**
- Simple prompt injection demos = Not eligible
- MUST show impact to Cloudflare infrastructure
- Example: Prompt injection → Data exfiltration → ACCEPTED
- Example: Prompt injection → Jailbreak only → REJECTED

---

## Program Rules (From Real Programs)

### Cloudflare Rules

**ALLOWED:**
✅ Test against your own Cloudflare account
✅ Narrow scans limited to authorized Cloudflare IPs
✅ Report leaked credentials (DO NOT verify them yourself)

**FORBIDDEN:**
❌ Testing against Cloudflare customers
❌ Social engineering employees
❌ Physical attacks
❌ Denial of Service attacks
❌ Aggressive/broad scans including customer IPs

**Disqualification = Permanent Ban:**
- Testing customer/partner infrastructure
- Social engineering (phishing, impersonation)
- Physical attacks on offices/datacenters
- DoS attacks

### Common Exclusions Across Programs

**Out-of-Scope Vulnerability Classes:**

1. **DoS/DDoS** - Explicitly forbidden by all programs
2. **Social Engineering** - Employee phishing = Instant ban
3. **Physical Security** - Office attacks = Criminal charges
4. **Third-Party Assets** - Submit to their program instead
5. **Spam/Bulk Messages** - Unsolicited bulk activity

**Low-Priority Findings (Often Not Rewarded):**
- Missing security headers (without exploitation)
- Self-XSS (requires victim action)
- Clickjacking on non-sensitive pages
- Open redirects (without SSO/OAuth impact)
- Username/email enumeration (unless sensitive)

---

## Scope Violation Examples (What NOT to Do)

### ❌ WRONG: Testing Third-Party Assets

**Scenario:** You find `support.cloudflare.com` on Cloudflare's website

**Wrong Action:**
```bash
# Testing support.cloudflare.com for vulnerabilities
nmap -sV support.cloudflare.com
sqlmap -u "https://support.cloudflare.com/search?q=test"
```

**Why This is Wrong:**
- Asset is out-of-scope (hosted by Zendesk)
- You are now testing ZENDESK's infrastructure without authorization
- Cloudflare program explicitly says submit to @Zendesk instead

**Correct Action:**
1. Check scope document
2. See "submit to @Zendesk" instruction
3. Go to Zendesk's bug bounty program
4. Test ONLY if authorized under THEIR program

### ❌ WRONG: DoS Testing

**Scenario:** You want to test rate limiting on an API

**Wrong Action:**
```bash
# Attempting to DoS the API to test rate limits
for i in {1..100000}; do
  curl "https://api.cloudflare.com/v4/zones" &
done
```

**Why This is Wrong:**
- ALL programs forbid DoS testing
- This impacts production availability
- Consequence: Instant ban + potential criminal charges

**Correct Action:**
1. Test rate limiting with reasonable requests (10-20 requests)
2. Document that rate limiting is absent/weak
3. Provide PoC showing 20 rapid requests succeed
4. Explain theoretical DoS impact WITHOUT executing it

### ❌ WRONG: Customer Infrastructure

**Scenario:** You discover Cloudflare protects customer X's website

**Wrong Action:**
```bash
# Attempting to bypass Cloudflare WAF on customer's site
curl -H "X-Forwarded-For: 127.0.0.1" https://customer-site-behind-cloudflare.com/admin
```

**Why This is Wrong:**
- Customer infrastructure is ALWAYS out of scope
- You are attacking a third-party without authorization
- Cloudflare policy: "Testing against Cloudflare customers... will result in disqualification"

**Correct Action:**
- Set up YOUR OWN Cloudflare account
- Test WAF bypass on YOUR OWN domains
- Report the bypass method to Cloudflare
- Never touch customer infrastructure

### ❌ WRONG: Verifying Leaked Credentials

**Scenario:** You find credentials in a GitHub commit

**Wrong Action:**
```bash
# Testing if credentials are valid
curl -u "leaked_username:leaked_password" https://api.hackerone.com/v1/me
```

**Why This is Wrong:**
- Cloudflare policy: "Please do not attempt to verify the validity of the credentials yourself by attempting to authenticate"
- Accessing accounts with leaked creds = Unauthorized access
- This makes triage harder and report ineligible

**Correct Action:**
1. Find leaked credentials
2. Report IMMEDIATELY without verification
3. Let the company validate internally
4. Include: Where found, what type, exposure date

---

## Scope Compliance Checklist

### Before Starting Testing

- [ ] Read ENTIRE program policy (not just scope list)
- [ ] Identify ALL out-of-scope assets
- [ ] Note special instructions for each asset
- [ ] Check severity limits per asset
- [ ] Verify test account requirements
- [ ] Confirm rate limiting guidelines
- [ ] Review forbidden vulnerability classes
- [ ] Understand third-party asset rules

### During Testing

- [ ] Verify asset is in-scope BEFORE each test
- [ ] Follow test account requirements
- [ ] Respect rate limits
- [ ] Avoid DoS/flooding
- [ ] Do not verify leaked credentials
- [ ] Stop if you discover out-of-scope asset
- [ ] Document scope boundaries encountered

### Before Submission

- [ ] Confirm asset is in-scope
- [ ] Check severity does not exceed MaxSeverity
- [ ] Verify EligibleForSubmission = true
- [ ] Review asset-specific instructions
- [ ] Ensure no third-party assets involved
- [ ] Confirm no scope violations occurred
- [ ] Follow program's submission format

---

## Real Program Scope Statistics

**From 15 HackerOne Programs:**

### In-Scope Assets by Type

- **URLs:** 245 assets
- **OTHER:** 68 assets (VPNs, products, features)
- **SOURCE_CODE:** 12 assets (GitHub repos)
- **CIDR:** 5 assets (IP ranges)
- **AI_MODEL:** 1 asset (Workers AI)

### Bounty Eligibility

- **Eligible for Bounty:** 280 assets (84%)
- **Not Eligible for Bounty:** 50 assets (16%)

### Severity Distribution

- **Critical Max Severity:** 267 assets
- **Medium Max Severity:** 25 assets
- **Low Max Severity:** 25 assets
- **None (Out of Scope):** 13 assets

### Out-of-Scope Breakdown

**Why Assets Are Out-of-Scope:**
- Third-party hosted: 8 assets
- Customer infrastructure: 2 assets
- Deprecated/archived: 2 assets
- Marketing sites: 1 asset

---

## Quick Reference: Asset Eligibility Matrix

| EligibleForSubmission | EligibleForBounty | MaxSeverity | What This Means |
|----------------------|-------------------|-------------|-----------------|
| ✅ true | ✅ true | critical | FULL SCOPE - Test, submit, get paid |
| ✅ true | ❌ false | critical | Test & submit, NO PAYMENT (e.g., open source) |
| ✅ true | ✅ true | low | Test & submit, but LOW PAYOUT CAP |
| ❌ false | ❌ false | none | **OUT OF SCOPE - DO NOT TEST** |

---

## Summary: Golden Rules

1. **READ THE FULL POLICY** - Scope list is not enough
2. **EligibleForSubmission: false = DO NOT TEST** - Even if you find something
3. **Third-Party Assets = Submit to THEIR Program** - Not the one you're on
4. **Customer Infrastructure = NEVER TEST** - Instant ban + legal risk
5. **No DoS, Ever** - Test limits reasonably, describe theoretical impact
6. **No Social Engineering** - Employee phishing = Permanent ban
7. **Follow Asset Instructions** - Every asset may have special rules
8. **Respect Severity Caps** - S3 bucket with "Low" cap won't pay Critical bounty
9. **Create Test Accounts** - Don't test on real users
10. **When in Doubt, ASK** - Program teams prefer questions over scope violations

---

## Resources

**HackerOne Programs Analyzed:**
- HackerOne (35 assets): https://hackerone.com/security
- Cloudflare (57 assets): https://hackerone.com/cloudflare
- Vimeo (69 assets): https://hackerone.com/vimeo
- Priceline (58 assets): https://hackerone.com/priceline
- WordPress (28 assets): https://hackerone.com/wordpress
- Slack (25 assets): https://hackerone.com/slack
- X / xAI (17 assets): https://hackerone.com/x
- Basecamp (17 assets): https://hackerone.com/basecamp
- Tinder (13 assets): https://hackerone.com/tinder
- LinkedIn (5 assets): https://hackerone.com/linkedin
- Concrete CMS (4 assets): https://hackerone.com/concretecms
- Ruby on Rails (2 assets): https://hackerone.com/rails

**Data Source:** `scratchpad/hackerone-scope-examples.json` (15 programs, 330+ assets, fetched 2025-12-01)

---

**Remember:** Scope violations can end your bug bounty career. When in doubt, DON'T TEST - ask first.
