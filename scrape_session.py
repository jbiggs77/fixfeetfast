import json

# Load existing posts
with open('/tmp/fixfeetfast2/posts.json') as f:
    existing_posts = json.load(f)

print(f"Loaded {len(existing_posts)} existing posts")

# Track existing post keys for dedup
existing_keys = {}
for p in existing_posts:
    key = p['body'][:80].lower().strip()
    existing_keys[key] = p

# New posts to add
new_posts = []
enriched_count = 0
new_comments_added = 0

def add_post(body, comments, source_group, conditions='', surgery='', treatments='', products=''):
    global enriched_count, new_comments_added
    key = body[:80].lower().strip()
    if key in existing_keys:
        # MERGE
        existing = existing_keys[key]
        merged_any = False
        # Merge comments
        if comments:
            existing_comment_keys = set(c[:50].lower().strip() for c in existing.get('comments', []))
            for c in comments:
                if c[:50].lower().strip() not in existing_comment_keys:
                    existing.setdefault('comments', []).append(c)
                    new_comments_added += 1
                    merged_any = True
        # Merge longer body
        if len(body) > len(existing.get('body', '')):
            existing['body'] = body
            merged_any = True
        # Merge metadata
        for field, val in [('conditions_mentioned', conditions), ('surgery_types_mentioned', surgery), 
                           ('treatments_mentioned', treatments), ('products_mentioned', products)]:
            if val:
                existing_vals = set(v.strip().lower() for v in existing.get(field, '').split(',') if v.strip())
                new_vals = set(v.strip().lower() for v in val.split(',') if v.strip())
                combined = existing_vals | new_vals
                if combined != existing_vals:
                    existing[field] = ', '.join(sorted(combined))
                    merged_any = True
        if merged_any:
            enriched_count += 1
        return 'enriched' if merged_any else 'duplicate'
    else:
        post = {
            'id': None,  # assigned later
            'body': body,
            'comments': comments or [],
            'author': None,
            'url': None,
            'source_group': source_group,
            'images': [],
            'conditions_mentioned': conditions,
            'surgery_types_mentioned': surgery,
            'treatments_mentioned': treatments,
            'products_mentioned': products
        }
        new_posts.append(post)
        existing_keys[key] = post
        return 'new'

def save_all():
    global existing_posts, new_posts
    next_id = max(p['id'] for p in existing_posts) + 1
    for p in new_posts:
        p['id'] = next_id
        next_id += 1
        existing_posts.append(p)
    with open('/tmp/fixfeetfast2/posts.json', 'w') as f:
        json.dump(existing_posts, f, indent=2)
    total_comments = sum(len(p.get('comments', [])) for p in existing_posts)
    posts_with_comments = sum(1 for p in existing_posts if p.get('comments') and len(p['comments']) > 0)
    print(f"Saved {len(existing_posts)} total posts ({len(new_posts)} new, {enriched_count} enriched)")
    print(f"New comments added: {new_comments_added}")
    print(f"Total comments: {total_comments}, Posts with comments: {posts_with_comments}")

print("Scrape session initialized. Use add_post() and save_all()")
