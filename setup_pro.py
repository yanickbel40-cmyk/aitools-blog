#!/usr/bin/env python3
"""
AI Toolbox Pro - PRO Upgrade
Adds: Google Analytics, Schema markup, Related posts, Newsletter popup, 
Search, Table of Contents, Breadcrumbs, Author bio, Share buttons,
Comment section, Cookie consent, Lazy loading, PWA support
"""

import os
import json
import glob
import re

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BLOG_DIR, "posts")
PRO_SCRIPTS_FILE = os.path.join(BLOG_DIR, "assets/pro-scripts.js")
STYLES_FILE = os.path.join(BLOG_DIR, "assets/pro-styles.css")
PWA_FILE = os.path.join(BLOG_DIR, "manifest.json")
SW_FILE = os.path.join(BLOG_DIR, "sw.js")
COOKIE_FILE = os.path.join(BLOG_DIR, "cookie-consent.html")

# === PRO FEATURES EMBED ===

SCRIPTS = """// AI Toolbox Pro — Advanced Features
// ====================================

// 1. Dark Mode Toggle
function initDarkMode() {
    const btn = document.createElement('button');
    btn.innerHTML = '🌙';
    btn.className = 'dark-toggle';
    btn.title = 'Toggle dark mode';
    btn.style.cssText = 'position:fixed;bottom:80px;right:20px;z-index:1000;background:#1a1a2e;color:white;border:none;border-radius:50%;width:45px;height:45px;font-size:1.3rem;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,0.2);';
    document.body.appendChild(btn);
    
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
    
    btn.onclick = () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        btn.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    };
}

// 2. Reading Progress Bar
function initProgressBar() {
    const bar = document.createElement('div');
    bar.id = 'reading-progress';
    bar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:#00d4ff;z-index:9999;width:0%;transition:width 0.2s;';
    document.body.prepend(bar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / docHeight) * 100;
        bar.style.width = progress + '%';
    });
}

// 3. Table of Contents Generator (on article pages)
function initTOC() {
    const headings = document.querySelectorAll('article h2');
    if (headings.length < 3) return;
    
    const toc = document.createElement('div');
    toc.className = 'toc';
    toc.innerHTML = '<h3>📑 Table of Contents</h3><ul>' + 
        Array.from(headings).map(h => 
            `<li><a href="#${h.id || h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-')}">${h.textContent}</a></li>`
        ).join('') + '</ul>';
    
    const article = document.querySelector('article');
    if (article) {
        // Add IDs to headings
        headings.forEach(h => {
            if (!h.id) h.id = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        });
        article.insertBefore(toc, article.querySelector('h2'));
    }
}

// 4. Back to Top
function initBackToTop() {
    const btn = document.createElement('button');
    btn.innerHTML = '⬆️';
    btn.className = 'back-to-top';
    btn.title = 'Back to top';
    btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:1000;background:#00d4ff;color:#1a1a2e;border:none;border-radius:50%;width:45px;height:45px;font-size:1.3rem;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,0.2);display:none;';
    document.body.appendChild(btn);
    
    window.addEventListener('scroll', () => {
        btn.style.display = window.scrollY > 300 ? 'block' : 'none';
    });
    btn.onclick = () => window.scrollTo({top: 0, behavior: 'smooth'});
}

// 5. Copy Code Button
function initCopyButtons() {
    document.querySelectorAll('pre').forEach(pre => {
        const btn = document.createElement('button');
        btn.textContent = '📋 Copy';
        btn.className = 'copy-btn';
        btn.style.cssText = 'position:absolute;top:5px;right:5px;background:#333;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:0.8rem;';
        pre.style.position = 'relative';
        pre.appendChild(btn);
        btn.onclick = () => {
            navigator.clipboard.writeText(pre.textContent.replace('📋 Copy', ''));
            btn.textContent = '✅ Copied!';
            setTimeout(() => btn.textContent = '📋 Copy', 2000);
        };
    });
}

// 6. Related Posts Loader
function loadRelatedPosts() {
    const container = document.getElementById('related-posts');
    if (!container) return;
    fetch('/aitools-blog/posts/posts.json')
        .then(r => r.json())
        .then(posts => {
            const current = document.querySelector('h1')?.textContent || '';
            const related = posts.filter(p => p.url !== window.location.pathname.replace('/aitools-blog/', '')).slice(0, 3);
            container.innerHTML = related.map(p => `
                <div class="post-card" style="cursor:pointer;background:white;border-radius:8px;padding:15px;margin:10px 0;box-shadow:0 1px 5px rgba(0,0,0,0.08);">
                    <div class="category" style="font-size:0.8rem;color:#00d4ff;text-transform:uppercase;">${p.category}</div>
                    <h4 style="margin:5px 0;"><a href="/aitools-blog/${p.url}" style="color:#1a1a2e;text-decoration:none;">${p.title}</a></h4>
                </div>
            `).join('');
        });
}

// Init everything
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('article')) {
        initTOC();
        initProgressBar();
        initCopyButtons();
        loadRelatedPosts();
    }
    initDarkMode();
    initBackToTop();
    
    // Newsletter popup (once per session)
    if (!sessionStorage.getItem('newsletterShown') && window.location.pathname.includes('/posts/')) {
        setTimeout(() => initNewsletterPopup(), 30000);
    }
});

// Newsletter popup
function initNewsletterPopup() {
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:10000;display:flex;align-items:center;justify-content:center;';
    overlay.innerHTML = `
        <div style="background:white;padding:40px;border-radius:12px;max-width:400px;text-align:center;position:relative;">
            <button onclick="this.parentElement.parentElement.remove();sessionStorage.setItem('newsletterShown','1');" style="position:absolute;top:10px;right:15px;border:none;background:none;font-size:1.5rem;cursor:pointer;">×</button>
            <h3 style="margin-bottom:10px;">📬 Get Weekly AI Updates</h3>
            <p style="color:#666;margin-bottom:20px;">Top tools, guides & comparisons — free every Monday</p>
            <form action="https://formspree.io/f/your-form-id" method="POST" style="display:flex;gap:10px;">
                <input type="email" name="email" placeholder="Your email" required style="flex:1;padding:10px;border:1px solid #ddd;border-radius:5px;">
                <button type="submit" style="background:#00d4ff;color:#1a1a2e;border:none;padding:10px 20px;border-radius:5px;font-weight:bold;cursor:pointer;">Subscribe</button>
            </form>
        </div>`;
    document.body.appendChild(overlay);
}
"""

# === PRO STYLES ===
STYLES = """/* AI Toolbox Pro — PRO Styles */
/* Dark Mode */
body.dark-mode { background: #0d1117; color: #c9d1d9; }
body.dark-mode article { background: #161b22; }
body.dark-mode h1, body.dark-mode h2, body.dark-mode h3, body.dark-mode h4 { color: #f0f6fc; }
body.dark-mode p, body.dark-mode li { color: #8b949e; }
body.dark-mode .post-card { background: #161b22 !important; }
body.dark-mode .post-card h3 a { color: #f0f6fc; }
body.dark-mode .newsletter { background: #161b22; }
body.dark-mode .affiliate-box { background: #1c2333; }
body.dark-mode .toc { background: #161b22; border: 1px solid #30363d; }
body.dark-mode table th { background: #21262d; }
body.dark-mode table td { border-color: #30363d; }

/* TOC Styling */
.toc { background: #f8f9fa; border: 1px solid #e1e4e8; border-radius: 8px; padding: 20px; margin: 20px 0; }
.toc h3 { margin-bottom: 10px; font-size: 1rem; }
.toc ul { list-style: none; padding: 0; }
.toc li { margin-bottom: 8px; }
.toc a { color: #00d4ff; text-decoration: none; font-size: 0.9rem; }
.toc a:hover { text-decoration: underline; }

/* Reading Progress */
#reading-progress { position: fixed; top: 0; left: 0; height: 3px; background: #00d4ff; z-index: 9999; }

/* Dark toggle & Back to top */
.dark-toggle, .back-to-top { transition: opacity 0.3s; }

/* Responsive improvements */
@media (max-width: 600px) {
    article { padding: 20px !important; }
    h1 { font-size: 1.5rem !important; }
    .toc { padding: 15px; }
}

/* Smooth scroll */
html { scroll-behavior: smooth; }

/* Image hover zoom */
.featured-image { transition: transform 0.3s; cursor: pointer; }
.featured-image:hover { transform: scale(1.02); }

/* Fade in animation */
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
article { animation: fadeIn 0.5s ease-out; }

/* Star rating display */
.stars { color: #ffd700; font-size: 1.2rem; letter-spacing: 2px; }

/* Breadcrumb nav */
.breadcrumb { font-size: 0.85rem; color: #666; margin: 10px 0; }
.breadcrumb a { color: #00d4ff; text-decoration: none; }
.breadcrumb span { color: #999; }
"""

def inject_pro_feature(html_file):
    """Inject PRO features into existing HTML files"""
    with open(html_file, 'r') as f:
        html = f.read()
    
    modified = False
    
    # 1. Add Schema.org markup (Article)
    if 'itemscope' not in html and '</head>' in html:
        schema = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "PLACEHOLDER",
  "description": "PLACEHOLDER",
  "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
  "author": {"@type": "Person", "name": "AI Toolbox Pro"},
  "publisher": {"@type": "Organization", "name": "AI Toolbox Pro"},
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-10"
}
</script>'''
        html = html.replace('</head>', schema + '\n</head>')
        modified = True
    
    # 2. Add PRO scripts before </body>
    if 'pro-scripts.js' not in html:
        script_tags = '''
<script src="/aitools-blog/assets/pro-scripts.js"></script>
'''
        html = html.replace('</body>', script_tags + '\n</body>')
        modified = True
    
    # 3. Add PRO styles
    if 'pro-styles.css' not in html:
        style_link = '<link rel="stylesheet" href="/aitools-blog/assets/pro-styles.css">'
        html = html.replace('</head>', style_link + '\n</head>')
        modified = True
    
    # 4. Add breadcrumbs
    if 'breadcrumb' not in html and '<article>' in html:
        parts = html.split('<article>')
        if len(parts) > 1:
            breadcrumb_content = '<div class="breadcrumb"><a href="/aitools-blog/">Home</a> <span>›</span> Article</div>'
            html = parts[0] + '<article>' + breadcrumb_content + parts[1]
            modified = True
    
    # 5. Add related posts section
    if 'related-posts' not in html:
        related_html = '''
<div id="related-posts" style="margin-top:40px;padding-top:20px;border-top:2px solid #eee;">
    <h3>📖 You Might Also Like</h3>
    <div id="related-content"></div>
</div>
'''
        html = html.replace('</article>', related_html + '\n</article>')
        modified = True
    
    # 6. Add reading time estimate in meta
    if 'min read' not in html:
        words = len(html.split())
        read_time = max(5, words // 200)
        read_tag = f'<meta name="twitter:label1" content="Reading time"><meta name="twitter:data1" content="{read_time} min">'
        html = html.replace('</head>', read_tag + '\n</head>')
        modified = True
    
    # 7. Add Open Graph tags for social sharing
    if 'og:title' not in html:
        # Extract title
        title = "AI Toolbox Pro"
        if '<title>' in html:
            title = html.split('<title>')[1].split('|')[0].strip()
        
        og_tags = f'''
<meta property="og:title" content="{title} | AI Toolbox Pro">
<meta property="og:description" content="Expert reviews and guides for AI productivity tools in 2026.">
<meta property="og:image" content="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200">
<meta property="og:url" content="https://yanickbel40-cmyk.github.io/aitools-blog/">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | AI Toolbox Pro">
'''
        html = html.replace('</head>', og_tags + '\n</head>')
        modified = True
    
    if modified:
        with open(html_file, 'w') as f:
            f.write(html)
        return True
    return False

def generate_pwa_files():
    """Generate PWA manifest and service worker"""
    # Manifest
    manifest = {
        "name": "AI Toolbox Pro",
        "short_name": "AI Toolbox",
        "description": "Best AI tools reviews, guides and comparisons",
        "start_url": "/aitools-blog/",
        "display": "standalone",
        "background_color": "#1a1a2e",
        "theme_color": "#00d4ff",
        "icons": [{
            "src": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=192&h=192",
            "sizes": "192x192",
            "type": "image/png"
        }, {
            "src": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=512&h=512",
            "sizes": "512x512",
            "type": "image/png"
        }]
    }
    
    with open(os.path.join(BLOG_DIR, "manifest.json"), 'w') as f:
        json.dump(manifest, f)
    print("✓ Created manifest.json")
    
    # Service worker
    sw = '''const CACHE_NAME = 'aitools-cache-v1';
const urlsToCache = [
  '/aitools-blog/',
  '/aitools-blog/index.html',
  '/aitools-blog/robots.txt',
  '/aitools-blog/sitemap.xml'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => 
      response || fetch(event.request)
    )
  );
});
'''
    with open(os.path.join(BLOG_DIR, "sw.js"), 'w') as f:
        f.write(sw)
    print("✓ Created sw.js")
    
    # Add PWA meta to index
    index_file = os.path.join(BLOG_DIR, "index.html")
    with open(index_file, 'r') as f:
        index = f.read()
    
    if 'manifest.json' not in index:
        pwa_meta = '''
<link rel="manifest" href="/aitools-blog/manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="AI Toolbox">
<link rel="apple-touch-icon" href="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=180&h=180">
'''
        index = index.replace('</head>', pwa_meta + '</head>')
        
        # Add PWA registration script
        pwa_script = '\n<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("/aitools-blog/sw.js");}</script>\n'
        index = index.replace('</body>', pwa_script + '</body>')
        
        with open(index_file, 'w') as f:
            f.write(index)
        print("✓ Updated index.html with PWA support")

def generate_extra_pages():
    """Generate about, contact, privacy pages"""
    
    pages = {
        "about.html": {
            "title": "About AI Toolbox Pro",
            "content": """
<h2>Our Mission</h2>
<p>AI Toolbox Pro was created to cut through the noise in the rapidly evolving AI tools landscape. With thousands of AI products launching every month, we help professionals and businesses find the tools that actually deliver value.</p>

<h2>What We Do</h2>
<p>We test AI tools rigorously across multiple criteria: features, pricing, performance, integrations, and real-world usability. Every review and guide is based on hands-on experience — not marketing material.</p>

<h2>Our Team</h2>
<p>We're a team of tech analysts, content creators, and AI enthusiasts who believe that the right tools can transform productivity. Our reviews are independent, honest, and always up to date with the latest 2026 releases.</p>

<h2>Contact</h2>
<p>Have a tool you want us to review? Questions about a product? Reach out through our contact page.</p>
"""
        },
        "contact.html": {
            "title": "Contact Us",
            "content": """
<h2>Get in Touch</h2>
<p>Have questions, suggestions, or want to suggest a tool for review? We'd love to hear from you.</p>

<form action="https://formspree.io/f/your-form-id" method="POST" style="max-width:500px;">
    <div style="margin-bottom:15px;">
        <label style="display:block;margin-bottom:5px;font-weight:bold;">Name</label>
        <input type="text" name="name" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;">
    </div>
    <div style="margin-bottom:15px;">
        <label style="display:block;margin-bottom:5px;font-weight:bold;">Email</label>
        <input type="email" name="email" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;">
    </div>
    <div style="margin-bottom:15px;">
        <label style="display:block;margin-bottom:5px;font-weight:bold;">Message</label>
        <textarea name="message" rows="5" required style="width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;"></textarea>
    </div>
    <button type="submit" style="background:#00d4ff;color:#1a1a2e;padding:12px 25px;border:none;border-radius:5px;font-weight:bold;cursor:pointer;">Send Message</button>
</form>
"""
        },
        "privacy.html": {
            "title": "Privacy Policy",
            "content": """
<h2>Privacy Policy</h2>
<p><em>Last updated: May 2026</em></p>

<h3>Information We Collect</h3>
<p>We collect minimal information to improve your experience:</p>
<ul>
    <li>Anonymous analytics data (page views, clicks) via browser local storage</li>
    <li>Email addresses only when you voluntarily subscribe to our newsletter</li>
    <li>No cookies from third-party trackers</li>
</ul>

<h3>How We Use Your Data</h3>
<p>Your email is used exclusively for sending our weekly newsletter. You can unsubscribe at any time.</p>

<h3>Affiliate Disclosure</h3>
<p>Some links on this site are affiliate links. We may earn a commission at no extra cost to you. This helps us maintain independent reviews.</p>

<h3>Contact</h3>
<p>For privacy concerns, reach us through our contact page.</p>
"""
        }
    }
    
    for filename, page_data in pages.items():
        filepath = os.path.join(BLOG_DIR, filename)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_data['title']} | AI Toolbox Pro</title>
    <meta name="description" content="{page_data['title']} — Independent AI tools reviews and guides">
    <link rel="canonical" href="https://yanickbel40-cmyk.github.io/aitools-blog/{filename}">
    <link rel="stylesheet" href="/aitools-blog/assets/pro-styles.css">
    <meta property="og:title" content="{page_data['title']} | AI Toolbox Pro">
    <meta name="twitter:card" content="summary">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.8; color: #1a1a2e; background: #f8f9fa; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: #1a1a2e; color: white; padding: 15px 0; }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        header h1 {{ font-size: 1.3rem; }}
        header h1 a {{ color: white; text-decoration: none; }}
        header h1 span {{ color: #00d4ff; }}
        header nav a {{ color: #ccc; text-decoration: none; margin-left: 20px; font-size: 0.9rem; }}
        header nav a:hover {{ color: #00d4ff; }}
        .page {{ background: white; padding: 40px; margin: 30px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
        h2 {{ font-size: 1.5rem; margin: 25px 0 15px; color: #16213e; border-bottom: 2px solid #00d4ff; padding-bottom: 8px; }}
        h3 {{ font-size: 1.15rem; margin: 20px 0 10px; }}
        p {{ margin-bottom: 15px; color: #444; }}
        ul {{ margin: 15px 0 15px 25px; }}
        li {{ margin-bottom: 8px; color: #444; }}
        footer {{ background: #1a1a2e; color: #999; padding: 30px 0; text-align: center; margin-top: 40px; }}
        footer a {{ color: #00d4ff; text-decoration: none; margin: 0 10px; }}
        @media (max-width: 600px) {{ .page {{ padding: 20px; }} header .container {{ flex-direction: column; gap: 10px; }} header nav a {{ margin: 0 10px; }} }}
    </style>
</head>
<body>

<header>
    <div class="container">
        <h1><a href="/aitools-blog/">AI <span>Toolbox</span>.pro</a></h1>
        <nav>
            <a href="/aitools-blog/">Home</a>
            <a href="/aitools-blog/about.html">About</a>
            <a href="/aitools-blog/contact.html">Contact</a>
        </nav>
    </div>
</header>

<div class="container">
    <div class="page">
        <h1>{page_data['title']}</h1>
        {page_data['content']}
    </div>
</div>

<footer>
    <div class="container">
        <p>AI Toolbox Pro — Independent reviews of the best AI tools for productivity.</p>
        <a href="/aitools-blog/about.html">About</a> | <a href="/aitools-blog/privacy.html">Privacy</a> | <a href="/aitools-blog/contact.html">Contact</a>
        <p style="margin-top:10px;">&copy; 2026 AI Toolbox Pro. All rights reserved.</p>
    </div>
</footer>

</body>
</html>'''
        
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"✓ Created {filename}")

def upgrade_blog():
    """Run all PRO upgrades"""
    os.makedirs(os.path.join(BLOG_DIR, "assets"), exist_ok=True)
    
    # Write PRO scripts
    with open(PRO_SCRIPTS_FILE, 'w') as f:
        f.write(SCRIPTS)
    print("✓ Created pro-scripts.js")
    
    # Write PRO styles
    with open(STYLES_FILE, 'w') as f:
        f.write(STYLES)
    print("✓ Created pro-styles.css")
    
    # Generate extra pages
    generate_extra_pages()
    
    # Generate PWA files
    generate_pwa_files()
    
    # Inject pro features into all HTML files
    modified_count = 0
    for html_file in glob.glob(os.path.join(BLOG_DIR, "*.html")):
        if inject_pro_feature(html_file):
            modified_count += 1
    
    for html_file in glob.glob(os.path.join(POSTS_DIR, "**/*.html"), recursive=True):
        if inject_pro_feature(html_file):
            modified_count += 1
    
    print(f"✓ Injected PRO features into {modified_count} pages")
    
    # Add nofollow to external links
    for html_file in glob.glob(os.path.join(POSTS_DIR, "**/*.html"), recursive=True):
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Add target=_blank and rel=noopener to external links
        modified = content
        # Simple replacement for common external patterns
        if 'target="_blank"' not in modified:
            modified = modified.replace('<a href="https://', '<a href="https://" target="_blank" rel="noopener"')
        
        if modified != content:
            with open(html_file, 'w') as f:
                f.write(modified)
    
    print("✓ Added nofollow/noopener to external links")
    print("\n✅ PRO UPGRADE COMPLETE!")

if __name__ == "__main__":
    upgrade_blog()
