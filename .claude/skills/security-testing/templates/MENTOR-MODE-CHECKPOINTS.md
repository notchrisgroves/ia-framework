
## Overview

Mentor mode transforms security testing into a learning experience by offering checkpoints after each phase where the mentee can:
- **Try it themselves** (guided practice with review)
- **Watch and learn** (demonstration with explanation)
- **Continue standard** (return to director mode)

This mirrors real professional engagements where a senior pentester asks "want to take this one?"

---

## Checkpoint Pattern Template

```markdown
✅ [PHASE NAME] complete. [Brief results summary]

🎓 MENTOR MODE:
What would you like to do next?
  A) I'll try [NEXT_PHASE] myself (you review my approach)
  B) Show me how to do [NEXT_PHASE] (I'll watch and learn)
  C) Continue testing (standard mode, no teaching)
```

**Implementation:**
- Security agent presents checkpoint
- User selects A/B/C
- Agent routes to appropriate mode
- Advisor agent may assist with teaching moments

---

## Phase-Specific Checkpoints

### Checkpoint 1: After Reconnaissance

**Trigger:** Subdomain enumeration, initial port scans complete

```markdown
✅ Reconnaissance complete.

FINDINGS:
- [X] subdomains discovered
- [X] unique IP addresses identified
- [X] services detected on standard ports
- Notable: [Any interesting findings]

🎓 NEXT PHASE: Service Enumeration & Technology Fingerprinting

This involves:
- Running httpx for web server identification
- Technology detection (frameworks, versions)
- SSL/TLS analysis
- Response header analysis

What would you like to do?
  A) I'll run service enumeration myself (you review my commands)
  B) Show me how to do effective service enumeration
  C) Continue standard testing (no teaching mode)
```

**Option A - Self-Guided:**
```markdown
Great! Here's what you need to accomplish:

OBJECTIVES:
1. Identify web servers and versions
2. Detect technologies/frameworks in use
3. Check SSL/TLS configurations
4. Save structured output for analysis

TOOLS AVAILABLE:
- httpx (web server fingerprinting)
- nuclei (template-based detection)
- nmap NSE scripts (specific service probes)

Go ahead - tell me what command you'll run and I'll review your approach.
```

**Option B - Demonstration:**
```markdown
I'll demonstrate effective service enumeration. Watch what I do:

STEP 1: Technology Fingerprinting with httpx
  Command: httpx -l subdomains.txt -status-code -tech-detect -title -json -o httpx-results.json -silent -threads 50

  WHY THESE FLAGS:
  - -tech-detect: Identifies frameworks (React, Laravel, etc.)
  - -json: Structured output for parsing
  - -silent: Reduces noise in output
  - -threads 50: Parallel processing for speed

  EXPECTED RESULTS:
  - HTTP status codes (200, 301, 403 tell different stories)
  - Server headers (Apache, Nginx, custom)
  - Technologies in use (helps prioritize testing)

[Executes command]

RESULTS ANALYSIS:
[Explains what the output reveals and why it matters]

Ready for the next step?
```

---

### Checkpoint 2: After Service Enumeration

**Trigger:** Technology stack identified, web servers fingerprinted

```markdown
✅ Service Enumeration complete.

FINDINGS:
- Web Servers: [List with versions]
- Technologies: [Frameworks, libraries detected]
- Interesting Services: [Non-standard ports, unusual configs]
- Potential Issues: [Outdated versions, known CVEs]

🎓 NEXT PHASE: Vulnerability Scanning

This involves:
- Running automated scanners (Nuclei, Wapiti)
- CVE matching against detected versions
- Directory/endpoint discovery
- Initial attack surface mapping

What would you like to do?
  A) I'll set up vulnerability scanning (you review my scanner selection)
  B) Show me how to run effective vulnerability scans
  C) Continue standard testing
```

**Option A - Self-Guided:**
```markdown
Good choice! Here's the challenge:

SCENARIO: You have 3 web applications running different stacks:
1. api.target.com - Nginx 1.21 / Node.js backend
2. staging.target.com - Apache 2.4.29 / PHP 7.4
3. admin.target.com - Custom server / Unknown backend

TASK: Choose appropriate scanners and explain your selection
- Which tool for which target?
- What flags/templates will you use?
- Why did you choose each tool?

Tell me your scanning plan and I'll review it before we execute.
```

**Option B - Demonstration:**
```markdown
I'll show you strategic scanner selection. This is critical - wrong tool wastes time.

DECISION MATRIX:

Target 1 (api.target.com - Node.js API):
  ✅ Nuclei with API-specific templates
  ✅ httpx for endpoint discovery
  ❌ NOT nikto (designed for traditional web apps)

  WHY: APIs need focused testing (auth, rate limits, business logic)

Target 2 (staging.target.com - PHP/Apache):
  ✅ Nuclei for CVE detection
  ✅ Wapiti for automated crawling + injection testing
  ✅ WPScan IF WordPress detected

  WHY: Traditional web app benefits from comprehensive scanners

Target 3 (admin.target.com - Custom):
  ✅ Manual proxy testing (Reaper) FIRST
  ✅ Light Nuclei scan to avoid WAF triggers
  ❌ NOT aggressive automated scanners

  WHY: Custom apps = custom vulnerabilities, need manual analysis

EXECUTION ORDER MATTERS:
1. Start passive (Nuclei templates)
2. Escalate to active (Wapiti crawling)
3. Manual validation last

Let me run these in order and explain what we find...
```

---

### Checkpoint 3: After Vulnerability Scanning

**Trigger:** Automated scans complete, potential vulnerabilities identified

```markdown
✅ Vulnerability Scanning complete.

FINDINGS:
- [X] potential vulnerabilities identified
- Severity breakdown: [Critical/High/Medium/Low counts]
- Top findings: [Brief list of notable issues]
- False positive likelihood: [Estimate based on scanner]

🎓 NEXT PHASE: Manual Validation & Exploitation

This involves:
- Validating scanner findings (separating real from false positives)
- Manual testing of business logic
- Exploitation of confirmed vulnerabilities
- Impact demonstration

What would you like to do?
  A) I'll validate findings myself (you review my methodology)
  B) Show me how to validate and exploit vulnerabilities
  C) Continue standard testing
```

**Option A - Self-Guided:**
```markdown
Here's your validation challenge:

SCANNER REPORTED: SQL Injection in /api/users?id=1
  Tool: Nuclei (high confidence)
  Evidence: Error-based detection
  Severity: High

YOUR TASKS:
1. Manually verify the vulnerability exists
2. Determine actual exploitability
3. Assess real-world impact
4. Document proof-of-concept

Walk me through your validation plan:
- What will you test first?
- How will you confirm it's not a false positive?
- What impact will you demonstrate?

Show me your commands and I'll review before execution.
```

**Option B - Demonstration:**
```markdown
I'll demonstrate professional vulnerability validation. This separates good pentesters from script kiddies.

FINDING: SQL Injection in /api/users?id=1

VALIDATION STEPS:

Step 1: MANUAL CONFIRMATION
  Before running SQLMap, let's verify manually:

  Test 1: Error-based detection
    curl "https://api.target.com/users?id=1'" -H "Authorization: Bearer TOKEN"

  EXPECTED: Database error message
  ACTUAL: [Shows result]
  CONCLUSION: Confirms vulnerability exists

Step 2: IMPACT ASSESSMENT
  What can we actually do with this?

  Test 2: Database enumeration
    sqlmap -u "..." --dbs --batch

  EXPECTED: List of databases
  ACTUAL: [Shows result]
  IMPACT: Access to [X] databases including 'users_production'

Step 3: DATA EXTRACTION (Controlled)
  We can extract data, but should we?

  PENTEST MODE: Extract sample records (proof of impact)
  VULN-SCAN MODE: STOP HERE, document finding

  What's appropriate for this engagement? [Checks SCOPE.md mode]

Step 4: DOCUMENTATION
  Writing this up while fresh:
  - Vulnerability: SQL Injection
  - Location: /api/users?id parameter
  - Impact: Full database access (PII exposure)
  - CVSS: 8.6 (High)
  - POC: [Exact commands with sanitized output]

Notice how we:
1. Confirmed manually (not just trusting scanner)
2. Assessed real impact (not theoretical)
3. Stayed within scope (checked authorization)
4. Documented immediately (don't lose details)

This is professional validation.
```

---

## "I'm Stuck" Help Patterns

**Trigger:** User invokes help during self-guided phase

**Pattern:** Advisor agent provides diagnostic troubleshooting

---

### Help Pattern 1: Tool Not Working

**User Request:**
```
"I'm trying to run nuclei but it's not finding any vulnerabilities, even though we know there are issues"
```

**Advisor Response:**
```markdown
🎓 LET'S TROUBLESHOOT:

SYMPTOM: Nuclei running but finding nothing

COMMON CAUSES (in order of likelihood):
1. Wrong templates selected
2. Target requires authentication
3. Rate limiting blocking requests
4. Network/WAF interference
5. Tool misconfiguration

DIAGNOSTIC PROCESS:

Question 1: What command did you run?
[User provides: nuclei -u https://target.com]

DIAGNOSIS: Missing templates! Nuclei needs explicit template selection.

FIX:
  nuclei -u https://target.com -tags cve,owasp,sqli -severity critical,high

WHY THIS WORKS:
  -tags: Specifies which vulnerability classes to test
  -severity: Filters to high-impact findings

Alternative approach:
  nuclei -u https://target.com -t /path/to/custom/templates

TRY THIS:
Would you like to:
  A) Try the fixed command yourself
  B) I'll run it and explain the results
```

---

### Help Pattern 2: Unexpected Results

**User Request:**
```
"I ran nmap -sV but I'm not getting version info on port 8080, just shows 'unknown'"
```

**Advisor Response:**
```markdown
🎓 LET'S DEBUG:

SYMPTOM: Nmap version detection failing on specific port

WHY THIS HAPPENS:
1. Custom service (not in nmap's signature database)
2. Service fingerprint obfuscation
3. Firewall filtering version probes
4. Application-level service (HTTP on non-standard port)

INVESTIGATION STEPS:

Step 1: Check if it's HTTP
  curl -v http://target:8080

  IF returns HTML/JSON → It's HTTP, just non-standard port

Step 2: Try aggressive version detection
  nmap -p 8080 -sV --version-intensity 9 -Pn target

  WHY: Intensity 9 tries more probes

Step 3: Manual banner grab
  nc target 8080
  [Send HTTP request manually]

  OR

  echo -e "GET / HTTP/1.1\r\nHost: target\r\n\r\n" | nc target 8080

Step 4: Check with httpx (if HTTP)
  httpx -u http://target:8080 -status-code -tech-detect -server

EXPECTED OUTCOME:
You'll identify the service through one of these methods.

LEARNING POINT:
Nmap is powerful but not perfect. Manual investigation is often needed for:
- Custom applications
- Non-standard ports
- Obfuscated services

Want me to run these diagnostics, or try yourself?
```

---

### Help Pattern 3: Don't Know Next Step

**User Request:**
```
"I found what looks like an IDOR vulnerability but I'm not sure how to prove it or what impact it has"
```

**Advisor Response:**
```markdown
🎓 GREAT FIND! Let's validate and assess impact.

IDOR (Insecure Direct Object Reference) - Classic authorization flaw

VALIDATION PROCESS:

Step 1: CONFIRM THE VULNERABILITY
  What you have: Access to object you shouldn't
  What you need: Proof this breaks authorization

  Test Matrix:
  - User A can access User B's resource? → IDOR confirmed
  - Resource ID predictable (1,2,3 or UUID)? → Document pattern
  - Any authorization check? → Test bypass methods

Step 2: ASSESS SCOPE
  Critical questions:
  - What data is exposed? (PII, financial, system info)
  - How many objects affected? (1 user or entire database)
  - Can you modify or just read? (CRUD operations)

Step 3: DEMONSTRATE IMPACT
  Non-technical stakeholder test:
  "Because of this flaw, any user can [IMPACT]"

  Examples:
  ✅ "...access any other user's private messages"
  ✅ "...view financial transactions of all customers"
  ❌ "...enumerate user IDs" (technical, no clear impact)

Step 4: BUILD POC
  Proof of Concept should show:
  1. Login as User A (ID: 123)
  2. Access User B's resource (ID: 456)
  3. Receive User B's data
  4. Screenshot/HTTP logs as evidence

SEVERITY CALCULATION:
  - Data sensitivity: PII = High, Public = Low
  - Scope: All users = Critical, Single user = Medium
  - Authentication required: Yes = Medium, No = Critical

  Your scenario: [Guide calculation based on their finding]

DOCUMENTATION TEMPLATE:
I'll help you write this up. We need:
- Vulnerability title
- Affected endpoint
- Steps to reproduce (exact)
- Impact statement
- Evidence (sanitized screenshots)
- Remediation recommendation

Want me to walk through writing the finding, or try yourself with my template?
```

---

## Progression Tracking

**Purpose:** Track mentee progress to adapt checkpoint offers

**Storage:** `[engagement-dir]/MENTOR-PROGRESS.md`

```yaml
mentee_progress:
  comfortable_with:
    - subdomain_enumeration
    - port_scanning
    - httpx_fingerprinting
  learning:
    - vulnerability_validation
    - sql_injection_exploitation
  needs_help_with:
    - business_logic_testing
    - smart_contract_analysis

  checkpoint_history:
    - phase: reconnaissance
      choice: A  # Tried themselves
      outcome: success
    - phase: service_enumeration
      choice: B  # Watched demonstration
      outcome: learned_new_technique
    - phase: vuln_scanning
      choice: A  # Tried themselves
      outcome: got_stuck  # Invoked help pattern
    - phase: vuln_validation
      choice: C  # Returned to standard mode
      outcome: completed

  skill_graduation:
    - reconnaissance: graduated  # Always chooses A or C now
    - enumeration: comfortable    # Mix of A and C
    - exploitation: learning      # Still choosing B frequently
```

**Adaptive Behavior:**
- If mentee consistently chooses A or C for a phase → Stop offering checkpoint
- If mentee frequently invokes help → Offer more guidance in checkpoint
- If mentee graduates entire workflow → Suggest director mode permanently

---

## Implementation Notes

**For Security Agent:**
1. After completing phase, check if `engagement_mode == "mentor"`
2. If yes, present checkpoint using AskUserQuestion tool
3. Route based on response:
   - A → Enter coaching mode (review user's approach)
   - B → Enter demonstration mode (explain while executing)
   - C → Return to standard workflow

**For Advisor Agent:**
1. Listen for "stuck" signals (user asks for help mid-phase)
2. Analyze the problem category (tool failure, unexpected results, methodology question)
3. Provide diagnostic troubleshooting with teaching context
4. Offer to demonstrate or let user retry with guidance

**Handoff Pattern:**
```
Security Agent: [Presents checkpoint]
User: [Chooses A]
Security Agent: [Provides objectives and coaching framework]
User: [Attempts task]
  → If successful: Security agent reviews and continues
  → If stuck: Advisor agent provides help pattern
  → If needs demo: Security agent demonstrates (option B retrospectively)
```

---

## Cost Optimization

**Mentor mode will use more tokens than director mode**

**Mitigation strategies:**
1. Use Haiku for checkpoint presentations (simple A/B/C choice)
2. Use Sonnet for teaching moments (explanation requires depth)
3. Cache common help patterns (reduce re-generation)
4. Offer "skip checkpoints" option if budget-conscious

**Estimated cost increase:** 20-30% over director mode (worthwhile for learning value)

---

## Version History

- **1.0** (2025-11-14): Initial checkpoint patterns and help templates
