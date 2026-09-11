"""Safe local community photo and comment rendering for the static site."""

from html import escape
import re


IMAGE_PATH = re.compile(r"images/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_.-]+\.(?:webp|png|jpe?g|gif)\Z", re.I)
COMMENT_ID = re.compile(r"[A-Za-z0-9_-]+\Z")


def render_images(owner, limit=None):
    if not isinstance(owner, dict):
        return ""
    candidates = [item for item in (owner.get("attachments") or []) if isinstance(item, dict)]
    candidates.extend({"path": path} for path in (owner.get("images") or []) if isinstance(path, str))
    images, seen = [], set()
    for item in candidates:
        path = item.get("path", "")
        if (not isinstance(path, str) or not IMAGE_PATH.fullmatch(path)
                or any(piece in {"", ".", ".."} for piece in path.split("/")) or path in seen):
            continue
        seen.add(path)
        alt = escape(str(item.get("alt") or "Community photo"), quote=True)
        dimensions = "".join(f' {key}="{item[key]}"' for key in ("width", "height")
                             if type(item.get(key)) is int and 0 < item[key] <= 10000)
        url = "/" + escape(path, quote=True)
        images.append(f'<a href="{url}" target="_blank" rel="noopener"><img src="{url}" alt="{alt}"{dimensions} loading="lazy" decoding="async"></a>')
        if limit is not None and len(images) >= limit:
            break
    if not images:
        return ""
    kind = "single" if len(images) == 1 else "gallery"
    return f'<div class="discussion-images {kind}">' + "\n".join(images) + "</div>\n"


def render_comment(comment, compact=False, depth=0):
    value = comment if isinstance(comment, dict) else {"comment_text": str(comment)}
    text = str(value.get("comment_text") or "")
    if compact and len(text) > 200:
        text = text[:200] + "..."
    photos = render_images(value, limit=1 if compact else None)
    replies = ""
    if depth < 20 and isinstance(value.get("replies"), list):
        replies = "".join(render_comment(reply, compact, depth + 1) for reply in value["replies"])
    if not text and not photos:
        return replies
    comment_id = str(value.get("comment_id") or "")
    parent_id = str(value.get("parent_comment_id") or "")
    attributes = ""
    if COMMENT_ID.fullmatch(comment_id):
        attributes += f' id="comment-{escape(comment_id, quote=True)}"'
    if COMMENT_ID.fullmatch(parent_id):
        attributes += f' data-parent-comment-id="{escape(parent_id, quote=True)}"'
    reply = bool(parent_id or depth)
    kind = "comment" if compact else "post-comment-card"
    if reply:
        kind += " reply"
        attributes += ' style="margin-left: 1.5rem; border-left: 3px solid var(--border);"'
    label = "Community member · Reply" if reply else "Community member"
    return (f'<div class="{kind}"{attributes}><div class="comment-text">{escape(text)}</div>'
            f'{photos}<div class="comment-meta">{label}</div>{replies}</div>\n')
