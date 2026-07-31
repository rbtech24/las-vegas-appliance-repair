# SEO fixes applied (phone still placeholder)

**Date:** 2026-07-30  
**Phone:** still demo `(725) 215-1313` — swap later via `site_config.json` (see `REPLACE-PHONE.md`).

## 1) Technical SEO
- All internal links + canonicals normalized to **clean URLs** (no `.html`)
- **Sitemap** rebuilt: 193 URLs, `<lastmod>`, `/blog` not `/blog/`
- Remaining `.html` href count: **0**

## 2) Local schema (ready for real NAP)
- `LocalBusiness` + `HomeAndConstructionBusiness` with `@id`
- **Geo** (Las Vegas center), **opening hours**, **28 areaServed** places
- Service-area business wording (no fake street address)
- **Service** + **BreadcrumbList** on service/brand/area pages
- `sameAs: []` in `site_config.json` — add GBP URL when ready

## 3) Image SEO
- Home hero + page heroes use real **`<img>`** (not only CSS background)
- Service/aside cards use `<img>` with alts
- CSS supports `.hero-img` / `.page-hero-img`

## 4) Content uniqueness
| Layer | Approx. avg main words (after) |
|--------|--------------------------------:|
| Services (14) | ~470+ |
| Brands (40) | ~400 |
| Areas (28) | ~410 |
| Unique symptoms, local desert notes, FAQs, repair-vs-replace, booking steps |

## When you have the real phone
1. Edit `site_config.json` → `phone_display` + `phone_raw`
2. Project-wide replace old display + tel digits
3. Optionally add GBP to `sameAs`
4. Re-run `_apply_seo_upgrades.py` **or** ask the agent to re-inject schema
5. Then GSC + ads + GBP

## Files of note
- `site_config.json` — single config source for NAP-ish fields
- `REPLACE-PHONE.md` — swap instructions
- `_apply_seo_upgrades.py` — re-runnable upgrade script
- `SEO-AUDIT.md` — original deep audit
