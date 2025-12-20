---
type: template
name: osint-report-example
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# OSINT Research Report Example

**Example of dual-source intelligence gathering for pentest scoping**

---

## Research Request

**Target:** Acme Corp
**Purpose:** Cybersecurity posture assessment for pentest scoping
**Research Mode:** DEEP MODE (comprehensive investigation)
**Duration:** 60 minutes
**Sources:** Claude WebSearch + Grok Integration

---

## Agent Response: Dual-Source Research

### 1. Claude WebSearch (Primary Intelligence)

**Company Website Analysis**
- **Source:** https://acmecorp.com (Accessed: 2024-12-01)
- **Findings:**
  - Industry: Enterprise SaaS (CRM platform)
  - Size: 500-1000 employees
  - Headquarters: San Francisco, CA
  - Key products: Cloud-based CRM, sales automation

**Technology Stack**
- **Source 1:** BuiltWith analysis (https://builtwith.com/acmecorp.com)
  - Cloud: AWS (CloudFront CDN, S3 storage)
  - Frontend: React.js, Next.js
  - Backend: Node.js, Express
  - Database: PostgreSQL (inferred from job postings)

- **Source 2:** Job postings (https://acmecorp.com/careers)
  - Backend: "Experience with Node.js, Express, PostgreSQL required"
  - DevOps: "AWS, Docker, Kubernetes, Terraform"
  - Frontend: "React, TypeScript, Redux"

**Security Certifications**
- **Source:** Press release (https://acmecorp.com/press/soc2-certification-2024)
  - SOC 2 Type II certified (2024-06-15)
  - ISO 27001 certified (2023-11-20)
  - PCI DSS compliant (payment processing)

**Public GitHub Repositories**
- **Source:** GitHub organization (https://github.com/acmecorp)
  - 12 public repositories
  - Open-source React component library
  - Technical documentation site
  - **Findings:** No exposed secrets in commit history (automated scan completed)

**Job Postings Intelligence**
- **Source:** LinkedIn Jobs (https://linkedin.com/jobs/search?company=acmecorp)
  - Hiring: Security Engineer (recent breach incident mentioned in req)
  - Tech stack confirmed: AWS, Kubernetes, PostgreSQL
  - Pain points: "Scale our security program as we grow"

**News Articles**
- **Source 1:** TechCrunch (https://techcrunch.com/2024/09/15/acmecorp-security-incident)
  - Security incident: Q3 2024 (September 15)
  - Type: Unauthorized access to customer database
  - Impact: 10,000 customer records potentially exposed
  - Response: Notified customers within 48 hours, hired forensics firm

- **Source 2:** Company blog (https://acmecorp.com/blog/incident-response-update)
  - Post-incident update (2024-09-20)
  - Root cause: Misconfigured S3 bucket
  - Remediation: Third-party security audit, S3 bucket hardening

**Total Claude Sources:** 15 URLs with citations

---

### 2. Grok Integration (Social/Real-Time Intelligence)

**X/Twitter Corporate Account (@AcmeCorp)**
- **Source:** https://x.com/AcmeCorp/status/1234567890
  - Post (2024-09-16): "We take security seriously... working with forensics team..."
  - Engagement: 450 retweets, 1.2K likes
  - Comments: Mix of supportive customers and security criticism

**Employee Social Media**
- **Source 1:** https://x.com/johndoe_dev/status/1234567891
  - Developer tweet (2024-10-05): "Excited to deploy our new Kubernetes security controls"
  - Indicates: Recent security improvements post-incident

- **Source 2:** https://x.com/janedoe_ciso/status/1234567892
  - CISO tweet (2024-10-15): "Hiring for security team, looking for AWS security experts"
  - Indicates: Security team expansion, AWS focus

**Customer Complaints**
- **Source:** https://x.com/angry_customer/status/1234567893
  - Customer tweet (2024-09-17): "Just got notified my data was exposed... not happy"
  - Engagement: 85 retweets, 200 likes
  - **Analysis:** Customer frustration over incident

**Industry Analyst Commentary**
- **Source:** https://x.com/security_analyst/status/1234567894
  - Security analyst (2024-09-18): "Acme Corp's S3 misconfiguration is common issue... need better cloud security"
  - **Analysis:** Industry perspective on vulnerability type

**Recent Security Discussions**
- **Source:** https://x.com/search?q=acmecorp%20security
  - Time range: Last 30 days
  - **Findings:**
    - 150+ mentions of "acmecorp security"
    - Sentiment: 60% negative (post-incident), 30% neutral, 10% positive
    - Key themes: S3 security, incident response speed, transparency

**Total Grok Sources:** 10 tweet URLs with engagement metrics

---

### 3. Cross-Validation (Multi-Source Confirmation)

**Technology Stack Confirmed:**
- **Claude:** Job postings, BuiltWith analysis
- **Grok:** Developer tweets, CTO mentions
- **Confidence:** **HIGH** (AWS, React, Node.js, PostgreSQL confirmed by both sources)

**SOC 2 Certification Verified:**
- **Claude:** Press release (2024-06-15)
- **Grok:** Employee LinkedIn update mentioning SOC 2
- **Confidence:** **HIGH** (official press release + employee confirmation)

**Recent Security Incident Confirmed:**
- **Claude:** News article (TechCrunch 2024-09-15), company blog
- **Grok:** Social media chatter, corporate account post, customer complaints
- **Confidence:** **HIGH** (news coverage + official response + social confirmation)

**Root Cause: S3 Misconfiguration:**
- **Claude:** Company blog post-mortem
- **Grok:** Security analyst commentary
- **Confidence:** **HIGH** (official disclosure + industry analysis)

---

### 4. Synthesis Report

**Comprehensive OSINT Profile: Acme Corp**

#### Company Overview
- **Industry:** Enterprise SaaS (CRM platform)
- **Size:** 500-1000 employees
- **Locations:** San Francisco (HQ), distributed remote team
- **Confidence:** HIGH (official website + LinkedIn)

#### Technology Stack
- **Cloud:** AWS (CloudFront, S3, EC2, RDS)
- **Backend:** Node.js, Express, PostgreSQL
- **Frontend:** React, TypeScript, Redux
- **DevOps:** Docker, Kubernetes, Terraform
- **Confidence:** HIGH (job postings + developer social media + BuiltWith)

#### Security Posture
**Positive Indicators:**
- SOC 2 Type II certified (2024-06-15)
- ISO 27001 certified (2023-11-20)
- PCI DSS compliant
- Rapid incident response (48-hour notification)
- Third-party security audit post-incident

**Negative Indicators:**
- Recent security incident (Q3 2024)
- S3 misconfiguration led to 10,000 customer record exposure
- Security team appears understaffed (aggressive hiring)
- Customer sentiment negative post-incident (60% negative)

**Confidence:** HIGH (official disclosures + news coverage + social validation)

#### Security Incident Timeline
- **2024-09-15:** Incident discovered and disclosed (TechCrunch)
- **2024-09-16:** Corporate response on X/Twitter
- **2024-09-17:** Customer notifications sent
- **2024-09-20:** Post-mortem blog published (root cause: S3 misconfiguration)
- **2024-10-05:** New Kubernetes security controls deployed (developer tweet)
- **2024-10-15:** Security team hiring surge (CISO tweet)

**Confidence:** HIGH (news + official + social timeline matches)

#### Intelligence Gaps (Requiring Further Research)
1. Exact AWS services used beyond CloudFront/S3
2. Third-party integrations and SaaS dependencies
3. Network architecture and segmentation
4. Current vulnerability management process
5. Penetration test history (if any)

---

## Citations

### Claude WebSearch Sources
1. https://acmecorp.com - Company website (Accessed: 2024-12-01)
2. https://builtwith.com/acmecorp.com - Technology stack analysis (Accessed: 2024-12-01)
3. https://acmecorp.com/careers - Job postings (Accessed: 2024-12-01)
4. https://acmecorp.com/press/soc2-certification-2024 - SOC 2 announcement (Published: 2024-06-15)
5. https://github.com/acmecorp - GitHub organization (Accessed: 2024-12-01)
6. https://linkedin.com/jobs/search?company=acmecorp - Job listings (Accessed: 2024-12-01)
7. https://techcrunch.com/2024/09/15/acmecorp-security-incident - Incident news (Published: 2024-09-15)
8. https://acmecorp.com/blog/incident-response-update - Post-mortem blog (Published: 2024-09-20)
[... 7 more sources ...]

### Grok Social Intelligence
1. https://x.com/AcmeCorp/status/1234567890 - Corporate incident response (Posted: 2024-09-16, 450 RT, 1.2K likes)
2. https://x.com/johndoe_dev/status/1234567891 - Developer security update (Posted: 2024-10-05, 25 RT, 80 likes)
3. https://x.com/janedoe_ciso/status/1234567892 - CISO hiring announcement (Posted: 2024-10-15, 40 RT, 150 likes)
4. https://x.com/angry_customer/status/1234567893 - Customer complaint (Posted: 2024-09-17, 85 RT, 200 likes)
5. https://x.com/security_analyst/status/1234567894 - Analyst commentary (Posted: 2024-09-18, 120 RT, 300 likes)
[... 5 more tweets ...]

---

**Research Completed:** 2024-12-01
**Total Time:** 60 minutes
**Confidence Levels:** High (both sources confirmed), Medium (one source), Low (social media only)
**Next Steps:** Use findings for pentest scoping, focus on AWS security and S3 configurations

---

**Related:**
- `methodologies/dual-source-research.md` - Research methodology used
- `reference/intelligence-areas.md` - Intelligence categories covered
- `workflows/deep-mode-research.md` - Workflow followed for this example
