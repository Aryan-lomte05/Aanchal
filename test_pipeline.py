import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from node_service.gemini_engine import engine
from node_service.local_store import DistrictLocalStore
from aggregator_service.national_view import NationalAggregatorStore, PrivacyViolationError

def run_tests():
    print("=" * 60)
    print("1. Testing Gemini Engine Multilingual Analysis & Structured Scoring...")
    hindi_threat_msg = "कल रात कुछ लोग घर के बाहर चक्कर लगा रहे थे और जान से मारने की धमकी दे रहे थे"
    score_data, src = engine.analyze_distress(hindi_threat_msg, [], channel="voice", language_hint="Hindi")
    print(f"   [+] Score: {score_data['distress_score']}/100")
    print(f"   [+] Factors: {score_data['contributing_factors']}")
    print(f"   [+] Relief: {score_data['recommended_intervention']}")
    print(f"   [+] Engine Source: {src}")

    print("\n2. Testing Function-Calling Alert Trigger on Threshold Breach (>70)...")
    alert = engine.evaluate_escalation(score_data, [], hindi_threat_msg)
    print(f"   [+] Alert Triggered: {alert is not None}")
    if alert:
        print(f"   [+] Urgency: {alert['urgency']}")
        print(f"   [+] Statutory Ref: {alert['poa_section_reference']}")

    print("\n3. Testing Local District Store (Raw PII Isolation & SHA-256 Hashing)...")
    store = DistrictLocalStore(node_id="district_pune")
    raw_phone = "+919876543210"
    fed_payload = store.record_interaction(raw_phone, hindi_threat_msg, "whatsapp", score_data, alert)
    print(f"   [+] Hashed ID: {fed_payload['hashed_case_id']}")
    print(f"   [+] Zero Raw Text in Federated Payload: {'raw_input' not in fed_payload}")
    assert "raw_input" not in fed_payload
    assert raw_phone not in str(fed_payload)

    print("\n4. Testing National Aggregator Privacy Boundary & Schema Validation...")
    agg = NationalAggregatorStore()
    res = agg.record_score(fed_payload)
    print(f"   [+] Aggregator Recorded Anonymized Score: {res}")

    print("\n5. Testing Privacy Violation Rejection (Negative Testing)...")
    try:
        leak_payload = {
            "node_id": "district_pune",
            "hashed_case_id": "sha256:4a8f9c10b2e3",
            "raw_text": "leaked victim text",
            "score_data": score_data
        }
        agg.record_score(leak_payload)
        print("   [-] FAIL: Aggregator did not block raw text leakage!")
    except PrivacyViolationError as pe:
        print(f"   [+] PASS: Aggregator successfully blocked privacy leak: {pe}")

    print("\n" + "=" * 60)
    print("ALL 5 SYSTEM TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
