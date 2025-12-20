#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aapt wrapper - APK metadata extraction"""
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.vps_utils import docker_exec

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def aapt_dump(
    apk_path: str,
    dump_type: str = "badging",
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Extract APK metadata and manifest information using aapt.

    Token efficiency:
    - Minimal mode: ~80 tokens (package name, version, SDK versions)
    - Standard mode: ~200 tokens (+ permissions, activities)
    - Full mode: ~500 tokens (complete badging output)
    - No caching (unique per APK)

    Args:
        apk_path: Path to APK file
        dump_type: aapt dump type (badging, permissions, configurations, resources)
        engagement_dir: Optional engagement directory
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputFile, and message
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    apk_name = Path(apk_path).stem

    # Determine output location
    if engagement_dir:
        output_dir = Path(engagement_dir) / "04-analysis" / "aapt"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "aapt"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{apk_name}-{dump_type}-{timestamp}.txt"

    # Execute aapt
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "aapt", "dump", dump_type, f"/data/{Path(apk_path).name}"],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Save full output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["stdout"])

        # Parse metadata
        summary = _parse_aapt_output(result["stdout"], dump_type, detail_level)

        message = f"[+] AAPT metadata extraction complete\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Package: {summary.get('package', 'unknown')}\n"
        message += f"    Version: {summary.get('versionName', 'unknown')}\n"
        message += f"    Full output: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "aapt dump timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_aapt_output(output: str, dump_type: str, detail_level: str) -> Dict:
    """Parse aapt dump output."""
    lines = output.split('\n')

    if dump_type == "badging":
        # Extract package info
        package = None
        version_code = None
        version_name = None
        sdk_version = None
        target_sdk = None

        for line in lines:
            if line.startswith("package:"):
                parts = line.split()
                for part in parts:
                    if part.startswith("name="):
                        package = part.split("=", 1)[1].strip("'\"")
                    elif part.startswith("versionCode="):
                        version_code = part.split("=", 1)[1].strip("'\"")
                    elif part.startswith("versionName="):
                        version_name = part.split("=", 1)[1].strip("'\"")
            elif line.startswith("sdkVersion:"):
                sdk_version = line.split(":", 1)[1].strip().strip("'\"")
            elif line.startswith("targetSdkVersion:"):
                target_sdk = line.split(":", 1)[1].strip().strip("'\"")

        # Minimal: Basic metadata
        if detail_level == "minimal":
            return {
                "package": package,
                "versionCode": version_code,
                "versionName": version_name,
                "sdkVersion": sdk_version,
                "targetSdkVersion": target_sdk
            }

        # Standard: Add permissions and activities
        elif detail_level == "standard":
            permissions = [line.split(":", 1)[1].strip().strip("'\"") for line in lines if line.startswith("uses-permission:")]
            activities = [line for line in lines if "activity" in line.lower()][:5]

            return {
                "package": package,
                "versionCode": version_code,
                "versionName": version_name,
                "sdkVersion": sdk_version,
                "targetSdkVersion": target_sdk,
                "permissionCount": len(permissions),
                "topPermissions": permissions[:10],
                "activityCount": len(activities)
            }

        # Full: Complete badging data
        else:
            return {
                "package": package,
                "versionCode": version_code,
                "versionName": version_name,
                "sdkVersion": sdk_version,
                "targetSdkVersion": target_sdk,
                "rawOutput": output[:2000]  # First 2000 chars
            }

    else:
        # Other dump types - return raw with length limit
        return {
            "dumpType": dump_type,
            "lineCount": len(lines),
            "preview": '\n'.join(lines[:20]) if detail_level != "minimal" else None
        }

if __name__ == "__main__":
    import json
    result = aapt_dump(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
