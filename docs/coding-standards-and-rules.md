# coding-standards-and-rules.md

## 1. Repo structure

```
/repo
  run.py                # Unified launcher for full stack
  /backend
    /node_service       # District Node Service (FastAPI / Port 8000)
      /gemini_engine    # Shared Gemini AI Engine (5 Jobs, Key Pool, Schemas)
        key_pool.py
        schemas.py
        prompts.py
        engine.py
      local_store.py    # Local-only victim case repository & SHA-256 hashing
      main.py           # Twilio webhooks, PWA check-in, federated push
    /aggregator_service # National Aggregator Service (FastAPI / Port 9000)
      national_view.py  # Strict privacy filter & Pan-India rollups
      main.py           # Dashboard polling API & officer workflows
    run_all.py          # Backend dual-service runner
  /frontend             # Comforting Glassmorphic PWA Frontend
    index.html          # 4 Viewports (Saathi, District, National, Sandbox)
    styles.css          # Design system, soothing theme, animations
    app.js              # Web Speech voice I/O, 3s polling, demo injector
    manifest.json       # PWA manifest
    sw.js               # Service Worker for offline capability
  /test_data            # Synthetic multilingual check-in test suite
    scripts.md
  /docs                 # Architecture, engineering contracts, and assignment docs
```

## 2. Naming conventions

- Python: `snake_case` for functions/variables, `PascalCase` for schema/class names (`DistressSchema`, `GeminiKeyPool`)
- Env vars: `SCREAMING_SNAKE_CASE` (`GEMINI_API_KEYS`, `TWILIO_AUTH_TOKEN`, `NODE_ID`, `AGGREGATOR_URL`)
- Endpoints: lowercase, hyphen-free, verb-free where possible (`/dashboard/summary`, not `/get-dashboard-summary`)
- Node IDs: `district_<name>` (e.g. `district_pune`) — consistent across code, logs, and dashboard display

## 3. Git workflow (hackathon-speed version)

- One shared repo, branch per person: `aryan/`, `advay/`, `netal/`
- Commit early, commit often — a broken intermediate commit is fine during a hackathon, an unpushed hour of work is not
- Merge to `main` at natural checkpoints: end of the "one working vertical slice" milestone, end of Round 1, and continuously through Round 2
- Commit message format: `[component] short description` — e.g. `[gemini-engine] add key pool cooldown logic`, `[frontend] alert banner polling`
- If your change touches `api-contracts.md`'s documented shape, update that doc in the **same commit**

## 4. Environment variables (finalize the list night-before)

```
GEMINI_API_KEYS=key1,key2,...,key15
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
TWILIO_VOICE_NUMBER=
NODE_ID=district_pune          # different per node instance
AGGREGATOR_URL=http://localhost:9000
DISTRESS_ALERT_THRESHOLD=70
```

Never commit a `.env` file with real values. `.env.example` with placeholder values goes in the repo; real `.env` stays local and in `.gitignore`.

## 5. Testing bar for a hackathon (be honest about what "tested" means here)

- Every Gemini-calling function gets manually run against at least 2 of Netal's synthetic scripts before Round 1 ends — one low-distress, one high-distress
- No unit test suite expected given the timeline — manual verification, logged in a shared doc/chat, is acceptable
- Before the demo, run the full happy path (WhatsApp message → score → dashboard update → threshold breach → alert) at least twice end-to-end, not just per-component

## 6. Communication cadence during the hackathon

- Quick sync at the start of Round 2 (1:30 PM) — confirm the Round 1 vertical slice actually works before building on top of it
- Anyone blocked for more than 15 minutes says so immediately rather than quietly falling behind — the timeline in `context.md` §4 has no slack built in
- 30 minutes before judging: feature freeze, move straight to demo rehearsal per `CLAUDE.md` §5

## 7. What "done" means for a component, in this hackathon

A component is done when it works in the live demo path, not when it's "clean." Refactoring for elegance is explicitly deprioritized below "does the judge-facing demo work reliably" — this is a deliberate, stated trade-off, not sloppiness.
