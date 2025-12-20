#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Model OSINT Research for Vulnerability Remediation

Researches best fix using:
- Perplexity: Official sources (OWASP, NIST, CWE)
- Context7: Community intelligence (Reddit, GitHub, Stack Overflow)
- Grok: Adversarial validation (bypass analysis)

Usage:
    python research-fix.py --vuln VULN-001 --engagement /path/to/engagement --output research.md

Author: Intelligence Adjacent
Version: 1.0
Last Updated: 2025-11-24
"""

import argparse
import json
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

# Add tools directory to path for imports
sys.path.insert(0, str(Path.home() / '.claude'))

from tools.openrouter.client import OpenRouterClient


def extract_vulnerability_context(vuln_file):
    """
    Extract context from vulnerability document

    Returns:
        dict: {cwe_id, vuln_type, language, framework, code_snippet, attack_vector, cvss}
    """
    if not vuln_file.exists():
        print(f"[!] Vulnerability file not found: {vuln_file}")
        return None

    with open(vuln_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract key information using regex patterns
    context = {
        'file': str(vuln_file),
        'vuln_type': None,
        'cwe_id': None,
        'cvss': None,
        'language': None,
        'framework': None,
        'code_snippet': None,
        'attack_vector': None,
        'description': None
    }

    # Extract CWE
    cwe_match = re.search(r'CWE[:-]?\s*(\d+)', content, re.IGNORECASE)
    if cwe_match:
        context['cwe_id'] = f"CWE-{cwe_match.group(1)}"

    # Extract CVSS
    cvss_match = re.search(r'CVSS[:-]?\s*(\d+\.?\d*)', content, re.IGNORECASE)
    if cvss_match:
        context['cvss'] = cvss_match.group(1)

    # Extract vulnerability type (look for common patterns)
    vuln_types = [
        'SQL Injection', 'XSS', 'Cross-Site Scripting', 'CSRF',
        'Authentication Bypass', 'IDOR', 'Path Traversal',
        'Command Injection', 'SSRF', 'XXE', 'Deserialization'
    ]
    for vtype in vuln_types:
        if vtype.lower() in content.lower():
            context['vuln_type'] = vtype
            break

    # Extract language/framework
    languages = ['Python', 'PHP', 'Java', 'JavaScript', 'Ruby', 'C#', 'Go']
    frameworks = ['Django', 'Flask', 'Laravel', 'Spring', 'Express', 'Rails', 'ASP.NET']

    for lang in languages:
        if lang.lower() in content.lower():
            context['language'] = lang
            break

    for fw in frameworks:
        if fw.lower() in content.lower():
            context['framework'] = fw
            break

    # Extract code snippet (look for code blocks)
    code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)
    if code_blocks:
        context['code_snippet'] = code_blocks[0][:500]  # First 500 chars

    # Extract description (first paragraph after title)
    desc_match = re.search(r'##?\s+Description\s*\n\n(.*?)(?:\n\n|\Z)', content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        context['description'] = desc_match.group(1).strip()[:300]

    return context


def query_perplexity(client, vuln_context):
    """
    Query Perplexity for official sources

    Returns:
        dict: {findings, citations, duration, success}
    """
    # Build research query
    vuln_type = vuln_context.get('vuln_type', 'vulnerability')
    cwe_id = vuln_context.get('cwe_id', '')
    language = vuln_context.get('language', '')
    framework = vuln_context.get('framework', '')

    prompt = f"""Research the best remediation approach for {vuln_type} ({cwe_id}) in {language} {framework}.

Search official security sources including:
- OWASP guidelines
- NIST standards
- CWE database
- Vendor security documentation
- Official framework security guides

Provide:
1. Recommended remediation approach
2. Code examples if available
3. Official citations
4. Performance considerations
5. Common implementation mistakes to avoid"""

    print(f"    [Perplexity] Searching OWASP, NIST, CWE...")
    result = client.query_model(
        model='perplexity',
        prompt=prompt,
        temperature=0.2,
        max_tokens=2000
    )

    return {
        'findings': result.get('content', ''),
        'model': result.get('model', 'perplexity'),
        'tokens': result.get('tokens', 0),
        'cost': result.get('cost', 0.0),
        'duration': result.get('duration', 0.0),
        'success': result.get('success', False)
    }


def query_context7(client, vuln_context):
    """
    Query Context7 for community intelligence

    Returns:
        dict: {findings, sources, duration, success}
    """
    vuln_type = vuln_context.get('vuln_type', 'vulnerability')
    language = vuln_context.get('language', '')
    framework = vuln_context.get('framework', '')

    prompt = f"""Find real-world solutions and gotchas for fixing {vuln_type} in {language} {framework}.

Search community sources:
- Reddit (r/netsec, r/websecurity, r/AskNetsec)
- GitHub (issues, pull requests, security advisories)
- Stack Overflow (security tag)
- Security blogs and write-ups

Focus on:
1. Production-tested solutions
2. Common gotchas and pitfalls
3. Performance impact reports
4. Failed approaches to avoid
5. Edge cases discovered in practice

Cite specific sources."""

    print(f"    [Context7] Searching Reddit, GitHub, Stack Overflow...")
    result = client.query_model(
        model='context7',
        prompt=prompt,
        temperature=0.3,
        max_tokens=2000
    )

    return {
        'findings': result.get('content', ''),
        'model': result.get('model', 'context7'),
        'tokens': result.get('tokens', 0),
        'cost': result.get('cost', 0.0),
        'duration': result.get('duration', 0.0),
        'success': result.get('success', False)
    }


def query_grok(client, vuln_context, proposed_fix):
    """
    Query Grok for adversarial validation

    Returns:
        dict: {analysis, risks, alternatives, duration, success}
    """
    vuln_type = vuln_context.get('vuln_type', 'vulnerability')
    cwe_id = vuln_context.get('cwe_id', '')

    prompt = f"""Red team analysis of {vuln_type} ({cwe_id}) remediation approach.

Proposed fix summary:
{proposed_fix[:800]}

Evaluate from an attacker's perspective:
1. Bypass vectors - Can this fix be circumvented?
2. Edge cases - What unusual inputs might break the fix?
3. Second-order effects - Could this introduce new vulnerabilities?
4. Performance impact - Could this create DoS vectors?
5. Incomplete fixes - What might developers miss when implementing?

Be specific and technical. Focus on practical attack scenarios."""

    print(f"    [Grok] Red team validation...")
    result = client.query_model(
        model='grok',
        prompt=prompt,
        temperature=0.4,
        max_tokens=2000
    )

    return {
        'analysis': result.get('content', ''),
        'model': result.get('model', 'grok'),
        'tokens': result.get('tokens', 0),
        'cost': result.get('cost', 0.0),
        'duration': result.get('duration', 0.0),
        'success': result.get('success', False)
    }


def synthesize_findings(perplexity_result, context7_result, grok_result):
    """
    Aggregate findings from all 3 models

    Returns:
        dict: {
            best_solution: str,
            official_guidance: str,
            community_validation: str,
            adversarial_analysis: str,
            gotchas: list,
            edge_cases: list,
            citations: list,
            total_cost: float,
            total_duration: float
        }
    """
    synthesis = {
        'best_solution': '',
        'official_guidance': perplexity_result.get('findings', 'N/A'),
        'community_validation': context7_result.get('findings', 'N/A') if context7_result else 'N/A',
        'adversarial_analysis': grok_result.get('analysis', 'N/A') if grok_result else 'N/A',
        'gotchas': [],
        'edge_cases': [],
        'citations': [],
        'total_cost': 0.0,
        'total_duration': 0.0,
        'models_used': []
    }

    # Aggregate costs and durations
    for result in [perplexity_result, context7_result, grok_result]:
        if result and result.get('success'):
            synthesis['total_cost'] += result.get('cost', 0.0)
            synthesis['total_duration'] += result.get('duration', 0.0)
            synthesis['models_used'].append(result.get('model', 'unknown'))

    # Extract best solution (prioritize official sources)
    if perplexity_result and perplexity_result.get('success'):
        synthesis['best_solution'] = perplexity_result.get('findings', '')[:1000]

    # Extract gotchas from community intelligence
    if context7_result and 'gotcha' in context7_result.get('findings', '').lower():
        synthesis['gotchas'].append("See community intelligence section for gotchas")

    # Extract edge cases from adversarial analysis
    if grok_result and 'edge case' in grok_result.get('analysis', '').lower():
        synthesis['edge_cases'].append("See adversarial validation section for edge cases")

    return synthesis


def generate_research_report(vuln_id, vuln_context, findings, output_file):
    """
    Generate markdown research report

    Format:
        # VULN-XXX Remediation Research
        ## Vulnerability Context
        ## Official Sources (Perplexity)
        ## Community Intelligence (Context7)
        ## Adversarial Validation (Grok)
        ## Final Recommendation
        ## Research Metadata
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report = f"""# {vuln_id} - Remediation Research Report

**Generated:** {timestamp}
**Research Method:** Multi-Model OSINT (Perplexity + Context7 + Grok)
**Total Cost:** ${findings['total_cost']:.4f}
**Total Duration:** {findings['total_duration']:.2f}s

---

## Vulnerability Context

- **Type:** {vuln_context.get('vuln_type', 'N/A')}
- **CWE:** {vuln_context.get('cwe_id', 'N/A')}
- **CVSS:** {vuln_context.get('cvss', 'N/A')}
- **Language:** {vuln_context.get('language', 'N/A')}
- **Framework:** {vuln_context.get('framework', 'N/A')}

**Description:**
{vuln_context.get('description', 'N/A')}

---

## Research Phase 1: Official Sources (Perplexity)

**Model:** `perplexity/llama-3.1-sonar-large-128k-online`
**Sources:** OWASP, NIST, CWE, Vendor Documentation

{findings['official_guidance']}

---

## Research Phase 2: Community Intelligence (Context7)

**Model:** `context7/web-search`
**Sources:** Reddit, GitHub, Stack Overflow, Security Blogs

{findings['community_validation']}

---

## Research Phase 3: Adversarial Validation (Grok)

**Model:** `x-ai/grok-2-1212`
**Analysis:** Red Team Perspective

{findings['adversarial_analysis']}

---

## Final Recommendation

**Best Solution (Synthesized):**

{findings['best_solution']}

**Key Gotchas:**
{chr(10).join(f"- {g}" for g in findings['gotchas']) if findings['gotchas'] else "- None identified"}

**Edge Cases to Consider:**
{chr(10).join(f"- {e}" for e in findings['edge_cases']) if findings['edge_cases'] else "- None identified"}

---

## Research Metadata

- **Models Used:** {', '.join(findings['models_used'])}
- **Total API Calls:** {len(findings['models_used'])}
- **Total Cost:** ${findings['total_cost']:.4f}
- **Total Time:** {findings['total_duration']:.2f} seconds
- **Research Depth:** Multi-model validation (Official + Community + Adversarial)

---

## Next Steps

1. Review findings above
2. Generate code patch: `python tools/security/remediation/generate-fix.py --research {output_file}`
3. Test fix in isolation: `python tools/security/remediation/test-fix.py --patch fix.patch`
4. Apply with backup: `python tools/security/remediation/apply-fix.py --patch fix.patch`
5. Validate in production: `python tools/security/remediation/validate-fix.py --vuln {vuln_id}`

---

*Research conducted by Intelligence Adjacent remediation system*
*Report format: v1.0*
"""

    # Write report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return report


def main():
    parser = argparse.ArgumentParser(
        description='Multi-model OSINT research for vulnerability remediation'
    )
    parser.add_argument(
        '--vuln',
        required=True,
        help='Vulnerability ID (e.g., VULN-001)'
    )
    parser.add_argument(
        '--engagement',
        required=True,
        help='Engagement directory path'
    )
    parser.add_argument(
        '--research-depth',
        choices=['quick', 'standard', 'comprehensive'],
        default='standard',
        help='Research thoroughness level (affects token limits)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output research report path'
    )
    parser.add_argument(
        '--skip-context7',
        action='store_true',
        help='Skip Context7 (if unavailable)'
    )
    parser.add_argument(
        '--skip-grok',
        action='store_true',
        help='Skip Grok (if unavailable)'
    )

    args = parser.parse_args()

    print(f"[*] Starting multi-model research for {args.vuln}")
    print(f"[*] Research depth: {args.research_depth}")
    print()

    # Initialize OpenRouter client
    try:
        client = OpenRouterClient(timeout=120)
        print(f"[+] OpenRouter client initialized")
    except Exception as e:
        print(f"[!] Failed to initialize OpenRouter client: {e}")
        return 1

    # Find vulnerability file
    engagement_path = Path(args.engagement)
    findings_dir = engagement_path / '05-findings'

    if not findings_dir.exists():
        print(f"[!] Findings directory not found: {findings_dir}")
        return 1

    # Glob for vulnerability file
    vuln_files = list(findings_dir.glob(f"{args.vuln}*.md"))
    if not vuln_files:
        print(f"[!] Vulnerability file not found: {findings_dir}/{args.vuln}*.md")
        return 1

    vuln_file = vuln_files[0]
    print(f"[+] Found vulnerability file: {vuln_file.name}")

    # Extract context
    print(f"\n[*] Extracting vulnerability context...")
    vuln_context = extract_vulnerability_context(vuln_file)

    if not vuln_context:
        print(f"[!] Failed to extract vulnerability context")
        return 1

    print(f"[+] Type: {vuln_context.get('vuln_type', 'Unknown')}")
    print(f"[+] CWE: {vuln_context.get('cwe_id', 'Unknown')}")
    print(f"[+] Language: {vuln_context.get('language', 'Unknown')}")

    # Research Phase 1: Perplexity (Official)
    print(f"\n[*] Research Phase 1/3: Official Sources")
    perplexity_result = query_perplexity(client, vuln_context)

    if perplexity_result.get('success'):
        print(f"[+] Perplexity complete ({perplexity_result['duration']:.2f}s, ${perplexity_result['cost']:.4f})")
    else:
        print(f"[!] Perplexity failed: {perplexity_result.get('error', 'Unknown error')}")
        print(f"[!] Continuing with limited research...")

    # Research Phase 2: Context7 (Community)
    context7_result = None
    if not args.skip_context7:
        print(f"\n[*] Research Phase 2/3: Community Intelligence")
        context7_result = query_context7(client, vuln_context)

        if context7_result.get('success'):
            print(f"[+] Context7 complete ({context7_result['duration']:.2f}s, ${context7_result['cost']:.4f})")
        else:
            print(f"[!] Context7 failed: {context7_result.get('error', 'Unknown error')}")
            context7_result = None
    else:
        print(f"\n[*] Research Phase 2/3: Skipped (--skip-context7)")

    # Synthesize initial findings for Grok
    print(f"\n[*] Synthesizing findings for adversarial review...")
    initial_synthesis = synthesize_findings(perplexity_result, context7_result, None)
    proposed_fix = initial_synthesis.get('best_solution', 'No solution synthesized')

    # Research Phase 3: Grok (Adversarial)
    grok_result = None
    if not args.skip_grok:
        print(f"\n[*] Research Phase 3/3: Adversarial Validation")
        grok_result = query_grok(client, vuln_context, proposed_fix)

        if grok_result.get('success'):
            print(f"[+] Grok complete ({grok_result['duration']:.2f}s, ${grok_result['cost']:.4f})")
        else:
            print(f"[!] Grok failed: {grok_result.get('error', 'Unknown error')}")
            grok_result = None
    else:
        print(f"\n[*] Research Phase 3/3: Skipped (--skip-grok)")

    # Final Synthesis
    print(f"\n[*] Synthesizing all findings...")
    final_findings = synthesize_findings(perplexity_result, context7_result, grok_result)

    # Generate report
    print(f"[*] Generating research report...")
    report = generate_research_report(args.vuln, vuln_context, final_findings, args.output)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Research Complete - {args.vuln}")
    print(f"{'='*60}")
    print(f"Report: {args.output}")
    print(f"Models: {', '.join(final_findings['models_used'])}")
    print(f"Cost: ${final_findings['total_cost']:.4f}")
    print(f"Duration: {final_findings['total_duration']:.2f}s")
    print(f"\n[+] Next: Generate code patch from research findings")

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
