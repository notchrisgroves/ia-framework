# Industry Standards & Methodology Sources

**Authoritative frameworks for OSINT research and intelligence gathering**

---

## Primary Standards

### OSINT Framework

**URL:** https://osintframework.com/

**Coverage:** Comprehensive OSINT tool taxonomy

**Focus:**
- Social media research (LinkedIn, Twitter, Facebook, Instagram)
- Domain research (WHOIS, DNS, subdomain enumeration)
- Dark web monitoring
- Public records (business registrations, court records, property records)

**Application:** Primary methodology for intelligence gathering and tool selection

**Tool Categories:**
- Username search (Sherlock, WhatsMyName)
- Email investigation (Hunter.io, Have I Been Pwned)
- Domain/IP research (Shodan, Censys, SecurityTrails)
- Social media OSINT (Social-Searcher, TweetDeck)
- Document and file analysis (FOCA, ExifTool)

---

### Bellingcat's Open Source Investigation Toolkit

**URL:** https://www.bellingcat.com/resources/

**Coverage:** Advanced OSINT techniques and investigative case studies

**Focus:**
- Source verification and fact-checking
- Geolocation techniques (reverse image search, landmark identification)
- Image and video analysis (metadata extraction, deepfake detection)
- Social media investigations (graph analysis, timeline reconstruction)
- Collaborative investigations

**Application:** Professional investigation techniques for complex cases

**Key Techniques:**
- Reverse image search (Google, TinEye, Yandex)
- Geolocation (Google Earth, Sentinel Hub, sun angle analysis)
- Archive.org/Wayback Machine for historical data
- Social network mapping
- Timestamp and metadata verification

---

### NIST SP 800-115 - Security Testing (OSINT Section)

**URL:** https://csrc.nist.gov/publications/detail/sp/800-115/final

**Coverage:** Information gathering for security testing and penetration testing

**Focus:**
- Passive reconnaissance techniques
- Public information analysis (DNS, WHOIS, public records)
- Network intelligence gathering
- Metadata extraction from documents

**Application:** Security-focused OSINT methodology for pentesting

**Methodology:**
- Information gathering (DNS enumeration, Google dorking)
- Vulnerability identification through public sources
- Social engineering data collection
- Non-intrusive reconnaissance

---

### PTES - Intelligence Gathering Phase

**URL:** http://www.pentest-standard.org/index.php/Intelligence_Gathering

**Coverage:** Penetration testing reconnaissance standards

**Focus:**
- Footprinting and scanning
- DNS enumeration (zone transfers, subdomain brute force)
- Metadata extraction (EXIF, document properties)
- Social media profiling of employees

**Application:** Target-focused intelligence gathering for security assessments

**Process:**
1. Identify initial target data (domains, IP ranges, key personnel)
2. Footprinting (whois, DNS records, SPF/DMARC policies)
3. Document analysis (leaked documents, public filings)
4. Search engine discovery (Google dorking, job postings)
5. Social media reconnaissance (LinkedIn org charts, employee posts)

---

## Supporting Standards

### MITRE ATT&CK - Reconnaissance Tactics (TA0043)

**URL:** https://attack.mitre.org/tactics/TA0043/

**Application:** Adversarial perspective on intelligence gathering

**Techniques:**
- T1595: Active Scanning (port scanning, vulnerability scanning)
- T1592: Gather Victim Host Information (hardware, software, configurations)
- T1589: Gather Victim Identity Information (employee names, email addresses)
- T1598: Phishing for Information (spearphishing, service enumeration)
- T1593: Search Open Websites/Domains (social media, search engines)
- T1594: Search Victim-Owned Websites (company sites, blogs, forums)

**Use Case:** Understanding how adversaries perform reconnaissance for defensive planning

---

### OWASP Testing Guide - Information Gathering

**URL:** https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/

**Application:** Web application reconnaissance methodology

**Focus:**
- Search engine discovery and reconnaissance
- Fingerprinting web servers and applications
- Reviewing webpage content for information leakage
- Identifying application entry points
- Mapping application architecture

**Techniques:**
- Google dorking (site:, inurl:, filetype: operators)
- Robots.txt and sitemap.xml analysis
- HTTP header fingerprinting
- JavaScript file analysis
- Public API enumeration

---

## Standards Integration

**When performing OSINT research:**

1. **Tool Selection:** OSINT Framework (comprehensive tool taxonomy)
2. **Verification:** Bellingcat (fact-checking and source validation)
3. **Security Context:** NIST SP 800-115 + PTES (pentesting reconnaissance)
4. **Adversarial Perspective:** MITRE ATT&CK TA0043 (how attackers gather intel)
5. **Web App Research:** OWASP Testing Guide (application-specific OSINT)

**Methodology Hierarchy:**
- OSINT Framework: Tool discovery and selection
- Bellingcat: Investigation techniques and verification
- NIST/PTES: Security assessment context
- MITRE ATT&CK: Defensive intelligence (know how adversaries operate)
- OWASP: Web application-specific reconnaissance

---

**Related:**
- `methodologies/dual-source-research.md` - Claude + Grok research methodology
- `workflows/fast-mode-research.md` - Quick intelligence gathering
- `workflows/deep-mode-research.md` - Comprehensive investigation workflow
