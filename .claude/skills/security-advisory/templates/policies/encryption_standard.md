---
type: template
name: encryption_standard
category: CATEGORY_NAME
classification: public
version: 1.0
last_updated: 2025-12-02
---

# Encryption Standard
*(Effective: {{EFFECTIVE_DATE}} | Version: {{VERSION}})*

## Document Control

| Version | Date | Author | Changes | Approved By | Next Review |
|---------|------|--------|---------|-------------|-------------|
| {{VERSION}} | {{EFFECTIVE_DATE}} | {{AUTHOR_NAME}} | {{CHANGE_SUMMARY}} | {{APPROVER_NAME}} | {{NEXT_REVIEW_DATE}} |

**Document History:**
- Track all standard revisions in the table above
- Include version number, date, author, summary of changes, approver, and next review date
- Maintain historical versions for audit purposes
- Archive superseded versions per document retention policy

---

## Purpose
This standard establishes comprehensive encryption requirements for protecting {{ORGANIZATION_NAME}}'s sensitive information and ensuring compliance with regulatory and industry standards. The standard provides guidance for selecting appropriate encryption algorithms, key management practices, and implementation methodologies that have received substantial public review and proven effectiveness. This standard aims to protect data confidentiality and integrity across all information systems, maintain compliance with federal regulations, and establish uniform encryption practices that support business operations while mitigating cybersecurity risks.

## Scope
This standard applies to all {{ORGANIZATION_NAME}} employees, contractors, consultants, temporary workers, and third-party users who handle, process, or access organizational data. Coverage includes all encryption technologies used for data protection including symmetric and asymmetric encryption, digital signatures, key exchange protocols, and cryptographic hash functions. The standard governs encryption implementation across all platforms including on-premises systems, cloud services, mobile devices, communication channels, and data storage repositories regardless of location or ownership.

## Standard Requirements

### 1. Symmetric Encryption Algorithms

**1.1 Approved Algorithms**
- Advanced Encryption Standard (AES) is the mandatory standard for all symmetric encryption
- AES-256 required for highly sensitive data and cryptographic operations
- AES-128 acceptable for standard business data with appropriate key management
- All implementations must use cryptographically secure modes of operation

**1.2 Implementation Requirements**
- AES implementations must comply with FIPS 140-2 Level 2 or higher certification
- Cipher Block Chaining (CBC), Galois/Counter Mode (GCM), or Counter (CTR) modes required
- Electronic Codebook (ECB) mode strictly prohibited for all implementations
- Initialization vectors (IVs) must be cryptographically random and unique per encryption operation

**1.3 Legacy Algorithm Transition**
- DES and 3DES algorithms must be phased out by {{LEGACY_SUNSET_DATE}}
- RC4 and other stream ciphers prohibited for new implementations
- Legacy systems requiring encryption must have documented migration plans
- Risk assessments required for any continued use of deprecated algorithms

### 2. Asymmetric Encryption and Digital Signatures

**2.1 Public Key Algorithms**
- RSA with minimum 2048-bit key length required for new implementations
- RSA-4096 recommended for long-term data protection and high-value assets
- Elliptic Curve Cryptography (ECC) with P-256 minimum curve size
- Ed25519 and Ed448 curves acceptable for digital signature applications

**2.2 Digital Signature Requirements**

| Algorithm | Minimum Key Size | Implementation Notes |
|-----------|------------------|---------------------|
| RSA | 2048 bits | Must use secure padding (PSS recommended) |
| ECDSA | P-256 curve | Consider RFC 6090 for patent compliance |
| EdDSA | Ed25519 | Preferred for new signature implementations |
| DSA | Deprecated | Migration required by {{LEGACY_SUNSET_DATE}} |

**2.3 Key Exchange Protocols**
- Ephemeral Diffie-Hellman (DHE) with minimum 2048-bit group parameters
- Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) with P-256 or stronger curves
- RSA key transport deprecated for new implementations
- Perfect Forward Secrecy (PFS) required for all external communications

### 3. Cryptographic Hash Functions

**3.1 Approved Hash Algorithms**
- SHA-256 minimum requirement for all new implementations
- SHA-384 and SHA-512 recommended for high-security applications
- SHA-3 family acceptable for specialized applications
- Blake2 and Blake3 approved for performance-critical applications

**3.2 Prohibited Hash Functions**
- MD5 strictly prohibited for all cryptographic purposes
- SHA-1 prohibited except for legacy compatibility with documented risk acceptance
- SHA-0 and other deprecated algorithms prohibited
- Custom or proprietary hash functions require {{POLICY_OWNER}} approval

### 4. Key Management Requirements

**4.1 Key Generation**
- Cryptographic keys must be generated using FIPS 140-2 approved random number generators
- Key generation must occur in secure, controlled environments
- Entropy sources must be validated and regularly tested
- Hardware Security Modules (HSMs) required for high-value key generation

**4.2 Key Storage and Protection**
- Master keys must be stored in FIPS 140-2 Level 3 or higher certified devices
- Key encryption keys (KEKs) must be protected with multi-person control
- Software-based key storage must use secure key vaults with proper access controls
- Key backup and recovery procedures must maintain security equivalence

**4.3 Key Lifecycle Management**
- Regular key rotation required based on data sensitivity and usage volume
- Automated key rotation preferred where technically feasible
- Key escrow required for business-critical encryption with proper governance
- Secure key destruction must be verifiable and documented

### 5. Transport Layer Security (TLS)

**5.1 TLS Version Requirements**
- TLS 1.3 required for all new implementations and external communications
- TLS 1.2 acceptable for internal communications with strong cipher suites
- TLS 1.1 and earlier versions prohibited for all implementations
- DTLS 1.2 or later required for UDP-based encrypted communications

**5.2 Cipher Suite Requirements**
- Perfect Forward Secrecy mandatory for all TLS connections
- AEAD cipher suites preferred (AES-GCM, ChaCha20-Poly1305)
- RSA key transport cipher suites prohibited
- NULL encryption and export-grade ciphers strictly prohibited

**5.3 Certificate Management**
- All TLS certificates must be issued by trusted Certificate Authorities
- Extended Validation (EV) certificates required for public-facing services
- Certificate pinning implemented for high-security applications
- Certificate transparency monitoring for all issued certificates

### 6. Application-Specific Requirements

**6.1 Database Encryption**
- Transparent Data Encryption (TDE) required for all production databases
- Column-level encryption for personally identifiable information (PII)
- Database connection encryption mandatory for all database communications
- Key management integration with enterprise key management systems

**6.2 Email Security**
- S/MIME or PGP encryption required for sensitive email communications
- Email gateway encryption for all external email communications
- Digital signatures required for executive and financial communications
- Secure email policies must align with data classification requirements

**6.3 Cloud Service Encryption**
- Customer-managed encryption keys (CMEK) required for sensitive cloud data
- Cloud-native encryption services must meet organizational standards
- Multi-cloud encryption key management strategy required
- Regular security assessments of cloud encryption implementations

## Roles and Responsibilities

**Cryptography Team:**
- Develop and maintain encryption standards and implementation guidelines
- Evaluate new encryption technologies and update approved algorithm lists
- Provide technical guidance for encryption implementation projects
- Conduct security reviews of cryptographic implementations

**System Administrators:**
- Implement encryption controls according to approved standards
- Maintain encryption key management systems and procedures
- Monitor encryption system performance and security
- Report encryption failures and security incidents

**Security Architecture Team:**
- Design encryption architectures that meet business and security requirements
- Review encryption implementations for compliance with standards
- Integrate encryption requirements into system design processes
- Coordinate encryption requirements across enterprise architecture

**{{POLICY_OWNER}}:**
- Overall encryption program governance and policy management
- Approve exceptions to encryption standards and requirements
- Coordinate with legal and compliance teams on regulatory requirements
- Ensure encryption standards align with industry best practices

## Compliance and Monitoring

**Performance Metrics:**
- Percentage of systems compliant with encryption standards
- Encryption key rotation compliance rates
- Time to implement encryption for new systems
- Encryption-related security incident rates

**Monitoring Activities:**
- Continuous monitoring of encryption implementations and configurations
- Regular assessments of encryption key management practices
- Automated scanning for weak or deprecated encryption algorithms
- Annual encryption program effectiveness reviews

**Audit Requirements:**
- Quarterly encryption compliance assessments
- Annual penetration testing of encryption implementations
- Independent validation of key management procedures
- Regular reviews of encryption policy adherence

## Exception Management

**Exception Process:**
Requests for exceptions to encryption standards must include:
- Detailed business justification and risk assessment
- Alternative security controls and risk mitigation measures
- Timeline for achieving compliance with standards
- Regular review and re-evaluation of exception status

**Approval Authority:**
- Standard exceptions: {{POLICY_OWNER}} approval required
- High-risk exceptions: {{POLICY_OWNER}} and CISO approval required
- Regulatory exceptions: Legal and compliance team consultation required
- All exceptions subject to regular review and time limitations

## Related Policies and Standards

- **Data Classification and Protection Policy**
- **Key Management Procedures**
- **Certificate Management Standards**
- **Cloud Security Requirements**
- **Information Security Architecture Standards**
- **Cryptographic Module Standards**

## Framework Compliance Mapping

**NIST Cybersecurity Framework:**
- PR.DS-1: Data-at-rest is protected
- PR.DS-2: Data-in-transit is protected
- PR.AC-1: Identities and credentials are issued and managed

**ISO 27001 Controls:**
- A.10.1.1: Policy on the use of cryptographic controls
- A.10.1.2: Key management
- A.13.1.1: Network controls

**COBIT Framework:**
- DSS05.02: Manage network and connectivity security
- DSS05.06: Manage network security

**FIPS 140-2:**
- Security Level 2 minimum for all cryptographic modules
- Security Level 3 required for key management systems
- Regular validation and certification maintenance

---
*This standard supports compliance with: {{COMPLIANCE_FRAMEWORKS}}*  
*Policy Owner: {{POLICY_OWNER}} | Next Review: {{NEXT_REVIEW_DATE}}*  
*For questions or clarifications, contact: {{CONTACT_EMAIL}}*