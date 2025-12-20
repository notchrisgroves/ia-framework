
## 1. SCOPE.md Validation

**SCOPE.md Last Modified:** [Check file timestamp]
**Program Last Updated:** [Check program policy page]

### In-Scope Assets (Confirm EACH)

**Smart Contracts:**
- [ ] Contract 1: [Name/Address] - ✅ In scope (SCOPE.md line X)
- [ ] Contract 2: [Name/Address] - ✅ In scope (SCOPE.md line X)
- [ ] Contract 3: [Name/Address] - ✅ In scope (SCOPE.md line X)
- [ ] Contract 4: [Name/Address] - ✅ In scope (SCOPE.md line X)

**Web/Application Assets:**
- [ ] URL 1: [Full URL] - ✅ In scope (SCOPE.md line X)
- [ ] URL 2: [Full URL] - ✅ In scope (SCOPE.md line X)
- [ ] API Endpoint: [Base URL] - ✅ In scope (SCOPE.md line X)
- [ ] WebSocket: [WSS URL] - ✅ In scope (SCOPE.md line X)

**Add/Remove as needed based on your engagement**

### Out-of-Scope Items (Confirm NOT Testing)

- [ ] Reviewed out-of-scope section (SCOPE.md lines X-Y)
- [ ] Confirmed NO testing of out-of-scope assets
- [ ] Verified prohibited activities list
- [ ] Checked known issues exclusions

**Specific Prohibitions for THIS Session:**
- [List any specific restrictions that apply to today's testing]
- Example: "NO mainnet testing - only local forks"
- Example: "NO DoS/load testing"
- Example: "NO social engineering/phishing"

---

## 2. Authorization Validation

### Program Status Check

**Platform:** [HackerOne/Immunefi/Bugcrowd/Direct Client]
**Program URL:** [Full URL to program page]

- [ ] **Program is ACTIVE** (verified on platform)
- [ ] Program is NOT paused
- [ ] Program is NOT closed
- [ ] No "paused until [date]" notice

**If paused/closed:** STOP immediately, do not proceed with testing

### Scope Change Detection

**Checked for:**
- [ ] New assets added (compare with SCOPE.md)
- [ ] Assets removed from scope (compare with SCOPE.md)
- [ ] New restrictions added
- [ ] Reward structure changes (may indicate scope change)
- [ ] Policy updates (check "Last Updated" date)

**Scope Changes Detected?**
- [ ] NO - Proceed with session
- [ ] YES - Update SCOPE.md BEFORE proceeding

**If YES, document changes:**
- Change 1: [Description]
- Change 2: [Description]
- Updated SCOPE.md: [Yes/No]

### Communication Review

**Recent Communications:**
- [ ] Checked platform messages (last 7 days)
- [ ] Reviewed email notifications
- [ ] Checked program announcements
- [ ] Verified no testing pause notifications

**Any relevant communications?**
- [ ] NO - Proceed
- [ ] YES - Document below

**If YES:**
- Date: [YYYY-MM-DD]
- From: [Client/Platform]
- Summary: [Brief description]
- Impact on testing: [Does this affect scope/authorization?]

---

## 3. Session-Specific Target Validation

### Planned Targets for THIS Session

**Session Objective:** [Brief description of what you're testing today]

**Specific Targets:**

1. **Target 1:** [Specific asset/endpoint/function]
   - [ ] Confirmed in-scope (SCOPE.md line X)
   - [ ] No restrictions apply
   - Testing approach: [Brief description]

2. **Target 2:** [Specific asset/endpoint/function]
   - [ ] Confirmed in-scope (SCOPE.md line X)
   - [ ] No restrictions apply
   - Testing approach: [Brief description]

3. **Target 3:** [Specific asset/endpoint/function]
   - [ ] Confirmed in-scope (SCOPE.md line X)
   - [ ] No restrictions apply
   - Testing approach: [Brief description]

**Add as many targets as needed for this session**

### Testing Methods Validation

**Planned Methods:**
- [ ] Method 1: [e.g., Static analysis] - Allowed per program policy
- [ ] Method 2: [e.g., Manual testing] - Allowed per program policy
- [ ] Method 3: [e.g., Automated scanning] - Allowed per program policy

**Prohibited Methods (Confirm NOT Using):**
- [ ] DoS/Load testing (if prohibited)
- [ ] Social engineering (if prohibited)
- [ ] Physical testing (if prohibited)
- [ ] Third-party testing (if prohibited)
- [ ] [Other prohibited methods specific to program]

---

## 4. Authorization Confirmation

### Safe Harbor Validation

**Safe Harbor Statement Present?**
- [ ] YES - SCOPE.md contains safe harbor language
- [ ] NO - Contact client/platform for clarification

**Authorization Language Reviewed:**
- [ ] Authorization section read (SCOPE.md lines X-Y)
- [ ] Understand scope of authorization
- [ ] Understand limitations of authorization
- [ ] Emergency contact information noted

### Testing Headers/Identification

**Required Headers (for HTTP/HTTPS testing):**

**Platform:** [HackerOne/Immunefi/Bugcrowd/Other]

```
[Copy required headers from SCOPE.md]
Example:
X-Bug-Bounty: immunefi
X-Researcher: notchrisgroves
From: chris@notchrisgroves.com
```

- [ ] Headers documented
- [ ] Will include in all requests
- [ ] Understand purpose (identification during testing)

---

## 5. Risk Assessment for THIS Session

### Potential Impact

**What could go wrong?**
- Risk 1: [e.g., False positive leads to unnecessary alert]
- Risk 2: [e.g., Test causes temporary service impact]
- Risk 3: [e.g., Accidentally test out-of-scope asset]

**Mitigation:**
- Mitigation 1: [How you'll prevent/detect Risk 1]
- Mitigation 2: [How you'll prevent/detect Risk 2]
- Mitigation 3: [How you'll prevent/detect Risk 3]

### Emergency Procedures

**If something goes wrong:**

1. **STOP testing immediately**
2. **Document exactly what happened**
3. **Contact:** [Emergency contact from SCOPE.md]
4. **Notify platform:** [Platform-specific process]
5. **Do NOT continue until cleared**

**Emergency Contact (from SCOPE.md):**
- Platform: [HackerOne/Immunefi/Direct]
- Method: [Platform messaging/Email/Other]
- Response Time: [Expected timeframe]

---

## 6. Final Validation

### Pre-Session Checklist

**I confirm:**

- [ ] I have read SCOPE.md in full TODAY
- [ ] All targets for THIS session are in scope
- [ ] Program is active and accepting submissions
- [ ] No scope changes detected (or SCOPE.md updated)
- [ ] No new restrictions apply to my testing
- [ ] I understand prohibited activities
- [ ] I have emergency contact information
- [ ] I will include required testing headers
- [ ] I will document all activities
- [ ] I will STOP if any ambiguity arises

**Signature (Digital):**

**Name:** notchrisgroves
**Date:** [YYYY-MM-DD HH:MM]
**Session:** [Session Number]

**Status:** ✅ AUTHORIZED TO PROCEED with Session [N]

---

## 7. Post-Session Update

**Completed:** [YYYY-MM-DD HH:MM]

**Scope Issues Encountered:**
- [ ] None
- [ ] YES - Document below

**If scope issues encountered:**
- Issue: [Description]
- Action taken: [What did you do?]
- Resolution: [How was it resolved?]

**Findings Submitted:**
- [ ] None this session
- [ ] [Number] findings submitted
- [ ] All submissions within scope

**Next Session Scope Validation:** Will be performed before Session [N+1]

---

**Template Version:** 1.0
**Last Updated:** 2025-11-10
**Purpose:** Ensure professional authorization validation before EVERY testing session
