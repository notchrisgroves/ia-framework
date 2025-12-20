
## Core Principle: Scope-Based Context Loading

**CRITICAL RULE:** Only load cloud-specific methodology when platform is in scope

**Why:** Each cloud framework is 300-400 lines. Loading all 3 = 900-1200 lines of unnecessary context.

**Pattern:**
```
1. Read SCOPE.md
2. Identify cloud platform(s) in scope
3. Load ONLY relevant framework(s):
   - AWS in scope → Read aws-framework.md
   - GCP in scope → Read gcp-framework.md
   - Azure in scope → Read azure-framework.md
4. Execute platform-specific methodology
```

---

## Scope Detection Decision Tree

### Step 1: Read SCOPE.md

**Look for cloud platform indicators:**

**AWS Indicators:**
- Account IDs (12 digits)
- Regions (us-east-1, eu-west-2, etc.)
- Services (EC2, S3, RDS, Lambda, etc.)
- ARNs (arn:aws:...)
- Keywords: "AWS", "Amazon Web Services"

**GCP Indicators:**
- Project IDs (alphanumeric with hyphens)
- Regions (us-central1, europe-west1, etc.)
- Services (Compute Engine, Cloud Storage, GKE, etc.)
- Resource names (projects/*/locations/*)
- Keywords: "GCP", "Google Cloud Platform"

**Azure Indicators:**
- Subscription IDs (GUIDs)
- Regions (eastus, westeurope, etc.)
- Services (VMs, Storage Accounts, SQL Database, AKS, etc.)
- Resource IDs (/subscriptions/.../resourceGroups/...)
- Keywords: "Azure", "Microsoft Azure"

---

### Step 2: Load Relevant Framework(s)

**Decision Logic:**

```python
# Pseudo-code for scope-based loading
scope = read("SCOPE.md")

if "AWS" in scope or detect_aws_resources(scope):
    methodology = read("aws-framework.md")
    execute_aws_testing()

if "GCP" in scope or detect_gcp_resources(scope):
    methodology = read("gcp-framework.md")
    execute_gcp_testing()

if "Azure" in scope or detect_azure_resources(scope):
    methodology = read("azure-framework.md")
    execute_azure_testing()

if multiple_platforms_in_scope:
    apply_multi_cloud_considerations()
```

**Examples:**

**Example 1: AWS-Only Scope**
```
SCOPE.md contains:
- AWS Account: 123456789012
- Regions: us-east-1, us-west-2
- Services: EC2, S3, RDS

Action: Read aws-framework.md ONLY
Skip: gcp-framework.md, azure-framework.md
```

**Example 2: Multi-Cloud Scope**
```
SCOPE.md contains:
- AWS Account: 123456789012
- GCP Project: my-project-prod
- Azure Subscription: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Action: Read aws-framework.md + gcp-framework.md + azure-framework.md
Apply multi-cloud considerations
```

**Example 3: GCP-Only Scope**
```
SCOPE.md contains:
- GCP Project: acme-production
- Services: GKE, Cloud SQL, Cloud Storage

Action: Read gcp-framework.md ONLY
Skip: aws-framework.md, azure-framework.md
```

---

## Multi-Cloud Testing Considerations

**ONLY apply these if multiple cloud platforms are in scope.**

### Cross-Cloud Attack Vectors

**1. Federated Identity Exploitation**
- AWS IAM roles with OIDC federation to GCP
- Azure AD as identity provider for AWS SSO
- Cross-cloud service account impersonation

**2. Data Exfiltration Across Clouds**
- AWS S3 → GCP Cloud Storage transfer
- Azure Blob → AWS S3 sync
- Cross-cloud database replication

**3. Network Connectivity**
- AWS VPC ↔ GCP VPC peering
- Azure VNet ↔ AWS VPC via VPN
- Cross-cloud private connectivity (AWS PrivateLink, GCP Private Service Connect, Azure Private Link)

**4. Hybrid IAM Misconfigurations**
- AWS IAM roles trusting GCP service accounts
- Azure AD groups with permissions in AWS
- Cross-cloud service principal permissions

---

## Universal Cloud Security Principles

**Applicable to ALL cloud platforms:**

### 1. Shared Responsibility Model
- **Provider:** Physical infrastructure, hypervisor, network
- **Customer:** Applications, data, access controls, encryption keys
- **Varies by:** IaaS (customer manages most) vs PaaS vs SaaS (provider manages most)

### 2. Least Privilege
- Grant minimum permissions required
- Use temporary credentials (STS, workload identity)
- Regular access reviews

### 3. Defense in Depth
- Multiple security layers
- Network segmentation
- Encryption at rest and in transit
- Logging and monitoring

### 4. Zero Trust
- Never trust, always verify
- Verify every access request
- Microsegmentation
- Continuous authentication

---

## Common Multi-Cloud Misconfigurations

**Applicable across AWS/GCP/Azure:**

### Identity & Access
- Overly permissive roles at highest level (AWS: Organization, GCP: Organization, Azure: Management Group)
- Missing MFA on admin accounts
- Long-lived credentials (access keys, service account keys)
- Unused IAM principals

### Data Storage
- Public storage buckets/blobs
- Unencrypted data at rest
- Missing versioning and soft delete
- Weak access policies

### Networking
- Overly permissive firewall rules (0.0.0.0/0)
- Public instances/VMs
- Missing network flow logs
- Weak VPC/VNet segmentation

### Logging & Monitoring
- Disabled audit logging
- Short log retention (<90 days)
- Missing threat detection services
- No SIEM integration

### Encryption
- Default encryption only (not customer-managed keys)
- Missing encryption in transit
- Weak key rotation policies
- Exposed encryption keys

---

## Tool Selection by Platform

### AWS
**Primary Tool:** prowler (CIS benchmark scanning)
**CLI:** aws-cli
**Exploitation:** pacu

### GCP
**Primary Tool:** scoutsuite (CIS benchmark scanning)
**CLI:** gcloud CLI
**Exploitation:** gcpwn

### Azure
**Primary Tool:** scoutsuite (CIS benchmark scanning)
**CLI:** az CLI
**Exploitation:** MicroBurst, AzureHound

### Multi-Cloud
**Primary Tool:** scoutsuite (supports all 3)
**Alternative:** Cloud Custodian, Prowler (AWS/Azure modules)

---

## Testing Workflow (Universal)

**EXPLORE → PLAN → CODE → COMMIT** (same across all clouds)

### EXPLORE Phase (All Clouds)
1. Read SCOPE.md for cloud platforms and services
2. Enumerate accounts/projects/subscriptions
3. Map IAM permissions and roles
4. Identify public-facing resources
5. Threat modeling

### PLAN Phase (All Clouds)
1. Prioritize vulnerabilities (Critical → High → Medium → Low)
2. Check `/servers` for platform-specific tools
3. Generate platform-specific test plan
4. Get user approval

### CODE Phase (All Clouds)
1. Automated scanning (prowler/scoutsuite)
2. Manual enumeration (CLI)
3. Privilege escalation testing
4. Network penetration testing
5. Evidence collection

### COMMIT Phase (All Clouds)
1. Document findings with framework control IDs
2. Provide platform-specific remediation guidance
3. Map to compliance frameworks (CIS, NIST, ISO)
4. Generate executive summary

---

## Scope-Based Methodology Loading Pattern

**Implementation for security agent:**

```markdown
## Cloud Security Testing Startup Sequence

**Step 1: Read Scope**
Read `SCOPE.md` or scope section in engagement documentation

**Step 2: Detect Platforms**
Identify which cloud platform(s) are in scope:
- AWS? (Account IDs, ARNs, AWS services)
- GCP? (Project IDs, GCP services)
- Azure? (Subscription GUIDs, Azure services)

**Step 3: Load Relevant Frameworks**
- IF AWS in scope → Read `skills/security-testing/methodologies/cloud/aws-framework.md`
- IF GCP in scope → Read `skills/security-testing/methodologies/cloud/gcp-framework.md`
- IF Azure in scope → Read `skills/security-testing/methodologies/cloud/azure-framework.md`
- IF multiple platforms → Read multi-cloud considerations from this file

**Step 4: Execute Platform-Specific Testing**
Follow EXPLORE-PLAN-CODE-COMMIT phases from loaded framework(s)

**DO NOT:**
- Load all 3 cloud frameworks by default
- Load AWS framework for GCP-only engagements
- Load GCP framework for Azure-only engagements
```

---

## CIS Benchmark Comparison

| Control Area | AWS CIS | GCP CIS | Azure CIS |
|-------------|---------|---------|-----------|
| IAM | 60% | 50% | 33% |
| Logging | 15% | 20% | 11% |
| Networking | 10% | 14% | 11% |
| Storage | 8% | 11% | 11% |
| Compute | 7% | 5% | 11% |
| Total Controls | 60+ | 70+ | 90+ |

---

## Compliance Framework Mapping

**CIS Benchmarks:**
- AWS: CIS AWS Foundations Benchmark v3.0.0
- GCP: CIS Google Cloud Platform Foundations Benchmark v2.0.0
- Azure: CIS Microsoft Azure Foundations Benchmark v2.1.0

**Additional Frameworks:**
- NIST SP 800-53 (AWS, Azure)
- NIST SP 800-171 (AWS, Azure)
- ISO 27001 (All platforms)
- PCI-DSS (All platforms)
- HIPAA (All platforms)

---

## Reference Materials

**AWS:**
- Framework: `skills/security-testing/methodologies/cloud/aws-framework.md`
- Resources: https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference.html

**Azure:**
- Framework: `skills/security-testing/methodologies/cloud/azure-framework.md`
- Resources: https://learn.microsoft.com/en-us/security/benchmark/azure/

**GCP:**
- Framework: `skills/security-testing/methodologies/cloud/gcp-framework.md`
- Resources: https://cloud.google.com/security/best-practices

**General:**
- Cloud Security Alliance: https://cloudsecurityalliance.org/

---

## Summary: Context Loading Decision Tree

```
Start
  ↓
Read SCOPE.md
  ↓
Detect Cloud Platform(s)
  ↓
┌─────────────────────────────────┐
│ AWS in scope?                   │
│ ├── YES → Read aws-framework.md │
│ └── NO → Skip                   │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│ GCP in scope?                   │
│ ├── YES → Read gcp-framework.md │
│ └── NO → Skip                   │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│ Azure in scope?                 │
│ ├── YES → Read azure-framework.md│
│ └── NO → Skip                   │
└─────────────────────────────────┘
  ↓
Execute Platform-Specific Testing
  ↓
EXPLORE → PLAN → CODE → COMMIT
  ↓
End
```

**Result:** Only relevant context loaded, 60-70% reduction in unnecessary framework content

---

**Created:** 2025-12-03
**Framework:** Intelligence Adjacent (IA) - Cloud Security Testing
**Version:** 1.0
**Pattern:** Scope-based context loading for efficient agent operation
