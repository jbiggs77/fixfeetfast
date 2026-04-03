# FixFeetFast.com - Site Generator

A complete static site generator for a longtail foot health content website that aggregates real experiences from support communities.

## Files

- **generate_site.py** - Main generator script (1,223 lines, fully self-contained)
- **posts.json** - JSON file containing post data (empty by default)

## Running the Generator

```bash
python3 generate_site.py
```

This will generate the complete site in the `site/` directory.

## Output Structure

```
site/
├── index.html              # Homepage with stats and topic grid
├── about/index.html        # About page with disclaimer
├── bunion-surgery-recovery/index.html
├── minimally-invasive-bunion-surgery/index.html
├── lapiplasty-surgery/index.html
├── hammer-toe-surgery/index.html
├── bunion-surgery-swelling/index.html
├── post-surgery-shoes/index.html
├── bunion-surgery-pain/index.html
├── walking-after-surgery/index.html
├── scarf-akin-osteotomy/index.html
├── bunion-surgery-complications/index.html
├── physical-therapy-foot/index.html
├── toe-spacers-orthotics/index.html
├── flat-feet-arch-support/index.html
├── plantar-fasciitis/index.html
├── toenail-fungus/index.html
├── sitemap.xml             # SEO sitemap
├── robots.txt              # Robot instructions
└── llms.txt                # LLM-friendly metadata
```

## Features

### Homepage
- Hero section with site branding
- Stats dashboard (discussions, comments, topics, products)
- Grid of 15 topic cards
- How It Works section
- Top mentioned products section

### Topic Pages
- Breadcrumb navigation
- Community insights (stats)
- Top products mentioned
- Common treatments mentioned
- Real discussions with:
  - Source group attribution
  - Title and excerpt
  - Product badges (teal)
  - Treatment badges (yellow)
  - Surgery type badges (blue)
  - Comments preview
- FAQ section with accordion
- Mobile responsive design

### SEO & Technical
- Schema.org markup
- SEO-optimized meta descriptions
- Responsive CSS (mobile-first)
- Sticky header navigation
- Semantic HTML5

## Data Format (posts.json)

```json
[
  {
    "id": 1,
    "body": "post text...",
    "title": "short title",
    "source_group": "group name",
    "conditions_mentioned": "condition1, condition2",
    "treatments_mentioned": "treatment1, treatment2",
    "products_mentioned": "Product1, Product2",
    "surgery_types_mentioned": "SurgeryType1, SurgeryType2",
    "comments": [
      {
        "comment_text": "reply text...",
        "conditions_mentioned": "",
        "treatments_mentioned": "",
        "products_mentioned": ""
      }
    ]
  }
]
```

## Configuration

Edit constants in `generate_site.py`:
- `SITE_URL` - Base URL
- `SITE_NAME` - Site name
- `SITE_TAGLINE` - Tagline
- `SITE_DESCRIPTION` - Meta description
- `COLORS` - Color scheme
- `NICHE_MAP` - Topic definitions

## Features Included

- 15 pre-configured niches/topics
- Automatic content matching by keywords
- Discussion aggregation and display
- Badge system for products, treatments, and surgeries
- FAQ generation per topic
- Statistics dashboard
- Product popularity tracking
- Treatment mention tracking
- Comment preview system
- Fully responsive design
- Mobile menu
- Accordion FAQs with JavaScript
- Complete CSS styling (no external dependencies)
- SEO optimization
- Breadcrumb navigation
- About page with disclaimer
- Footer with links

## Color Scheme

- Primary: #0d9488 (teal)
- Primary Dark: #0f766e
- Primary Light: #ccfbf1
- Success: #059669
- Various grays for text and backgrounds

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive
- Graceful degradation for older browsers

## Production Ready

The generator includes:
- Error handling
- Proper file path handling
- Directory creation
- JSON loading
- Complete HTML/CSS templates
- SEO best practices
- Accessibility considerations
- Mobile optimization

Just populate `posts.json` with your data and run the generator!
