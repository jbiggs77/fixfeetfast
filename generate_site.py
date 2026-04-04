#!/usr/bin/env python3
"""
FixFeetFast.com - Site Generator
Generates static HTML pages from foot health discussion data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from urllib.parse import quote

# Configuration
SITE_URL = "https://fixfeetfast.com"
SITE_NAME = "FixFeetFast.com"
SITE_TAGLINE = "Real foot health answers from real people"
SITE_DESCRIPTION = "Find real experiences and advice about foot conditions, surgery recovery, and treatments from people who've been through it."
SITE_COPYRIGHT = "Built for people seeking real foot health experiences."

OUTPUT_DIR = Path(__file__).parent / "site"

# Color scheme - WebMD inspired
COLORS = {
    "primary": "#1a237e",          # Deep navy
    "primary-light": "#3f51b5",    # Medium blue
    "accent": "#2196f3",           # Bright blue
    "accent-light": "#bbdefb",     # Light blue
    "success": "#4caf50",          # Medical green
    "warning": "#ff9800",          # Orange
    "background": "#ffffff",        # White
    "bg-light": "#f5f5f5",         # Very light gray
    "text-primary": "#212121",     # Dark charcoal
    "text-secondary": "#666666",   # Medium gray
    "border": "#e0e0e0",           # Light border
}

# Niche definitions - Topics for the site
NICHE_MAP = {
    "bunion-surgery-recovery": {
        "title": "Bunion Surgery Recovery",
        "keywords": ["bunion surgery", "bunion recovery", "bunionectomy", "post-op bunion"],
        "description": "Recovery timeline, experiences, and tips after bunion surgery",
    },
    "minimally-invasive-bunion-surgery": {
        "title": "Minimally Invasive Bunion Surgery (MIS)",
        "keywords": ["mis", "minimally invasive", "mis bunion", "keyhole bunion"],
        "description": "Minimally invasive approaches to bunion correction",
    },
    "lapiplasty-surgery": {
        "title": "Lapiplasty 3D Bunion Surgery",
        "keywords": ["lapiplasty", "3d bunion", "lapiplasty procedure"],
        "description": "Lapiplasty 3D procedure experiences and recovery",
    },
    "hammer-toe-surgery": {
        "title": "Hammer Toe Surgery & Correction",
        "keywords": ["hammer toe", "hammertoe", "toe fusion", "claw toe", "mallet toe"],
        "description": "Hammer toe surgery options and recovery experiences",
    },
    "bunion-surgery-swelling": {
        "title": "Post-Surgery Swelling & Inflammation",
        "keywords": ["swelling", "inflammation", "edema", "swollen foot", "swollen toe"],
        "description": "Managing swelling and inflammation after foot surgery",
    },
    "post-surgery-shoes": {
        "title": "Best Shoes After Foot Surgery",
        "keywords": ["shoes", "sneakers", "trainers", "footwear", "orthofeet", "hoka", "new balance", "skechers", "wide shoes"],
        "description": "Footwear recommendations for post-surgery comfort and recovery",
    },
    "bunion-surgery-pain": {
        "title": "Pain Management After Foot Surgery",
        "keywords": ["pain", "pain management", "nerve pain", "throbbing", "aching"],
        "description": "Pain management strategies and experiences post-surgery",
    },
    "walking-after-surgery": {
        "title": "Walking & Weight Bearing After Surgery",
        "keywords": ["walking", "weight bearing", "non weight bearing", "nwb", "crutches", "knee scooter", "boot", "cast"],
        "description": "Walking progression and weight bearing recommendations",
    },
    "scarf-akin-osteotomy": {
        "title": "Scarf & Akin Osteotomy",
        "keywords": ["scarf", "akin", "scarf akin", "osteotomy", "chevron"],
        "description": "Scarf and Akin osteotomy surgical techniques and recovery",
    },
    "bunion-surgery-complications": {
        "title": "Surgery Complications & Wound Healing",
        "keywords": ["infection", "wound", "complication", "hardware", "screw", "pin", "scar", "keloid"],
        "description": "Complications, wound healing, and scar management",
    },
    "physical-therapy-foot": {
        "title": "Physical Therapy & Foot Exercises",
        "keywords": ["physical therapy", "pt", "exercises", "stretching", "range of motion", "rom", "rehab"],
        "description": "Physical therapy, exercises, and rehabilitation strategies",
    },
    "toe-spacers-orthotics": {
        "title": "Toe Spacers, Orthotics & Braces",
        "keywords": ["toe spacer", "toe separator", "orthotic", "insole", "bunion corrector", "splint", "brace"],
        "description": "Orthotics, braces, and toe spacers for foot health",
    },
    "flat-feet-arch-support": {
        "title": "Flat Feet & Arch Support",
        "keywords": ["flat feet", "flat foot", "arch", "arch support", "fallen arch", "pronation", "overpronation"],
        "description": "Flat feet, arch support, and pronation management",
    },
    "plantar-fasciitis": {
        "title": "Plantar Fasciitis Treatment",
        "keywords": ["plantar fasciitis", "heel pain", "heel spur", "plantar", "fascia"],
        "description": "Plantar fasciitis treatments and heel pain relief",
    },
    "toenail-fungus": {
        "title": "Toenail Fungus Treatment",
        "keywords": ["toenail fungus", "fungal nail", "onychomycosis", "fungus", "antifungal", "terbinafine", "lamisil"],
        "description": "Toenail fungus treatments and prevention",
    },
}

def load_posts(filepath):
    """Load posts from JSON file"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def ensure_output_dir():
    """Create output directory structure"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "about").mkdir(exist_ok=True)

def get_css():
    """Return complete CSS for all pages"""
    return f"""* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

:root {{
  --primary: {COLORS['primary']};
  --primary-light: {COLORS['primary-light']};
  --accent: {COLORS['accent']};
  --accent-light: {COLORS['accent-light']};
  --success: {COLORS['success']};
  --warning: {COLORS['warning']};
  --background: {COLORS['background']};
  --bg-light: {COLORS['bg-light']};
  --text-primary: {COLORS['text-primary']};
  --text-secondary: {COLORS['text-secondary']};
  --border: {COLORS['border']};
}}

html {{
  scroll-behavior: smooth;
}}

body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.7;
  color: var(--text-primary);
  background-color: var(--background);
  font-size: 16px;
}}

a {{
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s ease;
}}

a:hover {{
  color: var(--primary);
  text-decoration: underline;
}}

h1, h2, h3, h4, h5, h6 {{
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-primary);
}}

h1 {{
  font-size: 2.25rem;
  font-weight: 700;
}}

h2 {{
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
}}

h3 {{
  font-size: 1.25rem;
  margin-bottom: 1rem;
}}

/* Medical Disclaimer Banner */
.medical-disclaimer {{
  background: var(--accent-light);
  border-left: 4px solid var(--accent);
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  border-radius: 4px;
}}

.medical-disclaimer-icon {{
  display: inline-block;
  width: 24px;
  height: 24px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  font-weight: bold;
  margin-right: 0.75rem;
  font-size: 14px;
}}

.medical-disclaimer p {{
  font-size: 0.95rem;
  color: var(--primary);
  margin: 0;
  display: inline;
}}

/* Layout */
.container {{
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}}

/* Header/Navigation */
header {{
  background: var(--primary);
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}}

header a {{
  color: white;
}}

header a:hover {{
  color: var(--accent-light);
  text-decoration: none;
}}

nav {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}}

.logo {{
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}

.logo span {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--accent);
  border-radius: 50%;
  font-weight: 700;
  color: white;
}}

nav ul {{
  list-style: none;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}}

nav a {{
  font-weight: 500;
  font-size: 0.95rem;
}}

/* Footer */
footer {{
  background: var(--primary);
  color: white;
  padding: 3rem 0 2rem;
  margin-top: 4rem;
}}

footer .container {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}}

footer h3 {{
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: white;
}}

footer p {{
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  line-height: 1.6;
}}

footer ul {{
  list-style: none;
}}

footer li {{
  margin-bottom: 0.75rem;
}}

footer a {{
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.9rem;
}}

footer a:hover {{
  color: white;
  text-decoration: none;
}}

.copyright {{
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  margin-top: 2rem;
  padding-top: 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
}}

/* Hero Section */
.hero {{
  background: var(--background);
  padding: 3rem 0;
  margin-bottom: 3rem;
  border-bottom: 1px solid var(--border);
}}

.hero h1 {{
  margin-bottom: 1rem;
  color: var(--primary);
}}

.hero p {{
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  max-width: 700px;
}}

.hero .tagline {{
  font-weight: 600;
  color: var(--accent);
  font-size: 1rem;
}}

/* Breadcrumb */
.breadcrumb {{
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  padding: 1rem 0;
}}

.breadcrumb a {{
  color: var(--accent);
}}

.breadcrumb span {{
  margin: 0 0.5rem;
}}

/* Grid */
.grid {{
  display: grid;
  gap: 1.5rem;
}}

.grid-2 {{
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}}

.grid-3 {{
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}}

.grid-4 {{
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}}

/* Cards */
.card {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.5rem;
  transition: all 0.2s ease;
  display: block;
}}

.card:hover {{
  border-color: var(--accent);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);
}}

.card h3 {{
  color: var(--primary);
  margin-bottom: 0.75rem;
}}

.card p {{
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 1rem;
}}

.card .stats {{
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}}

.stat {{
  display: flex;
  align-items: center;
  gap: 0.3rem;
}}

/* Badges/Pills */
.badge {{
  display: inline-block;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  background: var(--bg-light);
  color: var(--text-primary);
}}

.badge.product {{
  background: var(--accent-light);
  color: var(--primary);
}}

.badge.treatment {{
  background: #c8e6c9;
  color: #1b5e20;
}}

.badge.surgery {{
  background: #f8bbd0;
  color: #880e4f;
}}

/* Section */
section {{
  margin-bottom: 3rem;
}}

/* Discussion Card */
.discussion {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.2s ease;
}}

.discussion:hover {{
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}}

.discussion-header {{
  margin-bottom: 1rem;
}}

.discussion-meta {{
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}}

.discussion-title {{
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 0.5rem;
}}

.discussion-body {{
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.7;
}}

.discussion-badges {{
  margin-bottom: 1rem;
}}

.discussion-comments {{
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}}

.discussion-comments strong {{
  color: var(--primary);
}}

.comment {{
  background: var(--bg-light);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  border-left: 3px solid var(--accent);
}}

.comment-text {{
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.6;
}}

.comment-meta {{
  font-size: 0.8rem;
  color: var(--text-secondary);
}}

/* Info Box */
.info-box {{
  background: var(--bg-light);
  border-left: 4px solid var(--accent);
  padding: 1.5rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}}

.info-box h3 {{
  color: var(--primary);
  margin-top: 0;
}}

.info-box p {{
  margin: 0.5rem 0;
  color: var(--text-secondary);
}}

/* Stats */
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}}

.stat-box {{
  padding: 1.5rem;
  background: var(--bg-light);
  border-radius: 4px;
  border: 1px solid var(--border);
  text-align: center;
}}

.stat-number {{
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent);
}}

.stat-label {{
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  font-weight: 500;
}}

/* How It Works */
.how-it-works {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}}

.step {{
  text-align: center;
}}

.step-number {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}}

.step h3 {{
  color: var(--primary);
  margin-bottom: 0.75rem;
}}

.step p {{
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}}

/* FAQ - Accordion Style */
.faq-item {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-bottom: 1rem;
  overflow: hidden;
}}

.faq-question {{
  padding: 1.25rem 1.5rem;
  background: var(--background);
  border: none;
  width: 100%;
  text-align: left;
  font-weight: 600;
  color: var(--primary);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  transition: background 0.2s ease;
}}

.faq-question:hover {{
  background: var(--bg-light);
}}

.faq-question::after {{
  content: '+';
  display: inline-block;
  font-size: 1.5rem;
  font-weight: 300;
  transition: transform 0.3s ease;
}}

.faq-item.active .faq-question {{
  background: var(--bg-light);
  border-bottom: 1px solid var(--border);
}}

.faq-item.active .faq-question::after {{
  content: '−';
}}

.faq-answer {{
  padding: 1.5rem;
  background: var(--bg-light);
  display: none;
  color: var(--text-secondary);
  line-height: 1.7;
}}

.faq-item.active .faq-answer {{
  display: block;
}}

/* Responsive */
@media (max-width: 768px) {{
  nav {{
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }}

  nav ul {{
    flex-direction: column;
    gap: 0.75rem;
  }}

  .container {{
    padding: 0 16px;
  }}

  h1 {{
    font-size: 1.75rem;
  }}

  h2 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }}

  .grid-2,
  .grid-3,
  .grid-4 {{
    grid-template-columns: 1fr;
  }}

  .stats-grid {{
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }}

  .how-it-works {{
    grid-template-columns: 1fr;
  }}
}}

@media (max-width: 480px) {{
  header {{
    padding: 0.75rem 0;
  }}

  nav {{
    gap: 1rem;
  }}

  .logo {{
    font-size: 1.25rem;
  }}

  nav ul {{
    gap: 0.5rem;
  }}

  nav a {{
    font-size: 0.85rem;
  }}

  h1 {{
    font-size: 1.5rem;
  }}

  h2 {{
    font-size: 1.25rem;
  }}

  .card {{
    padding: 1rem;
  }}

  .discussion {{
    padding: 1rem;
  }}

  .stats-grid {{
    grid-template-columns: 1fr;
  }}

  .stat-number {{
    font-size: 1.75rem;
  }}
}}
"""

def get_page_header(title, description=""):
    """HTML header template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description or SITE_DESCRIPTION}">
  <meta name="theme-color" content="{COLORS['primary']}">
  <link rel="canonical" href="{SITE_URL}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
{get_css()}
  </style>
</head>
<body>
  <header>
    <nav class="container">
      <div class="logo">
        <span>F</span>
        <a href="/">{SITE_NAME}</a>
      </div>
      <ul>
        <li><a href="/">Topics</a></li>
        <li><a href="/#how-it-works">How It Works</a></li>
        <li><a href="/about/">About</a></li>
      </ul>
    </nav>
  </header>

  <div class="container">
    <div class="medical-disclaimer">
      <span class="medical-disclaimer-icon">i</span>
      <p><strong>Community Information:</strong> This site contains personal experiences and discussions, not medical advice. Always consult a healthcare provider before making medical decisions.</p>
    </div>
  </div>
"""

def get_page_footer():
    """HTML footer template"""
    return f"""
  <footer>
    <div class="container">
      <div>
        <h3>{SITE_NAME}</h3>
        <p>{SITE_TAGLINE}</p>
      </div>
      <div>
        <h3>Pages</h3>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h3>Resources</h3>
        <ul>
          <li><a href="/robots.txt">Robots.txt</a></li>
          <li><a href="/llms.txt">LLMs.txt</a></li>
        </ul>
      </div>
    </div>
    <div class="container">
      <div class="copyright">
        <p>{SITE_COPYRIGHT}</p>
      </div>
    </div>
  </footer>
  <script>
    // FAQ accordion
    document.querySelectorAll('.faq-question').forEach(btn => {{
      btn.addEventListener('click', () => {{
        btn.parentElement.classList.toggle('active');
      }});
    }});
  </script>
</body>
</html>
"""

def generate_homepage(posts):
    """Generate index.html"""

    # Calculate statistics
    total_discussions = len(posts)
    total_comments = sum(len(p.get('comments', [])) for p in posts)

    # Collect all mentioned products and count them
    product_counts = defaultdict(int)
    for post in posts:
        if products := post.get('products_mentioned'):
            for product in products.split(','):
                product = product.strip()
                if product:
                    product_counts[product] += 1

    # Count posts per niche
    niche_counts = defaultdict(int)
    for post in posts:
        if conditions := post.get('conditions_mentioned'):
            conditions_lower = conditions.lower()
            # Find matching niche based on keywords
            for niche_id, niche_data in NICHE_MAP.items():
                for keyword in niche_data['keywords']:
                    if keyword.lower() in conditions_lower:
                        niche_counts[niche_id] += 1
                        break

    top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:8]

    html = get_page_header(SITE_NAME, SITE_DESCRIPTION)

    html += f"""
  <main>
    <section class="hero">
      <div class="container">
        <h1>{SITE_NAME}</h1>
        <p>{SITE_TAGLINE}</p>
        <p>{SITE_DESCRIPTION}</p>
      </div>
    </section>

    <section class="container">
      <h2>Community Insights</h2>
      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-number">{total_discussions:,}</div>
          <div class="stat-label">Discussions</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{total_comments:,}</div>
          <div class="stat-label">Comments</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(NICHE_MAP)}</div>
          <div class="stat-label">Topics</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(product_counts)}</div>
          <div class="stat-label">Products</div>
        </div>
      </div>
    </section>

    <section class="container">
      <h2>Explore Foot Health Topics</h2>
      <div class="grid grid-3">
"""

    for niche_id, niche_data in NICHE_MAP.items():
        count = niche_counts.get(niche_id, 0)
        html += f"""        <a href="/{niche_id}/" class="card">
          <h3>{niche_data['title']}</h3>
          <p>{niche_data['description']}</p>
          <div class="stats">
            <span class="stat">💬 {count} discussions</span>
          </div>
        </a>
"""

    html += """      </div>
    </section>
"""

    if top_products:
        html += f"""
    <section class="container">
      <h2>Top Mentioned Products</h2>
      <div class="grid grid-4">
"""
        for product, count in top_products:
            html += f"""        <div class="card">
          <h3>{product}</h3>
          <p>Mentioned in {count} discussions</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    html += f"""
    <section class="container" id="how-it-works">
      <h2>How It Works</h2>
      <div class="how-it-works">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Real Experiences</h3>
          <p>Content comes from real people sharing their foot health journeys in support groups</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>Browse Topics</h3>
          <p>Find discussions organized by condition, procedure, and treatment type</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>Learn & Discover</h3>
          <p>See what treatments and products people are actually using and recommending</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>Ask Your Doctor</h3>
          <p>Use insights to ask informed questions with your healthcare provider</p>
        </div>
      </div>
    </section>
  </main>
"""

    html += get_page_footer()
    return html

def generate_topic_page(niche_id, niche_data, posts):
    """Generate individual topic page"""

    # Filter posts for this niche
    topic_posts = []
    for post in posts:
        if conditions := post.get('conditions_mentioned'):
            conditions_lower = conditions.lower()
            # Check if any keyword matches the conditions
            for keyword in niche_data['keywords']:
                if keyword.lower() in conditions_lower:
                    topic_posts.append(post)
                    break

    # Aggregate data
    treatment_mentions = defaultdict(int)
    product_mentions = defaultdict(int)
    surgery_mentions = defaultdict(int)
    total_comments = 0

    for post in topic_posts:
        total_comments += len(post.get('comments', []))

        if treatments := post.get('treatments_mentioned'):
            for treatment in treatments.split(','):
                treatment = treatment.strip()
                if treatment:
                    treatment_mentions[treatment] += 1

        if products := post.get('products_mentioned'):
            for product in products.split(','):
                product = product.strip()
                if product:
                    product_mentions[product] += 1

        if surgeries := post.get('surgery_types_mentioned'):
            for surgery in surgeries.split(','):
                surgery = surgery.strip()
                if surgery:
                    surgery_mentions[surgery] += 1

        for comment in post.get('comments', []):
            if products := comment.get('products_mentioned'):
                for product in products.split(','):
                    product = product.strip()
                    if product:
                        product_mentions[product] += 1

    description = f"{len(topic_posts)} real discussions about {niche_data['title'].lower()}"

    html = get_page_header(niche_data['title'], description)

    html += f"""
  <main>
    <section class="container">
      <div class="breadcrumb">
        <a href="/">Home</a> <span>›</span> {niche_data['title']}
      </div>
    </section>

    <section class="hero">
      <div class="container">
        <h1>{niche_data['title']}</h1>
        <p>{niche_data['description']}</p>
      </div>
    </section>

    <section class="container">
      <div class="info-box">
        <h3>Topic Overview</h3>
        <p><strong>{len(topic_posts)}</strong> discussions | <strong>{total_comments}</strong> community replies | Based on real experiences</p>
      </div>
    </section>

    <section class="container">
      <h2>Community Insights</h2>
      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-number">{len(topic_posts)}</div>
          <div class="stat-label">Discussions</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{total_comments}</div>
          <div class="stat-label">Comments</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(product_mentions)}</div>
          <div class="stat-label">Products Mentioned</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{len(treatment_mentions)}</div>
          <div class="stat-label">Treatments</div>
        </div>
      </div>
    </section>
"""

    # Top mentioned sections
    if product_mentions:
        top_products = sorted(product_mentions.items(), key=lambda x: x[1], reverse=True)[:6]
        html += f"""
    <section class="container">
      <h2>Popular Products</h2>
      <div class="grid grid-3">
"""
        for product, count in top_products:
            html += f"""        <div class="card">
          <h3>{product}</h3>
          <p class="stat">Mentioned {count} times</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    if treatment_mentions:
        top_treatments = sorted(treatment_mentions.items(), key=lambda x: x[1], reverse=True)[:4]
        html += f"""
    <section class="container">
      <h2>Common Treatments</h2>
      <div style="display: grid; gap: 1rem;">
"""
        for treatment, count in top_treatments:
            html += f"""        <div class="card">
          <h3>{treatment}</h3>
          <p class="stat">Mentioned {count} times in discussions</p>
        </div>
"""
        html += """      </div>
    </section>
"""

    # Discussions section
    if topic_posts:
        html += f"""
    <section class="container">
      <h2>What People Are Saying</h2>
"""

        for post in topic_posts[:20]:  # Limit to 20 per page
            html += f"""      <div class="discussion">
        <div class="discussion-header">
          <div class="discussion-meta">From {post.get('source_group', 'Community')}</div>
          <div class="discussion-title">{post.get('title', 'Discussion')}</div>
        </div>
        <div class="discussion-body">{post.get('body', '')[:400]}...</div>
        <div class="discussion-badges">
"""

            # Add product badges
            if products := post.get('products_mentioned'):
                for product in products.split(',')[:3]:
                    product = product.strip()
                    if product:
                        html += f'          <span class="badge product">{product}</span>\n'

            # Add treatment badges
            if treatments := post.get('treatments_mentioned'):
                for treatment in treatments.split(',')[:3]:
                    treatment = treatment.strip()
                    if treatment:
                        html += f'          <span class="badge treatment">{treatment}</span>\n'

            # Add surgery badges
            if surgeries := post.get('surgery_types_mentioned'):
                for surgery in surgeries.split(',')[:2]:
                    surgery = surgery.strip()
                    if surgery:
                        html += f'          <span class="badge surgery">{surgery}</span>\n'

            html += """        </div>
"""

            # Comments
            if post.get('comments'):
                html += """        <div class="discussion-comments">
          <strong>Comments:</strong>
"""
                for comment in post.get('comments', [])[:3]:
                    html += f"""          <div class="comment">
            <div class="comment-text">{comment.get('comment_text', '')[:200]}...</div>
            <div class="comment-meta">Community member</div>
          </div>
"""
                if len(post.get('comments', [])) > 3:
                    html += f"""          <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">+{len(post.get('comments', [])) - 3} more comments</p>
"""
                html += """        </div>
"""

            html += """      </div>
"""

        html += """    </section>
"""

    # FAQ Section
    faqs = generate_faqs(niche_data['title'])
    if faqs:
        html += f"""
    <section class="container">
      <h2>Frequently Asked Questions</h2>
      <div>
"""
        for question, answer in faqs:
            html += f"""        <div class="faq-item">
          <button class="faq-question">{question}</button>
          <div class="faq-answer">{answer}</div>
        </div>
"""
        html += """      </div>
    </section>
"""

    html += """  </main>
"""
    html += get_page_footer()
    return html

def generate_faqs(topic_title):
    """Generate FAQ content for a topic"""
    topic_lower = topic_title.lower()

    # Template FAQs
    if 'recovery' in topic_lower or 'surgery' in topic_lower:
        return [
            (f"What is {topic_title} recovery like?",
             "Recovery experiences vary by individual and surgical technique. Most people report gradual improvement over weeks to months. Many community members share their timelines and recovery tips online."),
            (f"How long does {topic_title} take to heal?",
             "Healing timelines typically range from 6 weeks to several months depending on the procedure and individual factors. Full recovery may take even longer for some individuals. Your surgeon can provide specific recovery estimates."),
            (f"What treatments help with {topic_title}?",
             "Treatment approaches vary by condition and severity. Common treatments mentioned in communities include physical therapy, pain management, ice therapy, compression, and specialized footwear. Discuss options with your healthcare provider."),
            (f"What products do people recommend for {topic_title}?",
             "Community members frequently recommend products like specialized shoes, compression socks, insoles, and therapeutic devices. Product recommendations should be discussed with your healthcare provider to ensure they're appropriate for your situation."),
        ]
    elif 'shoe' in topic_lower or 'footwear' in topic_lower:
        return [
            ("What shoes are best after foot surgery?",
             "Comfort and support are key. Many people recommend wide shoes, breathable materials, and styles with good arch support. Popular brands mentioned include Hoka, Orthofeet, New Balance, and Skechers. Consult your surgeon for specific recommendations."),
            ("How soon can I wear regular shoes?",
             "This depends on your specific surgery and healing progress. Most surgeons recommend waiting several weeks to months. Follow your surgeon's guidance on when to transition footwear."),
            ("Should I buy shoes with insoles or orthotics?",
             "Many people find custom or over-the-counter insoles helpful for comfort and support. Discuss orthotic needs with your doctor or a podiatrist."),
        ]
    else:
        return [
            (f"What should I know about {topic_title}?",
             "The community shares diverse experiences about this topic. Reading real experiences can help you understand what to expect and what questions to ask your healthcare provider."),
            (f"Who should consider {topic_title}?",
             "This is a personal decision best made with your healthcare provider. Community experiences can inform your conversations with your doctor."),
        ]

def generate_about_page():
    """Generate about/index.html"""
    html = get_page_header("About FixFeetFast", "Learn about FixFeetFast.com and how we source content")

    html += f"""
  <main>
    <section class="container">
      <div class="breadcrumb">
        <a href="/">Home</a> <span>›</span> About
      </div>
    </section>

    <section class="hero">
      <div class="container">
        <h1>About {SITE_NAME}</h1>
        <p>{SITE_TAGLINE}</p>
      </div>
    </section>

    <section class="container">
      <div class="card" style="max-width: 800px; margin: 0 auto;">
        <h2>Our Mission</h2>
        <p>{SITE_DESCRIPTION}</p>

        <h2 style="margin-top: 2rem;">How It Works</h2>
        <p>{SITE_NAME} aggregates real experiences and discussions from foot health support communities. We organize this content by condition and treatment type to help people understand what others have experienced and what treatments are being used.</p>

        <h2 style="margin-top: 2rem;">About Our Content</h2>
        <p>All content on {SITE_NAME} comes from real people sharing their experiences in foot health support groups and online communities. These are first-hand accounts of surgeries, recovery, treatments, and product recommendations from people who have lived through these experiences.</p>

        <h2 style="margin-top: 2rem;">Important Disclaimer</h2>
        <p><strong>This site does not provide medical advice.</strong> The content here represents personal experiences and should not be substituted for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before making any medical decisions.</p>

        <p style="margin-top: 1rem;">Every person's situation is unique. What worked for one person may not work for you. Your doctor or podiatrist is the best source for medical advice tailored to your specific condition.</p>

        <h2 style="margin-top: 2rem;">How to Use This Site</h2>
        <ul style="margin-left: 2rem; margin-top: 1rem; color: var(--text-secondary);">
          <li>Browse topics to explore common foot conditions and treatments</li>
          <li>Read real experiences to understand what others have gone through</li>
          <li>Note products, treatments, and strategies that people mention</li>
          <li>Use these insights to ask informed questions with your healthcare provider</li>
          <li>Make decisions with your doctor, not based solely on what you read here</li>
        </ul>

        <h2 style="margin-top: 2rem;">Contact & Attribution</h2>
        <p>Content is sourced from public discussions in foot health support communities. We appreciate the people sharing their experiences to help others.</p>
      </div>
    </section>
  </main>
"""

    html += get_page_footer()
    return html

def generate_sitemap(niche_ids):
    """Generate sitemap.xml"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Homepage
    xml += f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n'

    # Topic pages
    for niche_id in niche_ids:
        xml += f'  <url>\n    <loc>{SITE_URL}/{niche_id}/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'

    # About page
    xml += f'  <url>\n    <loc>{SITE_URL}/about/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'

    xml += '</urlset>\n'
    return xml

def generate_robots_txt():
    """Generate robots.txt"""
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""

def generate_llms_txt():
    """Generate llms.txt"""
    return f"""{SITE_NAME}

Description: {SITE_DESCRIPTION}

Categories: Health, Medical Information, Support Community Content

Privacy Policy: {SITE_URL}/privacy
Terms of Service: {SITE_URL}/terms
About: {SITE_URL}/about/
"""

def main():
    """Main generation function"""
    print(f"Generating {SITE_NAME}...")

    # Load posts
    posts_file = Path(__file__).parent / "posts.json"
    posts = load_posts(str(posts_file))
    print(f"Loaded {len(posts)} posts")

    # Create output directories
    ensure_output_dir()

    # Generate homepage
    print("Generating homepage...")
    index_html = generate_homepage(posts)
    (OUTPUT_DIR / "index.html").write_text(index_html)

    # Generate topic pages
    print(f"Generating {len(NICHE_MAP)} topic pages...")
    for niche_id, niche_data in NICHE_MAP.items():
        topic_html = generate_topic_page(niche_id, niche_data, posts)
        niche_dir = OUTPUT_DIR / niche_id
        niche_dir.mkdir(exist_ok=True)
        (niche_dir / "index.html").write_text(topic_html)

    # Generate about page
    print("Generating about page...")
    about_html = generate_about_page()
    (OUTPUT_DIR / "about" / "index.html").write_text(about_html)

    # Generate sitemap
    print("Generating sitemap.xml...")
    sitemap_xml = generate_sitemap(NICHE_MAP.keys())
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap_xml)

    # Generate robots.txt
    print("Generating robots.txt...")
    robots_txt = generate_robots_txt()
    (OUTPUT_DIR / "robots.txt").write_text(robots_txt)

    # Generate llms.txt
    print("Generating llms.txt...")
    llms_txt = generate_llms_txt()
    (OUTPUT_DIR / "llms.txt").write_text(llms_txt)

    print(f"Done! Generated site at {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
