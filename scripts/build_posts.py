#!/usr/bin/env python3
"""
Simple converter: reads Markdown files from `incoming_posts/` with optional YAML front matter,
converts to HTML files under `posts/` using a simple template.

Run: python3 scripts/build_posts.py
"""
import os
import re
import sys
import datetime
from pathlib import Path

try:
    import markdown
    import yaml
except Exception:
    print("Missing dependencies. Install with: pip install -r requirements.txt")
    raise

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "incoming_posts"
OUTDIR = ROOT / "posts"
TEMPLATE = ROOT / "templates" / "post_template.html"
INDEX_TEMPLATE = ROOT / "templates" / "index_template.html"
ARCHIVE_TEMPLATE = ROOT / "templates" / "archive_template.html"

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"(^-|-$)", "", text)
    return text or "post"


def parse_front_matter(content: str):
    m = FRONT_RE.match(content)
    if not m:
        return {}, content
    raw = m.group(1)
    body = content[m.end():]
    data = yaml.safe_load(raw) or {}
    return data, body


def render_post(md_content: str, meta: dict):
    html = markdown.markdown(md_content, extensions=["fenced_code", "codehilite", "tables"])
    title = meta.get("title") or "Untitled"
    date = meta.get("date") or datetime.date.today().isoformat()
    author = meta.get("author", "")
    out = TEMPLATE.read_text(encoding="utf-8")
    out = out.replace("{{ title }}", title)
    out = out.replace("{{ date }}", str(date))
    out = out.replace("{{ author }}", author)
    out = out.replace("{{ content }}", html)
    return out


def parse_date(text: str):
    """Try several date formats, return datetime.date or None."""
    from datetime import datetime
    text = text.strip()
    formats = ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"]
    for f in formats:
        try:
            return datetime.strptime(text, f).date()
        except Exception:
            continue
    # try ISO without dashes
    try:
        return datetime.fromisoformat(text).date()
    except Exception:
        return None


def read_post_meta_from_html(path: Path):
    text = path.read_text(encoding='utf-8')
    # title from first <h1>
    import re
    t = re.search(r"<h1>(.*?)</h1>", text, re.IGNORECASE | re.DOTALL)
    title = t.group(1).strip() if t else path.stem
    d = re.search(r"<p class=\"date\">([^<]+)</p>", text, re.IGNORECASE)
    date_text = d.group(1).strip() if d else ""
    date = parse_date(date_text)
    return {"title": title, "date": date, "date_text": date_text, "slug": path.name}


def generate_index_and_archive(posts_dir: Path, index_template: Path, archive_template: Path, root: Path):
    posts = []
    for p in posts_dir.glob("*.html"):
        meta = read_post_meta_from_html(p)
        posts.append(meta)

    # sort by date (None last)
    import datetime
    posts.sort(key=lambda x: (x["date"] is None, x["date"] or datetime.date.min), reverse=True)

    # generate index
    if not index_template.exists() or not archive_template.exists():
        print("Index or archive template missing; skipping index/archive generation")
        return

    index_html = index_template.read_text(encoding='utf-8')
    # build posts list markup
    posts_items = []
    for p in posts:
        title = p["title"]
        href = f"/posts/{p['slug']}"
        date = p.get("date_text") or ""
        item = f'<li><a href="{href}">{title}</a> <span class="date">{date}</span></li>'
        posts_items.append(item)
    index_html = index_html.replace("{{ posts_list }}", "\n".join(posts_items))
    (root / 'index.html').write_text(index_html, encoding='utf-8')
    print("Wrote index.html")

    # generate archive grouped by year
    from collections import defaultdict
    years = defaultdict(list)
    for p in posts:
        year = p["date"].year if p["date"] else "Unknown"
        years[year].append(p)

    archive_html = archive_template.read_text(encoding='utf-8')
    year_blocks = []
    for y in sorted(years.keys(), reverse=True):
        items = []
        for p in sorted(years[y], key=lambda x: x.get('date') or datetime.date.min, reverse=True):
            title = p['title']
            href = f"/posts/{p['slug']}"
            date = p.get('date_text') or ""
            items.append(f'<li><span class="archive-date">{date}</span><a href="{href}">{title}</a></li>')
        block = f"<h2>{y}</h2>\n<ul class=\"archive-list\">\n" + "\n".join(items) + "\n</ul>"
        year_blocks.append(block)
    archive_html = archive_html.replace("{{ archive_blocks }}", "\n".join(year_blocks))
    (root / 'archive.html').write_text(archive_html, encoding='utf-8')
    print("Wrote archive.html")


def main():
    if not INCOMING.exists():
        print("Creating incoming_posts/ — put your .md posts there (with optional YAML front matter).")
        INCOMING.mkdir(parents=True, exist_ok=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    if not TEMPLATE.exists():
        print(f"Missing template at {TEMPLATE}. Create templates/post_template.html")
        sys.exit(1)

    converted = []
    for p in sorted(INCOMING.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        title = meta.get("title") or p.stem
        slug = meta.get("slug") or slugify(title)
        filename = slug + ".html"
        outpath = OUTDIR / filename
        html = render_post(body, meta)
        outpath.write_text(html, encoding="utf-8")
        converted.append(str(outpath.relative_to(ROOT)))
        print("Wrote", outpath)

    if converted:
        print("Converted:")
        for c in converted:
            print(" -", c)
    else:
        print("No Markdown files found in incoming_posts/")
    
    # Rebuild index and archive from all posts
    generate_index_and_archive(OUTDIR, INDEX_TEMPLATE, ARCHIVE_TEMPLATE, ROOT)


if __name__ == '__main__':
    main()

