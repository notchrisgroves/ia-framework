#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apkleaks wrapper - Hardcoded secrets scanner for APK files"""
import sys
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def apkleaks_scan(
    apk_path: str,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Scan APK for hardcoded secrets, API keys, and sensitive URLs using apkleaks.

    Token efficiency:
    - Minimal mode: ~100 tokens (secret count by type, severity summary)
    - Standard mode: ~300 tokens (sample findings, URLs, API keys)
    - Full mode: ~1000 tokens (all findings with context)
    - No caching (unique per APK)

    Args:
        apk_path: Path to APK file
        engagement_dir: Optional engagement directory
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputFile, and message
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    apk_name = Path(apk_path).stem

    # Determine output location
    if engagement_dir:
        output_dir = Path(engagement_dir) / "04-analysis" / "apkleaks"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "apkleaks"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{apk_name}-{timestamp}.json"

    # Execute apkleaks
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "apkleaks", "-f", f"/data/{Path(apk_path).name}",
             "--json"],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Parse JSON output
        try:
            findings = json.loads(result["stdout"]) if result["stdout"] else []
        except json.JSONDecodeError:
            findings = []

        # Save full output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=2)

        # Parse findings
        summary = _parse_findings(findings, detail_level)

        message = f"[+] APK secrets scan complete\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Secrets found: {summary.get('totalFindings', 0)}\n"
        message += f"    API keys: {summary.get('apiKeyCount', 0)}\n"
        message += f"    URLs: {summary.get('urlCount', 0)}\n"
        message += f"    Full report: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "apkleaks scan timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_findings(findings: list, detail_level: str) -> Dict:
    """Parse apkleaks findings."""
    if not findings:
        return {"totalFindings": 0, "apiKeyCount": 0, "urlCount": 0}

    # Categorize findings
    api_keys = [f for f in findings if "api" in str(f).lower() or "key" in str(f).lower()]
    urls = [f for f in findings if "http" in str(f).lower()]
    credentials = [f for f in findings if any(kw in str(f).lower() for kw in ["password", "secret", "token", "credential"])]

    # Minimal: Just counts
    if detail_level == "minimal":
        return {
            "totalFindings": len(findings),
            "apiKeyCount": len(api_keys),
            "urlCount": len(urls),
            "credentialCount": len(credentials)
        }

    # Standard: Add samples
    elif detail_level == "standard":
        return {
            "totalFindings": len(findings),
            "apiKeyCount": len(api_keys),
            "urlCount": len(urls),
            "credentialCount": len(credentials),
            "sampleAPIKeys": api_keys[:3],
            "sampleURLs": urls[:5]
        }

    # Full: Complete findings
    else:
        return {
            "totalFindings": len(findings),
            "apiKeyCount": len(api_keys),
            "urlCount": len(urls),
            "credentialCount": len(credentials),
            "apiKeys": api_keys,
            "urls": urls,
            "credentials": credentials,
            "allFindings": findings[:50]  # Limit to 50 findings
        }

if __name__ == "__main__":
    result = apkleaks_scan(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
