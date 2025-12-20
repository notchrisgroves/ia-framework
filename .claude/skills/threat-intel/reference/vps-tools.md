# VPS Tool Integration

**Docker-based security tools for threat intelligence research**

---

## cvemap - CVE Mapping and Research Tool

**Container:** kali-pentest (Kali Linux tools environment)

**Purpose:** Automated CVE searching and enrichment

**Capabilities:**
- Search CVEs by product, vendor, severity
- Filter by CVSS score ranges
- Retrieve CVE metadata from multiple sources
- Export results in JSON format

---

## Python Integration

### Basic Usage

```python
from servers.kali_pentest.cvemap import cvemap

# Search CVEs by product
result = cvemap.search(
    query="apache struts",
    severity="critical,high",
    limit=20
)

# Returns: CVE IDs, CVSS scores, descriptions, references
```

### Advanced Filtering

```python
# Search with CVSS threshold
result = cvemap.search(
    query="windows server",
    severity="critical",
    cvss_score=">9.0",
    limit=50
)

# Search by vendor
result = cvemap.search(
    query="vendor:microsoft",
    severity="high,critical",
    year="2024",
    limit=100
)

# Search with CWE filter
result = cvemap.search(
    query="apache tomcat",
    cwe="CWE-502",  # Deserialization vulnerabilities
    limit=30
)
```

### Result Format

```json
{
  "cves": [
    {
      "id": "CVE-2024-12345",
      "cvss": 9.8,
      "severity": "CRITICAL",
      "description": "Remote Code Execution in Apache Struts",
      "published": "2024-11-01",
      "references": [
        "https://nvd.nist.gov/vuln/detail/CVE-2024-12345",
        "https://struts.apache.org/announce-2024"
      ],
      "cwe": "CWE-502",
      "affected_products": [
        "cpe:2.3:a:apache:struts:2.5.0:*:*:*:*:*:*:*"
      ]
    }
  ],
  "total": 15,
  "query": "apache struts"
}
```

---

## Use Cases

### 1. Vulnerability Research for Pentesting

```python
# Research CVEs for target technology stack
target_stack = ["apache struts", "tomcat", "spring boot"]

for product in target_stack:
    result = cvemap.search(
        query=product,
        severity="critical,high",
        limit=10
    )
    # Analyze for exploitation potential
```

### 2. Patch Priority Analysis

```python
# Get all critical CVEs for organization's stack
critical_cves = cvemap.search(
    query="vendor:microsoft OR vendor:apache OR vendor:oracle",
    severity="critical",
    limit=100
)

# Cross-reference with CISA KEV catalog
# Prioritize CISA KEV CVEs first
```

### 3. Threat Intelligence Enrichment

```python
# Enrich IOC with CVE context
def enrich_cve(cve_id):
    result = cvemap.search(query=cve_id, limit=1)
    return {
        "cvss": result["cves"][0]["cvss"],
        "description": result["cves"][0]["description"],
        "references": result["cves"][0]["references"]
    }
```

---

## Configuration

**VPS Access:** Requires Twingate connection to VPS network

**Container Path:** `servers/kali-pentest/`

**Dependencies:**
- Docker (VPS-side)
- Twingate client (local)
- Python `servers` package (local wrapper)

**See:** `skills/infrastructure-ops/SKILL.md` for VPS setup details

---

## Alternative Tools

**For local CVE research (no VPS required):**
- NIST NVD API: `https://nvd.nist.gov/developers/vulnerabilities`
- CISA KEV CSV: `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv`
- EPSS API: `https://api.first.org/data/v1/epss`
- WebFetch/WebSearch for vendor advisories

**For advanced automation:**
- `nuclei` (Kali pentest container) - Vulnerability scanning with CVE templates
- `searchsploit` (Kali pentest container) - Exploit-DB local search
- `metasploit` (Kali pentest container) - Exploitation framework

---

**Related:**
- `reference/standards.md` - NVD, CISA KEV, EPSS APIs
- `methodologies/cve-research.md` - CVE research process
- `skills/infrastructure-ops/SKILL.md` - VPS infrastructure setup
