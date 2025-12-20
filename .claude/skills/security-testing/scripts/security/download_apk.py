#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download Android APK files from APKPure mirror
"""

import sys
import io
import requests
from bs4 import BeautifulSoup
import re

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def download_apk(package_id, output_path):
    """
    Download APK from APKPure by package ID

    Args:
        package_id: Android package identifier (e.g., com.formagrid.airtable)
        output_path: Where to save the APK file
    """
    print(f"[+] Downloading APK for: {package_id}")

    # APKPure download URL format
    apkpure_url = f"https://apkpure.net/{package_id}"

    try:
        # Get the page
        print(f"[+] Fetching: {apkpure_url}")
        response = requests.get(apkpure_url, timeout=30)
        response.raise_for_status()

        # Parse HTML to find download link
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for download button/link
        download_link = None
        for link in soup.find_all('a', href=True):
            if 'download' in link.get('href', '').lower():
                download_link = link['href']
                break

        if not download_link:
            print("[-] Could not find download link on page")
            return False

        # Make sure it's a full URL
        if not download_link.startswith('http'):
            download_link = f"https://apkpure.net{download_link}"

        print(f"[+] Download URL: {download_link}")

        # Download the APK
        print(f"[+] Downloading APK file...")
        apk_response = requests.get(download_link, stream=True, timeout=120)
        apk_response.raise_for_status()

        # Save to file
        with open(output_path, 'wb') as f:
            for chunk in apk_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[+] APK saved to: {output_path}")
        return True

    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_apk.py <package_id> <output_path>")
        print("Example: python download_apk.py com.formagrid.airtable airtable.apk")
        sys.exit(1)

    package_id = sys.argv[1]
    output_path = sys.argv[2]

    success = download_apk(package_id, output_path)
    sys.exit(0 if success else 1)
