# system-overview.md

## 1. Component diagram

```
                     ┌─────────────────────────────────────────┐
                     │           INPUT CHANNELS                │
                     │  WhatsApp (Twilio)   Voice Call (Twilio)│
                     │     Aanchal Saathi PWA (Web Check-in)   │
                     └───────────────┬─────────────────────────┘
                                     │  raw text/speech-to-text
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │       DISTRICT NODE SERVICE (`backend/node_service`)   │
        │  - Owns raw case history for its victims (LOCAL ONLY)  │
        │  - Calls Gemini Engine for structured distress scoring │
        │  - Long-context: full history stays IN this service    │
        │  - Runs function-calling alert trigger locally         │
        └───────────────┬────────────────────────────────────────┘
                        │  ONLY: {node_id, hashed_case_id, score_data}
                        │  NEVER: raw transcript, real victim identity
                        ▼
        ┌────────────────────────────────────────────────────────┐
        │     AGGREGATOR SERVICE (`backend/aggregator_service`)  │
        │  - Receives anonymized scores only (Strict Firewall)   │
        │  - Builds district / state / national rollups          │
        │  - Serves dashboard API & officer action workflows     │
        └───────────────┬────────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────────────┐
        │            FRONTEND DASHBOARD (`frontend/`)            │
        │   Aanchal Saathi PWA · District Desk · National MoSJE  │
        │   Live alert banner on threshold breach (>70)          │
        └────────────────────────────────────────────────────────┘

        ┌────────────────────────────────────────────────────────┐
        │        GEMINI AI ENGINE (`node_service/gemini_engine`) │
        │   - 15-key pool w/ round-robin + cooldown failover     │
        │   - Structured output (DistressSchema)                 │
        │   - Long-context baseline trajectory reasoning         │
        │   - Function calling (trigger_alert)                   │
        │   - Grounded POA Act 1989 scheme recommendations       │
        └────────────────────────────────────────────────────────┘
```

## 2. Why this shape

- **Node service is where all sensitive reasoning happens.** It is the only service that ever sees raw victim input. This is deliberate and is the entire privacy story — see `privacy-rules.md`.
- **Aggregator never calls Gemini.** It only receives already-computed, already-anonymized scores. This makes the privacy boundary a literal network boundary, not just a policy — easy to explain to judges, easy to point at in code.
- **Gemini Engine is a shared library, not a service.** Both the node service and (only) the node service import it directly. Keeping it a library (not a network hop) means one less thing that can leak data over the wire.

## 3. Data flow for a single interaction (end to end)

1. Victim sends WhatsApp message, speaks on a call, or uses the PWA → hits the relevant webhook on the **District Node service** (`api-contracts.md` §1-2)
2. Node service loads that victim's local history (if any), builds a long-context prompt (`gemini-engine.md` §3), calls Gemini Engine
3. Gemini Engine picks an available key from the pool, returns structured JSON matching `DistressSchema`
4. Node service appends this interaction + score to **local** history (`local_case_history`, never serialized outward)
5. Node service hashes the victim's channel ID (phone number → SHA-256), pushes `{node_id, hashed_case_id, score_data}` to the aggregator's `/federated/push_score` endpoint
6. If `distress_score >= DISTRESS_ALERT_THRESHOLD (70)`, node service triggers `trigger_alert()` — a function-calling-driven action, logged locally and also pushed (as an alert event, not raw data) to the aggregator
7. Dashboard polls `/dashboard/summary` on the aggregator every 3 seconds, rendering real-time updates and emergency banners

## 4. Failure modes to design for (own these explicitly, don't discover them live)

| Failure | Handled by |
|---|---|
| A Gemini key is rate-limited | Key pool auto-rotates, logs visibly (`gemini-engine.md` §2) |
| ngrok URL changes after a restart | Advay re-registers both Twilio webhook URLs — see `assignments/advay.md` checklist |
| Node service restarts, loses in-memory history | Acceptable for hackathon demo; note as a known limitation, would be a real DB in production |
| Gemini returns malformed/non-schema JSON | Node service catches, retries once, falls back to a safe default score with `confidence: 0` and logs the raw response for debugging |

## 5. Tech stack summary

- Backend: Python, FastAPI (both node and aggregator services)
- AI: Gemini API (`google-genai` SDK), structured output + function calling
- Channels: Twilio (WhatsApp sandbox, Voice with Gather/Say)
- Tunnel: ngrok
- Frontend: React (or plain HTML/JS if time is short — decision owned by Netal, see `frontend.md`)
- No database — in-memory dicts, acceptable for a single-day demo (explicitly noted as a limitation, not hidden)
