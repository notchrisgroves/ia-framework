# Threat Intelligence Output Structure

**Standard directory organization and file naming for threat intelligence engagements**

---

## Directory Structure

```
output/engagements/threat-intel/{client}-{YYYY-MM}/
├── README.md                          # Intelligence objectives, scope, timeline
├── #  Multi-session tracking in `../../sessions/                   # Multi-session checkpoint tracking
├── 01-cve-research/
│   ├── CVE-2024-12345-analysis.md     # Individual CVE reports
│   ├── CVE-2024-67890-analysis.md
│   ├── kev-catalog-review.md          # CISA KEV catalog analysis
│   └── vulnerability-prioritization.md # Prioritization matrix
├── 02-threat-landscape/
│   ├── threat-actor-profiles.md       # APT groups, cybercrime orgs
│   ├── attack-campaigns.md            # Campaign analysis
│   └── industry-threats.md            # Sector-specific threats
├── 03-attck-mapping/
│   ├── technique-mappings.md          # Tactic/technique inventory
│   ├── navigator-layers/
│   │   ├── observed-techniques.json   # ATT&CK Navigator layer
│   │   └── detection-coverage.json    # Blue team coverage layer
│   └── detection-rules/
│       ├── sigma/                     # Sigma detection rules
│       └── yara/                      # YARA malware rules
├── 04-iocs/
│   ├── indicators.csv                 # IP, domain, hash IOCs
│   ├── stix-bundle.json               # STIX 2.1 format for TIP integration
│   └── yara-rules/                    # Malware detection rules
└── 05-reporting/
    ├── executive-summary.md           # C-suite summary (2-3 pages)
    ├── threat-intelligence-report.md  # Technical report (20-50 pages)
    ├── remediation-roadmap.md         # Prioritized fixes (5-10 pages)
    └── deliverables/                  # Final PDFs for client
```

---

## File Naming Conventions

### CVE Reports
**Format:** `CVE-{YEAR}-{ID}-analysis.md`
**Examples:**
- `CVE-2024-12345-analysis.md`
- `CVE-2024-67890-analysis.md`

### Threat Actor Profiles
**Format:** `threat-actor-{name}.md`
**Examples:**
- `threat-actor-apt28.md`
- `threat-actor-fin7.md`
- `threat-actor-lockbit.md`

### Attack Campaigns
**Format:** `campaign-{name}-{YYYY-MM}.md`
**Examples:**
- `campaign-solarwinds-2020-12.md`
- `campaign-mozi-botnet-2024-11.md`

### ATT&CK Navigator Layers
**Format:** `{type}-{description}.json`
**Examples:**
- `observed-techniques.json` (red team layer)
- `detection-coverage.json` (blue team layer)
- `apt28-ttps.json` (threat actor layer)

### IOC Files
**Format:** `indicators.{format}`
**Examples:**
- `indicators.csv` (spreadsheet import)
- `indicators.json` (JSON for automation)
- `stix-bundle.json` (STIX 2.1 for TIP platforms)

---

## Report Templates

### README.md (Engagement Overview)
```markdown
# Threat Intelligence - {Client Name}

**Engagement Period:** {YYYY-MM-DD} to {YYYY-MM-DD}
**Intelligence Type:** CVE Research | Threat Landscape | Strategic Intelligence
**Scope:** {Brief description}

## Intelligence Objectives
1. Objective 1
2. Objective 2

## Research Scope
- Target technologies
- Threat actors of interest
- Time range

## Deliverables
- [ ] CVE Research Reports
- [ ] Threat Landscape Analysis
- [ ] ATT&CK Mappings
- [ ] Executive Summary
```

### CVE Analysis Report Template
See `templates/cve-research-report.md`

---

## Integration Formats

### SIEM/TIP Integration

**STIX 2.1 Bundle Format:**
```json
{
  "type": "bundle",
  "id": "bundle--{uuid}",
  "objects": [
    {
      "type": "indicator",
      "id": "indicator--{uuid}",
      "created": "2024-12-01T00:00:00.000Z",
      "modified": "2024-12-01T00:00:00.000Z",
      "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
      "pattern_type": "stix",
      "valid_from": "2024-12-01T00:00:00.000Z"
    }
  ]
}
```

**CSV Format (IOCs):**
```csv
indicator_type,indicator_value,confidence,threat_actor,campaign,first_seen,last_seen
ip,192.0.2.1,high,APT28,Campaign-X,2024-11-01,2024-11-30
domain,malicious.example.com,medium,FIN7,Campaign-Y,2024-11-15,2024-11-30
hash_md5,d41d8cd98f00b204e9800998ecf8427e,high,LockBit,Ransomware,2024-11-20,2024-11-30
```

---

## Related

- `workflows/threat-intelligence.md` - Complete 5-phase workflow
- `templates/cve-research-report.md` - CVE report template
- `reference/standards.md` - Threat intelligence frameworks
