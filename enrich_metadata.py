import json
import re
from collections import Counter

CONDITIONS = {
    'plantar fasciitis': ['plantar fasciitis', 'plantar fascitis', 'plantar faciitis', 'plantar fascia'],
    'bunion': ['bunion', 'bunions', 'hallux valgus'],
    'hammer toe': ['hammer toe', 'hammertoe', 'hammer toes', 'hammertoes'],
    'heel spur': ['heel spur', 'heel spurs'],
    'bone spur': ['bone spur', 'bone spurs'],
    "Morton's neuroma": ['neuroma', "morton's neuroma", 'mortons neuroma', 'morton neuroma'],
    'ingrown toenail': ['ingrown toenail', 'ingrown nail', 'ingrown toenails'],
    'toenail fungus': ['toenail fungus', 'nail fungus', 'fungal nail', 'onychomycosis', 'fungal toenail', 'fungus nail', 'fungus toenail', 'yellow nail', 'thick nail'],
    'Achilles tendonitis': ['achilles tendonitis', 'achilles tendinitis', 'achilles tendinopathy', 'achilles tear', 'achilles rupture', 'achilles injury'],
    'flat feet': ['flat feet', 'flat foot', 'fallen arches', 'fallen arch', 'pes planus', 'overpronation'],
    'neuropathy': ['neuropathy', 'peripheral neuropathy', 'nerve damage', 'nerve pain', 'diabetic neuropathy'],
    'gout': ['gout', 'gouty'],
    'metatarsalgia': ['metatarsalgia', 'ball of foot pain', 'metatarsal pain'],
    'heel fat pad syndrome': ['heel fat pad', 'fat pad syndrome', 'fat pad atrophy'],
    'posterior tibial tendon dysfunction': ['posterior tibial', 'pttd'],
    'sesamoiditis': ['sesamoiditis', 'sesamoid'],
    'tarsal tunnel syndrome': ['tarsal tunnel'],
    'stress fracture': ['stress fracture', 'stress fractures', 'hairline fracture'],
    'arthritis': ['arthritis', 'osteoarthritis', 'rheumatoid arthritis'],
    'corns and calluses': ['callus', 'calluses', 'callous', 'corns'],
    'plantar warts': ['plantar wart', 'plantar warts', 'verruca'],
    'bursitis': ['bursitis'],
    'capsulitis': ['capsulitis'],
    'edema': ['edema', 'swollen feet', 'swollen foot', 'swollen ankle'],
}

SURGERY_TYPES = {
    'Lapiplasty': ['lapiplasty'],
    'bunionectomy': ['bunionectomy'],
    'osteotomy': ['osteotomy', 'chevron osteotomy', 'scarf osteotomy', 'akin osteotomy', 'weil osteotomy'],
    'fusion': ['fusion', 'arthrodesis'],
    'plantar fascia release': ['plantar fascia release', 'fasciotomy', 'fascia release'],
    'hardware removal': ['hardware removal', 'screw removal', 'pin removal', 'plate removal', 'remove hardware', 'remove screws'],
    'revision surgery': ['revision surgery'],
    'hammertoe surgery': ['hammertoe surgery', 'hammer toe surgery', 'toe straightening surgery'],
    'neuroma surgery': ['neuroma surgery', 'neuroma excision', 'neurectomy'],
    'nail surgery': ['nail avulsion', 'matrixectomy', 'partial nail removal', 'nail surgery'],
    'tarsal tunnel release': ['tarsal tunnel release', 'tarsal tunnel surgery'],
    'Achilles surgery': ['achilles surgery', 'achilles repair', 'achilles reconstruction'],
    'tendon repair': ['tendon repair', 'tendon surgery', 'tendon transfer'],
    'minimally invasive surgery': ['minimally invasive', 'mis surgery'],
}

PRODUCTS = {
    'Hoka': ['hoka', 'hokas'],
    'Brooks': ['brooks'],
    'New Balance': ['new balance'],
    'Altra': ['altra', 'altras'],
    'OOFOS': ['oofos'],
    'Birkenstock': ['birkenstock', 'birkenstocks', 'birks'],
    'Vionic': ['vionic'],
    'Correct Toes': ['correct toes'],
    'Skechers': ['skechers', 'sketchers'],
    'Crocs': ['crocs'],
    'Strassburg Sock': ['strassburg sock', 'strassburg'],
    'Vicks VapoRub': ['vicks', 'vaporub'],
    'tea tree oil': ['tea tree oil', 'tea tree'],
    'Lamisil': ['lamisil', 'terbinafine'],
    'Jublia': ['jublia'],
    'walking boot': ['walking boot', 'cam boot', 'air cast', 'aircast'],
    'orthotics': ['orthotics', 'orthotic inserts', 'custom orthotics', 'insoles', 'arch support', 'arch supports', 'superfeet', 'powerstep'],
    'Voltaren': ['voltaren', 'diclofenac'],
    'ibuprofen': ['ibuprofen', 'advil', 'motrin'],
    'Gabapentin': ['gabapentin', 'neurontin'],
    'Epsom salt': ['epsom salt', 'epsom salts'],
    'KT Tape': ['kt tape', 'kinesiology tape'],
    'massage gun': ['theragun', 'massage gun'],
    'compression socks': ['compression socks', 'compression stockings', 'compression sleeve'],
    'toe spacers': ['toe spacers', 'toe separators', 'toe spreaders'],
    'Xero Shoes': ['xero shoes'],
    'Vivobarefoot': ['vivobarefoot'],
    'night splint': ['night splint', 'night splints'],
}

TREATMENTS = {
    'cortisone injection': ['cortisone', 'cortisone injection', 'cortisone shot', 'steroid injection', 'steroid shot'],
    'physical therapy': ['physical therapy', 'physiotherapy', 'pt exercises', 'rehab exercises'],
    'shockwave therapy': ['shockwave', 'eswt', 'shock wave therapy'],
    'dry needling': ['dry needling'],
    'acupuncture': ['acupuncture'],
    'ice therapy': ['icing', 'frozen bottle', 'ice bath', 'cold therapy'],
    'stretching': ['stretching', 'calf stretch', 'calf stretches', 'towel stretch', 'wall stretch', 'plantar stretch'],
    'massage therapy': ['foot massage', 'deep tissue massage', 'lacrosse ball', 'golf ball massage'],
    'taping': ['taping', 'low-dye taping'],
    'PRP injection': ['prp', 'platelet rich plasma'],
    'laser therapy': ['laser therapy', 'laser treatment', 'cold laser', 'mls laser'],
    'ultrasound therapy': ['ultrasound therapy', 'therapeutic ultrasound'],
    'Graston technique': ['graston'],
    'vinegar soak': ['vinegar soak', 'apple cider vinegar soak'],
    'essential oils': ['essential oil', 'essential oils'],
    'rolling': ['foam roller', 'frozen water bottle roll'],
    'surgery': ['surgery', 'surgical', 'operation', 'procedure'],
}

def normalize_existing(val):
    """Convert existing metadata to a clean list."""
    if not val:
        return []
    if isinstance(val, str):
        if not val.strip():
            return []
        return [item.strip() for item in val.split(',') if item.strip()]
    if isinstance(val, list):
        result = []
        for item in val:
            if isinstance(item, str):
                for sub in item.split(','):
                    sub = sub.strip()
                    if sub and len(sub) > 1:
                        result.append(sub)
        return result
    return []

def get_full_text(post):
    text = post.get('body', '') or ''
    for comment in post.get('comments', []):
        if isinstance(comment, str):
            text += ' ' + comment
        elif isinstance(comment, dict):
            text += ' ' + comment.get('text', '') + ' ' + comment.get('body', '')
    return text.lower()

def detect_items(text, dictionary):
    found = set()
    for label, keywords in dictionary.items():
        for kw in keywords:
            if len(kw) <= 4:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found.add(label)
                    break
            else:
                if kw in text:
                    found.add(label)
                    break
    return list(found)

def enrich_posts(posts):
    enriched_count = 0
    for post in posts:
        text = get_full_text(post)
        changed = False

        for field, dictionary in [
            ('conditions_mentioned', CONDITIONS),
            ('surgery_types_mentioned', SURGERY_TYPES),
            ('products_mentioned', PRODUCTS),
            ('treatments_mentioned', TREATMENTS),
        ]:
            existing = normalize_existing(post.get(field))
            detected = detect_items(text, dictionary)
            merged = list(set(existing + detected))
            
            # Normalize the field regardless (fix string/list inconsistency)
            if post.get(field) != merged:
                post[field] = merged
                changed = True

        if changed:
            enriched_count += 1

    return posts, enriched_count

posts = json.load(open('posts.json'))
posts, enriched = enrich_posts(posts)

with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=2)

print(f'Total posts: {len(posts)}')
print(f'Posts enriched/normalized: {enriched}')

# Post-enrichment stats
missing_c = sum(1 for p in posts if not p.get('conditions_mentioned'))
missing_s = sum(1 for p in posts if not p.get('surgery_types_mentioned'))
missing_p = sum(1 for p in posts if not p.get('products_mentioned'))
missing_t = sum(1 for p in posts if not p.get('treatments_mentioned'))
print(f'Still missing conditions: {missing_c}')
print(f'Still missing surgery types: {missing_s}')
print(f'Still missing products: {missing_p}')
print(f'Still missing treatments: {missing_t}')

total_comments = sum(len(p.get('comments', [])) for p in posts)
posts_with_comments = sum(1 for p in posts if p.get('comments'))
print(f'\nTotal comments: {total_comments}')
print(f'Posts with comments: {posts_with_comments} ({posts_with_comments*100//len(posts)}%)')

all_conditions = []
all_surgery = []
all_products = []
all_treatments = []
for p in posts:
    all_conditions.extend(p.get('conditions_mentioned', []))
    all_surgery.extend(p.get('surgery_types_mentioned', []))
    all_products.extend(p.get('products_mentioned', []))
    all_treatments.extend(p.get('treatments_mentioned', []))

print('\n--- TOP CONDITIONS ---')
for item, count in Counter(all_conditions).most_common(15):
    print(f'  {item}: {count}')
print('\n--- TOP SURGERY TYPES ---')
for item, count in Counter(all_surgery).most_common(10):
    print(f'  {item}: {count}')
print('\n--- TOP PRODUCTS ---')
for item, count in Counter(all_products).most_common(15):
    print(f'  {item}: {count}')
print('\n--- TOP TREATMENTS ---')
for item, count in Counter(all_treatments).most_common(15):
    print(f'  {item}: {count}')
