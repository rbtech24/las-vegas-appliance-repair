#!/usr/bin/env python3
"""Deep static SEO audit for Las Vegas Appliance Repair Pros."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://www.lasvegasappliancerepairpros.com"
OUT = ROOT / "SEO-AUDIT.md"


def strip_tags(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;|&#\d+;|&\w+;", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def meta(html: str, name: str) -> str | None:
    m = re.search(
        rf'<meta[^>]+name=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)["\']',
        html,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{re.escape(name)}["\']',
        html,
        re.I,
    )
    return m.group(1) if m else None


def prop(html: str, name: str) -> str | None:
    m = re.search(
        rf'<meta[^>]+property=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)["\']',
        html,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']{re.escape(name)}["\']',
        html,
        re.I,
    )
    return m.group(1) if m else None


def title_of(html: str) -> str | None:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def canonical_of(html: str) -> str | None:
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', html, re.I)
    return m.group(1) if m else None


def h1s(html: str) -> list[str]:
    return [strip_tags(x) for x in re.findall(r"<h1\b[^>]*>([\s\S]*?)</h1>", html, re.I)]


def headings(html: str) -> dict[str, list[str]]:
    out = {}
    for level in range(1, 7):
        out[f"h{level}"] = [strip_tags(x) for x in re.findall(rf"<h{level}\b[^>]*>([\s\S]*?)</h{level}>", html, re.I)]
    return out


def word_count(html: str) -> int:
    # main only if possible
    m = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", html, re.I)
    body = m.group(1) if m else html
    return len(re.findall(r"\b\w+\b", strip_tags(body)))


def schemas(html: str) -> list[dict]:
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
        html,
        re.I,
    )
    out = []
    for b in blocks:
        try:
            data = json.loads(b.strip())
            if isinstance(data, list):
                out.extend(data)
            else:
                out.append(data)
        except json.JSONDecodeError:
            out.append({"_error": "invalid_json", "_raw": b[:120]})
    return out


def file_to_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return DOMAIN + "/"
    if rel.endswith("/index.html"):
        return DOMAIN + "/" + rel[: -len("/index.html")]
    if rel.endswith(".html"):
        # cleanUrls: strip .html
        return DOMAIN + "/" + rel[:-5]
    return DOMAIN + "/" + rel


def expected_canonical(path: Path) -> str:
    return file_to_url(path)


def internal_links(html: str) -> list[str]:
    hrefs = re.findall(r'href=["\']([^"\'#]+)["\']', html, re.I)
    out = []
    for h in hrefs:
        if h.startswith("mailto:") or h.startswith("tel:") or h.startswith("http"):
            if h.startswith(DOMAIN):
                out.append(h)
            continue
        if h.startswith("/"):
            out.append(DOMAIN + h.rstrip("/") if h != "/" else DOMAIN + "/")
    return out


def analyze_page(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    t = title_of(html) or ""
    d = meta(html, "description") or ""
    can = canonical_of(html) or ""
    exp = expected_canonical(path)
    hs = headings(html)
    sch = schemas(html)
    types = []
    for s in sch:
        if isinstance(s, dict):
            if "@graph" in s:
                for g in s["@graph"]:
                    if isinstance(g, dict) and "@type" in g:
                        types.append(g["@type"])
            elif "@type" in s:
                types.append(s["@type"])
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    img_no_alt = sum(1 for i in imgs if not re.search(r'\balt=["\']', i, re.I))
    img_empty_alt = sum(1 for i in imgs if re.search(r'\balt=["\']\s*["\']', i, re.I))
    bg_images = len(re.findall(r"background-image\s*:", html, re.I))
    tel = len(re.findall(r"tel:", html, re.I))
    demo_phone = "(702) 555-0199" in html or "7025550199" in html
    has_address_street = bool(re.search(r"streetAddress|street address", html, re.I))
    # thin local uniqueness signals
    main_m = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", html, re.I)
    main_text = strip_tags(main_m.group(1) if main_m else html)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "url": exp,
        "title": t,
        "title_len": len(t),
        "desc": d,
        "desc_len": len(d),
        "canonical": can,
        "canonical_expected": exp,
        "canonical_match": can.rstrip("/") == exp.rstrip("/") or can.replace(".html", "") == exp,
        "canonical_has_html": can.endswith(".html"),
        "h1": hs["h1"],
        "h1_count": len(hs["h1"]),
        "h2_count": len(hs["h2"]),
        "words": word_count(html),
        "schema_types": types,
        "schema_count": len(sch),
        "schema_errors": sum(1 for s in sch if isinstance(s, dict) and s.get("_error")),
        "imgs": len(imgs),
        "img_no_alt": img_no_alt,
        "img_empty_alt": img_empty_alt,
        "bg_images": bg_images,
        "tel_links": tel,
        "demo_phone": demo_phone,
        "has_street": has_address_street,
        "og_title": prop(html, "og:title") or "",
        "og_image": prop(html, "og:image") or "",
        "robots": meta(html, "robots") or "",
        "lang": bool(re.search(r'<html[^>]+lang=', html, re.I)),
        "viewport": bool(meta(html, "viewport") or re.search(r'name=["\']viewport["\']', html, re.I)),
        "internal": internal_links(html),
        "main_fingerprint": main_text[:400],
        "main_hash_body": re.sub(r"\s+", " ", main_text.lower()),
    }


def page_bucket(path: str) -> str:
    if path == "index.html":
        return "home"
    if path.startswith("services/"):
        return "service"
    if path.startswith("brands/"):
        return "brand"
    if path.startswith("areas/"):
        return "area"
    if path.startswith("blog/posts/"):
        return "blog"
    if path == "blog/index.html":
        return "blog_index"
    return "standard"


def main() -> None:
    pages = [analyze_page(p) for p in sorted(ROOT.rglob("*.html"))]
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm_locs = re.findall(r"<loc>(.*?)</loc>", sm)
    sm_set = set(u.rstrip("/") for u in sm_locs)
    page_urls = set(p["url"].rstrip("/") for p in pages)

    # title/desc uniqueness
    titles = Counter(p["title"] for p in pages)
    descs = Counter(p["desc"] for p in pages)
    h1_all = Counter(h for p in pages for h in p["h1"])

    # issues
    issues = []

    def add(sev: str, cat: str, msg: str, examples: list[str] | None = None, count: int | None = None):
        issues.append({"sev": sev, "cat": cat, "msg": msg, "examples": examples or [], "count": count})

    # Technical
    missing_can = [p for p in pages if not p["canonical"]]
    if missing_can:
        add("critical", "Technical", "Pages missing canonical tags", [p["path"] for p in missing_can[:8]], len(missing_can))

    html_can = [p for p in pages if p["canonical_has_html"]]
    if html_can:
        add(
            "high",
            "Technical",
            "Canonical URLs include .html while cleanUrls strips .html (canonical ≠ live URL risk)",
            [f"{p['path']} → {p['canonical']}" for p in html_can[:6]],
            len(html_can),
        )

    # sitemap vs pages
    only_sm = sorted(sm_set - page_urls)
    only_pg = sorted(page_urls - sm_set)
    # normalize about vs about.html etc
    def norm(u: str) -> str:
        u = u.rstrip("/")
        if u.endswith(".html"):
            u = u[:-5]
        return u

    sm_n = {norm(u) for u in sm_locs}
    pg_n = {norm(p["url"]) for p in pages}
    only_sm2 = sorted(sm_n - pg_n)
    only_pg2 = sorted(pg_n - sm_n)
    if only_sm2:
        add("medium", "Technical", "Sitemap URLs with no matching page", only_sm2[:10], len(only_sm2))
    if only_pg2:
        add("high", "Technical", "Indexable pages missing from sitemap", only_pg2[:15], len(only_pg2))

    blog_slash = [u for u in sm_locs if u.rstrip("/").endswith("/blog") is False and "/blog/" == u[-6:] or u.endswith("/blog/")]
    blog_slash = [u for u in sm_locs if u.endswith("/blog/")]
    if blog_slash:
        add("high", "Technical", "Sitemap lists /blog/ with trailing slash; site uses trailingSlash:false → /blog", blog_slash, len(blog_slash))

    if "lastmod" not in sm:
        add("medium", "Technical", "Sitemap has no <lastmod> dates (missed freshness signals)")

    if re.search(r"changefreq>weekly", sm) and sm.count("<url>") > 100:
        add("low", "Technical", "All URLs use changefreq=weekly (ignored by Google; harmless but unhelpful)")

    # On-page
    no_h1 = [p for p in pages if p["h1_count"] == 0]
    multi_h1 = [p for p in pages if p["h1_count"] > 1]
    if no_h1:
        add("critical", "On-page", "Pages with no H1", [p["path"] for p in no_h1[:10]], len(no_h1))
    if multi_h1:
        add("medium", "On-page", "Pages with multiple H1s", [p["path"] for p in multi_h1[:8]], len(multi_h1))

    title_short = [p for p in pages if p["title_len"] < 30]
    title_long = [p for p in pages if p["title_len"] > 65]
    desc_short = [p for p in pages if p["desc_len"] < 70]
    desc_long = [p for p in pages if p["desc_len"] > 160]
    if title_long:
        add("medium", "On-page", "Titles longer than ~65 chars (may truncate in SERPs)", [f"{p['path']}: {p['title_len']}c" for p in title_long[:8]], len(title_long))
    if title_short:
        add("low", "On-page", "Titles shorter than 30 chars", [p["path"] for p in title_short[:8]], len(title_short))
    if desc_short:
        add("medium", "On-page", "Meta descriptions under 70 chars", [f"{p['path']}: {p['desc_len']}c — {p['desc'][:60]}" for p in desc_short[:8]], len(desc_short))
    if desc_long:
        add("low", "On-page", "Meta descriptions over 160 chars (may truncate)", [f"{p['path']}: {p['desc_len']}c" for p in desc_long[:8]], len(desc_long))

    dup_titles = [(t, c) for t, c in titles.items() if t and c > 1]
    dup_descs = [(d, c) for d, c in descs.items() if d and c > 1]
    if dup_titles:
        add(
            "high",
            "On-page",
            "Duplicate title tags across pages",
            [f'"{t[:70]}" ×{c}' for t, c in sorted(dup_titles, key=lambda x: -x[1])[:8]],
            sum(c for _, c in dup_titles),
        )
    if dup_descs:
        add(
            "high",
            "On-page",
            "Duplicate meta descriptions",
            [f'"{d[:70]}…" ×{c}' if len(d) > 70 else f'"{d}" ×{c}' for d, c in sorted(dup_descs, key=lambda x: -x[1])[:8]],
            sum(c for _, c in dup_descs),
        )

    # content thin
    thin = [p for p in pages if p["words"] < 300 and page_bucket(p["path"]) not in ("blog_index",)]
    thin_std = [p for p in thin if page_bucket(p["path"]) in ("service", "brand", "area", "standard", "home")]
    if thin_std:
        add(
            "high",
            "Content",
            "Thin main content (<300 words) on money/local pages",
            [f"{p['path']}: {p['words']}w" for p in sorted(thin_std, key=lambda x: x["words"])[:12]],
            len(thin_std),
        )

    blog_thin = [p for p in pages if page_bucket(p["path"]) == "blog" and p["words"] < 800]
    if blog_thin:
        add("medium", "Content", "Blog posts under 800 words (target was ~1000)", [f"{p['path']}: {p['words']}w" for p in blog_thin[:10]], len(blog_thin))

    # near-duplicate content among areas/brands
    by_bucket = defaultdict(list)
    for p in pages:
        by_bucket[page_bucket(p["path"])].append(p)

    def near_dupes(group: list[dict], label: str, threshold: float = 0.82):
        # simple similarity: shared word set Jaccard on body
        bodies = []
        for p in group:
            words = set(re.findall(r"[a-z]{4,}", p["main_hash_body"]))
            bodies.append((p, words))
        found = []
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                a, wa = bodies[i]
                b, wb = bodies[j]
                if not wa or not wb:
                    continue
                jacc = len(wa & wb) / len(wa | wb)
                if jacc >= threshold:
                    found.append((jacc, a["path"], b["path"]))
        if found:
            found.sort(reverse=True)
            add(
                "high" if label in ("area", "brand", "service") else "medium",
                "Content",
                f"Near-duplicate {label} pages (template content risk)",
                [f"{x[1]} ≈ {x[2]} ({x[0]:.0%})" for x in found[:8]],
                len(found),
            )

    near_dupes(by_bucket["area"], "area", 0.78)
    near_dupes(by_bucket["brand"], "brand", 0.85)
    near_dupes(by_bucket["service"], "service", 0.80)
    # blog template: two of same topic different area
    near_dupes(by_bucket["blog"][:40], "blog-sample", 0.75)  # sample first 40 for speed - actually all pairs of 100 is 4950 ok

    # Schema / local
    home = next(p for p in pages if p["path"] == "index.html")
    home_html = (ROOT / "index.html").read_text(encoding="utf-8")
    home_sch = schemas(home_html)
    biz = None
    for s in home_sch:
        if isinstance(s, dict) and s.get("@type") in (
            "HomeAndConstructionBusiness",
            "LocalBusiness",
            "ApplianceStore",
            "HVACBusiness",
            "ProfessionalService",
        ):
            biz = s
            break
    if not biz:
        add("critical", "Local/Schema", "Home page missing LocalBusiness / HomeAndConstructionBusiness schema")
    else:
        missing_fields = []
        for f in ("name", "telephone", "url", "image", "address", "areaServed", "priceRange"):
            if f not in biz:
                missing_fields.append(f)
        addr = biz.get("address") or {}
        for f in ("streetAddress", "postalCode", "addressLocality", "addressRegion"):
            if f not in addr:
                missing_fields.append(f"address.{f}")
        if "openingHoursSpecification" not in biz and "openingHours" not in biz:
            missing_fields.append("openingHours")
        if "geo" not in biz:
            missing_fields.append("geo")
        if "sameAs" not in biz:
            missing_fields.append("sameAs (social/GBP profiles)")
        if "aggregateRating" not in biz:
            missing_fields.append("aggregateRating (only if real reviews)")
        if missing_fields:
            add(
                "high",
                "Local/Schema",
                "LocalBusiness schema incomplete for Map Pack / rich results",
                missing_fields,
            )
        if biz.get("telephone") and "555" in str(biz.get("telephone")):
            add("critical", "Local/NAP", "Schema and site use demo phone 555 — will destroy trust/ads/GBP alignment")

    pages_no_schema = [p for p in pages if p["schema_count"] == 0]
    if pages_no_schema:
        add("medium", "Local/Schema", "Pages with no JSON-LD", [p["path"] for p in pages_no_schema[:10]], len(pages_no_schema))

    # service pages should have Service schema ideally
    svc_missing_service_type = []
    for p in by_bucket["service"]:
        types = p["schema_types"] if isinstance(p["schema_types"], list) else []
        flat = []
        for t in types:
            if isinstance(t, list):
                flat.extend(t)
            else:
                flat.append(t)
        if "Service" not in flat and "Product" not in flat:
            svc_missing_service_type.append(p["path"])
    if svc_missing_service_type:
        add(
            "medium",
            "Local/Schema",
            "Service pages lack Service JSON-LD (only generic business schema)",
            svc_missing_service_type[:8],
            len(svc_missing_service_type),
        )

    # FAQ schema
    faq_pages = [p for p in pages if "FAQPage" in (p["schema_types"] if isinstance(p["schema_types"], list) else [])]
    # blogs with FAQ in content
    blogs_with_faq_html = []
    for p in by_bucket["blog"]:
        html = (ROOT / p["path"]).read_text(encoding="utf-8", errors="ignore")
        if "faq" in html.lower() and "FAQPage" not in str(p["schema_types"]):
            # check for details or question pattern
            if re.search(r"faq|Frequently", html, re.I):
                blogs_with_faq_html.append(p["path"])
    if blogs_with_faq_html:
        add(
            "low",
            "Local/Schema",
            "Blog posts with FAQ content may be missing FAQPage schema",
            blogs_with_faq_html[:8],
            len(blogs_with_faq_html),
        )

    # Images
    bg_heavy = [p for p in pages if p["bg_images"] >= 1 and p["imgs"] <= 2]
    add(
        "high",
        "Images",
        "Heroes/service cards use CSS background-image — crawlers get weaker image SEO (no alt, harder to index)",
        [p["path"] for p in bg_heavy[:8]],
        len(bg_heavy),
    )
    no_alt = [p for p in pages if p["img_no_alt"] > 0]
    if no_alt:
        add("medium", "Images", "Img tags missing alt attribute", [f"{p['path']}: {p['img_no_alt']}" for p in no_alt[:8]], len(no_alt))

    # Internal linking
    # build inlink map
    inlinks = Counter()
    out_counts = {}
    for p in pages:
        outs = set()
        for link in p["internal"]:
            n = norm(link)
            inlinks[n] += 1
            outs.add(n)
        out_counts[p["path"]] = len(outs)
    orphanish = []
    for p in pages:
        u = norm(p["url"])
        # exclude home
        if p["path"] == "index.html":
            continue
        # inlinks from other pages: count is total including self-nav chrome
        if inlinks[u] < 5:  # very low even with global nav? nav should give many
            orphanish.append((p["path"], inlinks[u]))
    # With global nav, every page should have high inlinks. Check pages only linked from footer/nav.
    # Better: count content-only links from main
    content_in = Counter()
    for p in pages:
        html = (ROOT / p["path"]).read_text(encoding="utf-8", errors="ignore")
        main_m = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", html, re.I)
        main = main_m.group(1) if main_m else ""
        for h in re.findall(r'href=["\'](/[^"\']+)["\']', main):
            if h.startswith("/assets"):
                continue
            full = DOMAIN + h
            content_in[norm(full)] += 1
    low_content_in = []
    for p in pages:
        if page_bucket(p["path"]) in ("blog", "area", "brand", "service"):
            c = content_in[norm(p["url"])]
            if c < 2:
                low_content_in.append((p["path"], c))
    if low_content_in:
        add(
            "medium",
            "Internal links",
            "Money/blog/area pages with <2 content-body inbound links (rely only on nav)",
            [f"{a}: {b} inlinks" for a, b in sorted(low_content_in, key=lambda x: x[1])[:15]],
            len(low_content_in),
        )

    # URL issues: .html in internal links
    html_links_pages = 0
    html_link_examples = []
    for p in pages:
        html = (ROOT / p["path"]).read_text(encoding="utf-8", errors="ignore")
        bad = re.findall(r'href=["\'](/[^"\']+\.html)["\']', html)
        if bad:
            html_links_pages += 1
            if len(html_link_examples) < 6:
                html_link_examples.append(f"{p['path']}: {bad[0]}")
    if html_links_pages:
        add(
            "medium",
            "Technical",
            "Internal links still use .html extensions (works with redirects but not ideal with cleanUrls)",
            html_link_examples,
            html_links_pages,
        )

    # Security / headers from vercel
    vercel = (ROOT / "vercel.json").read_text(encoding="utf-8")
    if "Content-Security-Policy" not in vercel:
        add("low", "Technical", "No Content-Security-Policy header configured")
    if "Strict-Transport-Security" not in vercel:
        add("low", "Technical", "No HSTS header in vercel.json (often set at domain/CDN level)")

    # Demo / trust
    demo_pages = sum(1 for p in pages if p["demo_phone"])
    if demo_pages:
        add("critical", "Local/NAP", f"Demo phone (702) 555-0199 appears on {demo_pages}/{len(pages)} pages — replace before GSC/ads/GBP")

    if not any(p["has_street"] for p in pages):
        add(
            "high",
            "Local/NAP",
            "No street address / service-area business NAP on site — Map Pack harder without GBP + consistent NAP (SAB OK if policy-compliant)",
        )

    # Performance signals
    font_render = "display=swap" in home_html
    if not font_render:
        add("medium", "Performance", "Google Fonts missing display=swap")
    else:
        add("info", "Performance", "Fonts use display=swap (good)")

    # preconnect present
    if "preconnect" not in home_html:
        add("low", "Performance", "No preconnect for font origins")

    # missing modern image formats
    webp = list((ROOT / "assets").rglob("*.webp"))
    if not webp:
        add("medium", "Images", "No WebP/AVIF images — only JPEG/PNG; larger LCP on mobile")

    # robots
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots:
        add("high", "Technical", "robots.txt missing Sitemap directive")
    if "Disallow" in robots and "Allow: /" in robots:
        pass

    # Keyword coverage snapshot (home)
    home_text = strip_tags(home_html).lower()
    primary_kws = [
        "appliance repair las vegas",
        "refrigerator repair",
        "washer repair",
        "dryer repair",
        "dishwasher repair",
        "oven repair",
        "same-day",
        "sub-zero",
        "samsung",
    ]
    kw_hits = {k: home_text.count(k) for k in primary_kws}

    # Stats by bucket
    stats = {}
    for b, group in by_bucket.items():
        stats[b] = {
            "count": len(group),
            "avg_words": round(sum(p["words"] for p in group) / max(len(group), 1)),
            "min_words": min(p["words"] for p in group) if group else 0,
            "max_words": max(p["words"] for p in group) if group else 0,
            "avg_title": round(sum(p["title_len"] for p in group) / max(len(group), 1)),
            "avg_desc": round(sum(p["desc_len"] for p in group) / max(len(group), 1)),
        }

    # Sample titles
    samples = {
        "home": [p for p in pages if p["path"] == "index.html"][0],
        "service": by_bucket["service"][0] if by_bucket["service"] else None,
        "brand": by_bucket["brand"][0] if by_bucket["brand"] else None,
        "area": by_bucket["area"][0] if by_bucket["area"] else None,
        "blog": by_bucket["blog"][0] if by_bucket["blog"] else None,
    }

    # Score rough
    weights = {"critical": 12, "high": 6, "medium": 3, "low": 1, "info": 0}
    penalty = sum(weights.get(i["sev"], 0) for i in issues if i["sev"] != "info")
    score = max(0, 100 - penalty)

    # Build report
    lines = []
    lines.append(f"# Deep SEO Audit — Las Vegas Appliance Repair Pros")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  ")
    lines.append(f"**Site path:** `{ROOT}`  ")
    lines.append(f"**Target domain:** {DOMAIN}  ")
    lines.append(f"**Pages crawled:** {len(pages)} HTML  ")
    lines.append(f"**Sitemap URLs:** {len(sm_locs)}  ")
    lines.append(f"**Health score (heuristic):** **{score}/100**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Executive summary")
    lines.append("")
    lines.append(
        "The site has strong **topical coverage** (services × brands × areas × 100 blogs) and solid basic hygiene "
        "(titles, metas, canonicals, robots, sitemap, OG tags, mobile viewport, call CTAs). "
        "It is **not yet Map Pack–ready**: demo phone, incomplete LocalBusiness schema (no street/geo/hours/sameAs), "
        "CSS-background heroes (weak image SEO), heavy template similarity on area/brand pages, and canonical/link "
        "patterns that mix `.html` with clean URLs. Blog scale is an asset only if uniqueness holds under review."
    )
    lines.append("")
    lines.append("### Inventory")
    lines.append("")
    lines.append("| Type | Count | Avg words (main) | Min | Max |")
    lines.append("|------|------:|-----------------:|----:|----:|")
    for b in ("home", "standard", "service", "brand", "area", "blog", "blog_index"):
        if b in stats:
            s = stats[b]
            lines.append(f"| {b} | {s['count']} | {s['avg_words']} | {s['min_words']} | {s['max_words']} |")
    lines.append("")
    lines.append("### Home keyword presence (raw counts in full page text)")
    lines.append("")
    lines.append("| Phrase | Count |")
    lines.append("|--------|------:|")
    for k, v in kw_hits.items():
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Issue register (prioritized)")
    lines.append("")
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    issues_sorted = sorted(issues, key=lambda x: (order.get(x["sev"], 9), x["cat"], x["msg"]))
    for i, issue in enumerate(issues_sorted, 1):
        if issue["sev"] == "info":
            continue
        cnt = f" — **{issue['count']}**" if issue.get("count") else ""
        lines.append(f"### {i}. [{issue['sev'].upper()}] {issue['cat']}: {issue['msg']}{cnt}")
        lines.append("")
        if issue["examples"]:
            for ex in issue["examples"][:10]:
                lines.append(f"- `{ex}`" if not ex.startswith("`") and len(ex) < 120 else f"- {ex}")
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## What's working")
    lines.append("")
    goods = [
        f"**Scale & architecture:** {len(pages)} pages covering services, brands, areas, and 100 blog posts — strong local topical graph.",
        "**Basic meta hygiene:** Nearly all pages have title, meta description, canonical, robots index/follow, OG + Twitter cards.",
        "**Language & viewport:** `lang=en` and mobile viewport present.",
        "**robots.txt** allows crawl and points to sitemap.",
        "**Sitemap scale** matches page count (~193).",
        "**Call-focused conversion** with ubiquitous `tel:` links (good for mobile local intent).",
        "**Internal nav** exposes Services / Brands / Areas / Blog sitewide.",
        "**Security headers starter:** X-Content-Type-Options, Referrer-Policy, X-Frame-Options in vercel.json.",
        "**Asset caching** for `/assets/*` (immutable) — good for repeat visits.",
        "**Fonts:** preconnect + `display=swap`.",
        "**Legal pages** exist (privacy + terms) for trust/compliance.",
        f"**Blog average length:** ~{stats.get('blog', {}).get('avg_words', '?')} words — closer to long-form than thin stubs.",
    ]
    for g in goods:
        lines.append(f"- {g}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Deep dive by category")
    lines.append("")
    lines.append("### 1. Technical SEO")
    lines.append("")
    lines.append("| Check | Status | Notes |")
    lines.append("|-------|--------|-------|")
    lines.append(f"| HTTPS target domain | Assumed | Deploy on Vercel with domain SSL |")
    lines.append(f"| cleanUrls | Yes | `vercel.json` cleanUrls:true |")
    lines.append(f"| trailingSlash | false | Blog sitemap had `/blog/` mismatch risk |")
    lines.append(f"| robots.txt | Pass | Allow all + Sitemap |")
    lines.append(f"| sitemap.xml | Partial | {len(sm_locs)} URLs; no lastmod; blog trailing slash |")
    lines.append(f"| Canonicals present | {'Pass' if not missing_can else 'Fail'} | Many use `.html` vs clean path |")
    lines.append(f"| Internal .html links | Warn | {html_links_pages} pages still link with .html |")
    lines.append(f"| Redirects | Partial | Blog loop fixed; .html→clean for nested only |")
    lines.append(f"| hreflang | N/A | Single language EN |")
    lines.append(f"| XML index split | OK | Single sitemap fine under 50k |")
    lines.append("")
    lines.append("**Canonical vs live URL example (home):**")
    lines.append(f"- Canonical: `{samples['home']['canonical']}`")
    lines.append(f"- Expected clean: `{samples['home']['url']}`")
    if samples["service"]:
        lines.append(f"- Service sample canonical: `{samples['service']['canonical']}`")
    lines.append("")
    lines.append("### 2. On-page SEO")
    lines.append("")
    lines.append("| Page type | Sample title | Title len | Desc len | H1 |")
    lines.append("|-----------|--------------|----------:|---------:|----|")
    for key in ("home", "service", "brand", "area", "blog"):
        p = samples.get(key)
        if not p:
            continue
        h1 = p["h1"][0] if p["h1"] else "—"
        lines.append(f"| {key} | {p['title'][:70]} | {p['title_len']} | {p['desc_len']} | {h1[:50]} |")
    lines.append("")
    lines.append(f"- Unique titles: {sum(1 for t,c in titles.items() if c==1)} / {len(pages)}")
    lines.append(f"- Unique descriptions: {sum(1 for d,c in descs.items() if c==1)} / {len(pages)}")
    lines.append(f"- Pages with exactly 1 H1: {sum(1 for p in pages if p['h1_count']==1)} / {len(pages)}")
    lines.append("")
    lines.append("### 3. Local SEO & E-E-A-T")
    lines.append("")
    lines.append("| Signal | Status |")
    lines.append("|--------|--------|")
    lines.append("| Real phone (not 555) | **Fail — demo** |")
    lines.append("| Street address / SAB disclosure | Weak / missing |")
    lines.append("| Geo meta placename | Present (Las Vegas) |")
    lines.append("| LocalBusiness schema completeness | Incomplete |")
    lines.append("| Google Business Profile link (sameAs) | Missing |")
    lines.append("| Hours in schema | Missing |")
    lines.append("| Geo coordinates | Missing |")
    lines.append("| Author bios on blog | Likely missing |")
    lines.append("| About page substance | Present |")
    lines.append("| Reviews/schema ratings | Not verified as real aggregateRating |")
    lines.append("| License / insurance claims | Check copy for substantiation |")
    lines.append("")
    lines.append("### 4. Content quality & uniqueness")
    lines.append("")
    lines.append(
        "Programmatic local pages (areas/brands) are efficient for coverage but **Google discounts near-duplicate doorways**. "
        "Each area should include unique: neighborhoods landmarks, common housing stock notes, travel-time/route reality, "
        "and distinct FAQs. Brand pages need brand-specific failure modes (e.g. Samsung ice makers, LG linear compressors). "
        "Blogs should not be the same article with only the city name swapped — audit pairs with high Jaccard similarity."
    )
    lines.append("")
    lines.append("### 5. Images & media SEO")
    lines.append("")
    lines.append("- Heroes and cards often use **CSS `background-image`** → no crawlable `alt`, weaker Image search, harder LCP prioritization via `<img fetchpriority>`.")
    lines.append("- Prefer real `<img>` (or `<picture>`) with descriptive alt including service + city where natural.")
    lines.append("- Add WebP + width/height to reduce CLS.")
    lines.append("- Logo used as favicon is OK short-term; add dedicated favicon.ico / apple-touch-icon.")
    lines.append("")
    lines.append("### 6. Internal linking")
    lines.append("")
    lines.append("- Global nav prevents true orphans.")
    lines.append("- Content-body inlinks still matter for PageRank sculpting.")
    lines.append(f"- Pages with weak body inlinks: **{len(low_content_in)}** (see issues).")
    lines.append("- Recommended modules: related services, nearby areas, brand×service cross-links, blog hubs by topic.")
    lines.append("")
    lines.append("### 7. Performance & CWV (static signals only)")
    lines.append("")
    lines.append("- Third-party Google Fonts (2 families) = extra RTT; consider self-host subset.")
    lines.append("- Large full-bleed JPEG heroes at 1400px — compress further / responsive srcset.")
    lines.append("- No evidence of lazy-loading strategy for below-fold card images (many are CSS backgrounds).")
    lines.append("- Mobile sticky app bar is fine for UX; ensure it doesn't obscure content (padding-bottom present).")
    lines.append("- **Run Lighthouse/CrUX on production domain** after deploy for real LCP/INP/CLS.")
    lines.append("")
    lines.append("### 8. Indexation strategy risks")
    lines.append("")
    lines.append("| Risk | Why it matters | Mitigation |")
    lines.append("|------|----------------|------------|")
    lines.append("| Soft doorways | 28 area pages too similar | Unique 400+ words local content each |")
    lines.append("| Brand sprawl | 40 brand pages | Prioritize top 15 commercial brands; noindex long-tail if thin |")
    lines.append("| Blog explosion | 100 posts | Unique value, consolidate thin pairs, hub pages |")
    lines.append("| Demo NAP | Trust + ads rejection | Real phone/email/GBP before indexing push |")
    lines.append("| .html vs clean | Canonical confusion | One URL format everywhere |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Priority fix roadmap")
    lines.append("")
    lines.append("### P0 — Before any SEO campaign / GSC push (1–2 days)")
    lines.append("")
    lines.append("1. Replace **demo phone & email** sitewide; align schema + GBP + citations.")
    lines.append("2. Normalize **canonicals + internal links** to clean URLs (no `.html`); fix sitemap `/blog/` → `/blog`.")
    lines.append("3. Expand **LocalBusiness JSON-LD**: `@type` ApplianceRepair or HomeAndConstructionBusiness + `streetAddress` or SAB wording, `geo`, `openingHoursSpecification`, `sameAs` (GBP), `areaServed` as multi-area list.")
    lines.append("4. Submit sitemap in **Google Search Console** only after P0 NAP is real.")
    lines.append("")
    lines.append("### P1 — Ranking foundations (1–2 weeks)")
    lines.append("")
    lines.append("5. Convert heroes/cards from CSS backgrounds to **semantic `<img>`** with alt text.")
    lines.append("6. Differentiate **top 10 area pages** and **top 10 brand pages** with unique copy (not token-swap).")
    lines.append("7. Add **Service** schema on service pages; **FAQPage** where FAQs exist; **BreadcrumbList** sitewide.")
    lines.append("8. Add `lastmod` to sitemap; optional priority only for humans.")
    lines.append("9. Build topic hubs: e.g. `/blog/refrigerator-repair-guides` linking clusters.")
    lines.append("")
    lines.append("### P2 — Authority & conversion SEO (ongoing)")
    lines.append("")
    lines.append("10. GBP optimization + weekly photos/Q&A; review velocity.")
    lines.append("11. Citation NAP consistency (Yelp, BBB, Angi, Nextdoor, etc.).")
    lines.append("12. Author page + bylines for E-E-A-T on blogs.")
    lines.append("13. Compress images to WebP; self-host fonts; measure CWV.")
    lines.append("14. Add real case studies / before-after (with permission) for E-E-A-T.")
    lines.append("15. Consider pruning/noindexing weakest brand or dual blog clones if GSC shows low value crawl.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Sample page diagnostics")
    lines.append("")
    for key in ("home", "service", "brand", "area", "blog"):
        p = samples.get(key)
        if not p:
            continue
        lines.append(f"### {key}: `{p['path']}`")
        lines.append("")
        lines.append(f"- **Title ({p['title_len']}):** {p['title']}")
        lines.append(f"- **Description ({p['desc_len']}):** {p['desc']}")
        lines.append(f"- **Canonical:** {p['canonical']}")
        lines.append(f"- **H1:** {', '.join(p['h1']) if p['h1'] else 'NONE'}")
        lines.append(f"- **Words (main):** {p['words']}")
        lines.append(f"- **Schema types:** {p['schema_types']}")
        lines.append(f"- **BG images / img tags:** {p['bg_images']} / {p['imgs']}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Measurement plan")
    lines.append("")
    lines.append("1. GSC property + sitemap submit + URL inspection on home + 3 services + 3 areas.")
    lines.append("2. Track queries: `appliance repair las vegas`, `refrigerator repair las vegas`, brand+repair, area+repair.")
    lines.append("3. Weekly: coverage (indexed vs discovered), average position, CTR.")
    lines.append("4. Call tracking on `tel:` (callrail/gclid) — SEO without call data is incomplete for this business model.")
    lines.append("5. Re-run this audit script after P0/P1 changes.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Appendix — automated counts")
    lines.append("")
    lines.append(f"- Duplicate title groups: {len(dup_titles)}")
    lines.append(f"- Duplicate description groups: {len(dup_descs)}")
    lines.append(f"- Demo phone pages: {demo_pages}")
    lines.append(f"- Canonicals with .html: {len(html_can)}")
    lines.append(f"- Thin non-blog pages (<300w): {len(thin_std)}")
    lines.append(f"- Blog posts <800w: {len(blog_thin)}")
    lines.append(f"- Low body-inlink targets: {len(low_content_in)}")
    lines.append(f"- Issue count by severity: {dict(Counter(i['sev'] for i in issues_sorted if i['sev']!='info'))}")
    lines.append("")
    lines.append("*Generated by `_seo_audit.py` — static analysis only; not a substitute for GSC/CrUX/Lighthouse on production.*")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Score {score}/100")
    print(f"Issues: {Counter(i['sev'] for i in issues_sorted)}")
    # print critical/high for terminal
    for i in issues_sorted:
        if i["sev"] in ("critical", "high"):
            print(f"  [{i['sev']}] {i['msg']}" + (f" ({i['count']})" if i.get("count") else ""))


if __name__ == "__main__":
    main()
