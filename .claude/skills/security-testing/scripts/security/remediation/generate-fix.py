#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Fix Patch from Research Findings

Creates minimal code patch from multi-model research report with:
- Research-driven recommendations
- Full citation trail
- Unified diff format
- Implementation notes

Usage:
    python generate-fix.py --research research.md --target file.py --output fix.patch

Author: Intelligence Adjacent
Version: 1.0
Last Updated: 2025-11-24
"""

import argparse
import sys
import io
import re
from pathlib import Path
from datetime import datetime

# =============================================================================
# MANDATORY: UTF-8 Encoding for Windows Console Output
# =============================================================================
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def parse_research_report(research_file):
    """
    Parse research report to extract key recommendations

    Returns:
        dict: {
            vuln_id, vuln_type, cwe_id,
            official_guidance, community_intel, adversarial_analysis,
            best_solution, gotchas, edge_cases
        }
    """
    if not Path(research_file).exists():
        print(f"[!] Research file not found: {research_file}")
        return None

    with open(research_file, 'r', encoding='utf-8') as f:
        content = f.read()

    research = {
        'vuln_id': None,
        'vuln_type': None,
        'cwe_id': None,
        'language': None,
        'framework': None,
        'official_guidance': '',
        'community_intel': '',
        'adversarial_analysis': '',
        'best_solution': '',
        'gotchas': [],
        'edge_cases': []
    }

    # Extract vulnerability ID from title
    vuln_match = re.search(r'#\s+(VULN-\d+)', content)
    if vuln_match:
        research['vuln_id'] = vuln_match.group(1)

    # Extract context fields
    type_match = re.search(r'\*\*Type:\*\*\s*(.+)', content)
    if type_match:
        research['vuln_type'] = type_match.group(1).strip()

    cwe_match = re.search(r'\*\*CWE:\*\*\s*(CWE-\d+)', content)
    if cwe_match:
        research['cwe_id'] = cwe_match.group(1)

    lang_match = re.search(r'\*\*Language:\*\*\s*(.+)', content)
    if lang_match:
        research['language'] = lang_match.group(1).strip()

    fw_match = re.search(r'\*\*Framework:\*\*\s*(.+)', content)
    if fw_match:
        research['framework'] = fw_match.group(1).strip()

    # Extract sections
    sections = {
        'official_guidance': r'## Research Phase 1: Official Sources.*?\n\n(.+?)(?=\n## |$)',
        'community_intel': r'## Research Phase 2: Community Intelligence.*?\n\n(.+?)(?=\n## |$)',
        'adversarial_analysis': r'## Research Phase 3: Adversarial Validation.*?\n\n(.+?)(?=\n## |$)',
        'best_solution': r'## Final Recommendation.*?\n\n(.+?)(?=\n## |$)'
    }

    for key, pattern in sections.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            research[key] = match.group(1).strip()

    # Extract gotchas
    gotchas_section = re.search(r'\*\*Key Gotchas:\*\*\n(.*?)(?=\n\*\*|$)', content, re.DOTALL)
    if gotchas_section:
        gotchas = re.findall(r'-\s+(.+)', gotchas_section.group(1))
        research['gotchas'] = [g.strip() for g in gotchas if g.strip() != 'None identified']

    # Extract edge cases
    edge_section = re.search(r'\*\*Edge Cases to Consider:\*\*\n(.*?)(?=\n---|$)', content, re.DOTALL)
    if edge_section:
        edges = re.findall(r'-\s+(.+)', edge_section.group(1))
        research['edge_cases'] = [e.strip() for e in edges if e.strip() != 'None identified']

    return research


def extract_vulnerable_code(target_file):
    """
    Extract vulnerable code from target file

    Returns:
        tuple: (original_content, line_count)
    """
    target_path = Path(target_file)

    if not target_path.exists():
        print(f"[!] Target file not found: {target_file}")
        return None, 0

    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    line_count = content.count('\n') + 1

    return content, line_count


def generate_fix_code(research, original_code, target_file):
    """
    Generate fixed code based on research recommendations

    Returns:
        str: Fixed code with citations in comments
    """
    vuln_type = research.get('vuln_type', 'vulnerability')
    best_solution = research.get('best_solution', '')

    # Extract code examples from best solution if available
    code_blocks = re.findall(r'```[\w]*\n(.*?)```', best_solution, re.DOTALL)

    if not code_blocks:
        # No code examples in research - provide template with guidance
        fix_template = f"""# Fix generated from research findings
# Vulnerability: {vuln_type}
# CWE: {research.get('cwe_id', 'N/A')}
#
# Research Summary:
# {best_solution[:500]}...
#
# Implementation Notes:
# - Review official guidance in research report
# - Consider gotchas: {', '.join(research.get('gotchas', [])[:3])}
# - Test edge cases: {', '.join(research.get('edge_cases', [])[:3])}
#
# MANUAL IMPLEMENTATION REQUIRED
# This research did not contain specific code examples.
# Review the research report and implement based on official guidance.

{original_code}
"""
        return fix_template

    # Use first code block as the fix
    fixed_code = code_blocks[0]

    # Add citation comments
    citations = f"""# Fix applied based on multi-model research
# Research file: {research.get('research_file', 'N/A')}
# Vulnerability: {vuln_type} ({research.get('cwe_id', 'N/A')})
#
# Sources:
# - Official: OWASP, NIST, CWE database
# - Community: Reddit, GitHub, Stack Overflow
# - Validation: Red team analysis (Grok)
#
# Gotchas addressed:
"""
    if research.get('gotchas'):
        for gotcha in research.get('gotchas', []):
            citations += f"# - {gotcha}\n"
    else:
        citations += "# - None identified\n"

    citations += "#\n# Edge cases considered:\n"
    if research.get('edge_cases'):
        for edge in research.get('edge_cases', []):
            citations += f"# - {edge}\n"
    else:
        citations += "# - None identified\n"

    return citations + "\n" + fixed_code


def create_patch_file(original_code, fixed_code, target_file, output_file, research):
    """
    Create unified diff patch file

    Format:
        --- original.py
        +++ fixed.py
        @@ line numbers @@
        -old line
        +new line
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create simple unified diff
    patch_header = f"""# Remediation Patch
# Generated: {timestamp}
# Vulnerability: {research.get('vuln_type', 'N/A')} ({research.get('cwe_id', 'N/A')})
# Target: {target_file}
# Research: Multi-model OSINT validation
#
# To apply:
#   python tools/security/remediation/apply-fix.py --patch {output_file} --target {target_file}
#
# To test first:
#   python tools/security/remediation/test-fix.py --patch {output_file} --target {target_file}
#
--- a/{Path(target_file).name}
+++ b/{Path(target_file).name}
@@ -1,{original_code.count(chr(10))+1} +1,{fixed_code.count(chr(10))+1} @@
"""

    # Add line-by-line diff
    original_lines = original_code.splitlines()
    fixed_lines = fixed_code.splitlines()

    diff_lines = []

    # Simple diff: show all old lines as removed, all new lines as added
    for line in original_lines:
        diff_lines.append(f"-{line}")

    for line in fixed_lines:
        diff_lines.append(f"+{line}")

    patch_content = patch_header + "\n".join(diff_lines)

    # Write patch file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(patch_content)

    return patch_content


def main():
    parser = argparse.ArgumentParser(
        description='Generate fix patch from research findings'
    )
    parser.add_argument(
        '--research',
        required=True,
        help='Research report file (from research-fix.py)'
    )
    parser.add_argument(
        '--target',
        required=True,
        help='Target file to fix'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output patch file'
    )
    parser.add_argument(
        '--manual',
        action='store_true',
        help='Generate manual implementation guide instead of automatic patch'
    )

    args = parser.parse_args()

    print(f"[*] Generating fix patch from research findings")
    print(f"[*] Research: {args.research}")
    print(f"[*] Target: {args.target}")
    print()

    # Parse research report
    print(f"[*] Parsing research report...")
    research = parse_research_report(args.research)

    if not research:
        print(f"[!] Failed to parse research report")
        return 1

    research['research_file'] = args.research

    print(f"[+] Vulnerability: {research.get('vuln_type', 'Unknown')}")
    print(f"[+] CWE: {research.get('cwe_id', 'Unknown')}")

    if research.get('gotchas'):
        print(f"[+] Gotchas found: {len(research['gotchas'])}")
    if research.get('edge_cases'):
        print(f"[+] Edge cases found: {len(research['edge_cases'])}")

    # Extract vulnerable code
    print(f"\n[*] Reading target file...")
    original_code, line_count = extract_vulnerable_code(args.target)

    if original_code is None:
        print(f"[!] Failed to read target file")
        return 1

    print(f"[+] File: {line_count} lines")

    # Generate fix
    print(f"\n[*] Generating fixed code from research...")
    fixed_code = generate_fix_code(research, original_code, args.target)

    if "MANUAL IMPLEMENTATION REQUIRED" in fixed_code:
        print(f"[!] No code examples in research - manual implementation required")
        print(f"[!] Review research report for guidance")

    # Create patch
    print(f"\n[*] Creating patch file...")
    patch = create_patch_file(original_code, fixed_code, args.target, args.output, research)

    print(f"[+] Patch created: {args.output}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Patch Generated")
    print(f"{'='*60}")
    print(f"Target: {args.target}")
    print(f"Patch: {args.output}")
    print(f"Research: {args.research}")
    print(f"\nOriginal: {original_code.count(chr(10))+1} lines")
    print(f"Fixed: {fixed_code.count(chr(10))+1} lines")
    print(f"\nGotchas: {len(research.get('gotchas', []))}")
    print(f"Edge cases: {len(research.get('edge_cases', []))}")

    print(f"\n[+] Next: Test patch in isolated environment")
    print(f"    python tools/security/remediation/test-fix.py --patch {args.output} --target {args.target}")

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
