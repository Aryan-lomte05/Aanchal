# context.md

## 1. Why this problem statement

Open-ended hackathon, judged on meaningful/well-integrated Gemini usage. SIH26094 was chosen because:
- It's a genuinely hard, real problem (government-scale victim welfare monitoring)
- Its "expected solution" list is dense enough that we can show many *different* Gemini capabilities each solving a real, named requirement — not one gimmick stretched thin
- It has an obvious, demonstrable "wow" moment: a live alert firing from a live phone call

## 2. Why federated architecture, specifically

The official PS says "ensure privacy protection" but gives no mechanism. Most teams will bolt on a privacy policy paragraph. We instead borrow the core idea from a federated learning project one of us (Aryan) already built for a different domain (menstrual health anomaly detection, CEPDT project): keep raw sensitive data local to the point of collection, only share aggregated/anonymized signal upward. Applied here: raw transcripts and full case history stay at the "district node" that collected them; only the distress score (a few numbers, not the transcript) and a hashed case ID get pushed to the state/national aggregator.

This is inference-time federation of a *signal*, not federated *training* of a model — an important distinction, see `privacy-rules.md` §2.

## 3. Decisions log

| Decision | Reasoning |
|---|---|
| Channels: WhatsApp + Voice (Twilio), not SMS | WhatsApp sandbox needs zero approval and gives a rich demo; Voice gives the most dramatic live moment; SMS adds a third webhook for marginal demo value given the time budget |
| Voice via Twilio's built-in speech-to-text + Gemini text reasoning, not raw Gemini Live audio streaming | Full bidirectional audio streaming via Twilio Media Streams is a real chunk of engineering (websocket relay, frame encoding) — not worth the risk in a 6.5-hour window. Stretch goal only if everything else finishes early. |
| 15-key API pool with round-robin + cooldown failover | Structured-output calls plus live testing burn quota fast; a single rate-limited key mid-demo is an avoidable failure |
| Dashboard via polling, not websockets | A poll every few seconds is visually indistinguishable from "real-time" for judges and saves real engineering hours for the parts that matter more |
| No real victim data, ever, including local testing | Non-negotiable — see `privacy-rules.md` §4 |

## 4. Timeline

**Night before:**
- Repo skeleton, both services scaffolded (node + aggregator)
- Gemini structured-output schema finalized and tested with dummy input
- Twilio sandbox + phone number provisioned, ngrok tested
- 4-5 synthetic multilingual test scripts written (see `assignments/netal.md`)
- Dashboard wireframe agreed

**Round 1 (10:00–1:00):** One working vertical slice — text input → Gemini structured score → stored on one node. No federation, no UI polish yet. Prove the core loop.

**Round 2 (1:30–5:00):** Federated aggregation across 2-3 simulated nodes, function-calling alert trigger, WhatsApp + Voice webhooks live, dashboard connected and polling.

**Last 30–45 min before judging:** Demo script rehearsal (see `CLAUDE.md` §5), not new features. Feature freeze.

## 5. Team, at a glance

| Person | Primary | Secondary |
|---|---|---|
| Aryan | System architecture, Gemini engine, key pool, federated logic, function-calling alerts | Privacy-rules enforcement across all services |
| Advay | FastAPI backend for both services, Twilio webhook integration (WhatsApp + Voice), ngrok/deployment | API contract ownership, integration testing across all three people's work |
| Netal | Frontend dashboard, conversational UX & tone, officer workflow UX | Full pitch deck, judge Q&A prep sheet, Aanchal branding, synthetic test suite |

Full detail per person in `assignments/`.
