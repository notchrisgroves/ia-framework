
## Program Description

[Brief description of the target organization, product, or platform. Include key technologies, blockchain networks, or infrastructure details.]

**Technology Stack:**
- [Primary tech stack items]
- [Blockchain/Layer if applicable]
- [Key frameworks or platforms]

---

## Authorization & Safe Harbor

[State authorization basis - bug bounty program, signed SOW, VDP policy, etc.]

**Key Terms:**
- **KYC Required:** [Yes/No]
- **Proof of Concept:** [Required/Optional]
- **Primacy of Impact:** [Enabled/Disabled]
- **Responsible Publication:** [Category and disclosure requirements]

**Safe Harbor Statement:**
[Copy safe harbor language from program policy]

---

## In-Scope Assets

### [Asset Category 1: e.g., Smart Contracts]

1. **[Asset Name/Description]**
   - Address/URL: `[identifier]`
   - Function: [What this asset does]
   - Special Notes: [Any specific testing considerations]

2. **[Asset Name/Description]**
   - Address/URL: `[identifier]`
   - Function: [What this asset does]

### [Asset Category 2: e.g., Web/Application Assets]

1. **[Asset Name]**
   - URL: `[full URL]`
   - Function: [Purpose/functionality]

2. **[Asset Name]**
   - URL: `[full URL]`
   - Function: [Purpose/functionality]

### [Asset Category 3: e.g., APIs]

1. **[API Name]**
   - Endpoint: `[base URL]`
   - Documentation: [docs URL if available]
   - Authentication: [auth method]

---

## Out-of-Scope Assets & Activities

### Explicitly Excluded Vulnerabilities

[List vulnerabilities that are out of scope per program policy]

**Common Exclusions:**
- Third-party oracle incorrect data (unless oracle manipulation)
- Governance attacks (51% attacks)
- Sybil attack impacts
- Centralization risk impacts
- Theoretical impacts without proof of concept
- Self-XSS vulnerabilities
- CSRF without state modification
- Missing HTTP headers without demonstrated impact
- DDoS-only impacts
- Browser/plugin defects

### Known Issues (Excluded)

[List known issues from previous audits or program disclosures]

**Examples:**
- All [dependency name] issues
- Acknowledged issues from [audit firm] audit
- Issues listed in [security documentation URL]

### Prohibited Testing Activities

[Critical restrictions from program policy]

**Common Prohibitions:**
1. **Mainnet/Production Testing Restrictions:**
   - [Specify if testing allowed on production or only on local forks/testnets]

2. **Additional Prohibited Activities:**
   - Phishing attacks against team/users
   - Testing on third-party systems/dependencies
   - Denial of Service (DoS) attacks
   - Automated traffic generation/load testing
   - Public disclosure of unpatched vulnerabilities
   - [Add program-specific restrictions]

---

## Reward Structure

### [Asset Type 1: e.g., Smart Contract Vulnerabilities]

| Severity | Max Reward | Calculation Method |
|----------|------------|-------------------|
| Critical | $[amount] | [How calculated - % of funds, fixed, range] |
| High | $[amount] | [Calculation method] |
| Medium | $[amount] | [Calculation method] |
| Low | $[amount] | [Calculation method] |

**Special Rules:**
- [Any multipliers, minimums, or special conditions]
- [Payment token and chain]

### [Asset Type 2: e.g., Web/Application Vulnerabilities]

| Severity | Max Reward | Special Conditions |
|----------|------------|-------------------|
| Critical | $[amount] | [Conditions for this severity] |
| High | $[amount] | [Conditions] |
| Medium | $[amount] | [Conditions] |
| Low | $[amount] | [Conditions] |

**Payment Terms:**
- Handled by: [Platform or direct client]
- Payment Token: [USDC, BTC, direct wire, etc.]
- Payment Chain: [Ethereum, Polygon, etc.]
- Rate Calculation: [How crypto prices determined]

---

## Testing Requirements

### Mandatory Testing Headers (HTTP/HTTPS)

**Platform:** [HackerOne / Immunefi / Bugcrowd / Other]

**HackerOne Programs:**
```
X-HackerOne-Username: notchrisgroves
X-Bug-Bounty: notchrisgroves
From: notchrisgroves@wearehackerone.com
```

**Immunefi Programs:**
```
X-Bug-Bounty: immunefi
X-Researcher: notchrisgroves
From: chris@notchrisgroves.com
```

**Bugcrowd Programs:**
```
X-Bugcrowd-Researcher: notchrisgroves
X-Bug-Bounty: bugcrowd
```

**Direct Client (No Platform):**
```
X-Security-Test: authorized
X-Tester: notchrisgroves
From: chris@notchrisgroves.com
```

**Note:** [Any program-specific header requirements or clarifications]

### Environment Requirements

1. **[Asset Type] Testing:**
   - Environment: [Local fork / Testnet / Production with restrictions]
   - Tools: [Required or recommended tools]
   - Setup: [Any specific environment setup requirements]

2. **[Asset Type] Testing:**
   - [Requirements for this asset type]

### Proof of Concept Requirements

- Required for: [Which severities require PoC]
- Must demonstrate: [What needs to be shown]
- Format: [Any specific PoC format requirements]
- Should NOT include: [Restrictions on PoC content]

### Rate Limiting & Testing Constraints

- **Rate Limits:** [Any API rate limits or testing frequency restrictions]
- **Test Accounts:** [Guidelines for creating test accounts]
- **Data Sensitivity:** [Rules about handling sensitive data]
- **Logging:** [Whether tests are logged/monitored]

---

## Special Considerations

### [Asset Type] Focus Areas

1. **[Security Domain 1]**
   - [Specific vulnerability classes to investigate]
   - [Platform-specific considerations]

2. **[Security Domain 2]**
   - [Attack vectors]
   - [Common pitfalls in this technology]

3. **[Security Domain 3]**
   - [Testing approaches]
   - [Edge cases to consider]

### Industry-Specific Threats

**Relevant Industry:** [e.g., DeFi, Exchange, NFT Marketplace, Payment Processor]

**See:** `02-reconnaissance/industry-threat-intel.md` for detailed analysis of:
- Recent breaches in this industry
- Known vulnerabilities in competitor platforms
- Novel attack patterns specific to this sector
- Applicable CVEs and security advisories

---

## Engagement Credentials

**Location:** `creds.txt` (git-ignored)

**Credential Types:**
- [List types of credentials available - test accounts, API keys, etc.]
- [Note if credentials need to be created vs provided]

---

## Emergency Contacts

**Critical Vulnerability Disclosure:**
- Platform: [Contact method through bug bounty platform]
- Direct Contact: [If provided, otherwise use platform only]
- Severity Threshold: [When to use emergency contact vs normal submission]

**Escalation Process:**
- [Steps for reporting critical vulnerabilities]
- [Expected response time]

---

## Testing Methodology References

**Applicable Standards:**
- [Relevant OWASP Top 10 versions]
- [Industry-specific security standards]
- [Blockchain/smart contract security guides]
- [Platform-specific testing methodologies]

**Audit References:**
- [List any available audit reports for context]
- Location: `02-reconnaissance/audits/`

---

**Last Updated:** [YYYY-MM-DD]
**Version:** 1.0
