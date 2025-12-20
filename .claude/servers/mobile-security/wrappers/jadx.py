#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jadx wrapper - Java decompiler for APK files"""
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

def jadx_decompile(
    apk_path: str,
    output_dir: Optional[str] = None,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Decompile APK to Java source code using jadx.

    Token efficiency:
    - Minimal mode: ~100 tokens (file counts, package structure summary)
    - Standard mode: ~300 tokens (detailed package listing)
    - Full mode: ~1000 tokens (includes sample class names)
    - No caching (unique per APK)

    Args:
        apk_path: Path to APK file
        output_dir: Optional output directory name
        engagement_dir: Optional engagement directory
        detail_level: "minimal" | "standard" | "full"

    Returns:
        Dict with summary, outputPath, and message
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    apk_name = Path(apk_path).stem

    # Determine base directory
    if engagement_dir:
        base_dir = Path(engagement_dir) / "04-analysis" / "jadx"
    else:
        base_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "jadx"

    base_dir.mkdir(parents=True, exist_ok=True)

    # Output directory
    if output_dir is None:
        output_dir = f"{apk_name}-{timestamp}"

    output_path = base_dir / output_dir

    # Execute jadx
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "jadx", f"/data/{Path(apk_path).name}",
             "-d", f"/data/{output_dir}"],
            capture_output=True,
            text=True,
            timeout=600  # Decompilation can take time
        )

        # Parse decompiled output
        summary = _parse_java_output(output_path, detail_level)

        message = f"[+] APK decompiled to Java successfully\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Java files: {summary.get('javaCount', 0)}\n"
        message += f"    Packages: {summary.get('packageCount', 0)}\n"
        message += f"    Output: {output_path}"

        return {
            "summary": summary,
            "outputPath": str(output_path),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "jadx decompilation timed out", "outputPath": str(output_path)}
    except Exception as e:
        return {"error": str(e), "outputPath": str(output_path)}

def _parse_java_output(output_path: Path, detail_level: str) -> Dict:
    """Parse decompiled Java directory structure."""
    if not output_path.exists():
        return {"error": "Output directory not found"}

    try:
        sources_dir = output_path / "sources"
        if not sources_dir.exists():
            return {"error": "Sources directory not found"}

        # Count Java files
        java_files = list(sources_dir.rglob("*.java"))
        java_count = len(java_files)

        # Count packages (directories in sources)
        packages = [d for d in sources_dir.rglob("*") if d.is_dir()]
        package_count = len(packages)

        # Minimal: Just counts
        if detail_level == "minimal":
            return {
                "javaCount": java_count,
                "packageCount": package_count
            }

        # Standard: Add top packages
        elif detail_level == "standard":
            top_packages = [str(p.relative_to(sources_dir)) for p in sorted(packages)[:10]]
            return {
                "javaCount": java_count,
                "packageCount": package_count,
                "topPackages": top_packages
            }

        # Full: Add sample class names
        else:
            top_packages = [str(p.relative_to(sources_dir)) for p in sorted(packages)[:10]]
            sample_classes = [f.stem for f in java_files[:20]]
            return {
                "javaCount": java_count,
                "packageCount": package_count,
                "topPackages": top_packages,
                "sampleClasses": sample_classes
            }

    except Exception as e:
        return {"error": f"Failed to parse output: {str(e)}"}

if __name__ == "__main__":
    import json
    result = jadx_decompile(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
