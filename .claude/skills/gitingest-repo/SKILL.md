---
name: gitingest-repo
description: GitHub repository ingestion for reference materials using gitingest to convert repositories into LLM-digestible text format. Use for ingesting NIST frameworks, CIS Controls, OWASP projects, and MITRE ATT&CK content into framework knowledge base.
---

# GitHub Repository Ingestion Skill

**Auto-loaded when `advisor` agent invoked for repository ingestion**

Convert GitHub repositories (NIST, CIS, OWASP) into LLM-digestible text format using gitingest tool for framework reference materials.

**Core Philosophy:** Repository verification required (valid URL, size <100MB). Skill routing mandatory (NIST → security-advisory, CIS → secure-config). Metadata tracking ensures provenance preservation.

---

## 🚀 Quick Access

**Purpose:** Automated ingestion of GitHub repositories containing cybersecurity frameworks and reference materials

**Tool:** gitingest (https://github.com/cyclotruc/gitingest)

**Installation:**
```bash
uv tool install gitingest
```

---

## 🚨 Critical Rules

**Before starting any repository ingestion:**

1. **Load Context First** - Read CLAUDE.md → SKILL.md
2. **Verify Repository Before Ingestion** - Never ingest without checking: (1) Valid GitHub URL (HTTPS format), (2) Repository size < 100MB, (3) Primary content type identified (prevents failed ingestion, wasted resources)
3. **Checkpoint After Each Repository** - Update STATUS.md with repository name, URL, timestamp, file paths, content stats (enables resumption and tracking)
4. **Route to Correct Skill Directory** - Always map repositories to appropriate skills (NIST → security-advisory, CIS → secure-config, OWASP → varies, ensures content findability)
5. **Track Metadata** - Never skip metadata creation (metadata.json with source URL, timestamp, stats, ensures provenance preservation)

**Refresh Trigger:** If conversation exceeds 3 hours OR after 5+ repositories ingested, refresh rules.

---

## Model Preference

**Recommended:** Claude Haiku 4.5

**Rationale:** Simple repository ingestion process, efficient for batch processing, cost-effective for multiple ingestions

**Use Sonnet for:** Complex repository analysis, selective directory ingestion, troubleshooting ingestion failures

---

## When to Use

✅ **Use gitingest-repo for:**
- Ingesting NIST frameworks (OSCAL, SP 800-53, SP 800-171)
- Ingesting CIS Controls/Benchmarks (CISControls_OSCAL, platform hardening guides)
- Ingesting OWASP projects (ASVS, Top 10, WSTG, Code Review Guide)
- Ingesting MITRE ATT&CK (adversary tactics and techniques)
- Building knowledge bases from public repositories
- Updating existing reference materials from GitHub

❌ **Don't use if:**
- Repository is private (gitingest requires public repos)
- Repository > 100MB (exceeds tool limits)
- Content is not text-based (binaries, images only)
- Not using GitHub as source (use WebFetch for web content)

---

## Repository-to-Skill Mapping

**Quick reference:**

| Repository Type | Target Skill | Examples |
|----------------|--------------|----------|
| NIST frameworks | security-advisory | OSCAL, SP 800-53 |
| CIS Controls/Benchmarks | secure-config | CISControls_OSCAL |
| OWASP ASVS | architecture-review | ASVS |
| OWASP Top 10 | security-advisory | Top10 |
| OWASP Testing Guide | security-testing | WSTG |
| OWASP Code Review | code-review | Code Review Guide |
| MITRE ATT&CK | security-advisory | CTI |

**Note:** Mapping table above covers primary use cases

---

## Workflow: 4-Phase Repository Ingestion

**Total Duration:** 5-15 minutes per repository

### Phase 1: Repository Analysis (2-3 min)

**Goal:** Validate repository and determine target skill

**Actions:**
1. Validate GitHub URL format (must be HTTPS)
2. Check repository size (must be < 100 MB)
3. Identify primary content type (OSCAL, markdown, code)
4. Determine target skill directory using mapping table

**Deliverables:**
- Repository validated
- Target skill identified
- Output path planned

**Checkpoint:** Repository verified, target skill determined

---

### Phase 2: Ingestion (3-5 min)

**Goal:** Run gitingest on repository URL

**Actions:**
1. Run gitingest on repository URL
2. Capture output to text file
3. Verify output quality (spot-check content)
4. Check file size is reasonable (not empty, not excessive)

**Command Example:**
```bash
gitingest https://github.com/usnistgov/OSCAL \
  -o resources/security-advisory/github/nist-oscal/nist-oscal.txt
```

**Deliverables:**
- Ingested text file ([repo-name].txt)

**Checkpoint:** Repository ingested, output validated

---

### Phase 3: Metadata Creation (2-3 min)

**Goal:** Create metadata.json with provenance information

**Metadata Template:**
```json
{
  "repository": "https://github.com/usnistgov/OSCAL",
  "skill": "security-advisory",
  "framework_name": "NIST OSCAL",
  "ingestion_method": "gitingest",
  "ingested_at": "2025-12-12T10:30:00Z",
  "stats": {
    "output_size_bytes": 5242880,
    "repository_size_mb": 15.5,
    "file_count": 342
  },
  "gitingest_version": "0.1.8",
  "branch": "main"
}
```

**Deliverables:**
- metadata.json

**Checkpoint:** Metadata created (use template above)

---

### Phase 4: Storage (1-2 min)

**Goal:** Store ingested files and update tracking

**Actions:**
1. Create target directory: `resources/[skill]/github/[repo-name]/`
2. Move ingested files to target
3. Create README.md (optional - repository description)
4. Update STATUS.md with new entry

**Output Structure:**
```
resources/[skill-name]/github/[repo-name]/
├── [repo-name].txt          # gitingest output
├── metadata.json            # ingestion metadata
└── README.md                # optional description
```

**Deliverables:**
- Files organized in skill directory
- STATUS.md updated

**Checkpoint:** Ingestion complete, tracking updated

---

## Tool: gitingest

**Basic Usage:**
```bash
# Ingest repository to text file
gitingest https://github.com/usnistgov/OSCAL -o nist-oscal.txt

# Ingest with specific branch
gitingest https://github.com/org/repo -b main -o output.txt

# Check version
gitingest --version
```

**Output Format:**
- Single text file containing all repository contents
- Markdown formatting preserved
- Binary files excluded
- Directory structure documented

**Limitations:**
- Repository size limit: ~100MB recommended
- Processes text files only
- Requires internet connection
- Rate limited by GitHub

---

## Common Commands

**Ingest NIST OSCAL:**
```bash
gitingest https://github.com/usnistgov/OSCAL \
  -o resources/security-advisory/github/nist-oscal/nist-oscal.txt
```

**Ingest CIS Controls:**
```bash
gitingest https://github.com/CISecurity/CISControls_OSCAL \
  -o resources/secure-config/github/cis-controls-oscal/cis-controls.txt
```

**Ingest OWASP Top 10:**
```bash
gitingest https://github.com/OWASP/Top10 \
  -o resources/security-advisory/github/owasp-top10/owasp-top10.txt
```

---

## Best Practices

**Before Ingestion:**
- Check repository size first (avoid >100MB)
- Use official organization repositories (not forks)
- Verify repository is public

**During Ingestion:**
- Monitor gitingest output for errors
- Check output file size is reasonable
- Verify content quality with spot-checks

**After Ingestion:**
- Always create metadata.json
- Update STATUS.md immediately
- Archive old versions before re-ingesting

**Regular Maintenance:**
- Re-ingest periodically for framework updates (quarterly recommended)
- Clean old ingested files (keep latest + 1 previous version)
- Track ingestion dates for freshness

---

## Troubleshooting

**Problem:** gitingest fails with "Repository too large"
**Solution:**
1. Check repository size (must be < 100 MB)
2. Clone repository locally
3. Use gitingest on local path with `--max-file-size` flag
4. Or consider selective directory ingestion

**Problem:** Output file is empty or corrupt
**Solution:**
1. Check repository exists and is public
2. Verify gitingest version is current (`gitingest --version`)
3. Try re-running with verbose flag
4. Check internet connection

**Problem:** Ingestion takes too long (>5 minutes)
**Solution:**
1. Repository may be too large (check size)
2. Network issue (check connection)
3. Consider canceling and using smaller repository
4. Or run during off-peak hours

**Problem:** Binary files included in output
**Solution:**
1. gitingest should exclude binaries automatically
2. Check gitingest version (update: `uv tool upgrade gitingest`)
3. Report issue to gitingest maintainers

---

## Context Loading

**This SKILL.md is self-contained:**
- Repository-to-skill mapping table (see above)
- 4-phase workflow with checkpoints
- Metadata template (JSON format)
- Troubleshooting guide

---

## Long-Session Rule Refresh

**Triggers:** Session > 3 hours OR 5+ repositories ingested OR `/refresh-rules`

**Refresh statement:**
```
Refreshing critical rules for repository ingestion:
- Context loaded (CLAUDE.md + SKILL.md)
- Repository verified (valid URL, size < 100MB, content type identified)
- Checkpoints maintained (STATUS.md updated after each ingestion)
- Correct skill routing (NIST → security-advisory, CIS → secure-config, etc.)
- Metadata tracked (metadata.json created for every ingestion)
```

**Benefit:** 15-20% improvement in long-session ingestion accuracy + metadata compliance

---

## Primary Use Cases

**NIST Frameworks:**
- NIST OSCAL (Open Security Controls Assessment Language)
- NIST SP 800-53 (Security Controls)
- NIST SP 800-171 (Protecting CUI)

**CIS Frameworks:**
- CIS Controls (OSCAL format)
- CIS Benchmarks (platform-specific hardening guides)

**OWASP Projects:**
- OWASP ASVS (Application Security Verification Standard)
- OWASP Top 10 (Web application security risks)
- OWASP WSTG (Web Security Testing Guide)
- OWASP Code Review Guide

**MITRE Frameworks:**
- MITRE ATT&CK (Adversary tactics and techniques)

**Key Advantage:** GitHub materials are structured, versioned, and machine-readable

---

## References

- **gitingest Documentation:** https://github.com/cyclotruc/gitingest
- **NIST OSCAL:** https://github.com/usnistgov/OSCAL
- **CIS Controls OSCAL:** https://github.com/CISecurity/CISControls_OSCAL
- **OWASP Projects:** https://github.com/OWASP

---

**Version:** 2.0
**Last Updated:** 2025-12-12
**Model:** Claude Haiku 4.5 (primary), Sonnet 4.5 (complex analysis)
**Tool:** gitingest (https://github.com/cyclotruc/gitingest)
**Framework:** Intelligence Adjacent (IA) - Reference Material Ingestion
