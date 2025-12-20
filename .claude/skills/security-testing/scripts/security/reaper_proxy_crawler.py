#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated proxy traffic collection using headless browser + Reaper proxy.

This script launches a headless browser configured to route all traffic through
Reaper's proxy (localhost:8080), automatically capturing HTTP requests/responses
for analysis.

Usage:
    # Basic crawl with authentication
    python reaper_proxy_crawler.py --url https://staging.airtable.com --cookies "session_id=abc123"

    # Login flow + crawl
    python reaper_proxy_crawler.py --url https://staging.airtable.com --login --username user@example.com --password "pass123"

    # Crawl with custom depth
    python reaper_proxy_crawler.py --url https://staging.airtable.com --depth 2 --max-pages 50

Prerequisites:
    uv pip install playwright
    playwright install chromium

    # Reaper must be running on localhost:8080
    docker-compose up -d  # (in reaper-mcp-server directory)
"""

import sys
import io
import argparse
import asyncio
import time
from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright

# Force UTF-8 encoding for Windows console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ReaperProxyCrawler:
    """Automated browser-based proxy traffic collector for Reaper."""

    def __init__(self, base_url, proxy_url="http://127.0.0.1:8080",
                 max_pages=20, depth=1, headless=True):
        self.base_url = base_url
        self.proxy_url = proxy_url
        self.max_pages = max_pages
        self.depth = depth
        self.headless = headless
        self.visited_urls = set()
        self.domain = urlparse(base_url).netloc

    async def crawl(self, cookies=None, auth_token=None, login_flow=None):
        """
        Start crawling with optional authentication.

        Args:
            cookies: Dict of cookies to set (e.g., {"session_id": "abc123"})
            auth_token: Bearer token for Authorization header
            login_flow: Dict with login credentials {"username": "...", "password": "...",
                       "username_selector": "#email", "password_selector": "#password",
                       "submit_selector": "button[type=submit]"}
        """
        async with async_playwright() as p:
            print(f"[+] Launching browser with Reaper proxy ({self.proxy_url})...")

            browser = await p.chromium.launch(
                headless=self.headless,
                proxy={"server": self.proxy_url}
            )

            context = await browser.new_context(
                ignore_https_errors=True,  # Accept Reaper's CA cert
                extra_http_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )

            # Add authorization header if provided
            if auth_token:
                await context.set_extra_http_headers({"Authorization": f"Bearer {auth_token}"})

            page = await context.new_page()

            # Set cookies if provided
            if cookies:
                cookie_list = [{"name": k, "value": v, "domain": self.domain, "path": "/"}
                              for k, v in cookies.items()]
                await context.add_cookies(cookie_list)
                print(f"[+] Added {len(cookie_list)} cookies")

            # Perform login flow if specified
            if login_flow:
                await self._perform_login(page, login_flow)

            # Start crawling
            print(f"[+] Starting crawl from {self.base_url}")
            print(f"    Max pages: {self.max_pages}, Max depth: {self.depth}")

            await self._crawl_recursive(page, self.base_url, 0)

            print(f"\n[+] Crawl complete!")
            print(f"    Pages visited: {len(self.visited_urls)}")
            print(f"    All traffic captured in Reaper database")
            print(f"\n[+] Next steps:")
            print(f"    1. Analyze with: analyze_bola_vulnerabilities(hostname='{self.domain}')")
            print(f"    2. Check injection points: analyze_injection_points(hostname='{self.domain}')")
            print(f"    3. Generate report: generate_report(hostname='{self.domain}')")

            await browser.close()

    async def _perform_login(self, page, login_flow):
        """Perform login flow to get authenticated session."""
        print(f"[+] Performing login at {self.base_url}")

        try:
            await page.goto(self.base_url, wait_until="networkidle", timeout=30000)

            # Fill username
            username_selector = login_flow.get("username_selector", "input[type=email]")
            await page.fill(username_selector, login_flow["username"])
            print(f"    [+] Filled username field")

            # Fill password
            password_selector = login_flow.get("password_selector", "input[type=password]")
            await page.fill(password_selector, login_flow["password"])
            print(f"    [+] Filled password field")

            # Click submit and wait for navigation
            submit_selector = login_flow.get("submit_selector", "button[type=submit]")
            await page.click(submit_selector)
            print(f"    [+] Clicked submit button")

            # Wait for navigation after login
            await page.wait_for_load_state("networkidle", timeout=15000)
            print(f"    [+] Login successful")

        except Exception as e:
            print(f"    [-] Login failed: {e}")
            print(f"    [!] Continuing with unauthenticated session")

    async def _crawl_recursive(self, page, url, current_depth):
        """Recursively crawl pages up to max_depth."""

        # Check limits
        if len(self.visited_urls) >= self.max_pages:
            return
        if current_depth > self.depth:
            return
        if url in self.visited_urls:
            return

        # Only crawl same domain
        if urlparse(url).netloc != self.domain:
            return

        try:
            print(f"    [{len(self.visited_urls)+1}/{self.max_pages}] Visiting: {url}")
            self.visited_urls.add(url)

            # Navigate to page (all traffic captured by Reaper)
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait a bit for any AJAX requests
            await page.wait_for_timeout(2000)

            # If we haven't reached max depth, extract and follow links
            if current_depth < self.depth:
                links = await page.query_selector_all("a[href]")
                for link in links[:20]:  # Limit links per page to avoid explosion
                    href = await link.get_attribute("href")
                    if href:
                        absolute_url = urljoin(url, href)
                        # Skip anchors, mailto, tel, javascript
                        if not any(absolute_url.startswith(x) for x in ["#", "mailto:", "tel:", "javascript:"]):
                            await self._crawl_recursive(page, absolute_url, current_depth + 1)
                            if len(self.visited_urls) >= self.max_pages:
                                break

        except Exception as e:
            print(f"    [-] Error visiting {url}: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="Automated proxy traffic collection with headless browser + Reaper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic crawl with cookies
  python reaper_proxy_crawler.py --url https://staging.airtable.com --cookies "session_id=abc123"

  # Login flow + crawl
  python reaper_proxy_crawler.py --url https://staging.airtable.com --login \\
      --username user@example.com --password "pass123" \\
      --username-selector "#email" --password-selector "#password"

  # Deep crawl with auth token
  python reaper_proxy_crawler.py --url https://api.example.com --auth-token "Bearer abc123" \\
      --depth 3 --max-pages 100

Prerequisites:
  - Reaper must be running: docker-compose up -d
  - Playwright installed: uv pip install playwright && playwright install chromium
        """
    )

    parser.add_argument("--url", required=True, help="Base URL to crawl")
    parser.add_argument("--proxy", default="http://127.0.0.1:8080", help="Reaper proxy URL (default: http://127.0.0.1:8080)")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum pages to visit (default: 20)")
    parser.add_argument("--depth", type=int, default=1, help="Maximum crawl depth (default: 1)")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode (default: True)")
    parser.add_argument("--visible", action="store_true", help="Run with visible browser (for debugging)")

    # Authentication options
    auth_group = parser.add_argument_group("Authentication Options")
    auth_group.add_argument("--cookies", help="Cookies as key=value pairs, comma-separated (e.g., 'session_id=abc,token=xyz')")
    auth_group.add_argument("--auth-token", help="Bearer token for Authorization header")
    auth_group.add_argument("--login", action="store_true", help="Perform login flow")
    auth_group.add_argument("--username", help="Username for login flow")
    auth_group.add_argument("--password", help="Password for login flow")
    auth_group.add_argument("--username-selector", default="input[type=email]", help="CSS selector for username field")
    auth_group.add_argument("--password-selector", default="input[type=password]", help="CSS selector for password field")
    auth_group.add_argument("--submit-selector", default="button[type=submit]", help="CSS selector for submit button")

    args = parser.parse_args()

    # Validate
    if args.login and (not args.username or not args.password):
        parser.error("--login requires --username and --password")

    # Parse cookies
    cookies = None
    if args.cookies:
        cookies = {}
        for pair in args.cookies.split(","):
            k, v = pair.strip().split("=", 1)
            cookies[k.strip()] = v.strip()

    # Prepare login flow
    login_flow = None
    if args.login:
        login_flow = {
            "username": args.username,
            "password": args.password,
            "username_selector": args.username_selector,
            "password_selector": args.password_selector,
            "submit_selector": args.submit_selector
        }

    # Create crawler
    crawler = ReaperProxyCrawler(
        base_url=args.url,
        proxy_url=args.proxy,
        max_pages=args.max_pages,
        depth=args.depth,
        headless=not args.visible
    )

    # Start crawl
    print("[+] Reaper Proxy Crawler")
    print("=" * 60)
    await crawler.crawl(cookies=cookies, auth_token=args.auth_token, login_flow=login_flow)


if __name__ == "__main__":
    asyncio.run(main())
