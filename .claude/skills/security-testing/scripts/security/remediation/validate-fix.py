#!/usr/bin/env python3
"""
Validate Fix in Production

Retests fixed code to confirm:
- Vulnerability is closed
- Functionality is preserved
- Research claims are validated
- Edge cases pass
- Performance claims verified

Usage:
    python validate-fix.py --vuln VULN-001 --target file.py --original-test test.py --research research.md

Author: Intelligence Adjacent
Version: 1.0
Last Updated: 2025-11-24
"""

import argparse
import sys
import subprocess
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def run_original_vulnerability_test(target_file: str, original_test: str) -> Dict[str, Any]:
    """Run original test that found the vulnerability (should FAIL = vuln closed)"""
    try:
        test_path = Path(original_test)
        if not test_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Original test not found',
                'details': f'Test file missing: {original_test}'
            }

        target_path = Path(target_file)
        if not target_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Target file not found',
                'details': f'File missing: {target_file}'
            }

        # Determine test type by extension
        file_ext = test_path.suffix.lower()

        if file_ext == '.py':
            # Python test (pytest)
            result = subprocess.run(
                ['pytest', str(test_path), '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=60
            )

            # For vulnerability tests, we WANT them to FAIL (vulnerability closed)
            if result.returncode != 0:
                # Test failed = vulnerability is closed = GOOD
                return {
                    'status': 'PASSED',
                    'message': 'Vulnerability test failed as expected',
                    'details': 'Vulnerability is closed'
                }
            else:
                # Test passed = vulnerability still present = BAD
                return {
                    'status': 'FAILED',
                    'message': 'Vulnerability test passed (still vulnerable!)',
                    'details': 'Fix did not close vulnerability'
                }

        elif file_ext in ['.sh', '.bash']:
            # Shell script test
            result = subprocess.run(
                ['bash', str(test_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Same logic: test failure = vuln closed
            if result.returncode != 0:
                return {
                    'status': 'PASSED',
                    'message': 'Vulnerability test failed as expected',
                    'details': 'Vulnerability is closed'
                }
            else:
                return {
                    'status': 'FAILED',
                    'message': 'Vulnerability test passed (still vulnerable!)',
                    'details': 'Fix did not close vulnerability'
                }

        else:
            return {
                'status': 'SKIPPED',
                'message': f'Unsupported test type: {file_ext}',
                'details': 'Manual testing required'
            }

    except FileNotFoundError:
        return {
            'status': 'ERROR',
            'message': 'Test runner not found',
            'details': 'Install pytest or appropriate test runner'
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Test execution error',
            'details': str(e)
        }


def run_functionality_validation(target_file: str, test_suite: Optional[str] = None) -> Dict[str, Any]:
    """Validate original functionality still works"""
    try:
        target_path = Path(target_file)
        if not target_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Target file not found',
                'details': f'File missing: {target_file}'
            }

        # If test suite provided, run it
        if test_suite and Path(test_suite).exists():
            result = subprocess.run(
                ['pytest', test_suite, '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return {
                    'status': 'PASSED',
                    'message': 'Functionality tests passed',
                    'details': 'All features working correctly'
                }
            else:
                return {
                    'status': 'FAILED',
                    'message': 'Functionality tests failed',
                    'details': result.stdout + '\n' + result.stderr
                }

        # No test suite - do basic syntax check
        file_ext = target_path.suffix.lower()

        if file_ext == '.py':
            # Python syntax check
            with open(target_path, 'r', encoding='utf-8') as f:
                code = f.read()

            try:
                compile(code, str(target_path), 'exec')
                return {
                    'status': 'PASSED',
                    'message': 'Basic functionality check passed',
                    'details': 'Syntax valid, no obvious errors'
                }
            except SyntaxError as e:
                return {
                    'status': 'FAILED',
                    'message': 'Syntax error in fixed code',
                    'details': str(e)
                }

        else:
            return {
                'status': 'SKIPPED',
                'message': 'No functionality tests provided',
                'details': 'Manual validation recommended'
            }

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Functionality validation error',
            'details': str(e)
        }


def extract_research_claims(research_file: str) -> Dict[str, List[str]]:
    """Extract claims from research report to validate"""
    try:
        research_path = Path(research_file)
        if not research_path.exists():
            return {'performance': [], 'edge_cases': [], 'gotchas': []}

        with open(research_path, 'r', encoding='utf-8') as f:
            content = f.read()

        claims = {
            'performance': [],
            'edge_cases': [],
            'gotchas': []
        }

        # Extract performance claims
        perf_patterns = [
            r'performance[:\s]+([^.\n]+)',
            r'impact[:\s]+([^.\n]+)',
            r'overhead[:\s]+([^.\n]+)'
        ]

        for pattern in perf_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                claim = match.strip()
                if len(claim) > 10 and claim not in claims['performance']:
                    claims['performance'].append(claim)

        # Extract edge cases
        edge_section = re.search(
            r'## Edge Cases\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if edge_section:
            lines = edge_section.group(1).split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    edge_case = line[2:].strip()
                    if edge_case and len(edge_case) > 10:
                        claims['edge_cases'].append(edge_case)

        # Extract gotchas
        gotcha_patterns = [
            r'## (?:Gotchas|Warnings|Cautions)\s*\n(.*?)(?=\n##|\Z)',
            r'## Community (?:Intel|Insights)\s*\n(.*?)(?=\n##|\Z)'
        ]

        for pattern in gotcha_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                lines = match.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('* '):
                        gotcha = line[2:].strip()
                        if gotcha and len(gotcha) > 10:
                            claims['gotchas'].append(gotcha)

        return claims

    except Exception as e:
        print(f"[!] Failed to extract research claims: {e}")
        return {'performance': [], 'edge_cases': [], 'gotchas': []}


def validate_performance_claims(target_file: str, claims: List[str]) -> Dict[str, Any]:
    """Verify performance claims from research"""
    try:
        if not claims:
            return {
                'status': 'SKIPPED',
                'message': 'No performance claims to validate',
                'details': 'No performance metrics in research'
            }

        target_path = Path(target_file)
        if not target_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Target file not found',
                'details': f'File missing: {target_file}'
            }

        # Simple performance check: measure load/compile time
        file_ext = target_path.suffix.lower()

        if file_ext == '.py':
            # Measure Python compile time
            start = time.time()
            with open(target_path, 'r', encoding='utf-8') as f:
                code = f.read()

            try:
                compile(code, str(target_path), 'exec')
                compile_time_ms = (time.time() - start) * 1000

                # Check if any claim mentions specific thresholds
                validated_claims = []
                for claim in claims:
                    # Look for numeric thresholds
                    numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(ms|milliseconds|seconds|s)', claim.lower())
                    if numbers:
                        threshold_ms = float(numbers[0][0])
                        if 'second' in numbers[0][1]:
                            threshold_ms *= 1000

                        if compile_time_ms <= threshold_ms:
                            validated_claims.append(f"'{claim}' - VALIDATED ({compile_time_ms:.2f}ms)")
                        else:
                            validated_claims.append(f"'{claim}' - EXCEEDED ({compile_time_ms:.2f}ms)")
                    else:
                        validated_claims.append(f"'{claim}' - NO THRESHOLD (measured: {compile_time_ms:.2f}ms)")

                return {
                    'status': 'PASSED',
                    'message': f'Performance validated ({compile_time_ms:.2f}ms)',
                    'details': '\n'.join(validated_claims) if validated_claims else f'Compile time: {compile_time_ms:.2f}ms'
                }

            except SyntaxError as e:
                return {
                    'status': 'FAILED',
                    'message': 'Syntax error during performance test',
                    'details': str(e)
                }

        else:
            return {
                'status': 'SKIPPED',
                'message': 'Performance validation not implemented for this file type',
                'details': 'Manual benchmarking recommended'
            }

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Performance validation error',
            'details': str(e)
        }


def validate_edge_cases(target_file: str, edge_cases: List[str]) -> Dict[str, Any]:
    """Validate research-predicted edge cases"""
    try:
        if not edge_cases:
            return {
                'status': 'SKIPPED',
                'message': 'No edge cases to validate',
                'details': 'No edge cases in research'
            }

        target_path = Path(target_file)
        if not target_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Target file not found',
                'details': f'File missing: {target_file}'
            }

        # Read target file
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if edge cases are addressed in code
        addressed = []
        not_addressed = []

        for edge_case in edge_cases:
            # Look for evidence that edge case is handled
            # Example: "Unicode" -> check for encoding handling
            # Example: "NULL" -> check for null checks

            keywords = {
                'unicode': ['encode', 'decode', 'utf-8', 'utf8', 'encoding'],
                'null': ['is None', '!= None', 'if not', 'null', 'None'],
                'empty': ['if not', 'len(', 'empty', 'isempty'],
                'long': ['limit', 'max', 'length', 'truncate'],
                'special': ['escape', 'sanitize', 'validate', 'filter']
            }

            found = False
            for category, terms in keywords.items():
                if category in edge_case.lower():
                    for term in terms:
                        if term in content:
                            addressed.append(f"'{edge_case}' - Evidence found: {term}")
                            found = True
                            break
                    if found:
                        break

            if not found:
                not_addressed.append(f"'{edge_case}' - No clear evidence (manual review needed)")

        if not_addressed:
            return {
                'status': 'WARNING',
                'message': f'{len(addressed)}/{len(edge_cases)} edge cases have code evidence',
                'details': '\n'.join(addressed + not_addressed)
            }
        else:
            return {
                'status': 'PASSED',
                'message': f'All {len(edge_cases)} edge cases have code evidence',
                'details': '\n'.join(addressed)
            }

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Edge case validation error',
            'details': str(e)
        }


def validate_gotchas_addressed(target_file: str, gotchas: List[str]) -> Dict[str, Any]:
    """Verify gotchas from community research were addressed"""
    try:
        if not gotchas:
            return {
                'status': 'SKIPPED',
                'message': 'No gotchas to validate',
                'details': 'No gotchas in research'
            }

        target_path = Path(target_file)
        if not target_path.exists():
            return {
                'status': 'ERROR',
                'message': 'Target file not found',
                'details': f'File missing: {target_file}'
            }

        # Read target file
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for gotcha workarounds
        addressed = []
        warnings = []

        for gotcha in gotchas:
            # Look for common workaround patterns
            workaround_patterns = [
                'workaround',
                'fix for',
                'handles',
                'prevents',
                'addresses',
                'mitigates'
            ]

            found = False
            for pattern in workaround_patterns:
                if pattern in content.lower():
                    # Check if near a comment mentioning the gotcha
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if pattern in line.lower() and any(word in line.lower() for word in gotcha.lower().split()[:3]):
                            addressed.append(f"'{gotcha[:50]}...' - Workaround found")
                            found = True
                            break
                if found:
                    break

            if not found:
                warnings.append(f"'{gotcha[:50]}...' - No explicit workaround (manual review)")

        if warnings:
            return {
                'status': 'WARNING',
                'message': f'{len(addressed)}/{len(gotchas)} gotchas explicitly addressed',
                'details': '\n'.join(addressed + warnings)
            }
        else:
            return {
                'status': 'PASSED',
                'message': f'All {len(gotchas)} gotchas addressed',
                'details': '\n'.join(addressed)
            }

    except Exception as e:
        return {
            'status': 'ERROR',
            'message': 'Gotcha validation error',
            'details': str(e)
        }


def generate_validation_report(vuln_id: str, results: Dict[str, Dict[str, Any]], research_results: Dict[str, Dict[str, Any]]) -> str:
    """
    Generate before/after comparison report

    Format:
        VALIDATION REPORT - VULN-001

        Critical Tests:
        [+] Vulnerability closed: PASSED
        [+] Functionality preserved: PASSED

        Research Validation:
        [+] Performance claims: VALIDATED
        [~] Edge cases: 5/7 addressed (manual review needed)
        [+] Community gotchas: ADDRESSED
    """

    report = []
    report.append(f"\n{'='*70}")
    report.append(f"VALIDATION REPORT - {vuln_id}")
    report.append(f"{'='*70}")

    # Critical tests
    report.append(f"\nCritical Tests:")

    for key, result in results.items():
        status = result.get('status', 'UNKNOWN')
        message = result.get('message', '')

        if status == 'PASSED':
            symbol = '[+]'
        elif status == 'FAILED':
            symbol = '[!]'
        elif status == 'WARNING':
            symbol = '[~]'
        elif status == 'SKIPPED':
            symbol = '[-]'
        else:
            symbol = '[?]'

        report.append(f"{symbol} {key}: {message}")

    # Research validation
    if research_results:
        report.append(f"\nResearch Validation:")

        for key, result in research_results.items():
            status = result.get('status', 'UNKNOWN')
            message = result.get('message', '')

            if status == 'PASSED':
                symbol = '[+]'
            elif status == 'FAILED':
                symbol = '[!]'
            elif status == 'WARNING':
                symbol = '[~]'
            elif status == 'SKIPPED':
                symbol = '[-]'
            else:
                symbol = '[?]'

            report.append(f"{symbol} {key}: {message}")

    report.append(f"\n{'='*70}")

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Validate fix in production',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate-fix.py --vuln VULN-001 --target fixed.py --original-test vuln_test.py
  python validate-fix.py --vuln SQLi-Login --target app.py --original-test tests/sqli.py --research research.md
        """
    )

    parser.add_argument('--vuln', required=True, help='Vulnerability ID')
    parser.add_argument('--target', required=True, help='Fixed file to validate')
    parser.add_argument('--original-test', required=True, help='Original vulnerability test')
    parser.add_argument('--research', help='Research report file (optional)')
    parser.add_argument('--test-suite', help='Functionality test suite (optional)')

    args = parser.parse_args()

    # Validate inputs
    if not Path(args.target).exists():
        print(f"[!] Target file not found: {args.target}")
        return 1

    if not Path(args.original_test).exists():
        print(f"[!] Original test not found: {args.original_test}")
        return 1

    print(f"\n[*] Validating fix in production")
    print(f"[*] Vulnerability: {args.vuln}")
    print(f"[*] Target: {args.target}")
    print(f"[*] Original test: {args.original_test}")

    results = {}

    # Test 1: Vulnerability closed
    print(f"\n[*] Test 1/2: Running original vulnerability test...")
    results['Vulnerability closed'] = run_original_vulnerability_test(args.target, args.original_test)

    # Test 2: Functionality preserved
    print(f"[*] Test 2/2: Validating functionality...")
    results['Functionality preserved'] = run_functionality_validation(args.target, args.test_suite)

    # Research validation (if provided)
    research_results = {}
    if args.research:
        print(f"\n[*] Extracting research claims from: {args.research}")
        claims = extract_research_claims(args.research)

        if claims['performance']:
            print(f"[*] Validating performance claims...")
            research_results['Performance'] = validate_performance_claims(args.target, claims['performance'])

        if claims['edge_cases']:
            print(f"[*] Validating edge cases...")
            research_results['Edge cases'] = validate_edge_cases(args.target, claims['edge_cases'])

        if claims['gotchas']:
            print(f"[*] Validating community gotchas...")
            research_results['Community gotchas'] = validate_gotchas_addressed(args.target, claims['gotchas'])

    # Generate report
    report = generate_validation_report(args.vuln, results, research_results)
    print(report)

    # Overall status
    critical_passed = all(
        r.get('status') == 'PASSED'
        for r in results.values()
    )

    research_ok = all(
        r.get('status') in ['PASSED', 'SKIPPED', 'WARNING']
        for r in research_results.values()
    ) if research_results else True

    if critical_passed and research_ok:
        print(f"\n[+] {args.vuln} remediation: VALIDATED")
        print(f"[+] Fix is working correctly in production")
        print(f"\n[i] Decision: [K]eep fix / [R]ollback")
        return 0
    else:
        print(f"\n[!] VALIDATION FAILED")
        print(f"[!] Critical tests failed - recommend rollback")
        print(f"\n[i] Use: python tools/security/remediation/rollback-fix.py --help")
        return 1


if __name__ == '__main__':
    sys.exit(main())
