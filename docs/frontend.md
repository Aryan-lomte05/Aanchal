# frontend.md — Aanchal Design Bible & Frontend Architecture

**Project:** Aanchal — Wrapping Every Victim in Continuous Care, Without Ever Exposing Them
**Design Philosophy:** "Sanctuary of Healing" — Light-Mode, Trauma-Informed, Anti-Clinical, Human-Grade Empathy
**Lead Owner:** Netal (Frontend & UX Lead · Conversational Design · Pitch Owner)
**Technical Architecture Partner:** Advay (FastAPI, Webhooks, SSE/WebSocket Bridge)

---

## 1. Aesthetic Vision: The Anti-AI-Slop Manifesto

Traditional emergency & tech hackathon projects default to harsh neon-on-black terminal themes that look clinical, threatening, and cold. For survivors of atrocities under the SC/ST (Prevention of Atrocities) Act 1989, interface tone is an active therapeutic intervention.

**Aanchal is designed as a warm, luminous Sanctuary:**
- **Luminous Light Palette:** Creamy Silk (`#FAF9F6`), Alabaster Warmth (`#FFFFFF`), Soft Pearl Sand (`#F4F1EA`), and Translucent Cloud Glass (`rgba(255, 255, 255, 0.85)`).
- **Healing Color Harmony:**
  - **Aanchal Rose (Empathy & Care):** Radiant Warm Coral-Rose (`#E11D48`, `#FB7185`, `#FFF1F2`).
  - **Oasis Sage & Mint (Grounding):** Calming Herbal Sage (`#0D9488`, `#14B8A6`, `#F0FDFA`).
  - **Morning Sunbeam (Hope):** Soft Amber Glow (`#D97706`, `#F59E0B`, `#FEF3C7`).
  - **Dusk Lavender (Stillness):** Serene Lavender (`#7C3AED`, `#A78BFA`, `#F5F3FF`).
  - **Crisp Editorial Typography:** Deep Velvet Slate (`#0F172A`, `#334155`) for crystal-clear readability without harsh black contrast.
- **Organic Geometry & Micro-Interactions:** 24px+ soft-rounded squircle corners, delicate 1px translucent glass borders, multi-layered diffuse shadows (`box-shadow: 0 20px 40px -15px rgba(225, 29, 72, 0.08)`), and spring-physics easing.

---

## 2. Advanced Feature Ecosystem

### 2.1 🌸 Aanchal Saathi (Victim Comfort Companion)
- **Harmonic Petal Breathing Orb:** Interactive animated 6-petal sacred geometry orb that expands and contracts on a 4-7-8 trauma-grounding cadence (`Inhale Calm... Hold Space... Release Tension...`).
- **Binaural Calming Audio Synthesizer:** Real-time Web Audio API frequency oscillator generating 432 Hz ("Miracle / Healing Frequency") and 528 Hz gentle theta-wave soothing tones with volume envelope shaping to de-escalate anxiety attacks on demand.
- **Multilingual Voice & Chat Hub:** Seamless voice input (Web Speech API supporting Hindi `hi-IN` & English `en-US`) with real-time waveform pulsation and SpeechSynthesis soothing audio playback.
- **Zero-Exposure Privacy Shield:** Interactive architectural diagram explaining how voice recordings never leave the device/district node.
- **One-Tap Emergency SOS Bar:** Immediate tactile dialers for Tele-MANAS (`14416`), National SC/ST Helpline (`14566`), and Women Crisis Helpline (`1091`).

### 2.2 🏛️ District Welfare Command Desk (Officer Workbench)
- **Longitudinal Trajectory Canvas:** Smooth Bezier-spline charting of victim distress trajectories over time, showing prior baselines against current scores.
- **Gemini Explainability Inspector:** Plain-language, non-diagnostic synthesis explaining why Gemini flagged the case, highlighting detected factor chips (`repeated_threat_mentions`, `social_ostracism_indicated`).
- **Interactive Triage Action Workbench:** Drag-and-drop / single-click state transition workflow:
  - `[Mark Contacted]` · `[Assign Nodal Counsellor]` · `[Deploy Section 15A Protection]` · `[Dispatch Rule 12 Relief]` · `[Dismiss False Positive]`

### 2.3 🌐 National MoSJE Mission Control (Aggregator View)
- **Pan-India District Heat Grid:** Real-time district health statuses (`Pune`, `Nagpur`, `Patna`, `Varanasi`).
- **Live Privacy Boundary Packet Inspector:** Live network telemetry proving that only 32-byte SHA-256 hashes and numeric score metadata cross the wire.
- **Statutory Intervention Distribution:** Real-time percentage breakdown across MoSJE schemes.

### 2.4 ⚡ Gemini AI Live Hackathon Sandbox
- **1-Click Synthetic Scenario Injector:** Instantly runs test scenarios (Scripts 1 to 5 from `test_data/scripts.md`) in Hindi, Hinglish, and English through the live Gemini 2.5 Flash pipeline.
- **Gemini Key Pool Telemetry Grid:** Real-time visual monitoring of all 15 API keys, showing active states, 60s cooldown triggers, RPM/TPM usage, and failover rotation logs.

---

## 3. High-Tech Additions for Netal & Advay

| Lead | Technology / Feature | Purpose |
|---|---|---|
| **Netal** | **Web Audio API 432Hz Sound Synthesizer** | Real-time binaural trauma de-escalation sound generation in browser without external audio assets. |
| **Netal** | **Canvas Spline Mood Visualizer** | Interactive longitudinal Bezier curves rendering historical baseline trends. |
| **Netal** | **PWA Offline Service Worker & Manifest** | Installable on iOS/Android/Desktop with cached helpline directories. |
| **Advay** | **Server-Sent Events (SSE) & Fast Polling** | Sub-second real-time alert broadcasts from Node to Aggregator to UI. |
| **Advay** | **Strict Cryptographic Privacy Firewall** | Hard rejection of any payload containing unhashed phone numbers or raw transcripts. |
| **Advay** | **Twilio Voice STT & WhatsApp TwiML Gateway** | Multi-channel ingestion from real phones during the onstage live demo. |

---

## 4. UI Typography Scale & Design Tokens

```css
:root {
  /* Surface Colors */
  --surface-cream: #FAF9F6;
  --surface-card: rgba(255, 255, 255, 0.88);
  --surface-glass: rgba(255, 255, 255, 0.72);
  --surface-overlay: rgba(15, 23, 42, 0.04);

  /* Typography */
  --font-display: 'Outfit', -apple-system, sans-serif;
  --font-body: 'Plus Jakarta Sans', 'Noto Sans Devanagari', sans-serif;
  --text-main: #0F172A;
  --text-muted: #64748B;
  --text-soft: #94A3B8;

  /* Therapeutic Accents */
  --rose-primary: #E11D48;
  --rose-soft: #FFF1F2;
  --rose-border: rgba(225, 29, 72, 0.2);
  --teal-primary: #0D9488;
  --teal-soft: #F0FDFA;
  --amber-primary: #D97706;
  --amber-soft: #FEF3C7;
  --lavender-primary: #7C3AED;
  --lavender-soft: #F5F3FF;

  /* Elevation */
  --shadow-warm: 0 10px 30px -5px rgba(225, 29, 72, 0.08), 0 4px 12px rgba(15, 23, 42, 0.03);
  --shadow-float: 0 20px 40px -10px rgba(15, 23, 42, 0.07);
}
```
