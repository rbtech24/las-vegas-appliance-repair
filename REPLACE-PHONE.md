# Replace phone before launch

Edit **`site_config.json`**:

```json
"phone_display": "(702) XXX-XXXX",
"phone_raw": "702XXXXXXX"
```

Then run a project-wide replace:

- Display form: `(725) 215-1313` → your display number  
- Raw/tel form: `7252151313` → digits only  
- Also update `build_lvar_site.py` constants if you regenerate pages  

Add your Google Business Profile URL to `sameAs` in `site_config.json` and re-run schema injection or tell the agent to refresh schema.

**Do not run ads or claim GBP until the real number is live on every page.**
