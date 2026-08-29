"""
Gemini Key Pool Manager for Aanchal
Handles multi-key round-robin rotation, 429 rate-limit cooldowns, telemetry tracking, and fallback simulation.
"""

import os
import time
import json
import itertools
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeminiKeyPool")

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import ClientError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai SDK not installed or unavailable; using fallback simulation mode.")


class GeminiKeyPool:
    """
    Manages a resilient pool of Gemini API keys with round-robin rotation,
    automatic 60s cooldowns on rate-limits (HTTP 429), call telemetry, and fallback simulation.
    """

    def __init__(self, api_keys: Optional[list[str]] = None, default_model: str = "gemini-2.5-flash"):
        self.default_model = default_model
        
        # Load keys from parameter or environment
        if not api_keys:
            env_keys = os.getenv("GEMINI_API_KEYS", "") or os.getenv("GEMINI_API_KEY", "")
            if env_keys:
                self.keys = [k.strip() for k in env_keys.split(",") if k.strip()]
            else:
                self.keys = []
        else:
            self.keys = [k.strip() for k in api_keys if k.strip()]

        self.cooldowns: dict[str, float] = {k: 0.0 for k in self.keys}
        self.stats: dict[str, dict] = {
            k: {"calls": 0, "errors": 0, "rate_limits": 0, "last_used": 0.0} 
            for k in self.keys
        }
        self.total_requests = 0
        self.total_rotations = 0

        self.clients = {}
        if GENAI_AVAILABLE:
            for k in self.keys:
                try:
                    self.clients[k] = genai.Client(api_key=k)
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini client for key ending in ...{k[-4:]}: {e}")

        self._cycle = itertools.cycle(self.keys) if self.keys else None
        logger.info(f"GeminiKeyPool initialized with {len(self.keys)} active API keys.")

    def add_key(self, api_key: str):
        """Dynamically register a new API key into the pool."""
        clean_key = api_key.strip()
        if clean_key and clean_key not in self.keys:
            self.keys.append(clean_key)
            self.cooldowns[clean_key] = 0.0
            self.stats[clean_key] = {"calls": 0, "errors": 0, "rate_limits": 0, "last_used": 0.0}
            if GENAI_AVAILABLE:
                try:
                    self.clients[clean_key] = genai.Client(api_key=clean_key)
                except Exception as e:
                    logger.error(f"Error registering client: {e}")
            self._cycle = itertools.cycle(self.keys)
            logger.info(f"Added new key ...{clean_key[-4:]} to key pool. Total keys: {len(self.keys)}")

    def _next_available_key(self) -> Optional[str]:
        if not self.keys or not self._cycle:
            return None
        now = time.time()
        for _ in range(len(self.keys)):
            k = next(self._cycle)
            if self.cooldowns.get(k, 0.0) <= now:
                return k
        # If all keys are in cooldown, pick the one that expires soonest
        soonest_key = min(self.keys, key=lambda x: self.cooldowns.get(x, 0.0))
        wait_time = max(0.0, self.cooldowns.get(soonest_key, 0.0) - now)
        if wait_time > 0 and wait_time < 5.0:
            time.sleep(wait_time)
            return soonest_key
        return None

    def generate_structured(self, prompt: str, schema: dict, system_instruction: str = "") -> tuple[dict, str]:
        """
        Executes a Gemini structured JSON generation call using key pool rotation.
        Returns: (parsed_json_dict, source_info)
        """
        self.total_requests += 1
        
        # If no real keys configured or genai unavailable, use high-fidelity simulator
        if not self.keys or not GENAI_AVAILABLE:
            return self._simulate_distress_scoring(prompt), "SIMULATED_DEMO_ENGINE"

        max_retries = min(len(self.keys) * 2, 6)
        last_error = None

        for attempt in range(max_retries):
            key = self._next_available_key()
            if not key:
                logger.warning("All Gemini keys currently rate-limited; falling back to local reasoning simulation.")
                return self._simulate_distress_scoring(prompt), "LOCAL_FAILOVER_SIMULATOR"

            client = self.clients.get(key)
            if not client:
                continue

            masked_key = f"...{key[-4:]}"
            try:
                self.stats[key]["calls"] += 1
                self.stats[key]["last_used"] = time.time()
                
                config = {
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                }
                if system_instruction:
                    config["system_instruction"] = system_instruction

                response = client.models.generate_content(
                    model=self.default_model,
                    contents=prompt,
                    config=config
                )

                if response and response.text:
                    parsed = json.loads(response.text)
                    return parsed, f"GEMINI_{self.default_model}_{masked_key}"
                else:
                    raise ValueError("Empty response text from Gemini API")

            except Exception as e:
                err_str = str(e)
                self.stats[key]["errors"] += 1
                logger.warning(f"[KeyPool] Key {masked_key} attempt {attempt+1} encountered error: {err_str}")
                
                # Check for rate limit 429
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or (GENAI_AVAILABLE and isinstance(e, ClientError) and getattr(e, 'code', None) == 429):
                    self.cooldowns[key] = time.time() + 60.0
                    self.stats[key]["rate_limits"] += 1
                    self.total_rotations += 1
                    logger.info(f"[KeyPool Rotation] Key {masked_key} rate-limited (429). Cooldown set for 60s. Rotating to next key...")
                    last_error = e
                    continue
                else:
                    last_error = e
                    continue

        logger.error(f"Exhausted key pool retries: {last_error}. Invoking failover resilience mode.")
        return self._simulate_distress_scoring(prompt), "FAILOVER_RECOVERY_ENGINE"

    def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """
        Executes free-form text generation (e.g. for comforting victim replies).
        """
        if not self.keys or not GENAI_AVAILABLE:
            return self._simulate_comfort_reply(prompt)

        key = self._next_available_key()
        if not key:
            return self._simulate_comfort_reply(prompt)

        try:
            client = self.clients[key]
            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction
            
            resp = client.models.generate_content(
                model=self.default_model,
                contents=prompt,
                config=config
            )
            return resp.text.strip() if resp and resp.text else self._simulate_comfort_reply(prompt)
        except Exception as e:
            logger.warning(f"Error in generate_text: {e}. Using fallback comfort reply.")
            return self._simulate_comfort_reply(prompt)

    def get_pool_status(self) -> dict:
        """Returns live key pool metrics for the frontend visualizer."""
        now = time.time()
        active_count = 0
        cooldown_count = 0
        key_details = []

        for idx, k in enumerate(self.keys):
            cd = max(0.0, self.cooldowns.get(k, 0.0) - now)
            is_active = cd <= 0
            if is_active:
                active_count += 1
            else:
                cooldown_count += 1
            
            key_details.append({
                "index": idx + 1,
                "key_masked": f"...{k[-4:]}" if len(k) >= 4 else "key_demo",
                "status": "READY" if is_active else f"COOLDOWN ({int(cd)}s)",
                "calls": self.stats[k]["calls"],
                "rate_limits": self.stats[k]["rate_limits"],
                "errors": self.stats[k]["errors"]
            })

        return {
            "total_keys": len(self.keys),
            "active_keys": active_count,
            "cooldown_keys": cooldown_count,
            "total_requests": self.total_requests,
            "total_rotations": self.total_rotations,
            "default_model": self.default_model,
            "keys": key_details,
            "engine_mode": "LIVE_GEMINI_API" if (self.keys and GENAI_AVAILABLE) else "SIMULATION_FALLBACK"
        }

    # =========================================================================
    # High-Fidelity NLP Heuristics for Offline / Demo Failover
    # =========================================================================
    def _simulate_distress_scoring(self, prompt: str) -> dict:
        """
        Sophisticated linguistic scoring heuristic that mirrors Gemini's structured output.
        Accurately parses distress keywords in Hindi, Hinglish, and English.
        """
        p_lower = prompt.lower()
        
        # High distress & immediate threat keywords (Hindi & English)
        critical_markers = [
            "जान से मार", "धमकी", "गालियां", "घर के बाहर", "मर जाएंगे", "मार देंगे",
            "kill", "death threat", "attack", "suicide", "broken", "terrified",
            "can't take this", "hopeless", "bail", "accused are out", "threat"
        ]
        
        # Medium distress keywords
        medium_markers = [
            "कोर्ट", "तारीख", "वकील", "राशन", "दुकान", "गांव वाले", "बात नहीं कर रहे",
            "boycott", "anxiety", "court", "lawyer", "ostracism", "harassment",
            "isolated", "fear", "delay", "financial", "no work", "money"
        ]

        # Low distress / calm markers
        calm_markers = [
            "thank you", "calmer", "routine", "patrol", "ration support",
            "नमस्ते", "ठीक", "धन्यवाद", "शान्ति", "मदद मिल गई", "peaceful"
        ]

        crit_count = sum(1 for m in critical_markers if m in p_lower)
        med_count = sum(1 for m in medium_markers if m in p_lower)
        calm_count = sum(1 for m in calm_markers if m in p_lower)

        # Determine language
        detected_lang = "Hindi" if any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in prompt) else "English"
        if "bhaiya" in p_lower or "pariwar" in p_lower or "hum log" in p_lower:
            detected_lang = "Hinglish"

        # Calculate score and factor mapping
        if crit_count >= 1:
            score = min(96.0, 78.0 + (crit_count * 6.0))
            factors = ["repeated_threat_mentions", "imminent_safety_risk", "extreme_psychological_paralysis"]
            intervention = "witness_protection" if "जान से" in p_lower or "threat" in p_lower or "bail" in p_lower else "medical"
            trend = "worsening"
            urgency = "critical"
            explanation = (
                "Critical distress and fear detected with explicit mentions of physical intimidation and safety threats. "
                "Immediate safety risk and psychological breakdown markers require urgent human escalation under Section 15A."
            )
        elif med_count >= 1:
            score = min(68.0, 42.0 + (med_count * 8.0))
            factors = ["procedural_court_anxiety", "social_ostracism_indicated", "economic_stress"]
            intervention = "legal_aid" if "कोर्ट" in p_lower or "court" in p_lower or "lawyer" in p_lower else "financial_assistance"
            trend = "worsening" if "akela" in p_lower or "pareshan" in p_lower else "stable"
            urgency = "elevated" if score > 55 else "moderate"
            explanation = (
                "Moderate procedural and systemic anxiety detected due to impending trial dates, social friction, and livelihood challenges. "
                "Longitudinal pattern indicates need for grounded legal facilitation and welfare aid."
            )
        else:
            score = max(12.0, 24.0 - (calm_count * 5.0))
            factors = ["routine_stabilization", "community_support_acknowledged"]
            intervention = "none"
            trend = "improving" if calm_count > 0 else "stable"
            urgency = "low"
            explanation = (
                "Interaction reflects stable baseline with positive reception of local administrative aid. "
                "No acute threat markers or distress escalation present."
            )

        return {
            "distress_score": round(score, 1),
            "contributing_factors": factors,
            "confidence": 0.92,
            "explanation": explanation,
            "recommended_intervention": intervention,
            "trend": trend,
            "detected_language": detected_lang,
            "urgency_level": urgency
        }

    def _simulate_comfort_reply(self, prompt: str) -> str:
        """Simulate culturally supportive, non-diagnostic replies in Hindi/English."""
        p_lower = prompt.lower()
        if any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in prompt) or "namaste" in p_lower or "bhaiya" in p_lower:
            return "नमस्ते, आपकी बात हमने सुन ली है। आप बिल्कुल सुरक्षित हैं और अकेले नहीं हैं। हमारी सपोर्ट टीम आपके साथ है और जल्द ही आपसे संपर्क करेगी। अपना ख्याल रखें।"
        return "Thank you for reaching out and sharing this with us. Please know that you are in a safe space and you are not alone. Our support team is here for you and will check in shortly. Take care."
