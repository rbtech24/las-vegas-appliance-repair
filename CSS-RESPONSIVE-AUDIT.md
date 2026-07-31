# Full CSS & Responsive Audit — Las Vegas Appliance Repair Pros

**Date:** 2026-07-30  
**CSS:** `assets/css/styles.css` (rewritten for responsive fixes)  
**JS:** `assets/js/main.js` (mobile menu accordion)

---

## Executive summary

| Area | Grade before fixes | After fixes (this pass) |
|------|--------------------|-------------------------|
| Desktop layout | B | B+ |
| Tablet (768–1040) | D | B |
| Mobile (&lt;640) | F | B |
| Mobile nav | F (broken UX) | B |
| App bar | D (easy to “lose”) | B |
| Hero / images | D (blue square) | B |
| Breadcrumbs (visible) | C– (easy to miss) | B |
| CSS maintainability | C (duplicate rules) | B |

---

## Why no breadcrumbs? (answered)

**They were already on most interior pages** — but easy to think they were “missing”:

| What | Status |
|------|--------|
| **Visual** `div.breadcrumb` | On services, brands, areas, blog posts, about, contact, pricing, FAQ, hubs, legal |
| **Home** | No visual trail (correct — you’re already Home) |
| **JSON-LD** `BreadcrumbList` | On money pages + many hubs |
| **Why invisible?** | Trails lived **inside the dark hero** with low-contrast white/gray text; on some viewports the hero image/`height:auto` fight left a **solid navy block** so crumbs looked like empty hero chrome, not navigation |

**Contrast fix:** breadcrumbs now use gold underlined links (`#ffd084`) on the hero gradient so they read as a trail.

**Example (service page):**  
`Home / Services / Refrigerator Repair`

**Schema example:**  
`BreadcrumbList` → Home → Services → [page]

Home still has schema with only “Home” from an earlier SEO pass — harmless; visual trail stays off on home.

---

## Critical bugs found (and fixed)

### 1. Mobile menu not responsive
**Root causes:**
- Logo at **84–100px tall** + wide wordmark squeezed hamburger and “Call Now”
- All three mega-dropdowns forced **always open** (`display:block`) on ≤1040px → unusable scroll trap
- Open panel `z-index` too low vs sticky header stacking
- No body scroll lock, no accordion, no Escape/close-on-link

**Fixes:**
- Smaller mobile logo (`52px`, max-width ~52vw)
- Hide header “Call Now” on ≤1040 (call lives on app bar)
- Dropdowns **collapsed by default**; tap parent to accordion
- Drawer `z-index: 1100`, body `nav-open` overflow lock
- JS: toggle, accordion, Escape, resize cleanup

### 2. Mobile app bar “gone”
**Root causes:**
- `z-index: 1001` could lose to other layers; not forced visible
- Footer padding competed; call FAB could clip
- Perception: dark bar on dark footer + hidden by broken menu

**Fixes:**
- `z-index: 2000` + `display: block !important` under 860px
- Clearer safe-area + body padding for app bar height
- Slightly larger call FAB

### 3. Home blank blue square
**Root causes:**
- Global `img { max-width:100%; height:auto }` fought absolute hero fill
- `.hero { background:#081428 }` showed when image didn’t cover
- Hero min-height 76vh with non-covering img → solid navy “square/block”

**Fixes:**
- `.hero-img` / `.page-hero-img`: `height/width 100% !important`, `max-width:none !important`, `object-fit:cover`
- Mobile hero min-height reduced to ~58vh
- Full-width CTAs on small screens

### 4. CSS self-conflicts
**Found:**
- `.pill` / `.brand-pill` redefined twice (chip vs grid tile) — last rules won unpredictably
- Duplicate `.page-hero` / `.hero` blocks (background CSS var vs img overlay)
- Duplicate `.blog-hero-img` rules

**Fix:** single coherent stylesheet, chips vs `.brand-grid .brand-pill` separated

---

## Breakpoint map (current)

| Max width | Intent |
|----------:|--------|
| 1100px | Show desktop header phone |
| 1040px | Hamburger nav, hide header Call btn |
| 900px | 1-col cards/split, 2-col footer |
| 860px | Hide topbar; show mobile app bar |
| 640px | Stack form cols; full-width hero CTAs |
| 560px | 1-col footer |
| 520px | 1-col trust + brand grid |

---

## Component audit

### Header
| Check | Status |
|-------|--------|
| Sticky | Yes |
| Logo overflow | Fixed (min-width:0, max-width) |
| Touch targets ≥44px | Hamburger yes; nav links padded on mobile |
| Focus states | Partial (browser default) — improve later |

### Navigation
| Check | Status |
|-------|--------|
| Desktop hover dropdowns | Yes |
| Mobile accordion | Yes (after fix) |
| Keyboard Escape | Yes |
| Mega-list length | Still long (14 services) — acceptable with scroll |

### Hero / page-hero
| Check | Status |
|-------|--------|
| Semantic img | Yes |
| Cover without blue block | Fixed |
| Text contrast | Overlay gradient helps |
| Breadcrumbs readable | Gold links after fix |

### Grids
| Component | Desktop | Mobile |
|-----------|---------|--------|
| cards-3 | 3 | 1 |
| trust-bar | 4 | 2 → 1 |
| brand-grid | 4 | 2 → 1 |
| footer | 4 | 2 → 1 |
| split | 2 | 1 |

### Typography
| Check | Status |
|-------|--------|
| Fluid type (clamp) | Hero H1, section titles |
| Base 17px | OK; consider 16px mobile later |
| Bebas Neue long titles | Can wrap tightly — monitor |

### App bar
| Check | Status |
|-------|--------|
| Phone only ≤860 | Yes |
| 3 items Home/Call/Areas | Yes |
| Safe area | Yes |
| Active state | JS path match |

### Forms
| Check | Status |
|-------|--------|
| Forms removed sitewide | Yes (call-only) |
| Residual form CSS | Harmless dead CSS |

### A11y / motion
| Check | Status |
|-------|--------|
| `prefers-reduced-motion` | Added |
| `aria-expanded` on menu | Yes |
| Skip link | Missing (P2) |
| Focus ring on buttons | Weak (P2) |

---

## Performance / CSS quality notes

| Issue | Severity | Note |
|-------|----------|------|
| Google Fonts remote | Medium | Extra RTT; self-host later |
| Single large CSS file | Low | Fine at this size |
| No critical CSS | Low | Static host OK |
| JPEG heroes only | Medium | WebP later |
| `box-shadow: var(--glow)` removed from split-media | Low | Glow was decorative |

---

## Breadcrumb product guidance

| Page type | Visual breadcrumb | Schema |
|-----------|-------------------|--------|
| Home | No | Optional / Home only |
| Service / Brand / Area | Yes (hero) | Yes multi-level |
| Blog post | Yes | Yes |
| Legal / About / Contact | Yes | Yes |
| Blog index | Yes | Yes |

If you want breadcrumbs **below the white header** (always visible, not on photo), we can add a `.breadcrumb-bar` strip sitewide in a follow-up.

---

## Manual test checklist (do on phone or DevTools)

1. **iPhone SE / 375px:** open hamburger → Services expands only when tapped → link navigates → menu closes  
2. **App bar** pinned: Home / Call / Areas visible above home indicator  
3. **Home hero** shows kitchen photo, not solid navy block  
4. **Service page:** gold `Home / Services / …` trail visible under header area of hero  
5. **Landscape phone:** menu scrollable, app bar still usable  
6. **Tablet 900px:** cards single column, nav still hamburger until 1041  

---

## Remaining P2 (not blockers)

1. Skip-to-content link  
2. Visible `:focus-visible` rings on all interactive controls  
3. Collapse service dropdown to “top 6 + View all” on mobile  
4. Self-host fonts + WebP heroes  
5. Optional always-on breadcrumb bar under header  
6. Test on real iOS Safari (sticky + 100vh quirks)

---

## Files changed this pass

- `assets/css/styles.css` — full responsive rewrite  
- `assets/js/main.js` — mobile nav accordion + body lock  
- `CSS-RESPONSIVE-AUDIT.md` — this document  
