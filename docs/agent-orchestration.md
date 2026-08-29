# agent-orchestration.md

This doc is the single source of truth for how Gemini is actually invoked, in what order, with what data. If `gemini-engine.md` is the "what" (schemas, keys, models), this is the "when and why."

## 1. The five Gemini jobs, and where each lives

| # | Job | Gemini capability used | Runs in |
|---|---|---|---|
| 1 | Understand a raw check-in (text or voice-transcribed) | Standard `generate_content` call, multilingual prompt | Node service, per interaction |
| 2 | Produce a scored, explainable output | Structured output (`response_schema=DistressSchema`) | Same call as #1 |
| 3 | Compare against personal baseline | Long context — full local history injected into the prompt | Same call as #1, via prompt construction |
| 4 | Decide and execute escalation | Function calling (`trigger_alert` function declared to the model) | Node service, immediately after #1-3 |
| 5 | Recommend a real intervention category | Enum-constrained field inside `DistressSchema` (not free text) | Part of #2's schema |

Jobs 1–3 happen in **one Gemini call**. Job 4 is a second call (or a tool-call turn in the same call, see §3). Job 5 is a field inside the first call's output, not a separate call — don't build a second "recommend intervention" prompt, that's redundant and burns quota.

## 2. Prompt construction (owned by Aryan, referenced by Advay for webhook integration)

```
SYSTEM PROMPT (fixed):
You are a distress-signal analysis engine supporting district welfare
officers monitoring victims under the SC/ST (Prevention of Atrocities)
Act. You do not diagnose. You flag patterns for human review only.
Respond ONLY in the required JSON schema. Be conservative — under
no circumstances should distress_score be inflated or deflated
based on assumptions not present in the input.

CONTEXT (dynamic, per victim, LOCAL ONLY — never logged outward):
Prior interactions: [chronological list of {timestamp, score, top_factors}]
(If no prior interactions: "This is the first recorded interaction.")

CURRENT INPUT:
Channel: {whatsapp|voice|web}
Language detected: {lang}
Raw content: {victim's message or transcribed speech}
```

Full history objects (not just scores) are also available locally for job #3's baseline comparison — the prompt above sends a *summary* of prior scores to keep token usage sane; if a session needs deeper comparison, the node service can inject more of the raw prior text, since that stays local to the node either way.

## 3. Function calling — the alert trigger

Declare one function to Gemini:

```python
trigger_alert_function = {
    "name": "trigger_alert",
    "description": "Escalate to a human counsellor or district officer when distress risk crosses a critical threshold.",
    "parameters": {
        "type": "object",
        "properties": {
            "urgency": {"type": "string", "enum": ["high", "critical"]},
            "reason": {"type": "string"},
            "recommended_immediate_action": {"type": "string"}
        },
        "required": ["urgency", "reason", "recommended_immediate_action"]
    }
}
```

Orchestration logic:
1. Node service always requests the structured `DistressSchema` output first (job #1-3, §1)
2. Node service checks `distress_score` in code (a simple `if score > THRESHOLD`) — **do not rely on the model to decide whether to call the function**; that's an unreliable pattern for a safety-critical trigger
3. If threshold is crossed, node service makes a second Gemini call, this time with `trigger_alert_function` as an available tool, asking Gemini to fill in `reason` and `recommended_immediate_action` using the same context
4. The actual "alert" (in our demo: a POST to the aggregator's `/federated/alert` endpoint + a visible log line) is executed by **our code**, using the function-call arguments Gemini returned — Gemini decides the content of the alert, our code decides that an alert fires

This split (code decides *whether*, Gemini decides *what*) is important — say this explicitly if a judge asks "what if Gemini hallucinates and doesn't call the function." It can't skip the alert; the threshold check is deterministic.

## 4. Sequence for one full interaction

```
Victim → Twilio webhook → Node Service
  1. Node builds prompt (system + local history summary + current input)
  2. Node → Gemini Engine.generate() → DistressSchema JSON
  3. Node appends to local_case_history[victim_id]
  4. Node → Aggregator: push_score(node_id, hash(victim_id), score_data)
  5. IF score_data.distress_score > THRESHOLD:
       Node → Gemini Engine.generate(tools=[trigger_alert_function])
       Node → Aggregator: push_alert(node_id, hash(victim_id), alert_data)
  6. Node replies to victim via Twilio (supportive, generic message —
     never reveals the score or "you seem distressed" language)
```

## 5. Rules for anyone touching this pipeline

- Never skip step 3 (local storage) — job #3 (baseline comparison) breaks silently without it, and you won't notice until a demo shows a flat score with no trend.
- Never let the victim-facing reply (step 6) leak the score or diagnostic language. The output channel is for support, not for exposing the AI's assessment.
- If you add a new channel (e.g. web form), it must call the **same** node-service function that WhatsApp/Voice call — don't fork the orchestration logic per channel. One function, multiple webhook entry points.
