# Credential Handling Enforcement

**Zero Tolerance Policy for Hardcoded Credentials**

---

## Core Rules

1. **ALL scripts MUST load credentials from `.env` ONLY**
2. **NO hardcoded API keys, passwords, or secrets in any file**
3. **Scripts MUST fail if required credentials are missing** (no fallbacks)
4. **Pre-commit hook blocks commits containing detected secrets**

---

## Implementation Standards

### Python Scripts

```python
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Get required credential
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in .env - see .env.template")

# Use credential
client = SomeClient(api_key=api_key)
```

### Bash Scripts

```bash
#!/bin/bash

# Load .env if exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Verify required credential
if [ -z "$API_KEY" ]; then
    echo "ERROR: API_KEY not set. Copy .env.template to .env and configure."
    exit 1
fi

# Use credential
curl -H "Authorization: Bearer $API_KEY" ...
```

### PowerShell Scripts

```powershell
# Load .env
$envFile = ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Verify required credential
$apiKey = [Environment]::GetEnvironmentVariable("API_KEY")
if (-not $apiKey) {
    throw "API_KEY not found in .env - see .env.template"
}
```

---

## .env Setup

1. **Copy template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit .env** - Replace `REPLACE_WITH_YOUR_*` placeholders with actual values

3. **Verify .env is gitignored** - Check `.gitignore` contains `.env`

---

## Credential Categories

### Required (Framework Core)
- `ANTHROPIC_API_KEY` - Claude API access

### Optional (Enhanced Features)
- `OPENAI_API_KEY` - GPT models
- `GROK_API_KEY` - Verification agent
- `PERPLEXITY_API_KEY` - Research
- `OPENROUTER_API_KEY` - Multi-model routing

### Service-Specific
- `GHOST_*` - Blog publishing
- `GITHUB_TOKEN` - Automation
- `VPS_*` - Security testing infrastructure

See `.env.template` for complete list with documentation.

---

## Pre-Commit Enforcement

The framework includes a pre-commit hook that scans for:
- Hardcoded API keys (pattern matching)
- AWS credentials
- Private keys
- Common secret patterns

**Location:** `hooks/pre-commit/`

**Bypass (emergency only):**
```bash
git commit --no-verify -m "message"
```

---

## Security Checklist

Before committing any script:

- [ ] No hardcoded credentials
- [ ] Uses `os.getenv()` or equivalent
- [ ] Fails with clear error if credential missing
- [ ] No fallback default values for credentials
- [ ] Tested with `.env` configured

---

## Violations

If pre-commit blocks your commit:

1. Identify the flagged line
2. Replace hardcoded value with environment variable lookup
3. Add the variable name to `.env.template` with documentation
4. Re-run commit

---

**Version:** 1.0
**Last Updated:** 2025-12-17
