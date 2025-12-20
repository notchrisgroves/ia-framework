#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apktool wrapper - APK decompilation with resource extraction"""
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

def apktool_decode(
    apk_path: str,
    output_dir: Optional[str] = None,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Decompile APK using apktool to extract resources and smali code.

    Token efficiency:
    - Minimal mode: ~100 tokens (file counts, directory structure summary)
    - Standard mode: ~300 tokens (detailed file listing)
    - Full mode: ~1000 tokens (includes sample file contents)
    - No caching (unique per APK)

    Args:
        apk_path: Path to APK file
        output_dir: Optional output directory name (defaults to APK name)
        engagement_dir: Optional engagement directory for organized storage
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputPath, and message
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    apk_name = Path(apk_path).stem

    # Determine base directory
    if engagement_dir:
        base_dir = Path(engagement_dir) / "04-analysis" / "apktool"
    else:
        base_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "apktool"

    base_dir.mkdir(parents=True, exist_ok=True)

    # Output directory for decompiled content
    if output_dir is None:
        output_dir = f"{apk_name}-{timestamp}"

    output_path = base_dir / output_dir

    # Execute apktool
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "apktool", "d", f"/data/{Path(apk_path).name}",
             "-o", f"/data/{output_dir}"],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Parse output directory
        summary = _parse_decompiled_output(output_path, detail_level)

        message = f"[+] APK decompiled successfully\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Resources: {summary.get('resourceCount', 0)}\n"
        message += f"    Smali files: {summary.get('smaliCount', 0)}\n"
        message += f"    Output: {output_path}"

        return {
            "summary": summary,
            "outputPath": str(output_path),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "apktool decompilation timed out", "outputPath": str(output_path)}
    except Exception as e:
        return {"error": str(e), "outputPath": str(output_path)}

def _parse_decompiled_output(output_path: Path, detail_level: str) -> Dict:
    """Parse decompiled APK directory structure."""
    if not output_path.exists():
        return {"error": "Output directory not found"}

    try:
        # Count resources
        res_dir = output_path / "res"
        resource_count = len(list(res_dir.rglob("*"))) if res_dir.exists() else 0

        # Count smali files
        smali_dir = output_path / "smali"
        smali_count = len(list(smali_dir.rglob("*.smali"))) if smali_dir.exists() else 0

        # Minimal: Just counts
        if detail_level == "minimal":
            return {
                "resourceCount": resource_count,
                "smaliCount": smali_count,
                "hasManifest": (output_path / "AndroidManifest.xml").exists()
            }

        # Standard: Add directory structure
        elif detail_level == "standard":
            dirs = [d.name for d in output_path.iterdir() if d.is_dir()]
            return {
                "resourceCount": resource_count,
                "smaliCount": smali_count,
                "hasManifest": (output_path / "AndroidManifest.xml").exists(),
                "directories": dirs[:10]  # First 10 directories
            }

        # Full: Add sample files
        else:
            dirs = [d.name for d in output_path.iterdir() if d.is_dir()]
            sample_smali = [f.name for f in (smali_dir.rglob("*.smali") if smali_dir.exists() else [])][:5]
            return {
                "resourceCount": resource_count,
                "smaliCount": smali_count,
                "hasManifest": (output_path / "AndroidManifest.xml").exists(),
                "directories": dirs,
                "sampleSmaliFiles": sample_smali
            }

    except Exception as e:
        return {"error": f"Failed to parse output: {str(e)}"}

if __name__ == "__main__":
    import json
    result = apktool_decode(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
