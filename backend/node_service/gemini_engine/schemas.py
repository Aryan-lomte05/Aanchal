"""
Gemini Engine - Schemas & Function Declarations for Aanchal
SIH26094 · Ministry of Social Justice and Empowerment
"""

# Grounded Intervention Categories under SC/ST (Prevention of Atrocities) Act 1989
INTERVENTION_CATEGORIES = [
    "counselling",            # Psychological & trauma counselling (Rule 12/MoSJE)
    "medical",                # Emergency medical aid / psychiatric evaluation
    "witness_protection",    # Section 15A: Special witness protection measures
    "relocation",             # Emergency relocation / safe shelter support
    "financial_assistance",   # Section 15A(6) / Rule 12 Immediate financial relief
    "legal_aid",              # Legal assistance & Special Public Prosecutor
    "none"                    # Routine observation, no immediate statutory intervention
]

TREND_CATEGORIES = [
    "improving",
    "stable",
    "worsening",
    "insufficient_data"
]

# JSON Schema for Job 2 & 5: Structured, explainable scoring & grounded intervention
DistressSchema = {
    "type": "object",
    "properties": {
        "distress_score": {
            "type": "number",
            "description": "Calculated distress level on a strict 0 to 100 scale based on psychological indicators, threat perception, and trauma markers.",
            "minimum": 0,
            "maximum": 100
        },
        "contributing_factors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Short standardized category tags describing key distress factors (e.g., 'repeated_threat_mentions', 'social_boycott_indicated', 'procedural_court_anxiety', 'sleep_deprivation_fatigue'). Never quotes raw victim text directly."
        },
        "confidence": {
            "type": "number",
            "description": "Confidence score of the assessment between 0.0 and 1.0 based on linguistic clarity and input context depth.",
            "minimum": 0.0,
            "maximum": 1.0
        },
        "explanation": {
            "type": "string",
            "description": "Plain-language, objective, explainable justification for welfare officers explaining why this score was assigned. Strictly non-diagnostic."
        },
        "recommended_intervention": {
            "type": "string",
            "enum": INTERVENTION_CATEGORIES,
            "description": "Statutory relief category grounded in the SC/ST (POA) Act 1989 and MoSJE welfare rules."
        },
        "trend": {
            "type": "string",
            "enum": TREND_CATEGORIES,
            "description": "Longitudinal trend compared against the victim's prior baseline sessions held locally on this node."
        },
        "detected_language": {
            "type": "string",
            "description": "Primary language or dialect detected in the check-in (e.g., 'Hindi', 'Hinglish', 'English', 'Marathi', etc.)."
        },
        "urgency_level": {
            "type": "string",
            "enum": ["low", "moderate", "elevated", "critical"],
            "description": "Overall urgency indicator derived from distress score and trajectory."
        }
    },
    "required": [
        "distress_score",
        "contributing_factors",
        "confidence",
        "explanation",
        "recommended_intervention",
        "trend"
    ]
}

# Function Calling Declaration for Job 4: Escalation trigger to human welfare authorities
trigger_alert_tool = {
    "name": "trigger_alert",
    "description": "Escalates an urgent intervention alert to district nodal officers, counsellors, or police when distress crosses critical safety thresholds.",
    "parameters": {
        "type": "object",
        "properties": {
            "urgency": {
                "type": "string",
                "enum": ["high", "critical"],
                "description": "Severity of the escalation trigger."
            },
            "reason": {
                "type": "string",
                "description": "Synthesis of the risk factors triggering this alert without quoting raw personal identifiers."
            },
            "recommended_immediate_action": {
                "type": "string",
                "description": "Specific immediate action required by the district welfare team within 2-4 hours."
            },
            "poa_section_reference": {
                "type": "string",
                "description": "Relevant statutory section under SC/ST (POA) Act (e.g., 'Section 15A - Protection of Victims and Witnesses', 'Rule 12 - Relief and Rehabilitation')."
            },
            "notified_authorities": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Designated departments to alert (e.g., ['District Nodal Counsellor', 'Sub-Divisional Magistrate', 'Special Police Unit'])."
            }
        },
        "required": ["urgency", "reason", "recommended_immediate_action"]
    }
}
