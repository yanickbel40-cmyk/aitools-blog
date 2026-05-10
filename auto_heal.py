#!/usr/bin/env python3
"""
AI Toolbox Pro — Auto Healer & Monitor
Runs every 2 hours, tests ALL pages, auto-fixes broken links, reports issues
"""

import os
import json
import glob
import subprocess
import re
import sys
from datetime import datetime

BLOG_DIR = "/root/.openclaw/workspace/aitools-blog"
BASE_URL = "https://yanickbel40-cmyk.github.io/aitools-blog"
LOG_FILE = os.path.join(BLOG_DIR, "monitor.log")

# Pages to check every cycle
CRITICAL_PAGES = [
    "/",
    "/index.html",
    "/about.html",
    "/contact.html",
    "/privacy.html",
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def check_url(path):
    """Returns (status_code, is_ok)"""
    url = f"{BASE_URL}{path}"
    try:
        import urllib.request
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, True
    except Exception as e:
        code = getattr(e, 'code', None) or 0
        return code, False

def test_all_pages():
    """Test all known pages and return broken ones"""
    broken = []
    
    # Critical pages
    for path in CRITICAL_PAGES:
        code, ok = check_url(path)
        if not ok:
            broken.append({"path": path, "code": code, "type": "page"})
    
    # All article pages from posts.json
    posts_file = os.path.join(POSTS_DIR, "posts.json")
    if os.path.exists(posts_file):
        with open(posts_file) as f:
            posts = json.load(f)
        for post in posts:
            url_path = "/" + post['url'] if not post['url'].startswith('/') else post['url']
            code, ok = check_url(url_path)
            if not ok:
                broken.append({"path": url_path, "code": code, "type": "article"})
    
    # Check all HTML files on disk that should exist
    for html_file in glob.glob(os.path.join(POSTS_DIR, "**/*.html"), recursive=True):
        rel = os.path.relpath(html_file, BLOG_DIR)
        url_path = "/" + rel
        code, ok = check_url(url_path)
        if not ok:
            broken.append({"path": url_path, "code": code, "type": "orphan"})
    
    # Assets
    assets = ["/assets/pro-scripts.js", "/assets/pro-styles.css", "/manifest.json", "/robots.txt", "/sitemap.xml"]
    for path in assets:
        code, ok = check_url(path)
        if not ok:
            broken.append({"path": path, "code": code, "type": "asset"})
    
    return broken

def fix_broken_links():
    """Scan all HTML files and fix broken internal links"""
    fixes = 0
    for html_file in glob.glob(os.path.join(BLOG_DIR, "**/*.html"), recursive=True):
        with open(html_file, 'r') as f:
            content = f.read()
        
        original = content
        
        # Fix common broken patterns
        fixes_map = {
            # Double slash in paths
            '//aitools-blog/': '/aitools-blog/',
            # Wrong user prefix
            'yanissabile.github.io': 'yanickbel40-cmyk.github.io',
            # Missing base path
            'href="posts/': 'href="/aitools-blog/posts/',
            # Wrong home link
            'href="../aitools-blog/"': 'href="/aitools-blog/"',
            'href="../../aitools-blog/"': 'href="/aitools-blog/"',
            # Script src
            'src="assets/': 'src="/aitools-blog/assets/',
            # Style href
            'href="assets/': 'href="/aitools-blog/assets/',
            # Canonical
            'href="https://yanickbel40-cmyk.github.io/aitools-blog/">': 'href="/aitools-blog/">',
        }
        
        for old, new in fixes_map.items():
            content = content.replace(old, new)
        
        if content != original:
            with open(html_file, 'w') as f:
                f.write(content)
            fixes += 1
    
    return fixes

def fix_articles_from_generator():
    """Regenerate 2 fresh articles if articles are broken"""
    log("🔄 Running auto_content.py to replenish articles...")
    result = subprocess.run(
        ["python3", "auto_content.py"],
        cwd=BLOG_DIR,
        capture_output=True, text=True,
        timeout=30
    )
    return result.returncode == 0

def git_push_if_changed():
    """Commit and push any fixes"""
    status = subprocess.run(["git", "status", "--porcelain"], cwd=BLOG_DIR, capture_output=True, text=True)
    if status.stdout.strip():
        log("📦 Changes detected, pushing fixes...")
        subprocess.run(["git", "add", "-A"], cwd=BLOG_DIR)
        subprocess.run(["git", "commit", "-m", f"Auto-heal: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], cwd=BLOG_DIR)
        result = subprocess.run(["git", "push"], cwd=BLOG_DIR, capture_output=True, text=True)
        log(f"📤 Push: {result.stdout[:100] if result.stdout else 'OK'}")
        return True
    return False

def run_health_check():
    """Full health check cycle"""
    log("🚀 Starting health check...")
    
    # 1. Test all pages
    log("🔍 Testing all pages...")
    broken = test_all_pages()
    
    total_pages = len(CRITICAL_PAGES) + len(glob.glob(os.path.join(POSTS_DIR, "**/*.html"), recursive=True))
    log(f"📊 Pages tested: {total_pages}, Broken: {len(broken)}")
    
    if broken:
        log(f"⚠️ Found {len(broken)} broken URL(s):")
        for b in broken[:10]:
            log(f"   ❌ {b['code']} → {b['path']}")
        
        # 2. Auto-fix
        log("🔧 Running auto-fix...")
        fix_count = fix_broken_links()
        log(f"🔧 Fixed {fix_count} broken links in HTML")
        
        # 3. If still broken, regenerate
        remaining = test_all_pages()
        if remaining:
            log(f"⚠️ {len(remaining)} still broken, regenerating 2 articles...")
            fix_articles_from_generator()
        
        # 4. Push
        git_push_if_changed()
    else:
        log("✅ All pages OK!")
    
    # 5. Summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_pages": total_pages,
        "broken": len(broken),
        "fixed": False
    }
    
    summary_file = os.path.join(BLOG_DIR, "last_health.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f)
    
    return summary

if __name__ == "__main__":
    POSTS_DIR = os.path.join(BLOG_DIR, "posts")
    summary = run_health_check()
    
    # Exit with code 1 if broken pages remain
    if summary['broken'] > 0:
        log(f"❌ {summary['broken']} pages still broken after auto-fix")
        sys.exit(1)
    else:
        log("✅ Health check complete, all good!")
        sys.exit(0)
