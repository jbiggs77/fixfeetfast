import json
import re

# Load posts
with open('posts.json', 'r') as f:
    posts = json.load(f)

# Define keyword patterns for each metadata field
CONDITION_PATTERNS = {
    'bunion': r'\bbunion[s]?\b',
    'hallux valgus': r'\bhallux\s+valgus\b',
    'hallux rigidus': r'\bhallux\s+rigidus\b',
    'hammer toe': r'\bhammer\s*toe[s]?\b',
    'plantar fasciitis': r'\bplantar\s+fasciitis\b',
    'flat feet': r'\bflat\s+f[eo]+t\b',
    'heel spur': r'\bheel\s+spur[s]?\b',
    'morton\'s neuroma': r'\bmorton.?s?\s+neuroma\b',
    'neuropathy': r'\bneuropath[yic]+\b',
    'gout': r'\bgout\b',
    'arthritis': r'\barthritis\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'sesamoiditis': r'\bsesamoiditis\b',
    'capsulitis': r'\bcapsulitis\b',
    'tendonitis': r'\btendonitis\b|\btendinitis\b',
    'achilles tendon': r'\bachilles\b',
    'bone spur': r'\bbone\s+spur[s]?\b',
    'tailor\'s bunion': r'\btailor.?s?\s+bunion\b|\bbunionette\b',
    'ingrown toenail': r'\bingrown\s+toenail[s]?\b|\bingrown\s+nail[s]?\b',
    'toenail fungus': r'\btoenail\s+fungus\b|\bfungal\s+nail\b|\bfungal\s+toenail\b|\bonychomycosis\b',
    'foot pain': r'\bfoot\s+pain\b',
    'toe pain': r'\btoe\s+pain\b',
    'swelling': r'\bswell(ing|ed|s)?\b',
    'numbness': r'\bnumb(ness)?\b',
    'stiffness': r'\bstiff(ness)?\b',
    'crossover toe': r'\bcrossover\s+toe\b',
    'claw toe': r'\bclaw\s+toe[s]?\b',
    'mallet toe': r'\bmallet\s+toe[s]?\b',
    'heel pain': r'\bheel\s+pain\b',
    'big toe joint': r'\bbig\s+toe\s+joint\b|\b1st\s+mtp\b|\bfirst\s+mtp\b',
}

SURGERY_PATTERNS = {
    'Lapiplasty': r'\blapiplasty\b',
    'bunionectomy': r'\bbunionectom[yies]+\b',
    'osteotomy': r'\bosteotom[yies]+\b',
    'chevron osteotomy': r'\bchevron\b',
    'scarf osteotomy': r'\bscarf\b',
    'Austin bunionectomy': r'\baustin\b.*bunion',
    'arthrodesis': r'\barthrodesis\b',
    'fusion': r'\bfusion\b|\bfused\b',
    'Akin osteotomy': r'\bakin\b',
    'hardware removal': r'\bhardware\s+removal\b|\bscrew[s]?\s+remov\b|\bplate\s+remov\b',
    'minimally invasive': r'\bminimally\s+invasive\b|\bMIS\b',
    'hammer toe surgery': r'\bhammer\s*toe\s+(surgery|correction|repair)\b',
    'toe shortening': r'\btoe\s+shortening\b',
    'joint replacement': r'\bjoint\s+replacement\b',
    'Cartiva': r'\bcartiva\b',
    'plantar fascia release': r'\bplantar\s+fascia\s+release\b|\bfasciotomy\b',
}

PRODUCT_PATTERNS = {
    'Hoka': r'\bhoka\b',
    'Correct Toes': r'\bcorrect\s+toes\b',
    'Archies': r'\barchies\b',
    'Birkenstocks': r'\bbirkenstock[s]?\b',
    'New Balance': r'\bnew\s+balance\b',
    'Brooks': r'\bbrooks\b',
    'OOFOS': r'\boofos\b',
    'Vionic': r'\bvionic\b',
    'orthotics': r'\borthotic[s]?\b|\binsole[s]?\b|\binsert[s]?\b',
    'wide toe box shoes': r'\bwide\s+toe\s+box\b',
    'toe spacers': r'\btoe\s+spacer[s]?\b|\btoe\s+separator[s]?\b',
    'bunion splint': r'\bbunion\s+splint[s]?\b|\bbunion\s+corrector[s]?\b',
    'walking boot': r'\bwalking\s+boot\b|\bboot\b(?=.*(?:week|month|post|surgery))',
    'knee scooter': r'\bknee\s+scooter\b|\biwalk\b',
    'cast': r'\b(?:in\s+a\s+)?cast\b',
    'compression socks': r'\bcompression\s+sock[s]?\b',
    'night splint': r'\bnight\s+splint[s]?\b',
    'KT tape': r'\bkt\s+tape\b|\bkinesio\b',
    'Altra': r'\baltra\b',
    'Crocs': r'\bcrocs\b',
    'Skechers': r'\bskecher[s]?\b',
}

TREATMENT_PATTERNS = {
    'surgery': r'\bsurger[yies]+\b|\boperat(ion|ed|ing)\b|\bpost[\s-]?op\b',
    'cortisone': r'\bcortisone\b|\bcortisol\b|\bsteroid\s+inject\b',
    'physical therapy': r'\bphysical\s+therap[yist]+\b|\bPT\b(?=\s|$|\.)|\bphysio\b',
    'shockwave therapy': r'\bshockwave\b|\bECSWT\b|\bESWT\b',
    'ice therapy': r'\bic(e|ing)\b(?=.*(?:foot|toe|swell|pain))',
    'stretching': r'\bstretch(ing|es)?\b',
    'rest': r'\brest(ing)?\b(?=.*(?:foot|feet|toe))',
    'elevation': r'\belev(ation|ated|ating|ate)\b',
    'anti-inflammatory': r'\banti[\s-]?inflammator[yies]+\b|\bibuprofen\b|\bnaproxen\b|\bNSAID[s]?\b|\badvil\b|\bmotrin\b|\baleve\b',
    'platelet-rich plasma': r'\bPRP\b|\bplatelet[\s-]?rich\b',
    'laser therapy': r'\blaser\s+therap[yies]+\b',
    'massage': r'\bmassag(e|ing)\b',
    'acupuncture': r'\bacupuncture\b',
    'custom orthotics': r'\bcustom\s+orthotic[s]?\b',
    'taping': r'\btaping\b',
    'X-ray': r'\bx[\s-]?ray[s]?\b',
    'MRI': r'\bMRI\b',
    'cast immobilization': r'\bcast\b.*(?:week|month|immobil)',
    'weight bearing': r'\bweight[\s-]?bear(ing)?\b|\bnon[\s-]?weight[\s-]?bear(ing)?\b|\bNWB\b|\bFWB\b|\bPWB\b',
}

def get_full_text(post):
    """Get full searchable text from post body + comments."""
    text = post.get('body', '')
    for comment in post.get('comments', []):
        if isinstance(comment, dict):
            text += ' ' + comment.get('text', '') + ' ' + comment.get('body', '')
        elif isinstance(comment, str):
            text += ' ' + comment
    return text

def detect_items(text, patterns):
    """Detect items in text using regex patterns."""
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

enriched_count = 0
field_enriched = {'conditions_mentioned': 0, 'surgery_types_mentioned': 0, 'products_mentioned': 0, 'treatments_mentioned': 0}

for post in posts:
    text = get_full_text(post)
    changed = False
    
    # Enrich conditions
    detected_conditions = detect_items(text, CONDITION_PATTERNS)
    existing = post.get('conditions_mentioned', [])
    if not isinstance(existing, list):
        existing = []
    merged = list(set(existing + detected_conditions))
    if set(merged) != set(existing):
        post['conditions_mentioned'] = sorted(merged)
        field_enriched['conditions_mentioned'] += 1
        changed = True
    
    # Enrich surgery types
    detected_surgery = detect_items(text, SURGERY_PATTERNS)
    existing = post.get('surgery_types_mentioned', [])
    if not isinstance(existing, list):
        existing = []
    merged = list(set(existing + detected_surgery))
    if set(merged) != set(existing):
        post['surgery_types_mentioned'] = sorted(merged)
        field_enriched['surgery_types_mentioned'] += 1
        changed = True
    
    # Enrich products
    detected_products = detect_items(text, PRODUCT_PATTERNS)
    existing = post.get('products_mentioned', [])
    if not isinstance(existing, list):
        existing = []
    merged = list(set(existing + detected_products))
    if set(merged) != set(existing):
        post['products_mentioned'] = sorted(merged)
        field_enriched['products_mentioned'] += 1
        changed = True
    
    # Enrich treatments
    detected_treatments = detect_items(text, TREATMENT_PATTERNS)
    existing = post.get('treatments_mentioned', [])
    if not isinstance(existing, list):
        existing = []
    merged = list(set(existing + detected_treatments))
    if set(merged) != set(existing):
        post['treatments_mentioned'] = sorted(merged)
        field_enriched['treatments_mentioned'] += 1
        changed = True
    
    if changed:
        enriched_count += 1

# Save
with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=2)

print(f"Total posts: {len(posts)}")
print(f"Posts enriched: {enriched_count}")
for field, count in field_enriched.items():
    print(f"  {field}: {count} posts updated")

# Recheck gaps after enrichment
metadata_fields = ['conditions_mentioned', 'surgery_types_mentioned', 'products_mentioned', 'treatments_mentioned']
still_missing = {f: 0 for f in metadata_fields}
for p in posts:
    for f in metadata_fields:
        val = p.get(f)
        if val is None or val == [] or val == '':
            still_missing[f] += 1
print("\nRemaining gaps after enrichment:")
for f, count in still_missing.items():
    print(f"  {f}: {count}")
