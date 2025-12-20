#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apksigner wrapper - APK signature verification"""
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

def apksigner_verify(
    apk_path: str,
    engagement_dir: Optional[str] = None,
    detail_level: str = "minimal"
) -> Dict:
    """
    Verify APK signature and certificate information using apksigner.

    Token efficiency:
    - Minimal mode: ~50 tokens (signature valid, signer count)
    - Standard mode: ~150 tokens (certificate subject, validity dates)
    - Full mode: ~400 tokens (full certificate details)
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
        output_dir = Path(engagement_dir) / "04-analysis" / "apksigner"
    else:
        output_dir = Path.home() / ".claude" / "sessions" / datetime.now().strftime("%Y-%m-%d") / "mobile" / "apksigner"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{apk_name}-{timestamp}.txt"

    # Execute apksigner
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{Path(apk_path).parent}:/data",
             "mobile-tools-mcp-server", "apksigner", "verify", "--verbose", "--print-certs",
             f"/data/{Path(apk_path).name}"],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Save full output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result["stdout"])
            if result["stderr"]:
                f.write("\n\n=== STDERR ===\n")
                f.write(result["stderr"])

        # Parse signature info
        summary = _parse_signature(result["stdout"], detail_level)

        message = f"[+] APK signature verification complete\n"
        message += f"    APK: {apk_name}\n"
        message += f"    Valid: {summary.get('valid', False)}\n"
        message += f"    Signers: {summary.get('signerCount', 0)}\n"
        message += f"    Full report: {output_file}"

        return {
            "summary": summary,
            "outputFile": str(output_file),
            "message": message
        }

    except subprocess.TimeoutExpired:
        return {"error": "apksigner verification timed out", "outputFile": str(output_file)}
    except Exception as e:
        return {"error": str(e), "outputFile": str(output_file)}

def _parse_signature(output: str, detail_level: str) -> Dict:
    """Parse apksigner verification output."""
    lines = output.split('\n')

    # Check if valid
    valid = "Verified using" in output or "Verifies" in output

    # Count signers
    signer_count = output.count("Signer #")

    # Minimal: Just validation status
    if detail_level == "minimal":
        return {
            "valid": valid,
            "signerCount": signer_count
        }

    # Standard: Add certificate subject
    elif detail_level == "standard":
        subject = None
        for line in lines:
            if "DN:" in line or "Subject:" in line:
                subject = line.split(":", 1)[1].strip() if ":" in line else None
                break

        return {
            "valid": valid,
            "signerCount": signer_count,
            "subject": subject
        }

    # Full: Complete details
    else:
        # Extract all certificate info
        cert_info = []
        current_cert = {}
        for line in lines:
            if "Signer #" in line:
                if current_cert:
                    cert_info.append(current_cert)
                current_cert = {}
            elif ":" in line:
                key, value = line.split(":", 1)
                current_cert[key.strip()] = value.strip()

        if current_cert:
            cert_info.append(current_cert)

        return {
            "valid": valid,
            "signerCount": signer_count,
            "certificates": cert_info
        }

if __name__ == "__main__":
    import json
    result = apksigner_verify(sys.argv[1] if len(sys.argv) > 1 else "test.apk")
    print(json.dumps(result, indent=2))
