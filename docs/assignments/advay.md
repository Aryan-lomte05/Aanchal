# assignments/advay.md

**Role:** Full Stack + DevOps & Infrastructure Lead
**Owns:** `api-contracts.md` (implementation + integrity), FastAPI Microservices, Twilio Multi-Channel Gateways, ngrok Live Tunneling, Privacy Boundary Firewall, Aggregator Rollup Engine

---

## 1. Advanced Architecture Scope

1. **Dual FastAPI Microservices (`backend/`):**
   - `node_service` (Port 8000): Local District Node handling Twilio WhatsApp webhook, Twilio Voice STT/TTS Gather endpoint, and direct PWA `/api/checkin` gateway.
   - `aggregator_service` (Port 9000): Centralized National Aggregator handling federated score ingestion and dashboard rollups.

2. **Strict Privacy Boundary Technical Firewall:**
   - Implement programmatic payload inspection at `/federated/push_score` and `/federated/alert`.
   - Reject any incoming request with HTTP 422 containing forbidden fields (raw messages, phone numbers, transcripts, or unhashed identifiers).

3. **Multi-District Simulation Engine:**
   - Seed and serve 4 live district nodes (`district_pune`, `district_nagpur`, `district_patna`, `district_varanasi`) with realistic longitudinal cohorts.
   - Maintain real-time privacy verification audit logs proving zero raw PII bytes cross the wire.

4. **Officer Action State Machine (`POST /dashboard/action`):**
   - Handle triage state transitions (`MARK_CONTACTED`, `ESCALATE_POLICE`, `ASSIGN_COUNSELLOR`, `DISMISS_FALSE_POSITIVE`, `RESOLVE`).

---

## 2. Deliverables & Timeline

### Night before
- [ ] FastAPI skeleton for both `backend/node_service` and `backend/aggregator_service` matching `api-contracts.md`
- [ ] Twilio account setup: WhatsApp sandbox joined, Voice-capable number provisioned
- [ ] ngrok installed and verified (`ngrok http 8000`)
- [ ] Implement and test `PrivacyViolationError` middleware rejecting malformed/leaked payloads

### Round 1 (10:00 AM – 1:00 PM)
- [ ] `POST /whatsapp/webhook` and `POST /voice/incoming` + `POST /voice/process` wired to Aryan's `process_interaction_core()`
- [ ] Basic aggregator skeleton: `POST /federated/push_score` accepting and storing sanitized payloads
- [ ] Confirm one real WhatsApp message and voice call round-trips with TwiML responses

### Round 2 (1:30 PM – 5:00 PM)
- [ ] `POST /federated/alert` real-time escalation receiver
- [ ] `GET /dashboard/summary` and `GET /dashboard/node/{node_id}` fast 3-second polling endpoints
- [ ] `POST /dashboard/action` officer triage state updates
- [ ] Test multi-node data aggregation across simulated districts

### Last 30–45 min (Freeze & Rehearsal)
- [ ] Verify ngrok URLs are live in Twilio console settings
- [ ] Run full live demo flow with Netal (WhatsApp message → Voice call → Live alert pop)
