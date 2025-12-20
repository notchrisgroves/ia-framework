# Changelog

All notable changes to the IA Framework will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-12-19

### Added

**Framework Core**
- Hierarchical context loading architecture (CLAUDE.md → SKILL.md → reference/)
- Centralized path management for cross-platform portability
- Framework update tool with conflict detection
- Pre-commit validation hooks for agents, credentials, documentation

**Agents**
- Security agent - Penetration testing, code review, architecture analysis
- Writer agent - Blog posts, technical documentation, security reports
- Advisor agent - Career development, OSINT research, QA review
- Legal agent - Compliance review with citation verification

**Skills**
- Security testing (pentest, vuln-scan, segmentation-test)
- Security analysis (code-review, arch-review, threat-intel, dependency-audit)
- Security advisory (risk-assessment, secure-config, benchmark-generation)
- Career development (job analysis, mentorship, CliftonStrengths)
- Content creation (blog posts, diagrams, newsletters)
- Health & wellness (fitness programming, alternative health)
- Legal compliance (HIPAA, PCI DSS, GDPR, SOC 2)

**Commands**
- `/pentest`, `/vuln-scan`, `/segmentation-test` - Security testing
- `/code-review`, `/arch-review`, `/threat-intel` - Security analysis
- `/risk-assessment`, `/secure-config`, `/benchmark-gen` - Compliance
- `/job-analysis`, `/mentorship`, `/clifton` - Career
- `/blog-post`, `/newsletter`, `/diagram` - Content
- `/training`, `/wellness` - Health
- `/compliance`, `/policy` - Legal

**Resources**
- NIST CSF, SP 800-53 framework references
- OWASP Top 10, ASVS, testing guides
- CIS Benchmarks, DISA STIGs
- MITRE ATT&CK, CVE research integration

**VPS Integration**
- Kali pentest tools (nmap, nuclei, sqlmap, nikto)
- Web3 security tools (slither, mythril, echidna)
- Mobile security tools (apktool, jadx, frida)
- Metasploit framework

### Technical

- Python 3.10+ required for validation tools
- Cross-platform support (Windows, macOS, Linux)
- Environment variable configuration via `.env`
- Git-based installation to `~/.claude`

---

**Framework:** Intelligence Adjacent (IA)
**Repository:** https://github.com/notchrisgroves/ia-framework
