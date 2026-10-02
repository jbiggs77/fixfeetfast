# Building the community archive

Run `python3 generate_site.py` to build `site/` using only the Python standard library.
`site_config.py` contains the original taxonomy and legacy input cleanup. `site_builder.py`
contains the shared renderer; `site_assets/` contains its CSS and progressive search script.
FixFeetFast also uses `site_media.py` to render verified, local photo assets.

The daily scraper runs `facebook_scraper.rebuild` from the parent Scrapers workspace,
which builds into a fresh temporary directory, validates the complete output, copies only
allowed public files and stages an explicit manifest. WhereToPlace retains its existing
tracked `site/` mirror via `site-output.json`; root and mirror receive identical pages.

Keep `site-routes.json` and `site-history.json` when rebuilding. They preserve discussion
URLs, legacy aliases and meaningful modification dates across content backfills. Never
replace missing record dates with the build date. Pagination pages are self-canonical;
legacy aliases point to a single current discussion. Removed legacy records are noindex.

Search-facing behaviour (since 2026-10-02):

- `lastmod` and `dateModified` track each page's own content (`content_key` in
  `write_page`), not the rendered body, so related-link lists, counts and sidebars
  that shift when other records arrive no longer re-date the whole site. Bump
  `TEMPLATE_VERSION` in `site_builder.py` to deliberately re-date every page after a
  markup change search engines should re-fetch.
- Pagination pages (`/page/N/`) are `noindex,follow` and are not listed in the sitemap.
- Discussion pages are indexable only when they have a real exchange:
  `INDEX_MIN_REPLIES` replies and `INDEX_MIN_WORDS` words, or a question of at least
  `INDEX_RICH_BODY_WORDS` words. Thinner records stay published and linked but are
  `noindex,follow` and leave the sitemap. The build summary reports
  `indexable_discussions` and `noindex_thin_discussions`.
- Each discussion page carries `DiscussionForumPosting` structured data with its
  archived replies as `Comment` nodes. Attribution is the anonymised
  "Community member"; member names are never published.
- A record may carry an editorial `seo_title` in `posts.json`; when present (12–120
  characters) it becomes the page title, H1 and headline. Existing routes never change.

All question and reply text is rendered in HTML. Search indexes complete archived text.
No model-generated clinical answers, placement claims, invented authors or publication
history are added. Existing sourced market guides retain their stated editorial dates.
Structured data describes the visible webpage, collection and breadcrumbs. These changes
support discovery and citation; they do not promise rankings or AI answer inclusion.

Validation for this migration is recorded in the parent workspace at
`audits/site-redesign-20260911/summary.md`.
