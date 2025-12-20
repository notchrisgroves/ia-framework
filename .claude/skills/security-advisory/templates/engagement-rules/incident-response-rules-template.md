---
type: template
name: incident-response-rules-template
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Incident Response Template

## Incident Classification
- **Incident ID:** [IR-YYYY-XXXX]
- **Severity Level:** [Critical/High/Medium/Low]
- **Incident Type:** [Data Breach/System Outage/Security Event/Compliance Violation]
- **Date/Time Detected:** [ISO 8601 format]
- **Detection Method:** [Automated/Manual/Third-party]

## Initial Assessment
### Incident Summary
[Brief description of the incident, what happened, and initial impact assessment]

### Affected Systems/Data
- **Systems:** [List of affected systems, applications, or infrastructure]
- **Data Types:** [PII, PHI, Financial, Intellectual Property, etc.]
- **Records Potentially Affected:** [Number/scope]
- **Geographic Scope:** [Locations affected]

## Timeline of Events
| Date/Time | Event Description | Source | Action Taken |
|-----------|------------------|--------|--------------|
| [Timestamp] | [Event] | [System/Person] | [Response] |

## Response Team
- **Incident Commander:** [Name, Contact]
- **IT Security Lead:** [Name, Contact]
- **Legal Counsel:** [Name, Contact]
- **Communications Lead:** [Name, Contact]
- **Business Continuity Lead:** [Name, Contact]

## Containment Actions
### Immediate Containment (0-1 hour)
- [ ] Isolate affected systems
- [ ] Preserve evidence
- [ ] Document initial findings
- [ ] Notify incident response team

### Short-term Containment (1-24 hours)
- [ ] Implement temporary controls
- [ ] Assess scope of compromise
- [ ] Begin forensic analysis
- [ ] Prepare stakeholder communications

## Investigation Findings
### Root Cause Analysis
[Detailed analysis of how the incident occurred and contributing factors]

### Evidence Collected
- [List of logs, files, and other evidence preserved]
- [Chain of custody documentation]
- [Forensic analysis results]

### Attack Vector/Vulnerability
[Description of how the incident occurred and what vulnerabilities were exploited]

## Impact Assessment
### Business Impact
- **Financial Impact:** [Estimated costs, lost revenue]
- **Operational Impact:** [Service disruptions, productivity loss]
- **Reputational Impact:** [Customer/partner concerns, media attention]

### Compliance Impact
- **Regulatory Requirements:** [GDPR, HIPAA, PCI DSS notification requirements]
- **Notification Deadlines:** [Legal obligations and timelines]
- **Potential Penalties:** [Regulatory fines or sanctions]

## Recovery Actions
### System Recovery
- [ ] Remove threats/malware
- [ ] Patch vulnerabilities
- [ ] Restore from clean backups
- [ ] Implement additional monitoring

### Business Recovery
- [ ] Resume normal operations
- [ ] Customer/partner communications
- [ ] Service restoration validation
- [ ] Performance monitoring

## External Notifications
### Regulatory Notifications
- **Data Protection Authority:** [Required: Yes/No, Date Submitted]
- **Industry Regulators:** [Required: Yes/No, Date Submitted]
- **Law Enforcement:** [Required: Yes/No, Date Submitted]

### Customer/Partner Notifications
- **Customer Notification:** [Required: Yes/No, Method, Date]
- **Partner Notification:** [Required: Yes/No, Method, Date]
- **Media Statement:** [Required: Yes/No, Date]

## Lessons Learned
### What Went Well
- [List effective response actions and controls]

### What Could Be Improved
- [List areas for improvement in detection, response, or recovery]

### Action Items
| Action Item | Owner | Due Date | Status |
|-------------|-------|----------|---------|
| [Action] | [Person] | [Date] | [Open/Complete] |

## Post-Incident Activities
- [ ] Update incident response procedures
- [ ] Implement security improvements
- [ ] Conduct tabletop exercises
- [ ] Review and update risk assessments
- [ ] Archive incident documentation

## Incident Closure
- **Incident Closed By:** [Name, Title]
- **Closure Date:** [Date]
- **Final Status:** [Resolved/Contained/Ongoing]