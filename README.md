# Aanchal: Wrapping Every Victim in Continuous Care, Without Ever Exposing Them

> **A Federated AI Companion for Continuous, Private Distress Monitoring and Care of Atrocity Victims**
> Built for KJSSE CSI Gemini Hackday 2.0 (Problem Statement: SIH26094, Ministry of Social Justice and Empowerment)

[![Status](https://img.shields.io/badge/status-hackathon%20prototype-8B7CF6?style=flat-square)](#status-and-honest-limits)
[![Privacy](https://img.shields.io/badge/raw%20transcripts-never%20leave%20the%20district-4BC8C0?style=flat-square)](#architecture--privacy-boundary)
[![Channels](https://img.shields.io/badge/channels-WhatsApp%20·%20Voice%20·%20PWA-15181D?style=flat-square)](#the-5-gemini-engine-capabilities-in-one-pipeline)
[![License](https://img.shields.io/badge/license-MIT-15181D?style=flat-square)](LICENSE)

**The problem in one line:** existing support systems for victims of atrocities under the SC/ST (Prevention of
Atrocities) Act track legal and financial milestones, so a victim being intimidated into silence looks
identical to a victim who is safe. Aanchal watches for psychological distress instead, and is built so that
watching cannot itself become a way to expose the person being watched.

**The central design constraint:** a national dashboard needs to see distress, but nobody above the district
should ever be able to see *a person*. So raw transcripts and identities are confined to a district node, and
only `{node_id, hashed_case_id, score_data}` crosses the boundary upward. The privacy boundary is enforced by a
validator in the aggregator, not by convention.

---

## 🌟 Overview

Victims of atrocities under the SC/ST (Prevention of Atrocities) Act, 1989 face immense trauma and prolonged vulnerability after filing a complaint, ranging from social ostracism and intimidation to procedural delays. Existing systems only monitor legal and financial parameters, leaving psychological well-being unaddressed.

**Aanchal** is a multi-channel, privacy-preserving distress monitoring and support companion. By deploying **Gemini 2.5 Flash** at localized **District Nodes**, Aanchal conducts continuous multilingual check-ins (WhatsApp, Voice Calls, Web) while ensuring **raw victim data and transcripts never leave the district node**. Only anonymized distress metrics and risk signals are federated to state and national dashboards, triggering immediate real-world interventions when critical thresholds are breached.

---

## 🏗️ Architecture & Privacy Boundary

```
                     ┌─────────────────────────────────────────┐
                     │           INPUT CHANNELS                │
                     │  WhatsApp (Twilio)   Voice Call (Twilio)│
                     │        Web check-in form (fallback)     │
                     └───────────────┬─────────────────────────┘
                                     │  raw text/speech-to-text
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │              DISTRICT NODE SERVICE                     │
        │  - Owns raw case history for its victims (LOCAL ONLY)  │
        │  - Calls Gemini Engine for structured distress scoring │
        │  - Long-context: full history stays IN this service    │
        │  - Runs function-calling alert trigger locally         │
        └───────────────┬────────────────────────────────────────┘
                        │  ONLY: {node_id, hashed_case_id, score_data}
                        │  NEVER: raw transcript, real victim identity
                        ▼
        ┌────────────────────────────────────────────────────────┐
        │             AGGREGATOR SERVICE (National View)         │
        │  - Receives anonymized scores only                     │
        │  - Builds district / state / national rollups          │
        │  - Serves dashboard API                                │
        └───────────────┬────────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────────────────────┐
        │                  FRONTEND DASHBOARD                    │
        │   District view → State view → National view           │
        │   Live alert banner on threshold breach                │
        └────────────────────────────────────────────────────────┘
```

### The 5 Gemini Engine Capabilities in One Pipeline
1. **Multilingual Understanding**: Native comprehension of Hindi and regional dialect transcripts & messages.
2. **Structured Scoring**: Deterministic `DistressSchema` output (scores 0-100, confidence, trend, contributing factors).
3. **Longitudinal History Context**: Local in-memory victim interaction baseline evaluation without central storage.
4. **Function Calling Escalation**: Gemini-driven alert reasoning (`trigger_alert`) on threshold breach.
5. **Grounded Interventions**: Enum-constrained categorization directly mapped to POA Act schemes (legal aid, counselling, witness protection, relocation).

---

## 📁 Repository Structure

```
.
├── CLAUDE.md                    # Project master index & 60-second pitch
├── run.py                       # Unified full-stack runner
├── README.md                    # Project overview & documentation guide
├── .env.example                 # Environment variable templates
├── backend/                     # Modular backend services
│   ├── node_service/            # Local District Node service (FastAPI / Port 8000)
│   │   ├── gemini_engine/       # Shared Gemini Engine (Key Pool, Prompts, Schemas, 5 Jobs)
│   │   ├── local_store.py       # In-memory local case repository & SHA-256 hashing
│   │   └── main.py              # Twilio WhatsApp/Voice webhooks, PWA check-in, federated push
│   ├── aggregator_service/      # National Aggregator service (FastAPI / Port 9000)
│   │   ├── national_view.py     # Privacy validator & Pan-India district rollups
│   │   └── main.py              # Dashboard summary API & officer action workflows
│   └── run_all.py               # Dual-service backend launcher
├── frontend/                    # Comforting Glassmorphic PWA Frontend
│   ├── index.html               # 4 Viewports (Aanchal Saathi, District, National, Sandbox)
│   ├── styles.css               # Soothing design system, animations & responsive styling
│   ├── app.js                   # Web Speech voice I/O, 3s polling & demo injector
│   ├── manifest.json            # PWA manifest
│   └── sw.js                    # Service Worker for offline resilience
├── test_data/                   # Synthetic multilingual check-in scripts
│   └── scripts.md
└── docs/                        # Complete technical specification & assignment docs

---

## 📚 Documentation Index

For in-depth details, refer to the documents in [`docs/`](./docs/):
- **Master Index & Pitch:** [CLAUDE.md](./CLAUDE.md)
- **Problem Statement & Scope:** [docs/requirements.md](./docs/requirements.md)
- **Privacy Architecture:** [docs/privacy-rules.md](./docs/privacy-rules.md)
- **Gemini Engine Spec:** [docs/gemini-engine.md](./docs/gemini-engine.md)
- **Agent Orchestration:** [docs/agent-orchestration.md](./docs/agent-orchestration.md)
- **API Contracts:** [docs/api-contracts.md](./docs/api-contracts.md)
- **Frontend Specs:** [docs/frontend.md](./docs/frontend.md)
- **Coding Standards:** [docs/coding-standards-and-rules.md](./docs/coding-standards-and-rules.md)

---

## Status and honest limits

This was built as a **hackathon prototype** over a single build cycle, and it should be read as a working
demonstration of the privacy architecture rather than a deployable system.

- **Not deployed, not piloted.** It has never been used with a real victim, and it must not be without ethical
  review, consent design and clinical supervision. Distress scoring on a vulnerable population is a serious
  intervention, not a feature.
- **The district node keeps case history in memory,** which is deliberate for the privacy demonstration but
  means durability and node-level access control are unbuilt.
- **Distress scores are model outputs, not clinical assessments.** They are routed to human officers for
  judgement; no escalation is automated end-to-end without a person in the loop.
- **Tested on synthetic multilingual check-in scripts** (`test_data/scripts.md`), not on real conversations.
- **No formal privacy guarantee.** The architecture restricts what crosses the district boundary; it does not
  provide differential privacy over the aggregated scores, so small-district re-identification risk is
  unquantified.

The part worth taking seriously is the boundary itself: the aggregator validates the shape of what it receives
and rejects anything carrying raw text or identity, so a careless change upstream fails loudly instead of
quietly leaking.

---

## 👥 Team
- **Aryan**: System Dev & AI (`docs/assignments/aryan.md`)
- **Advay**: Full Stack + DevOps (`docs/assignments/advay.md`)
- **Netal**: Frontend & UX Lead · Conversational Design · Pitch Owner (`docs/assignments/netal.md`)
