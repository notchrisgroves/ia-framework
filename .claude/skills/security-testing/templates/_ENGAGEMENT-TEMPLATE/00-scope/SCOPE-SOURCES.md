
## ✅ ALLOWED Scope Sources (ONLY)

### HackerOne Programs
- ✅ **HackerOne API ONLY** - `https://api.hackerone.com/v1/hackers/programs/{handle}`
- ✅ Use authenticated API calls with your API token
- ✅ Extract scope from API response JSON
- ❌ **NEVER use HackerOne web searches**
- ❌ **NEVER use WebSearch for HackerOne programs**

### Immunefi Programs
- ✅ **Program page ONLY** - `https://immunefi.com/bug-bounty/{program-name}/`
- ✅ Direct URL to specific program
- ❌ **NEVER use Immunefi search**
- ❌ **NEVER use WebSearch for Immunefi programs**

### Bugcrowd Programs
- ✅ **Program page ONLY** - `https://bugcrowd.com/{program-handle}`
- ✅ Direct URL to specific program
- ❌ **NEVER use Bugcrowd search**

### YesWeHack Programs
- ✅ **Program page ONLY** - `https://yeswehack.com/programs/{program-id}`
- ✅ Direct URL to specific program

### Intigriti Programs
- ✅ **Program page ONLY** - `https://app.intigriti.com/programs/{program-id}`
- ✅ Direct URL to specific program

### HackenProof Programs
- ✅ **Program page ONLY** - `https://hackenproof.com/programs/{program-id}`
- ✅ Direct URL to specific program

### Private/Client Engagements
- ✅ **Signed SOW (Statement of Work)** - Document provided by client
- ✅ **Email authorization** - Written approval from authorized contact
- ✅ **Client-provided scope document** - Official PDF/document

---

## ❌ FORBIDDEN Scope Sources (NEVER USE)

### ❌ NEVER Use WebSearch for Scope
- ❌ `WebSearch("program bug bounty scope")`  - **DANGEROUS**
- ❌ `WebSearch("program vulnerability disclosure")` - **DANGEROUS**
- ❌ `WebSearch("program security")`  - **DANGEROUS**
- ❌ Random blog posts about program
- ❌ Third-party aggregator sites
- ❌ Outdated documentation
- ❌ Forum discussions
- ❌ Social media posts

**Why:** Web searches can return:
- Production scope instead of staging
- Outdated scope from old programs
- Different programs with similar names
- Unauthorized testing targets
- **RESULT: Scope violation = legal liability**

### ❌ NEVER Use WebFetch on Generic URLs
- ❌ `WebFetch("company.com")` - **WRONG**
- ❌ `WebFetch("company.com/security")` - **WRONG**
- ✅ `WebFetch("hackerone.com/program-handle")` - **CORRECT** (direct program URL)

---

## Correct Workflow

### Step 1: Identify Platform
Determine which platform hosts the program:
- HackerOne
- Immunefi
- Bugcrowd
- etc.

### Step 2: Use Platform-Specific Method

**HackerOne:**
```python
# Use API ONLY
powershell -File query_h1.ps1  # Gets program via API
# OR
curl -u "$H1_USER:$H1_TOKEN" "https://api.hackerone.com/v1/hackers/programs/{handle}"
```

**Immunefi:**
```python
# Use direct WebFetch to program page
WebFetch("https://immunefi.com/bug-bounty/morpho/")
```

**Other Platforms:**
```python
# Use direct WebFetch to specific program URL
WebFetch("https://bugcrowd.com/{program-handle}")
```

### Step 3: Download Official Documentation
- Use WebFetch on ONLY the official program URLs from scope
- Save documentation locally for offline reference
- Create `00-scope/docs/` folder for downloaded materials

### Step 4: NO Additional Research
- ❌ Do NOT search for "similar vulnerabilities"
- ❌ Do NOT search for "recent exploits"
- ❌ Do NOT search for "program writeups"
- ✅ ONLY use official scope documentation

---

## Why This Matters

**Scenario: Wrong Approach**
```
User: "Test Airtable bug bounty"
Claude: WebSearch("Airtable bug bounty scope 2025")
Result: Finds old blog post mentioning production airtable.com
Claude: Tests production airtable.com
OUTCOME: ❌ UNAUTHORIZED ACCESS - OUT OF SCOPE
```

**Scenario: Correct Approach**
```
User: "Test Airtable bug bounty"
Claude: Uses HackerOne API to fetch program
API Response: "Only test staging.airtable.com"
Claude: Tests ONLY staging.airtable.com
OUTCOME: ✅ AUTHORIZED - IN SCOPE
```

---

## Emergency Check

Before ANY testing activity, verify:
1. ✅ Scope came from official platform (API or direct URL)
2. ✅ No WebSearch was used for scope lookup
3. ✅ All URLs match official program documentation
4. ✅ Testing environment matches scope (staging vs production)
5. ✅ SCOPE.md is re-read THIS SESSION

**If you used WebSearch for scope → STOP → Re-verify from official source**

---

## Documentation for This Engagement

**Platform:** [HackerOne / Immunefi / Bugcrowd / etc.]
**Scope Source:** [API call / Direct program URL]
**Scope Retrieved:** [Date/Time]
**Verification Method:** [API JSON / WebFetch of official URL]

**Official Documentation Downloaded:**
- [ ] Program policy
- [ ] Scope document
- [ ] Testing guidelines
- [ ] Known issues/duplicates

---

**REMEMBER: Scope violation = Unauthorized access = Legal consequences**
**ALWAYS verify scope from OFFICIAL sources ONLY**
