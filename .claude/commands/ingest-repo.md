---
name: ingest-repo
description: GitHub repository ingestion using gitingest to convert repositories into LLM-digestible text format
---

# /ingest-repo - GitHub Repository Ingestion

Convert GitHub repositories (NIST, CIS, OWASP, MITRE) into LLM-digestible text format for framework reference materials.

**Agent:** advisor
**Skill:** gitingest-repo
**Output:** `resources/library/repositories/{repo-name}/`

---

## Quick Start

```
/ingest-repo https://github.com/OWASP/ASVS
```

**Or by topic:**
```
/ingest-repo OWASP Web Security Testing Guide
/ingest-repo NIST OSCAL
/ingest-repo MITRE ATT&CK STIX data
```

---

## When to Use

**Use /ingest-repo when:**
- Adding security frameworks to reference library
- Ingesting NIST, CIS, OWASP projects
- Building knowledge base from public repositories
- Converting GitHub content to LLM-friendly format

**Don't use if:**
- Repository >100MB (may fail)
- Private repositories (need auth)
- Binary content (PDFs, images)

---

## Prerequisites

**Install gitingest:**
```bash
uv tool install gitingest
```

---

## Supported Repositories

### Security Frameworks

| Source | Examples |
|--------|----------|
| **NIST** | OSCAL, SP 800-53, SP 800-171 |
| **CIS** | CIS Controls OSCAL, Benchmarks |
| **OWASP** | ASVS, Top 10, WSTG, Cheat Sheets |
| **MITRE** | ATT&CK STIX, CAPEC, CWE |

### Skill Routing

| Content Type | Routes To |
|--------------|-----------|
| NIST frameworks | security-advisory skill |
| CIS Controls | secure-config skill |
| OWASP projects | code-review, security-testing |
| MITRE ATT&CK | threat-intel skill |

---

## Workflow

### Phase 1: Verify Repository
- Valid GitHub URL (HTTPS format)
- Repository size <100MB
- Primary content type identified

### Phase 2: Ingest
```bash
gitingest https://github.com/org/repo -o output.txt
```

### Phase 3: Route to Skill
- Determine appropriate skill directory
- Create metadata.json with provenance
- Update STATUS.md

### Phase 4: Checkpoint
- Repository name, URL, timestamp
- File paths, content stats
- Enable resumption

---

## Web Search Integration

**For repository discovery:**
- Find official repository URLs
- Verify repository is current/maintained
- Check for forks or mirrors
- Identify related repositories

**Search sources:**
- GitHub search
- Framework official websites
- Security community references

---

## Agent Routing

```typescript
Task({
  subagent_type: "advisor",
  model: "haiku",  // Simple ingestion task
  prompt: `
Mode: ingest-repo
Skill: gitingest-repo

Repository: {url or description}

Instructions:
1. Verify repository (valid URL, size <100MB)
2. Run gitingest
3. Route to appropriate skill directory
4. Create metadata.json
5. Update STATUS.md

Output: resources/library/repositories/{repo-name}/
`
})
```

---

## Output Structure

```
resources/library/repositories/{repo-name}/
├── {repo-name}.txt      # Full ingested content
└── metadata.json        # Source URL, timestamp, stats
```

**Metadata format:**
```json
{
  "source_url": "https://github.com/org/repo",
  "ingested_at": "2025-12-19T10:00:00Z",
  "file_count": 150,
  "total_chars": 500000,
  "routed_to": "security-testing"
}
```

---

## Examples

### OWASP ASVS
```
/ingest-repo https://github.com/OWASP/ASVS

→ Ingest: OWASP Application Security Verification Standard
→ Route: code-review, security-testing skills
→ Output: resources/library/repositories/owasp-asvs/
```

### NIST OSCAL
```
/ingest-repo NIST OSCAL content

→ Search: Find official OSCAL repositories
→ Ingest: Core OSCAL definitions
→ Route: security-advisory skill
→ Output: resources/library/repositories/nist-oscal/
```

---

## Related Commands

- `/threat-intel` - Uses MITRE ATT&CK data
- `/secure-config` - Uses CIS Controls
- `/code-review` - Uses OWASP content

---

**Version:** 1.0
**Last Updated:** 2025-12-19
**Framework:** Intelligence Adjacent (IA)
