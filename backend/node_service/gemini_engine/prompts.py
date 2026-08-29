"""
Gemini Engine - Prompts & Prompt Builders for Aanchal
Enforces privacy preservation, longitudinal context injection, and non-diagnostic framing.
"""

import json

SYSTEM_INSTRUCTION = """
You are the AI core of Aanchal, a specialized distress-signal monitoring companion built to assist District Welfare Officers and counsellors under the Scheduled Castes and the Scheduled Tribes (Prevention of Atrocities) Act, 1989 (MoSJE).

CRITICAL OPERATIONAL BOUNDARIES:
1. NON-DIAGNOSTIC: You do NOT provide clinical medical diagnoses. You evaluate distress signals, psychological vulnerability, threat perception, and social pressure to flag patterns for HUMAN REVIEW ONLY.
2. OBJECTIVITY: Be conservative and calibrated. Never inflate or deflate distress scores based on assumptions not supported by the evidence in the interaction.
3. EXPLAINABILITY: Always provide a clear, factual explanation summarizing the linguistic and contextual reasoning behind your assessment.
4. GROUNDED INTERVENTIONS: Map recommended interventions strictly to the statutory schemes defined in the POA Act 1989 (counselling, medical, witness_protection, relocation, financial_assistance, legal_aid, none).
5. LONGITUDINAL TRAJECTORY: Compare the current interaction against the provided historical baseline. Note whether distress is improving, stable, or worsening over time.
6. OUTPUT FORMAT: Respond strictly in the specified JSON schema.
""".strip()


def build_scoring_prompt(current_input: str, local_history: list[dict], channel: str = "web", language_hint: str = "auto") -> str:
    """
    Constructs the prompt for Jobs 1, 2, 3, and 5:
    Multilingual comprehension, structured scoring, longitudinal baseline comparison, and grounded recommendation.
    """
    history_summary = []
    if not local_history:
        history_text = "Baseline: This is the victim's first recorded interaction with the Aanchal system."
    else:
        for idx, item in enumerate(local_history, start=1):
            sc = item.get("score_data", {})
            history_summary.append(
                f"- Session {idx} ({item.get('timestamp', 'past')} via {item.get('channel', 'unknown')}): "
                f"Distress Score: {sc.get('distress_score', 'N/A')}/100, "
                f"Factors: {', '.join(sc.get('contributing_factors', []))}, "
                f"Trend: {sc.get('trend', 'N/A')}, "
                f"Intervention: {sc.get('recommended_intervention', 'none')}"
            )
        history_text = "Prior Local Interaction Baseline (held securely on this district node):\n" + "\n".join(history_summary)

    prompt = f"""
{history_text}

CURRENT INTERACTION INPUT:
- Channel: {channel}
- Language Hint: {language_hint}
- Raw Interaction Content:
\"\"\"{current_input}\"\"\"

TASK:
1. Analyze the raw message/transcription for emotional distress, threat indicators, helplessness, court anxiety, social ostracism, or fear.
2. Compare the emotional state against the prior interaction baseline to establish the longitudinal trend ('improving', 'stable', 'worsening', or 'insufficient_data').
3. Assign an objective distress score between 0 and 100.
4. Provide structured contributing factor category tags (generic tags only, never verbatim quote sensitive PII).
5. Recommend the most appropriate statutory intervention category under the POA Act 1989.
6. Provide a concise, plain-language explainability paragraph for the human welfare officer.
""".strip()

    return prompt


def build_alert_escalation_prompt(distress_data: dict, local_history: list[dict], current_input: str) -> str:
    """
    Constructs the prompt for Job 4: Function calling escalation tool invocation.
    """
    return f"""
EMERGENCY ESCALATION EVALUATION:
A distress threshold breach has occurred (Distress Score: {distress_data.get('distress_score')}/100, Urgency: {distress_data.get('urgency_level', 'critical')}).

ASSESSMENT DETAILS:
- Factors: {json.dumps(distress_data.get('contributing_factors', []))}
- Explanation: {distress_data.get('explanation', '')}
- Recommended Intervention: {distress_data.get('recommended_intervention', 'none')}
- Trend: {distress_data.get('trend', 'worsening')}

CURRENT CONTEXT:
\"\"\"{current_input}\"\"\"

Invoke the 'trigger_alert' tool immediately with high/critical urgency, structured rationale, immediate action plan, and POA Act statutory references.
""".strip()


def build_victim_comfort_prompt(current_input: str, detected_language: str = "Hindi") -> str:
    """
    Constructs prompt for generating empathetic, culturally reassuring, non-diagnostic response.
    """
    return f"""
You are Aanchal Saathi, a gentle, compassionate, and culturally supportive companion for individuals navigating difficult life situations.
The user just sent the following message:
\"\"\"{current_input}\"\"\"

Generate a short (2-3 sentences max) comforting response in the language/dialect of the user (Default: {detected_language}).
CRITICAL RULES:
- Never mention scores, assessments, mental health diagnoses, or monitoring.
- Acknowledge their feelings with warmth and reassurance.
- Remind them that they are safe and support is available whenever they wish.
- Keep it natural, human, respectful, and comforting.
""".strip()
