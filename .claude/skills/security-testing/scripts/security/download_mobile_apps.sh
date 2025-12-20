#!/usr/bin/env bash
# Mobile App Download Helper Script
# Downloads iOS (.ipa) and Android (.apk) files for security testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VPS_HOST="root@72.60.27.87"
VPS_KEY="C:\Users\Chris\.ssh\gro_256"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 [ios|android] <app-identifier> <output-directory>"
    echo ""
    echo "Download mobile apps for security testing"
    echo ""
    echo "Examples:"
    echo "  $0 ios 914172636 ./00-scope/binaries"
    echo "  $0 android com.formagrid.airtable ./00-scope/binaries"
    echo ""
    echo "iOS Requirements:"
    echo "  - Apple ID credentials (will prompt interactively)"
    echo "  - App ID from iTunes URL (e.g., 914172636)"
    echo ""
    echo "Android Requirements:"
    echo "  - Package ID (e.g., com.formagrid.airtable)"
    echo "  - No authentication needed"
    exit 1
}

download_ios_app() {
    local app_id="$1"
    local output_dir="$2"

    echo -e "${BLUE}[*] Downloading iOS app: ${app_id}${NC}"
    echo -e "${YELLOW}[!] This requires Apple ID credentials${NC}"
    echo ""

    # Check if ipatool is installed on VPS
    echo -e "${BLUE}[*] Checking ipatool installation on VPS...${NC}"
    ssh -i "$VPS_KEY" "$VPS_HOST" "which ipatool > /dev/null 2>&1" || {
        echo -e "${RED}[-] ipatool not installed on VPS${NC}"
        echo -e "${BLUE}[*] Installing ipatool...${NC}"
        ssh -i "$VPS_KEY" "$VPS_HOST" "cd /tmp && curl -L -o ipatool-linux.tar.gz https://github.com/majd/ipatool/releases/download/v2.2.0/ipatool-2.2.0-linux-amd64.tar.gz && tar -xzf ipatool-linux.tar.gz && mv bin/ipatool-2.2.0-linux-amd64 /usr/local/bin/ipatool && chmod +x /usr/local/bin/ipatool"
        echo -e "${GREEN}[+] ipatool installed successfully${NC}"
    }

    echo -e "${BLUE}[*] Authenticating with Apple ID...${NC}"
    echo -e "${YELLOW}[!] You will be prompted for your Apple ID and password${NC}"
    ssh -i "$VPS_KEY" "$VPS_HOST" "ipatool auth login"

    echo -e "${BLUE}[*] Downloading app...${NC}"
    ssh -i "$VPS_KEY" "$VPS_HOST" "cd /tmp && ipatool download --bundle-identifier $app_id --purchase"

    # Find the downloaded IPA file
    ipa_file=$(ssh -i "$VPS_KEY" "$VPS_HOST" "ls -t /tmp/*.ipa 2>/dev/null | head -1")

    if [ -z "$ipa_file" ]; then
        echo -e "${RED}[-] Failed to download IPA file${NC}"
        return 1
    fi

    echo -e "${GREEN}[+] Downloaded: $ipa_file${NC}"

    # Copy back to Windows
    local output_file="$output_dir/$(basename "$ipa_file")"
    echo -e "${BLUE}[*] Copying to Windows: $output_file${NC}"
    scp -i "$VPS_KEY" "$VPS_HOST:$ipa_file" "$output_file"

    # Cleanup VPS
    ssh -i "$VPS_KEY" "$VPS_HOST" "rm -f $ipa_file"

    echo -e "${GREEN}[+] iOS app downloaded successfully: $output_file${NC}"
    return 0
}

download_android_app() {
    local package_id="$1"
    local output_dir="$2"

    echo -e "${BLUE}[*] Downloading Android APK: ${package_id}${NC}"
    echo ""
    echo -e "${YELLOW}[!] Manual download required from APK mirror sites${NC}"
    echo ""
    echo "Recommended sources (in order of preference):"
    echo "  1. APKPure: https://apkpure.net/$package_id"
    echo "  2. APKMirror: https://www.apkmirror.com/"
    echo "  3. Google Play Store (requires authentication)"
    echo ""
    echo -e "${BLUE}Steps:${NC}"
    echo "  1. Visit one of the above URLs"
    echo "  2. Download the latest version"
    echo "  3. Save to: $output_dir/"
    echo "  4. Rename to: $package_id.apk"
    echo ""
    echo -e "${YELLOW}[!] Verify APK signature after download${NC}"
    echo "  Command: apksigner verify --verbose <apk-file>"
    echo ""
    return 0
}

# Main script logic
if [ $# -lt 3 ]; then
    usage
fi

PLATFORM="$1"
APP_ID="$2"
OUTPUT_DIR="$3"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

case "$PLATFORM" in
    ios)
        download_ios_app "$APP_ID" "$OUTPUT_DIR"
        ;;
    android)
        download_android_app "$APP_ID" "$OUTPUT_DIR"
        ;;
    *)
        echo -e "${RED}[-] Invalid platform: $PLATFORM${NC}"
        usage
        ;;
esac
