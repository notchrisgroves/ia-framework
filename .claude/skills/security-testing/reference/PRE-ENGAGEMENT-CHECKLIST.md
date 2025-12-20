# Pre-Engagement Checklist - Security Testing

**Purpose:** Verify ALL requirements before starting any security engagement
**When to use:** BEFORE creating engagement directory or planning tests
**Time investment:** 30-60 minutes upfront (saves 5-10+ hours later)

---

## ✅ Phase 1: Scope & Assets Verification (MANDATORY)

### 1.1 Scope Documentation
- [ ] SCOPE.md or equivalent provided by program
- [ ] Clear in-scope assets list (contracts, hosts, URLs)
- [ ] Clear out-of-scope restrictions documented
- [ ] Testing methodology constraints (local fork required? read-only mainnet allowed?)
- [ ] PoC requirements clarified (all severities? high/critical only?)
- [ ] Attack scenarios examples provided

### 1.2 Asset Inventory Completeness
- [ ] Contract addresses provided AND verified to exist on chain
- [ ] Source code repository links provided
- [ ] Documentation links (technical docs, architecture diagrams)
- [ ] Known issues / previous audit reports referenced
- [ ] Deployment information (network, block numbers, versions)

**RED FLAG:** If scope doc says "test these 5 contracts" but provides zero source code or ABIs → STOP

---

## ✅ Phase 2: Source Code & ABI Access (CRITICAL)

### 2.1 Smart Contract Engagements
- [ ] **Source code files present** in provided repository
  - [ ] Verify files match in-scope contract addresses
  - [ ] Check commit hash matches deployed version
  - [ ] Compile locally to confirm it works
- [ ] **ABIs available** via one of:
  - [ ] Included in repository (artifacts/ or build/ directory)
  - [ ] Downloadable from block explorer (verify 403/rate limits)
  - [ ] Provided separately by program
- [ ] **Function signatures documented**
  - [ ] Can we identify privileged functions?
  - [ ] Do we know expected authorization patterns?

**If ABIs NOT available:**
- [ ] Can we generate selectors manually? (test this)
- [ ] Can we use block explorer APIs? (test API access)
- [ ] FALLBACK: Ask program to provide ABIs before starting

### 2.2 Web/API Engagements
- [ ] API documentation provided (OpenAPI/Swagger preferred)
- [ ] Authentication mechanism documented
- [ ] Test accounts provided (or can create freely)
- [ ] Rate limiting documented

### 2.3 Infrastructure Engagements
- [ ] Network diagrams provided
- [ ] IP ranges / CIDR blocks documented
- [ ] Access credentials provided (VPN, SSH keys, etc.)
- [ ] Firewall rules documented

---

## ✅ Phase 3: Testing Environment Setup (TEST BEFORE COMMITTING)

### 3.1 Local Devnet / Testnet Setup
- [ ] **Test the fork setup** with a simple contract FIRST
  - [ ] Can devnet reach external RPC endpoints?
  - [ ] Does the devnet version support the Cairo/Solidity version used?
  - [ ] Can we make read calls successfully?
  - [ ] Can we make write calls (invoke transactions)?
- [ ] **Predeployed accounts** accessible
  - [ ] Can we get account addresses and private keys?
  - [ ] Can we sign transactions?
- [ ] **Network connectivity** verified
  - [ ] Docker → External RPC (if using Docker)
  - [ ] VPS → External RPC (if using VPS)
  - [ ] Local → Devnet endpoint

**CRITICAL:** Spend 15-30 minutes testing the SIMPLEST possible transaction before planning complex test scenarios

### 3.2 Tooling Compatibility Check
- [ ] SDK version supports contract version (starknet-py, ethers.js, web3.py)
  - [ ] Test imports work
  - [ ] Test basic contract interaction
  - [ ] Test selector calculation (if needed)
- [ ] CLI tools installed and functional
  - [ ] starknet CLI / cast / hardhat
  - [ ] Version check (`--version` works)
- [ ] No known packaging bugs in current versions
  - [ ] Check GitHub issues for blockers
  - [ ] Test file paths resolve correctly

### 3.3 MCP Tool Validation (if using)
- [ ] MCP server installed and running
- [ ] Test call to simplest tool works
- [ ] Verify output format is usable
- [ ] Check token usage is acceptable

---

## ✅ Phase 4: Engagement Feasibility Assessment

### 4.1 Time & Resource Estimate
- [ ] Infrastructure setup estimated time: _____ hours
- [ ] Testing estimated time: _____ hours
- [ ] Total estimated time: _____ hours
- [ ] **Is this realistic given bounty payout range?**
  - Low severity: $______
  - High severity: $______
  - Critical severity: $______

### 4.2 Blocker Assessment
Count the number of "NO" or "UNKNOWN" answers above:
- **0-2:** Good to proceed ✅
- **3-5:** High risk - address blockers first ⚠️
- **6+:** DO NOT START - too many unknowns 🛑

### 4.3 Go/No-Go Decision
- [ ] **GO:** All critical items verified, setup tested, realistic timeline
- [ ] **NO-GO:** Document missing items, request from program, wait for clarity

---

## ✅ Phase 5: Documentation Before Starting

### 5.1 Create Engagement Structure
```
engagements/pentests/[program-name-YYYY-MM]/
├── 00-scope/
│   ├── SCOPE.md (from program)
│   ├── PRE-ENGAGEMENT-CHECKLIST.md (this file, filled out)
│   └── GO-DECISION.md (why we're starting or why we're pausing)
├── 01-inventory/
│   ├── CONTRACTS.md (addresses, ABIs, source locations)
│   ├── ENDPOINTS.md (API endpoints, hosts)
│   └── CREDENTIALS.md (test accounts, keys - GITIGNORE)
├── 02-reconnaissance/
├── 03-analysis/
├── 04-exploitation/
├── 05-findings/
└── SESSION-NOTES.md
```

### 5.2 Session 0 Documentation
Create a **SESSION-0-PREFLIGHT.md** file documenting:
- [ ] What was verified
- [ ] What tools were tested
- [ ] Any warnings or limitations discovered
- [ ] Estimated timeline
- [ ] Go/No-Go decision rationale

---

## 🚨 RED FLAGS - STOP IMMEDIATELY

**If you encounter ANY of these, PAUSE the engagement:**

1. ❌ **"Test these 10 contracts"** but zero source code provided
2. ❌ **ABIs not accessible** via any method (repo, explorer, APIs)
3. ❌ **Devnet fork fails** after 2 hours of troubleshooting
4. ❌ **SDK has critical bug** blocking core functionality
5. ❌ **Scope says "local fork required"** but RPC unreachable or devnet incompatible
6. ❌ **Documentation is stub** ("Coming soon", placeholder text)
7. ❌ **No response from program** after asking for missing materials (48+ hours)

**Action:** Document the blocker, notify program, request missing items, PAUSE until resolved

---

## 📊 Lessons Learned: Paradex Engagement (2025-11-10/11)

**What went wrong:**
- Started engagement with only SCOPE.md and deployed contract addresses
- Assumed we could get ABIs from explorers (both returned 403)
- Assumed starknet-py would work (v0.28.0 has packaging bug)
- Assumed devnet fork would work (5+ blockers across 7 hours)
- **Result:** 7 hours, 96k tokens, ZERO functions tested

**What we SHOULD have done:**
1. Verify source code repository contains Paraclear/Registry/Oracle contracts (it didn't - only StarkGate bridge)
2. Test ABI extraction from Voyager/Starkscan BEFORE starting (both 403)
3. Test devnet fork with simple contract FIRST (would have caught Docker networking issue)
4. Check starknet-py GitHub issues (would have seen v0.28.0 bug reports)
5. Estimate: "This will take 10+ hours of infrastructure work before ANY testing"
6. Decision: "ROI doesn't justify time investment, request better materials from program"

**Cost of not doing preflight:**
- Time wasted: 7 hours
- Tokens wasted: 96k (48% of budget)
- Findings: 0
- Frustration: High
- Opportunity cost: Could have tested 2-3 EVM programs in same time

---

## ✅ Checklist Template (Copy-Paste for New Engagements)

```markdown
# Pre-Engagement Checklist - [Program Name]
**Date:** YYYY-MM-DD
**Bounty Platform:** HackerOne / Immunefi / Bugcrowd / etc
**Program:** [Name]

## Phase 1: Scope & Assets ✅❌
- [ ] SCOPE.md reviewed
- [ ] Asset list complete
- [ ] Testing constraints clear
- [ ] PoC requirements clear

## Phase 2: Source Code & ABIs ✅❌
- [ ] Source code accessible
- [ ] Source matches deployed contracts
- [ ] ABIs available (source: _____)
- [ ] Function signatures documented

## Phase 3: Environment Setup ✅❌
- [ ] Devnet fork tested (15 min test successful)
- [ ] SDK compatibility verified
- [ ] Network connectivity verified
- [ ] Can calculate selectors / interact with contracts

## Phase 4: Feasibility ✅❌
- [ ] Estimated time: _____ hours
- [ ] Payout range justifies time: YES / NO
- [ ] Blocker count: _____ (max 2 acceptable)

## Phase 5: Go/No-Go Decision
- **Decision:** GO / NO-GO
- **Rationale:** _____
- **Start Date:** YYYY-MM-DD or "PAUSED - awaiting [X]"
```

---

## 🎯 Success Metrics

**Good preflight check:**
- 30-60 minutes invested upfront
- All items verified before Session 1
- Infrastructure setup completes in <2 hours
- Testing begins within 3 hours of engagement start

**Bad preflight check:**
- Jumped straight to testing
- Discovered blockers 5+ hours in
- Multiple pivot points
- No testing after 7+ hours

---

**REMEMBER:** An hour of preflight verification saves ten hours of frustrated debugging.
