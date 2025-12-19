#!/usr/bin/env bash
#
# Pre-Commit Hook: Block Infrastructure Leaks
#
# Purpose: Prevent commits containing sensitive infrastructure details
# Triggers: git commit (runs before commit is created)
# Exit codes: 0 = allow commit, 1 = block commit
#
# Blocked patterns:
# - IP addresses (except safe documentation ranges)
# - VPS hostnames
# - SSH credentials (keys, usernames, ports)
# - Provider-specific identifiers
#
# Safe patterns (allowed):
# - Private IP ranges: 192.168.x.x, 10.x.x.x, 172.16-31.x.x
# - Documentation IPs: 192.0.2.x (TEST-NET-1), 198.51.100.x (TEST-NET-2), 203.0.113.x (TEST-NET-3)
# - Localhost: 127.0.0.1, ::1
# - Generic examples: example.com, example.org
#
# Created: 2025-12-15
# Updated: Auto-maintained by framework

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[Pre-Commit]${NC} Scanning for infrastructure leaks..."

# Get list of staged files (only text files: .md, .yaml, .json, .ts, .py, etc.)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(md|yaml|yml|json|ts|js|py|sh|txt)$' || true)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}[Pre-Commit]${NC} No text files staged - skipping infrastructure leak check"
    exit 0
fi

LEAK_FOUND=0

# Pattern 1: IP addresses (excluding safe ranges)
echo -n "  Checking for IP addresses... "
for file in $STAGED_FILES; do
    # Find all IP addresses
    IPS=$(grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$file" 2>/dev/null || true)

    if [ -n "$IPS" ]; then
        while IFS= read -r ip; do
            # Skip safe IP ranges
            if [[ "$ip" =~ ^192\.168\. ]] || \
               [[ "$ip" =~ ^10\. ]] || \
               [[ "$ip" =~ ^172\.(1[6-9]|2[0-9]|3[01])\. ]] || \
               [[ "$ip" =~ ^127\. ]] || \
               [[ "$ip" =~ ^192\.0\.2\. ]] || \
               [[ "$ip" =~ ^198\.51\.100\. ]] || \
               [[ "$ip" =~ ^203\.0\.113\. ]] || \
               [[ "$ip" =~ ^0\.0\.0\.0$ ]]; then
                continue
            fi

            # Public IP found - potential leak
            echo -e "\n${RED}[BLOCKED]${NC} Public IP address found: $ip"
            echo "  File: $file"
            grep -n "$ip" "$file" | head -3
            LEAK_FOUND=1
        done <<< "$IPS"
    fi
done
if [ $LEAK_FOUND -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
fi

# Pattern 2: VPS hostnames (hstgr.cloud, ovh.us, vps.ovh.*)
echo -n "  Checking for VPS hostnames... "
for file in $STAGED_FILES; do
    if grep -qE '(hstgr\.cloud|vps\.ovh|ovh\.us)' "$file" 2>/dev/null; then
        # Check if it's an environment variable reference
        if ! grep -qE '\$\{.*VPS.*\}' "$file" 2>/dev/null; then
            echo -e "\n${RED}[BLOCKED]${NC} VPS hostname found in: $file"
            grep -nE '(hstgr\.cloud|vps\.ovh|ovh\.us)' "$file" | head -3
            LEAK_FOUND=1
        fi
    fi
done
if [ $LEAK_FOUND -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
fi

# Pattern 3: SSH key paths (hardcoded)
echo -n "  Checking for hardcoded SSH keys... "
for file in $STAGED_FILES; do
    if grep -qE '(~/.ssh/gro_256|C:\\\\Users\\\\Chris\\\\.ssh)' "$file" 2>/dev/null; then
        # Check if it's an environment variable reference or .env file
        if ! grep -qE '(\$\{.*SSH.*\}|^SSH_PRIV=|# \.env file)' "$file" 2>/dev/null; then
            echo -e "\n${RED}[BLOCKED]${NC} Hardcoded SSH key path found in: $file"
            grep -nE '(~/.ssh/gro_256|C:\\\\Users\\\\Chris\\\\.ssh)' "$file" | head -3
            LEAK_FOUND=1
        fi
    fi
done
if [ $LEAK_FOUND -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
fi

# Pattern 4: SSH connection strings (debian@IP, root@IP, groves@hostname)
echo -n "  Checking for SSH connection strings... "
for file in $STAGED_FILES; do
    if grep -qE 'ssh.*(@[0-9]+\.[0-9]+\.|debian@|root@|groves@)' "$file" 2>/dev/null; then
        # Check if it's a variable reference, example, or .env file
        if ! grep -qE '(\$\{|example\.com|# \.env file|Documentation|Example:)' "$file" 2>/dev/null; then
            echo -e "\n${RED}[BLOCKED]${NC} SSH connection string found in: $file"
            grep -nE 'ssh.*(@[0-9]+\.[0-9]+\.|debian@|root@|groves@)' "$file" | head -3
            LEAK_FOUND=1
        fi
    fi
done
if [ $LEAK_FOUND -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
fi

# Final result
if [ $LEAK_FOUND -eq 1 ]; then
    echo ""
    echo -e "${RED}[COMMIT BLOCKED]${NC} Infrastructure leaks detected!"
    echo ""
    echo "Infrastructure details (IPs, hostnames, SSH keys) must be stored in .env file."
    echo ""
    echo "Fix options:"
    echo "  1. Move sensitive values to .env file (recommended)"
    echo "  2. Use environment variable references: \${OVHCLOUD_VPS_IP}"
    echo "  3. Replace with generic placeholders: example.com, 192.0.2.1"
    echo ""
    echo "See: .env file for infrastructure configuration"
    echo "See: docs/CREDENTIAL-HANDLING-ENFORCEMENT.md for security policy"
    exit 1
fi

echo -e "${GREEN}[Pre-Commit]${NC} No infrastructure leaks detected - commit allowed"
exit 0
