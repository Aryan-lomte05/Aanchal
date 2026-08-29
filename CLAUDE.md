# CLAUDE.md — Project Master Index

**Project:** Aanchal — Wrapping Every Victim in Continuous Care, Without Ever Exposing Them
**Sub-title:** A Federated AI Companion for Continuous, Private Distress Monitoring and Care of Atrocity Victims (built on SIH26094)
**Event:** KJSSE CSI Gemini Hackday 2.0
**Team:** Aryan (System Dev & AI) · Advay (Full Stack + DevOps) · Netal (Frontend & UX Lead · Conversational Design · Pitch Owner)

This file is the front door. Every other doc in this repo answers one question. Read this first, then jump to whichever doc your current task needs.

---

## 1. What we're building, in one paragraph

An AI system that continuously monitors psychological distress in victims/complainants of atrocities (per SIH26094, Ministry of Social Justice and Empowerment) across multiple channels — WhatsApp, voice calls, and web — using Gemini to score distress in real time, while keeping all raw personal data local to a "district node" and only federating anonymized distress scores upward to a national dashboard. Privacy-by-architecture is our core differentiator, not a bullet point.

## 2. Doc map

| Doc | Answers |
|---|---|
| [docs/requirements.md](./docs/requirements.md) | What must this system do, per the official PS and hackathon rules? |
| [docs/context.md](./docs/context.md) | Why this project, why this architecture, what's the timeline? |
| [docs/system-overview.md](./docs/system-overview.md) | What are the components and how do they talk to each other? |
| [docs/agent-orchestration.md](./docs/agent-orchestration.md) | How does a single user interaction flow through Gemini end to end? |
| [docs/privacy-rules.md](./docs/privacy-rules.md) | What data goes where, and what never leaves a node? |
| [docs/gemini-engine.md](./docs/gemini-engine.md) | Exact models, schemas, key-pool logic, prompt design |
| [docs/frontend.md](./docs/frontend.md) | Dashboard UI spec, views, components, tech stack |
| [docs/coding-standards-and-rules.md](./docs/coding-standards-and-rules.md) | Naming, git workflow, folder structure, commit format |
| [docs/api-contracts.md](./docs/api-contracts.md) | Every endpoint, every request/response schema |
| [docs/assignments/aryan.md](./docs/assignments/aryan.md) | Aryan's exact deliverables and timeline |
| [docs/assignments/advay.md](./docs/assignments/advay.md) | Advay's exact deliverables and timeline |
| [docs/assignments/netal.md](./docs/assignments/netal.md) | Netal's exact deliverables and timeline |

## 3. The 60-second pitch (memorize this)

> "Existing victim-support systems track legal and financial status but not mental health — and any system that *does* monitor mental health has to centralize deeply sensitive trauma data to do it. We built a federated distress-monitoring system: Gemini does real multilingual, multimodal reasoning on WhatsApp, voice calls, and web check-ins *locally at each district node* — full case history never leaves that node. Only an anonymized distress score gets federated upward to state and national dashboards. When a score crosses a risk threshold, Gemini itself triggers the escalation via function calling — a real alert to a counsellor, not just a red number on a screen. This is privacy-preserving AI for the most sensitive population a government system can serve."

## 4. Why this wins "most innovative/crazy Gemini API usage"

Not because of one gimmick — because Gemini is doing **five distinct jobs** in one coherent pipeline, and no single job is decorative:
1. Multilingual voice/text understanding (Live API / speech-to-text bridge)
2. Structured, explainable scoring (constrained JSON schema output)
3. Long-context longitudinal reasoning (per-victim history, held locally)
4. Function-calling-driven real-world escalation (not just a chat reply)
5. Grounded, enum-constrained intervention recommendations (mapped to real POA Act 1989 scheme categories, not hallucinated)

## 5. Demo script (for judging, 5:00–6:00 PM slot)

1. Open national dashboard — empty/baseline state, explain the architecture in 20 seconds using the pitch above
2. Live WhatsApp message sent to the bot in Hindi, describing mild distress → show structured score appear on district node view within seconds
3. Live phone call to the Twilio number, describe escalating distress → show the score computed, then a second call where wording indicates crisis → **threshold breach triggers a live alert** on the national dashboard in front of judges
4. Zoom out to the privacy architecture diagram — explicitly say "the raw transcript from that call never left the district node — only this anonymized score did"
5. Close with the pitch line: "This is what a government-grade Gemini deployment for trauma survivors should look like."

## 6. Critical rules that apply to everyone (full detail in privacy-rules.md and coding-standards-and-rules.md)

- Never demo with real victim data. Synthetic scripts only.
- Never let the system present itself as "diagnosing" — always "flagging for human review."
- Raw text/audio never crosses from a node service to the aggregator service. Code review anyone's PR that touches `push_to_aggregator` extra carefully.
- All three of us can read every doc in this repo. If you change an API contract, update `api-contracts.md` in the same commit — don't let it drift.
