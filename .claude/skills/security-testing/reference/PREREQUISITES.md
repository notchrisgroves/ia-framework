# Security Testing Prerequisites

**Tool installation requirements for specialized testing engagements**

---

## Standard Pentesting (Always Available)

**Kali Pentest Container:**
- ✅ Deployed on VPS (configured via .env)
- ✅ Available immediately via VPS Code API wrappers
- ✅ No additional setup required

**Tools:**
- nmap, nuclei, httpx, subfinder, katana, naabu
- sqlmap, wapiti, wpscan, nikto, dirb
- hydra, crackmapexec, searchsploit, responder, netcat, cvemap

---

## Starknet / Blockchain Smart Contract Testing

### ⚠️ MANDATORY SETUP REQUIRED

**You MUST complete these steps BEFORE starting any Starknet pentest:**

**📚 Complete Documentation:**
- **Official Starknet Devnet Docs:** https://0xspaceshard.github.io/starknet-devnet/docs/forking
- **VPS Code API Architecture:** `../../servers/ARCHITECTURE.md`
- **Tool Inventory:** `../infrastructure-ops/analysis/VPS-TOOL-INVENTORY.md`

### Step 1: Install starknet-devnet

```powershell
cargo install starknet-devnet --version 0.5.0
```

**Verify installation:**
```powershell
starknet-devnet --version
# Should output: starknet-devnet 0.5.0
```

### Step 2: Start Forked Devnet

**⚠️ This MUST run in a SEPARATE terminal during the entire engagement:**

```powershell
# Get your Starknet RPC endpoint (Infura, Alchemy, or Blast)
# DO NOT use the placeholder - get actual API key from user!

# Fork mainnet at latest block
starknet-devnet --fork-network https://starknet-mainnet.g.alchemy.com/v2/YOUR-API-KEY

# OR fork at specific block
starknet-devnet --fork-network https://starknet-mainnet.g.alchemy.com/v2/YOUR-API-KEY --fork-block 500000
```

**Expected output:**
```
 * Running on http://127.0.0.1:5050
 * Forking network: https://starknet-mainnet.g.alchemy.com/v2/...
 * Fork block: latest
```

### Step 3: Verify Devnet is Running

**Before proceeding, verify connectivity:**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5050/is_alive
```

**Expected:** `200 OK` response

### Step 4: Use Starknet Code API Wrappers

**Now you can use the Starknet testing tools:**

```python
# Connect to devnet
start_fork(
    devnet_url="http://127.0.0.1:5050",
    engagement_dir=engagement_path
)

# Create test account
create_account(engagement_dir=engagement_path)

# Test contract calls
call_contract(
    address="0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
    function="balanceOf",
    calldata='["0x123..."]',
    engagement_dir=engagement_path
)

# Execute exploit
invoke_contract(
    address=target_contract,
    function=exploit_function,
    calldata=exploit_payload,
    engagement_dir=engagement_path
)

# Verify impact
get_storage(
    address=target_contract,
    key=storage_slot,
    engagement_dir=engagement_path
)

# Reset for new scenario
reset_fork()
```

---

## Mobile Application Testing

**Mobile Security Container:**
- ✅ Deployed on VPS (configured via .env)
- ✅ Available immediately via VPS Code API wrappers
- ✅ No additional setup required

**Tools:**
- apktool, jadx, androguard, apksigner, aapt, apkleaks, frida, objection

**For dynamic analysis with frida/objection:**
- Requires connected Android device or emulator
- USB debugging enabled
- See mobile security engagement workflow

---

## Web3 / Ethereum Smart Contract Testing

**Web3 Security Container:**
- ✅ Deployed on VPS (configured via .env)
- ✅ Available immediately via VPS Code API wrappers
- ✅ No additional setup required

**Cairo Security Tools:**
- ✅ Deployed on VPS (configured via .env)
- ✅ Available immediately via VPS Code API wrappers
- ✅ No additional setup required

**Tools:**
- Solidity: slither, mythril, semgrep, echidna, halmos
- Cairo: caracal, thoth, amarna
- Testing: forge, brownie
- Blockchain: cast (5 tools), solc (3 tools)

**For mainnet interaction (via cast tools):**
- Requires RPC endpoint (Infura, Alchemy)
- Get from user if needed

---

## API Security Testing (Reaper)

**Reaper Proxy (HTTP Interceptor):**
- ⚠️ Requires local Reaper binary running
- See `../infrastructure-ops/runbooks/REAPER-ARCHITECTURE.md`

**Setup:**
1. Build Reaper locally (one-time): `cd ../mcp-server-create/reaper-source/ && make build`
2. Run Reaper during engagement: `./reaper`
3. Configure browser proxy to Reaper (localhost:8080)
4. Database analysis via direct SQLite queries

---

## Troubleshooting

### Starknet Devnet Not Running

**Error:** "Could not connect to devnet at http://127.0.0.1:5050"

**Solution:**
```powershell
# Check if devnet is running
Invoke-RestMethod -Uri http://127.0.0.1:5050/is_alive

# If not running, start it
starknet-devnet --fork-network https://starknet-mainnet.g.alchemy.com/v2/YOUR-KEY

# Check for port conflicts
lsof -i :5050  # Linux/Mac
netstat -ano | findstr :5050  # Windows
```

### starknet-devnet Not Installed

**Error:** "starknet-devnet: command not found"

**Solution:**
```powershell
# Install via cargo
cargo install starknet-devnet --version 0.5.0

# Verify installation
which starknet-devnet
starknet-devnet --version
```

### RPC Connection Timeout

**Error:** "Connection timeout to RPC endpoint"

**Solutions:**
1. Verify API key is valid
2. Check network connectivity
3. Try different RPC provider:
   - Infura: `https://starknet-mainnet.infura.io/v3/YOUR-KEY`
   - Alchemy: `https://starknet-mainnet.g.alchemy.com/v2/YOUR-KEY`
   - Blast: `https://starknet-mainnet.blastapi.io/YOUR-KEY`

---

## Quick Reference

| Testing Type | Prerequisites | Status |
|--------------|---------------|--------|
| Standard Pentest | None | ✅ Ready |
| Mobile Security | None (APK only) | ✅ Ready |
| Web3 Ethereum | None | ✅ Ready |
| Cairo Security | None | ✅ Ready |
| **Starknet** | **starknet-devnet + RPC** | ⚠️ **SETUP REQUIRED** |
| Reaper API | Local binary | ⚠️ Setup required |

---

**Last Updated:** 2025-11-10
**For:** Security-Tester Agent
