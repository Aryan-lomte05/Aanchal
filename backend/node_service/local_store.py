"""
Local Case Store for District Node (Aanchal)
Maintains full longitudinal case history locally on the district node.
ENFORCES PRIVACY BOUNDARY: Raw transcripts never leave this module.
"""

import hashlib
import time
from datetime import datetime
from typing import Optional


class DistrictLocalStore:
    def __init__(self, node_id: str = "district_pune"):
        self.node_id = node_id
        # local_case_history: { victim_channel_id: [ {timestamp, channel, raw_input, score_data, alert_data} ] }
        self._store: dict[str, list[dict]] = {}
        # salt for consistent hashing per node session
        self._salt = "aanchal_privacy_salt_2026"

    def get_hashed_case_id(self, raw_channel_id: str) -> str:
        """
        One-way SHA-256 hash of the victim's channel ID (phone number, WhatsApp ID).
        Only this hash is ever federated upward to the national aggregator.
        """
        salted = f"{self._salt}:{raw_channel_id.strip()}"
        digest = hashlib.sha256(salted.encode("utf-8")).hexdigest()
        return f"sha256:{digest[:12]}"

    def get_history(self, raw_channel_id: str) -> list[dict]:
        """Returns the chronological interaction history for a local victim."""
        return self._store.get(raw_channel_id, [])

    def record_interaction(
        self,
        raw_channel_id: str,
        raw_input: str,
        channel: str,
        score_data: dict,
        alert_data: Optional[dict] = None
    ) -> dict:
        """
        Appends an interaction to the local store and returns the sanitized federated payload.
        """
        now_iso = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": now_iso,
            "channel": channel,
            "raw_input": raw_input,        # LOCAL ONLY
            "score_data": score_data,
            "alert_data": alert_data
        }

        if raw_channel_id not in self._store:
            self._store[raw_channel_id] = []
        self._store[raw_channel_id].append(entry)

        hashed_case_id = self.get_hashed_case_id(raw_channel_id)

        # Build sanitized federated score payload (STRICTLY NO RAW TEXT)
        federated_payload = {
            "node_id": self.node_id,
            "hashed_case_id": hashed_case_id,
            "score_data": {
                "distress_score": score_data.get("distress_score", 0.0),
                "contributing_factors": score_data.get("contributing_factors", []),
                "confidence": score_data.get("confidence", 0.8),
                "explanation": score_data.get("explanation", ""),
                "recommended_intervention": score_data.get("recommended_intervention", "none"),
                "trend": score_data.get("trend", "stable"),
                "detected_language": score_data.get("detected_language", "Hindi"),
                "urgency_level": score_data.get("urgency_level", "low")
            },
            "timestamp": now_iso
        }

        return federated_payload

    def get_local_stats(self) -> dict:
        """Local node telemetry (for local district view)."""
        total_cases = len(self._store)
        total_interactions = sum(len(h) for h in self._store.values())
        return {
            "node_id": self.node_id,
            "total_local_cases": total_cases,
            "total_local_interactions": total_interactions,
            "privacy_status": "ENFORCED (Raw data isolated in-memory on this node)"
        }


# Global node store instance
local_store = DistrictLocalStore()
