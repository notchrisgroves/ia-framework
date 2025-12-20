#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""androguard wrapper - Static analysis for APK files"""
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

def androguard_analyze(
    apk_path: str,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Perform static analysis on APK using androguard.

    Token efficiency:
    - Minimal mode: ~150 tokens (permission count, activity count, critical findings)
    - Standard mode: ~400 tokens (permission list, top activities/services)
    - Full mode: ~1200 tokens (detailed permissions, activities, security issues)
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
        output_dir = Path(engagement_dir) / "04-analysis" / "androguard"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "androguard"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{apk_name}-{timestamp}.json"

    # Execute androguard analysis via MCP
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "python", "-c",
             f"from androguard.misc import AnalyzeAPK; import json; a,d,dx = AnalyzeAPK('/data/{Path(apk_path).name}'); print(json.dumps({{'permissions': a.get_permissions(), 'activities': a.get_activities(), 'services': a.get_services(), 'package': a.get_package()}}))"],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Save full output
        analysis_data = json.loads(result["stdout"]) if result["stdout"] else {}
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2)

        # Parse based on detail level
        summary = _parse_analysis(analysis_data, detail_level)

        message = f"[+] Androguard analysis complete\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Permissions: {summary.get('permissionCount', 0)}\n"
        message += f"    Activities: {summary.get('activityCount', 0)}\n"
        message += f"    Services: {summary.get('serviceCount', 0)}\n"
        message += f"    Full analysis: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "androguard analysis timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_analysis(data: Dict, detail_level: str) -> Dict:
    """Parse androguard analysis results."""
    permissions = data.get("permissions", [])
    activities = data.get("activities", [])
    services = data.get("services", [])
    package = data.get("package", "unknown")

    # Minimal: Just counts + dangerous permissions
    if detail_level == "minimal":
        dangerous = [p for p in permissions if "DANGEROUS" in p or "INTERNET" in p or "WRITE" in p]
        return {
            "package": package,
            "permissionCount": len(permissions),
            "activityCount": len(activities),
            "serviceCount": len(services),
            "dangerousPermissionCount": len(dangerous)
        }

    # Standard: Add lists (limited)
    elif detail_level == "standard":
        dangerous = [p for p in permissions if "DANGEROUS" in p or "INTERNET" in p or "WRITE" in p]
        return {
            "package": package,
            "permissionCount": len(permissions),
            "activityCount": len(activities),
            "serviceCount": len(services),
            "dangerousPermissions": dangerous[:10],
            "topActivities": activities[:5],
            "topServices": services[:5]
        }

    # Full: Complete lists
    else:
        dangerous = [p for p in permissions if "DANGEROUS" in p or "INTERNET" in p or "WRITE" in p]
        return {
            "package": package,
            "permissionCount": len(permissions),
            "activityCount": len(activities),
            "serviceCount": len(services),
            "permissions": permissions,
            "dangerousPermissions": dangerous,
            "activities": activities,
            "services": services
        }

if __name__ == "__main__":
    result = androguard_analyze(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
