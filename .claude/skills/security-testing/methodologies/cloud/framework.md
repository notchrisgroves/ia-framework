
## Methodology Overview

Cloud security testing identifies misconfigurations, vulnerabilities, and policy violations in cloud infrastructure through automated scanning, manual security reviews, and compliance validation across AWS, Azure, GCP, and multi-cloud environments.

---

## Cloud Security Framework Integration

### AWS Security Hub Standards

**Reference:** AWS Security Hub documentation (use WebFetch)
**Coverage:** 7 compliance frameworks integrated into Security Hub

**Compliance Standards:**
1. **AWS Foundational Security Best Practices** - AWS-specific security baseline
2. **CIS AWS Foundations Benchmark** - Industry consensus security configuration
3. **PCI DSS v3.2.1** - Payment card industry requirements
4. **NIST 800-53 Rev. 5** - Federal security controls
5. **NIST Cybersecurity Framework (CSF)** - Risk management framework
6. **ISO/IEC 27001:2013** - Information security management
7. **SOC 2** - Service organization controls

**Key Focus Areas:**
- IAM (Identity and Access Management)
- S3 bucket security and public access
- EC2 instance hardening
- RDS database encryption
- Lambda function security
- VPC network segmentation
- CloudTrail logging and monitoring

---

### Azure Security (Microsoft Cloud Security Benchmark)

**Reference:** Microsoft Cloud Security Benchmark documentation (use WebFetch)
**Coverage:** Microsoft Cloud Security Benchmark (MCSB v2)

**Security Domains:**
1. **Network Security**
   - Virtual Network isolation
   - Network Security Groups (NSGs)
   - Azure Firewall configuration
   - Private endpoints and service endpoints

2. **Identity Management**
   - Azure AD security
   - Conditional Access policies
   - Privileged Identity Management (PIM)
   - Multi-factor authentication enforcement

3. **Privileged Access**
   - Role-Based Access Control (RBAC)
   - Just-In-Time (JIT) access
   - Azure Bastion for secure RDP/SSH
   - Service principals and managed identities

4. **Data Protection**
   - Azure Key Vault for secrets
   - Storage encryption at rest
   - TDE for SQL databases
   - Azure Information Protection

5. **Asset Management**
   - Resource tagging
   - Azure Policy compliance
   - Inventory management
   - Deprecated resource detection

6. **Logging and Threat Detection**
   - Azure Monitor integration
   - Microsoft Defender for Cloud
   - Azure Sentinel (SIEM)
   - Security alerts and incidents

7. **Posture and Vulnerability Management**
   - Secure Score monitoring
   - Vulnerability assessments
   - Compliance dashboards
   - Remediation workflows

8. **Endpoint Security**
   - VM security baselines
   - Microsoft Defender for Endpoint
   - Update management
   - Disk encryption

9. **Backup and Recovery**
   - Azure Backup configuration
   - Geo-redundant backups
   - Recovery testing
   - Backup retention policies

10. **DevOps Security**
    - Secure CI/CD pipelines
    - Container security (AKS)
    - GitHub Advanced Security
    - Infrastructure as Code scanning

---

### GCP Security Best Practices

**Reference:** GCP Security Best Practices documentation (use WebFetch)

**Key Focus Areas:**
- IAM and service accounts
- VPC firewall rules
- Cloud Storage (GCS) bucket permissions
- Compute Engine instance security
- Cloud SQL encryption
- Cloud KMS key management
- Stackdriver logging and monitoring

---

### Multi-Cloud Security Best Practices

**Reference:** Cloud Security Alliance (CSA) guidance (use WebFetch)
**Coverage:** 30+ vendor-neutral cloud security practices

**Universal Principles:**
1. **Shared Responsibility Model**
   - Provider responsibilities (physical security, hypervisor, network)
   - Customer responsibilities (data, identity, applications, network controls)
   - Clarity on boundaries

2. **Identity and Access Management**
   - Principle of least privilege
   - Regular access reviews
   - MFA enforcement
   - Service account management

3. **Data Protection**
   - Encryption at rest and in transit
   - Key management (customer-managed keys)
   - Data classification
   - Backup and recovery

4. **Network Security**
   - Network segmentation
   - Security groups and NACLs
   - Private connectivity (VPN, Direct Connect, ExpressRoute)
   - DDoS protection

5. **Monitoring and Logging**
   - Centralized logging (CloudTrail, Azure Monitor, Stackdriver)
   - Real-time alerting
   - Security Information and Event Management (SIEM)
   - Audit trail retention

6. **Compliance and Governance**
   - Policy-as-Code (Azure Policy, AWS Config, GCP Organization Policy)
   - Compliance frameworks (CIS, NIST, PCI DSS, HIPAA)
   - Automated compliance checks
   - Remediation workflows

7. **DevSecOps**
   - Shift-left security (scan IaC early)
   - Container security scanning
   - Secrets management (not hardcoded)
   - Secure CI/CD pipelines

---

## Testing Methodology Structure

### EXPLORE Phase

1. **Scope Review**
   - Read SCOPE.md for cloud environment details
   - Identify cloud providers (AWS, Azure, GCP, multi-cloud)
   - Understand account structure and subscriptions
   - Note compliance requirements (PCI DSS, HIPAA, SOC 2)
   - Identify workload types (compute, storage, databases, containers)

2. **Cloud Environment Reconnaissance**
   - Enumerate accounts/subscriptions/projects
   - Identify regions and availability zones
   - Map resource inventory (VMs, storage, databases, functions)
   - Review IAM structure (users, roles, service accounts)
   - Identify security tooling (Security Hub, Defender, Security Command Center)

3. **Framework Mapping**
   - Map cloud resources to compliance standards
   - Identify high-risk areas (public S3 buckets, overly permissive IAM)
   - Review security baselines (CIS Benchmarks)
   - Prioritize based on data sensitivity and exposure

4. **Threat Modeling**
   - Identify attack surface (internet-facing resources)
   - Review IAM privilege escalation paths
   - Analyze network segmentation
   - Evaluate data exposure risks

### PLAN Phase

1. **Vulnerability Prioritization**
   - **Critical:** Public storage buckets, overly permissive IAM, unencrypted data
   - **High:** Missing MFA, exposed credentials, network misconfigurations
   - **Medium:** Missing logs, outdated resources, policy violations
   - **Low:** Best practice deviations, optimization opportunities

2. **Tool Inventory Check** (CRITICAL)
   - Review `/servers` for cloud security tools
   - Check for: ScoutSuite, Prowler, Pacu, CloudSploit, CloudMapper, Steampipe
   - Identify missing tools
   - Request deployment if needed
   - Verify cloud API credentials and permissions

3. **Test Plan Generation**
   - Map compliance standards to specific tests
   - Document testing approach per cloud provider:
     - Automated scanning (ScoutSuite, Prowler)
     - Manual configuration review
     - IAM privilege escalation testing
     - Network segmentation validation
     - Data exposure testing
   - Plan for multi-cloud scenarios (cross-account, hybrid)
   - Get user approval before testing

### CODE Phase (Testing)

**Automated Cloud Security Scanning:**

1. **AWS Testing (ScoutSuite/Prowler)**
   - IAM security (excessive permissions, no MFA)
   - S3 bucket misconfigurations (public access, encryption)
   - EC2 security groups (overly permissive rules)
   - RDS encryption and snapshots
   - CloudTrail logging enabled
   - VPC security (flow logs, NACLs)
   - Lambda function security (environment variables, execution roles)

2. **Azure Testing (ScoutSuite/AzureHound)**
   - Azure AD security (users without MFA, guest accounts)
   - Storage account public access
   - NSG rules and network segmentation
   - Key Vault access policies
   - SQL Database encryption (TDE)
   - Azure Monitor and Defender configuration
   - RBAC role assignments

3. **GCP Testing (ScoutSuite)**
   - GCS bucket permissions
   - Compute Engine firewall rules
   - IAM bindings and service accounts
   - Cloud SQL encryption
   - VPC firewall rules
   - Stackdriver logging
   - Cloud KMS key management

**Manual Security Review:**

1. **IAM Security**
   - Review overly permissive policies
   - Test for privilege escalation paths
   - Validate MFA enforcement
   - Check service account key rotation
   - Analyze cross-account access

2. **Data Security**
   - Test for public data exposure
   - Validate encryption at rest and in transit
   - Review key management (customer-managed vs provider-managed)
   - Check backup encryption and retention
   - Test data exfiltration paths

3. **Network Security**
   - Validate network segmentation (public, private, isolated)
   - Test security group rules (overly permissive ingress)
   - Review VPN and peering configurations
   - Check for exposed management ports (SSH, RDP)
   - Validate egress controls

4. **Compliance Testing**
   - Run compliance scans (CIS Benchmarks)
   - Validate policy enforcement (Azure Policy, AWS Config)
   - Check logging and monitoring requirements
   - Review audit trail retention
   - Test incident response procedures

5. **Serverless Security**
   - **AWS Lambda:** Function permissions, environment variables, VPC configuration
   - **Azure Functions:** Managed identities, Key Vault integration
   - **GCP Cloud Functions:** Service account permissions, secrets management
   - Test for function vulnerabilities (injection, SSRF)

6. **Container Security**
   - **AWS ECS/EKS:** Task role permissions, secrets management
   - **Azure AKS:** Pod security policies, network policies
   - **GCP GKE:** Workload identity, binary authorization
   - Scan container images for vulnerabilities

**Evidence Collection:**
- Screenshots of misconfigurations
- Scan reports (ScoutSuite HTML, Prowler CSV)
- IAM policy documents demonstrating excessive permissions
- Network diagrams showing segmentation issues
- Map findings to compliance frameworks (CIS, NIST, PCI DSS)

### COMMIT Phase (Reporting)

1. **Findings Documentation**
   - Executive summary (business impact, compliance risks)
   - Technical findings mapped to compliance standards
   - Severity ratings (Critical, High, Medium, Low)
   - Evidence (scan reports, screenshots, policy examples)
   - Risk scoring (likelihood + impact)

2. **Remediation Recommendations**
   - **IAM:**
     - Principle of least privilege (remove excessive permissions)
     - Enforce MFA for all users
     - Rotate service account keys
     - Implement JIT access

   - **Data Protection:**
     - Enable encryption at rest (S3, RDS, Azure Storage)
     - Use customer-managed keys (CMK)
     - Restrict public access (S3 Block Public Access, Azure Storage firewalls)
     - Enable versioning and soft delete

   - **Network Security:**
     - Restrict security groups (remove 0.0.0.0/0 rules)
     - Enable VPC Flow Logs / NSG Flow Logs
     - Implement network segmentation
     - Use private endpoints

   - **Logging and Monitoring:**
     - Enable CloudTrail / Azure Monitor / Stackdriver
     - Configure SIEM integration
     - Set up security alerts
     - Retain logs per compliance requirements

   - **Policy Enforcement:**
     - Implement guardrails (AWS Config Rules, Azure Policy, GCP Organization Policy)
     - Automate remediation (Lambda/Functions for auto-fix)
     - Regular compliance scans

3. **Compliance Integration**
   - Map findings to CIS Benchmarks
   - Reference AWS Security Hub / Azure Secure Score
   - Include NIST, PCI DSS, HIPAA mappings where applicable
   - Provide compliance dashboard recommendations

---

## Common Cloud Vulnerabilities

### IAM and Access Control
- **Overly Permissive Policies:** AdministratorAccess, wildcards (*), full resource access
- **Missing MFA:** Root account / privileged users without MFA
- **Long-Lived Credentials:** Access keys not rotated
- **Public Access Keys:** Keys committed to GitHub
- **Cross-Account Access Issues:** Overly permissive trust relationships

### Data Exposure
- **Public S3 Buckets:** Buckets with public read/write access
- **Unencrypted Storage:** S3, EBS, Azure Storage, Cloud Storage without encryption
- **Public Snapshots:** RDS/EBS snapshots publicly accessible
- **Secrets in Environment Variables:** Lambda/Functions with hardcoded secrets
- **Unencrypted Backups:** Database backups without encryption

### Network Misconfigurations
- **Overly Permissive Security Groups:** 0.0.0.0/0 ingress on SSH/RDP
- **Missing Network Segmentation:** All resources in one subnet
- **Exposed Management Ports:** SSH (22), RDP (3389) open to internet
- **No VPC Flow Logs:** Missing network traffic visibility
- **Public Database Endpoints:** RDS/SQL databases internet-accessible

### Logging and Monitoring
- **CloudTrail Disabled:** No audit trail for API calls
- **Missing Log Encryption:** Logs stored without encryption
- **Insufficient Retention:** Logs deleted before compliance requirements
- **No Alerting:** Critical events not monitored
- **SIEM Not Integrated:** Logs not centralized

### Compliance Violations
- **Missing Guardrails:** No AWS Config / Azure Policy enforcement
- **Policy Drift:** Resources created outside of policy
- **Outdated Baselines:** Not following current CIS Benchmarks
- **Untagged Resources:** Missing required tags for compliance tracking

---

## Testing Tools

**Multi-Cloud:**
- **ScoutSuite** - Multi-cloud security auditing (AWS, Azure, GCP)
- **Steampipe** - SQL-based cloud security queries
- **CloudSploit** - Cloud security scanner
- **CloudMapper** - Cloud environment visualization

**AWS-Specific:**
- **Prowler** - AWS security assessment tool (CIS Benchmark)
- **Pacu** - AWS exploitation framework
- **AWS Security Hub** - Native compliance scanning
- **CloudTrail Analyzer** - Audit log analysis
- **IAM Policy Simulator** - Test IAM permissions

**Azure-Specific:**
- **AzureHound** - Azure AD enumeration
- **MicroBurst** - Azure security assessment
- **Microsoft Defender for Cloud** - Native security posture
- **Azure Policy** - Compliance and governance

**GCP-Specific:**
- **Forseti Security** - GCP security scanner
- **GCP Security Command Center** - Native security management
- **gcloud CLI** - Manual security audits

**General:**
- **Terraform Compliance** - IaC security testing
- **Checkov** - IaC static analysis (Terraform, CloudFormation)
- **Trivy** - Container image scanning
- **KICS** - Infrastructure as Code security scanning

---

## Reference Resources

### Local Resources (Dynamic Discovery)

**Compliance Frameworks:** `Glob: resources/library/frameworks/**/*`
- PCI-DSS: `**/*pci*`
- NIST SP 800: `**/*nist*` or `**/*800*`
- HIPAA: `**/*hipaa*`

**CIS Benchmarks:** `Glob: resources/library/benchmarks/**/*cis*`

### Web Resources (Cloud-Specific)

**AWS:**
- Security Hub: https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference.html
- CIS AWS Foundations: https://www.cisecurity.org/benchmark/amazon_web_services

**Azure:**
- MCSB: https://learn.microsoft.com/en-us/security/benchmark/azure/
- Best Practices: https://learn.microsoft.com/en-us/azure/security/fundamentals/best-practices-and-patterns

**GCP:**
- Security Best Practices: https://cloud.google.com/security/best-practices
- CIS GCP Foundations: https://www.cisecurity.org/benchmark/google_cloud_computing_platform

**Note:** Cloud provider-specific standards (AWS/Azure/GCP) use WebFetch. General compliance frameworks available locally.

---

**Created:** 2025-12-01
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Version:** 1.0
