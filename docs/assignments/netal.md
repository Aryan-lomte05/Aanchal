# assignments/netal.md

**Role:** Frontend & UX Lead · Conversational Design · Demo & Pitch Owner
**Design Paradigm:** "Sanctuary of Healing" — Light Mode, Anti-AI-Slop, High-Empathy Trauma-Informed Aesthetics
**Owns:** `frontend.md`, Sanctuary PWA UI, Web Audio Binaural Synthesizer, Canvas Trajectory Visualizer, Victim-facing Conversational UX, Officer Workflow UX, Synthetic Test Data, Pitch Deck, Judge Q&A Prep, "Aanchal" Branding

---

## 1. Expanded Scope & Responsibilities

1. **Anti-AI-Slop Sanctuary Aesthetic (Light-Mode First):**
   - Direct the visual overhaul from generic dark-mode hacker tropes to an award-winning, luminous sanctuary aesthetic (Creamy Silk, Warm Rose, Healing Mint Sage, and frosted glass with light refraction).
   - Ensure WCAG AAA contrast, fluid typography (`Outfit` + `Plus Jakarta Sans`), and gentle spring micro-animations.

2. **Therapeutic Audio & Biometric De-escalation UX:**
   - Implement real-time in-browser sound synthesis using Web Audio API: 432 Hz ("Healing Frequency") and 528 Hz gentle theta-wave oscillators to provide immediate non-verbal grounding for traumatized victims.
   - Build the 6-petal sacred geometry breathing orb with rhythmic 4-7-8 trauma de-escalation pacing.

3. **Victim-Facing Conversational UX (Multi-channel Tone & Copy):**
   - Own the exact wording of all automated WhatsApp and voice call responses victims receive.
   - Ensure messages are deeply empathetic, culturally sensitive, supportive, and strictly **non-diagnostic** (adhering to `privacy-rules.md` §5).
   - Provide localized message templates in English and Hindi/regional dialects.

4. **Officer-Side Actionable Triage Desk & Longitudinal Canvas:**
   - Canvas-based dynamic Bezier-spline charting of distress trajectories over time.
   - Design the actionable triage workflow with state transitions (`[Mark Contacted]`, `[Assign Nodal Counsellor]`, `[Deploy Section 15A Protection]`, `[Dispatch Rule 12 Relief]`, `[Dismiss False Positive]`).

5. **Full Pitch Deck Ownership (Visuals & Narrative):**
   - Own and build the complete 3–5 slide presentation deck:
     1. **The Human Problem:** Atrocity aftermath & mental health void (SIH26094).
     2. **The Aanchal Solution:** Multi-channel continuous care companion.
     3. **Privacy-First Federated Architecture:** Local node vs. national signal boundary (diagram from `system-overview.md`).
     4. **The Live Demo Arc:** Multi-lingual check-in → Gemini reasoning → threshold breach alert.
     5. **Impact & MoSJE Scheme Alignment:** Real POA Act 1989 intervention mapping.

6. **Judge Q&A Prep Sheet:**
   - Draft crisp, memorizable answers for the team covering the 6–8 hardest expected judge questions (federated privacy enforcement, deterministic vs. LLM escalation, hallucinations, rate limiting resilience, and production deployment roadmap).

7. **Aanchal Naming & Brand Consistency Pass:**
   - Enforce consistent "Aanchal" identity across all touchpoints: dashboard header, WhatsApp greeting ("Aanchal Saathi"), Voice IVR prompt, node district branding (`Aanchal Node - Pune District`), and presentation deck.

---

## 2. Deliverables & Timeline

### Night before
- [ ] **Lock Light-Mode Sanctuary Theme:** Finalize design tokens in `frontend.md` and CSS custom properties.
- [ ] **Web Audio Synthesizer Prototype:** Test Web Audio API 432Hz sine/theta wave generator across mobile & desktop browsers.
- [ ] **Wireframe Dashboard Views:** Sketch 3 key views (District Node, National Rollup, Alert Workflow Center).
- [ ] **Victim-Facing Copy Kit:** Finalize supportive greeting & acknowledgment copy across channels (WhatsApp/Voice) in English and Hindi.
- [ ] **Synthetic Multilingual Test Suite (`test_data/scripts.md`):**
  - 2 low-distress scripts (routine follow-up, stable baseline).
  - 1-2 medium-distress scripts (procedural anxiety, social pressure).
  - 1 high-distress script engineered to cross `DISTRESS_ALERT_THRESHOLD` (>70) for live demo alert triggering.
  - Multilingual coverage (Hindi / Hinglish / English).
- [ ] **Brand Asset & Copy Pass:** Ensure all headers and prompts use "Aanchal" branding.

### Round 1 (10:00 AM – 1:00 PM)
- [ ] **Static Sanctuary Shell:** Build layout, responsive navigation, creamy glassmorphic cards, and breathing orb.
- [ ] **Officer Alert Component:** Build the alert banner and workflow action modal (`[Mark Contacted]`, `[Escalate]`).
- [ ] **Pitch Deck v1:** Assemble slides 1–3 (Problem, Architecture Diagram, Solution Overview).
- [ ] **Contract Sync:** Confirm `/dashboard/summary` and `/dashboard/node/{node_id}` JSON shapes with Advay.

### Round 2 (1:30 PM – 5:00 PM)
- [ ] **Live Polling Integration:** Wire dashboard to real `/dashboard/summary` endpoint (`frontend.md` §3).
- [ ] **Live Alert Testing:** Verify banner pops and renders dynamic Gemini-generated reasons when threshold is crossed.
- [ ] **Pitch Deck Finalization:** Complete demo transition and impact slides; rehearse timing.
- [ ] **Judge Q&A Sheet:** Finalize talking points and distribute to Aryan and Advay.
- [ ] **Demo Sequencing Walkthrough:** Rehearse the exact trigger sequence (WhatsApp message → Voice call → Live alert pop).

### Last 30–45 min (Feature Freeze & Rehearsal)
- [ ] **End-to-End Live Rehearsal:** Timed execution of pitch + live WhatsApp/Voice demo + alert trigger.
- [ ] **Final UI Cleanliness Check:** Confirm zero raw personal data or phone numbers appear on screen.

---

## 3. Explicit Boundaries

- **No backend/orchestration modifications:** Do not alter Gemini prompts or FastAPI server code directly; coordinate with Aryan for prompt tuning and Advay for endpoint formats.
- **Strict Privacy Rule:** Under no circumstances should raw transcripts or unhashed identifiers be displayed on any frontend view (even in mock/debug panels).

---

## 4. Dependencies on Others

- **Advay:** Stable `/dashboard/summary` and `/dashboard/node/{node_id}` response structures.
- **Aryan:** Confirmation that test scripts in `test_data/scripts.md` reliably generate expected score bands and trigger function calling.

