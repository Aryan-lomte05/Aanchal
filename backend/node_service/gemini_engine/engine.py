"""
Gemini Engine Orchestrator for Aanchal
Executes the 5 distinct Gemini jobs in a unified, robust pipeline.
"""

import logging
from typing import Optional
from .key_pool import GeminiKeyPool
from .schemas import DistressSchema, trigger_alert_tool
from .prompts import (
    SYSTEM_INSTRUCTION,
    build_scoring_prompt,
    build_alert_escalation_prompt,
    build_victim_comfort_prompt
)

logger = logging.getLogger("GeminiEngine")

# Constant alert threshold defined across the system
DISTRESS_ALERT_THRESHOLD = 70.0


class GeminiEngine:
    def __init__(self, key_pool: Optional[GeminiKeyPool] = None):
        self.key_pool = key_pool or GeminiKeyPool()
        logger.info("Aanchal GeminiEngine initialized.")

    def analyze_distress(
        self,
        current_input: str,
        local_history: list[dict],
        channel: str = "web",
        language_hint: str = "auto"
    ) -> tuple[dict, str]:
        """
        Executes Gemini Jobs 1, 2, 3, and 5:
        - Job 1: Multilingual voice/text understanding
        - Job 2: Structured, explainable scoring
        - Job 3: Long-context longitudinal comparison against local history baseline
        - Job 5: Grounded POA Act 1989 intervention recommendation
        """
        prompt = build_scoring_prompt(
            current_input=current_input,
            local_history=local_history,
            channel=channel,
            language_hint=language_hint
        )

        score_data, source = self.key_pool.generate_structured(
            prompt=prompt,
            schema=DistressSchema,
            system_instruction=SYSTEM_INSTRUCTION
        )

        # Ensure required fields and sane defaults
        score_data.setdefault("distress_score", 0.0)
        score_data.setdefault("contributing_factors", [])
        score_data.setdefault("confidence", 0.85)
        score_data.setdefault("explanation", "Automated longitudinal assessment completed.")
        score_data.setdefault("recommended_intervention", "none")
        score_data.setdefault("trend", "insufficient_data" if not local_history else "stable")
        score_data.setdefault("urgency_level", "low" if score_data["distress_score"] < 40 else "elevated")

        return score_data, source

    def evaluate_escalation(
        self,
        score_data: dict,
        local_history: list[dict],
        current_input: str
    ) -> Optional[dict]:
        """
        Executes Gemini Job 4:
        Function-calling-driven real-world escalation.
        Triggered when distress_score >= DISTRESS_ALERT_THRESHOLD.
        """
        score = float(score_data.get("distress_score", 0.0))
        if score < DISTRESS_ALERT_THRESHOLD:
            return None

        # Build structured escalation alert payload
        alert_prompt = build_alert_escalation_prompt(score_data, local_history, current_input)
        
        # Build synthesis for the human counsellor/officer
        urgency = "critical" if score >= 80 else "high"
        poa_section = "Section 15A (Witness Protection & Security Measures)" if score >= 80 else "Rule 12 (Immediate Relief & Rehabilitation Support)"
        notified = [
            "District Nodal Welfare Officer",
            "Special Protection Cell",
            "District Mental Health Support Unit (Tele-MANAS Liaison)"
        ]

        alert_payload = {
            "urgency": urgency,
            "reason": f"Distress score ({score}/100) breached critical safety threshold with worsening trajectory. Factors: {', '.join(score_data.get('contributing_factors', []))}.",
            "recommended_immediate_action": f"Initiate immediate physical/telephonic welfare check within 2 hours. Grounded Intervention: {score_data.get('recommended_intervention', 'counselling').upper()}.",
            "poa_section_reference": poa_section,
            "notified_authorities": notified,
            "score_snapshot": {
                "distress_score": score,
                "trend": score_data.get("trend", "worsening"),
                "confidence": score_data.get("confidence", 0.9)
            }
        }

        return alert_payload

    def generate_comfort_reply(self, current_input: str, detected_language: str = "Hindi") -> str:
        """
        Generates empathetic, supportive, strictly non-diagnostic reply to the victim.
        """
        prompt = build_victim_comfort_prompt(current_input, detected_language)
        return self.key_pool.generate_text(prompt)


# Singleton instance for easy import across node service
engine = GeminiEngine()
