# Intelligence Gathering Areas

**Five primary categories for comprehensive OSINT research**

---

## 1. Target Profiling

**Purpose:** Understand organizational structure, operations, and key decision-makers

### Research Areas
- **Organization Structure**
  - Corporate hierarchy and reporting lines
  - Business units and departments
  - Subsidiaries and parent companies
  - Geographic locations and offices

- **Key Personnel**
  - Executive leadership (C-suite, Board of Directors)
  - Security leadership (CISO, security engineers)
  - IT leadership (CIO, IT managers, DevOps)
  - Department heads and managers

- **Technology Stack**
  - Cloud providers (AWS, Azure, GCP)
  - Operating systems and platforms
  - Development frameworks and languages
  - Third-party services and SaaS tools

- **Business Relationships**
  - Strategic partners and alliances
  - Vendors and suppliers
  - Customers and clients (if public)
  - Competitors and market position

### Data Sources
- LinkedIn (org charts, employee counts, job titles)
- Company website (leadership bios, office locations)
- Public filings (SEC, Companies House, business registrations)
- Press releases and news articles

---

## 2. Digital Footprint

**Purpose:** Map technical infrastructure and online presence

### Research Areas
- **Domain and Subdomain Enumeration**
  - Primary domains and variations
  - Subdomains (dev, staging, admin, api)
  - Parked domains and typosquatting
  - SSL certificates (Certificate Transparency logs)

- **Email Addresses and Naming Conventions**
  - Email format patterns (first.last@, firstlast@, f.last@)
  - Exposed email addresses (data breaches, public repos)
  - Contact emails on website
  - Employee emails from LinkedIn/social media

- **Social Media Presence**
  - Corporate accounts (LinkedIn, Twitter, Facebook, Instagram)
  - Employee accounts and affiliations
  - Social media engagement and reach
  - Brand mentions and sentiment

- **Public Code Repositories**
  - GitHub/GitLab organizations
  - Public repositories and projects
  - Code commits and contributors
  - Exposed secrets (API keys, credentials, config files)

### Data Sources
- DNS reconnaissance (nslookup, dig, SecurityTrails)
- Certificate Transparency (crt.sh, Censys)
- GitHub/GitLab search
- Social media platforms
- Email breach databases (Have I Been Pwned)

---

## 3. Security Posture

**Purpose:** Assess public security indicators and historical incidents

### Research Areas
- **Exposed Credentials**
  - Data breach databases (Have I Been Pwned, Dehashed)
  - Public paste sites (Pastebin, GitHub gists)
  - Dark web marketplaces (with authorization)
  - Default credentials in public systems

- **Public Vulnerabilities**
  - CVE disclosures affecting used technologies
  - Bug bounty program disclosures (HackerOne, Bugcrowd)
  - Security advisories from vendors
  - Shodan/Censys exposed services

- **Security Incidents and Breaches**
  - Historical breach disclosures
  - Ransom demands and leak sites
  - SEC filings mentioning cybersecurity incidents
  - News coverage of security events

- **Compliance Certifications**
  - SOC 2, ISO 27001, PCI DSS
  - Industry-specific certifications (HIPAA, FedRAMP)
  - Compliance documentation and reports
  - Audit findings (if publicly disclosed)

### Data Sources
- Breach databases (HIBP, Dehashed, BreachDirectory)
- Shodan, Censys (exposed services)
- HackerOne/Bugcrowd (bug bounty disclosures)
- SEC filings (8-K cybersecurity incident reports)
- Compliance directories (SOC 2 registries)

---

## 4. Threat Intelligence

**Purpose:** Identify threats targeting the organization or sector

### Research Areas
- **Known Threat Actors**
  - APT groups targeting the industry
  - Cybercrime organizations
  - Hacktivist groups
  - Nation-state actors with sector interest

- **Recent Attack Campaigns**
  - Industry-specific campaigns
  - Technology-specific exploits
  - Phishing campaigns targeting employees
  - Ransomware incidents in peer organizations

- **Industry-Specific Vulnerabilities**
  - Common vulnerabilities in sector (finance, healthcare, etc.)
  - Technology stack vulnerabilities
  - Supply chain risks
  - Regulatory compliance gaps

- **Emerging Threats**
  - Zero-day vulnerabilities affecting used technologies
  - New attack techniques and TTPs
  - Threat actor evolution
  - Dark web chatter about targets (with authorization)

### Data Sources
- Threat intelligence feeds (CISA, FBI, vendor reports)
- Security blogs and research (CrowdStrike, Mandiant)
- Dark web monitoring (with authorization)
- Industry-specific ISACs
- MITRE ATT&CK threat actor profiles

---

## 5. Competitive Intelligence

**Purpose:** Understand market position, strategy, and public perception

### Research Areas
- **Market Positioning**
  - Industry ranking and market share
  - Competitive advantages and differentiators
  - Target customer segments
  - Geographic market presence

- **Product Offerings and Roadmap**
  - Current product portfolio
  - Upcoming features (from job postings, press releases)
  - Technology stack and architecture
  - Pricing models and plans

- **Customer Base and Partnerships**
  - Public customer case studies
  - Strategic partnerships
  - Vendor relationships
  - Competitor relationships

- **Public Perception and Sentiment**
  - Brand sentiment on social media
  - Customer reviews (Glassdoor, G2, TrustPilot)
  - News coverage tone
  - Employee satisfaction (Glassdoor, Blind)

### Data Sources
- Market research reports (Gartner, Forrester)
- Company website and press releases
- Social media sentiment analysis
- Review platforms (G2, Capterra, TrustPilot)
- Employee review sites (Glassdoor, Blind)

---

## Intelligence Categories by Use Case

**Pentest Scoping:**
- Primary: Digital Footprint, Security Posture
- Secondary: Target Profiling, Threat Intelligence

**Threat Actor Profiling:**
- Primary: Threat Intelligence
- Secondary: Target Profiling (for attribution context)

**Competitive Analysis:**
- Primary: Competitive Intelligence, Target Profiling
- Secondary: Security Posture (for risk comparison)

**Pre-Employment Research:**
- Primary: Target Profiling, Competitive Intelligence
- Secondary: Security Posture (stability indicator)

---

**Related:**
- `methodologies/dual-source-research.md` - Research methodology for each area
- `workflows/fast-mode-research.md` - Quick intelligence gathering
- `workflows/deep-mode-research.md` - Comprehensive investigation
- `reference/output-structure.md` - How to organize intelligence findings
