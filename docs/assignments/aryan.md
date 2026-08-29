# assignments/aryan.md

**Role:** System Dev & AI
**Owns:** `gemini-engine.md`, `agent-orchestration.md`, `privacy-rules.md` enforcement across all code

## Deliverables

### Night before
- [ ] `backend/node_service/gemini_engine/key_pool.py` — `GeminiKeyPool` class, tested with key rotation and simulated 429 cooldowns
- [ ] `backend/node_service/gemini_engine/schemas.py` — `DistressSchema`, `trigger_alert_tool` declaration
- [ ] `backend/node_service/gemini_engine/prompts.py` — `build_scoring_prompt()`, `build_alert_escalation_prompt()` per `agent-orchestration.md` §2
- [ ] Confirm `gemini-2.5-flash` structured output consistently returns schema-valid JSON (5 distinct Gemini jobs)

### Round 1 (10–1)
- [ ] `process_session()` orchestration function (see `api-contracts.md` §2) — the core vertical slice: text in → Gemini call → score out → stored locally
- [ ] Wire this into a bare-minimum FastAPI route so Advay has something to hook Twilio into by the end of Round 1
- [ ] Confirm the full happy path once, manually, with one of Netal's test scripts

### Round 2 (1:30–5)
- [ ] Federated push: `push_to_aggregator()` function implementing `api-contracts.md` §3 exactly
- [ ] Hashing logic for `hashed_case_id` (SHA-256 of channel ID) — confirm it's applied before anything leaves the node
- [ ] Threshold check + `trigger_alert()` implementation per `agent-orchestration.md` §3
- [ ] Sit with Advay for ~20 min once WhatsApp/Voice webhooks are live to confirm they call `process_session()` correctly and nothing bypasses the orchestration path

### Last 30–45 min
- [ ] Confirm no raw text is visible anywhere outward-facing (spot-check the aggregator's received payloads)
- [ ] Be ready to explain `privacy-rules.md` §1-3 from memory during judging

## Explicit boundaries (don't do this — it's someone else's job)

- Don't build the dashboard — that's Netal's. If you need to sanity-check score output, use a `curl` or a print statement, not a UI.
- Don't write the Twilio webhook handlers yourself — write the function they should call (`process_session()`), let Advay wire the webhook to it. This keeps the orchestration logic in one place per `agent-orchestration.md` §5.

## Dependencies on others

- Need Advay's FastAPI app skeleton to exist before you can wire `process_session()` into a real route (or stub it yourself night-before and hand off)
- Need Netal's synthetic test scripts before you can verify prompt behavior produces a real range of scores
