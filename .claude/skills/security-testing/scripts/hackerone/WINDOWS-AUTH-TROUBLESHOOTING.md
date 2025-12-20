# HackerOne API Authentication Issue

**Date:** 2025-11-10
**Status:** ✅ FIXED - Working on Windows PowerShell
**Impact:** Can now programmatically fetch bug bounty programs

---

## Problem (SOLVED)

**Root Cause:** Bash commands don't work properly on Windows - need PowerShell-native script

**Original Error:**
```json
{"errors":[{"status":401}]}
```

**Original Command (bash - doesn't work on Windows):**
```bash
source .env && curl -s -u "$HACKERONE_USERNAME:$HACKERONE_API_TOKEN" \
  "https://api.hackerone.com/v1/hackers/programs"
```

---

## Solution

**Use PowerShell script instead of bash commands.**

**Working Command:**
```powershell
powershell -ExecutionPolicy Bypass -File "tools/hackerone/test-api.ps1"
```

**Script Location:** `tools/hackerone/test-api.ps1`

**Output:**
```
[+] Found credentials in .env file
[+] Username: notchrisgroves
[+] Token: CA1H60ugD7...
[+] Testing HackerOne API authentication...

[+] SUCCESS! API authentication working
[+] Found 25 programs

First 3 programs:
  - HackerOne (security)
  - Phabricator (phabricator)
  - Ruby on Rails (rails)
```

---

## Why This Happened

**Windows vs Linux Command Differences:**

1. **Bash `source` doesn't work on Windows** - PowerShell uses different syntax
2. **Environment variable syntax different** - `$VARIABLE` vs `$env:VARIABLE`
3. **Path separators** - `/` vs `\`
4. **Escaping rules** - Bash vs PowerShell have different quoting/escaping

**Wrong Diagnosis:**
- Initially thought it was credential issue (API identifier vs username)
- API credentials were correct all along
- Issue was platform-specific command execution

---

## Usage

**To fetch HackerOne programs:**
```powershell
powershell -ExecutionPolicy Bypass -File "tools/hackerone/test-api.ps1"
```

**Script automatically:**
1. Reads credentials from `.env`
2. Creates Basic Auth header
3. Calls HackerOne API
4. Parses JSON response
5. Displays first 3 programs

---

## Future Enhancements

**Create additional PowerShell scripts:**

1. `fetch-programs.ps1` - List all available programs with filtering
2. `get-program-scope.ps1` - Extract scope for specific program
3. `search-programs.ps1` - Search programs by keyword/technology

**Location:** `tools/hackerone/`

---

## Lessons Learned

**Windows Development Best Practices:**

1. **Create `.ps1` scripts** instead of inline PowerShell commands
2. **Test with `-ExecutionPolicy Bypass`** to avoid policy issues
3. **Use `curl.exe`** explicitly (not `curl` alias which might be Invoke-WebRequest)
4. **Parse `.env` files carefully** - handle both `"` and `'` quotes
5. **Show progress** - Use `Write-Host` for user feedback

---

## Status

✅ **FIXED** - 2025-11-10

**Working script:** `tools/hackerone/test-api.ps1`
**Test result:** Successfully fetched 25 bug bounty programs
**Authentication:** Basic Auth with username + API token

---

**Created:** 2025-11-10
**Fixed:** 2025-11-10
**Platform:** Windows PowerShell
