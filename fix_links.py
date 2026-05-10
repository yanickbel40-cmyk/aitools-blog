#!/usr/bin/env python3
"""
AI Toolbox Pro — Fix all paths for GitHub Pages
Ensures every link, asset, form and meta URL works
"""

import os
import glob
import re

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://yanickbel40-cmyk.github.io/aitools-blog"

def fix_file_paths(filepath):
    """Fix all relative paths in HTML files"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    filename = os.path.basename(filepath)
    
    # Fix root-relative paths: /aitools-blog/ is the base
    # When deployed at /aitools-blog/, we need all links to start with /aitools-blog/
    
    # Fix 1: Home links — make sure they point to /aitools-blog/
    content = re.sub(r'href="/(?!aitools-blog)', 'href="/aitools-blog/', content)
    content = re.sub(r'href=\'/(?!aitools-blog)', 'href=\'/aitools-blog/', content)
    
    # Fix 2: Asset paths (js, css, images)
    content = re.sub(r'src="/', 'src="/aitools-blog/', content)
    content = re.sub(r"src='/", "src='/aitools-blog/", content)
    
    # Fix 3: Canonical URLs
    content = re.sub(
        r'href="https://yanissabile\.github\.io/',
        'href="https://yanickbel40-cmyk.github.io/aitools-blog/',
        content
    )
    
    # Fix 4: nav links from header on subpages
    content = re.sub(r'href="/aitools-blog/posts/', 'href="posts/', content)
    
    # Fix 5: Back to home on article pages
    content = re.sub(r'href="/aitools-blog/"', 'href="../"', content)
    
    # Write if changed
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def rebuild_index_with_correct_links():
    """Rebuild index.html with correct paths"""
    index_path = os.path.join(BLOG_DIR, "index.html")
    
    with open(index_path, 'r') as f:
        index = f.read()
    
    # Fix nav links in header
    index = index.replace('href="/">Home</a>', 'href="/aitools-blog/">Home</a>')
    index = index.replace('href="posts/reviews/', 'href="/aitools-blog/posts/reviews/')
    index = index.replace('href="posts/guides/', 'href="/aitools-blog/posts/guides/')
    index = index.replace('href="posts/comparisons/', 'href="/aitools-blog/posts/comparisons/')
    index = index.replace('href="posts/trends/', 'href="/aitools-blog/posts/trends/')
    index = index.replace('href="posts/monetization/', 'href="/aitools-blog/posts/monetization/')
    
    # Fix the CTA button
    index = index.replace('href="posts/guides/best-ai-productivity-tools-2026.html"', 'href="/aitools-blog/posts/guides/best-ai-productivity-tools-2026.html"')
    
    # Fix newsletter form action
    index = index.replace('action="https://formspree.io/f/your-form-id"', 'action="#"')
    
    # Fix fetch path for posts.json
    index = index.replace("fetch('posts/posts.json')", "fetch('/aitools-blog/posts/posts.json')")
    
    with open(index_path, 'w') as f:
        f.write(index)
    
    print(f"✓ Fixed index.html")

def fix_extra_pages():
    """Fix about, contact, privacy pages"""
    for page in ['about.html', 'contact.html', 'privacy.html']:
        filepath = os.path.join(BLOG_DIR, page)
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Fix home links
        content = content.replace('href="/aitools-blog/"', 'href="../"')
        content = content.replace('href="/aitools-blog/', 'href="../')
        content = content.replace('href="../">Home', 'href="./">Home')
        content = content.replace('href="../about.html', 'href="about.html')
        content = content.replace('href="../contact.html', 'href="contact.html')
        content = content.replace('href="../privacy.html', 'href="privacy.html')
        
        # Fix asset paths
        content = content.replace('href="/aitools-blog/assets/', 'href="assets/')
        content = content.replace('/aitools-blog/assets/pro-styles.css', '../assets/pro-styles.css')
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Fixed {page}")

def fix_article_links():
    """Fix links inside article pages"""
    for html_file in sorted(glob.glob(os.path.join(BLOG_DIR, "posts/**/*.html"), recursive=True)):
        with open(html_file, 'r') as f:
            content = f.read()
        
        original = content
        rel_dir = os.path.relpath(BLOG_DIR, os.path.dirname(html_file))
        
        if rel_dir == '.':
            rel_dir = '..'
        
        # Fix back to home link
        content = content.replace(
            'href="/aitools-blog/">← AI Toolbox Pro</a>',
            'href="../../">← AI Toolbox Pro</a>'
        )
        content = content.replace(
            'href="/aitools-blog/" class="back">← Back to Home',
            f'href="../../" class="back">← Back to Home'
        )
        
        # Fix asset links
        content = content.replace(
            'href="/aitools-blog/assets/pro-styles.css"',
            f'href="{rel_dir}/assets/pro-styles.css"'
        )
        content = content.replace(
            'src="/aitools-blog/assets/pro-scripts.js"',
            f'src="{rel_dir}/assets/pro-scripts.js"'
        )
        
        # Fix affiliate links
        content = content.replace(
            'href="/aitools-blog/posts/monetization/best-ai-affiliate-programs-2026.html"',
            f'href="{rel_dir}/posts/monetization/best-ai-affiliate-programs-2026.html"'
        )
        
        # Fix related posts JS
        content = content.replace(
            "fetch('/aitools-blog/posts/posts.json')",
            f"fetch('{rel_dir}/posts/posts.json')"
        )
        
        # Fix PWA links
        content = content.replace(
            'href="/aitools-blog/manifest.json"',
            f'href="{rel_dir}/manifest.json"'
        )
        content = content.replace(
            '"serviceWorker" in navigator',
            '"serviceWorker" in navigator'
        )
        content = content.replace(
            'navigator.serviceWorker.register("/aitools-blog/sw.js")',
            f'navigator.serviceWorker.register("{rel_dir}/sw.js")'
        )
        
        # Fix canonical URL
        content = re.sub(
            r'href="https://yanickbel40-cmyk\.github\.io/aitools-blog/posts/',
            'href="https://yanickbel40-cmyk.github.io/aitools-blog/posts/',
            content
        )
        
        # Fix breadcrumb link
        content = content.replace(
            'href="/aitools-blog/">Home',
            f'href="{rel_dir}/">Home'
        )
        
        # Fix og:url
        content = re.sub(
            r'property="og:url" content="https://yanickbel40-cmyk\.github\.io/aitools-blog/([^"]+)"',
            f'property="og:url" content="https://yanickbel40-cmyk.github.io/aitools-blog/\\1"',
            content
        )
        
        if content != original:
            with open(html_file, 'w') as f:
                f.write(content)
    
    print(f"✓ Fixed article links ({len(list(glob.glob(os.path.join(BLOG_DIR, 'posts/**/*.html'), recursive=True)))} files)")

def fix_pro_scripts():
    """Fix script paths for related posts loader"""
    script_path = os.path.join(BLOG_DIR, "assets/pro-scripts.js")
    with open(script_path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        "fetch('/aitools-blog/posts/posts.json')",
        "fetch(window.location.pathname.replace('/posts/', '/posts/posts.json').replace(/article\/.*/, '') + '../posts/posts.json')"
    )
    content = content.replace(
        'p.url !== window.location.pathname.replace("/aitools-blog/", "")',
        '!window.location.pathname.includes(p.url)'
    )
    
    # Fix related posts links
    content = content.replace(
        'href="/aitools-blog/${p.url}"',
        'href="${p.url}"'
    )
    
    with open(script_path, 'w') as f:
        f.write(content)
    print("✓ Fixed pro-scripts.js paths")

def fix_sitemap():
    """Fix sitemap URLs"""
    sitemap_path = os.path.join(BLOG_DIR, "sitemap.xml")
    with open(sitemap_path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'https://yanissabile.github.io/aitools-blog/',
        'https://yanickbel40-cmyk.github.io/aitools-blog/'
    )
    
    with open(sitemap_path, 'w') as f:
        f.write(content)
    print("✓ Fixed sitemap.xml")

def fix_robots():
    """Fix robots.txt"""
    robots_path = os.path.join(BLOG_DIR, "robots.txt")
    with open(robots_path, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'yanissabile.github.io',
        'yanickbel40-cmyk.github.io'
    )
    
    with open(robots_path, 'w') as f:
        f.write(content)
    print("✓ Fixed robots.txt")

if __name__ == "__main__":
    rebuild_index_with_correct_links()
    fix_extra_pages()
    fix_article_links()
    fix_pro_scripts()
    fix_sitemap()
    fix_robots()
    
    # Also fix the posts.json path
    posts_json_path = os.path.join(BLOG_DIR, "posts/posts.json")
    with open(posts_json_path, 'r') as f:
        posts = f.read()
    
    # Fix URLs in posts.json
    posts = posts.replace('"url": "posts/', '"url": "./posts/')
    
    with open(posts_json_path, 'w') as f:
        f.write(posts)
    print("✓ Fixed posts.json paths")
    
    print("\n✅ ALL LINKS FIXED! Pushing to GitHub...")
    
    import subprocess
    subprocess.run(["git", "add", "-A"], cwd=BLOG_DIR)
    subprocess.run(["git", "commit", "-m", "Fix all paths, links and resources for GitHub Pages"], cwd=BLOG_DIR)
    subprocess.run(["git", "push"], cwd=BLOG_DIR)
    print("\n✅ Pushed! Wait 1-2 min and refresh the blog.")
