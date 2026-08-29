# api-contracts.md

Every endpoint in the system, in one place. If you change a request/response shape, update it here in the same commit (see `coding-standards-and-rules.md` §3).

## 1. Node Service — Twilio webhooks (inbound, victim-facing)

### `POST /whatsapp/webhook`
**Owner:** Advay (integration) / Aryan (orchestration call inside it)
Triggered by Twilio when a WhatsApp message arrives.

Request (Twilio form-encoded, key fields):
```
Body: str        # the victim's message text
From: str        # whatsapp:+91XXXXXXXXXX — used as raw channel ID, hashed before federating
```
Response: TwiML (`MessagingResponse`) with a generic supportive reply. See `agent-orchestration.md` §5 for reply-content rules.

### `POST /voice/incoming`
Triggered on an inbound call. Returns TwiML `<Gather>` prompting speech input (Hindi by default, per `frontend.md`'s multilingual test scripts).

Response: TwiML with `Gather(input="speech", action="/voice/process", language="hi-IN")`

### `POST /voice/process`
Triggered after Twilio's speech-to-text completes.

Request:
```
SpeechResult: str   # transcribed text
From: str           # caller's number, hashed before federating
```
Response: TwiML with a generic supportive spoken reply.

## 2. Node Service — internal orchestration (not exposed externally, called by webhook handlers)

```python
def process_session(victim_channel_id: str, raw_input: str, channel: str) -> dict:
    """
    Runs the full orchestration in agent-orchestration.md §4.
    Returns the DistressSchema-shaped score_data dict.
    Side effects: updates local_case_history, pushes to aggregator,
    triggers alert if threshold crossed.
    """
```

## 3. Node Service → Aggregator (outbound federated push)

### `POST /federated/push_score` (on the Aggregator)
**Owner:** Aryan (payload contents) / Advay (endpoint implementation)

Request body:
```json
{
  "node_id": "district_pune",
  "hashed_case_id": "sha256:...",
  "score_data": {
    "distress_score": 42,
    "contributing_factors": ["repeated_threat_mentions", "declining_engagement"],
    "confidence": 0.81,
    "explanation": "Score reflects...",
    "recommended_intervention": "counselling",
    "trend": "worsening"
  },
  "timestamp": "2026-08-29T14:03:00Z"
}
```
Response: `{"status": "received"}`

**Validation rule:** the aggregator MUST reject any payload containing a field not in this shape — this is the enforcement point for `privacy-rules.md` §2 (raw text can't leak through here even by accident, because the schema doesn't allow it).

### `POST /federated/alert` (on the Aggregator)

Request body:
```json
{
  "node_id": "district_pune",
  "hashed_case_id": "sha256:...",
  "urgency": "critical",
  "reason": "Distress score crossed threshold with worsening trend over 2 sessions.",
  "recommended_immediate_action": "Immediate counsellor contact recommended.",
  "timestamp": "2026-08-29T14:05:00Z"
}
```
Response: `{"status": "alert_received"}`

## 4. Aggregator → Frontend Dashboard

### `GET /dashboard/summary`
**Owner:** Advay (implementation) / Netal (consumer, see `frontend.md` §4)

Response body:
```json
{
  "national": {
    "total_cases": 12,
    "high_risk_count": 2
  },
  "nodes": [
    {
      "node_id": "district_pune",
      "case_count": 7,
      "average_score": 38.4,
      "highest_current_score": 76
    }
  ],
  "alerts": [
    {
      "node_id": "district_pune",
      "hashed_case_id": "sha256:...",
      "urgency": "critical",
      "reason": "...",
      "timestamp": "2026-08-29T14:05:00Z"
    }
  ]
}
```

### `GET /dashboard/node/{node_id}`
Returns the per-victim (hashed) list and score history for a single node's district view. Same score-only shape — no raw content, ever, per `privacy-rules.md`.

## 5. Change control

This file is the contract. If Aryan changes `DistressSchema` in `gemini-engine.md`, this file's §3 request body must be updated in the same commit, and Advay must be pinged directly (not just via commit message) since the aggregator's validation logic depends on it.
