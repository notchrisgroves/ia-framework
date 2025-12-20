
## Methodology Overview

Azure security testing identifies misconfigurations, excessive permissions, data exposure risks, and privilege escalation paths in Microsoft Azure environments using automated scanning (scoutsuite), manual enumeration (az CLI), and compliance frameworks (CIS, MCSB).

---

## CIS Azure Foundations Benchmark Integration

**Benchmark Version:** CIS Microsoft Azure Foundations Benchmark v2.1.0
**Coverage:** 90+ controls across 10 sections
**Tool:** scoutsuite (automated CIS compliance scanning)

### CIS Control Categories

1. **Identity and Access Management** (Azure AD, RBAC)
2. **Microsoft Defender for Cloud** (Security Center)
3. **Storage Accounts**
4. **Database Services** (SQL Database, PostgreSQL, MySQL)
5. **Logging and Monitoring** (Azure Monitor, Log Analytics)
6. **Networking** (Virtual Networks, NSGs, Firewall)
7. **Virtual Machines**
8. **Key Vault**
9. **App Service**
10. **Other Security Considerations** (AKS, Functions, Logic Apps)

**See:** Microsoft Cloud Security Benchmark documentation for control details (use WebFetch)

---

## Microsoft Cloud Security Benchmark (MCSB)

**MCSB v2 Design Principles:**

1. **Network Security** - Perimeter security, segmentation, DDoS protection
2. **Identity Management** - Azure AD, conditional access, privileged identity management
3. **Privileged Access** - Just-in-time access, MFA enforcement
4. **Data Protection** - Encryption at rest and in transit
5. **Asset Management** - Resource inventory, classification, lifecycle management
6. **Logging and Threat Detection** - Microsoft Sentinel, Azure Monitor
7. **Posture and Vulnerability Management** - Microsoft Defender for Cloud
8. **Endpoint Security** - Endpoint protection, device compliance
9. **Backup and Recovery** - Azure Backup, disaster recovery
10. **DevOps Security** - Secure development lifecycle
11. **Governance and Strategy** - Azure Policy, compliance management
12. **AI Security** ⭐ NEW - 7 AI-specific recommendations

**Monitoring:** Microsoft Defender for Cloud regulatory compliance dashboard

---

## Testing Methodology Structure

### EXPLORE Phase

**1. Scope Review**
   - Read SCOPE.md for target Azure subscriptions and resource groups
   - Identify services in scope (VMs, Storage, SQL, AKS, App Service, etc.)
   - Understand authorization level (Reader, Contributor, Owner, custom roles)
   - Note compliance requirements (CIS, MCSB, ISO 27001, PCI-DSS)
   - Identify sensitive data locations

**2. Subscription Reconnaissance**
   - Enumerate Azure subscriptions and management groups
   - List resource groups and resources per subscription
   - Identify Azure AD users, groups, service principals
   - Map RBAC role assignments
   - Identify public-facing resources

**3. Permission Mapping**
   - Review RBAC assignments at management group, subscription, resource group levels
   - Identify overly permissive roles (Owner, Contributor at subscription)
   - Map service principal permissions
   - Check for managed identity assignments
   - Identify custom roles with excessive permissions

**4. Threat Modeling**
   - Identify high-value targets (SQL databases, Storage accounts, Key Vaults)
   - Map privilege escalation paths
   - Analyze data exfiltration scenarios
   - Document trust boundaries
   - Prioritize attack vectors

---

### PLAN Phase

**1. Vulnerability Prioritization**
   - **Critical:** Public storage blobs with sensitive data, Owner role at subscription level, missing MFA on admin accounts
   - **High:** Overly permissive NSGs (0.0.0.0/0), unencrypted SQL databases, missing Azure Monitor
   - **Medium:** Unused service principals, missing VNet flow logs, unencrypted VM disks
   - **Low:** Missing resource tags, weak SQL password policy

**2. Tool Inventory Check** (CRITICAL)
   - Review `/servers` for cloud security tools
   - Check for: scoutsuite, az CLI, AzureHound, MicroBurst
   - Verify Azure credentials configured (`az login`)
   - Test API access with `az account show`
   - Request deployment if tools missing

**3. Test Plan Generation**
   - Map CIS controls to specific tests
   - Document testing approach:
     - Automated scanning (scoutsuite CIS checks)
     - Manual enumeration (az CLI queries)
     - Privilege escalation testing
     - Data exfiltration simulation
     - Container security testing (AKS)
   - Plan for both read-only and exploit scenarios
   - Get user approval before testing

---

### CODE Phase (Testing)

**Automated Scanning:**

**1. CIS Benchmark Compliance (scoutsuite)**
   ```bash
   # Run full Azure security audit
   scout azure --report-dir ./scoutsuite-report

   # Scan specific subscription
   scout azure --subscription-ids <subscription-id> --report-dir ./report

   # Generate JSON output for automation
   scout azure --no-browser --report-dir ./report
   ```

**2. Service-Specific Scans**
   - Azure AD: User enumeration, role assignments, conditional access
   - Storage Accounts: Public blob detection, encryption status, SAS tokens
   - Virtual Machines: NSG analysis, disk encryption, extensions
   - SQL Database: Public accessibility, encryption, firewall rules
   - AKS: Node security, pod security, network policies
   - Key Vault: Access policies, purge protection, soft delete

**Manual Enumeration:**

**3. Azure AD/RBAC Security Testing**
   ```bash
   # List subscriptions
   az account list --output table

   # Review RBAC assignments
   az role assignment list --all --output table

   # Find users with Owner role
   az role assignment list --role "Owner" --include-inherited --output table

   # Enumerate Azure AD users
   az ad user list --output table

   # Check for MFA enforcement
   az ad user list --query "[].{UPN:userPrincipalName, MFA:strongAuthenticationMethods}" --output table

   # List service principals
   az ad sp list --all --output table

   # Review managed identities
   az identity list --output table
   ```

**4. Storage Account Security Testing**
   ```bash
   # List storage accounts
   az storage account list --output table

   # Check for public blob access
   az storage account show --name <account-name> --query "allowBlobPublicAccess"

   # Review storage account network rules
   az storage account show --name <account-name> --query "networkRuleSet"

   # Check encryption configuration
   az storage account show --name <account-name> --query "encryption"

   # Test public access
   curl -I https://<account-name>.blob.core.windows.net/<container>/<blob>
   ```

**5. Virtual Machine Security Testing**
   ```bash
   # List VMs with public IPs
   az vm list-ip-addresses --output table

   # Review NSG rules for 0.0.0.0/0
   az network nsg list --output table
   az network nsg rule list --nsg-name <nsg-name> --resource-group <rg> --query "[?sourceAddressPrefix=='*' || sourceAddressPrefix=='Internet']"

   # Check for unencrypted disks
   az disk list --query "[?encryptionSettings==null].[name,diskSizeGb]" --output table

   # Review VM extensions
   az vm extension list --resource-group <rg> --vm-name <vm-name> --output table
   ```

**6. SQL Database Security Testing**
   ```bash
   # List SQL servers
   az sql server list --output table

   # Check for public accessibility
   az sql server firewall-rule list --server <server-name> --resource-group <rg> --query "[?startIpAddress=='0.0.0.0']"

   # Check encryption status (TDE)
   az sql db tde show --database <db-name> --server <server-name> --resource-group <rg>

   # Review auditing configuration
   az sql server audit-policy show --name <server-name> --resource-group <rg>

   # Check for Azure AD authentication
   az sql server ad-admin list --server <server-name> --resource-group <rg>
   ```

**7. AKS Security Testing**
   ```bash
   # List AKS clusters
   az aks list --output table

   # Review AKS configuration
   az aks show --name <cluster-name> --resource-group <rg> --query "{AAD:aadProfile,RBAC:enableRbac,NetworkPolicy:networkProfile.networkPolicy}"

   # Get AKS credentials
   az aks get-credentials --name <cluster-name> --resource-group <rg>

   # Check pod security policies (kubectl)
   kubectl get psp

   # Review network policies
   kubectl get networkpolicies --all-namespaces
   ```

**8. Key Vault Security Testing**
   ```bash
   # List Key Vaults
   az keyvault list --output table

   # Check network access
   az keyvault show --name <vault-name> --query "properties.networkAcls"

   # Review access policies
   az keyvault show --name <vault-name> --query "properties.accessPolicies"

   # Check for soft delete and purge protection
   az keyvault show --name <vault-name> --query "{SoftDelete:properties.enableSoftDelete,PurgeProtection:properties.enablePurgeProtection}"

   # List secrets
   az keyvault secret list --vault-name <vault-name> --output table
   ```

**Privilege Escalation Testing:**

**9. Azure RBAC Privilege Escalation Paths**
   - Test `Microsoft.Authorization/roleAssignments/write` for role assignment
   - Attempt `Microsoft.Compute/virtualMachines/runCommand/action` for VM command execution
   - Test `Microsoft.KeyVault/vaults/secrets/read` for secret extraction
   - Exploit automation account runbooks for privilege escalation
   - Test service principal credential creation

**10. Managed Identity Exploitation**
   - Test managed identity token extraction from VM metadata
   - Attempt IMDS (Instance Metadata Service) access
   - Exploit application-assigned managed identities

**Network Testing:**

**11. VNet Security Testing**
   ```bash
   # Review VNet configurations
   az network vnet list --output table

   # Check for VNet peering
   az network vnet peering list --resource-group <rg> --vnet-name <vnet-name> --output table

   # Review NSG associations
   az network nsg list --output table

   # Check for VNet flow logs
   az network watcher flow-log list --location <location> --output table
   ```

**Evidence Collection:**
- Screenshot of scoutsuite scan results
- az CLI command outputs demonstrating misconfigurations
- Proof of privilege escalation (role assignment screenshots)
- Evidence of data access (Storage blob retrieval)
- Map findings to CIS control IDs

---

### COMMIT Phase (Reporting)

**1. Findings Documentation**
   - Executive summary (business impact focus)
   - Technical findings mapped to CIS Azure Foundations Benchmark
   - Severity ratings (Critical, High, Medium, Low)
   - Successful exploit demonstrations
   - Impact analysis (data exposure, privilege escalation, compliance)

**2. Remediation Recommendations**

   **Azure AD/RBAC Hardening:**
   - Enforce MFA on all accounts via conditional access
   - Implement least privilege with custom roles
   - Enable Privileged Identity Management (PIM) for admin roles
   - Remove unused service principals
   - Use Azure AD Identity Protection

   **Storage Security:**
   - Disable public blob access at storage account level
   - Enable encryption with customer-managed keys (CMK)
   - Enable soft delete and versioning
   - Implement private endpoints for VNet access
   - Use SAS tokens with expiration

   **Network Security:**
   - Restrict NSG rules to minimum required ports
   - Enable NSG flow logs for all NSGs
   - Implement Azure Firewall for centralized filtering
   - Use Application Gateway with WAF
   - Segment workloads using multiple VNets

   **Logging & Monitoring:**
   - Enable Azure Monitor for all resources
   - Configure Log Analytics workspace
   - Deploy Microsoft Sentinel for SIEM
   - Set up activity log alerts for privileged operations
   - Implement log retention (90+ days)

   **Encryption:**
   - Enable Azure Disk Encryption for VMs
   - Use customer-managed keys in Key Vault
   - Enable TDE for SQL databases
   - Use HTTPS/TLS for data in transit
   - Rotate encryption keys annually

**3. Framework Integration**
   - Map all findings to CIS Azure Foundations Benchmark control IDs
   - Reference Microsoft Cloud Security Benchmark
   - Include Azure Policy definitions for fixes
   - Provide ARM templates or Bicep for remediation

---

## Common Azure Vulnerabilities

### Azure AD/RBAC Vulnerabilities
- **Missing MFA** - Admin accounts without MFA enforcement
- **Overly Permissive RBAC** - Owner/Contributor at subscription level
- **Unused Service Principals** - Service principals with credentials not used in 90+ days
- **Weak Conditional Access** - Missing location or device compliance requirements
- **Privilege Escalation Paths** - roleAssignments/write at subscription level

### Storage Account Vulnerabilities
- **Public Blob Access** - allowBlobPublicAccess enabled
- **Unencrypted Data** - No customer-managed encryption keys
- **Missing Soft Delete** - No protection against accidental deletion
- **Weak Network Rules** - Storage accessible from all networks
- **SAS Token Exposure** - Long-lived SAS tokens in code

### VM/Compute Vulnerabilities
- **Overly Permissive NSGs** - 0.0.0.0/0 inbound rules for RDP/SSH
- **Public VMs** - Critical instances with public IPs
- **Unencrypted Disks** - Azure Disk Encryption not enabled
- **Missing Extensions** - No Azure Security Center agent
- **Instance Metadata v1** - IMDSv1 allows SSRF exploitation

### SQL Database Vulnerabilities
- **Publicly Accessible Databases** - Firewall rules allowing 0.0.0.0/0
- **Unencrypted Databases** - TDE (Transparent Data Encryption) disabled
- **Missing Auditing** - Database auditing not configured
- **No Azure AD Authentication** - SQL authentication only
- **Weak Firewall Rules** - Allow Azure services rule enabled globally

### AKS/Container Vulnerabilities
- **Public AKS API** - API server accessible from internet
- **Missing Azure AD Integration** - Local Kubernetes accounts in use
- **Weak Network Policies** - No Kubernetes network policies
- **No Pod Security** - Pod security policies/standards not enforced

### Logging/Monitoring Vulnerabilities
- **Azure Monitor Disabled** - No centralized logging
- **Missing Log Analytics** - Logs not exported to workspace
- **No Microsoft Sentinel** - SIEM not deployed
- **Short Log Retention** - Activity logs retained <90 days

---

## Testing Tools

**Azure-Native:**
- az CLI - Azure command-line interface
- Microsoft Defender for Cloud - Security posture management
- Azure Policy - Compliance enforcement
- Azure Monitor - Logging and alerting
- Microsoft Sentinel - SIEM/SOAR

**Third-Party:**
- **scoutsuite** - CIS benchmark scanner (PRIMARY TOOL)
- AzureHound - Azure AD privilege escalation enumeration
- MicroBurst - Azure exploitation toolkit
- ROADtools - Azure AD reconnaissance
- Stormspotter - Azure Red Team tool

**Manual Testing:**
- curl/wget - HTTP requests for public resource testing
- kubectl - AKS cluster security testing
- PowerShell - Azure PowerShell module

---

## Azure Service Coverage Matrix

| Service | CIS Coverage | ScoutSuite Checks | Manual Testing Required |
|---------|--------------|-------------------|------------------------|
| Azure AD | ✅ High | 30+ checks | Privilege escalation |
| Storage Accounts | ✅ High | 25+ checks | Public access validation |
| Virtual Machines | ✅ Medium | 20+ checks | Network penetration |
| SQL Database | ✅ Medium | 15+ checks | Database enumeration |
| AKS | ✅ Medium | 15+ checks | Container security |
| VNet | ✅ Medium | 15+ checks | NSG flow analysis |
| Azure Monitor | ✅ High | 10+ checks | Log review |
| Key Vault | ✅ Medium | 10+ checks | Secret enumeration |
| App Service | ✅ Low | 10+ checks | Code review |
| Functions | ✅ Low | 8+ checks | Secrets extraction |

---

## Privilege Escalation Vectors

**18 Azure Privilege Escalation Techniques:**

1. **roleAssignments/write** - Assign roles to principals
2. **virtualMachines/runCommand** - Execute commands on VMs
3. **keyVault/secrets/read** - Extract secrets and certificates
4. **webApps/publishingCredentials** - Retrieve deployment credentials
5. **automationAccounts/jobs/write** - Execute runbooks
6. **storageAccounts/listKeys** - Retrieve storage account keys
7. **databaseAccounts/listKeys** - Retrieve Cosmos DB keys
8. **servicePrincipals/credentials** - Add credentials to service principals
9. **applications/credentials** - Add credentials to applications
10. **deployments/write** - Deploy ARM templates with privileged resources
11. **managedIdentities/assign** - Assign managed identities
12. **policyAssignments/write** - Modify Azure Policy assignments
13. **customRoleDefinitions/write** - Create custom roles
14. **containerServices/write** - Deploy AKS with privileged service principal
15. **logicApps/triggers** - Execute Logic Apps with elevated permissions
16. **functionApps/keys** - Retrieve function app keys
17. **dataSources/write** - Modify Log Analytics data sources
18. **virtualNetworks/subnets/join** - Join VNets for lateral movement

**See:** https://github.com/NetSPI/MicroBurst for detailed exploitation techniques

---

## Reference Resources

**CIS Azure Foundations Benchmark:**
- Website: https://www.cisecurity.org/benchmark/azure
- Use: Compliance baseline for Azure security

**Microsoft Cloud Security Benchmark:**
- Website: https://learn.microsoft.com/en-us/security/benchmark/azure/
- Use: Security controls and recommendations

**Azure Security Best Practices:**
- Website: https://learn.microsoft.com/en-us/azure/security/fundamentals/best-practices-and-patterns
- Use: Complete guidance and control details

**ScoutSuite Documentation:**
- Website: https://github.com/nccgroup/ScoutSuite
- Use: Automated CIS benchmark scanning

**Azure Security Documentation:**
- Website: https://learn.microsoft.com/en-us/azure/security/
- Use: Official security guidance

**MicroBurst:**
- GitHub: https://github.com/NetSPI/MicroBurst
- Use: Azure exploitation toolkit

---

**Created:** 2025-12-03
**Framework:** Intelligence Adjacent (IA) - Cloud Security Testing
**Version:** 1.0
