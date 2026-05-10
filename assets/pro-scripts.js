// AI Toolbox Pro — Advanced Features
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
    fetch(window.location.pathname.replace('/posts/', '/posts/posts.json').replace(/article\/.*/, '') + '../posts/posts.json')
        .then(r => r.json())
        .then(posts => {
            const current = document.querySelector('h1')?.textContent || '';
            const related = posts.filter(p => p.url !== window.location.pathname.replace('/aitools-blog/', '')).slice(0, 3);
            container.innerHTML = related.map(p => `
                <div class="post-card" style="cursor:pointer;background:white;border-radius:8px;padding:15px;margin:10px 0;box-shadow:0 1px 5px rgba(0,0,0,0.08);">
                    <div class="category" style="font-size:0.8rem;color:#00d4ff;text-transform:uppercase;">${p.category}</div>
                    <h4 style="margin:5px 0;"><a href="${p.url}" style="color:#1a1a2e;text-decoration:none;">${p.title}</a></h4>
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
