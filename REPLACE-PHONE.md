# Replace demo phone before launch

Edit **`site_config.json`**:

```json
"phone_display": "(702) XXX-XXXX",
"phone_raw": "702XXXXXXX"
```

Then run a project-wide replace:

- Display form: `(702) 555-0199` → your display number  
- Raw/tel form: `7025550199` → digits only  
- Also update `build_lvar_site.py` constants if you regenerate pages  

Add your Google Business Profile URL to `sameAs` in `site_config.json` and re-run schema injection or tell the agent to refresh schema.

**Do not run ads or claim GBP until the real number is live on every page.**
