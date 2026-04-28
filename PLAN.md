# Pilonidal Cyst Guide → Static Website

## Context

15k-word markdown guide about pilonidal cysts → polished static website at `pilonidal.lindapetrini.com` with email-gated PDF download, PayPal donations, sticky sidebar navigation.

Stack: plain HTML+CSS, Python build script (markdown+jinja2→HTML), WeasyPrint for PDF, Buttondown for email list, PayPal donate button.

---

## Phase 0: Repository Setup

1. Rename the long filename → `guide.md`
2. Extract 2 base64 images from end of file → `images/image1.png`, `images/image2.png`, update references
3. Create `.gitignore` (build/, *.pdf)
4. `git init` + initial commit

## Phase 1: Content Improvement

### 1A: Link Health Check
- Write `scripts/check_links.py` — extract all URLs, check each with HEAD/GET, report dead/redirected
- Fix or remove broken links

### 1B: Content Review (3 parallel agents)
1. **Medical accuracy** — flag outdated claims, verify surgery descriptions and recurrence rates
2. **Tone/voice** — harmonize mixed registers into consistent empathetic-but-informative voice
3. **Structure** — fix empty headings, inconsistent levels, stub sections (Conclusion, Controversies, Online Support)

### 1C: Apply edits, Linda adds personal story update, commit

## Phase 2: Site Build

### File structure
```
guide.md                     # source of truth
build.py                     # md → html + pdf
templates/index.html         # jinja2 page template
templates/pdf.html           # pdf-specific template
static/style.css             # warm, calming theme
static/print.css             # pdf/print styles
static/main.js               # scroll spy, mobile nav
images/                      # extracted images
build/                       # output (gitignored)
scripts/check_links.py
```

### build.py
- markdown lib (toc, tables, fenced_code, attr_list) → HTML
- Extract TOC for sidebar nav
- Render via jinja2 template
- WeasyPrint generates PDF
- Copy assets to build/

### Site layout
- Header: title, subtitle, "Download PDF" + "Donate" CTAs
- Sticky sidebar TOC with scroll-spy highlighting, collapsible subsections
- Main content area
- Footer: email signup, PayPal, byline, medical disclaimer
- Responsive: sidebar → hamburger below 768px

## Phase 3: Email Gate (Buttondown)
- Linda creates Buttondown account (manual)
- Embed form in footer + modal on "Download PDF" click
- Welcome email contains PDF download link
- PDF at non-guessable URL path

## Phase 4: PayPal Donate Button
- Standard HTML form, no API
- Header CTA + footer

## Phase 5: Deployment
1. DNS: A record `pilonidal.lindapetrini.com` → `91.98.143.115`
2. nginx config: static serving from build/
3. SSL: `certbot --nginx -d pilonidal.lindapetrini.com`
4. Deploy = just `python3 build.py`

## Phase 6: QA
- Test desktop + mobile, all anchor links, email flow, PayPal button
- Run link checker, add OG meta tags

## Manual steps (Linda)
- [ ] Write personal story update, add to guide.md
- [ ] Create Buttondown account, share embed form code
- [ ] Generate PayPal donate button (or share PayPal email)
- [ ] Add DNS A record for pilonidal.lindapetrini.com
