"""
National Aggregator Service - FastAPI Server for Aanchal
Receives ONLY anonymized scores and alert events from district nodes.
Serves Dashboard REST APIs for District, State, and National MoSJE portals.
"""

import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from .national_view import aggregator_store, PrivacyViolationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AggregatorService")

app = FastAPI(
    title="Aanchal National Aggregator Service",
    description="Federated Anonymized Score Aggregator & Dashboard API (SIH26094 · MoSJE)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OfficerActionRequest(BaseModel):
    alert_id: str
    action: str  # "MARK_CONTACTED" | "ESCALATE_POLICE" | "ASSIGN_COUNSELLOR" | "DISMISS_FALSE_POSITIVE" | "RESOLVE"
    officer_notes: Optional[str] = None


@app.post("/federated/push_score")
async def push_score(payload: dict = Body(...)):
    """
    Receives federated distress scores from district nodes.
    STRICT PRIVACY CHECK: Automatically rejected if raw text or phone numbers are present.
    """
    try:
        res = aggregator_store.record_score(payload)
        logger.info(f"[Federated Push] Received score {payload.get('score_data', {}).get('distress_score')} from {payload.get('node_id')} ({payload.get('hashed_case_id')})")
        return res
    except PrivacyViolationError as pe:
        logger.error(f"[PRIVACY VIOLATION REJECTED] {pe}")
        raise HTTPException(status_code=422, detail=str(pe))
    except Exception as e:
        logger.error(f"Error recording score: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/federated/alert")
async def push_alert(alert_payload: dict = Body(...)):
    """
    Receives function-calling-driven escalation alerts from district nodes.
    """
    try:
        res = aggregator_store.record_alert(alert_payload)
        logger.warning(f"[ALERT TRIGGERED] Urgency: {alert_payload.get('urgency')} from {alert_payload.get('node_id')} for {alert_payload.get('hashed_case_id')}")
        return res
    except PrivacyViolationError as pe:
        logger.error(f"[PRIVACY VIOLATION REJECTED] {pe}")
        raise HTTPException(status_code=422, detail=str(pe))
    except Exception as e:
        logger.error(f"Error recording alert: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dashboard/summary")
async def get_dashboard_summary():
    """
    Polled by the frontend dashboard every 3 seconds.
    Provides national counts, district node summaries, live alerts, and privacy audit packets.
    """
    return aggregator_store.get_summary()


@app.get("/dashboard/node/{node_id}")
async def get_node_dashboard(node_id: str):
    """
    Returns the district-level view (hashed victim cases and score trajectories).
    """
    return aggregator_store.get_node_detail(node_id)


@app.post("/dashboard/action")
async def perform_officer_action(req: OfficerActionRequest):
    """
    Officer workflow state transitions on live alerts.
    """
    success = aggregator_store.update_alert_action(
        alert_id=req.alert_id,
        action=req.action,
        officer_notes=req.officer_notes
    )
    if not success:
        raise HTTPException(status_code=404, detail="Alert ID not found")
    return {"status": "action_recorded", "alert_id": req.alert_id, "action": req.action}


@app.get("/dashboard/privacy_audit")
async def get_privacy_audit():
    """Returns real-time privacy verification log."""
    return {"audit_stream": aggregator_store.privacy_audit_log}


@app.post("/dashboard/reset_seed")
async def reset_seed():
    """Resets simulator data for fresh demo rehearsals."""
    global aggregator_store
    aggregator_store = NationalAggregatorStore()
    return {"status": "reset_successful"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "aggregator_service",
        "active_districts": len(aggregator_store.nodes)
    }
