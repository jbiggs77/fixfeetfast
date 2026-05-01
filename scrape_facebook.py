#!/usr/bin/env python3
"""
FixFeetFast.com — Playwright-based Facebook Group Scraper

Scrapes 10 foot health Facebook groups for patient discussion posts.
Uses Playwright (headless Chromium) instead of the Chrome MCP extension.

Usage:
    python3 scrape_facebook.py --terms "bunion,plantar fasciitis" [--max-posts 50] [--output new_posts.json]
    python3 scrape_facebook.py --save-auth   # Interactive: log in to Facebook and save cookies
    python3 scrape_facebook.py --backfill --posts-json posts.json --ids "100,200,300"

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import json
import os
import re
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ─── CONFIGURATION ───────────────────────────────────────────────────────────

# All 10 foot health Facebook groups
GROUPS = {
    "879667705436344": "Bunion Surgery / Foot Surgery Support",
    "88983293238": "Bunion Support Group",
    "2215735725397834": "Minimally Invasive Bunion Surgery",
    "589872944541186": "Plantar Fasciitis Talk and Tips",
    "ToenailFungus": "Toenail Fungus Support & Management",
    "187675031565510": "Forefoot Forum",
    "plantarfasciitissupport": "Plantar Fasciitis Support Group",
    "flatfeethelp": "Flat Feet / Fallen Arches Support",
    "footpainsupport": "Foot Pain Support Group",
    "595328721213805": "Foot Pain Community",
}

# Default groups to search per term (rotate through all groups)
DEFAULT_GROUPS_PER_TERM = 3

AUTH_STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fb_auth_state.json")

# ─── METADATA DETECTION ─────────────────────────────────────────────────────

KNOWN_CONDITIONS = [
    "bunion", "hammer toe", "hammertoe", "hallux valgus", "hallux limitus",
    "hallux rigidus", "tailor's bunion", "bunionette", "plantar fasciitis",
    "heel spur", "flat feet", "fallen arches", "toenail fungus", "fungal nail",
    "ingrown toenail", "metatarsalgia", "neuroma", "morton's neuroma",
    "sesamoiditis", "gout", "arthritis", "bone spur", "callus", "corn",
    "blister", "neuropathy", "edema", "tendonitis", "plantar plate tear",
    "achilles", "tarsal tunnel", "capsulitis", "bursitis", "stress fracture",
    "overpronation", "diabetic foot",
]

KNOWN_SURGERY_TYPES = [
    "MIS", "minimally invasive", "Lapiplasty", "scarf akin", "osteotomy",
    "chevron", "Austin", "arthroplasty", "arthrodesis", "bunionectomy",
    "toe fusion", "MICA", "percutaneous", "cheilectomy", "revision surgery",
    "hardware removal", "screw removal", "plate removal",
]

KNOWN_PRODUCTS = [
    "Hoka", "Orthofeet", "New Balance", "Skechers", "Brooks", "Nike", "Asics",
    "Birkenstock", "Vionic", "Oofos", "Crocs", "Correct Toes", "Yoga Toes",
    "Mind Bodhi", "Dr. Scholl's", "Superfeet", "Powerstep", "KT Tape",
    "Voltaren", "Biofreeze", "Theragun", "ERGOfoot", "Betadine", "Vicks",
    "Lamisil", "Jublia", "Kerasal", "FungiNail", "Altra", "Kuru",
    "Xero Shoes", "Vivobarefoot", "Lems", "Topo Athletic", "Dansko",
    "Alegria", "Penlac",
]

KNOWN_TREATMENTS = [
    "surgery", "physical therapy", "cortisone", "steroid injection", "orthotics",
    "taping", "icing", "elevation", "stretching", "massage", "acupuncture",
    "shockwave therapy", "laser therapy", "MLS laser", "anti-inflammatory",
    "ibuprofen", "gabapentin", "custom orthotics", "terbinafine", "tea tree oil",
    "night splint", "rolling", "arch support", "dry needling", "PRP",
    "TENS unit", "ESWT", "cryotherapy", "cupping", "graston",
    "epsom salt", "apple cider vinegar",
]


def detect_metadata(text):
    """Detect conditions, surgery types, products, and treatments in text."""
    if not text:
        return {}, {}, {}, {}

    text_lower = text.lower()

    conditions = []
    for c in KNOWN_CONDITIONS:
        if c.lower() in text_lower:
            conditions.append(c)

    surgery_types = []
    for s in KNOWN_SURGERY_TYPES:
        pattern = r'\b' + re.escape(s) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            surgery_types.append(s)

    products = []
    for p in KNOWN_PRODUCTS:
        pattern = r'\b' + re.escape(p) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            products.append(p)

    treatments = []
    for t in KNOWN_TREATMENTS:
        if t.lower() in text_lower:
            treatments.append(t)

    return (
        list(set(conditions)),
        list(set(surgery_types)),
        list(set(products)),
        list(set(treatments)),
    )


# ─── UTILITY FUNCTIONS ───────────────────────────────────────────────────────

def human_delay(min_s=1.5, max_s=3.5):
    """Random delay to mimic human browsing."""
    time.sleep(random.uniform(min_s, max_s))


def short_delay(min_s=0.5, max_s=1.5):
    """Shorter delay for within-page actions."""
    time.sleep(random.uniform(min_s, max_s))


def log(msg):
    """Print timestamped log message."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ─── AUTH MANAGEMENT ─────────────────────────────────────────────────────────

def save_auth_state():
    """Launch browser for manual Facebook login, then save auth state."""
    log("Launching browser for Facebook login...")
    log("Please log in to Facebook manually. The script will save your session.")
    log("TIP: After logging in, navigate to any Facebook page to confirm you're logged in.")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, channel="chrome")
            log("Using system Google Chrome.")
        except Exception:
            browser = p.chromium.launch(headless=False)
            log("Using bundled Chromium.")

        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.goto("https://www.facebook.com/login")

        log("Waiting for you to log in... (press Enter in terminal when done)")
        input(">>> Press Enter after logging in to Facebook...")

        context.storage_state(path=AUTH_STATE_FILE)
        log(f"Auth state saved to {AUTH_STATE_FILE}")
        browser.close()


def check_auth():
    """Verify auth state file exists and is recent enough."""
    if not os.path.exists(AUTH_STATE_FILE):
        log("ERROR: No auth state found. Run with --save-auth first.")
        return False
    age_days = (time.time() - os.path.getmtime(AUTH_STATE_FILE)) / 86400
    if age_days > 7:
        log(f"WARNING: Auth state is {age_days:.0f} days old. May need refresh.")
    return True


# ─── SCRAPING ENGINE ─────────────────────────────────────────────────────────

class FacebookScraper:
    def __init__(self, auth_state_file=AUTH_STATE_FILE, headless=True):
        self.auth_state_file = auth_state_file
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.seen_body_prefixes = set()

    def start(self):
        """Launch browser with saved auth state."""
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch(headless=self.headless, channel="chrome")
        except Exception:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            storage_state=self.auth_state_file,
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        self.page = self.context.new_page()
        self.page.route("**/*.{png,jpg,jpeg,gif,webp,mp4,webm}", lambda route: route.abort())
        log("Browser launched with saved auth state.")

    def stop(self):
        """Clean up browser."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        log("Browser closed.")

    def verify_login(self):
        """Check that we're actually logged in to Facebook."""
        first_group = list(GROUPS.keys())[0]
        self.page.goto(f"https://www.facebook.com/groups/{first_group}", wait_until="domcontentloaded")
        human_delay(2, 4)
        if "/login" in self.page.url:
            log("ERROR: Not logged in. Auth state may be expired.")
            log("Run: python3 scrape_facebook.py --save-auth")
            return False
        log("Login verified — Facebook group accessible.")
        return True

    def search_group(self, group_id, term, max_posts_per_term=8):
        """Search a specific group for a term and extract posts."""
        search_url = f"https://www.facebook.com/groups/{group_id}/search/?q={term.replace(' ', '%20')}"
        group_name = GROUPS.get(group_id, group_id)
        log(f"  Searching '{group_name}' for '{term}'")

        try:
            self.page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        except PWTimeout:
            log(f"    Timeout loading search, skipping.")
            return []

        # Handle sensitive content warning
        try:
            show_results = self.page.get_by_text("Show search results", exact=False)
            if show_results.count() > 0:
                show_results.first.click(timeout=3000)
                human_delay(1, 2)
        except Exception:
            pass

        human_delay(2, 4)

        posts_this_search = []
        scroll_attempts = 0
        max_scrolls = 5

        while scroll_attempts < max_scrolls:
            new_posts = self._extract_search_results()
            for post in new_posts:
                body_prefix = (post.get("body", "") or "")[:80].lower().strip()
                if body_prefix and body_prefix not in self.seen_body_prefixes:
                    self.seen_body_prefixes.add(body_prefix)
                    post["source_group"] = group_name
                    posts_this_search.append(post)

            if len(posts_this_search) >= max_posts_per_term:
                break

            self.page.evaluate("window.scrollBy(0, 1500)")
            short_delay(1, 2)
            scroll_attempts += 1

        log(f"    Found {len(posts_this_search)} unique posts")

        # Click into each post to capture comments
        posts_with_comments = []
        for i, post in enumerate(posts_this_search):
            if i >= max_posts_per_term:
                break
            enriched = self._capture_post_comments(post, term)
            posts_with_comments.append(enriched)
            human_delay(1.5, 3)

        return posts_with_comments

    def search_term(self, term, group_ids=None, max_posts_per_term=8):
        """Search multiple groups for a term."""
        if group_ids is None:
            # Pick a subset of groups to search
            all_ids = list(GROUPS.keys())
            random.shuffle(all_ids)
            group_ids = all_ids[:DEFAULT_GROUPS_PER_TERM]

        log(f"Searching: '{term}' across {len(group_ids)} groups")
        all_posts = []

        for gid in group_ids:
            remaining = max_posts_per_term - len(all_posts)
            if remaining <= 0:
                break
            posts = self.search_group(gid, term, max_posts_per_term=remaining)
            all_posts.extend(posts)
            human_delay(2, 4)

        return all_posts

    def _extract_search_results(self):
        """Parse search results from the full page text."""
        posts = []
        try:
            page_text = self.page.inner_text('body', timeout=10000)
            blocks = re.split(r'\nLike\nComment\nSend\n', page_text)

            for block in blocks:
                post_body = self._extract_body_from_block(block)
                if post_body and len(post_body) >= 20:
                    comment_count_match = re.search(r'(\d+)\s+comments?', block, re.IGNORECASE)
                    comment_hint = int(comment_count_match.group(1)) if comment_count_match else 0

                    posts.append({
                        "body": post_body,
                        "comments": [],
                        "comment_count_hint": comment_hint,
                        "search_term_used": "",
                    })

        except Exception as e:
            log(f"    Error extracting search results: {e}")

        return posts

    def _extract_body_from_block(self, block):
        """Extract the post body text from a raw text block."""
        lines = block.split('\n')
        body_lines = []
        found_separator = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # The '·' separates metadata from post body — check BEFORE single-char filter
            if '·' in line and len(line) <= 3:
                found_separator = True
                continue

            if line == "Facebook":
                continue

            if len(line) <= 2 and not line.isdigit():
                continue

            if line in ("Like", "Comment", "Share", "Send", "Reply",
                        "Most relevant", "Newest first", "All comments",
                        "Write a comment…", "Write a comment",
                        "Hide", "Report", "Search Results",
                        "Filters", "Recent Posts", "Posts You've Seen",
                        "Date Posted", "Show search results"):
                continue

            if re.match(r'^(All reactions?:?\s*)?\d+$', line):
                continue
            if re.match(r'^\d+\s+(comments?|likes?|shares?|reactions?)$', line, re.IGNORECASE):
                continue

            if found_separator and len(line) > 3:
                body_lines.append(line)

        return '\n'.join(body_lines).strip()

    def _capture_post_comments(self, post, search_term):
        """Click into a post to capture its comments."""
        post["search_term_used"] = search_term
        body_text = post.get("body", "")
        comment_hint = post.pop("comment_count_hint", 0)

        if comment_hint == 0:
            log(f"      Skipping comment capture (0 comments): {body_text[:50]}...")
            return post

        try:
            navigated = self._navigate_to_post(body_text)

            if navigated:
                self._expand_comments()
                comments = self._extract_comments_from_page()
                post["comments"] = comments

                # Re-extract full post body from individual post page
                try:
                    page_text = self.page.inner_text('body', timeout=10000)
                    blocks = re.split(r'\nLike\nComment\nSend\n', page_text)
                    if blocks:
                        better_body = self._extract_body_from_block(blocks[0])
                        if better_body and len(better_body) > len(body_text):
                            post["body"] = better_body
                except Exception:
                    pass

                self.page.go_back(wait_until="domcontentloaded", timeout=15000)
                human_delay(1, 2)

        except Exception as e:
            log(f"      Error capturing comments: {e}")

        # Auto-detect metadata from body + comments
        all_text = post.get("body", "")
        for c in post.get("comments", []):
            if isinstance(c, str):
                all_text += " " + c
            elif isinstance(c, dict):
                all_text += " " + c.get("comment_text", "")

        conditions, surgery_types, products, treatments = detect_metadata(all_text)
        post["conditions_mentioned"] = ", ".join(conditions)
        post["surgery_types_mentioned"] = ", ".join(surgery_types)
        post["products_mentioned"] = ", ".join(products)
        post["treatments_mentioned"] = ", ".join(treatments)

        return post

    def _expand_comments(self):
        """Click 'View more comments' and 'See more replies' buttons."""
        max_expansions = 10
        expanded = 0

        for _ in range(max_expansions):
            try:
                buttons = self.page.query_selector_all('div[role="button"]')
                clicked_any = False

                for btn in buttons:
                    try:
                        text = btn.inner_text(timeout=2000)
                        if any(phrase in text.lower() for phrase in [
                            "view more comment", "see more comment",
                            "view more replies", "see more replies",
                            "previous comments", "see all", "view all",
                        ]):
                            btn.click(timeout=3000)
                            short_delay(1, 2)
                            clicked_any = True
                            expanded += 1
                            break
                    except Exception:
                        continue

                see_more = self.page.query_selector_all('div[role="button"]:has-text("See more")')
                for sm in see_more[:5]:
                    try:
                        sm.click(timeout=2000)
                        short_delay(0.3, 0.5)
                    except Exception:
                        continue

                if not clicked_any:
                    break
            except Exception:
                break

        if expanded > 0:
            log(f"      Expanded {expanded} comment sections")

    def _navigate_to_post(self, body_text):
        """Navigate to an individual post by finding its link on the search page."""
        search_snippet = body_text[:50]

        try:
            JS_FIND_LINK = """
            (snippet) => {
                snippet = snippet.toLowerCase();
                const allLinks = document.querySelectorAll('a[href]');

                for (const link of allLinks) {
                    const href = link.href || '';
                    if (!href.includes('facebook.com') || href.includes('/search/') || href.includes('#')) continue;
                    if (!href.includes('/groups/') && !href.includes('/posts/') && !href.includes('/permalink/')) continue;

                    let el = link;
                    for (let i = 0; i < 12; i++) {
                        el = el.parentElement;
                        if (!el) break;
                        const text = (el.innerText || '').toLowerCase();
                        if (text.length > 30 && text.includes(snippet)) {
                            return link.href;
                        }
                    }
                }

                for (const link of allLinks) {
                    const href = link.href || '';
                    if (!href.includes('facebook.com')) continue;
                    if (href.includes('/search/') || href.includes('#') || href.includes('/?')) continue;

                    let el = link;
                    for (let i = 0; i < 8; i++) {
                        el = el.parentElement;
                        if (!el) break;
                        const text = (el.innerText || '').toLowerCase();
                        if (text.length > 30 && text.includes(snippet)) {
                            return link.href;
                        }
                    }
                }

                return null;
            }
            """
            result = self.page.evaluate(JS_FIND_LINK, search_snippet)

            if result:
                log(f"      Found link for post, navigating...")
                self.page.goto(result, wait_until="domcontentloaded", timeout=20000)
                human_delay(2, 3)
                return True

            # Strategy 3: Click on the post text directly
            try:
                first_line = body_text.split('\n')[0][:60]
                if len(first_line) > 20:
                    el = self.page.get_by_text(first_line, exact=False).first
                    if el:
                        el.click(timeout=5000)
                        human_delay(2, 3)
                        if "/posts/" in self.page.url or "/permalink/" in self.page.url:
                            log(f"      Clicked post text, navigated to post page")
                            return True
                        page_text = self.page.inner_text('body', timeout=5000)
                        if "Like\nReply" in page_text:
                            log(f"      Clicked post text, comments visible in overlay")
                            return True
            except Exception:
                pass

            log(f"      Could not find link or clickable element for post")
            return False

        except Exception as e:
            log(f"      Error navigating to post: {e}")
            return False

    def _extract_comments_from_page(self):
        """Extract comments from an individual post's page.

        NOTE: For FixFeetFast, comments are plain strings (not dicts).
        """
        comments = []
        try:
            page_text = self.page.inner_text('body', timeout=10000)

            parts = page_text.split("Like\nComment\nSend\n", 1)
            if len(parts) < 2:
                return []

            comments_section = parts[1]
            comment_blocks = re.split(r'\nLike\n(?:Reply\n)?', comments_section)

            for block in comment_blocks:
                lines = block.split('\n')
                content_lines = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if len(line) <= 2 and not line.isdigit():
                        continue
                    if line == "Facebook":
                        continue
                    if re.match(r'^\d+[hdwmy]$', line):
                        continue
                    if re.match(r'^(Just now|Yesterday|\d+\s*minutes?\s*ago)$', line, re.IGNORECASE):
                        continue
                    if line in ("Like", "Reply", "Share", "Send", "Hide",
                                "See more", "View replies", "Write a reply…",
                                "Write a comment…", "Write a comment",
                                "Most relevant", "All comments", "Newest first",
                                "Author", "Top fan", "Edited"):
                        continue
                    if re.match(r'^(All reactions?:?\s*)?\d+$', line):
                        continue
                    if re.match(r'^\d+\s+(comments?|likes?|shares?|reactions?|replies?)$', line, re.IGNORECASE):
                        continue
                    if line == '·':
                        continue

                    if len(line) > 3:
                        content_lines.append(line)

                comment_text = ' '.join(content_lines).strip()

                # Only keep substantive comments (skip one-word replies)
                if len(comment_text) > 15:
                    # For FixFeetFast: comments are plain strings
                    comments.append(comment_text)

        except Exception as e:
            log(f"      Error extracting comments: {e}")

        # Deduplicate
        seen = set()
        unique = []
        for c in comments:
            key = c[:60].lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(c)

        if unique:
            log(f"      Captured {len(unique)} comments")

        return unique

    def backfill_post_comments(self, post_body_snippet, source_group=None):
        """Search for a specific post and capture its comments."""
        search_query = post_body_snippet[:50].replace('"', '').replace("'", "")

        # Search in the source group if known, otherwise try the first few groups
        groups_to_try = []
        if source_group:
            for gid, name in GROUPS.items():
                if name == source_group:
                    groups_to_try.append(gid)
                    break
        if not groups_to_try:
            groups_to_try = list(GROUPS.keys())[:3]

        for gid in groups_to_try:
            search_url = f"https://www.facebook.com/groups/{gid}/search/?q={search_query.replace(' ', '%20')}"
            try:
                self.page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                human_delay(2, 4)

                posts = self._extract_search_results()
                for post in posts:
                    body_prefix = (post.get("body", "") or "")[:60].lower().strip()
                    target_prefix = post_body_snippet[:60].lower().strip()
                    if body_prefix == target_prefix or target_prefix[:40] in body_prefix:
                        enriched = self._capture_post_comments(post, "backfill")
                        return enriched.get("comments", [])

            except Exception as e:
                log(f"  Backfill error in group {gid}: {e}")

        return []


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scrape foot health Facebook groups")
    parser.add_argument("--save-auth", action="store_true",
                        help="Launch visible browser to log in and save cookies")
    parser.add_argument("--terms", type=str, default="",
                        help="Comma-separated search terms")
    parser.add_argument("--groups", type=str, default="",
                        help="Comma-separated group IDs to search (default: rotate through all)")
    parser.add_argument("--max-posts", type=int, default=50,
                        help="Max total new posts to capture")
    parser.add_argument("--max-per-term", type=int, default=8,
                        help="Max posts per search term per group")
    parser.add_argument("--output", type=str, default="new_posts.json",
                        help="Output JSON file for new posts")
    parser.add_argument("--existing", type=str, default="",
                        help="Path to existing posts.json for dedup")
    parser.add_argument("--headless", action="store_true", default=True,
                        help="Run in headless mode (default)")
    parser.add_argument("--no-headless", action="store_true",
                        help="Run with visible browser (for debugging)")
    parser.add_argument("--backfill", action="store_true",
                        help="Backfill comments on existing posts")
    parser.add_argument("--posts-json", type=str, default="",
                        help="Path to posts.json for backfill mode")
    parser.add_argument("--ids", type=str, default="",
                        help="Comma-separated post IDs to backfill")

    args = parser.parse_args()

    if args.save_auth:
        save_auth_state()
        return

    if not check_auth():
        sys.exit(1)

    headless = not args.no_headless

    # Load existing posts for deduplication
    existing_prefixes = set()
    if args.existing and os.path.exists(args.existing):
        with open(args.existing) as f:
            existing = json.load(f)
        for p in existing:
            prefix = (p.get("body", "") or "")[:80].lower().strip()
            if prefix:
                existing_prefixes.add(prefix)
        log(f"Loaded {len(existing)} existing posts for dedup")

    # Parse group IDs if specified
    group_ids = None
    if args.groups:
        group_ids = [g.strip() for g in args.groups.split(",") if g.strip()]

    scraper = FacebookScraper(headless=headless)

    try:
        scraper.start()

        if not scraper.verify_login():
            sys.exit(1)

        if args.backfill:
            if not args.posts_json:
                log("ERROR: --posts-json required for backfill mode")
                sys.exit(1)
            with open(args.posts_json) as f:
                posts = json.load(f)

            ids_to_backfill = [int(x) for x in args.ids.split(",") if x.strip()] if args.ids else []

            if not ids_to_backfill:
                for p in posts:
                    if p.get("id", 0) >= 465 and not p.get("comments"):
                        body = (p.get("body", "") or "").lower()
                        if any(phrase in body for phrase in [
                            "has anyone", "anyone else", "help me", "advice",
                            "is this normal", "how long", "should i",
                            "any recommendations", "what helped",
                        ]):
                            ids_to_backfill.append(p["id"])
                ids_to_backfill = ids_to_backfill[:10]

            log(f"Backfilling comments for {len(ids_to_backfill)} posts")
            backfilled = 0

            for pid in ids_to_backfill:
                post = next((p for p in posts if p["id"] == pid), None)
                if not post:
                    continue
                body = post.get("body", "")
                if not body:
                    continue

                log(f"  Backfilling post {pid}: {body[:50]}...")
                comments = scraper.backfill_post_comments(body, post.get("source_group"))
                if comments:
                    post["comments"] = comments
                    all_text = body + " " + " ".join(comments)
                    conds, surgs, prods, treats = detect_metadata(all_text)
                    post["conditions_mentioned"] = ", ".join(conds)
                    post["surgery_types_mentioned"] = ", ".join(surgs)
                    post["products_mentioned"] = ", ".join(prods)
                    post["treatments_mentioned"] = ", ".join(treats)
                    backfilled += 1
                    log(f"    Added {len(comments)} comments to post {pid}")

                human_delay(2, 4)

            with open(args.posts_json, 'w') as f:
                json.dump(posts, f, indent=2)
            log(f"Backfilled {backfilled}/{len(ids_to_backfill)} posts")

        else:
            # Normal scrape mode
            terms = [t.strip() for t in args.terms.split(",") if t.strip()]
            if not terms:
                log("ERROR: No search terms provided. Use --terms 'bunion,plantar fasciitis'")
                sys.exit(1)

            scraper.seen_body_prefixes = existing_prefixes.copy()
            all_new_posts = []

            for term in terms:
                if len(all_new_posts) >= args.max_posts:
                    log(f"Reached max posts limit ({args.max_posts}), stopping.")
                    break

                posts = scraper.search_term(term, group_ids=group_ids, max_posts_per_term=args.max_per_term)

                for post in posts:
                    prefix = (post.get("body", "") or "")[:80].lower().strip()
                    if prefix not in existing_prefixes:
                        all_new_posts.append(post)
                        existing_prefixes.add(prefix)

                human_delay(2, 5)

            # Format output
            for post in all_new_posts:
                post["author"] = None
                post["url"] = None
                post["date"] = datetime.now().strftime("%Y-%m-%d")
                post["images"] = []
                if "source_group" not in post:
                    post["source_group"] = ""

            # Save results
            with open(args.output, 'w') as f:
                json.dump(all_new_posts, f, indent=2)

            comment_count = sum(len(p.get("comments", [])) for p in all_new_posts)
            posts_with_comments = sum(1 for p in all_new_posts if p.get("comments"))

            log(f"\n{'='*60}")
            log(f"SCRAPE COMPLETE")
            log(f"  New posts captured: {len(all_new_posts)}")
            log(f"  Comments captured: {comment_count}")
            log(f"  Posts with comments: {posts_with_comments}/{len(all_new_posts)}")
            log(f"  Search terms used: {', '.join(terms)}")
            log(f"  Output saved to: {args.output}")
            log(f"{'='*60}")

    finally:
        scraper.stop()


if __name__ == "__main__":
    main()
