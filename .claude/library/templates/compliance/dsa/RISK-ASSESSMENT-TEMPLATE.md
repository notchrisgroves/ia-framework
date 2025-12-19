# DSA-Compliant Risk Assessment Policy & Methodology Template
## Articles 34-35: Systemic Risk Assessment and Mitigation

**Policy Type:** Risk Assessment Methodology & Documentation
**DSA Articles Covered:** Article 34 (Risk Assessment), Article 35 (Risk Mitigation)
**Target Services:** VLOP/VLOSE only (designated services with 45M+ monthly EU users)
**Template Version:** 1.0
**Last Updated:** 2025-12-02

---

## How to Use This Template

1. **Fill in all [bracketed] fields** with service-specific information
2. **Complete risk assessment for all 5 mandatory risk categories** (DSA Article 34(1))
3. **Update annually** or when significant changes occur (DSA Article 34(1))
4. **Submit to European Commission** via DSA transparency database
5. **Legal review required** before finalization and submission
6. **Independent audit required** (DSA Article 37) - conducted by certified auditors

**DSA Requirements Checklist:**
- [ ] All 5 systemic risk categories assessed
- [ ] Service-specific risks identified for your platform
- [ ] Platform design contribution to risks analyzed
- [ ] Risk severity ratings assigned (methodology documented)
- [ ] Mitigation measures defined for each risk
- [ ] Effectiveness measurement procedures established
- [ ] Independent audit planned (Article 37 requirement)
- [ ] Annual update scheduled

---

# [SERVICE NAME] Systemic Risk Assessment
## DSA Articles 34-35 Compliance Documentation

**Assessment for EU Digital Services Act VLOP/VLOSE Requirements**

---

## COMPONENT 1: Metadata & Scope

**Service Name:** [SERVICE NAME - e.g., Google Play, Google Search, Google Maps]

**Service Designation:** [VLOP / VLOSE]

**Monthly Active EU Users:** [NUMBER - e.g., 45M+]

**Designation Date:** [DATE - when EC designated service as VLOP/VLOSE]

**Assessment Version:** [VERSION - e.g., 1.0, 2.0]

**Assessment Period:** [START DATE] to [END DATE]

**Effective Date:** [DATE]

**Next Scheduled Assessment:** [DATE - must be within 12 months]

**Responsible Owner:**
- **Executive Sponsor:** [NAME, TITLE - C-level executive]
- **Assessment Lead:** [NAME, TITLE - VP or Director level]
- **Cross-Functional Team:** [LIST DEPARTMENTS - e.g., Trust & Safety, Legal, Product, Engineering, Policy, Data Science]

**Regulatory Basis:**
- EU Digital Services Act (Regulation 2022/2065), Articles 34-35
- EUR-Lex Reference: https://eur-lex.europa.eu/eli/reg/2022/2065

**Assessment Methodology:**
- Based on: [e.g., "ISO 31000 Risk Management," "NIST Cybersecurity Framework," "Internal Risk Assessment Framework v2.1"]
- Independent Validation: [AUDIT FIRM - per DSA Article 37]
- Audit Date: [DATE]
- Audit Report: [REFERENCE NUMBER / URL if public]

**Change History:**
| Version | Date | Changes | Approver |
|---------|------|---------|----------|
| [1.0] | [Date] | Initial DSA-compliant risk assessment | [C-Suite Name] |
| [2.0] | [Date] | [Description - e.g., "Added new risks from Q3 incidents"] | [C-Suite Name] |

---

## COMPONENT 2: Executive Summary

### Assessment Purpose

This Risk Assessment fulfills our obligations under DSA Articles 34 and 35 as a [VLOP/VLOSE] designated service. We assess **systemic risks** arising from the design, functioning, and use of [SERVICE NAME] to identify, analyze, and mitigate harms to:
- **Public Safety:** Illegal content dissemination
- **Civic Discourse:** Electoral integrity, public debate manipulation
- **Human Rights:** Fundamental rights impacts
- **Vulnerable Groups:** Minors, marginalized communities, violence victims

### Assessment Scope

**Services Covered:**
- [PRIMARY SERVICE NAME]
- [LIST ALL FEATURES - e.g., "Content upload, recommendations, search, comments, messaging, live streaming, advertising"]

**Geographic Scope:**
- **Primary Focus:** European Union (27 member states)
- **Global Context:** Where risks in other regions may impact EU users

**User Base:**
- **Total EU Users:** [NUMBER] monthly active users
- **User Demographics:** [BREAKDOWN - e.g., "Ages 13-17: 15%, 18-24: 30%, 25-34: 25%, 35+: 30%"]
- **Vulnerable Groups:** [PERCENTAGE - e.g., "Estimated 15% minors, 5% vulnerable adults"]

### Key Findings Summary

**Critical Risks Identified:** [NUMBER]
**High Risks Identified:** [NUMBER]
**Medium Risks Identified:** [NUMBER]
**Low Risks Identified:** [NUMBER]

**Top 3 Critical Risks:**
1. [RISK NAME - e.g., "Viral spread of child sexual abuse material (CSAM)"]
2. [RISK NAME - e.g., "Recommender systems amplifying election disinformation"]
3. [RISK NAME - e.g., "Coordinated inauthentic behavior targeting political campaigns"]

**Mitigation Investment:** €[AMOUNT] committed for [TIMEFRAME]

**Audit Status:** [COMPLETE / IN PROGRESS / SCHEDULED]

---

## COMPONENT 3: Risk Assessment Framework

### Methodology Overview

**Risk Assessment Process:**

```
┌─────────────────────────────────────────────────────────────┐
│              SYSTEMIC RISK ASSESSMENT PROCESS               │
└─────────────────────────────────────────────────────────────┘

STEP 1: RISK IDENTIFICATION
   │
   ├─→ Mandatory Categories (DSA Article 34)
   │   ├─ Illegal Content Dissemination
   │   ├─ Fundamental Rights Impacts
   │   ├─ Electoral Process Integrity
   │   ├─ Gender-Based Violence
   │   └─ Minor Protection
   │
   ├─→ Platform-Specific Risks
   │   └─ Service-specific risks based on features
   │
   └─→ Emerging Risks
       └─ New threats identified through monitoring

STEP 2: DESIGN CONTRIBUTION ANALYSIS
   │
   └─→ How does OUR platform amplify or enable each risk?
       ├─ Recommender systems (algorithms)
       ├─ Content moderation capabilities
       ├─ Viral spread mechanisms (sharing, reposting)
       ├─ User interface design (dark patterns?)
       ├─ Advertising systems
       └─ Community features (comments, messaging, etc.)

STEP 3: RISK SEVERITY RATING
   │
   └─→ Likelihood × Impact = Severity
       ├─ Likelihood: How often could this occur?
       ├─ Impact: How harmful if it occurs?
       └─ Severity: Critical / High / Medium / Low

STEP 4: MITIGATION PLANNING
   │
   └─→ For each risk, define:
       ├─ Prevention measures (stop it before it happens)
       ├─ Detection systems (identify it quickly)
       ├─ Response procedures (address it when found)
       └─ Recovery processes (support affected users)

STEP 5: EFFECTIVENESS MEASUREMENT
   │
   └─→ How do we know mitigation is working?
       ├─ Key Performance Indicators (KPIs)
       ├─ Metrics tracking (monthly/quarterly)
       ├─ Incident analysis (did we prevent/detect/respond?)
       └─ Continuous improvement (adjust based on results)
```

### Risk Severity Rating Scale

**Severity = Likelihood × Impact**

**Likelihood:**
- **Very High (5):** Occurs daily or continuously
- **High (4):** Occurs weekly or frequently
- **Medium (3):** Occurs monthly or occasionally
- **Low (2):** Occurs quarterly or rarely
- **Very Low (1):** Occurs annually or almost never

**Impact:**
- **Catastrophic (5):** Severe harm to large populations, loss of life, major rights violations
- **Major (4):** Significant harm to many users, substantial rights impacts
- **Moderate (3):** Noticeable harm to moderate number of users
- **Minor (2):** Limited harm to small number of users
- **Minimal (1):** Negligible harm, no lasting effects

**Severity Score (Likelihood × Impact):**
- **20-25:** CRITICAL - Immediate action required
- **12-19:** HIGH - Priority mitigation needed
- **6-11:** MEDIUM - Mitigation planned
- **1-5:** LOW - Monitor and review

---

## COMPONENT 4: Risk Category 1 - Illegal Content Dissemination

**DSA Article 34(1)(a):** Dissemination of illegal content

### Risk Identification

**Illegal Content Types Relevant to [SERVICE NAME]:**

[CHECK ALL THAT APPLY TO YOUR SERVICE:]

☐ **Child Sexual Abuse Material (CSAM)**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA - e.g., "0.001% of content flagged"]
   - User Reports: [NUMBER] reports per month (average)

☐ **Terrorist Content**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA]
   - User Reports: [NUMBER] per month

☐ **Hate Speech / Incitement to Violence**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA]
   - User Reports: [NUMBER] per month

☐ **Copyright Infringement**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA]
   - User Reports: [NUMBER] per month

☐ **Sale of Illegal Goods/Services**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Drugs, weapons, counterfeit products, stolen goods"]
   - User Reports: [NUMBER] per month

☐ **Fraud / Scams**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Phishing, fake products, pyramid schemes"]
   - User Reports: [NUMBER] per month

☐ **Other Illegal Content:**
   - [SPECIFY - e.g., "Revenge porn," "Defamation," "Illegal gambling"]

### Platform Design Contribution Analysis

**How does [SERVICE NAME]'s design contribute to illegal content risks?**

**Recommender Systems:**
[EXPLAIN IF/HOW RECOMMENDATIONS AMPLIFY ILLEGAL CONTENT]

**Example - Video Platform:**
"Our 'Up Next' recommender may surface related content after a user views borderline material, potentially creating pathways to illegal content. Viral coefficient for policy-violating content is [X] (average video leads to [X] additional views)."

**Example - Marketplace:**
"Search ranking algorithm prioritizes high-engagement listings, which can inadvertently boost illegal product listings if they receive significant initial traffic before detection."

**Content Velocity:**
[EXPLAIN UPLOAD/POSTING VOLUME AND SPEED]

**Example:**
"[NUMBER] pieces of content uploaded per minute. Current detection systems catch violations within [TIMEFRAME - e.g., '90 seconds on average'], but [PERCENTAGE] slip through initial moderation and require user reports."

**Virality Mechanisms:**
[EXPLAIN SHARING, REPOSTING, AMPLIFICATION FEATURES]

**Example:**
"Share/repost features allow content to reach [X] additional users within [TIMEFRAME]. Illegal content that evades initial detection can reach [NUMBER] users before removal."

**Anonymity / Pseudonymity:**
[EXPLAIN USER IDENTITY REQUIREMENTS]

**Example:**
"Users can create accounts without identity verification, enabling bad actors to create multiple accounts for illegal activity. Average time to detect repeat offenders: [TIMEFRAME]."

**Monetization:**
[EXPLAIN IF ILLEGAL ACTIVITY CAN BE MONETIZED]

**Example:**
"Advertising revenue sharing may incentivize upload of copyright-infringing content. Detection rate before monetization: [PERCENTAGE]%."

### Risk Severity Assessment

[FOR EACH ILLEGAL CONTENT TYPE:]

**Risk: [CONTENT TYPE]**

- **Likelihood:** [SCORE 1-5] - [JUSTIFICATION]
- **Impact:** [SCORE 1-5] - [JUSTIFICATION]
- **Severity:** [SCORE 1-25] - [CRITICAL / HIGH / MEDIUM / LOW]

**Example - CSAM:**
- **Likelihood:** 2 (Low) - "Detected in 0.001% of content; robust detection systems in place"
- **Impact:** 5 (Catastrophic) - "CSAM causes severe harm to victims and violates fundamental rights"
- **Severity:** 10 (MEDIUM-HIGH) - "Despite low likelihood, impact severity requires high-priority mitigation"

### Current Mitigation Measures

**Prevention:**
☐ Upload filters (e.g., PhotoDNA for CSAM, hash matching for known illegal content)
☐ Account restrictions (age verification, identity checks for certain features)
☐ Terms of Service prohibitions with clear examples
☐ User education (tooltips, warnings before posting)

**Detection:**
☐ Automated content scanning (AI/ML models for [CONTENT TYPES])
☐ Hash-based detection (for known illegal content)
☐ User reporting mechanisms (easy-to-find reporting buttons)
☐ Trusted flagger program (expedited review for expert reporters)
☐ Proactive monitoring (hunting for illegal content patterns)

**Response:**
☐ Rapid removal (within [TIMEFRAME] of detection)
☐ Account suspension/termination for uploaders
☐ Law enforcement reporting (for CSAM, terrorism, serious crimes)
☐ User notification (Statement of Reasons per Article 20)

**Recovery:**
☐ Victim support resources (for CSAM, abuse content)
☐ Appeal mechanisms (for false positives)
☐ Transparency reporting (public metrics per Article 24)

### Effectiveness Measurement

**Key Performance Indicators:**

1. **Detection Rate:** [PERCENTAGE]% of illegal content detected before public exposure
2. **Response Time:** [TIMEFRAME] average from upload to removal
3. **Recurrence Rate:** [PERCENTAGE]% of removed content re-uploaded
4. **False Positive Rate:** [PERCENTAGE]% of removed content reinstated on appeal
5. **User Report Volume:** [TREND - increasing/decreasing/stable]

**Monitoring Frequency:** [DAILY / WEEKLY / MONTHLY]

**Reporting:** [INTERNAL CADENCE - e.g., "Monthly to Trust & Safety leadership, Quarterly to Board"]

### Remaining Gaps & Planned Improvements

**Identified Gaps:**
1. [GAP - e.g., "Limited detection of [CONTENT TYPE] in [LANGUAGE]"]
2. [GAP - e.g., "Response time exceeds [TIMEFRAME] for [CONTENT TYPE]"]
3. [GAP - e.g., "Recommender systems may surface borderline content"]

**Improvement Roadmap:**
| Improvement | Timeline | Investment | Owner |
|-------------|----------|------------|-------|
| [INITIATIVE] | [Q1 2025] | [€ AMOUNT] | [TEAM] |
| [INITIATIVE] | [Q2 2025] | [€ AMOUNT] | [TEAM] |

---

## COMPONENT 5: Risk Category 2 - Fundamental Rights Impacts

**DSA Article 34(1)(b):** Negative effects on fundamental rights

### Risk Identification

**Fundamental Rights Potentially Impacted by [SERVICE NAME]:**

[CHECK ALL THAT APPLY:]

☐ **Freedom of Expression (Charter Article 11)**
   - Risk: [Over-removal of lawful content, censorship]
   - Severity: [SCORE]

☐ **Right to Privacy (Charter Article 7)**
   - Risk: [Excessive data collection, surveillance, tracking]
   - Severity: [SCORE]

☐ **Right to Non-Discrimination (Charter Article 21)**
   - Risk: [Algorithmic bias in content moderation or recommendations]
   - Severity: [SCORE]

☐ **Rights of the Child (Charter Article 24)**
   - Risk: [Age-inappropriate content exposure, exploitation]
   - Severity: [SCORE]

☐ **Right to Human Dignity (Charter Article 1)**
   - Risk: [Harassment, hate speech, doxing, defamation]
   - Severity: [SCORE]

☐ **Freedom of Assembly (Charter Article 12)**
   - Risk: [Disruption of legitimate organizing, protests]
   - Severity: [SCORE]

☐ **Other Rights:**
   - [SPECIFY - e.g., "Right to be forgotten," "Consumer rights"]

### Platform Design Contribution Analysis

**How does [SERVICE NAME]'s design impact fundamental rights?**

**Content Moderation:**
[ANALYZE OVER-REMOVAL vs UNDER-REMOVAL RISKS]

**Example:**
"Automated content moderation removes [NUMBER] posts per day. False positive rate: [PERCENTAGE]%, affecting freedom of expression for [NUMBER] users monthly. Appeal rate: [PERCENTAGE]%, reinstatement rate: [PERCENTAGE]%."

**Algorithmic Decision-Making:**
[ANALYZE RECOMMENDATION, RANKING, FILTERING ALGORITHMS]

**Example:**
"Recommender systems prioritize engagement, which may amplify extreme content over moderate voices. [PERCENTAGE]% of recommended content falls in 'borderline' policy area. Bias testing shows [DEMOGRAPHIC GROUP] content is [X] times more likely to be downranked/removed."

**Data Collection & Processing:**
[ANALYZE PRIVACY IMPACTS]

**Example:**
"Platform collects [LIST DATA TYPES - e.g., 'browsing history, location, contacts, device data']. Used for [PURPOSES - e.g., 'ad targeting, recommendations']. Users can opt out: [YES/NO]. If yes, impact on service: [DESCRIPTION]."

**Advertising & Targeting:**
[ANALYZE DISCRIMINATORY AD TARGETING RISKS]

**Example:**
"Advertisers can target by [CRITERIA - e.g., 'age, gender, location, interests']. Prohibited targeting: [LIST - e.g., 'race, religion, health conditions']. Enforcement rate: [PERCENTAGE]% of prohibited ads detected."

### Risk Severity Assessment

[FOR EACH FUNDAMENTAL RIGHT:]

**Risk: [RIGHT NAME]**

- **Likelihood:** [SCORE 1-5] - [JUSTIFICATION]
- **Impact:** [SCORE 1-5] - [JUSTIFICATION]
- **Severity:** [SCORE 1-25] - [CRITICAL / HIGH / MEDIUM / LOW]

**Example - Freedom of Expression:**
- **Likelihood:** 4 (High) - "Automated moderation processes [NUMBER] content pieces daily; false positives inevitable"
- **Impact:** 3 (Moderate) - "Over-removal silences voices but appeal process available"
- **Severity:** 12 (HIGH) - "Balance required between content moderation and free speech"

### Current Mitigation Measures

**Policy Design:**
☐ Clear content policies (avoid vague rules like "inappropriate content")
☐ Narrow restrictions (only prohibit what's necessary)
☐ Public exceptions (newsworthy, educational, satirical content protection)

**Process Safeguards:**
☐ Human review for borderline content (not fully automated)
☐ Appeal mechanisms (easy access, independent reviewers)
☐ Transparency (public policy explanations, transparency reports)
☐ User control (content filtering preferences, block/mute features)

**Algorithmic Safeguards:**
☐ Bias testing (regular audits for demographic disparities)
☐ Algorithmic transparency (explain how recommendations work)
☐ User control over algorithms (opt-out of personalization)
☐ Diverse content exposure (avoid filter bubbles)

**Data Protection:**
☐ Privacy-by-design (minimize data collection)
☐ User consent (clear opt-in for non-essential data uses)
☐ Data access (users can view/download/delete their data)
☐ Encryption (data protection at rest and in transit)

### Effectiveness Measurement

**Key Performance Indicators:**

1. **Appeal Reversal Rate:** [PERCENTAGE]% (indicates over-removal if high)
2. **User Complaints:** [NUMBER] rights-related complaints per quarter
3. **Bias Audit Results:** [FINDINGS - e.g., "No significant demographic disparities detected"]
4. **Transparency Score:** [METRIC - e.g., "Ranking Transparency Coalition score: [X]/100"]
5. **Privacy Compliance:** [STATUS - e.g., "GDPR audits: 0 violations in past 12 months"]

### Remaining Gaps & Planned Improvements

**Identified Gaps:**
1. [GAP]
2. [GAP]

**Improvement Roadmap:**
| Improvement | Timeline | Investment | Owner |
|-------------|----------|------------|-------|
| [INITIATIVE] | [DATE] | [€ AMOUNT] | [TEAM] |

---

## COMPONENT 6: Risk Category 3 - Electoral Process Integrity

**DSA Article 34(1)(c):** Negative effects on democratic processes, civic discourse, and electoral processes

### Risk Identification

**Electoral Risks Relevant to [SERVICE NAME]:**

[CHECK ALL THAT APPLY:]

☐ **Disinformation Campaigns**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "False voting information, candidate defamation, deepfakes"]

☐ **Foreign Interference**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "State-backed influence operations, fake accounts"]

☐ **Coordinated Inauthentic Behavior**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Bot networks, troll farms, astroturfing"]

☐ **Microtargeting / Political Ad Manipulation**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Discriminatory ad targeting, dark ads, misleading claims"]

☐ **Voter Suppression**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "False polling place info, intimidation"]

☐ **Polarization / Filter Bubbles**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Algorithmic amplification of extreme content"]

### Platform Design Contribution Analysis

**How does [SERVICE NAME] impact electoral integrity?**

**Information Spread:**
[EXPLAIN VIRALITY, AMPLIFICATION, ALGORITHMIC DISTRIBUTION]

**Example:**
"Election-related content receives [X] times more engagement than average content. Recommender systems prioritize highly engaging content, which may amplify sensational or false claims. [PERCENTAGE]% of election content comes from [TOP X%] of accounts."

**Ad Targeting:**
[EXPLAIN POLITICAL AD CAPABILITIES]

**Example:**
"Political ads can target by [CRITERIA]. We [DO / DO NOT] allow microtargeting for political ads. Political ad transparency: [PUBLIC AD LIBRARY - YES/NO]. Historical spending: €[AMOUNT] on political ads in [TIMEFRAME]."

**Account Authenticity:**
[EXPLAIN VERIFICATION, FAKE ACCOUNT DETECTION]

**Example:**
"We detect and remove [NUMBER] fake accounts per month. Coordinated networks of [X+] accounts detected [NUMBER] times in past year. [PERCENTAGE] were election-related."

### Risk Severity Assessment

**Risk: [ELECTION RISK TYPE]**

- **Likelihood:** [SCORE 1-5] - [JUSTIFICATION]
- **Impact:** [SCORE 1-5] - [JUSTIFICATION]
- **Severity:** [SCORE 1-25] - [CRITICAL / HIGH / MEDIUM / LOW]

**Example - Disinformation Campaigns:**
- **Likelihood:** 4 (High) - "Occurs during every major election cycle; detected [NUMBER] incidents in past year"
- **Impact:** 4 (Major) - "Can influence voter behavior and undermine democratic processes"
- **Severity:** 16 (HIGH) - "High priority mitigation required"

### Current Mitigation Measures

**Election Integrity Program:**
☐ Dedicated team (size: [NUMBER] people, availability: [24/7 during elections / always])
☐ Election Operations Center (activated [TIMEFRAME] before major elections)
☐ Fact-checking partnerships ([NUMBER] partners in EU)
☐ Labeling (disputed claims labeled with fact-check links)

**Political Ad Transparency:**
☐ Ad library (public searchable database of all political ads)
☐ Targeting transparency (show who was targeted, why)
☐ Spending caps (limit: €[AMOUNT] per advertiser)
☐ Verification (political advertisers must verify identity)

**Coordinated Behavior Detection:**
☐ Network analysis (detect coordinated account groups)
☐ Behavioral signals (unusual posting patterns, engagement manipulation)
☐ Takedown procedures ([TIMEFRAME] to investigate and remove)

**Crisis Response (Article 36):**
☐ Crisis protocol (activated during elections, crises)
☐ Government coordination (liaison with electoral commissions, law enforcement)
☐ Rapid response (can act within [TIMEFRAME] for urgent threats)

### Effectiveness Measurement

**Key Performance Indicators:**

1. **Disinformation Detection:** [PERCENTAGE]% of known false claims labeled within [TIMEFRAME]
2. **Fake Account Removal:** [NUMBER] accounts removed per month
3. **Political Ad Compliance:** [PERCENTAGE]% of ads in public library
4. **User Trust:** [METRIC - e.g., "User survey: [X]% trust election information on platform"]

### Remaining Gaps & Planned Improvements

**Identified Gaps:**
1. [GAP]
2. [GAP]

**Improvement Roadmap:**
| Improvement | Timeline | Investment | Owner |
|-------------|----------|------------|-------|
| [INITIATIVE] | [DATE] | [€ AMOUNT] | [TEAM] |

---

## COMPONENT 7: Risk Category 4 - Gender-Based Violence

**DSA Article 34(1)(d):** Negative effects on gender-based violence

### Risk Identification

**Gender-Based Violence Risks Relevant to [SERVICE NAME]:**

[CHECK ALL THAT APPLY:]

☐ **Online Harassment / Abuse**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA - e.g., "Women receive [X] times more harassment"]

☐ **Doxing / Privacy Violations**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Address/phone leaks targeting women, revenge porn"]

☐ **Threats of Violence**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Rape threats, death threats, stalking"]

☐ **Image-Based Abuse**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Non-consensual intimate images (NCII), deepfake porn"]

☐ **Coordinated Harassment Campaigns**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Brigading, pile-ons targeting women"]

☐ **Dating/Romance Scams**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Catfishing, financial exploitation"]

### Platform Design Contribution Analysis

**How does [SERVICE NAME] enable or amplify gender-based violence?**

**Visibility & Reach:**
[EXPLAIN HOW ABUSERS CAN REACH TARGETS]

**Example:**
"Public profiles allow anyone to contact users. [PERCENTAGE]% of harassment comes from unknown accounts. Women with public profiles receive [X] times more unwanted contact than men."

**Anonymity:**
[EXPLAIN IDENTITY PROTECTION FOR ABUSERS]

**Example:**
"Anonymous accounts can send messages without revealing identity. Abusers create [NUMBER] throwaway accounts monthly to evade blocks."

**Content Spread:**
[EXPLAIN SHARING, RESHARING OF ABUSIVE CONTENT]

**Example:**
"Intimate images can be shared [NUMBER] times before removal. Average spread: [NUMBER] views, [NUMBER] downloads before takedown."

### Risk Severity Assessment

**Risk: [GENDER-BASED VIOLENCE TYPE]**

- **Likelihood:** [SCORE 1-5] - [JUSTIFICATION]
- **Impact:** [SCORE 1-5] - [JUSTIFICATION]
- **Severity:** [SCORE 1-25] - [CRITICAL / HIGH / MEDIUM / LOW]

**Example - Image-Based Abuse:**
- **Likelihood:** 3 (Medium) - "Detected [NUMBER] cases per month; underreporting likely"
- **Impact:** 5 (Catastrophic) - "Severe psychological harm, safety risks, long-term trauma"
- **Severity:** 15 (HIGH) - "High priority mitigation required"

### Current Mitigation Measures

**Prevention:**
☐ Privacy controls (limit who can contact, view profile, share content)
☐ Safety mode (auto-filter messages from unknown accounts)
☐ Warnings (before posting potentially sensitive content)

**Detection:**
☐ Proactive scanning (for NCII using hash matching)
☐ User reporting (one-click reporting for harassment)
☐ Priority review (fast-track for violence/abuse reports)

**Response:**
☐ Rapid removal ([TIMEFRAME] for NCII, threats)
☐ Account penalties (suspension/termination for abusers)
☐ Safety features (block, mute, restrict)
☐ Victim support (resources, safety planning tools)

**Partnerships:**
☐ NGOs (collaborate with [ORGANIZATIONS - e.g., "Refuge, Women's Aid"])
☐ Law enforcement (reporting channel for serious threats)
☐ Helplines (in-platform links to [SERVICES])

### Effectiveness Measurement

**Key Performance Indicators:**

1. **Response Time:** [TIMEFRAME] average for high-priority reports
2. **Removal Rate:** [PERCENTAGE]% of reported content removed
3. **Recidivism:** [PERCENTAGE]% of removed abusers create new accounts
4. **User Safety:** [METRIC - e.g., "Survey: [X]% of women feel safe on platform"]

### Remaining Gaps & Planned Improvements

**Identified Gaps:**
1. [GAP]
2. [GAP]

**Improvement Roadmap:**
| Improvement | Timeline | Investment | Owner |
|-------------|----------|------------|-------|
| [INITIATIVE] | [DATE] | [€ AMOUNT] | [TEAM] |

---

## COMPONENT 8: Risk Category 5 - Minor Protection

**DSA Article 34(1)(d):** Protection of minors

### Risk Identification

**Minor Protection Risks Relevant to [SERVICE NAME]:**

[CHECK ALL THAT APPLY:]

☐ **Age-Inappropriate Content Exposure**
   - Risk Level: [SEVERITY SCORE]
   - Examples: [e.g., "Violence, sexual content, substance abuse"]

☐ **Online Predators / Grooming**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA]

☐ **Addictive Design Patterns**
   - Risk Level: [SEVERITY SCORE]
   - Features: [e.g., "Infinite scroll, autoplay, notifications, streaks, rewards"]

☐ **Targeted Advertising to Minors**
   - Risk Level: [SEVERITY SCORE]
   - Ad types: [e.g., "Gambling ads, unhealthy food, appearance products"]

☐ **Cyberbullying / Peer Harassment**
   - Risk Level: [SEVERITY SCORE]
   - Prevalence: [DATA - e.g., "[X]% of teen users report being bullied"]

☐ **Data Collection from Minors**
   - Risk Level: [SEVERITY SCORE]
   - Data types: [e.g., "Browsing habits, location, contacts"]

☐ **Child Sexual Abuse Material (CSAM)**
   - Risk Level: [SEVERITY SCORE]
   - See Component 4 (Illegal Content) for full analysis

### Platform Design Contribution Analysis

**How does [SERVICE NAME] impact minors?**

**Age Verification:**
[EXPLAIN CURRENT AGE GATE MECHANISMS]

**Example:**
"Users self-report age during signup. No verification required. [PERCENTAGE]% of accounts claim to be under 18. Estimated underreporting: [PERCENTAGE]% (based on [METHOD])."

**Content Recommendation:**
[EXPLAIN WHAT MINORS SEE]

**Example:**
"Minors receive age-appropriate recommendations [YES/NO]. If yes, method: [DESCRIPTION]. Effectiveness: [METRIC - e.g., "[X]% of content shown to minors is age-appropriate per third-party audit"]."

**Addictive Features:**
[LIST ENGAGEMENT-MAXIMIZING FEATURES]

**Example:**
"Platform includes [FEATURES - e.g., 'autoplay, infinite scroll, push notifications, likes, streaks']. Average session time for minors: [DURATION]. [PERCENTAGE]% of teen users report difficulty limiting usage."

**Advertising:**
[EXPLAIN AD TARGETING FOR MINORS]

**Example:**
"Targeted advertising to users under 18: [PROHIBITED / ALLOWED WITH RESTRICTIONS]. Restrictions: [LIST - e.g., 'No profiling, limited categories only']."

### Risk Severity Assessment

**Risk: [MINOR PROTECTION RISK TYPE]**

- **Likelihood:** [SCORE 1-5] - [JUSTIFICATION]
- **Impact:** [SCORE 1-5] - [JUSTIFICATION]
- **Severity:** [SCORE 1-25] - [CRITICAL / HIGH / MEDIUM / LOW]

**Example - Addictive Design:**
- **Likelihood:** 5 (Very High) - "All minors on platform exposed to engagement features"
- **Impact:** 3 (Moderate) - "Can contribute to excessive use, mental health impacts"
- **Severity:** 15 (HIGH) - "DSA Article 38 + regulatory scrutiny = high priority"

### Current Mitigation Measures

**Age Verification & Parental Controls:**
☐ Age verification (method: [DESCRIPTION])
☐ Parental consent (for users under [AGE])
☐ Parental controls (parent dashboard, usage limits, content filters)

**Content Restrictions:**
☐ Age gates (adult content hidden from minors)
☐ Minor accounts (different experience than adults)
☐ Default privacy (minor accounts private by default)

**Addictive Design Mitigation:**
☐ Usage time tools (screen time reminders, take-a-break prompts)
☐ Quiet mode (disable notifications during [HOURS])
☐ Disableable features (can turn off autoplay, infinite scroll)

**Advertising Restrictions:**
☐ No targeted ads to minors (based on [AGE / VERIFIED AGE])
☐ Limited ad categories (no alcohol, gambling, appearance products)
☐ Ad transparency (minors see why they see ads)

**Safety Features:**
☐ Restricted contact (adults cannot message minors unless connected)
☐ Comment filtering (hide potentially harmful comments)
☐ Reporting tools (easy reporting for parents and minors)

### Effectiveness Measurement

**Key Performance Indicators:**

1. **Age Verification Accuracy:** [PERCENTAGE]% of accounts have verified ages
2. **Minor Exposure to Adult Content:** [PERCENTAGE]% (should be near 0%)
3. **Parental Control Adoption:** [PERCENTAGE]% of minor accounts have parental oversight
4. **Usage Time:** [TREND - increasing/decreasing] for minors
5. **Safety Reports:** [NUMBER] CSAM/grooming/bullying reports per month

### Remaining Gaps & Planned Improvements

**Identified Gaps:**
1. [GAP]
2. [GAP]

**Improvement Roadmap:**
| Improvement | Timeline | Investment | Owner |
|-------------|----------|------------|-------|
| [INITIATIVE] | [DATE] | [€ AMOUNT] | [TEAM] |

---

## COMPONENT 9: Risk Mitigation Roadmap (Article 35)

### Mitigation Strategy Overview

**Total Investment:** €[AMOUNT] over [TIMEFRAME]

**Prioritization:** Risks addressed in order of severity score (Critical > High > Medium > Low)

**Governance:** [DESCRIPTION - e.g., "Risk Steering Committee meets quarterly to review progress"]

### Mitigation Projects

**Critical Priority (Severity 20-25):**

| Risk | Mitigation Project | Timeline | Budget | Owner | KPIs |
|------|-------------------|----------|--------|-------|------|
| [RISK] | [PROJECT] | [START-END] | €[AMOUNT] | [TEAM] | [METRICS] |
| [RISK] | [PROJECT] | [START-END] | €[AMOUNT] | [TEAM] | [METRICS] |

**High Priority (Severity 12-19):**

| Risk | Mitigation Project | Timeline | Budget | Owner | KPIs |
|------|-------------------|----------|--------|-------|------|
| [RISK] | [PROJECT] | [START-END] | €[AMOUNT] | [TEAM] | [METRICS] |
| [RISK] | [PROJECT] | [START-END] | €[AMOUNT] | [TEAM] | [METRICS] |

**Medium Priority (Severity 6-11):**

| Risk | Mitigation Project | Timeline | Budget | Owner | KPIs |
|------|-------------------|----------|--------|-------|------|
| [RISK] | [PROJECT] | [START-END] | €[AMOUNT] | [TEAM] | [METRICS] |

### Continuous Monitoring

**Ongoing Risk Monitoring:**
- **Frequency:** [DAILY / WEEKLY / MONTHLY] automated reports
- **Escalation:** [CRITERIA for escalating new risks to leadership]
- **Reporting:** [CADENCE - e.g., "Monthly to VP, Quarterly to CEO/Board"]

**Emerging Risk Detection:**
- **Incident Analysis:** All Trust & Safety incidents reviewed for new risks
- **External Monitoring:** Track regulatory actions against other platforms
- **Research Partnerships:** Collaborate with [UNIVERSITIES / NGOS] on emerging threats

**Assessment Updates:**
- **Annual Update:** Full re-assessment by [DEADLINE each year]
- **Triggered Updates:** Re-assess if [CRITERIA - e.g., "new features launched, major incident, regulatory guidance"]

---

## COMPONENT 10: Independent Audit (Article 37)

**DSA Article 37 Requirement:** VLOPs/VLOSEs must undergo annual independent audits

**Audit Firm:** [FIRM NAME - must be certified by DSA Coordinator]

**Audit Period:** [START DATE] to [END DATE]

**Audit Scope:**
- ☐ Risk assessment methodology review
- ☐ Mitigation measure effectiveness validation
- ☐ Compliance with DSA Articles 34-35
- ☐ Data accuracy verification
- ☐ Process audit (do we follow our stated procedures?)

**Audit Report:**
- **Report Date:** [DATE]
- **Reference:** [REPORT ID]
- **Public Summary:** [URL if published]
- **Key Findings:** [SUMMARY]
- **Recommendations:** [NUMBER] recommendations for improvement
- **Action Plan:** [SUMMARY of planned responses]

**Next Audit:** [DATE - must be within 12 months]

---

## Template Notes for Compliance Teams

### DSA Article 34 Requirements Met

This template ensures compliance with all DSA Article 34 requirements:

1. ✅ **All 5 Risk Categories Assessed** (Components 4-8)
2. ✅ **Platform Design Analysis** (in each risk category section)
3. ✅ **Severity Methodology** (Component 3 - documented and applied)
4. ✅ **Service-Specific Risks** (customized to platform features)
5. ✅ **Annual Update** (documented in metadata, Component 1)

### DSA Article 35 Requirements Met

This template ensures compliance with all DSA Article 35 requirements:

1. ✅ **Mitigation Measures** (defined for each risk)
2. ✅ **Proportionate & Effective** (prioritized by severity, resourced appropriately)
3. ✅ **Effectiveness Measurement** (KPIs for each risk category)
4. ✅ **Mitigation Roadmap** (Component 9)

### Customization Guidelines

**For Different Service Types:**

- **Social Media Platforms:** Focus on viral spread, recommender risks, coordinated behavior
- **Video Platforms:** Emphasize copyright, child safety, addictive design
- **Marketplaces:** Highlight illegal goods, fraud, consumer protection
- **App Stores:** Emphasize malicious apps, child safety, deceptive practices
- **Search Engines (VLOSE):** Focus on disinformation ranking, electoral integrity, illegal content surfacing

**Service-Specific Risks to Add:**

Beyond the 5 mandatory categories, consider:
- **Marketplace Fraud:** Fake sellers, counterfeit goods
- **Malicious Apps:** Malware, spyware, scamware (app stores)
- **Intellectual Property:** Copyright, trademark infringement (content platforms)
- **Gambling Addiction:** Loot boxes, in-app purchases (gaming)
- **Financial Scams:** Phishing, investment fraud (platforms with payments)

### Quality Assurance Checklist

Before finalizing risk assessment:

- [ ] All [bracketed] fields filled in with service-specific data
- [ ] All 5 mandatory risk categories completed
- [ ] Platform design contribution analysis is SPECIFIC (not generic)
- [ ] Severity scores calculated using documented methodology
- [ ] Mitigation measures are CONCRETE (not vague commitments)
- [ ] KPIs are MEASURABLE (specific metrics with targets)
- [ ] Legal review completed
- [ ] Executive sponsor approved
- [ ] Independent audit scheduled/completed (Article 37)
- [ ] Submitted to EC via DSA transparency database

### Common Mistakes to Avoid

❌ **Don't:** Use generic descriptions like "we take risks seriously"
✅ **Do:** Provide specific data, metrics, and examples

❌ **Don't:** Copy risk descriptions from other platforms
✅ **Do:** Analyze YOUR platform's unique design and risks

❌ **Don't:** Say "we will improve" without specifics
✅ **Do:** Provide concrete projects, timelines, budgets, KPIs

❌ **Don't:** Ignore platform design contribution
✅ **Do:** Honestly assess how YOUR features amplify risks (DSA enforcement focuses on this)

❌ **Don't:** Rate all risks as "low"
✅ **Do:** Use honest severity ratings; regulators expect to see critical/high risks

---

## EUR-Lex References

**Primary Regulation:**
- **EU Digital Services Act** (Regulation 2022/2065)
- **Full Regulation:** https://eur-lex.europa.eu/eli/reg/2022/2065

**DSA Article 34 - Risk Assessment:**
- **Article 34 Text:** https://eur-lex.europa.eu/eli/reg/2022/2065/oj#d1e4526-1-1
- **Article 34(1):** Obligation to assess systemic risks in five mandatory categories
- **Article 34(2):** Assessment must consider design, functioning, and use of service
- **Article 34(3):** Size and characteristics of service users
- **Article 34(4):** Annual assessment requirement

**DSA Article 35 - Risk Mitigation:**
- **Article 35 Text:** https://eur-lex.europa.eu/eli/reg/2022/2065/oj#d1e4581-1-1
- **Article 35(1):** Reasonable, proportionate, and effective mitigation measures
- **Article 35(2):** Reporting obligations to European Commission and Digital Services Coordinator

**DSA Article 37 - Independent Audit:**
- **Article 37 Text:** https://eur-lex.europa.eu/eli/reg/2022/2065/oj#d1e4641-1-1
- **Article 37(1):** Annual independent audit of DSA compliance obligations
- **Article 37(4):** Audit report submission to Commission and Coordinator

**Related DSA Articles:**
- **Article 15:** Transparency reporting - https://eur-lex.europa.eu/eli/reg/2022/2065/oj#d1e2953-1-1
- **Article 38:** Protection of minors (mandatory risk category) - https://eur-lex.europa.eu/eli/reg/2022/2065/oj#d1e4695-1-1

**Supporting EU Regulations:**
- **Delegated Regulation (EU) 2024/436:** Independent audit standards
- **EU Charter of Fundamental Rights:** https://eur-lex.europa.eu/eli/treaty/char_2012/oj

---

**Template Version:** 1.0
**Created:** 2025-12-02
**Status:** Production-ready
**Maintained By:** DSA Compliance Team
**Next Review:** Upon DSA guidance updates or significant platform changes
