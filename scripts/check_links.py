#!/usr/bin/env python3
"""Extract all URLs from guide.md and check each with HEAD/GET."""

import re
import sys
import requests

def extract_urls(filepath):
    with open(filepath) as f:
        text = f.read()
    return list(set(re.findall(r'https?://[^\s\)\]>"]+', text)))

def check_url(url):
    try:
        r = requests.head(url, timeout=10, allow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code >= 400:
            r = requests.get(url, timeout=10, allow_redirects=True,
                           headers={"User-Agent": "Mozilla/5.0"})
        return r.status_code, r.url if r.url != url else None
    except requests.RequestException as e:
        return None, str(e)

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "guide.md"
    urls = extract_urls(filepath)
    print(f"Found {len(urls)} unique URLs\n")

    broken, redirected, ok = [], [], []
    for url in sorted(urls):
        status, info = check_url(url)
        if status is None:
            broken.append((url, info))
            print(f"  BROKEN  {url}\n          {info}")
        elif status >= 400:
            broken.append((url, status))
            print(f"  {status}  {url}")
        elif info:
            redirected.append((url, info))
            print(f"  REDIR   {url}\n       -> {info}")
        else:
            ok.append(url)
            print(f"  OK      {url}")

    print(f"\n--- Summary ---")
    print(f"OK: {len(ok)}  Redirected: {len(redirected)}  Broken: {len(broken)}")
    return 1 if broken else 0

if __name__ == "__main__":
    sys.exit(main())
