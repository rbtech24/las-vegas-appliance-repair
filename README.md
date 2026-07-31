# Las Vegas Appliance Repair Pros

Ultimate local appliance-repair static site for Las Vegas, NV.

## Brand
- **Name:** Las Vegas Appliance Repair Pros
- **Domain:** https://www.lasvegasappliancerepairpros.com
- **Phone (demo):** (725) 215-1313 — replace before launch / GBP / ads
- **Email:** hello@lasvegasappliancerepairpros.com
- **Logo:** `assets/images/logo.png` (from Downloads)

## Page counts
- Standard: home, about, contact, pricing, faq, privacy, terms, services hub, brands hub, areas hub, blog index
- Services: 14
- Brands: 40
- Areas: 28
- Blog posts: 100 (~1000+ words, image, interlinking)

## Deploy on Vercel

Static HTML site — **no build step**. Deploy the folder as-is.

```powershell
cd C:\Users\rodba\las-vegas-appliance-repair
npx vercel login
npx vercel          # preview
npx vercel --prod   # production
```

**CLI prompts:** set the directory to `.` (this folder), Framework Preset = **Other**, no build command, output = current directory.

**Custom domain (dashboard or CLI):**
```powershell
npx vercel domains add lasvegasappliancerepairpros.com
```
Then point DNS (A/CNAME) as Vercel shows.

**After go-live:** submit `https://YOUR-DOMAIN/sitemap.xml` in Google Search Console.

## Replace before marketing
1. Phone / email / NAP
2. Connect contact form
3. Google Business Profile
4. Real reviews (no fake AggregateRating)
