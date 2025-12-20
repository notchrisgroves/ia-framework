
## Methodology Overview

Web3 security testing identifies vulnerabilities in smart contracts, DeFi protocols, and blockchain applications through static analysis, symbolic execution, fuzzing, and manual code review, validated against real-world exploit patterns.

---

## Framework Integration

### DeFiHackLabs - Real-World Exploit Patterns

**Discovery:** `Glob: resources/library/**/*defi*` or `**/*web3*` or `**/*consensys*`
**Coverage:** Real DeFi exploit proof-of-concepts and analysis

**What DeFiHackLabs Provides:**
- Actual exploit reproductions from major hacks
- Foundry/Hardhat test cases showing attack mechanics
- Step-by-step attack walkthroughs
- Flash loan attack patterns
- Reentrancy exploit examples
- Oracle manipulation PoCs
- Access control bypass cases
- Real case studies (Beanstalk, BonqDAO, Omni, Wormhole, etc.)

**Use Case:** Learn attack patterns from real exploits to build testing strategies

---

### Immunefi Top 10 Smart Contract Vulnerabilities

**Reference:** https://immunefi.com/immunefi-top-10/ (use WebFetch)
**Coverage:** Universal vulnerability checklist for smart contract auditing

**Top 10 Vulnerabilities:**

**V01: Improper Input Validation**
- Oracle price feed validation
- Token transfer parameters
- Governance proposal parameters
- DeFi protocol collateral ratios
- Bridge cross-chain message validation

**V02: Incorrect Calculation**
- Interest/yield calculations
- Liquidation price calculations
- Reward distribution logic
- Fee calculations
- Token price calculations
- Slippage calculations
- Margin/collateral calculations

**V03: Oracle/Price Manipulation** ⚠️ HIGH IMPACT
- Flash loan attacks on price oracles
- Staleness checks on price feeds
- Multi-source oracle aggregation
- Time-weighted average price (TWAP) manipulation
- Read-only reentrancy on price queries
- Chainlink/Pyth/Band integration issues

**V04: Weak Access Control**
- Admin function access (pause, upgrade, configuration)
- Ownership transfer mechanisms
- Role-based access control (RBAC) bypasses
- Modifier bypass attempts
- Function visibility issues (public vs external)
- Proxy admin controls

**V05: Replay Attacks/Signature Malleability**
- Order signature verification
- Nonce management issues
- Cross-chain message replay protection
- Signature malleability (ECDSA vs Schnorr)
- Domain separator usage (EIP-712)
- Transaction uniqueness checks

**V06: Rounding Error**
- Small amount transfers
- Fee calculations with multiple decimals
- Share/token minting calculations
- Interest accrual
- Price conversions between tokens
- Division before multiplication

**V07: Reentrancy** 🔴 CRITICAL
- Token transfer callbacks (ERC-777, ERC-721, ERC-1155)
- External protocol integrations
- Withdrawal patterns
- Read-only reentrancy (view/pure functions)
- Cross-contract calls
- **CEI Pattern:** Checks-Effects-Interactions

**V08: Frontrunning**
- DEX order placement
- Liquidation opportunities
- Oracle updates
- NFT minting/purchases
- Governance voting
- Vault entry/exit
- **Note:** Varies by chain (Ethereum vs L2s)

**V09: Uninitialized Proxy**
- UUPS proxy initialization
- Transparent proxy initialization
- Beacon proxy initialization
- Implementation contract selfdestruct
- Storage collision
- Upgrade authorization checks

**V10: Governance Attacks**
- Flash loan attacks on voting power
- Vote delegation manipulation
- Timelock bypass
- Proposal execution validation
- Quorum threshold bypass
- Multi-sig wallet compromises

---

### Smart Contract Security Fundamentals

**Reference:** "Fundamentals of Smart Contracts Security" (use WebSearch)
**Pages:** 88 (9 chunks of 10 pages each)
**Coverage:** Solidity security, common vulnerabilities, best practices

---

## Blockchain Platforms Covered

### Primary: EVM-Compatible Chains
- **Ethereum** (Solidity)
- **Polygon, Binance Smart Chain, Avalanche, Arbitrum, Optimism** (EVM-compatible)
- **Testing Framework:** Foundry, Hardhat, Truffle
- **Tools:** Slither, Mythril, Echidna, Manticore

### Secondary: Alternative Platforms
- **Solana** (Rust) - Limited coverage in DeFiHackLabs
- **Starknet** (Cairo) - Need Caracal tool
- **Cosmos** (CosmWasm) - Need additional resources
- **Polkadot** (Ink!) - Need additional resources

**Methodology Focus:** EVM/Solidity primarily, extensible to other platforms

---

## Testing Methodology Structure

### EXPLORE Phase

1. **Scope Review**
   - Read SCOPE.md for target contracts
   - Identify blockchain platform (Ethereum, Polygon, etc.)
   - Understand contract addresses and versions
   - Review whitepaper/documentation
   - Identify third-party integrations (oracles, DEXs, bridges)

2. **Contract Reconnaissance**
   - Verify contract source on Etherscan/block explorer
   - Identify contract architecture (upgradeable, immutable)
   - Map contract interactions and dependencies
   - Review token standards used (ERC-20, ERC-721, etc.)
   - Identify admin functions and access controls

3. **Immunefi Top 10 Mapping**
   - Map contract functions to vulnerability categories
   - Identify oracle dependencies (V03 priority)
   - Flag external calls (reentrancy risk V07)
   - Review math operations (V02, V06)
   - Check access control patterns (V04)

4. **Exploit Pattern Research**
   - Search DeFiHackLabs for similar protocol exploits
   - Review historical hacks in same category (DEX, lending, staking)
   - Identify applicable attack patterns
   - Study relevant PoCs from DeFiHackLabs

### PLAN Phase

1. **Vulnerability Prioritization**
   - **Critical:** Oracle manipulation (if present), Reentrancy
   - **High:** Access control, Incorrect calculations, Flash loan vectors
   - **Medium:** Input validation, Rounding errors
   - **Low:** Gas optimization, Code quality

2. **Tool Inventory Check** (CRITICAL)
   - Review `/servers` for blockchain testing tools
   - Check for: Slither, Mythril, Echidna, Foundry, Hardhat
   - Identify missing tools (especially Caracal for Cairo)
   - Request deployment if needed
   - Verify node access (Infura, Alchemy, or local)

3. **Test Plan Generation**
   - Map Immunefi Top 10 to specific contract functions
   - Document testing approach:
     - Static analysis (Slither, Semgrep)
     - Symbolic execution (Mythril, Manticore)
     - Fuzzing (Echidna, Foundry)
     - Manual review focus areas
   - Plan exploit PoC development (Foundry tests)
   - Get user approval before testing

### CODE Phase (Testing)

**Static Analysis:**

1. **Automated Scanning**
   - **Slither:** Comprehensive static analysis
   - **Semgrep:** Pattern-based vulnerability detection
   - **Caracal:** Cairo-specific analysis (Starknet)
   - Document findings

2. **Manual Code Review**
   - Review access control modifiers
   - Analyze state-changing functions
   - Check for CEI pattern violations (reentrancy)
   - Review math operations for overflow/underflow
   - Validate input checks
   - Examine external call patterns

**Symbolic Execution:**
- **Mythril:** Ethereum security scanner
- **Manticore:** Symbolic execution engine
- Identify edge cases and assertion failures

**Fuzzing:**
- **Echidna:** Smart contract fuzzer
- **Foundry Fuzzing:** Property-based testing
- Generate invariant tests
- Test boundary conditions

**Dynamic Testing (Testnet/Mainnet Fork):**

1. **Reentrancy Testing**
   - Test callback points (ERC-777, ERC-721 hooks)
   - Verify CEI pattern enforcement
   - Test cross-contract reentrancy
   - Check read-only reentrancy

2. **Oracle Manipulation Testing**
   - Flash loan + price manipulation simulation
   - Test staleness checks
   - Verify TWAP resistance
   - Test multi-oracle aggregation

3. **Access Control Testing**
   - Test admin function access
   - Attempt ownership takeover
   - Test role hierarchy
   - Verify modifier enforcement

4. **Business Logic Testing**
   - Flash loan attack simulations
   - Liquidation manipulation
   - Governance voting exploits
   - Reward farming exploits

5. **Integration Testing**
   - Test interactions with external protocols
   - Verify cross-chain message handling
   - Test bridge security
   - DEX integration security

**Exploit PoC Development:**
- Write Foundry tests reproducing vulnerabilities
- Use DeFiHackLabs patterns as reference
- Demonstrate impact with concrete examples
- Include setup, exploit, and verification

**Evidence Collection:**
- Foundry/Hardhat test scripts
- Transaction traces showing exploit
- Before/after balance comparisons
- Map findings to Immunefi Top 10

### COMMIT Phase (Reporting)

1. **Findings Documentation**
   - Executive summary
   - Technical findings mapped to Immunefi Top 10
   - Severity ratings (Critical, High, Medium, Low, Informational)
   - Working exploit PoCs (Foundry tests)
   - Impact analysis (potential funds at risk)

2. **Remediation Recommendations**
   - Specific code fixes
   - Reference OpenZeppelin secure patterns
   - Suggest audit scope for code changes
   - Best practices (CEI pattern, ReentrancyGuard, SafeMath)
   - Additional testing recommendations

3. **Framework Integration**
   - Map all findings to Immunefi Top 10 categories
   - Reference DeFiHackLabs similar exploits
   - Include real-world case studies
   - Provide detection strategies

---

## Common Smart Contract Vulnerabilities

### Critical Vulnerabilities
- **Reentrancy:** Unprotected external calls allowing state manipulation
- **Oracle Manipulation:** Flash loan attacks on price feeds
- **Access Control Bypass:** Unauthorized admin function calls
- **Integer Overflow/Underflow:** Math operations without SafeMath (Solidity <0.8.0)
- **Delegatecall to Untrusted Contract:** Arbitrary code execution

### High Severity
- **Front-running:** MEV exploitation opportunities
- **Signature Replay:** Cross-chain signature reuse
- **Uninitialized Proxy:** Implementation selfdestruct risk
- **Flash Loan Attacks:** Manipulation via large temporary capital
- **Governance Attacks:** Flash loan voting power manipulation

### Medium Severity
- **Incorrect Calculation:** Precision loss, rounding errors
- **Input Validation:** Missing bounds checks, overflow in user inputs
- **Gas Limit DoS:** Unbounded loops, high gas operations
- **Block Timestamp Manipulation:** Miner can manipulate timestamp
- **Centralization Risks:** Single admin key controls

### Informational
- **Code Quality:** Unused variables, missing events
- **Gas Optimization:** Inefficient storage patterns
- **Missing Documentation:** Undocumented functions
- **Deprecated Functions:** Use of deprecated Solidity features

---

## Testing Tools

**Static Analysis:**
- Slither (Trail of Bits) - Comprehensive Solidity analyzer
- Semgrep - Pattern-based security scanner
- Solhint - Solidity linter
- Caracal - Cairo smart contract analyzer (Starknet)

**Symbolic Execution:**
- Mythril - Security analysis framework
- Manticore - Symbolic execution engine
- Halmos - Symbolic testing with Foundry

**Fuzzing:**
- Echidna - Smart contract fuzzer
- Foundry - Built-in fuzzing capabilities
- Medusa - Parallelized fuzzer

**Development/Testing Frameworks:**
- Foundry - Fast, portable Ethereum testing framework
- Hardhat - Ethereum development environment
- Truffle - Smart contract development suite

**Formal Verification:**
- Certora - Formal verification platform
- K Framework - Formal specification and verification

**Blockchain Interaction:**
- Ethers.js / Web3.js - JavaScript libraries
- Cast (Foundry) - Command-line Ethereum tool
- Tenderly - Transaction simulation and debugging

---

## Reference Resources

### Local Resources (Dynamic Discovery)

**Web3 Security:** `Glob: resources/library/**/*defi*` or `**/*web3*` or `**/*consensys*` or `**/*smart-contract*`

**Books:** `Glob: resources/library/books/**/*smart-contract*` or `**/*blockchain*`

### Web Resources

**DeFiHackLabs:**
- Repository: https://github.com/SunWeb3Sec/DeFiHackLabs
- Use: Learn from real exploit patterns

**Immunefi Top 10:**
- Website: https://immunefi.com/immunefi-top-10/
- Use: Systematic vulnerability testing

**Additional Resources:**
- OpenZeppelin Contracts: https://docs.openzeppelin.com/contracts/
- Trail of Bits Security Blog: https://blog.trailofbits.com/category/security/
- Secureum: https://secureum.substack.com/

---

**Created:** 2025-12-01
**Framework:** Intelligence Adjacent (IA) - Security Testing
**Version:** 1.0
