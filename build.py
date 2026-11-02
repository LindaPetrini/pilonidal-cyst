#!/usr/bin/env python3
"""Build pilonidal cyst guide: markdown -> HTML + PDF."""

import os
import re
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, "build")
GUIDE_PATH = os.path.join(BASE_DIR, "guide.md")
SITE_URL = "https://pilonidal.lindapetrini.com/"
# Umami website ID for this site. Empty = no tracking tag. Must be this site's own ID.
UMAMI_WEBSITE_ID = ""
SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{site_url}</loc></url>
</urlset>
"""


def extract_toc(md_text):
    """Extract table of contents from markdown headings."""
    toc = []
    for match in re.finditer(r'^(#{1,3})\s+(.+?)(?:\s*\{#([^}]+)\})?\s*$', md_text, re.MULTILINE):
        level = len(match.group(1))
        title = match.group(2).strip()
        # Clean up numbered prefixes like "2. "
        title = re.sub(r'^\d+\.\s*', '', title)
        anchor = match.group(3)
        if not anchor:
            anchor = re.sub(r'[^\w\s-]', '', title.lower())
            anchor = re.sub(r'[\s]+', '-', anchor).strip('-')
        if title and not title.startswith('#'):
            toc.append({"level": level, "title": title, "anchor": anchor})
    return toc


def build_html(md_text):
    """Convert markdown to HTML with extensions."""
    extensions = ["toc", "tables", "fenced_code", "attr_list", "md_in_html"]
    md = markdown.Markdown(extensions=extensions)
    return md.convert(md_text)


def build():
    os.makedirs(BUILD_DIR, exist_ok=True)

    with open(GUIDE_PATH, "r") as f:
        md_text = f.read()

    # Skip the manual TOC at the top (everything before Introduction)
    intro_match = re.search(r'^(2\.\s*#\s*Introduction)', md_text, re.MULTILINE)
    if intro_match:
        md_text = md_text[intro_match.start():]

    toc = extract_toc(md_text)
    content_html = build_html(md_text)

    env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))

    # Build web page
    template = env.get_template("index.html")
    page_html = template.render(
        content=content_html, toc=toc, site_url=SITE_URL, umami_website_id=UMAMI_WEBSITE_ID
    )
    with open(os.path.join(BUILD_DIR, "index.html"), "w") as f:
        f.write(page_html)

    # Build sitemap
    with open(os.path.join(BUILD_DIR, "sitemap.xml"), "w") as f:
        f.write(SITEMAP_XML.format(site_url=SITE_URL))

    # Build PDF
    pdf_template = env.get_template("pdf.html")
    pdf_html = pdf_template.render(content=content_html)
    HTML(string=pdf_html, base_url=BASE_DIR).write_pdf(
        os.path.join(BUILD_DIR, "pilonidal-cyst-guide.pdf")
    )

    # Copy static assets
    static_src = os.path.join(BASE_DIR, "static")
    static_dst = os.path.join(BUILD_DIR, "static")
    if os.path.exists(static_dst):
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

    # Copy images
    images_src = os.path.join(BASE_DIR, "images")
    images_dst = os.path.join(BUILD_DIR, "images")
    if os.path.exists(images_dst):
        shutil.rmtree(images_dst)
    shutil.copytree(images_src, images_dst)

    print(f"Built: {BUILD_DIR}/index.html")
    print(f"Built: {BUILD_DIR}/pilonidal-cyst-guide.pdf")
    print(f"Built: {BUILD_DIR}/sitemap.xml")


if __name__ == "__main__":
    build()
