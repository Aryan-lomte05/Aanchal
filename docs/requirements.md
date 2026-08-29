# requirements.md

## 1. Source problem statement — SIH26094 (verbatim-derived)

**Title:** AI-Powered Dynamic Mental Health Monitoring and Distress Prediction System for Victims of Atrocities
**Sponsor:** Ministry of Social Justice and Empowerment (MoSJE)

### 1.1 Background
Victims of atrocities experience prolonged psychological distress after complaint registration — threats, intimidation, repeated court appearances, investigation/trial delays, social ostracism, economic hardship, rehabilitation challenges. Existing mechanisms cover legal/financial support only; no continuous well-being monitoring exists today.

### 1.2 Functional requirements (from the official "Expected Solution")
The system MUST:
- [ ] Conduct periodic interactions via chatbot, IVRS calls, SMS, mobile app, web portal, or helpline follow-up
- [ ] Analyse voice, text, behavioural responses, and engagement patterns using NLP, Sentiment Analysis, Emotion AI
- [ ] Generate a **Dynamic Distress Score** with longitudinal trend analysis
- [ ] Predict escalation of psychological distress **before** a crisis emerges
- [ ] Trigger alerts to counsellors, district authorities, designated officials on threshold breach
- [ ] Recommend interventions: counselling, medical treatment, witness protection, relocation support, financial assistance, legal aid, rehabilitation
- [ ] Provide dashboards at district, State, and national levels
- [ ] Ensure explainable AI, privacy protection, data security, legal/ethical compliance

### 1.3 Priority use cases (highest sensitivity — design for these explicitly)
- Victims of rape and gang rape
- Victims of murder, grievous hurt, arson
- Witnesses facing intimidation or threats
- Families affected by caste-based violence
- Beneficiaries under the SC/ST (Prevention of Atrocities) Act, 1989

## 2. What we are adding beyond the official PS

| Addition | Why |
|---|---|
| Federated privacy architecture | PS demands "privacy protection" but doesn't specify how — we answer this with architecture, not a policy statement |
| Multi-channel via Twilio (WhatsApp + Voice) | PS explicitly lists chatbot/IVRS/app/web as channels — we implement two real ones instead of mocking all five |
| API key pool with automatic failover | Operational resilience — demo can't die because of a single rate-limited key |
| Live, judge-triggerable demo | Static screenshots don't prove the pipeline works; a live call/message does |

## 3. Hackathon constraints (KJSSE CSI Gemini Hackday 2.0)

- Single-day event. Coding Round 1: 10:00 AM – 1:00 PM. Coding Round 2: 1:30 PM – 5:00 PM. Judging: 5:00–6:00 PM.
- Special prize category: most innovative/crazy use of the Gemini API — judged on **meaningful, well-integrated** usage, not surface-level.
- Effective build time: ~6.5 hours of coding, plus whatever is done the night before.
- 3-person team: Aryan (System Dev & AI), Advay (Full Stack + DevOps), Netal (Frontend + Demo/UX).

## 4. Explicit non-goals for this build (say these out loud if asked)

- No real production-grade encryption or differential privacy math — architecture is demonstrated conceptually and stated clearly as such.
- No real victim data anywhere, at any stage, including the night-before test scripts.
- No true federated *model training* (federated averaging of weights) — we federate distress *scores*, which is the correct scope for an LLM-based system and is explicitly called out in `privacy-rules.md`.
- No SMS channel — cut per team decision, see context.md §3.

## 5. Definition of done for the demo

1. A message/call through at least one live channel produces a Gemini-scored, schema-valid distress output within seconds.
2. That score appears on a node-level view without any raw transcript visible outside the node.
3. A second interaction that crosses the distress threshold visibly triggers an alert on the national dashboard live, in front of judges.
4. The privacy architecture can be explained in under 30 seconds using the diagram in `system-overview.md`.
