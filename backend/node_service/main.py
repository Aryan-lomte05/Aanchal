"""
District Node Service - FastAPI Server for Aanchal
Handles Twilio WhatsApp & Voice webhooks, PWA Web Check-ins, Gemini Engine Orchestration,
Local Privacy Storage, and Federated Push to the National Aggregator.
"""

import os
import logging
import httpx
from typing import Optional
from fastapi import FastAPI, Form, Body, Request, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Twilio TwiML imports with fallback
try:
    from twilio.twiml.messaging_response import MessagingResponse
    from twilio.twiml.voice_response import VoiceResponse, Gather
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

from .gemini_engine import engine, DISTRESS_ALERT_THRESHOLD
from .local_store import DistrictLocalStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NodeService")

NODE_ID = os.getenv("NODE_ID", "district_pune")
AGGREGATOR_URL = os.getenv("AGGREGATOR_URL", "http://localhost:9000")

app = FastAPI(
    title=f"Aanchal District Node ({NODE_ID})",
    description="Local Privacy-Preserving Distress Analysis Node (SIH26094 · MoSJE)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend PWA static directory if present
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/pwa", StaticFiles(directory=frontend_path, html=True), name="frontend_pwa")

# Local isolated store for this node instance
node_store = DistrictLocalStore(node_id=NODE_ID)


class WebCheckinRequest(BaseModel):
    victim_id: str
    message: str
    channel: str = "web"
    language_hint: str = "Hindi"


async def push_score_to_aggregator(payload: dict):
    """Pushes sanitized federated score to the national aggregator."""
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.post(f"{AGGREGATOR_URL}/federated/push_score", json=payload)
            logger.info(f"Federated push to aggregator: HTTP {resp.status_code}")
    except Exception as e:
        logger.warning(f"Could not push score to aggregator ({AGGREGATOR_URL}): {e}")


async def push_alert_to_aggregator(alert_event: dict):
    """Pushes function-calling escalation alert to the national aggregator."""
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.post(f"{AGGREGATOR_URL}/federated/alert", json=alert_event)
            logger.info(f"Federated alert push to aggregator: HTTP {resp.status_code}")
    except Exception as e:
        logger.warning(f"Could not push alert to aggregator ({AGGREGATOR_URL}): {e}")


def process_interaction_core(
    victim_channel_id: str,
    raw_input: str,
    channel: str = "whatsapp",
    language_hint: str = "auto"
) -> dict:
    """
    Synchronous / Core orchestrator executing the 5 Gemini jobs end-to-end:
    1. Multilingual reasoning
    2. Structured scoring
    3. Longitudinal history comparison
    4. Deterministic threshold + Function Calling escalation
    5. Grounded POA Act intervention recommendation
    """
    # Step 1: Fetch local history baseline (NEVER leaves this node)
    local_history = node_store.get_history(victim_channel_id)

    # Step 2: Call Gemini Engine for structured scoring (Jobs 1, 2, 3, 5)
    score_data, engine_source = engine.analyze_distress(
        current_input=raw_input,
        local_history=local_history,
        channel=channel,
        language_hint=language_hint
    )

    # Step 3: Evaluate escalation threshold (Job 4 - Function Calling trigger)
    alert_data = engine.evaluate_escalation(
        score_data=score_data,
        local_history=local_history,
        current_input=raw_input
    )

    # Step 4: Record interaction in local-only memory and get sanitized federated payload
    federated_payload = node_store.record_interaction(
        raw_channel_id=victim_channel_id,
        raw_input=raw_input,
        channel=channel,
        score_data=score_data,
        alert_data=alert_data
    )

    # Step 5: Generate empathetic victim comfort reply
    comfort_reply = engine.generate_comfort_reply(
        current_input=raw_input,
        detected_language=score_data.get("detected_language", "Hindi")
    )

    return {
        "score_data": score_data,
        "alert_data": alert_data,
        "federated_payload": federated_payload,
        "comfort_reply": comfort_reply,
        "engine_source": engine_source
    }


# =============================================================================
# INBOUND TWILIO WEBHOOKS (Multi-Channel Live Ingestion)
# =============================================================================

@app.post("/whatsapp/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    """
    Twilio WhatsApp Webhook:
    Inbound message from victim -> Gemini analysis -> Federated push -> Supportive TwiML reply.
    """
    logger.info(f"[WhatsApp] Incoming message from {From[:6]}...")
    result = process_interaction_core(
        victim_channel_id=From,
        raw_input=Body,
        channel="whatsapp"
    )

    # Push score and alert asynchronously
    await push_score_to_aggregator(result["federated_payload"])
    if result["alert_data"]:
        alert_event = {
            "node_id": NODE_ID,
            "hashed_case_id": result["federated_payload"]["hashed_case_id"],
            "urgency": result["alert_data"]["urgency"],
            "reason": result["alert_data"]["reason"],
            "recommended_immediate_action": result["alert_data"]["recommended_immediate_action"],
            "poa_section_reference": result["alert_data"].get("poa_section_reference", ""),
            "timestamp": result["federated_payload"]["timestamp"]
        }
        await push_alert_to_aggregator(alert_event)

    # Generate TwiML response
    if TWILIO_AVAILABLE:
        resp = MessagingResponse()
        resp.message(result["comfort_reply"])
        return Response(content=str(resp), media_type="application/xml")
    else:
        xml_fallback = f"""<?xml version="1.0" encoding="UTF-8"?><Response><Message>{result["comfort_reply"]}</Message></Response>"""
        return Response(content=xml_fallback, media_type="application/xml")


@app.post("/voice/incoming")
async def voice_incoming():
    """
    Twilio Voice Webhook (Inbound Call):
    Prompts the caller in Hindi/English with speech-to-text Gather.
    """
    if TWILIO_AVAILABLE:
        resp = VoiceResponse()
        gather = Gather(
            input="speech",
            action="/voice/process",
            language="hi-IN",
            speechTimeout="auto",
            enhanced=True
        )
        gather.say("नमस्ते, आँचल सहायता केंद्र में आपका स्वागत है। कृपया बताएं कि आप कैसा महसूस कर रहे हैं।", language="hi-IN")
        resp.append(gather)
        return Response(content=str(resp), media_type="application/xml")
    else:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="/voice/process" language="hi-IN" speechTimeout="auto">
        <Say language="hi-IN">नमस्ते, आँचल सहायता केंद्र में आपका स्वागत है। कृपया बताएं कि आप कैसा महसूस कर रहे हैं।</Say>
    </Gather>
</Response>"""
        return Response(content=xml, media_type="application/xml")


@app.post("/voice/process")
async def voice_process(SpeechResult: Optional[str] = Form(None), From: str = Form("voice_anonymous")):
    """
    Twilio Voice Speech Processor:
    Transcribed speech from victim -> Gemini analysis -> Federated push -> Spoken TwiML reply.
    """
    text = SpeechResult or "नमस्ते, मैं ठीक हूँ।"
    logger.info(f"[Voice STT] Processed speech transcript: \"{text[:40]}...\"")

    result = process_interaction_core(
        victim_channel_id=From,
        raw_input=text,
        channel="voice"
    )

    await push_score_to_aggregator(result["federated_payload"])
    if result["alert_data"]:
        alert_event = {
            "node_id": NODE_ID,
            "hashed_case_id": result["federated_payload"]["hashed_case_id"],
            "urgency": result["alert_data"]["urgency"],
            "reason": result["alert_data"]["reason"],
            "recommended_immediate_action": result["alert_data"]["recommended_immediate_action"],
            "poa_section_reference": result["alert_data"].get("poa_section_reference", ""),
            "timestamp": result["federated_payload"]["timestamp"]
        }
        await push_alert_to_aggregator(alert_event)

    reply = result["comfort_reply"]
    if TWILIO_AVAILABLE:
        resp = VoiceResponse()
        resp.say(reply, language="hi-IN")
        return Response(content=str(resp), media_type="application/xml")
    else:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?><Response><Say language="hi-IN">{reply}</Say></Response>"""
        return Response(content=xml, media_type="application/xml")


# =============================================================================
# WEB PWA & DEMO SANDBOX ENDPOINTS
# =============================================================================

@app.post("/api/checkin")
async def web_checkin(req: WebCheckinRequest):
    """
    Aanchal Saathi PWA Web Check-in endpoint:
    Processes user check-in from browser microphone or text box.
    """
    result = process_interaction_core(
        victim_channel_id=req.victim_id,
        raw_input=req.message,
        channel=req.channel,
        language_hint=req.language_hint
    )

    # Federated score push
    await push_score_to_aggregator(result["federated_payload"])

    # Federated alert push if triggered
    if result["alert_data"]:
        alert_event = {
            "node_id": NODE_ID,
            "hashed_case_id": result["federated_payload"]["hashed_case_id"],
            "urgency": result["alert_data"]["urgency"],
            "reason": result["alert_data"]["reason"],
            "recommended_immediate_action": result["alert_data"]["recommended_immediate_action"],
            "poa_section_reference": result["alert_data"].get("poa_section_reference", ""),
            "timestamp": result["federated_payload"]["timestamp"]
        }
        await push_alert_to_aggregator(alert_event)

    return {
        "status": "success",
        "comfort_reply": result["comfort_reply"],
        "hashed_case_id": result["federated_payload"]["hashed_case_id"],
        "score_data": result["score_data"],
        "alert_triggered": result["alert_data"] is not None,
        "alert_data": result["alert_data"],
        "engine_source": result["engine_source"]
    }


@app.post("/api/simulate")
async def simulate_script(payload: dict = Body(...)):
    """
    1-Click Hackathon Demo Simulator:
    Directly injects synthetic scripts (from test_data/scripts.md) into the full pipeline.
    """
    victim_id = payload.get("victim_id", "sim_victim_01")
    message = payload.get("message", "Routine follow up check in")
    channel = payload.get("channel", "whatsapp")
    language = payload.get("language", "Hindi")

    result = process_interaction_core(
        victim_channel_id=victim_id,
        raw_input=message,
        channel=channel,
        language_hint=language
    )

    await push_score_to_aggregator(result["federated_payload"])
    if result["alert_data"]:
        alert_event = {
            "node_id": NODE_ID,
            "hashed_case_id": result["federated_payload"]["hashed_case_id"],
            "urgency": result["alert_data"]["urgency"],
            "reason": result["alert_data"]["reason"],
            "recommended_immediate_action": result["alert_data"]["recommended_immediate_action"],
            "poa_section_reference": result["alert_data"].get("poa_section_reference", ""),
            "timestamp": result["federated_payload"]["timestamp"]
        }
        await push_alert_to_aggregator(alert_event)

    return {
        "status": "simulated",
        "result": result
    }


@app.get("/api/keypool/status")
async def get_keypool_status():
    """Returns live telemetry of the Gemini Key Pool."""
    return engine.key_pool.get_pool_status()


@app.get("/api/node/stats")
async def get_node_stats():
    """Returns local node status and case count."""
    return node_store.get_local_stats()


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "node_service",
        "node_id": NODE_ID,
        "threshold": DISTRESS_ALERT_THRESHOLD
    }
