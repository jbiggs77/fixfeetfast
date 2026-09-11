"""Site taxonomy and legacy input cleanup retained from the original builder."""

import json

import os

from pathlib import Path

from datetime import datetime

from collections import defaultdict

from urllib.parse import quote

from site_media import render_images, render_comment

def normalize_posts_metadata(posts):
    """Convert list metadata fields back to comma-separated strings for generator compatibility."""
    for post in posts:
        for field in ['conditions_mentioned', 'surgery_types_mentioned', 'treatments_mentioned', 'products_mentioned']:
            val = post.get(field, '')
            if isinstance(val, list):
                post[field] = ', '.join(str(x) for x in val if x)
            elif val is None:
                post[field] = ''
    return posts

NICHE_MAP = {'bunion-surgery-recovery': {'title': 'Bunion Surgery Recovery', 'keywords': ['bunion surgery', 'bunion recovery', 'bunionectomy', 'post-op bunion'], 'related': ['bunion-surgery-swelling', 'walking-after-surgery', 'post-surgery-shoes', 'bunion-surgery-pain']}, 'minimally-invasive-bunion-surgery': {'title': 'Minimally Invasive Bunion Surgery (MIS)', 'keywords': ['mis', 'minimally invasive', 'mis bunion', 'keyhole bunion'], 'related': ['bunion-surgery-recovery', 'lapiplasty-surgery', 'scarf-akin-osteotomy', 'walking-after-surgery']}, 'lapiplasty-surgery': {'title': 'Lapiplasty 3D Bunion Surgery', 'keywords': ['lapiplasty', '3d bunion', 'lapiplasty procedure'], 'related': ['bunion-surgery-recovery', 'minimally-invasive-bunion-surgery', 'walking-after-surgery', 'bunion-surgery-complications']}, 'hammer-toe-surgery': {'title': 'Hammer Toe Surgery & Correction', 'keywords': ['hammer toe', 'hammertoe', 'toe fusion', 'claw toe', 'mallet toe'], 'related': ['bunion-surgery-recovery', 'post-surgery-shoes', 'walking-after-surgery', 'physical-therapy-foot']}, 'bunion-surgery-swelling': {'title': 'Post-Surgery Swelling & Inflammation', 'keywords': ['swelling', 'inflammation', 'edema', 'swollen foot', 'swollen toe'], 'related': ['bunion-surgery-recovery', 'bunion-surgery-pain', 'walking-after-surgery', 'physical-therapy-foot']}, 'post-surgery-shoes': {'title': 'Best Shoes After Foot Surgery', 'keywords': ['shoes', 'sneakers', 'trainers', 'footwear', 'orthofeet', 'hoka', 'new balance', 'skechers', 'wide shoes'], 'related': ['bunion-surgery-recovery', 'bunion-surgery-swelling', 'walking-after-surgery', 'toe-spacers-orthotics']}, 'bunion-surgery-pain': {'title': 'Pain Management After Foot Surgery', 'keywords': ['pain', 'pain management', 'nerve pain', 'throbbing', 'aching'], 'related': ['bunion-surgery-recovery', 'bunion-surgery-swelling', 'bunion-surgery-complications', 'physical-therapy-foot']}, 'walking-after-surgery': {'title': 'Walking & Weight Bearing After Surgery', 'keywords': ['walking', 'weight bearing', 'non weight bearing', 'nwb', 'crutches', 'knee scooter', 'boot', 'cast'], 'related': ['bunion-surgery-recovery', 'post-surgery-shoes', 'physical-therapy-foot', 'bunion-surgery-swelling']}, 'scarf-akin-osteotomy': {'title': 'Scarf & Akin Osteotomy', 'keywords': ['scarf', 'akin', 'scarf akin', 'osteotomy', 'chevron'], 'related': ['bunion-surgery-recovery', 'minimally-invasive-bunion-surgery', 'walking-after-surgery', 'bunion-surgery-pain']}, 'bunion-surgery-complications': {'title': 'Surgery Complications & Wound Healing', 'keywords': ['infection', 'wound', 'complication', 'hardware', 'screw', 'pin', 'scar', 'keloid'], 'related': ['bunion-surgery-recovery', 'bunion-surgery-pain', 'bunion-surgery-swelling', 'physical-therapy-foot']}, 'physical-therapy-foot': {'title': 'Physical Therapy & Foot Exercises', 'keywords': ['physical therapy', 'pt', 'exercises', 'stretching', 'range of motion', 'rom', 'rehab'], 'related': ['bunion-surgery-recovery', 'walking-after-surgery', 'bunion-surgery-pain', 'bunion-surgery-swelling']}, 'toe-spacers-orthotics': {'title': 'Toe Spacers, Orthotics & Braces', 'keywords': ['toe spacer', 'toe separator', 'orthotic', 'insole', 'bunion corrector', 'splint', 'brace'], 'related': ['bunion-surgery-recovery', 'post-surgery-shoes', 'flat-feet-arch-support', 'plantar-fasciitis']}, 'flat-feet-arch-support': {'title': 'Flat Feet & Arch Support', 'keywords': ['flat feet', 'flat foot', 'arch', 'arch support', 'fallen arch', 'pronation', 'overpronation'], 'related': ['post-surgery-shoes', 'toe-spacers-orthotics', 'plantar-fasciitis', 'physical-therapy-foot']}, 'plantar-fasciitis': {'title': 'Plantar Fasciitis Treatment', 'keywords': ['plantar fasciitis', 'heel pain', 'heel spur', 'plantar', 'fascia'], 'related': ['post-surgery-shoes', 'toe-spacers-orthotics', 'flat-feet-arch-support', 'physical-therapy-foot']}, 'toenail-fungus': {'title': 'Toenail Fungus Treatment', 'keywords': ['toenail fungus', 'fungal nail', 'onychomycosis', 'fungus', 'antifungal', 'terbinafine', 'lamisil'], 'related': ['post-surgery-shoes', 'physical-therapy-foot', 'flat-feet-arch-support', 'toe-spacers-orthotics']}}

def slugify(text, post_id):
    """Generate URL-friendly slug from post body text"""
    import re

    # Take first ~60 chars of text
    text = text[:60] if text else ""

    # Lowercase and strip non-alphanumeric (keep spaces)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Trim hyphens from ends
    text = text.strip('-')

    # If slug is empty or very short, use fallback
    if not text or len(text) < 3:
        return f"discussion-{post_id}"

    return text

import re

BADGE = r"(?:All-star contributor|Top contributor|Rising contributor|New contributor|Group expert(?: in [A-Z][\w &-]*?(?=\s+[A-Z]|$))?|Admin|Moderator|Top fan|Follow)"

VIEWS = r"(?:View (?:all )?\d+ (?:replies|reply|Replies|Reply)|View more (?:answers|comments)|View previous comments|Hide \d+ replies|\d+ (?:Reply|Replies))"

ASJ   = r"(?:Answer|Comment) as Justin\b"

NAME  = r"[A-Z][\w'’.-]*(?: (?:[A-Z][\w'’.-]*|Jr\.?|Sr\.?|II|III)){1,4}"

FEEL  = r"is feeling \w+\.?"

ISWITH = r"is with [A-Z][\w'’-]*(?: [A-Z][\w'’-]*){0,3}\.?"

SOURCE_GROUPS = [
    "Toenail Fungus Support & Management",
    "Plantar Fasciitis Talk and Tips Support Group",
    "Plantar Fasciitis Talk and Tips",
    "bunion surgery / foot surgery support group",
    "Bunion Surgery / Foot Surgery Support",
    "Bunion Support Group",
    "Foot Pain Community",
    "Minimally Invasive Bunion Surgery",
    "Minimally invasive bunion surgery",
    "Forefoot Forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
    "Forefoot forum: Bunions, Hallux Limitus, Tailor's Bunion, Hammer Toes",
    "Forefoot Forum",
    "Forefoot forum",
]

_GROUPS_RE = "|".join(re.escape(g) for g in sorted(SOURCE_GROUPS, key=len, reverse=True))

POSTED_TO = rf"posted to (?:{_GROUPS_RE}|[A-Z][\w'’&/:,.-]*(?: [\w'’&/:,.-]+){{0,8}}?)™?(?=\s|$)"

AFTER_NAME = rf"(?:{BADGE}|posted to\b|replied\b|{FEEL}|{ISWITH}|·)"

LEAD = [
    re.compile(rf"^{VIEWS}\s*"),
    re.compile(rf"^{ASJ}\s*"),
    re.compile(rf"^(?:Comment|Answer|Edited|Reply)\b\s+(?=(?:Comment|Answer|Edited|Reply|View|{ASJ}|{BADGE}))"),
    re.compile(rf"^{BADGE}\s*"),
    re.compile(rf"^{POSTED_TO}\s*"),
    re.compile(rf"^(?:{_GROUPS_RE})™?\s*"),
    re.compile(rf"^{NAME}\s+(?={AFTER_NAME})"),
    re.compile(rf"^{FEEL}\s*"),
    re.compile(rf"^{ISWITH}\s*"),
    re.compile(r"^replied\b\s*"),
    re.compile(r"^[A-Za-z]{3,}\d[A-Za-z\d]*\s+(?=\S)"),   # digit-bearing usernames
    re.compile(r"^[·,:–—-]\s*"),
]

BADGE_CUT = re.compile(rf"^([^.!?]{{0,90}}?)\b{BADGE}\s*")

GLOBALS = [
    (re.compile(r"All reactions:?.*$", re.S), ""),
    (re.compile(rf"\s*{VIEWS}\s*"), " "),
    (re.compile(rf"\s*{ASJ}\s*"), " "),
    (re.compile(rf"\s*{POSTED_TO}\s*"), " "),
    (re.compile(rf"\s*(?:{_GROUPS_RE})™?\s*"), " "),
    (re.compile(r"\s*\S+ · Original audio\s*"), " "),
    (re.compile(r"\s*[……]?\s*See more\b"), " "),
    (re.compile(rf"\s*{NAME} is feeling \w+(?: in [A-Z][\w'’-]*)?\.?\s*"), " "),
    (re.compile(r"\s*(?:All-star|Top|Rising|New) contributor\s*"), " "),
    (re.compile(r"\s*Group expert(?: in [A-Z][\w &-]*?(?=\s+[A-Z]|$))?\s*"), " "),
]

GUARD_VOCAB = set("""Plantar Fasciitis Bunion Bunions Hallux Limitus Rigidus Valgus Lapiplasty Lapidus Scarf Akin
Osteotomy Achilles Morton Mortons Neuroma Hammer Toe Toes Toenail Foot Feet Heel Arch Ankle Surgery Surgeon
Podiatrist Orthopedic Ortho Doctor Dr PT Physical Therapy Therapist MRI Xray X-ray EPAT Shockwave Cortisone
Steroid Epsom Vinegar Tea Tree Oil Vicks Lamisil Tolnaftate Terbinafine Fungus Fungal KT Tape
Birkenstock Birkenstocks Hoka Hokas Oofos Vionic Altra Altras Topo Brooks Crocs Skechers Asics Kuru
New Balance Orthofeet Correct Archies Superfeet Powerstep Strutz YouTube Amazon Google Facebook TikTok
North South East West Lake Salt City Saint St Mount Mt Fort Port San Santa Los Las
Texas Florida Ohio California Georgia Michigan Indiana Missouri Wisconsin Tennessee Kentucky Alabama
Louisiana Oklahoma Arkansas Kansas Iowa Minnesota Illinois Colorado Arizona Nevada Oregon Washington Utah
Idaho Montana Wyoming Nebraska Maine Vermont Maryland Delaware Connecticut Massachusetts Pennsylvania
York Jersey Carolina Dakota Virginia Mexico Hampshire Rhode Island The""".split())

CAP_TOKEN = re.compile(r"^[A-Z][\w'’-]*$")

def _strip_post_marker_name(text):
    """After a UI marker was stripped, the next 2-3 capitalized tokens are the poster's
    name. Strip them unless they look like brand/condition/place vocabulary."""
    words = text.split()
    if len(words) < 3:
        if len(words) == 2 and all(CAP_TOKEN.match(w) for w in words) \
           and not any(w in GUARD_VOCAB for w in words):
            return ""
        return text
    if not (CAP_TOKEN.match(words[0]) and CAP_TOKEN.match(words[1])):
        return text
    if words[0] in GUARD_VOCAB or words[1] in GUARD_VOCAB:
        return text
    n = 2
    if len(words) > 3 and CAP_TOKEN.match(words[2]) and CAP_TOKEN.match(words[3]) \
       and words[2] not in GUARD_VOCAB and words[3] not in GUARD_VOCAB:
        n = 3
    return " ".join(words[n:])

_LEADING_MARKER = re.compile(rf"\s*(?:{VIEWS}|{ASJ}|(?:Comment|Answer|Edited|Reply)\b\s+(?:Comment|Answer|View|as Justin))")

def build_name_set(posts):
    """Collect poster names from deterministic artifact contexts across the dataset."""
    names = set()
    pat = re.compile(rf"({NAME})\s+(?:{BADGE}|posted to|replied\b|{FEEL}|{ISWITH})")
    pat2 = re.compile(rf"(?:Answer|Comment) as Justin\s+({NAME})")
    def texts():
        for p in posts:
            if isinstance(p.get('body'), str): yield p['body']
            for c in (p.get('comments') or []):
                if isinstance(c, str): yield c
            if isinstance(p.get('author'), str) and p['author'].strip():
                names.add(p['author'].strip())
    for t in texts():
        for m in pat.finditer(t): names.add(m.group(1).strip())
        for m in pat2.finditer(t): names.add(m.group(1).strip())
    return {n for n in names if 1 <= len(n.split()) <= 4}

def clean_artifacts(text, name_set=frozenset()):
    if not isinstance(text, str) or not text:
        return text
    raw = text
    for pat, repl in GLOBALS:
        text = pat.sub(repl, text)
    text = text.strip()
    changed = True
    marker_seen = bool(_LEADING_MARKER.match(raw))
    NAME_MARKERS = LEAD[:3] + [LEAD[9]]
    while changed:
        changed = False
        m = BADGE_CUT.match(text)
        if m:
            text, changed, marker_seen = text[m.end():].lstrip(), True, True
            continue
        for pat in LEAD:
            new = pat.sub("", text, count=1)
            if new != text:
                if pat in NAME_MARKERS:
                    marker_seen = True
                text, changed = new.lstrip(), True
                break
        if not changed and name_set:
            words = text.split()
            for n in (4, 3, 2, 1):
                if len(words) > n and " ".join(words[:n]) in name_set:
                    text, changed = " ".join(words[n:]), True
                    break
        if not changed and marker_seen:
            new = _strip_post_marker_name(text)
            if new != text:
                text, changed, marker_seen = new, True, False
    return re.sub(r"  +", " ", text).strip()

UI_ONLY = re.compile(r"^(?:Comment|Answer|Reply|Edited|View|Follow)$", re.I)

def is_junk_comment(text):
    if not isinstance(text, str):
        return True
    if UI_ONLY.match(text.strip()):
        return True
    return len(re.sub(r"[^A-Za-z0-9]", "", text)) < 2

def clean_post_artifacts(post, name_set):
    """Clean artifact junk from a post's text fields; drop junk/duplicate comments."""
    if isinstance(post.get('body'), str):
        post['body'] = clean_artifacts(post['body'], name_set)
    if isinstance(post.get('comments'), list):
        kept, seen = [], set()
        for c in post['comments']:
            if isinstance(c, str):
                c = clean_artifacts(c, name_set)
                if is_junk_comment(c):
                    continue
                key = c.strip().lower()
                if key in seen:
                    continue
                seen.add(key)
            kept.append(c)
        post['comments'] = kept
    return post
