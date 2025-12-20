
## Methodology Overview

GCP security testing identifies misconfigurations, excessive permissions, data exposure risks, and privilege escalation paths in Google Cloud Platform environments using automated scanning (scoutsuite), manual enumeration (gcloud CLI), and compliance frameworks (CIS, ISO).

---

## CIS GCP Foundations Benchmark Integration

**Benchmark Version:** CIS Google Cloud Platform Foundations Benchmark v2.0.0
**Coverage:** 70+ controls across 7 sections
**Tool:** scoutsuite (automated CIS compliance scanning)

### CIS Control Categories

1. **Identity and Access Management** (IAM)
2. **Logging and Monitoring** (Cloud Logging, Cloud Monitoring)
3. **Networking** (VPC, Firewall Rules, Cloud Armor)
4. **Virtual Machines** (Compute Engine)
5. **Storage** (Cloud Storage, Cloud SQL)
6. **Cloud SQL Database Services**
7. **BigQuery** (Data warehouse security)

---

## GCP Security Best Practices Framework

**5 Pillars:**

1. **Secure by Default** - Apply security controls automatically
2. **Secure at Scale** - Leverage automation and policy enforcement
3. **Defense in Depth** - Multiple layers of security controls
4. **Least Privilege** - Grant minimum necessary permissions
5. **Shared Responsibility** - Understand GCP vs. customer responsibilities

**Key Services:**
- **Security Command Center** - Centralized security findings
- **VPC Service Controls** - Data exfiltration protection
- **Identity-Aware Proxy (IAP)** - Zero-trust access control
- **Binary Authorization** - Container image signing and validation

---

## Testing Methodology Structure

### EXPLORE Phase

**1. Scope Review**
   - Read SCOPE.md for target GCP projects and organizations
   - Identify services in scope (Compute Engine, GCS, Cloud SQL, GKE, etc.)
   - Understand authorization level (Viewer, Editor, Owner, custom roles)
   - Note compliance requirements (CIS, ISO 27001, PCI-DSS)
   - Identify sensitive data locations

**2. Project Reconnaissance**
   - Enumerate GCP projects and organization hierarchy
   - List active services and APIs per project
   - Identify IAM principals (users, service accounts, groups)
   - Map resource inventory (VMs, storage buckets, databases)
   - Identify public-facing resources

**3. Permission Mapping**
   - Review IAM policies at organization, folder, and project levels
   - Identify overly permissive roles (Owner, Editor at org level)
   - Map service account key usage
   - Check for domain-wide delegation
   - Identify custom roles with excessive permissions

**4. Threat Modeling**
   - Identify high-value targets (Cloud SQL, GCS buckets, GKE clusters)
   - Map privilege escalation paths
   - Analyze data exfiltration scenarios via Cloud Storage
   - Document trust boundaries (VPC Service Controls)
   - Prioritize attack vectors

---

### PLAN Phase

**1. Vulnerability Prioritization**
   - **Critical:** Public GCS buckets with sensitive data, service accounts with domain-wide delegation, Owner role at organization level
   - **High:** Overly permissive firewall rules (0.0.0.0/0), unencrypted Cloud SQL, missing Cloud Logging
   - **Medium:** Unused service account keys, missing VPC Flow Logs, unencrypted persistent disks
   - **Low:** Missing resource labels, weak Cloud SQL password policy

**2. Tool Inventory Check** (CRITICAL)
   - Review `/servers` for cloud security tools
   - Check for: scoutsuite, gcloud CLI, gcpwn
   - Verify GCP credentials configured (application default credentials)
   - Test API access with `gcloud auth list`
   - Request deployment if tools missing

**3. Test Plan Generation**
   - Map CIS controls to specific tests
   - Document testing approach:
     - Automated scanning (scoutsuite CIS checks)
     - Manual enumeration (gcloud queries)
     - Privilege escalation testing
     - Data exfiltration simulation
     - Container security testing (GKE)
   - Plan for both read-only and exploit scenarios
   - Get user approval before testing

---

### CODE Phase (Testing)

**Automated Scanning:**

**1. CIS Benchmark Compliance (scoutsuite)**
   ```bash
   # Run full GCP security audit
   scout gcp --report-dir ./scoutsuite-report

   # Scan specific project
   scout gcp --project-id <project-id> --report-dir ./report

   # Generate JSON output for automation
   scout gcp --no-browser --report-dir ./report
   ```

**2. Service-Specific Scans**
   - IAM: Role analysis, service account enumeration
   - GCS: Public bucket detection, ACL review, encryption status
   - Compute Engine: Firewall rules, instance metadata, disk encryption
   - Cloud SQL: Public accessibility, encryption, backup retention
   - GKE: Node security, pod security policies, network policies
   - Cloud Logging: Log retention, sink configuration

**Manual Enumeration:**

**3. IAM Security Testing**
   ```bash
   # List projects and permissions
   gcloud projects list
   gcloud projects get-iam-policy <project-id>

   # Enumerate service accounts
   gcloud iam service-accounts list --project <project-id>

   # List service account keys
   gcloud iam service-accounts keys list --iam-account <sa-email>

   # Check for domain-wide delegation
   gcloud iam service-accounts get-iam-policy <sa-email>

   # Find overly permissive roles
   gcloud projects get-iam-policy <project-id> --flatten="bindings[].members" --filter="bindings.role:roles/owner"
   ```

**4. Cloud Storage Security Testing**
   ```bash
   # List all buckets
   gsutil ls -p <project-id>

   # Check bucket IAM policies
   gsutil iam get gs://<bucket-name>

   # Check for public access
   gsutil iam ch allUsers:objectViewer gs://<bucket-name> --dry-run

   # Check encryption configuration
   gsutil encryption get gs://<bucket-name>

   # Test public read access
   curl -I https://storage.googleapis.com/<bucket-name>/<object-name>
   ```

**5. Compute Engine Security Testing**
   ```bash
   # List instances with external IPs
   gcloud compute instances list --filter="networkInterfaces[].accessConfigs[0].natIP:*" --format="table(name,zone,networkInterfaces[0].accessConfigs[0].natIP)"

   # Review firewall rules for 0.0.0.0/0
   gcloud compute firewall-rules list --filter="sourceRanges:(0.0.0.0/0)" --format="table(name,direction,sourceRanges,allowed[])"

   # Check for unencrypted disks
   gcloud compute disks list --filter="NOT diskEncryptionKey:*" --format="table(name,zone,sizeGb)"

   # Test instance metadata access (from VM)
   curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/
   curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
   ```

**6. Cloud SQL Security Testing**
   ```bash
   # Find publicly accessible databases
   gcloud sql instances list --format="table(name,ipAddresses[0].ipAddress,settings.ipConfiguration.authorizedNetworks)"

   # Check encryption status
   gcloud sql instances describe <instance-name> --format="get(diskEncryptionConfiguration)"

   # Review database flags
   gcloud sql instances describe <instance-name> --format="get(settings.databaseFlags)"

   # Check for SSL enforcement
   gcloud sql instances describe <instance-name> --format="get(settings.ipConfiguration.requireSsl)"
   ```

**7. GKE Security Testing**
   ```bash
   # List GKE clusters
   gcloud container clusters list

   # Check cluster security settings
   gcloud container clusters describe <cluster-name> --zone <zone> --format="get(masterAuth,networkPolicy,binaryAuthorization)"

   # Review node pool configurations
   gcloud container node-pools describe <pool-name> --cluster <cluster-name> --zone <zone>

   # Check for public endpoints
   gcloud container clusters describe <cluster-name> --zone <zone> --format="get(endpoint)"
   ```

**8. Secrets & Credentials Testing**
   ```bash
   # List Secret Manager secrets
   gcloud secrets list --project <project-id>

   # Check secret IAM policies
   gcloud secrets get-iam-policy <secret-name>

   # Review service account keys
   gcloud iam service-accounts keys list --iam-account <sa-email> --managed-by=user

   # Check for hardcoded credentials in Cloud Functions
   gcloud functions list --format="table(name,runtime,environmentVariables)"
   ```

**Privilege Escalation Testing:**

**9. IAM Privilege Escalation Paths**
   - Test `iam.serviceAccounts.actAs` + resource creation
   - Attempt `iam.serviceAccountKeys.create` on other service accounts
   - Test `resourcemanager.projects.setIamPolicy` for policy modification
   - Exploit `deploymentmanager.deployments.create` for privileged resource creation
   - Test Cloud Functions deployment for privilege escalation

**10. Service Account Impersonation**
   - Test `iam.serviceAccounts.getAccessToken` for token generation
   - Attempt service account impersonation chains
   - Test domain-wide delegation exploitation

**Network Testing:**

**11. VPC Security Testing**
   ```bash
   # Review VPC Flow Logs status
   gcloud compute networks subnets list --format="table(name,region,enableFlowLogs)"

   # Check for default network usage
   gcloud compute networks describe default

   # Review VPC Service Controls
   gcloud access-context-manager perimeters list --policy=<policy-id>

   # Test VPC peering configurations
   gcloud compute networks peerings list
   ```

**Evidence Collection:**
- Screenshot of scoutsuite scan results
- gcloud CLI command outputs demonstrating misconfigurations
- Proof of privilege escalation (service account impersonation)
- Evidence of data access (GCS object retrieval)
- Map findings to CIS control IDs

---

### COMMIT Phase (Reporting)

**1. Findings Documentation**
   - Executive summary (business impact focus)
   - Technical findings mapped to CIS GCP Foundations Benchmark
   - Severity ratings (Critical, High, Medium, Low)
   - Successful exploit demonstrations
   - Impact analysis (data exposure, privilege escalation, compliance)

**2. Remediation Recommendations**

   **IAM Hardening:**
   - Remove Owner/Editor roles at organization level
   - Implement least privilege with custom roles
   - Rotate service account keys every 90 days
   - Remove unused service accounts
   - Enable Cloud Asset Inventory for access tracking

   **Cloud Storage Security:**
   - Block public access using organization policies
   - Enable default encryption with CMEK (Customer-Managed Encryption Keys)
   - Enable bucket logging and versioning
   - Implement bucket-level IAM policies
   - Use signed URLs for temporary access

   **Network Security:**
   - Restrict firewall rules to minimum required ports
   - Enable VPC Flow Logs for all subnets
   - Implement VPC Service Controls for data exfiltration prevention
   - Use Cloud Armor for DDoS protection
   - Segment workloads using multiple VPCs

   **Logging & Monitoring:**
   - Enable Cloud Logging for all projects
   - Configure log sinks to Cloud Storage or BigQuery
   - Set up Cloud Monitoring alerts for suspicious activity
   - Enable Security Command Center for threat detection
   - Implement log retention policies (90+ days)

   **Encryption:**
   - Enable encryption for persistent disks with CMEK
   - Use Customer-Supplied Encryption Keys (CSEK) for sensitive data
   - Enable encryption for Cloud SQL instances
   - Use TLS for data in transit
   - Rotate encryption keys annually

**3. Framework Integration**
   - Map all findings to CIS GCP Foundations Benchmark control IDs
   - Reference GCP Security Best Practices
   - Include Cloud Deployment Manager templates for fixes
   - Provide Terraform configurations for remediation

---

## Common GCP Vulnerabilities

### IAM Vulnerabilities
- **Overly Permissive Roles** - Owner/Editor at organization level
- **Service Account Key Exposure** - Keys in source code or environment variables
- **Domain-Wide Delegation** - Service accounts with excessive delegation
- **Unused Service Accounts** - Service accounts not used in 90+ days
- **Privilege Escalation Paths** - iam.serviceAccounts.actAs + resource creation

### Cloud Storage Vulnerabilities
- **Public Buckets** - allUsers or allAuthenticatedUsers permissions
- **Unencrypted Data** - Default encryption only (not CMEK)
- **Missing Logging** - No access logging enabled
- **Versioning Disabled** - No protection against accidental deletion
- **Weak IAM Policies** - Overly permissive bucket-level policies

### Compute Engine/VPC Vulnerabilities
- **Overly Permissive Firewall Rules** - 0.0.0.0/0 inbound rules for SSH/RDP
- **Public Instances** - Critical instances with external IPs
- **Unencrypted Disks** - Persistent disks without CMEK encryption
- **Missing VPC Flow Logs** - No network traffic logging
- **Default Network Usage** - Resources in default VPC

### Cloud SQL/Database Vulnerabilities
- **Publicly Accessible Databases** - Authorized networks including 0.0.0.0/0
- **Unencrypted Databases** - Storage encryption disabled
- **Missing Backups** - Automated backups disabled
- **No SSL Enforcement** - requireSsl flag not set

### GKE/Container Vulnerabilities
- **Public GKE Endpoints** - Master endpoint accessible from internet
- **Missing Binary Authorization** - No image signing validation
- **Weak Network Policies** - No Kubernetes network policies
- **Legacy ABAC Enabled** - Attribute-based access control instead of RBAC

### Logging/Monitoring Vulnerabilities
- **Cloud Logging Disabled** - No audit logging
- **Missing Log Sinks** - Logs not exported to long-term storage
- **No Security Command Center** - Threat detection not enabled
- **Short Log Retention** - Logs retained <90 days

---

## Testing Tools

**GCP-Native:**
- gcloud CLI - Google Cloud command-line interface
- Security Command Center - Centralized security findings
- Cloud Asset Inventory - Resource inventory and analysis
- Cloud Logging - Audit log review
- VPC Service Controls - Data exfiltration controls

**Third-Party:**
- **scoutsuite** - CIS benchmark scanner (PRIMARY TOOL)
- gcpwn - GCP privilege escalation and enumeration
- GCPBucketBrute - Cloud Storage bucket enumeration
- gcp-iam-privilege-escalation - Privilege escalation testing

**Manual Testing:**
- curl/wget - HTTP requests for public resource testing
- kubectl - GKE cluster security testing
- docker - Container image analysis

---

## GCP Service Coverage Matrix

| Service | CIS Coverage | ScoutSuite Checks | Manual Testing Required |
|---------|--------------|-------------------|------------------------|
| IAM | ✅ High | 35+ checks | Privilege escalation |
| Cloud Storage | ✅ High | 25+ checks | Public access validation |
| Compute Engine | ✅ Medium | 20+ checks | Network penetration |
| Cloud SQL | ✅ Medium | 15+ checks | Database enumeration |
| GKE | ✅ Medium | 20+ checks | Container security |
| VPC | ✅ Medium | 15+ checks | Flow log analysis |
| Cloud Logging | ✅ High | 10+ checks | Log integrity |
| KMS | ✅ Medium | 10+ checks | Key rotation validation |
| Secret Manager | ✅ Low | 5+ checks | Secret enumeration |
| Cloud Functions | ✅ Low | 10+ checks | Code review |

---

## Privilege Escalation Vectors

**15 GCP Privilege Escalation Techniques:**

1. **iam.serviceAccountKeys.create** - Create keys for other service accounts
2. **iam.serviceAccounts.actAs** - Impersonate service accounts
3. **iam.serviceAccounts.getAccessToken** - Generate access tokens
4. **iam.serviceAccounts.signBlob** - Sign arbitrary data as service account
5. **resourcemanager.projects.setIamPolicy** - Modify project IAM policies
6. **resourcemanager.organizations.setIamPolicy** - Modify organization policies
7. **compute.instances.create** - Create instance with privileged service account
8. **cloudfunctions.functions.create** - Deploy function with privileged service account
9. **cloudfunctions.functions.update** - Modify function code for escalation
10. **run.services.create** - Deploy Cloud Run service with privileged SA
11. **deploymentmanager.deployments.create** - Deploy resources with elevated permissions
12. **composer.environments.create** - Create Cloud Composer with privileged SA
13. **dataproc.clusters.create** - Create Dataproc cluster with privileged SA
14. **iam.roles.update** - Modify custom role permissions
15. **storage.buckets.setIamPolicy** - Modify bucket policies for access

**See:** https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation for detailed exploitation techniques

---

## Reference Resources

**CIS GCP Foundations Benchmark:**
- Website: https://www.cisecurity.org/benchmark/google_cloud_computing_platform
- Use: Compliance baseline for GCP security

**GCP Security Best Practices:**
- Website: https://cloud.google.com/security/best-practices
- Use: Security design principles and configurations

**ScoutSuite Documentation:**
- Website: https://github.com/nccgroup/ScoutSuite
- Use: Automated CIS benchmark scanning

**GCP IAM Privilege Escalation:**
- GitHub: https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation
- Use: Exploitation techniques for testing

**GCP Security Documentation:**
- Website: https://cloud.google.com/security/overview
- Use: Official security guidance

---

**Created:** 2025-12-03
**Framework:** Intelligence Adjacent (IA) - Cloud Security Testing
**Version:** 1.0
