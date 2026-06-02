import json
import re

with open('posts.json') as f:
    posts = json.load(f)

# Keyword dictionaries for detection
CONDITIONS = {
    'bunion': ['bunion', 'hallux valgus', 'bunionette'],
    'plantar fasciitis': ['plantar fasciitis', 'plantar fascia', 'heel pain', 'heel spur'],
    'toenail fungus': ['toenail fungus', 'fungal nail', 'fungal toenail', 'onychomycosis', 'nail fungus', 'fungus'],
    'hammer toe': ['hammer toe', 'hammertoe', 'claw toe'],
    'foot pain': ['foot pain', 'metatarsalgia', 'ball of foot', 'forefoot'],
    'ingrown toenail': ['ingrown toenail', 'ingrown nail'],
    'morton\'s neuroma': ['morton', 'neuroma'],
    'neuropathy': ['neuropathy', 'nerve pain', 'tingling', 'numbness in feet'],
    'gout': ['gout', 'uric acid'],
    'flat feet': ['flat feet', 'flat foot', 'fallen arch'],
    'surgery recovery': ['recovery', 'post op', 'post-op', 'weeks post', 'check up', 'checkup', 'follow up', 'healing', 'returning to work', 'return to work', 'pin removed', 'stitches', 'stitch', 'incision', 'wound'],
    'toenail damage': ['toenail fell off', 'nail fell off', 'lost toenail', 'damaged nail', 'nail damage', 'brown stain', 'toenail'],
    'top of foot pain': ['top of foot'],
    'bone spur': ['bone spur', 'bone growing'],
    'neuro sheath tumor': ['neuro sheath tumor'],
}

SURGERY_TYPES = {
    'Lapiplasty': ['lapiplasty', 'lapid'],
    'bunionectomy': ['bunionectomy'],
    'osteotomy': ['osteotomy'],
    'pin removal': ['pin removed', 'pin removal'],
    'biopsy': ['biopsy'],
}

PRODUCTS = {
    'Hoka': ['hoka'],
    'Correct Toes': ['correct toes'],
    'nail adhesive tabs': ['nail adhesive', 'adhesive tabs'],
    'Nonyx': ['nonyx'],
    'boric acid': ['boric acid'],
    'copper peptides': ['copper peptide'],
    'Primark': ['primark'],
    'band-aid': ['band-aid', 'bandaid'],
    'wide toe box shoes': ['wide toe box', 'wider toe box'],
    'orthotics': ['orthotic', 'orthotics', 'insole', 'insoles'],
    'slippers': ['slipper', 'slippers'],
}

TREATMENTS = {
    'physical therapy': ['physical therapy', 'pt exercises', 'range of motion'],
    'boot/cast': ['boot', 'cast', 'walking boot'],
    'cortisone': ['cortisone', 'steroid injection'],
    'shockwave therapy': ['shockwave', 'shock wave'],
    'topical treatment': ['treatment', 'concoction', 'cream'],
    'surgery': ['surgery', 'surgeon', 'operated', 'operation'],
    'barefoot walking': ['barefoot', 'walking barefoot'],
    'weight loss': ['lose weight'],
}

def detect_metadata(text):
    text_lower = text.lower()
    conditions = []
    surgeries = []
    products = []
    treatments = []
    
    for label, keywords in CONDITIONS.items():
        for kw in keywords:
            if kw in text_lower:
                conditions.append(label)
                break
    
    for label, keywords in SURGERY_TYPES.items():
        for kw in keywords:
            if kw in text_lower:
                surgeries.append(label)
                break
    
    for label, keywords in PRODUCTS.items():
        for kw in keywords:
            if kw in text_lower:
                products.append(label)
                break
    
    for label, keywords in TREATMENTS.items():
        for kw in keywords:
            if kw in text_lower:
                treatments.append(label)
                break
    
    return conditions, surgeries, products, treatments

# Known spam/off-topic patterns
SPAM_PATTERNS = [
    'deck builder', 'concrete contractor', 'real estate', 'auction',
    'southwest companion', 'southwest rapid reward', 'subscription program',
    'parade theme', 'delorean', 'jurassic park', 'book movie cars',
    'water in the village', 'shower water filter', 'water system',
    'granville leaders', 'housing development', 'fox 28 columbus',
    'drill day', 'elite foot health the onyx version'
]

enriched_count = 0
spam_count = 0

for i, p in enumerate(posts):
    if (not p.get('conditions_mentioned') and 
        not p.get('surgery_types_mentioned') and 
        not p.get('products_mentioned') and 
        not p.get('treatments_mentioned')):
        
        body = p.get('body', '') or ''
        comments = ' '.join(p.get('comments', []))
        full_text = body + ' ' + comments
        
        # Check for spam
        is_spam = any(sp in full_text.lower() for sp in SPAM_PATTERNS)
        if is_spam:
            spam_count += 1
            continue
        
        conditions, surgeries, products, treatments = detect_metadata(full_text)
        
        if conditions or surgeries or products or treatments:
            p['conditions_mentioned'] = conditions
            p['surgery_types_mentioned'] = surgeries
            p['products_mentioned'] = products
            p['treatments_mentioned'] = treatments
            enriched_count += 1
            print(f"Enriched index {i}: conditions={conditions}, surgeries={surgeries}, products={products}, treatments={treatments}")

print(f"\nTotal enriched: {enriched_count}")
print(f"Spam/off-topic skipped: {spam_count}")

with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=2)
print("Saved posts.json")
