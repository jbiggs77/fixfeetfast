import json
import re

with open('posts.json') as f:
    posts = json.load(f)

CONDITIONS = {
    'bunion': r'\bbunion[s]?\b',
    'hallux valgus': r'\bhallux\s*v[ao]l[gv]us\b',
    'plantar fasciitis': r'\bplantar\s*fasc[i]*[t]*is\b',
    'hammer toe': r'\bhammer\s*toe[s]?\b',
    'flat feet': r'\bflat\s*f[eo][eo]t\b',
    'heel spur': r'\bheel\s*spur[s]?\b',
    'mortons neuroma': r"\bmorton'?s?\s*neuroma\b",
    'gout': r'\bgout\b',
    'neuropathy': r'\bneuropath[yic]\b',
    'arthritis': r'\barthritis\b',
    'tendonitis': r'\btendon[i]*tis\b',
    'achilles tendonitis': r'\bachilles\s*(tendon[i]*tis|tear|rupture)\b',
    'ingrown toenail': r'\bingrown\s*toe\s*nail[s]?\b',
    'toenail fungus': r'\b(toenail|nail)\s*fungus\b|\bonychomycosis\b',
    'bone spur': r'\bbone\s*spur[s]?\b',
    'sesamoiditis': r'\bsesamoid[i]*tis\b',
    'metatarsalgia': r'\bmetatarsalgia\b',
    'swelling': r'\bswell(ing|ed|s)\b',
    'numbness': r'\bnumb(ness)?\b',
}

SURGERIES = {
    'Lapiplasty': r'\blapiplasty\b',
    'bunionectomy': r'\bbunionectomy\b',
    'osteotomy': r'\bosteotom[yies]+\b',
    'scarf osteotomy': r'\bscarf\s*(osteotomy|procedure)\b',
    'chevron osteotomy': r'\bchevron\s*(osteotomy|procedure)\b',
    'fusion': r'\b(joint|toe|foot|bone)\s*fusion\b|\bfusion\s*(surgery|procedure)\b',
    'hardware removal': r'\bhardware\s*remov(al|ed|ing)\b',
    'minimally invasive': r'\bminimally\s*invasive\b',
}

PRODUCTS = {
    'Hoka': r'\bhoka[s]?\b',
    'Correct Toes': r'\bcorrect\s*toes?\b',
    'orthotics': r'\borthotic[s]?\b|\binsole[s]?\b|\binsert[s]?\b',
    'toe spacers': r'\btoe\s*spacer[s]?\b|\btoe\s*separator[s]?\b',
    'bunion splint': r'\bbunion\s*splint[s]?\b',
    'night splint': r'\bnight\s*splint[s]?\b',
    'walking boot': r'\b(walking|cam)\s*boot\b',
    'knee scooter': r'\bknee\s*scooter[s]?\b|\biWalk\b',
    'New Balance': r'\bnew\s*balance\b',
    'Brooks': r'\bbrooks\b',
    'ASICS': r'\basics\b',
    'Birkenstock': r'\bbirkenstock[s]?\b',
    'Oofos': r'\boofos\b',
    'Vionic': r'\bvionic[s]?\b',
    'Skechers': r'\bskecher[s]?\b',
    'compression socks': r'\bcompression\s*(sock[s]?|stocking[s]?)\b',
    'crutches': r'\bcrutch(es)?\b',
    'KT tape': r'\bkt\s*tape\b|\bkinesio\s*tape\b',
    'Vicks': r'\bvicks\b',
    'Listerine': r'\blisterine\b',
    'tea tree oil': r'\btea\s*tree\b',
    'lidocaine': r'\blidocaine\b',
}

TREATMENTS = {
    'cortisone injection': r'\bcortisone\b',
    'steroid injection': r'\bsteroid\s*(injection|shot|jab)[s]?\b',
    'physical therapy': r'\bphysical\s*therap[yist]+\b|\bphysio\s*therap[yist]+\b',
    'shockwave therapy': r'\bshockwave\b|\bESWT\b',
    'stretching': r'\bstretch(ing|es)?\b',
    'massage': r'\bmassag(e|ing)\b',
    'acupuncture': r'\bacupuncture\b',
    'anti-inflammatory': r'\banti.?inflammator[yies]+\b|\bibuprofen\b|\bnaproxen\b|\badvil\b|\baleve\b',
    'PRP': r'\bPRP\b|\bplatelet.?rich\s*plasma\b',
    'custom orthotics': r'\bcustom\s*orthotic[s]?\b',
    'toe exercises': r'\btoe\s*exercis\b|\btoe\s*yoga\b',
    'elevation': r'\belev(ating|ation|ate)\b',
}

def detect(text, patterns):
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

metadata_fields = ['conditions_mentioned', 'surgery_types_mentioned', 'products_mentioned', 'treatments_mentioned']
enriched_count = 0

for i, post in enumerate(posts):
    all_empty = all(not post.get(f, []) for f in metadata_fields)
    if not all_empty:
        continue
    
    text = post.get('body', '')
    for comment in post.get('comments', []):
        if isinstance(comment, str):
            text += ' ' + comment
        elif isinstance(comment, dict):
            text += ' ' + comment.get('text', '')
    
    if not text.strip():
        continue
    
    conditions = detect(text, CONDITIONS)
    surgeries = detect(text, SURGERIES)
    products = detect(text, PRODUCTS)
    treatments = detect(text, TREATMENTS)
    
    if conditions or surgeries or products or treatments:
        post['conditions_mentioned'] = conditions
        post['surgery_types_mentioned'] = surgeries
        post['products_mentioned'] = products
        post['treatments_mentioned'] = treatments
        enriched_count += 1

print(f'Enriched {enriched_count} posts out of 62 with all-empty metadata')

with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)
print('Saved updated posts.json')

# Stats
total_comments = 0
posts_with_comments = 0
for p in posts:
    c_count = len(p.get('comments', []))
    total_comments += c_count
    if c_count > 0:
        posts_with_comments += 1

print(f'\nTotal posts: {len(posts)}')
print(f'Total comments: {total_comments}')
print(f'Posts with comments: {posts_with_comments} ({posts_with_comments*100//len(posts)}%)')
