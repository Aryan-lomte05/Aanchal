# privacy-rules.md

This is the doc a judge's hard question gets answered from. Everyone should be able to recite §1 and §2 from memory before judging.

## 1. The one rule that matters most

**Raw victim input — text, transcribed speech, full conversation history — is only ever held in the memory of the district node service that collected it. It is never serialized, logged, or transmitted to the aggregator, the dashboard, or any other node.**

Everything else in this doc is a consequence of that one rule.

## 2. What crosses the boundary from node → aggregator, exactly

Allowed (federated upward):
- `node_id` (e.g. `"district_pune"`) — identifies which node, not which person
- `hashed_case_id` — SHA-256 of the victim's channel identifier (phone number), one-way, not reversible without the node's local mapping
- `distress_score`, `confidence`, `trend`, `recommended_intervention` (enum), `contributing_factors` (short category tags, not raw quotes)
- Alert events: `urgency`, `reason` (Gemini-generated summary, not raw transcript), `recommended_immediate_action`

Never allowed across that boundary, under any circumstance:
- Raw message text or transcribed speech
- Phone numbers or any other reversible personal identifier
- Full conversation history (only the current score, not the interaction log)
- Anything from `contributing_factors` that quotes the victim directly — factors must be category labels (e.g. `"repeated_threat_mentions"`), not excerpts

## 3. Why this is "federated" and not just "we don't log stuff"

This mirrors the core idea of federated learning (data stays local, only a derived signal is shared) applied to inference instead of training. We are explicit that this is **not** federated model training — we are not averaging model weights across nodes. We are federating a *derived score*, which is the correct and honest framing for an LLM-based system built in a hackathon. Do not oversell this as "federated learning" in the literal ML sense during judging — say "federated architecture for privacy-preserving distress scoring," which is accurate and still impressive.

## 4. Demo data rules (non-negotiable)

- No real victim data, ever — not in testing, not in the repo, not in a screenshot, not "just to check it works."
- All test scripts are synthetic, written by the team (see `assignments/netal.md` for the test-script deliverable), and should avoid being modeled too closely on any real, identifiable case.
- If anyone screen-records the demo for submission, confirm no real phone numbers are visible (use a personal test number, crop if needed).

## 5. Framing rules for anything user- or judge-facing

- The system **flags patterns for human review**. It does not diagnose, and no UI text, victim-facing message, or pitch line should imply otherwise.
- Victim-facing replies (via WhatsApp/Voice) are always generic and supportive — never reveal the computed score or any distress-related language back to the victim.
- Dashboard-facing language for officers should be "risk indicator," "flagged for review," not "diagnosis" or "mental health status: X."

## 6. Explainability requirement (from the official PS)

Every score must ship with a plain-language `explanation` field (part of `DistressSchema`, see `gemini-engine.md`). This is not optional polish — it's a named requirement in the source PS ("Explainable AI") and it's also your best answer if a judge asks "how do you know the AI isn't just guessing."

## 7. If a judge asks "what about encryption / compliance / a real production deployment"

Answer honestly: this hackathon build demonstrates the architectural boundary (network-level separation of raw data from aggregated signal) but does not implement production-grade encryption at rest, formal differential privacy guarantees, or legal compliance review — all of which a real MoSJE deployment would require and would be the next engineering phase. Don't claim more than what's built.
