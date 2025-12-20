#!/usr/bin/env python3
"""
Diagram Export Tool

Exports Mermaid diagrams to PNG/SVG using Mermaid CLI or Kroki API.
Supports extracting diagrams from markdown files.

Usage:
    python export-diagram.py input.mmd -o output.png
    python export-diagram.py README.md --extract -o diagrams/
    python export-diagram.py input.mmd --kroki --format plantuml -o output.svg

Dependencies:
    - Mermaid CLI: npm install -g @mermaid-js/mermaid-cli
    - Kroki (optional): docker run -d -p 8000:8000 yuzutech/kroki

Author: Intelligence Adjacent Framework
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path
from typing import List, Optional, Tuple
from urllib import request, error

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")

def log_ok(msg: str):
    print(f"{Colors.GREEN}[OK]{Colors.END} {msg}")

def log_warn(msg: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {msg}")

def log_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")


def get_mmdc_path() -> Optional[str]:
    """Get the full path to mmdc executable."""
    # Try standard which
    mmdc = shutil.which('mmdc')
    if mmdc:
        return mmdc

    # Windows-specific: check common npm global paths
    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA', '')
        npm_path = os.path.join(appdata, 'npm', 'mmdc.cmd')
        if os.path.exists(npm_path):
            return npm_path

    return None


def check_mermaid_cli() -> bool:
    """Check if Mermaid CLI is installed."""
    return get_mmdc_path() is not None


def check_kroki(host: str = "http://localhost:8000") -> bool:
    """Check if Kroki server is available."""
    try:
        req = request.Request(f"{host}/health", method='GET')
        with request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except:
        return False


def extract_mermaid_from_markdown(content: str) -> List[Tuple[str, str]]:
    """
    Extract mermaid code blocks from markdown content.
    Returns list of (diagram_name, diagram_code) tuples.
    """
    # Pattern to match ```mermaid ... ``` blocks
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)

    diagrams = []
    for i, code in enumerate(matches):
        # Try to extract diagram type for naming
        first_line = code.strip().split('\n')[0]
        diagram_type = first_line.split()[0] if first_line else 'diagram'
        name = f"{diagram_type}_{i+1}"
        diagrams.append((name, code.strip()))

    return diagrams


def export_with_mermaid_cli(
    input_content: str,
    output_path: Path,
    theme: str = "default",
    width: int = 800,
    height: int = 600,
    background: str = "white"
) -> bool:
    """Export diagram using Mermaid CLI (mmdc)."""
    mmdc_path = get_mmdc_path()
    if not mmdc_path:
        log_error("Mermaid CLI (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return False

    # Create temp file for input
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
        f.write(input_content)
        temp_input = f.name

    try:
        # Build command using full path to mmdc
        cmd = [
            mmdc_path,
            '-i', temp_input,
            '-o', str(output_path),
            '-t', theme,
            '-w', str(width),
            '-H', str(height),
            '-b', background
        ]

        # Run mmdc with shell=True on Windows for .cmd files
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            shell=(sys.platform == 'win32' and mmdc_path.endswith('.cmd'))
        )

        if result.returncode != 0:
            log_error(f"Mermaid CLI failed: {result.stderr}")
            return False

        return True

    except subprocess.TimeoutExpired:
        log_error("Mermaid CLI timed out")
        return False
    except Exception as e:
        log_error(f"Export failed: {e}")
        return False
    finally:
        # Cleanup temp file
        os.unlink(temp_input)


def export_with_kroki(
    input_content: str,
    output_path: Path,
    diagram_type: str = "mermaid",
    output_format: str = "png",
    kroki_host: str = "http://localhost:8000"
) -> bool:
    """Export diagram using Kroki API."""
    # Check local Kroki first, fall back to public
    if not check_kroki(kroki_host):
        log_warn(f"Local Kroki not available at {kroki_host}, trying public API...")
        kroki_host = "https://kroki.io"

    try:
        # Kroki expects deflate + base64 encoded content
        compressed = zlib.compress(input_content.encode('utf-8'), 9)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')

        # Build URL
        url = f"{kroki_host}/{diagram_type}/{output_format}/{encoded}"

        # Make request
        req = request.Request(url, method='GET')
        with request.urlopen(req, timeout=30) as response:
            content = response.read()

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(content)

        return True

    except error.HTTPError as e:
        log_error(f"Kroki API error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        log_error(f"Kroki export failed: {e}")
        return False


def process_file(
    input_path: Path,
    output_path: Optional[Path],
    output_format: str,
    extract: bool,
    use_kroki: bool,
    diagram_type: str,
    theme: str,
    width: int,
    height: int,
    background: str,
    kroki_host: str
) -> int:
    """Process a single input file. Returns number of diagrams exported."""
    if not input_path.exists():
        log_error(f"Input file not found: {input_path}")
        return 0

    content = input_path.read_text(encoding='utf-8')
    exported = 0

    if extract or input_path.suffix.lower() == '.md':
        # Extract mermaid blocks from markdown
        diagrams = extract_mermaid_from_markdown(content)
        if not diagrams:
            log_warn(f"No mermaid diagrams found in {input_path}")
            return 0

        log_info(f"Found {len(diagrams)} diagram(s) in {input_path}")

        # Determine output directory
        if output_path:
            out_dir = output_path if output_path.is_dir() or not output_path.suffix else output_path.parent
        else:
            out_dir = input_path.parent / "diagrams"
        out_dir.mkdir(parents=True, exist_ok=True)

        for name, code in diagrams:
            out_file = out_dir / f"{name}.{output_format}"

            if use_kroki:
                success = export_with_kroki(code, out_file, diagram_type, output_format, kroki_host)
            else:
                success = export_with_mermaid_cli(code, out_file, theme, width, height, background)

            if success:
                log_ok(f"Exported: {out_file}")
                exported += 1
            else:
                log_error(f"Failed to export: {name}")

    else:
        # Direct diagram file (.mmd)
        if output_path:
            out_file = output_path if output_path.suffix else output_path / f"{input_path.stem}.{output_format}"
        else:
            out_file = input_path.with_suffix(f".{output_format}")

        out_file.parent.mkdir(parents=True, exist_ok=True)

        if use_kroki:
            success = export_with_kroki(content, out_file, diagram_type, output_format, kroki_host)
        else:
            success = export_with_mermaid_cli(content, out_file, theme, width, height, background)

        if success:
            log_ok(f"Exported: {out_file}")
            exported = 1
        else:
            log_error(f"Failed to export: {input_path}")

    return exported


def main():
    parser = argparse.ArgumentParser(
        description="Export diagrams from Mermaid/PlantUML to PNG/SVG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mmd -o output.png
  %(prog)s README.md --extract -o diagrams/
  %(prog)s diagram.puml --kroki --type plantuml -o output.svg
  %(prog)s *.mmd -o images/ --theme dark
        """
    )

    parser.add_argument('input', nargs='*', help='Input file(s) - .mmd, .md, or other diagram files')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-f', '--format', default='png', choices=['png', 'svg', 'pdf'],
                        help='Output format (default: png)')
    parser.add_argument('--extract', action='store_true',
                        help='Extract mermaid blocks from markdown files')
    parser.add_argument('--kroki', action='store_true',
                        help='Use Kroki API instead of local Mermaid CLI')
    parser.add_argument('--type', default='mermaid',
                        help='Diagram type for Kroki (mermaid, plantuml, d2, etc.)')
    parser.add_argument('--theme', default='default',
                        choices=['default', 'dark', 'forest', 'neutral'],
                        help='Mermaid theme (default: default)')
    parser.add_argument('--width', type=int, default=800,
                        help='Output width in pixels (default: 800)')
    parser.add_argument('--height', type=int, default=600,
                        help='Output height in pixels (default: 600)')
    parser.add_argument('--background', default='white',
                        help='Background color (default: white, use "transparent" for none)')
    parser.add_argument('--kroki-host', default='http://localhost:8000',
                        help='Kroki server URL (default: http://localhost:8000)')
    parser.add_argument('--check', action='store_true',
                        help='Check tool availability and exit')

    args = parser.parse_args()

    # Check mode
    if args.check:
        print("Checking diagram tools...")
        mmdc = check_mermaid_cli()
        print(f"  Mermaid CLI (mmdc): {'[OK] Available' if mmdc else '[X] Not found'}")

        kroki_local = check_kroki(args.kroki_host)
        print(f"  Kroki (local): {'[OK] Available' if kroki_local else '[X] Not running'}")

        kroki_public = check_kroki("https://kroki.io")
        print(f"  Kroki (public): {'[OK] Available' if kroki_public else '[X] Unavailable'}")

        return 0 if (mmdc or kroki_local or kroki_public) else 1

    # Require input files when not checking
    if not args.input:
        log_error("No input files specified. Use -h for help.")
        return 1

    # Validate tools
    if not args.kroki and not check_mermaid_cli():
        log_error("Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        log_info("Or use --kroki flag to use Kroki API instead")
        return 1

    # Process files
    total_exported = 0
    output_path = Path(args.output) if args.output else None

    for input_file in args.input:
        input_path = Path(input_file)

        # Handle glob patterns
        if '*' in input_file:
            for matched in Path('.').glob(input_file):
                exported = process_file(
                    matched, output_path, args.format, args.extract,
                    args.kroki, args.type, args.theme, args.width,
                    args.height, args.background, args.kroki_host
                )
                total_exported += exported
        else:
            exported = process_file(
                input_path, output_path, args.format, args.extract,
                args.kroki, args.type, args.theme, args.width,
                args.height, args.background, args.kroki_host
            )
            total_exported += exported

    print(f"\n{Colors.GREEN}Total exported: {total_exported} diagram(s){Colors.END}")
    return 0 if total_exported > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
