# Done Waiting — Protect Our Schools

Codex connected on 2025-09-08 — repo ready.

## Overview
Static site on Netlify for the petition and a Cloudflare Worker API for /api/sign and /api/count.

## Project Structure
- public/index.html — petition page (form posts to https://api.donewaiting.us/api/sign?redirect=https://donewaiting.us/thank-you.html)
- public/thank-you.html — share/CTA page
- src/worker.mjs — Cloudflare Worker (handles sign + count)
- wrangler.toml — Worker config (no secrets)
- netlify.toml — Netlify config (if present)

## Env & Secrets
Non-secret env:
- ALLOW_ORIGINS = https://donewaiting.us,https://www.donewaiting.us
- TURNSTILE_SITEKEY = <public_site_key>

Secrets (never in files; set in Worker/Codex):
- TURNSTILE_SECRET
- CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
- NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID
