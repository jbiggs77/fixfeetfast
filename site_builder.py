"""Shared static presentation for the two community archives.

The site-specific generate_site.py keeps its taxonomy and legacy cleanup. This
module owns stable routes, truthful metadata, crawlable navigation and rendering.
It requires only Python's standard library; no model calls occur during builds.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit


PAGE_SIZE = 30
EMPTY_TAGS = {"none", "n/a", "unknown", "null", "not specified", "other"}


def text(value):
    return str(value or "").strip()


def short(value, limit=160):
    value = re.sub(r"\s+", " ", text(value))
    if len(value) <= limit:
        return value
    return value[:limit - 1].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def tokens(value):
    if isinstance(value, list):
        values = [part for item in value for part in tokens(item)]
    else:
        values = [p.strip() for p in str(value or "").split(",")]
    seen, result = set(), []
    for value in values:
        key = value.casefold()
        if key and key not in EMPTY_TAGS and key not in seen:
            seen.add(key); result.append(value)
    return result


def slug(value):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text(value).lower())).strip("-")


def safe_url(value):
    try:
        parsed = urlsplit(value or "")
        if parsed.scheme in {"https", "http"} and parsed.hostname and not parsed.username and not parsed.password:
            return value
    except (TypeError, ValueError):
        pass
    return ""


def json_script(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def valid_date(value):
    try:
        value = text(value)
        if not re.match(r"^\d{4}-\d{2}-\d{2}(?:$|T| )", value):
            return None
        result = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        if result > datetime.now(timezone.utc).date() or result.year < 2004:
            return None
        return result.isoformat()
    except ValueError:
        return None


def archive_date(post):
    for field in ("date_captured", "date", "date_posted"):
        if valid_date(post.get(field)):
            return valid_date(post[field])
    return None


def comments(post):
    result = []
    def walk(items, parent=None):
        for index, raw in enumerate(items or []):
            value = dict(raw) if isinstance(raw, dict) else {"comment_text": str(raw)}
            if parent and not value.get("parent_comment_id"):
                value["parent_comment_id"] = parent
            if text(value.get("comment_text")) or value.get("images") or value.get("attachments"):
                result.append(value)
            if isinstance(value.get("replies"), list):
                walk(value["replies"], value.get("comment_id"))
    walk(post.get("comments"))
    return result


def title_for(post):
    proposed = text(post.get("title"))
    if len(proposed) < 12 or proposed.lower() in {"discussion", "question", "none"}:
        proposed = text(post.get("body"))
        sentences = re.split(r"(?<=[?.!])\s+", proposed)
        if sentences and 18 <= len(sentences[0]) <= 130:
            proposed = sentences[0]
    return short(proposed, 112) or f"Community discussion {post['id']}"


class InlineHTML(HTMLParser):
    """Preserve modest editorial formatting, never arbitrary supplied markup."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts = []; self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag in {"strong", "em", "b", "i", "code", "br"}:
            self.parts.append("<" + tag + ">")
        elif tag == "a":
            url = safe_url(dict(attrs).get("href"))
            self.parts.append(f'<a href="{escape(url, quote=True)}" rel="noopener noreferrer">' if url else "<span>")
            self.stack.append("a" if url else "span")
    def handle_endtag(self, tag):
        if tag in {"strong", "em", "b", "i", "code"}:
            self.parts.append("</" + tag + ">")
        elif tag == "a" and self.stack:
            self.parts.append("</" + self.stack.pop() + ">")
    def handle_data(self, value):
        self.parts.append(escape(value))


def rich(value):
    parser = InlineHTML(); parser.feed(text(value)); parser.close()
    return "".join(parser.parts)


class ArchiveSite:
    def __init__(self, site, source_dir, output_dir, posts, taxonomy,
                 classify=None, preferred_routes=None, legacy_routes=None):
        self.site = site
        self.fff = site == "fixfeetfast"
        self.name = "FixFeetFast" if self.fff else "WhereToPlace"
        self.origin = f"https://{site}.com"
        self.source = Path(source_dir); self.output = Path(output_dir)
        self.source_post_count = len(posts)
        self.excluded_ids = {str(p["id"]) for p in posts if isinstance(p.get("publication"), dict)
                             and p["publication"].get("status") == "excluded"}
        self.posts = [deepcopy(p) for p in posts if str(p["id"]) not in self.excluded_ids and
                      (text(p.get("body")) or p.get("comments") or p.get("images") or p.get("attachments"))]
        if len({str(p.get("id")) for p in posts}) != len(posts):
            raise ValueError("Duplicate site IDs must be resolved before building stable routes")
        self.taxonomy = deepcopy(taxonomy)
        self.taxonomy.setdefault("general-foot-health" if self.fff else "general-insurance-discussions", {
            "title": "More foot health experiences" if self.fff else "General insurance discussions",
            "name": "General insurance discussions", "keywords": []})
        self.groups = defaultdict(list); self.post_groups = {}; self.comment_map = {}
        self.tag_fields = ("conditions_mentioned", "surgery_types_mentioned", "products_mentioned", "treatments_mentioned") if self.fff else (
            "carriers_mentioned", "states_mentioned", "risk_types")
        self.term_patterns = {key: [re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)", re.I)
                                   for word in data.get("keywords", []) if len(word) > 2]
                              for key, data in taxonomy.items()}
        for post in self.posts:
            identifier = str(post["id"])
            if classify:
                matched = [s for s in classify(post) if s in self.taxonomy]
            else:
                haystack = " ".join([text(post.get("body")), *[", ".join(tokens(post.get(f))) for f in self.tag_fields]])
                matched = [key for key, patterns in self.term_patterns.items() if any(pattern.search(haystack) for pattern in patterns)]
                matched.extend(s for s in tokens(post.get("niches")) if s in self.taxonomy and s not in matched)
            # Classifiers may return a set in process-dependent order. Keep
            # breadcrumbs, related links and search data stable across rebuilds.
            matched = [key for key in self.taxonomy if key in set(matched)] or ["general-foot-health" if self.fff else "general-insurance-discussions"]
            self.post_groups[identifier] = matched
            self.comment_map[identifier] = comments(post)
            for key in matched:
                self.groups[key].append(post)
        self.groups = dict(self.groups)
        self.posts.sort(key=lambda p: (archive_date(p) or "", int(p["id"]) if str(p["id"]).isdigit() else 0), reverse=True)
        self.order = {str(p["id"]): i for i, p in enumerate(self.posts)}
        for group in self.groups.values():
            group.sort(key=lambda p: self.order[str(p["id"])])
        self.routes = {}; self.aliases = {}; self.pages = {}; self.indexable = set()
        self.archive_bases = set()
        registry = self.load_json(self.source / "site-routes.json", {})
        prior = self.prepare_retired_routes(registry, preferred_routes or {}, legacy_routes or {})
        self.old_history = self.load_json(self.source / "site-history.json", {}).get("pages", {})
        self.assign_routes(prior, preferred_routes or {}, legacy_routes or {})
        for route, identifier in {**registry.get("aliases", {}), **self.retired_aliases}.items():
            if self.valid_route(route) and str(identifier) in self.routes and route not in self.routes.values():
                self.aliases.setdefault(route, str(identifier))
        self.retired_posts = {identifier: route for identifier, route in self.retired_posts.items()
                              if identifier not in self.routes}
        self.retired_aliases = {route: identifier for route, identifier in self.retired_aliases.items()
                                if identifier not in self.routes and route not in self.retired_posts.values()}
        self.retired_routes = {**self.retired_aliases,
                               **{route: identifier for identifier, route in self.retired_posts.items()}}
        if not self.fff:
            # Earlier WTP rebuilds changed title-based slugs. The original URL
            # embeds the immutable record ID, so its destination is unambiguous.
            for old_page in (self.source / "discussions").glob("*/index.html"):
                match = re.search(r"-(\d+)$", old_page.parent.name)
                route = "/discussions/" + old_page.parent.name + "/"
                if match and match[1] in self.routes and route not in self.routes.values() and self.valid_route(route):
                    self.aliases.setdefault(route, match[1])
        self.guides_data = self.load_json(self.source / "guides.json", {}) if not self.fff else {}
        self.assets = {}; self.search_asset = None
        self.today = datetime.now(timezone.utc).date().isoformat()
        self.link_terms = []
        for key, data in taxonomy.items():
            if key not in self.groups:
                continue
            for word in data.get("keywords", []):
                if len(word) >= 5:
                    self.link_terms.append((word, "/" + key + "/"))
        self.link_terms.sort(key=lambda pair: -len(pair[0]))
        self.link_lookup = {word.casefold(): route for word, route in self.link_terms}
        self.link_pattern = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(w) for w, _ in self.link_terms) + r")(?!\w)", re.I) if self.link_terms else None

    @staticmethod
    def load_json(path, fallback):
        if not path.exists():
            return fallback
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def valid_route(value):
        return isinstance(value, str) and bool(re.fullmatch(r"/(?:[^\W_][\w-]*/)+", value))

    def prepare_retired_routes(self, registry, preferred, legacy):
        # Keep removed route ownership without retaining advertising content.
        # A missing record alone is not an exclusion decision.
        self.retired_posts = {str(identifier): route for identifier, route in registry.get("retired_posts", {}).items()
                              if self.valid_route(route)}
        self.retired_aliases = {route: str(identifier) for route, identifier in registry.get("retired_aliases", {}).items()
                                if self.valid_route(route)}
        prior = {**self.retired_posts, **{str(identifier): route for identifier, route in registry.get("posts", {}).items()}}
        canonical_owners = {route: identifier for identifier, route in prior.items() if self.valid_route(route)}
        for identifier in self.excluded_ids:
            choices = [prior.get(identifier), preferred.get(identifier), *legacy.get(identifier, [])]
            canonical = next((route for route in choices if self.valid_route(route)
                              and canonical_owners.get(route, identifier) == identifier), None)
            if canonical:
                self.retired_posts[identifier] = canonical
                prior[identifier] = canonical
                canonical_owners[canonical] = identifier
        candidates = dict(registry.get("aliases", {}))
        for identifier in self.excluded_ids:
            for route in [preferred.get(identifier), *legacy.get(identifier, [])]:
                if self.valid_route(route):
                    candidates.setdefault(route, identifier)
        for route, identifier in candidates.items():
            identifier = str(identifier)
            if (identifier in self.excluded_ids and self.valid_route(route)
                    and canonical_owners.get(route, identifier) == identifier):
                self.retired_aliases[route] = identifier
        self.retired_routes = {**self.retired_aliases,
                               **{route: identifier for identifier, route in self.retired_posts.items()}}
        return prior

    def assign_routes(self, prior, preferred, legacy):
        owners = {}
        for post in self.posts[::-1]:
            for route in legacy.get(str(post["id"]), []):
                if self.valid_route(route):
                    owners[route] = str(post["id"])
        # A legacy alias that was overwritten belonged to the last original
        # record, not whichever record happens to sort first today.
        for identifier, aliases in legacy.items():
            for route in aliases:
                if self.valid_route(route):
                    owners[route] = str(identifier)
        reserved = {route: str(identifier) for identifier, route in prior.items() if self.valid_route(route)}
        if len(reserved) != sum(self.valid_route(route) for route in prior.values()):
            raise ValueError("Duplicate persisted canonical routes")
        for route, identifier in self.retired_routes.items():
            if route in reserved and reserved[route] != identifier:
                raise ValueError("Retired route belongs to another record")
            reserved[route] = identifier
        used = set()
        for post in sorted(self.posts, key=lambda p: str(p["id"])):
            identifier = str(post["id"])
            choices = [prior.get(identifier), preferred.get(identifier)]
            choices.extend(r for r in legacy.get(identifier, []) if owners.get(r) == identifier)
            route = next((r for r in choices if self.valid_route(r) and r not in used
                          and reserved.get(r, identifier) == identifier), None)
            if not route:
                stem = slug(short(title_for(post), 65)) or "community-question"
                route = f"/discussions/{stem}-{slug(identifier)}/"
            if route in used or reserved.get(route, identifier) != identifier:
                raise ValueError("Canonical route collision: " + route)
            self.routes[identifier] = route; used.add(route)
        for alias, identifier in owners.items():
            if (identifier in self.routes and alias != self.routes[identifier] and alias not in used
                    and reserved.get(alias, identifier) == identifier):
                self.aliases[alias] = identifier
        # Preserve old WTP slug URLs if titles changed after the registry exists.
        for identifier, alias in preferred.items():
            if (self.valid_route(alias) and alias not in used and identifier in self.routes
                    and reserved.get(alias, identifier) == identifier):
                self.aliases[alias] = identifier

    def topic_name(self, key):
        data = self.taxonomy[key]
        return data.get("title" if self.fff else "name") or data.get("title") or key.replace("-", " ").title()

    def link_text(self, value, current=""):
        value = text(value); out = []; start = 0; used = set()
        for match in self.link_pattern.finditer(value) if self.link_pattern else []:
            route = self.link_lookup.get(match.group().casefold())
            if not route or route == current or route in used or len(used) >= 4:
                continue
            out.extend((escape(value[start:match.start()]), f'<a href="{route}">{escape(match.group())}</a>'))
            used.add(route); start = match.end()
        out.append(escape(value[start:])); return "".join(out)

    def source_url(self, post):
        return safe_url(post.get("source_url") or post.get("url"))

    def brand(self):
        mark = "F" if self.fff else "W"
        return f'<a class="brand" href="/" aria-label="{self.name} home"><span class="brand-mark" aria-hidden="true">{mark}</span>{self.name}<small>.</small></a>'

    def nav(self):
        items = [("/discussions/", "Discussions"), ("/#topics", "Topics" if self.fff else "Risk classes")]
        if not self.fff:
            items.append(("/hard-to-place-insurance/", "Market guides"))
        items.append(("/about/", "About"))
        links = "".join(f'<a href="{url}">{label}</a>' for url, label in items)
        return f'<header class="site-header"><div class="wrap header-inner">{self.brand()}<nav class="site-nav" aria-label="Main navigation">{links}</nav><details class="mobile-nav"><summary>Menu</summary><nav class="mobile-links" aria-label="Mobile navigation">{links}</nav></details></div></header>'

    def footer(self):
        role = ("Personal experiences about foot conditions, surgery and recovery. Community discussions are not medical advice."
                if self.fff else "Insurance market research informed by community discussions. A carrier mention is a research lead, not confirmation of underwriting appetite or coverage.")
        popular = sorted(self.groups, key=lambda k: -len(self.groups[k]))[:4]
        links = "".join(f'<a href="/{key}/">{escape(self.topic_name(key))}</a>' for key in popular)
        return f'<footer class="site-footer"><div class="wrap"><div class="footer-grid"><div>{self.brand()}<p>{role}</p></div><div><h2>Explore the archive</h2><div class="footer-links">{links}</div></div><div><h2>About this resource</h2><div class="footer-links"><a href="/about/">How the archive works</a><a href="/about/#sources">Sources &amp; limitations</a><a href="/discussions/">All discussions</a><a href="/sitemap.xml">Sitemap</a></div></div></div><div class="footer-bottom"><span>© {self.name}</span><span>Community perspectives. Original context matters.</span></div></div></footer>'

    def breadcrumbs(self, items):
        items = [("Home", "/"), *items]
        visible = '<nav aria-label="Breadcrumb"><ol class="breadcrumb">' + "".join(
            f'<li><a href="{escape(url, quote=True)}">{escape(short(name, 65))}</a></li>' if i < len(items)-1
            else f'<li aria-current="page">{escape(short(name, 65))}</li>' for i, (name, url) in enumerate(items)) + '</ol></nav>'
        schema = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": name, "item": self.origin+url} for i, (name, url) in enumerate(items)]}
        return visible, schema

    def write_page(self, route, title, description, body, *, kind="WebPage", extra=None,
                   canonical=None, index=True, citations=None):
        canonical = canonical or route
        signature = sha256(json.dumps([title, description, body, canonical, kind, extra, citations,
                                       self.assets], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        old = self.old_history.get(route, {})
        modified = old.get("modified") if old.get("hash") == signature and valid_date(old.get("modified")) else self.today
        self.pages[route] = {"hash": signature, "modified": modified}
        if index and canonical == route:
            self.indexable.add(route)
        page = {"@type": kind, "@id": self.origin+canonical+"#webpage", "url": self.origin+canonical,
                "name": title, "description": description, "inLanguage": "en-US", "dateModified": modified,
                "isPartOf": {"@id": self.origin+"/#website"}, "publisher": {"@id": self.origin+"/#organization"}}
        if citations:
            page["citation"] = citations
        graph = [{"@type": "Organization", "@id": self.origin+"/#organization", "name": self.name, "url": self.origin+"/"},
                 {"@type": "WebSite", "@id": self.origin+"/#website", "name": self.name, "url": self.origin+"/", "publisher": {"@id": self.origin+"/#organization"}}, page, *(extra or [])]
        favicon = "/favicon.ico" if not self.fff else self.assets["favicon"]
        markup = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | {self.name}</title><meta name="description" content="{escape(short(description, 165), quote=True)}">
<link rel="canonical" href="{self.origin}{canonical}"><meta name="robots" content="{'index,follow,max-image-preview:large' if index else 'noindex,follow'}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{self.name}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(short(description,165), quote=True)}"><meta property="og:url" content="{self.origin}{canonical}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:description" content="{escape(short(description,165), quote=True)}">
<meta name="theme-color" content="{'#133e3c' if self.fff else '#102d43'}"><link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{self.assets['css']}"><script src="{self.assets['js']}" defer></script>
<script type="application/ld+json">{json_script({'@context':'https://schema.org','@graph':graph})}</script></head>
<body data-site="{self.site}"><a class="skip-link" href="#main">Skip to content</a>{self.nav()}<main id="main">{body}</main>{self.footer()}</body></html>'''
        relative = route.strip("/") + "/index.html" if route != "/" else "index.html"
        target = self.output / relative; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('\n'.join(line.rstrip() for line in markup.splitlines())+'\n', encoding="utf-8")

    def reply_count(self, post):
        return len(self.comment_map[str(post["id"])])

    def row(self, post):
        identifier = str(post["id"]); topic = self.post_groups[identifier][0]; count = self.reply_count(post)
        date = archive_date(post); stamp = f'<span>Archive date <time datetime="{date}">{date}</time></span>' if date else ''
        return f'<article class="discussion-row"><h3><a href="{self.routes[identifier]}">{escape(title_for(post))}</a></h3><p>{escape(short(post.get("body"),185))}</p><div class="row-meta"><a class="category" href="/{topic}/">{escape(self.topic_name(topic))}</a><span>{count} archived {"reply" if count==1 else "replies"}</span>{stamp}</div></article>'

    def sidebar(self, keys=None):
        keys = keys or sorted(self.groups, key=lambda k: -len(self.groups[k]))[:7]
        links = "".join(f'<a class="side-link" href="/{key}/"><span>{escape(self.topic_name(key))}</span><span>{len(self.groups[key]):,}</span></a>' for key in keys if key in self.groups)
        trust = ("These are personal accounts, not treatment instructions. Your own care team can interpret what applies to your situation."
                 if self.fff else "A name appearing in a discussion does not establish current appetite, licensing, availability or a successful placement. Confirm details with the market.")
        return f'<aside class="sidebar"><div class="sidebar-card"><h2>{"Explore topics" if self.fff else "Browse risk classes"}</h2>{links}</div><div class="context-note"><strong>Keep the context.</strong><p>{trust}</p><a href="/about/#sources">About our sources</a></div></aside>'

    def topic_cards(self, keys):
        return '<div class="topic-grid">' + "".join(f'<a class="topic-card" href="/{key}/"><div class="topic-number">{i+1:02d} / {"COMMUNITY TOPIC" if self.fff else "RISK CLASS"}</div><span class="arrow" aria-hidden="true">↗</span><h3>{escape(self.topic_name(key))}</h3><span>{len(self.groups[key]):,} discussions</span></a>' for i, key in enumerate(keys)) + '</div>'

    def homepage(self):
        popular = sorted(self.groups, key=lambda k: -len(self.groups[k]))
        total_replies = sum(self.reply_count(p) for p in self.posts)
        if self.fff:
            title = "Foot health experiences & recovery discussions"
            intro = '<p class="eyebrow">The foot health community archive</p><h1>Real experiences.<br>A little more clarity.</h1><p class="lede">Explore what people share about foot surgery, recovery and everyday foot health. Read their questions, follow the replies, and bring better questions to your own care team.</p><div class="hero-actions"><a class="button" href="#topics">Explore topics</a><a class="button secondary" href="/discussions/">Read discussions</a></div>'
            featured = [k for k in ("bunion-surgery-recovery", "post-surgery-shoes", "plantar-fasciitis") if k in self.groups]
            picture = '<figure class="hero-picture"><img src="/images/topics/homepage-hero.jpg" width="1200" height="350" alt="A clinician examining a foot X-ray" fetchpriority="high"></figure>' if (self.source / "images/topics/homepage-hero.jpg").is_file() else ''
            aside = picture + '<p class="eyebrow">Start with what is on your mind</p>' + "".join(f'<a class="side-link" href="/{k}/"><span>{escape(self.topic_name(k))}</span><span>Explore →</span></a>' for k in featured)
        else:
            title = "Insurance market discussions for independent agents"
            intro = '<p class="eyebrow">Community intelligence for insurance agents</p><h1>Find your next<br>market lead.</h1><p class="lede">Research how other agents discuss hard-to-place risks. Explore carrier mentions, state context and the original questions—all in one searchable archive.</p><form class="search-form" action="/discussions/" method="get"><label class="sr-only" for="home-search">Search risks, carriers and states</label><input id="home-search" type="search" name="q" placeholder="Try roofing, USLI or Florida" required><button class="button" type="submit">Search archive</button></form><p class="hero-note">Research leads from discussions. Current appetite must be confirmed.</p>'
            aside = '<p class="eyebrow">Explore a risk class</p><h2>Start where the risk is.</h2>' + "".join(f'<a class="side-link" href="/{k}/"><span>{escape(self.topic_name(k))}</span><span>{len(self.groups[k]):,} threads</span></a>' for k in popular[:5])
        hero = f'<section class="home-hero"><div class="wrap hero-grid"><div>{intro}</div><div class="hero-aside">{aside}</div></div></section>'
        stats = f'<div class="trust-strip"><div class="wrap trust-inner"><div class="stat"><strong>{len(self.posts):,}</strong><span>archived discussions</span></div><div class="stat"><strong>{total_replies:,}</strong><span>captured replies</span></div><div class="stat"><strong>{len(self.groups)}</strong><span>{"community topics" if self.fff else "risk classes"}</span></div></div></div>'
        all_cards = self.topic_cards(popular[:12])
        if len(popular) > 12:
            all_cards += '<details class="more-topics"><summary>Explore all '+str(len(popular))+' topics</summary>'+self.topic_cards(popular[12:])+'</details>'
        topics = f'<section id="topics" class="section"><div class="wrap"><div class="section-top"><h2>{"Find your starting point" if self.fff else "Research by risk class"}</h2><a href="/discussions/">Browse all discussions →</a></div>{all_cards}</div></section>'
        # The recent archive is drawn from record dates, never the build clock.
        subject = re.compile(r'\b(?:foot|feet|bunion\w*|fasciitis|pf|heel\w*|toe\w*|lapiplasty|lapidus|orthotic\w*|ankle\w*)\b' if self.fff else
                             r'\b(?:insurance|carrier\w*|polic(?:y|ies)|underwrit\w*|liability|workers?\s+comp\w*|coverage|premium\w*|broker\w*)\b', re.I)
        featured = [p for p in self.posts if self.reply_count(p) > 0 and
                    subject.search(text(p.get("body"))[:600])][:5]
        recent = f'<section class="section wash"><div class="wrap"><div class="section-top"><h2>Questions with community replies</h2><a href="/discussions/">View all →</a></div><div class="two-col"><div class="discussion-list">{"".join(self.row(p) for p in featured)}</div>{self.sidebar(popular[:4])}</div></div></section>'
        self.write_page("/", title, "Explore community questions, captured replies and source context about " + ("foot surgery, recovery and foot conditions." if self.fff else "insurance risks, carrier mentions and market research."), hero+stats+topics+recent)

    def mentions(self, posts, field):
        result = defaultdict(list)
        names = {}
        for post in posts:
            values = tokens(post.get(field))
            for reply in self.comment_map[str(post["id"])]:
                values.extend(tokens(reply.get(field)))
            seen = set()
            for value in values:
                key = value.casefold()
                if key not in seen:
                    names.setdefault(key, value); result[key].append(post); seen.add(key)
        return [(names[key], rows) for key, rows in sorted(result.items(), key=lambda pair: (-len(pair[1]), pair[0]))]

    def pagination(self, base, number, total):
        if total <= 1:
            return ""
        url = lambda n: base if n == 1 else base + f"page/{n}/"
        numbers = sorted({1, total, *range(max(1, number-2), min(total, number+2)+1)})
        links = []
        if number > 1:
            links.append(f'<a href="{url(number-1)}" rel="prev">Previous</a>')
        last = 0
        for n in numbers:
            if last and n > last+1:
                links.append('<span class="dots" aria-hidden="true">…</span>')
            links.append(f'<strong aria-current="page" aria-label="Page {n}">{n}</strong>' if n == number else
                         f'<a href="{url(n)}" aria-label="Page {n}">{n}</a>')
            last = n
        if number < total:
            links.append(f'<a href="{url(number+1)}" rel="next">Next</a>')
        return '<nav class="pagination" aria-label="Discussion pages">' + ''.join(links) + '</nav>'

    def evidence(self, posts):
        field = "products_mentioned" if self.fff else "carriers_mentioned"
        mentions = self.mentions(posts, field)[:8]
        if not mentions:
            return ""
        label = "Products mentioned" if self.fff else "Carrier & market mentions"
        rows = []
        for name, source_posts in mentions:
            sources = "".join(f'<a href="{self.routes[str(p["id"])]}" aria-label="Read discussion mentioning {escape(name,quote=True)}">Discussion {i+1}</a>' for i, p in enumerate(source_posts[:3]))
            rows.append(f'<tr><td>{escape(name)}</td><td>{len(source_posts)}</td><td><div class="evidence-links">{sources}</div></td></tr>')
        note = ("A mention can be a question, a positive experience or a criticism. It is not an endorsement."
                if self.fff else "Mentions can include questions, suggestions and declines. They do not confirm successful placements or current appetite.")
        return f'<section id="mentions" class="section"><h2>{label}</h2><div class="table-wrap"><table class="evidence-table"><caption>{note}</caption><thead><tr><th scope="col">Name in the archive</th><th scope="col">Discussions</th><th scope="col">Read the context</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>'

    def archive_pages(self, base, heading, posts, topic=None, state=None):
        self.archive_bases.add(base)
        total = max(1, (len(posts)+PAGE_SIZE-1)//PAGE_SIZE)
        for number in range(1, total+1):
            route = base if number == 1 else base+f"page/{number}/"
            visible = posts[(number-1)*PAGE_SIZE:number*PAGE_SIZE]
            title = heading + (f" — page {number}" if number > 1 else "")
            trail = [(heading, base)] + ([(f"Page {number}", route)] if number > 1 else [])
            crumb, schema = self.breadcrumbs(trail)
            subject = (f"community discussions about {heading.lower()}" if self.fff else f"agent discussions about {heading.lower()}")
            intro = f'Explore {len(posts):,} {subject}, with {sum(self.reply_count(p) for p in posts):,} replies preserved in the archive.'
            if base == "/discussions/":
                intro = f'Browse every archived discussion, with direct links to the question, replies and available source context.'
            search = ""
            if not self.fff and base == "/discussions/":
                all_states = sorted({s for p in self.posts for s in tokens(p.get("states_mentioned"))})
                options = ''.join(f'<option value="{escape(s,quote=True)}">{escape(s)}</option>' for s in all_states)
                search = f'<form class="search-form" action="/discussions/" method="get" data-archive-search="{self.search_asset}"><label for="archive-query" class="sr-only">Search discussions by risk, carrier or state</label><input id="archive-query" name="q" type="search" placeholder="Search a risk, carrier or state"><button class="button" type="submit">Search</button></form><div class="archive-toolbar"><label class="filter-label" for="state-filter">State <select id="state-filter" data-state-filter><option value="">All states</option>{options}</select></label><span>{len(posts):,} archived discussions</span></div><p class="search-status" data-search-status role="status" aria-live="polite"></p><div class="discussion-list search-results" data-search-results></div>'
            pager = self.pagination(base, number, total)
            counter = f'{(number-1)*PAGE_SIZE+1 if posts else 0}–{min(number*PAGE_SIZE,len(posts))} of {len(posts):,} discussions'
            list_html = '<div data-browse-results><div class="archive-toolbar"><span>'+counter+'</span><span>Ordered by archive date</span></div><div class="discussion-list">'+''.join(self.row(p) for p in visible)+'</div>'+pager+'</div>'
            aside = self.sidebar([topic] if topic else None)
            if topic and not self.fff:
                state_groups = self.state_groups(topic)
                state_links = ''.join(f'<a class="side-link" href="/{topic}/{slug(s)}/"><span>{escape(s)}</span><span>{len(rows)} threads</span></a>' for s, rows in sorted(state_groups.items(), key=lambda pair:-len(pair[1]))[:12])
                if state_links:
                    aside = '<aside class="sidebar"><div class="sidebar-card"><h2>State context</h2>'+state_links+'</div><div class="context-note">These are states mentioned in each discussion, not confirmed carrier availability by state.</div></aside>'
            overview = self.evidence(posts) if topic and number == 1 else ""
            if topic and number == 1 and not self.fff:
                codes = [(kind, code, label) for kind in ("NAICS", "SIC") for code, label in self.taxonomy[topic].get(kind.lower(), [])]
                if codes:
                    overview += '<section class="section"><h2>Classification references</h2><p class="site-note">Codes listed for this risk class are a starting point; confirm the classification for the actual operation.</p><div class="pill-row">'+''.join(f'<span class="pill neutral">{kind} {escape(str(code))} · {escape(label)}</span>' for kind,code,label in codes)+'</div></section>'
            note = 'Personal experiences can differ. These discussions are not clinical guidance.' if self.fff else 'Carrier names are mentions in community conversations, not verified placement outcomes.'
            body = f'<div class="wrap">{crumb}<header class="page-head"><p class="eyebrow">{"Community experiences" if self.fff else "Insurance market research"}</p><h1>{escape(title)}</h1><p class="lede">{escape(intro)}</p><p class="site-note">{note}</p></header><div class="two-col"><div>{search}{list_html}{overview}</div>{aside}</div></div>'
            items = {"@type":"ItemList","numberOfItems":len(visible),"itemListElement":[{"@type":"ListItem","position":(number-1)*PAGE_SIZE+i+1,"url":self.origin+self.routes[str(p["id"])],"name":title_for(p)} for i,p in enumerate(visible)]}
            self.write_page(route, title, short(intro, 160), body, kind="CollectionPage", extra=[schema,items])

    def state_groups(self, topic):
        groups = defaultdict(list)
        for p in self.groups[topic]:
            for state in tokens(p.get("states_mentioned")):
                if state in getattr(self, "states", set()) and slug(state):
                    groups[state].append(p)
        return {state:rows for state,rows in groups.items() if len(rows)>=2}

    def images(self, owner):
        if not self.fff:
            return ""
        from site_media import render_images
        return render_images(owner)

    def post_page(self, post, route=None):
        identifier = str(post["id"]); canonical = self.routes[identifier]; route = route or canonical
        heading = title_for(post); groups = self.post_groups[identifier]; first = groups[0]
        crumb, breadcrumb = self.breadcrumbs([(self.topic_name(first), "/"+first+"/"), (heading, canonical)])
        replies = self.comment_map[identifier]
        date = archive_date(post)
        date_label = f'<span>Archive date <time datetime="{date}">{date}</time></span>' if date else ''
        pills = ''.join(f'<a class="pill" href="/{key}/">{escape(self.topic_name(key))}</a>' for key in groups[:5])
        status = (post.get("capture") or {}).get("status")
        if status == "complete":
            completeness = 'The visible discussion was fully captured at the time of collection.'
        elif replies:
            completeness = 'This archive may not include every reply to the original discussion.'
        else:
            completeness = 'Replies have not been captured for this archived discussion.'
        publication = post.get("publication") or {}
        omitted = publication.get("comments_excluded", 0) if isinstance(publication, dict) else 0
        if type(omitted) is int and omitted > 0:
            completeness += ' Promotional replies have been omitted.'
        source = self.source_url(post)
        group = text(post.get("source_group")) or ("a foot health support community" if self.fff else "an insurance community")
        attribution = f'Archived from {escape(group)}. '
        attribution += f'<a href="{escape(source,quote=True)}" rel="ugc nofollow noopener noreferrer">View the original discussion on Facebook</a> (sign-in may be required).' if source else 'The original discussion link is unavailable in this record.'
        question = f'<section aria-label="Original community question"><div class="question"><p>{self.link_text(post.get("body"),canonical)}</p>{self.images(post)}</div><p class="source-line">{attribution}</p></section>'
        comment_html = []; anchors = []; occurrences = Counter()
        for i, reply in enumerate(replies):
            raw_id = text(reply.get("comment_id") or reply.get("local_id"))
            base = slug(raw_id) if raw_id else sha256(text(reply.get("comment_text")).encode()).hexdigest()[:12]
            occurrences[base] += 1; anchor = "comment-"+base+(f'-{occurrences[base]}' if occurrences[base]>1 else '')
            anchors.append(anchor)
            parent = text(reply.get("parent_comment_id"))
            parent_link = f' · <a href="#comment-{slug(parent)}">In reply to an earlier comment</a>' if parent and any(text(c.get("comment_id"))==parent for c in replies) else ''
            comment_html.append(f'<article class="comment{" reply" if parent else ""}" id="{anchor}" data-parent-comment-id="{escape(parent, quote=True)}"><div class="comment-top"><span>{"Community reply" if parent else "Community comment"}{parent_link}</span><a href="#{anchor}" aria-label="Link to comment {i+1}">#{i+1}</a></div><p>{self.link_text(reply.get("comment_text"),canonical)}</p>{self.images(reply)}</article>')
        empty = 'No comments were visible when this discussion was captured.' if status == 'complete' else 'Replies have not yet been captured for this archived question.'
        discussion = '<section id="replies"><div class="comment-heading"><h2>Community replies</h2><span>'+str(len(replies))+' in this archive</span></div><p class="site-note">'+completeness+'</p>'+(''.join(comment_html) if replies else f'<p class="notice">{empty}</p>')+'</section>'
        # This overview reports archive facts and links to the underlying text.
        # It never synthesizes unsupported treatment or coverage advice.
        metadata = self.mentions([post], "products_mentioned" if self.fff else "carriers_mentioned")[:6]
        labels = ', '.join(escape(label) for label,_ in metadata)
        overview = '<div class="sidebar-card"><h2>In this discussion</h2><a class="side-link" href="#question"><span>Original question</span><span>Read</span></a><a class="side-link" href="#replies"><span>Community replies</span><span>'+str(len(replies))+'</span></a>'
        if labels:
            overview += '<p style="margin-top:18px"><strong>'+('Products mentioned' if self.fff else 'Carrier mentions')+'</strong><br>'+labels+'</p>'
        overview += '<p>'+completeness+'</p></div>'
        related = []; seen = {identifier}
        for key in groups:
            for other in self.groups[key]:
                if str(other['id']) not in seen:
                    related.append(other); seen.add(str(other['id']))
                if len(related)>=5: break
            if len(related)>=5: break
        related_html = '<div class="sidebar-card"><h2>Related discussions</h2>'+''.join(f'<a class="side-link" href="{self.routes[str(p["id"])]}"><span>{escape(short(title_for(p),78))}</span></a>' for p in related)+'</div>' if related else ''
        note = 'Shared experiences do not establish what is safe or appropriate for your recovery. Discuss your situation with a qualified clinician.' if self.fff else 'Treat names and experiences as research leads. Confirm current underwriting appetite, terms and availability with the carrier or intermediary.'
        aside = '<aside class="sidebar">'+overview+related_html+'<div class="context-note">'+note+' <a href="/about/#sources">How to use this archive</a></div></aside>'
        body = f'<div class="wrap">{crumb}<header class="discussion-head" id="question"><p class="eyebrow">Community discussion</p><h1>{escape(heading)}</h1><div class="row-meta">{date_label}<span>{len(replies)} archived replies</span></div><div class="pill-row">{pills}</div></header><div class="two-col"><div class="prose">{question}{discussion}</div>{aside}</div><a class="back-link" href="/{first}/">← More {escape(self.topic_name(first))}</a></div>'
        description = short(text(post.get("body")), 115) + f' Read {len(replies)} archived replies and the available source context.'
        self.write_page(route, heading, description, body, extra=[breadcrumb], canonical=canonical,
                        citations=[source] if source else None)

    def about(self):
        heading = f"About {self.name}"
        crumb, breadcrumb = self.breadcrumbs([(heading, "/about/")])
        subject = 'foot health and recovery' if self.fff else 'insurance placement and market research'
        role = ('This site is a community-experience archive. It is not a medical practice, and discussions are not reviewed or endorsed as clinical advice.' if self.fff else
                'This site is a community-discussion archive. It is not a carrier appetite database, and a mention does not verify coverage, eligibility or a successful placement.')
        guide = '' if self.fff else '<h2>Market guides</h2><p>Editorial market guides are presented separately from community discussions. Each guide retains its stated update period and supporting source links. Availability and terms can change; confirm them with the named market.</p>'
        prose = f'<div class="prose"><p class="lede">A clearer way to explore community conversations about {subject}.</p><h2>What you will find</h2><p>The archive contains {len(self.posts):,} discussions, organized by topic, with the replies and source links available in each record. Questions and comments describe individual experiences; they do not establish consensus.</p><h2 id="sources">Sources &amp; limitations</h2><p>{role}</p><p>Discussions originate in online communities, including Facebook groups. An original source link is shown when available; accessing it may require sign-in or group membership. Older records can be missing their source link or replies. Pages say when the archived discussion may be incomplete.</p><h2>How the archive is maintained</h2><p>The collection process retains discussion identities and reply relationships, revisits older records, and expands accessible comments. It cannot recover material that is deleted or inaccessible. No missing answers are invented. Topic labels and mention counts organize the archive; they are not professional recommendations.</p><h2>Dates and context</h2><p>Archive dates come from stored records. They are not replaced with today’s date each time the site is rebuilt and may differ from the date of the original conversation. Always read the surrounding question and replies before using an excerpt.</p>{guide}<h2>Using a community account responsibly</h2><p>{"Use these accounts to prepare questions for your care team, not to diagnose a condition or choose a treatment without professional advice." if self.fff else "Use these accounts to identify questions and markets to research. Confirm current appetite, state eligibility and terms directly before relying on any suggestion."}</p></div>'
        self.write_page('/about/', heading, f'Learn how {self.name} organizes community discussions, preserves source context and labels limitations.', '<div class="wrap">'+crumb+'<header class="page-head"><p class="eyebrow">Sources and methodology</p><h1>'+heading+'</h1></header>'+prose+'</div>', kind='AboutPage', extra=[breadcrumb])

    def guide_pages(self):
        guides = self.guides_data.get('guides', [])
        hub = self.guides_data.get('hub', {})
        if not guides:
            return
        for guide in guides:
            route = '/guides/'+slug(guide['slug'])+'/'
            heading = text(guide['title']); crumb, breadcrumb = self.breadcrumbs([('Market guides','/hard-to-place-insurance/'),(heading,route)])
            updated = text(guide.get('updated'))
            content = ''.join('<p>'+rich(p)+'</p>' for p in guide.get('intro',[]))
            if guide.get('alert'):
                alert = guide['alert']; content += '<div class="notice">'+rich(alert if isinstance(alert,str) else alert.get('text', ''))+'</div>'
            if guide.get('markets'):
                rows = ''.join('<tr>'+''.join('<td>'+rich(market.get(key,''))+'</td>' for key in ('name','type','access','notes'))+'</tr>' for market in guide['markets'])
                content += '<h2>Markets and access</h2><div class="table-wrap"><table class="evidence-table"><caption>Editorial research from the guide’s stated update period. Confirm current availability and terms.</caption><thead><tr><th scope="col">Market</th><th scope="col">Type</th><th scope="col">Access</th><th scope="col">Context</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
            if guide.get('pain_points'):
                content += '<h2>Issues to research</h2><ul>'+''.join('<li>'+rich(p)+'</li>' for p in guide['pain_points'])+'</ul>'
            if guide.get('faq'):
                content += '<h2>Questions covered in this guide</h2><div class="details-list">'+''.join('<details><summary>'+escape(item['q'])+'</summary><p>'+rich(item['a'])+'</p></details>' for item in guide['faq'])+'</div>'
            content += self.sources(guide.get('sources',[]))
            niche = guide.get('niche'); related = self.groups.get(niche,[])[:4]
            if related:
                content += '<h2>Related community discussions</h2><div class="discussion-list">'+''.join(self.row(p) for p in related)+'</div>'
            body = '<div class="wrap">'+crumb+'<header class="page-head"><p class="eyebrow">Editorial market guide'+(' · Updated '+escape(updated) if updated else '')+'</p><h1>'+escape(heading)+'</h1></header><div class="two-col"><article class="prose">'+content+'</article>'+self.sidebar([niche] if niche else None)+'</div></div>'
            self.write_page(route, heading, text(guide.get('meta_description')), body, extra=[breadcrumb], citations=[safe_url(s.get('url')) for s in guide.get('sources',[]) if safe_url(s.get('url'))])
        cards = '<div class="guide-grid">'+''.join('<a class="guide-card" href="/guides/'+slug(g['slug'])+'/"><h3>'+escape(g['title'])+'</h3><p>'+escape(short(g.get('meta_description'),150))+'</p><span>Read the guide →</span></a>' for g in guides)+'</div>'
        content = ''.join('<p>'+rich(p)+'</p>' for p in hub.get('intro',[]))
        if hub.get('wholesalers'):
            content += '<h2>Wholesalers and access platforms</h2><div class="table-wrap"><table class="evidence-table"><caption>Names and descriptions from the guide’s stated update period.</caption><thead><tr><th scope="col">Organization</th><th scope="col">Context</th></tr></thead><tbody>'+''.join('<tr><td>'+escape(m['name'])+'</td><td>'+rich(m.get('notes'))+'</td></tr>' for m in hub['wholesalers'])+'</tbody></table></div>'
        content += ''.join('<h2>'+escape(item['h'])+'</h2><p>'+rich(item['p'])+'</p>' for item in hub.get('basics',[]))
        content += self.sources(hub.get('sources',[]))
        crumb, breadcrumb = self.breadcrumbs([('Hard-to-place insurance guides','/hard-to-place-insurance/')])
        body = '<div class="wrap">'+crumb+'<header class="page-head"><p class="eyebrow">Market guides · '+escape(text(hub.get('updated')))+'</p><h1>Research your next route to market.</h1><p class="lede">Sourced guides to specialty risks, wholesalers and market access, alongside the community discussions that add context.</p></header>'+cards+'<section class="section prose">'+content+'</section></div>'
        self.write_page('/hard-to-place-insurance/','Hard-to-place insurance market guides',text(hub.get('meta_description')),body,kind='CollectionPage',extra=[breadcrumb])

    @staticmethod
    def sources(sources):
        valid = [s for s in sources if safe_url(s.get('url'))]
        return '<h2>Sources</h2><ul class="source-list">'+''.join(f'<li><a href="{escape(s["url"],quote=True)}" rel="noopener noreferrer">{escape(s.get("label") or s["url"])}</a></li>' for s in valid)+'</ul>' if valid else ''

    def prepare_assets(self):
        self.output.mkdir(parents=True,exist_ok=True)
        asset_dir = self.output/'assets'; asset_dir.mkdir(exist_ok=True)
        for kind, filename in (('css','site.css'),('js','site.js')):
            data = (self.source/'site_assets'/filename).read_bytes()
            name = f'{kind}-{sha256(data).hexdigest()[:12]}.{kind}'
            (asset_dir/name).write_bytes(data); self.assets[kind] = '/assets/'+name
        if self.fff:
            favicon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#133e3c"/><path d="M10 7h14v4H14v5h8v4h-8v7h-4z" fill="white"/></svg>'
            (asset_dir/'favicon.svg').write_text(favicon); self.assets['favicon']='/assets/favicon.svg'
        else:
            for pattern in ('favicon*','apple-touch-icon.png','android-chrome-*.png'):
                for source in self.source.glob(pattern):
                    if source.is_file() and not source.is_symlink() and source.suffix in {'.ico','.png','.svg'}:
                        shutil.copy2(source,self.output/source.name)
            records=[]
            for post in self.posts:
                identifier=str(post['id']); title=title_for(post); topic=self.topic_name(self.post_groups[identifier][0])
                searchable=' '.join([title,text(post.get('body')),*[' '.join(tokens(post.get(field))) for field in self.tag_fields],*[text(c.get('comment_text')) for c in self.comment_map[identifier]]]).casefold()
                records.append({'title':title,'url':self.routes[identifier],'excerpt':short(post.get('body'),185),'replies':self.reply_count(post),'topic':topic,'states':tokens(post.get('states_mentioned')),'search':searchable})
            data=json_script(records).encode(); name='search-'+sha256(data).hexdigest()[:12]+'.json'; (asset_dir/name).write_bytes(data); self.search_asset='/assets/'+name
        if (self.source/'images').is_dir():
            shutil.copytree(self.source/'images',self.output/'images',dirs_exist_ok=True)

    def finish(self):
        routes={'version':1,'posts':self.routes,'aliases':self.aliases,
                'retired_posts':self.retired_posts,'retired_aliases':self.retired_aliases}
        (self.output/'site-routes.json').write_text(json.dumps(routes,indent=2,ensure_ascii=False)+'\n')
        (self.output/'site-history.json').write_text(json.dumps({'version':1,'pages':self.pages},indent=2,sort_keys=True)+'\n')
        sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(self.origin+route)+'</loc><lastmod>'+self.pages[route]['modified']+'</lastmod></url>\n' for route in sorted(self.indexable))+'</urlset>\n'
        (self.output/'sitemap.xml').write_text(sitemap)
        old_robots=(self.source/'robots.txt').read_text() if (self.source/'robots.txt').exists() else 'User-agent: *\nAllow: /\n'
        old_robots=re.sub(r'^Sitemap:.*$', '', old_robots,flags=re.M).strip()
        if 'OAI-SearchBot' not in old_robots:
            old_robots+='\n\n# Search inclusion is distinct from model-training permissions.\nUser-agent: OAI-SearchBot\nAllow: /'
        (self.output/'robots.txt').write_text(old_robots+'\n\nSitemap: '+self.origin+'/sitemap.xml\n')
        existing=(self.source/'_headers').read_text() if (self.source/'_headers').exists() else ''
        # Replace stale agent-service advertising while retaining unrelated headers.
        existing=re.sub(r'\n?# BEGIN ARCHIVE HEADERS.*?# END ARCHIVE HEADERS\n?', '', existing, flags=re.S)
        blocks=[]
        for block in re.split(r'\n\s*\n', existing.strip()):
            lines=block.splitlines()
            if not lines or any(word in lines[0] for word in ('mcp/server-card','agent-skills','api-catalog')):
                continue
            lines=[line for line in lines if not any(word in line for word in ('mcp/server-card','agent-skills','api-catalog'))]
            if len(lines)>1:
                blocks.append('\n'.join(lines))
        headers='\n\n'.join(blocks)+'\n\n# BEGIN ARCHIVE HEADERS\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n\n/site-history.json\n  X-Robots-Tag: noindex\n/site-routes.json\n  X-Robots-Tag: noindex\n/site-build-report.json\n  X-Robots-Tag: noindex\n/posts.json\n  X-Robots-Tag: noindex\n/*.py\n  X-Robots-Tag: noindex\n# END ARCHIVE HEADERS\n'
        (self.output/'_headers').write_text(headers)
        if (self.source/'redirects.json').exists():
            redirects=self.load_json(self.source/'redirects.json',[])
            redirects=[dict(r,to=self.routes[self.aliases[r['to']]]) if isinstance(r,dict) and r.get('to') in self.aliases else r for r in redirects]
            lines=[f"{r['from']} {r['to']} 301" for r in redirects if isinstance(r,dict) and text(r.get('from')).startswith('/') and text(r.get('to')).startswith('/') and not any(c.isspace() for c in str(r['from'])+str(r['to']))]
            (self.output/'_redirects').write_text('\n'.join(lines)+'\n')
        elif (self.source/'_redirects').exists():
            shutil.copy2(self.source/'_redirects',self.output/'_redirects')
        info=f'# {self.name}\n\nA static archive of community discussions about '+('foot health and recovery.' if self.fff else 'insurance market research.')+'\n\n- [About and source limitations]('+self.origin+'/about/)\n- [All discussions]('+self.origin+'/discussions/)\n- [Sitemap]('+self.origin+'/sitemap.xml)\n\nQuestions and replies reflect individual experiences. Mention counts are not recommendations or verified outcomes. The site offers no MCP server or callable agent tools.\n'
        (self.output/'llms.txt').write_text(info)
        descriptions={'.well-known/api-catalog':{'name':self.name,'apis':[],'resources':[{'url':self.origin+'/sitemap.xml','type':'sitemap'}]},'.well-known/agent-skills/index.json':{'name':self.name,'skills':[],'url':self.origin+'/'},'.well-known/mcp/server-card.json':{'name':self.name,'type':'static-website','description':'No MCP server or callable tools are provided.','url':self.origin+'/'}}
        for relative,value in descriptions.items():
            path=self.output/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
        report={'site':self.site,'source_posts':self.source_post_count,'usable_posts':len(self.posts),'excluded_posts':len(self.excluded_ids),'retired_discussion_routes':len(self.retired_routes),'canonical_discussions':len(self.routes),'legacy_aliases':len(self.aliases),'indexable_pages':len(self.indexable),'generated_pages':len(self.pages),'topics':len(self.groups),'shared_css_bytes':len((self.source/'site_assets/site.css').read_bytes())}
        (self.output/'site-build-report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report),flush=True)

    def removed_page(self, route, *, archive=False):
        heading = 'This archive page is no longer available' if archive else 'This discussion is no longer in the archive'
        body = '<div class="wrap"><header class="page-head"><h1>'+heading+'</h1><p>Browse the current collection for available community discussions.</p><a class="button" href="/discussions/">Browse discussions</a></header></div>'
        self.write_page(route, heading, 'Browse the available community discussions.', body, index=False)

    def retire_obsolete_archives(self):
        # Rebuild overlays files. Replace obsolete owned indexes so their old
        # excerpts cannot remain public after a topic or final page empties.
        bases = self.archive_bases | {'/discussions/'} | {'/'+key+'/' for key in self.taxonomy}
        candidates = set()
        for base in bases:
            if base in self.old_history or (self.source/base.strip('/')/'index.html').is_file():
                candidates.add(base)
            pagination = self.source/base.strip('/')/'page'
            for old_page in pagination.glob('*/index.html'):
                number = old_page.parent.name
                if number.isdigit() and int(number) >= 2:
                    candidates.add(base+'page/'+number+'/')
        for route in self.old_history:
            match = re.fullmatch(r'(.+/)page/([1-9][0-9]*)/', route)
            if match and match[1] in bases and int(match[2]) >= 2:
                candidates.add(route)
        for route in sorted(candidates):
            if route not in self.pages and self.valid_route(route):
                self.removed_page(route, archive=True)

    def build(self, states=None):
        self.states=set(states or [])
        self.prepare_assets()
        self.homepage()
        self.archive_pages('/discussions/', 'All foot health discussions' if self.fff else 'All insurance discussions', self.posts)
        for topic, rows in self.groups.items():
            self.archive_pages('/'+topic+'/',self.topic_name(topic),rows,topic=topic)
            if not self.fff:
                for state,state_rows in self.state_groups(topic).items():
                    self.archive_pages('/'+topic+'/'+slug(state)+'/',self.topic_name(topic)+' in '+state,state_rows,topic=topic,state=state)
                # Retain previously published state pages even when only one
                # current record remains; empty old routes get an honest noindex page.
                for old_page in (self.source/topic).glob('*/index.html'):
                    route='/'+topic+'/'+old_page.parent.name+'/'
                    if route in self.pages or old_page.parent.name=='page':
                        continue
                    state=next((s for s in self.states if slug(s)==old_page.parent.name),None)
                    if state:
                        state_rows=[p for p in rows if state in tokens(p.get('states_mentioned'))]
                        if state_rows:
                            self.archive_pages(route,self.topic_name(topic)+' in '+state,state_rows,topic=topic,state=state)
                        else:
                            heading='No current archived discussions for this state'
                            body='<div class="wrap"><header class="page-head"><h1>'+heading+'</h1><p>The archive currently has no matching '+escape(self.topic_name(topic))+' discussions tagged '+escape(state)+'.</p><a class="button" href="/'+topic+'/">Browse this risk class</a></header></div>'
                            self.write_page(route,heading,'Browse related insurance discussions in the archive.',body,index=False)
        by_id={str(p['id']):p for p in self.posts}
        for post in self.posts:
            self.post_page(post)
        for alias, identifier in self.aliases.items():
            self.post_page(by_id[identifier],alias)
        for route in sorted(self.retired_routes):
            if route not in self.pages:
                self.removed_page(route)
        self.retire_obsolete_archives()
        if not self.fff:
            for old_page in (self.source/'discussions').glob('*/index.html'):
                route='/discussions/'+old_page.parent.name+'/'
                if route in self.pages or not self.valid_route(route):
                    continue
                heading='This discussion is no longer in the archive'
                body='<div class="wrap"><header class="page-head"><h1>'+heading+'</h1><p>The old link does not match a discussion in the current collection.</p><a class="button" href="/discussions/">Browse available discussions</a></header></div>'
                self.write_page(route,heading,'Browse the available insurance discussions.',body,index=False)
        self.about()
        self.guide_pages()
        self.finish()
        return self


def build_site(*, site, source_dir, output_dir, posts, taxonomy, classify=None,
               preferred_routes=None, legacy_routes=None, states=None):
    return ArchiveSite(site,source_dir,output_dir,posts,taxonomy,classify,
                       preferred_routes,legacy_routes).build(states)
