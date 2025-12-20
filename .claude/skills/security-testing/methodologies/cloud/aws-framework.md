
## Methodology Overview

AWS security testing identifies misconfigurations, excessive permissions, data exposure risks, and privilege escalation paths in Amazon Web Services environments using automated scanning (prowler), manual enumeration (aws-cli), and compliance frameworks (CIS, NIST).

---

## CIS AWS Foundations Benchmark Integration

**Benchmark Version:** CIS AWS Foundations Benchmark v3.0.0
**Coverage:** 60+ controls across 5 sections
**Tool:** prowler (automated CIS compliance scanning)

### CIS Control Categories

1. **Identity and Access Management** (IAM)
2. **Storage** (S3)
3. **Logging** (CloudTrail, VPC Flow Logs, Config)
4. **Monitoring** (CloudWatch, GuardDuty)
5. **Networking** (VPC, Security Groups, NACLs)

**See:** AWS Security Hub documentation for complete control mappings (use WebFetch)

---

## AWS Well-Architected Framework: Security Pillar

**7 Design Principles:**

1. **Implement a strong identity foundation** - Centralize privilege management, eliminate long-term credentials
2. **Enable traceability** - Monitor, alert, audit actions in real-time
3. **Apply security at all layers** - Defense in depth (edge, VPC, subnet, load balancer, instance, OS, application)
4. **Automate security best practices** - Automated detection and remediation
5. **Protect data in transit and at rest** - Encryption, tokenization, access controls
6. **Keep people away from data** - Mechanisms and tools reduce manual access
7. **Prepare for security events** - Incident response planning, automated remediation

---

## Testing Methodology Structure

### EXPLORE Phase

**1. Scope Review**
   - Read SCOPE.md for target AWS accounts and regions
   - Identify services in scope (IAM, EC2, S3, RDS, Lambda, etc.)
   - Understand authorization level (read-only, admin, specific roles)
   - Note compliance requirements (CIS, NIST, PCI-DSS)
   - Identify sensitive data locations

**2. Account Reconnaissance**
   - Enumerate AWS accounts and organization structure
   - List regions with active resources
   - Identify IAM users, roles, groups, policies
   - Map service inventory per region
   - Identify public-facing resources

**3. Permission Mapping**
   - Review IAM policies attached to roles/users
   - Identify overly permissive policies (AdministratorAccess, wildcards)
   - Map trust relationships and AssumeRole chains
   - Check for cross-account access
   - Identify service-linked roles

**4. Threat Modeling**
   - Identify high-value targets (databases, S3 buckets, secrets)
   - Map privilege escalation paths
   - Analyze data exfiltration scenarios
   - Document trust boundaries
   - Prioritize attack vectors

---

### PLAN Phase

**1. Vulnerability Prioritization**
   - **Critical:** Public S3 buckets with sensitive data, root account without MFA, AdministratorAccess to users
   - **High:** Overly permissive Security Groups (0.0.0.0/0), unencrypted RDS, missing CloudTrail
   - **Medium:** Unused IAM keys, missing VPC flow logs, unencrypted EBS volumes
   - **Low:** Missing resource tags, outdated IAM password policy

**2. Tool Inventory Check** (CRITICAL)
   - Review `/servers` for cloud security tools
   - Check for: prowler, scoutsuite, pacu, aws-cli
   - Verify AWS credentials configured (AWS_PROFILE or environment variables)
   - Test API access with `aws sts get-caller-identity`
   - Request deployment if tools missing

**3. Test Plan Generation**
   - Map CIS controls to specific tests
   - Document testing approach:
     - Automated scanning (prowler CIS checks)
     - Manual enumeration (aws-cli queries)
     - Privilege escalation testing
     - Data exfiltration simulation
     - Network penetration testing
   - Plan for both read-only and exploit scenarios
   - Get user approval before testing

---

### CODE Phase (Testing)

**Automated Scanning:**

**1. CIS Benchmark Compliance (prowler)**
   ```bash
   # Run full CIS benchmark scan
   prowler aws --compliance cis_aws_1.5 --output-formats json,html

   # Scan specific services
   prowler aws --services iam,s3,ec2,rds --output-formats json

   # Check specific CIS controls
   prowler aws --checks iam_root_mfa_enabled,s3_bucket_public_access
   ```

**2. Service-Specific Scans**
   - IAM: Policy analysis, privilege escalation paths
   - S3: Public bucket detection, ACL review, encryption status
   - EC2: Security group analysis, instance metadata exposure
   - RDS: Encryption status, public accessibility, backup retention
   - Lambda: Environment variable secrets, execution role permissions
   - CloudTrail: Logging enabled, log file validation, KMS encryption

**Manual Enumeration:**

**3. IAM Security Testing**
   ```bash
   # List users without MFA
   aws iam list-users --query 'Users[*].[UserName]' --output table
   aws iam list-mfa-devices --user-name <username>

   # Find overly permissive policies
   aws iam list-policies --scope Local --query 'Policies[?PolicyName==`AdministratorAccess`]'

   # Check for unused access keys
   aws iam get-credential-report

   # Enumerate roles with AssumeRole permissions
   aws iam list-roles --query 'Roles[*].[RoleName,AssumeRolePolicyDocument]'
   ```

**4. S3 Security Testing**
   ```bash
   # List all buckets
   aws s3 ls

   # Check bucket ACLs for public access
   aws s3api get-bucket-acl --bucket <bucket-name>

   # Check bucket policies
   aws s3api get-bucket-policy --bucket <bucket-name>

   # Check encryption status
   aws s3api get-bucket-encryption --bucket <bucket-name>

   # Test public read access
   curl -I https://<bucket-name>.s3.amazonaws.com/<object-key>
   ```

**5. EC2 Security Testing**
   ```bash
   # List instances with public IPs
   aws ec2 describe-instances --query 'Reservations[*].Instances[?PublicIpAddress!=`null`].[InstanceId,PublicIpAddress]'

   # Review Security Groups for 0.0.0.0/0 rules
   aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'

   # Check for unencrypted EBS volumes
   aws ec2 describe-volumes --query 'Volumes[?Encrypted==`false`].[VolumeId,Size]'

   # Test instance metadata access (from EC2 instance)
   curl http://169.254.169.254/latest/meta-data/
   curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
   ```

**6. RDS Security Testing**
   ```bash
   # Find publicly accessible databases
   aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].[DBInstanceIdentifier,Endpoint.Address]'

   # Check encryption status
   aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,StorageEncrypted]'

   # Review security groups
   aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,VpcSecurityGroups]'
   ```

**7. Secrets & Credentials Testing**
   ```bash
   # Check Lambda environment variables for secrets
   aws lambda list-functions --query 'Functions[*].[FunctionName]' | while read func; do
       aws lambda get-function-configuration --function-name $func --query 'Environment.Variables'
   done

   # Review Secrets Manager secrets
   aws secretsmanager list-secrets

   # Check for hardcoded credentials in CloudFormation templates
   aws cloudformation list-stacks --query 'StackSummaries[?StackStatus!=`DELETE_COMPLETE`].[StackName]'
   ```

**Privilege Escalation Testing:**

**8. IAM Privilege Escalation Paths**
   - Test `iam:PassRole` + service creation combinations
   - Attempt `iam:CreateAccessKey` on other users
   - Test `iam:AttachUserPolicy` or `iam:PutUserPolicy`
   - Exploit `iam:UpdateAssumeRolePolicy` for role hijacking
   - Test Lambda function manipulation for privilege escalation

**9. Cross-Account Access Testing**
   - Test AssumeRole chains across accounts
   - Attempt unauthorized cross-account S3 access
   - Test cross-account SNS/SQS subscriptions

**Network Testing:**

**10. VPC Security Testing**
   ```bash
   # Review VPC Flow Logs status
   aws ec2 describe-flow-logs

   # Check for default VPCs in use
   aws ec2 describe-vpcs --query 'Vpcs[?IsDefault==`true`]'

   # Review NACLs for overly permissive rules
   aws ec2 describe-network-acls
   ```

**Evidence Collection:**
- Screenshot of prowler scan results
- AWS CLI command outputs demonstrating misconfigurations
- Proof of privilege escalation (before/after screenshots)
- Evidence of data access (S3 object retrieval)
- Map findings to CIS control IDs

---

### COMMIT Phase (Reporting)

**1. Findings Documentation**
   - Executive summary (business impact focus)
   - Technical findings mapped to CIS AWS Foundations Benchmark
   - Severity ratings (Critical, High, Medium, Low)
   - Successful exploit demonstrations
   - Impact analysis (data exposure, privilege escalation, compliance)

**2. Remediation Recommendations**

   **IAM Hardening:**
   - Enable MFA on all accounts, especially root
   - Implement least privilege IAM policies
   - Rotate access keys every 90 days
   - Remove unused IAM users and roles
   - Enable IAM Access Analyzer

   **S3 Security:**
   - Block public access at account level
   - Enable default encryption (SSE-S3 or SSE-KMS)
   - Enable bucket versioning and logging
   - Implement bucket policies with explicit denies
   - Use S3 Access Points for application-specific access

   **Network Security:**
   - Restrict Security Groups to minimum required ports
   - Enable VPC Flow Logs for all VPCs
   - Use AWS Network Firewall for deep packet inspection
   - Implement VPC endpoints for AWS service access
   - Segment workloads using multiple subnets

   **Logging & Monitoring:**
   - Enable CloudTrail in all regions
   - Enable CloudTrail log file validation
   - Configure CloudWatch alarms for suspicious activity
   - Enable AWS Config for configuration tracking
   - Deploy GuardDuty for threat detection

   **Encryption:**
   - Enable default EBS encryption
   - Use KMS customer-managed keys (CMKs)
   - Enable encryption for RDS instances
   - Use SSL/TLS for data in transit
   - Rotate encryption keys annually

**3. Framework Integration**
   - Map all findings to CIS AWS Foundations Benchmark control IDs
   - Reference AWS Well-Architected Security Pillar best practices
   - Include AWS Config remediation rules
   - Provide CloudFormation/Terraform templates for fixes

---

## Common AWS Vulnerabilities

### IAM Vulnerabilities
- **No MFA on Root Account** - Root account accessible with password only
- **Overly Permissive Policies** - AdministratorAccess attached to users/roles
- **Unused Access Keys** - IAM access keys not rotated in 90+ days
- **Cross-Account Misconfigurations** - Overly permissive AssumeRole trust policies
- **Privilege Escalation Paths** - iam:PassRole + service creation combinations

### S3 Vulnerabilities
- **Public Buckets** - ACLs allowing public read/write
- **Unencrypted Data** - Server-side encryption disabled
- **Missing Bucket Policies** - No explicit deny for public access
- **Logging Disabled** - No access logging enabled
- **Versioning Disabled** - No protection against accidental deletion

### EC2/VPC Vulnerabilities
- **Overly Permissive Security Groups** - 0.0.0.0/0 inbound rules for SSH/RDP
- **Public Instances** - Critical instances with public IP addresses
- **Unencrypted EBS Volumes** - Encryption at rest not enabled
- **Missing VPC Flow Logs** - No network traffic logging
- **Instance Metadata v1** - IMDSv2 not enforced (SSRF risk)

### RDS/Database Vulnerabilities
- **Publicly Accessible Databases** - Public accessibility enabled
- **Unencrypted Databases** - Storage encryption disabled
- **Missing Backups** - Automated backups disabled
- **Weak Security Groups** - Database accessible from 0.0.0.0/0

### Logging/Monitoring Vulnerabilities
- **CloudTrail Disabled** - No audit logging
- **Missing Log File Validation** - CloudTrail logs not validated
- **No GuardDuty** - Threat detection not enabled
- **Missing Config** - Configuration changes not tracked

---

## Testing Tools

**AWS-Native:**
- aws-cli - AWS command-line interface for manual enumeration
- AWS Security Hub - Centralized security findings dashboard
- AWS Config - Configuration compliance tracking
- Amazon Inspector - Automated vulnerability scanning
- Amazon GuardDuty - Threat detection service

**Third-Party:**
- **prowler** - CIS benchmark scanner (PRIMARY TOOL)
- scoutsuite - Multi-cloud security auditing
- pacu - AWS exploitation framework
- CloudMapper - Network diagram visualization
- CloudSploit - Configuration scanning

**Manual Testing:**
- curl/wget - HTTP requests for public resource testing
- nmap - Network scanning (authorized testing only)
- sqlmap - SQL injection testing (RDS endpoints)

---

## AWS Service Coverage Matrix

| Service | CIS Coverage | Prowler Checks | Manual Testing Required |
|---------|--------------|----------------|------------------------|
| IAM | ✅ High | 40+ checks | Privilege escalation |
| S3 | ✅ High | 30+ checks | Public access validation |
| EC2 | ✅ Medium | 25+ checks | Network penetration |
| RDS | ✅ Medium | 15+ checks | Database enumeration |
| Lambda | ✅ Low | 10+ checks | Secrets extraction |
| VPC | ✅ Medium | 20+ checks | Flow log analysis |
| CloudTrail | ✅ High | 15+ checks | Log integrity |
| KMS | ✅ Medium | 10+ checks | Key rotation validation |
| Secrets Manager | ✅ Low | 5+ checks | Secret enumeration |
| GuardDuty | ✅ Low | 5+ checks | Alert configuration |

---

## Privilege Escalation Vectors

**21 AWS Privilege Escalation Techniques:**

1. **iam:CreateAccessKey** - Create access keys for other users
2. **iam:CreateLoginProfile** - Create console password for other users
3. **iam:UpdateLoginProfile** - Reset console password for other users
4. **iam:AttachUserPolicy** - Attach AdministratorAccess to users
5. **iam:AttachGroupPolicy** - Attach policies to groups
6. **iam:AttachRolePolicy** - Attach policies to roles
7. **iam:PutUserPolicy** - Create inline policies for users
8. **iam:PutGroupPolicy** - Create inline policies for groups
9. **iam:PutRolePolicy** - Create inline policies for roles
10. **iam:AddUserToGroup** - Add users to privileged groups
11. **iam:UpdateAssumeRolePolicy** - Modify role trust relationships
12. **iam:PassRole + ec2:RunInstances** - Launch instance with privileged role
13. **iam:PassRole + lambda:CreateFunction** - Create Lambda with privileged role
14. **iam:PassRole + glue:CreateJob** - Create Glue job with privileged role
15. **iam:PassRole + datapipeline:CreatePipeline** - Create pipeline with privileged role
16. **lambda:UpdateFunctionCode** - Modify Lambda to execute malicious code
17. **ec2:ModifyInstanceAttribute** - Attach privileged instance profile
18. **sts:AssumeRole** - Assume roles with elevated permissions
19. **cloudformation:CreateStack** - Deploy stack with privileged resources
20. **codestar:CreateProjectFromTemplate** - Create project with CloudFormation
21. **datapipeline:ActivatePipeline** - Execute pipeline with privileged role

**See:** https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation for detailed exploitation techniques

---

## Reference Resources

**CIS AWS Foundations Benchmark:**
- Website: https://www.cisecurity.org/benchmark/amazon_web_services
- Use: Compliance baseline for AWS security

**AWS Well-Architected Framework:**
- Website: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
- Use: Security design principles and best practices

**AWS Security Hub Standards:**
- Website: https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference.html
- Use: Complete control mappings and testing procedures

**Prowler Documentation:**
- Website: https://github.com/prowler-cloud/prowler
- Use: Automated CIS benchmark scanning

**AWS IAM Privilege Escalation:**
- GitHub: https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation
- Use: Exploitation techniques for testing

---

**Created:** 2025-12-03
**Framework:** Intelligence Adjacent (IA) - Cloud Security Testing
**Version:** 1.0
