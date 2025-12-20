
## Overview

**Demo mode for security testing** enables quick validation of tools, infrastructure, and techniques without the overhead of full OSINT, threat intelligence, and test planning.

**Typical use cases:**
- Tool connectivity testing (Reaper, MCP servers, VPS tools)
- Infrastructure validation (Docker containers, network access)
- Quick proof-of-concept demonstrations
- Troubleshooting and debugging
- Technique experimentation

**Time savings:** 90-95% reduction (5-30 minutes vs. 4-6 hours)

---

## Demo Mode Workflows

### 1. Reaper Proxy Connectivity Test

**Purpose:** Verify Reaper is running and accessible for web app traffic capture

**Estimated Time:** 3-5 minutes

**Prerequisites:**
- Docker installed
- Reaper docker-compose.yml available
- Port 8080 free on localhost

#### Workflow

```markdown
🎯 DEMO MODE: Reaper Proxy Connectivity Test

OBJECTIVE: Verify Reaper is functional and accessible
ESTIMATED TIME: 3-5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Container Status Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Verify Docker container is running
Command: docker ps --filter "name=reaper" --format "{{.Names}}: {{.Status}}"
Expected: reaper: Up {X} hours/minutes
Actual: [Execute]

IF NOT RUNNING:
  Start container:
    docker-compose -f C:\Users\Chris\.claude\servers\reaper\docker-compose.yml up -d

  Wait 10 seconds for startup:
    Start-Sleep -Seconds 10

  Re-check status:
    docker ps --filter "name=reaper" --format "{{.Names}}: {{.Status}}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Port Accessibility Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Test localhost port 8080 accessibility
Command: Invoke-WebRequest -Uri http://localhost:8080 -UseBasicParsing -TimeoutSec 5
Expected: StatusCode: 200 (or any response indicating port is listening)
Actual: [Execute]

IF FAILED:
  Troubleshooting steps:

  1. Check port binding:
     docker port reaper
     Expected: 8080/tcp -> 0.0.0.0:8080

  2. Check if port is in use by another process:
     Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue

  3. Check Docker logs for errors:
     docker logs reaper --tail 20

  4. Test network connectivity:
     Test-NetConnection -ComputerName localhost -Port 8080

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Database Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Verify SQLite database is accessible
Command: docker exec reaper ls -lh /app/reaper.db
Expected: -rw-r--r-- 1 root root {size} {date} /app/reaper.db
Actual: [Execute]

IF FAILED:
  Check database initialization:
    docker logs reaper | Select-String "database"

  Database should auto-create on first request

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Proxy Test (Optional - Quick Capture Test)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Send test request through proxy
Command:
  Invoke-WebRequest -Uri http://httpbin.org/get `
    -Proxy http://localhost:8080 `
    -UseBasicParsing

Expected: StatusCode: 200 (request proxied successfully)
Actual: [Execute]

Note: This captures one request in Reaper database for verification

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO MODE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Container Status: {Running/Stopped}
✅ Port 8080: {Accessible/Blocked}
✅ Database: {Present/Missing}
✅ Proxy Function: {Working/Failed}
✅ Overall Status: {READY FOR USE / NEEDS TROUBLESHOOTING}

NEXT STEPS:

[IF WORKING]
- Reaper is ready for pentest engagement
- Configure browser proxy: localhost:8080 (HTTP & HTTPS)
- Install CA certificate: C:\Users\Chris\.claude\scratchpad\reaper-ca-cert.pem
- Start browsing target application to capture traffic
- Analysis tools available:
  * analyze_bola_vulnerabilities(hostname)
  * analyze_parameter_pollution(hostname)
  * analyze_injection_points(hostname)
  * generate_report(hostname)

[IF BROKEN]
- Review troubleshooting steps above
- Check Docker logs: docker logs reaper
- Verify docker-compose.yml configuration
- Check for port conflicts (8080 in use?)
- Restart Docker if necessary

REFERENCES:
- Architecture: skills/infrastructure-ops/runbooks/REAPER-ARCHITECTURE.md
- Database Access: engagement/REAPER-DATABASE-ACCESS.md template
- IDOR Analysis: scratchpad/analyze-reaper-idor.py

ACTUAL TIME: {X} minutes
```

---

### 2. VPS Tool Wrapper Test (Nmap)

**Purpose:** Verify VPS connectivity and tool wrapper functionality

**Estimated Time:** 5-10 minutes

**Prerequisites:**
- VPS accessible (OVHcloud: ${OVHCLOUD_VPS_IP})
- SSH key configured
- Python wrapper available

#### Workflow

```markdown
🎯 DEMO MODE: Nmap VPS Wrapper Validation

OBJECTIVE: Verify nmap wrapper executes via VPS and returns valid output
ESTIMATED TIME: 5-10 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: VPS Connectivity Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Verify SSH connection to VPS
Command: ssh -p 2222 root@${OVHCLOUD_VPS_IP} "echo 'Connection successful'"
Expected: "Connection successful"
Actual: [Execute]

IF FAILED:
  Check SSH key: Test-Path ~/.ssh/id_rsa
  Check VPS status: ping ${OVHCLOUD_VPS_IP}
  Verify port 2222: Test-NetConnection -ComputerName ${OVHCLOUD_VPS_IP} -Port 2222

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Docker Container Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Check kali-pentest container is running
Command: ssh -p 2222 root@${OVHCLOUD_VPS_IP} "docker ps --filter 'name=kali-pentest' --format '{{.Names}}: {{.Status}}'"
Expected: kali-pentest: Up {X} hours/days
Actual: [Execute]

IF NOT RUNNING:
  Start container:
    ssh -p 2222 root@${OVHCLOUD_VPS_IP} "docker start kali-pentest"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Wrapper Import Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Import nmap wrapper module
Command (Python):
  from servers.kali_pentest.nmap import nmap
  print("Wrapper imported successfully")

Expected: "Wrapper imported successfully" (no import errors)
Actual: [Execute]

IF FAILED:
  Check servers directory exists
  Verify __init__.py files present
  Check Python path includes servers/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Execution Test (Safe Target)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Run nmap against safe test target
Command (Python):
  result = nmap(
      target="scanme.nmap.org",
      options="-p 80,443 -sV",
      engagement_dir="scratchpad/demo-nmap-test"
  )
  print(result['message'])
  print(f"Output file: {result['outputFile']}")

Expected:
  - Scan completes without errors
  - Output file created
  - Summary dictionary returned with open ports

Actual: [Execute and show summary]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO MODE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VPS Connection: {Success/Failed}
✅ Docker Container: {Running/Stopped}
✅ Wrapper Import: {Success/Failed}
✅ Tool Execution: {Success/Failed}
✅ Output Parsing: {Valid/Error}
✅ Overall Status: {FUNCTIONAL / NEEDS DEBUGGING}

NEXT STEPS:

[IF WORKING]
- Nmap wrapper is ready for pentest engagements
- Use in director mode with real targets
- All 17 kali-pentest tools follow same pattern:
  * nuclei, httpx, subfinder, katana, naabu
  * sqlmap, wapiti, wpscan, nikto, dirb
  * hydra, crackmapexec, searchsploit
  * responder, netcat, cvemap

[IF BROKEN]
- Check VPS access (Twingate or SSH)
- Verify Docker container running
- Review wrapper code for errors
- Check output file permissions

ACTUAL TIME: {X} minutes
```

---

### 3. Nuclei MCP Server Test

**Purpose:** Verify nuclei template scanning functionality

**Estimated Time:** 5-10 minutes

**Prerequisites:**
- Nuclei MCP tool available
- Safe test target accessible

#### Workflow

```markdown
🎯 DEMO MODE: Nuclei Scanner Validation

OBJECTIVE: Verify nuclei executes and detects vulnerabilities
ESTIMATED TIME: 5-10 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Wrapper Import
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Import nuclei wrapper
Command (Python):
  from servers.kali_pentest.nuclei import nuclei
  print("Nuclei wrapper loaded")

Expected: No import errors
Actual: [Execute]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Execute Against Safe Target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Run nuclei with basic templates
Command (Python):
  result = nuclei(
      target="http://testphp.vulnweb.com",
      templates="-tags tech-detect,cve -severity high,critical",
      engagement_dir="scratchpad/demo-nuclei-test"
  )
  print(result['summary'])

Expected:
  - Scan completes (testphp is intentionally vulnerable)
  - Detects some findings (known CVEs, tech stack)
  - Returns structured summary

Actual: [Execute and show findings]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Output Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Verify output file structure
Command (Python):
  import json
  with open(result['outputFile'], 'r') as f:
      findings = [json.loads(line) for line in f if line.strip()]
  print(f"Found {len(findings)} vulnerabilities")
  if findings:
      print(f"Sample: {findings[0]['info']['name']}")

Expected: Valid JSON output with vulnerability details
Actual: [Execute and show sample]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO MODE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Wrapper Import: {Success/Failed}
✅ Scan Execution: {Success/Failed}
✅ Findings Detected: {X findings}
✅ Output Format: {Valid/Invalid}
✅ Overall Status: {FUNCTIONAL / NEEDS DEBUGGING}

NEXT STEPS:

[IF WORKING]
- Nuclei is ready for vulnerability scanning
- Use with targeted templates (-tags)
- Filter by severity (-severity critical,high)
- Primary tool for automated vuln detection

[IF BROKEN]
- Check VPS Docker container
- Verify nuclei templates updated
- Review error messages
- Test network connectivity to target

ACTUAL TIME: {X} minutes
```

---

### 4. Quick CORS Vulnerability Demo

**Purpose:** Demonstrate CORS misconfiguration testing without full pentest

**Estimated Time:** 10-15 minutes

**Prerequisites:**
- Test target with CORS issue (use httpbin.org for demo)
- curl or PowerShell available

#### Workflow

```markdown
🎯 DEMO MODE: CORS Vulnerability Demonstration

OBJECTIVE: Show CORS testing technique on safe target
ESTIMATED TIME: 10-15 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Understanding CORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCEPT:
- CORS = Cross-Origin Resource Sharing
- Controls which websites can access an API
- Misconfiguration = any origin can access

VULNERABILITY:
Server allows arbitrary origins → Data theft via malicious website

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Test for CORS Misconfiguration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Send request with malicious origin
Command:
  $headers = @{
      "Origin" = "https://evil-attacker.com"
  }
  $response = Invoke-WebRequest -Uri https://httpbin.org/get -Headers $headers -UseBasicParsing
  $response.Headers

Expected VULNERABLE response:
  Access-Control-Allow-Origin: https://evil-attacker.com
  (or: Access-Control-Allow-Origin: *)

Expected SECURE response:
  (No Access-Control-Allow-Origin header)
  (Or specific allowed origins only)

Actual: [Execute and check headers]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Impact Demonstration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action: Create simple POC HTML
Command: Create file demo-cors-poc.html:

<!DOCTYPE html>
<html>
<head><title>CORS POC</title></head>
<body>
<h1>CORS Vulnerability Proof of Concept</h1>
<div id="result"></div>
<script>
fetch('https://httpbin.org/get', {
  method: 'GET',
  credentials: 'include'
})
.then(r => r.json())
.then(data => {
  document.getElementById('result').innerHTML =
    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
})
.catch(e => {
  document.getElementById('result').innerHTML =
    'CORS blocked (secure): ' + e;
});
</script>
</body>
</html>

Expected:
- Open in browser
- If vulnerable: Data displays (cross-origin request succeeded)
- If secure: Error in console (CORS policy blocked request)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Severity Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CVSS FACTORS:
- Attack Vector: Network (AV:N)
- Attack Complexity: Low (AC:L)
- Privileges Required: None (PR:N)
- User Interaction: Required (UI:R) - victim must visit malicious site
- Scope: Changed (S:C) - affects other users
- Confidentiality: High (C:H) - data theft
- Integrity: High (I:H) - can modify via API
- Availability: None (A:N)

CVSS Score: ~8.8 (HIGH)

Real-world impact: Any logged-in user who visits attacker's site → data stolen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO MODE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CORS Test: {Vulnerable/Secure}
✅ POC Created: {Yes/No}
✅ Impact: {Demonstrated/Explained}
✅ Technique: DEMONSTRATED

KEY LEARNINGS:
- How to test for CORS misconfig (Origin header)
- What vulnerable response looks like
- Real-world attack scenario (malicious website)
- Professional impact assessment

NEXT STEPS:

[FOR PRODUCTION TESTING]
- Use this technique in full pentest (director mode)
- Test with authentication tokens
- Check Access-Control-Allow-Credentials header
- Document with POC and HTTP logs
- Assign CVSS score and remediation

ACTUAL TIME: {X} minutes
```

---

## Demo Mode Entry Points

### Automatic Triggers

**Agent detects demo mode when user says:**
- "Test Reaper connectivity"
- "Is nmap wrapper working?"
- "Quick CORS demonstration"
- "Verify nuclei is functional"
- "Demo mode: {tool/technique}"

### Manual Mode Selection

**User explicitly chooses demo mode from 3-option dialog:**

```markdown
C) DEMO MODE (Testing/Quick Validation)
   - Minimal workflow for tool/skill testing
   - Skip OSINT and threat intelligence
   - No production deliverables
   - ~15-30 minutes for targeted testing
```

---

## Demo Mode Restrictions

### Safety Rules

**NEVER in demo mode:**
- ❌ Test production systems
- ❌ Test real client targets without scope
- ❌ Create production deliverables
- ❌ Perform extensive OSINT
- ❌ Conduct full attack chain

**ALWAYS in demo mode:**
- ✅ Use safe test targets only
- ✅ Label output as "DEMO - NOT PRODUCTION"
- ✅ Provide upgrade path to director mode
- ✅ Keep total time under 30 minutes
- ✅ Focus on validation, not exploitation

### Approved Safe Targets

**Network scanning:**
- `scanme.nmap.org` - Official Nmap test server

**Web application testing:**
- `http://testphp.vulnweb.com` - Intentionally vulnerable
- `https://httpbin.org` - HTTP testing service
- `https://jsonplaceholder.typicode.com` - Fake API

**Local testing:**
- `localhost` services only
- Docker containers (local)
- Development environments (explicitly marked)

---

## Transitioning to Production

### Demo → Director Mode

**When demo confirms tool is working:**

```markdown
User: "Reaper works! Let's test the real target now"

Agent:
  ✅ Demo mode complete - Reaper is functional

  Switching to DIRECTOR MODE for production engagement

  [Loads full pentest workflow]
  - Creating engagement folder structure
  - Parsing SCOPE.md
  - Running OSINT intelligence gathering
  - Generating test plan
  - Starting systematic testing with Reaper

  This will now follow the complete pentest methodology with
  professional deliverables.
```

### Demo Findings → Production Documentation

**If demo discovers real vulnerability:**

```markdown
⚠️ IMPORTANT: Demo mode found potential vulnerability

This requires proper documentation:
- Switch to director mode
- Create formal engagement structure
- Document finding with evidence
- Assign CVSS score
- Write remediation guidance

Demo mode output is NOT suitable for submission.

Would you like to:
A) Switch to director mode and document properly
B) Note finding and continue demo
C) Exit demo mode
```

---

## Version History

- **1.0** (2025-11-15): Initial security testing demo mode
  - Reaper connectivity test
  - VPS tool wrapper validation
  - Nuclei scanner test
  - CORS vulnerability demonstration

---

**Related Documentation:**
- `library/patterns/demo-mode.md` - Universal demo mode pattern
- `../SKILL.md` - Full security testing methodology
- `skills/infrastructure-ops/runbooks/REAPER-ARCHITECTURE.md` - Reaper deployment
- `servers/ARCHITECTURE.md` - VPS tool wrapper architecture

**Version:** 1.0
**Status:** Production Ready
