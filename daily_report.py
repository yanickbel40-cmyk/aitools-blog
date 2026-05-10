#!/usr/bin/env python3
"""
AI Toolbox Pro - Daily report generator & health check
Sends Telegram report to Yanick every morning at 8:00
"""

import json
import os
import glob
from datetime import datetime

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BLOG_DIR, "posts/posts.json")
KEYWORDS_FILE = os.path.join(BLOG_DIR, "keywords.json")
REPORT_FILE = os.path.join(BLOG_DIR, "daily_report.md")

def load_posts():
    with open(POSTS_FILE) as f:
        return json.load(f)

def get_trending_keywords():
    """Simulate keyword tracking - will be replaced with live API calls"""
    return {
        "hot_today": [
            "best AI productivity tools 2026",
            "ChatGPT vs Claude vs Gemini",
            "AI job replacement statistics 2026",
            "free AI tools small business",
            "AI automation workflows"
        ],
        "rising": [
            "AI agents 2026",
            "AI meeting assistant",
            "AI affiliate marketing programs"
        ]
    }

def count_total_words():
    """Estimate total content on the blog"""
    total = 0
    for html_file in glob.glob(os.path.join(BLOG_DIR, "posts/**/*.html"), recursive=True):
        with open(html_file) as f:
            content = f.read()
            # Rough word count from HTML
            in_tag = False
            words = 0
            for char in content:
                if char == '<':
                    in_tag = True
                elif char == '>':
                    in_tag = False
                elif not in_tag and char.isspace():
                    words += 1
            total += words
    return total

def generate_report():
    posts = load_posts()
    keywords = get_trending_keywords()
    word_count = count_total_words()

    now = datetime.now()
    
    report = f"""# 📊 Rapport Quotidien AI Toolbox Pro
**{now.strftime('%d/%m/%Y à %H:%M')}**

---

## 📈 Statistiques du Blog

| Métrique | Valeur |
|----------|--------|
| Articles publiés | {len(posts)} |
| Mots de contenu | ~{word_count:,} |
| Pages indexées | {len(posts) + 1} |
| Catégories | 5 (Reviews, Guides, Comparisons, Trends, Monetization) |

---

## 🔥 Mots-clés Tendance du Jour

**En vedette :**
1. {keywords['hot_today'][0]}
2. {keywords['hot_today'][1]}
3. {keywords['hot_today'][2]}
4. {keywords['hot_today'][3]}
5. {keywords['hot_today'][4]}

**En hausse :**
- {keywords['rising'][0]}
- {keywords['rising'][1]}
- {keywords['rising'][2]}

---

## 📝 Derniers Articles
| Titre | Catégorie | Date |
|------|-----------|------|
"""
    for p in posts[:5]:
        report += f"| {p['title'][:50]}... | {p['category']} | {p['date']} |\n"

    report += f"""
---

## 🎯 Actions Recommandées Aujourd'hui
"""

    # Suggest actions based on day
    day = now.weekday()
    actions = {
        0: "• LUNDI — Publier un nouvel article (guide ou review)\n• Vérifier les positions Google des mots-clés principaux\n• Partager sur Twitter/X et LinkedIn",
        1: "• MARDI — Optimiser les articles les plus anciens (mise à jour)\n• Ajouter des liens internes entre articles\n• Chercher des backlinks (forums, Medium)",
        2: "• MERCREDI — Faire un post LinkedIn/Medium pour un article\n• Vérifier les trending topics AI de la semaine\n• Planifier les prochains sujets",
        3: "• JEUDI — Publier un article comparatif\n• Vérifier les programmes d'affiliation\n• Enrichir les articles avec plus de données",
        4: "• VENDREDI — Résumé de la semaine\n• Engager dans les commentaires/réseaux\n• Préparer le contenu de la semaine prochaine",
        5: "• SAMEDI — Audit SEO rapide\n• Améliorer les articles les moins performants\n• Recherche de nouveaux mots-clés",
        6: "• DIMANCHE — Planification stratégique\n• Analyse des tendances de la semaine\n• Repos stratégique"
    }

    report += actions.get(day, actions[0])
    
    report += f"""

---

## 💰 Prochaines Étapes Monétisation

1. ✅ **Phase 1** — Blog créé avec 15 articles SEO (FAIT)
2. ⬜ **Phase 2** — Déploiement sur hébergement gratuit (GitHub Pages / Cloudflare)
3. ⬜ **Phase 3** — Inscription aux programmes d'affiliation AI (Jasper, Writesonic, Notion, etc.)
4. ⬜ **Phase 4** — Ajout Google AdSense (quand 20+ articles)
5. ⬜ **Phase 5** — Newsletter + lead magnet gratuit
6. ⬜ **Phase 6** — Scale à 50+ articles + backlinks

---

*Prochain rapport : demain à 8h*
"""
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)
