#!/usr/bin/env python3
"""Build the complete static archive; no API calls or model dependencies."""
import json
from pathlib import Path
from site_builder import build_site
from site_config import NICHE_MAP, build_name_set, clean_post_artifacts

SOURCE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SOURCE_DIR / "site"

def main():
    posts = json.loads((SOURCE_DIR / "posts.json").read_text(encoding="utf-8"))
    from site_config import normalize_posts_metadata, slugify
    posts = normalize_posts_metadata(posts)
    old_aliases = {str(p['id']): ['/'+key+'/'+slugify(p.get('body',''),p['id'])+'/'
        for key in NICHE_MAP if (SOURCE_DIR/key/slugify(p.get('body',''),p['id'])/'index.html').exists()]
        for p in posts}
    names = build_name_set(posts)
    posts = [clean_post_artifacts(p, names) for p in posts]
    legacy = {}
    for post in posts:
        conditions = post.get("conditions_mentioned", "").lower()
        legacy[str(post["id"])] = ["/"+key+"/"+slugify(post.get("body", ""), post["id"])+"/"
            for key, data in NICHE_MAP.items() if any(word.lower() in conditions for word in data["keywords"])]
        legacy[str(post['id'])].extend(old_aliases[str(post['id'])])
    return build_site(site="fixfeetfast", source_dir=SOURCE_DIR, output_dir=OUTPUT_DIR,
                      posts=posts, taxonomy=NICHE_MAP, legacy_routes=legacy)

if __name__ == "__main__":
    main()
