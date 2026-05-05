import json
import re

with open('posts.json') as f:
    posts = json.load(f)

# Comprehensive keyword dictionaries for detection
CONDITIONS = {
    'bunion': r'\bbunion[s]?\b',
    'hallux valgus': r'\bhallux\s+valgus\b',
    'hallux rigidus': r'\bhallux\s+rigidus\b',
    'hammer toe': r'\bhammer\s*toe[s]?\b',
    'claw toe': r'\bclaw\s*toe[s]?\b',
    'mallet toe': r'\bmallet\s*toe[s]?\b',
    'plantar fasciitis': r'\bplantar\s+fasciitis\b',
    'heel spur': r'\bheel\s+spur[s]?\b',
    'heel pain': r'\bheel\s+pain\b',
    'flat feet': r'\bflat\s+f[eo]{2}t\b',
    'fallen arches': r'\bfallen\s+arch(es)?\b',
    'high arches': r'\bhigh\s+arch(es)?\b',
    'morton\'s neuroma': r'\bmorton\'?s?\s+neuroma\b',
    'neuroma': r'\bneuroma\b',
    'neuropathy': r'\bneuropathy\b',
    'peripheral neuropathy': r'\bperipheral\s+neuropathy\b',
    'toenail fungus': r'\btoenail\s+fungus\b',
    'fungal nail': r'\bfungal\s+nail\b',
    'onychomycosis': r'\bonychomycosis\b',
    'ingrown toenail': r'\bingrown\s+toenail[s]?\b',
    'gout': r'\bgout\b',
    'arthritis': r'\barthritis\b',
    'sesamoiditis': r'\bsesamoiditis\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'bone spur': r'\bbone\s+spur[s]?\b',
    'stress fracture': r'\bstress\s+fracture[s]?\b',
    'tendonitis': r'\btendonitis\b',
    'tendinitis': r'\btendinitis\b',
    'achilles tendon': r'\bachilles\s+tendon\b',
    'plantar plate tear': r'\bplantar\s+plate\s+tear\b',
    'tailor\'s bunion': r'\btailor\'?s?\s+bunion\b',
    'bunionette': r'\bbunionette\b',
    'capsulitis': r'\bcapsulitis\b',
    'swelling': r'\bswelling\b',
    'nerve pain': r'\bnerve\s+pain\b',
    'numbness': r'\bnumbness\b',
    'tingling': r'\btingling\b',
    'infection': r'\binfection\b',
    'wound': r'\bwound\b',
    'scar tissue': r'\bscar\s+tissue\b',
    'dvt': r'\b(dvt|deep\s+vein\s+thrombosis)\b',
    'blood clot': r'\bblood\s+clot[s]?\b',
    'diabetic foot': r'\bdiabetic\s+foot\b',
    'diabetes': r'\bdiabet(es|ic)\b',
}

SURGERY_TYPES = {
    'lapiplasty': r'\blapiplasty\b',
    'bunionectomy': r'\bbunionectomy\b',
    'osteotomy': r'\bosteotomy\b',
    'chevron osteotomy': r'\bchevron\s+osteotomy\b',
    'scarf osteotomy': r'\bscarf\s+osteotomy\b',
    'akin osteotomy': r'\bakin\s+osteotomy\b',
    'scarf akin': r'\bscarf[\s-]+akin\b',
    'Austin bunionectomy': r'\baustin\s+bunionectomy\b',
    'MIS': r'\b(mis|minimally\s+invasive)\b',
    'arthrodesis': r'\barthrodesis\b',
    'fusion': r'\bfusion\b',
    'hardware removal': r'\bhardware\s+removal\b',
    'revision surgery': r'\brevision\s+surgery\b',
    'hammer toe surgery': r'\bhammer\s*toe\s+surgery\b',
    'amputation': r'\bamputation\b',
    'MICA': r'\bmica\b',
    'lapidus': r'\blapidus\b',
    'bilateral': r'\bbilateral\b',
}

PRODUCTS = {
    'Hoka': r'\bhoka\b',
    'New Balance': r'\bnew\s+balance\b',
    'Skechers': r'\bskechers\b',
    'Brooks': r'\bbrooks\b',
    'Orthofeet': r'\borthofeet\b',
    'Vionic': r'\bvionic\b',
    'Oofos': r'\boofos\b',
    'Correct Toes': r'\bcorrect\s+toes\b',
    'Vicks VapoRub': r'\bvicks?\s*(vaporub)?\b',
    'Kerasal': r'\bkerasal\b',
    'Lamisil': r'\blamisil\b',
    'terbinafine': r'\bterbinafine\b',
    'Jublia': r'\bjublia\b',
    'tea tree oil': r'\btea\s+tree\s+oil\b',
    'apple cider vinegar': r'\bapple\s+cider\s+vinegar\b',
    'knee scooter': r'\bknee\s+scooter\b',
    'iWalk': r'\biwalk\b',
    'walking boot': r'\b(walking\s+boot|cam\s+boot|surgical\s+boot)\b',
    'orthotics': r'\borthotics?\b',
    'custom orthotics': r'\bcustom\s+orthotics?\b',
    'toe spacers': r'\btoe\s+spacer[s]?\b',
    'bunion corrector': r'\bbunion\s+corrector[s]?\b',
    'night splint': r'\bnight\s+splint[s]?\b',
    'compression socks': r'\bcompression\s+socks?\b',
    'Voltaren': r'\bvoltaren\b',
    'biofreeze': r'\bbiofreeze\b',
    'Epsom salt': r'\bepsom\s+salt[s]?\b',
    'ice machine': r'\bice\s+machine\b',
    'CROCS': r'\bcrocs\b',
    'Birkenstock': r'\bbirkenstock[s]?\b',
    'Altra': r'\baltra\b',
}

TREATMENTS = {
    'surgery': r'\bsurger(y|ies)\b',
    'physical therapy': r'\b(physical\s+therapy|pt\b)',
    'cortisone': r'\bcortisone\b',
    'steroid injection': r'\bsteroid\s+injection[s]?\b',
    'cortisone injection': r'\bcortisone\s+(injection|shot)[s]?\b',
    'shockwave therapy': r'\bshockwave\s+therapy\b',
    'ESWT': r'\beswt\b',
    'PRP': r'\bprp\b',
    'platelet rich plasma': r'\bplatelet\s+rich\s+plasma\b',
    'laser treatment': r'\blaser\s+treatment\b',
    'acupuncture': r'\bacupuncture\b',
    'stretching': r'\bstretch(ing|es)?\b',
    'icing': r'\b(icing|ice\s+pack)\b',
    'elevation': r'\belevat(ion|e|ed|ing)\b',
    'rest': r'\brest(ing)?\b',
    'medication': r'\bmedication[s]?\b',
    'anti-inflammatory': r'\banti[\s-]?inflammator(y|ies)\b',
    'ibuprofen': r'\bibuprofen\b',
    'gabapentin': r'\bgabapentin\b',
    'nerve block': r'\bnerve\s+block\b',
    'dry needling': r'\bdry\s+needling\b',
    'massage': r'\bmassage\b',
    'ultrasound': r'\bultrasound\b',
    'taping': r'\btaping\b',
    'vinegar soak': r'\bvinegar\s+soak\b',
    'home remedy': r'\bhome\s+remed(y|ies)\b',
    'antifungal': r'\bantifungal\b',
    'topical treatment': r'\btopical\s+treatment\b',
    'weight bearing': r'\bweight\s+bear(ing)?\b',
    'non-weight bearing': r'\bnon[\s-]?weight\s+bear(ing)?\b',
}

def detect_metadata(text, keyword_dict):
    """Detect keywords in text, return comma-separated matches."""
    text_lower = text.lower()
    found = []
    for name, pattern in keyword_dict.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found.append(name)
    return ', '.join(found)

enriched_count = 0
for p in posts:
    # Build full text including comments
    full_text = p.get('body', '')
    for c in p.get('comments', []):
        if isinstance(c, dict):
            full_text += ' ' + c.get('text', '') + ' ' + c.get('body', '')
        elif isinstance(c, str):
            full_text += ' ' + c
    
    changed = False
    
    if not p.get('conditions_mentioned'):
        detected = detect_metadata(full_text, CONDITIONS)
        if detected:
            p['conditions_mentioned'] = detected
            changed = True
    
    if not p.get('surgery_types_mentioned'):
        detected = detect_metadata(full_text, SURGERY_TYPES)
        if detected:
            p['surgery_types_mentioned'] = detected
            changed = True
    
    if not p.get('products_mentioned'):
        detected = detect_metadata(full_text, PRODUCTS)
        if detected:
            p['products_mentioned'] = detected
            changed = True
    
    if not p.get('treatments_mentioned'):
        detected = detect_metadata(full_text, TREATMENTS)
        if detected:
            p['treatments_mentioned'] = detected
            changed = True
    
    if changed:
        enriched_count += 1

print(f"Enriched {enriched_count} posts with detected metadata")

# Final stats
empty_conditions = sum(1 for p in posts if not p.get('conditions_mentioned'))
empty_surgery = sum(1 for p in posts if not p.get('surgery_types_mentioned'))
empty_products = sum(1 for p in posts if not p.get('products_mentioned'))
empty_treatments = sum(1 for p in posts if not p.get('treatments_mentioned'))
print(f"Remaining empty after enrichment:")
print(f"  Empty conditions: {empty_conditions}")
print(f"  Empty surgery types: {empty_surgery}")
print(f"  Empty products: {empty_products}")
print(f"  Empty treatments: {empty_treatments}")

with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=2)
print("Saved enriched posts.json")
