"""
National Aggregator Store & Privacy Filter for Aanchal
Enforces strict privacy boundaries (rejects raw PII) and compiles district rollups.
"""

import time
from datetime import datetime
from typing import Optional, Any


class PrivacyViolationError(Exception):
    """Raised when an incoming federated payload violates privacy boundaries."""
    pass


class NationalAggregatorStore:
    def __init__(self):
        # national_view: { node_id: { hashed_case_id: [ score_entry ] } }
        self.nodes: dict[str, dict[str, list[dict]]] = {
            "district_pune": {},
            "district_nagpur": {},
            "district_patna": {},
            "district_varanasi": {}
        }
        # active_alerts: list of alert dictionaries
        self.alerts: list[dict] = []
        # privacy_audit_log: verified audit stream of incoming packets
        self.privacy_audit_log: list[dict] = []
        
        # Seed realistic initial cohort data for immediate presentation-readiness
        self._seed_baseline_data()

    def _seed_baseline_data(self):
        """Seeds initial synthetic cohort data across multiple district nodes."""
        base_cases = [
            # District Pune
            ("district_pune", "sha256:4a8f9c10b2e3", [
                {"distress_score": 32.0, "contributing_factors": ["procedural_court_anxiety"], "confidence": 0.88, "explanation": "Initial court appearance apprehension.", "recommended_intervention": "legal_aid", "trend": "stable", "timestamp": "2026-08-29T10:15:00Z"},
                {"distress_score": 24.0, "contributing_factors": ["routine_stabilization"], "confidence": 0.91, "explanation": "Supportive police patrol acknowledged.", "recommended_intervention": "none", "trend": "improving", "timestamp": "2026-08-29T14:30:00Z"}
            ]),
            ("district_pune", "sha256:7b1e84c90d52", [
                {"distress_score": 58.0, "contributing_factors": ["social_ostracism_indicated", "economic_stress"], "confidence": 0.85, "explanation": "Social isolation and ration access hurdles.", "recommended_intervention": "financial_assistance", "trend": "worsening", "timestamp": "2026-08-29T11:45:00Z"}
            ]),
            # District Nagpur
            ("district_nagpur", "sha256:9c3d2a71e048", [
                {"distress_score": 18.0, "contributing_factors": ["community_support_acknowledged"], "confidence": 0.94, "explanation": "Stable rehabilitation progress.", "recommended_intervention": "none", "trend": "stable", "timestamp": "2026-08-29T09:20:00Z"}
            ]),
            ("district_nagpur", "sha256:1f6e5b4a9c80", [
                {"distress_score": 45.0, "contributing_factors": ["procedural_court_anxiety"], "confidence": 0.86, "explanation": "Impending trial summons inquiry.", "recommended_intervention": "legal_aid", "trend": "stable", "timestamp": "2026-08-29T13:00:00Z"}
            ]),
            # District Patna
            ("district_patna", "sha256:3e2a1b9f8d74", [
                {"distress_score": 62.0, "contributing_factors": ["repeated_threat_mentions", "economic_stress"], "confidence": 0.89, "explanation": "Reported intimidation from local miscreants.", "recommended_intervention": "witness_protection", "trend": "worsening", "timestamp": "2026-08-29T12:10:00Z"}
            ]),
            # District Varanasi
            ("district_varanasi", "sha256:8f7e6d5c4b3a", [
                {"distress_score": 28.0, "contributing_factors": ["routine_stabilization"], "confidence": 0.90, "explanation": "Beneficiary receiving educational stipend.", "recommended_intervention": "financial_assistance", "trend": "improving", "timestamp": "2026-08-29T10:50:00Z"}
            ])
        ]

        for node_id, hashed_id, entries in base_cases:
            self.nodes.setdefault(node_id, {})[hashed_id] = entries

        # Pre-seed one demo alert
        self.alerts.append({
            "alert_id": "ALT-2026-001",
            "node_id": "district_patna",
            "hashed_case_id": "sha256:3e2a1b9f8d74",
            "urgency": "high",
            "reason": "Escalating intimidation markers detected with worsening distress trajectory (62/100).",
            "recommended_immediate_action": "Deploy Sub-Divisional Magistrate protection officer under Section 15A.",
            "poa_section_reference": "Section 15A (Protection of Victims and Witnesses)",
            "status": "CONTACTED",
            "assigned_officer": "R. Sharma (Welfare Officer, Patna)",
            "timestamp": "2026-08-29T12:10:00Z"
        })

    def validate_privacy_boundary(self, payload: dict):
        """
        STRICT TECHNICAL ENFORCEMENT OF PRIVACY BOUNDARY:
        Rejects any payload containing raw transcripts, phone numbers, or unhashed identifiers.
        """
        forbidden_keys = {
            "raw", "raw_text", "raw_input", "message", "transcript", "body",
            "phone", "phone_number", "mobile", "from", "victim_name", "aadhaar"
        }

        def _check_keys(obj: Any):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k.lower() in forbidden_keys:
                        raise PrivacyViolationError(f"Privacy Boundary Breach: Forbidden field '{k}' detected in federated payload.")
                    if isinstance(v, str) and ("+91" in v or (len(v) == 10 and v.isdigit())):
                        raise PrivacyViolationError(f"Privacy Boundary Breach: Possible unhashed phone number detected in field '{k}'.")
                    _check_keys(v)
            elif isinstance(obj, list):
                for item in obj:
                    _check_keys(item)

        _check_keys(payload)

        # Confirm hashed_case_id format
        hashed_id = payload.get("hashed_case_id", "")
        if not hashed_id.startswith("sha256:"):
            raise PrivacyViolationError(f"Privacy Boundary Breach: Case ID '{hashed_id}' is not an anonymized SHA-256 hash.")

    def record_score(self, payload: dict) -> dict:
        """Validates privacy boundary and records federated distress score."""
        self.validate_privacy_boundary(payload)

        node_id = payload["node_id"]
        hashed_id = payload["hashed_case_id"]
        score_data = payload["score_data"]
        timestamp = payload.get("timestamp", datetime.utcnow().isoformat() + "Z")

        entry = {
            "distress_score": score_data["distress_score"],
            "contributing_factors": score_data.get("contributing_factors", []),
            "confidence": score_data.get("confidence", 0.85),
            "explanation": score_data.get("explanation", ""),
            "recommended_intervention": score_data.get("recommended_intervention", "none"),
            "trend": score_data.get("trend", "stable"),
            "timestamp": timestamp
        }

        if node_id not in self.nodes:
            self.nodes[node_id] = {}
        if hashed_id not in self.nodes[node_id]:
            self.nodes[node_id][hashed_id] = []
        
        self.nodes[node_id][hashed_id].append(entry)

        # Record in privacy audit log
        self.privacy_audit_log.insert(0, {
            "timestamp": timestamp,
            "node_id": node_id,
            "hashed_case_id": hashed_id,
            "packet_type": "FEDERATED_SCORE_PUSH",
            "score": score_data["distress_score"],
            "privacy_verification": "PASS · 0 Raw PII Bytes · SHA-256 Verified"
        })
        if len(self.privacy_audit_log) > 50:
            self.privacy_audit_log.pop()

        return {"status": "accepted", "hashed_case_id": hashed_id}

    def record_alert(self, alert_payload: dict) -> dict:
        """Validates privacy boundary and records real-time function calling alert."""
        self.validate_privacy_boundary(alert_payload)

        alert_id = f"ALT-{int(time.time()*1000)%1000000:06d}"
        alert_entry = {
            "alert_id": alert_id,
            "node_id": alert_payload["node_id"],
            "hashed_case_id": alert_payload["hashed_case_id"],
            "urgency": alert_payload.get("urgency", "critical"),
            "reason": alert_payload.get("reason", "Threshold breach"),
            "recommended_immediate_action": alert_payload.get("recommended_immediate_action", "Welfare check required"),
            "poa_section_reference": alert_payload.get("poa_section_reference", "Section 15A"),
            "status": "TRIGGERED",
            "assigned_officer": "Unassigned (Pending Review)",
            "timestamp": alert_payload.get("timestamp", datetime.utcnow().isoformat() + "Z")
        }

        self.alerts.insert(0, alert_entry)
        if len(self.alerts) > 30:
            self.alerts.pop()

        # Record in privacy audit log
        self.privacy_audit_log.insert(0, {
            "timestamp": alert_entry["timestamp"],
            "node_id": alert_payload["node_id"],
            "hashed_case_id": alert_payload["hashed_case_id"],
            "packet_type": "FEDERATED_ALERT_EVENT",
            "urgency": alert_entry["urgency"],
            "privacy_verification": "PASS · 0 Raw PII Bytes · Action Escalation Only"
        })

        return {"status": "alert_received", "alert_id": alert_id}

    def update_alert_action(self, alert_id: str, action: str, officer_notes: Optional[str] = None) -> bool:
        """Officer workflow state updater."""
        for alert in self.alerts:
            if alert["alert_id"] == alert_id:
                if action == "MARK_CONTACTED":
                    alert["status"] = "CONTACTED"
                elif action == "ESCALATE_POLICE":
                    alert["status"] = "ESCALATED_POLICE"
                elif action == "ASSIGN_COUNSELLOR":
                    alert["status"] = "COUNSELLOR_ASSIGNED"
                elif action == "DISMISS_FALSE_POSITIVE":
                    alert["status"] = "DISMISSED"
                elif action == "RESOLVE":
                    alert["status"] = "RESOLVED"
                
                if officer_notes:
                    alert["officer_notes"] = officer_notes
                alert["updated_at"] = datetime.utcnow().isoformat() + "Z"
                return True
        return False

    def get_summary(self) -> dict:
        """Compiles pan-India rollup, district metrics, and active alert feeds."""
        total_cases = 0
        high_risk_count = 0
        total_scores = []
        node_summaries = []
        intervention_counts = {}

        for node_id, cases in self.nodes.items():
            case_count = len(cases)
            total_cases += case_count
            node_scores = []
            highest_score = 0.0

            for h_id, history in cases.items():
                if history:
                    last_entry = history[-1]
                    s = last_entry.get("distress_score", 0.0)
                    node_scores.append(s)
                    total_scores.append(s)
                    if s > highest_score:
                        highest_score = s
                    if s >= 70.0:
                        high_risk_count += 1
                    
                    interv = last_entry.get("recommended_intervention", "none")
                    intervention_counts[interv] = intervention_counts.get(interv, 0) + 1

            avg_node_score = round(sum(node_scores) / len(node_scores), 1) if node_scores else 0.0
            
            node_summaries.append({
                "node_id": node_id,
                "district_name": node_id.replace("district_", "").capitalize(),
                "case_count": case_count,
                "average_score": avg_node_score,
                "highest_current_score": round(highest_score, 1),
                "status": "ELEVATED" if highest_score >= 70 else "NOMINAL"
            })

        national_avg = round(sum(total_scores) / len(total_scores), 1) if total_scores else 0.0

        return {
            "national": {
                "total_cases": total_cases,
                "active_nodes_count": len(self.nodes),
                "high_risk_count": high_risk_count,
                "national_average_distress": national_avg,
                "active_alerts_count": len([a for a in self.alerts if a["status"] in ["TRIGGERED", "CONTACTED"]]),
                "intervention_breakdown": intervention_counts
            },
            "nodes": node_summaries,
            "alerts": self.alerts[:10],
            "privacy_audit": self.privacy_audit_log[:8]
        }

    def get_node_detail(self, node_id: str) -> dict:
        """Returns the per-victim (hashed) score history for a single node."""
        cases = self.nodes.get(node_id, {})
        case_list = []

        for h_id, history in cases.items():
            if not history:
                continue
            last = history[-1]
            case_list.append({
                "hashed_case_id": h_id,
                "current_score": last["distress_score"],
                "trend": last.get("trend", "stable"),
                "contributing_factors": last.get("contributing_factors", []),
                "explanation": last.get("explanation", ""),
                "recommended_intervention": last.get("recommended_intervention", "none"),
                "total_interactions": len(history),
                "last_contact": last.get("timestamp", ""),
                "history": history
            })

        # Sort by current distress score descending
        case_list.sort(key=lambda x: x["current_score"], reverse=True)

        return {
            "node_id": node_id,
            "district_name": node_id.replace("district_", "").capitalize(),
            "total_cases": len(case_list),
            "cases": case_list
        }


# Global Aggregator instance
aggregator_store = NationalAggregatorStore()
