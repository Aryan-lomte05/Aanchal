# gemini-engine.md

Owner: Aryan. This is the only module that should ever need to change if we swap models, adjust the schema, or tune the key pool. Everything else imports from this module and should not reimplement any of it.

## 1. Model choice

- **`gemini-2.5-flash`** for all distress-scoring calls — fast, cheap, sufficient reasoning depth for structured classification + short explanation generation. Don't reach for a heavier model without a specific reason logged in `context.md`'s decisions table.
- If Live API audio is attempted as a stretch goal (see `context.md` §3), use the dedicated Live model — check current model name at ai.google.dev before wiring it, names change.

## 2. Key pool manager (module: `backend/node_service/gemini_engine/key_pool.py`)

```python
import itertools
import time
from google import genai
from google.genai.errors import ClientError

class GeminiKeyPool:
    def __init__(self, api_keys: list[str]):
        assert len(api_keys) > 0
        self.keys = api_keys
        self.clients = {k: genai.Client(api_key=k) for k in api_keys}
        self.cooldowns = {k: 0.0 for k in api_keys}
        self._cycle = itertools.cycle(api_keys)

    def _next_available_key(self):
        now = time.time()
        for _ in range(len(self.keys)):
            k = next(self._cycle)
            if self.cooldowns[k] <= now:
                return k
        raise RuntimeError("All keys are rate-limited right now")

    def generate(self, *args, max_retries=None, **kwargs):
        max_retries = max_retries or len(self.keys)
        last_err = None
        for _ in range(max_retries):
            key = self._next_available_key()
            client = self.clients[key]
            try:
                return client.models.generate_content(*args, **kwargs)
            except ClientError as e:
                if e.code == 429:
                    self.cooldowns[key] = time.time() + 60
                    print(f"[key_pool] key ...{key[-4:]} rate-limited, rotating")
                    last_err = e
                    continue
                raise
        raise last_err
```

Rules:
- Round-robin, not "smartest key first" — we don't have real-time quota visibility per key, so even distribution is the safest default.
- 60s cooldown on a 429. Verify this against current published limits before the event, don't trust an old number.
- Retry budget capped at pool size (15) so a genuinely broken request doesn't spin silently.
- **Log every rotation visibly** — this is a demo asset, not just error handling. If it fires live, point at the log line and call it resilience.

## 3. DistressSchema — the one schema everything depends on

```python
DistressSchema = {
    "type": "object",
    "properties": {
        "distress_score": {"type": "number", "minimum": 0, "maximum": 100},
        "contributing_factors": {
            "type": "array",
            "items": {"type": "string"}
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "explanation": {"type": "string"},
        "recommended_intervention": {
            "type": "string",
            "enum": [
                "counselling", "medical", "witness_protection",
                "relocation", "financial_assistance", "legal_aid", "none"
            ]
        },
        "trend": {
            "type": "string",
            "enum": ["improving", "stable", "worsening", "insufficient_data"]
        }
    },
    "required": [
        "distress_score", "contributing_factors", "confidence",
        "explanation", "recommended_intervention", "trend"
    ]
}
```

**Do not modify this schema without updating `api-contracts.md` §3 and notifying Advay** — the aggregator's `push_score` endpoint validates against this shape.

## 4. Standard call pattern

```python
response = key_pool.generate(
    model="gemini-2.5-flash",
    contents=build_prompt(current_input, local_history_summary),
    config={
        "response_mime_type": "application/json",
        "response_schema": DistressSchema
    }
)
score_data = json.loads(response.text)
```

## 5. Error handling for malformed output

If `json.loads` fails or required fields are missing:
1. Retry once with the same prompt (transient issue, don't burn more than one retry)
2. If it fails again, fall back to:
   ```python
   {"distress_score": 0, "contributing_factors": [], "confidence": 0.0,
    "explanation": "Automated scoring unavailable for this interaction.",
    "recommended_intervention": "none", "trend": "insufficient_data"}
   ```
3. Log the raw failed response to a local debug file (never push it to the aggregator) for post-hoc review

## 6. Function-calling setup

See `agent-orchestration.md` §3 for the full `trigger_alert_function` declaration and the logic for when it's invoked. This file only owns the mechanics of the call itself — the *decision* to call it lives in the node service's orchestration code, not here.

## 7. Threshold constant

```python
DISTRESS_ALERT_THRESHOLD = 70  # out of 100
```

Defined once, here, imported everywhere. If it needs tuning during testing, change it in exactly one place.
