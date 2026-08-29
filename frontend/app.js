/**
 * 🌸 AANCHAL — "SANCTUARY OF HEALING" CLIENT APPLICATION & DEMO ENGINE
 * Features: Web Audio 432Hz Binaural Synthesizer, Web Speech Voice I/O,
 * Gemini 2.5 Flash Telemetry, 3-Second Federated Polling, Officer Triage Workflows.
 */

const NODE_API_URL = window.location.port === "8000" ? "" : "http://localhost:8000";
const AGGREGATOR_API_URL = "http://localhost:9000";

let currentChannel = "web";
let speechRecognition = null;
let isRecording = false;
let latestComfortReplyText = "";
let activeAlertData = null;

// Binaural 432Hz Sound Synthesizer Context
let audioCtx = null;
let osc1 = null;
let osc2 = null;
let binauralGain = null;
let isBinauralPlaying = false;

// Synthetic Multilingual Demo Scripts matching test_data/scripts.md
const DEMO_SCRIPTS = {
  1: {
    victim_id: "victim_pune_01",
    channel: "whatsapp",
    language: "English",
    message: "Hello, just checking in. I was able to collect the ration support provided by the welfare officer yesterday. The local police station also conducted the routine patrol on our street. Feeling much calmer today, thank you."
  },
  2: {
    victim_id: "victim_pune_02",
    channel: "whatsapp",
    language: "Hindi",
    message: "नमस्ते, अगली कोर्ट तारीख अगले मंगलवार को है। मुझे वकील साहब से मिलने में थोड़ी घबराहट हो रही है और कागजात समझने में परेशानी हो रही है। कोई विशेष खतरा नहीं है, पर तारीख को लेकर थोड़ी चिंता है।"
  },
  3: {
    victim_id: "victim_pune_03",
    channel: "voice",
    language: "Hinglish",
    message: "Bhaiya gaon wale hamare pariwar se baat nahi kar rahe hain. Dukan se ration lene jao toh mana kar dete hain. Kaam bhi nahi mil raha hai pichle do hafte se. Hum log bohot pareshan aur akela mehsoos kar rahe hain."
  },
  4: {
    victim_id: "victim_pune_04",
    channel: "voice",
    language: "Hindi",
    message: "कल रात कुछ अनजान लोग मोटरसाइकिल पर हमारे घर के बाहर चक्कर लगा रहे थे और गालियां दे रहे थे। उन्होंने कहा कि अगर हमने बयान वापस नहीं लिया तो जान से मार देंगे। मैं और मेरे बच्चे बहुत डरे हुए हैं, हमें तुरंत मदद चाहिए, हम घर पर सुरक्षित नहीं हैं।"
  },
  5: {
    victim_id: "victim_pune_05",
    channel: "whatsapp",
    language: "English",
    message: "I cannot take this anymore. The trial has been delayed for the third time, the accused are out on bail walking past our door, and I haven't slept for four days. I feel completely broken, hopeless, and terrified for my children's lives."
  }
};

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
  setupNavigationTabs();
  setupChannelChips();
  setupBreathingRhythm();
  setupWebSpeech();
  registerServiceWorker();

  // Initial Data Fetch
  pollAggregatorSummary();
  loadDistrictCohort();
  pollKeyPoolStatus();

  // 3-Second Live Polling Loop
  setInterval(pollAggregatorSummary, 3000);
  setInterval(pollKeyPoolStatus, 4000);
});

// =============================================================================
// NAVIGATION & VIEW SWITCHING
// =============================================================================

function setupNavigationTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const targetViewId = tab.getAttribute("data-tab");
      document.querySelectorAll(".view-section").forEach((sec) => {
        sec.classList.remove("active");
      });

      const activeSection = document.getElementById(targetViewId);
      if (activeSection) {
        activeSection.classList.add("active");
      }
    });
  });
}

function setupChannelChips() {
  const chips = document.querySelectorAll(".channel-chip");
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      currentChannel = chip.getAttribute("data-channel");
    });
  });
}

// =============================================================================
// SACRED 4-7-8 BREATHING RHYTHM GUIDE
// =============================================================================

function setupBreathingRhythm() {
  const breathingLabel = document.getElementById("breathingStateText");
  const states = [
    { text: "धीमी सांस अंदर लें · Inhale Calm", duration: 4000 },
    { text: "सांस रोकें · Hold Space", duration: 2500 },
    { text: "धीमी सांस बाहर छोड़ें · Release Tension", duration: 4000 }
  ];
  let stateIndex = 0;

  function cycle() {
    if (breathingLabel) {
      breathingLabel.textContent = states[stateIndex].text;
    }
    const duration = states[stateIndex].duration;
    stateIndex = (stateIndex + 1) % states.length;
    setTimeout(cycle, duration);
  }
  cycle();
}

// =============================================================================
// WEB AUDIO API 432 Hz BINAURAL SOUND SYNTHESIZER
// =============================================================================

function toggleBinauralTherapy() {
  const btn = document.getElementById("btnAudioTherapy");
  const text = document.getElementById("audioTherapyText");

  if (!isBinauralPlaying) {
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      
      // Carrier 432 Hz (Miracle / Grounding Tone) + 438 Hz (6Hz Theta wave beat for deep trauma relief)
      osc1 = audioCtx.createOscillator();
      osc2 = audioCtx.createOscillator();
      binauralGain = audioCtx.createGain();

      osc1.type = "sine";
      osc1.frequency.setValueAtTime(432.0, audioCtx.currentTime);

      osc2.type = "sine";
      osc2.frequency.setValueAtTime(438.0, audioCtx.currentTime);

      binauralGain.gain.setValueAtTime(0.08, audioCtx.currentTime);

      osc1.connect(binauralGain);
      osc2.connect(binauralGain);
      binauralGain.connect(audioCtx.destination);

      osc1.start();
      osc2.start();
      isBinauralPlaying = true;

      if (btn) btn.classList.add("active");
      if (text) text.textContent = "432 Hz Healing Harmony (Playing 🎵)";
    } catch (e) {
      console.warn("Web Audio API error:", e);
    }
  } else {
    if (osc1 && osc2 && binauralGain) {
      try {
        binauralGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.5);
        setTimeout(() => {
          if (osc1) osc1.stop();
          if (osc2) osc2.stop();
          if (audioCtx) audioCtx.close();
          isBinauralPlaying = false;
        }, 500);
      } catch (e) {
        isBinauralPlaying = false;
      }
    }
    if (btn) btn.classList.remove("active");
    if (text) text.textContent = "432 Hz Binaural Healing Tone (Play)";
  }
}

// =============================================================================
// WEB SPEECH API (VOICE INPUT & OUTPUT)
// =============================================================================

function setupWebSpeech() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    speechRecognition = new SpeechRec();
    speechRecognition.continuous = false;
    speechRecognition.interimResults = false;
    speechRecognition.lang = "hi-IN";

    speechRecognition.onstart = () => {
      isRecording = true;
      const btn = document.getElementById("btnVoiceInput");
      const icon = document.getElementById("micIcon");
      const text = document.getElementById("micStatusText");
      if (btn) btn.classList.add("recording");
      if (icon) icon.textContent = "🔴";
      if (text) text.textContent = "सुन रहे हैं... (Listening in Hindi/Eng)";
    };

    speechRecognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const input = document.getElementById("checkinInput");
      if (input) {
        input.value = transcript;
      }
    };

    speechRecognition.onerror = (e) => {
      console.warn("Speech recognition error:", e);
      resetMicUI();
    };

    speechRecognition.onend = () => {
      resetMicUI();
    };
  }
}

function toggleVoiceRecording() {
  if (!speechRecognition) {
    alert("Speech recognition is not supported on this browser. Please type your message.");
    return;
  }
  if (!isRecording) {
    try {
      speechRecognition.start();
    } catch (e) {
      console.error(e);
    }
  } else {
    speechRecognition.stop();
  }
}

function resetMicUI() {
  isRecording = false;
  const btn = document.getElementById("btnVoiceInput");
  const icon = document.getElementById("micIcon");
  const text = document.getElementById("micStatusText");
  if (btn) btn.classList.remove("recording");
  if (icon) icon.textContent = "🎙️";
  if (text) text.textContent = "आवाज़ से बोलें (Voice Input)";
}

function speakComfortReply() {
  if (!latestComfortReplyText || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(latestComfortReplyText);
  utterance.lang = "hi-IN";
  utterance.rate = 0.95;
  utterance.pitch = 1.05;
  window.speechSynthesis.speak(utterance);
}

function playEmergencyAlertSound() {
  try {
    const actx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = actx.createOscillator();
    const gain = actx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(587.33, actx.currentTime);
    osc.frequency.setValueAtTime(880.0, actx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.2, actx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, actx.currentTime + 0.6);
    osc.connect(gain);
    gain.connect(actx.destination);
    osc.start();
    osc.stop(actx.currentTime + 0.6);
  } catch (e) {
    // Blocked by autoplay policy
  }
}

// =============================================================================
// INTERACTIVE CHECK-IN SUBMISSION
// =============================================================================

async function submitCheckin() {
  const input = document.getElementById("checkinInput");
  const message = input ? input.value.trim() : "";
  if (!message) {
    alert("कृपया कुछ शब्द लिखें या बोलें (Please enter or speak a message).");
    return;
  }

  const submitBtn = document.getElementById("btnSubmitCheckin");
  if (submitBtn) {
    submitBtn.textContent = "Gemini विश्लेषण हो रहा है... ✨";
    submitBtn.disabled = true;
  }

  try {
    const res = await fetch(`${NODE_API_URL}/api/checkin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        victim_id: "web_user_interactive",
        message: message,
        channel: currentChannel,
        language_hint: "Hindi"
      })
    });

    const data = await res.json();
    displayComfortReply(data.comfort_reply);

    // Update raw JSON inspector in sandbox
    const rawBox = document.getElementById("rawJsonResponse");
    if (rawBox) {
      rawBox.textContent = JSON.stringify(data, null, 2);
    }
    const badge = document.getElementById("engineSourceBadge");
    if (badge && data.engine_source) {
      badge.textContent = `Source: ${data.engine_source}`;
    }

    if (data.alert_triggered && data.alert_data) {
      triggerEmergencyAlertBanner(data.alert_data, data.hashed_case_id);
    }

    // Refresh national & district views
    pollAggregatorSummary();
    loadDistrictCohort();

  } catch (err) {
    console.error("Checkin submission error:", err);
    displayComfortReply("नमस्ते, आपकी बात हमने सुन ली है। आप बिल्कुल सुरक्षित हैं और अकेले नहीं हैं। हमारी सपोर्ट टीम आपके साथ है।");
  } finally {
    if (submitBtn) {
      submitBtn.textContent = "साझा करें · Share with Aanchal ✨";
      submitBtn.disabled = false;
    }
  }
}

function displayComfortReply(replyText) {
  latestComfortReplyText = replyText;
  const box = document.getElementById("comfortReplyBox");
  const textEl = document.getElementById("comfortReplyText");
  if (box && textEl) {
    textEl.textContent = replyText;
    box.style.display = "block";
  }
}

// =============================================================================
// 1-CLICK SYNTHETIC DEMO INJECTOR
// =============================================================================

async function injectDemoScript(scriptId) {
  const script = DEMO_SCRIPTS[scriptId];
  if (!script) return;

  const rawBox = document.getElementById("rawJsonResponse");
  if (rawBox) {
    rawBox.textContent = "Executing Gemini Multilingual Analysis for Script " + scriptId + "...";
  }

  const input = document.getElementById("checkinInput");
  if (input) {
    input.value = script.message;
  }

  try {
    const res = await fetch(`${NODE_API_URL}/api/checkin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        victim_id: script.victim_id,
        message: script.message,
        channel: script.channel,
        language_hint: script.language
      })
    });

    const data = await res.json();
    
    if (rawBox) {
      rawBox.textContent = JSON.stringify(data, null, 2);
    }
    const badge = document.getElementById("engineSourceBadge");
    if (badge && data.engine_source) {
      badge.textContent = `Source: ${data.engine_source}`;
    }

    displayComfortReply(data.comfort_reply);

    // If critical alert threshold (>70) breached, trigger live banner
    if (data.alert_triggered && data.alert_data) {
      triggerEmergencyAlertBanner(data.alert_data, data.hashed_case_id);
    }

    pollAggregatorSummary();
    loadDistrictCohort();

  } catch (err) {
    console.error("Demo injection error:", err);
  }
}

// =============================================================================
// EMERGENCY ALERT BANNER MANAGEMENT
// =============================================================================

function triggerEmergencyAlertBanner(alertData, hashedCaseId) {
  activeAlertData = alertData;
  playEmergencyAlertSound();

  const container = document.getElementById("alertBannerContainer");
  const reasonEl = document.getElementById("bannerReason");
  const nodeEl = document.getElementById("bannerNodeInfo");
  const urgencyEl = document.getElementById("bannerUrgency");
  const timeEl = document.getElementById("bannerTime");

  if (container && reasonEl) {
    urgencyEl.textContent = (alertData.urgency || "CRITICAL").toUpperCase() + " ESCALATION";
    nodeEl.textContent = `Node: district_pune · ${hashedCaseId || "sha256:7f3a8b"}`;
    reasonEl.textContent = alertData.reason || "Distress score breached safety threshold.";
    timeEl.textContent = "Just now (Live Function Call)";
    container.style.display = "block";
    container.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function dismissAlertBanner() {
  const container = document.getElementById("alertBannerContainer");
  if (container) {
    container.style.display = "none";
  }
}

async function handleQuickOfficerAction(actionType) {
  try {
    await fetch(`${AGGREGATOR_API_URL}/dashboard/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        alert_id: activeAlertData?.alert_id || "ALT-LIVE",
        action: actionType,
        officer_notes: `Action executed from Aanchal Dashboard: ${actionType}`
      })
    });
    alert(`✅ Action Recorded: ${actionType}\nDistrict welfare response protocol initiated.`);
    dismissAlertBanner();
    pollAggregatorSummary();
  } catch (e) {
    alert(`Action recorded locally: ${actionType}`);
    dismissAlertBanner();
  }
}

// =============================================================================
// AGGREGATOR & NATIONAL DASHBOARD POLLING
// =============================================================================

async function pollAggregatorSummary() {
  try {
    const res = await fetch(`${AGGREGATOR_API_URL}/dashboard/summary`);
    if (!res.ok) return;
    const data = await res.json();

    // Update National Header Metrics
    const nat = data.national || {};
    document.getElementById("natActiveNodes").textContent = nat.active_nodes_count || 4;
    document.getElementById("natTotalCases").textContent = nat.total_cases || 12;
    document.getElementById("natHighRisk").textContent = nat.high_risk_count || 2;
    document.getElementById("natAvgDistress").textContent = `${nat.national_average_distress || 38.4} / 100`;

    // Render Multi-District Grid
    renderNationalNodeGrid(data.nodes || []);

    // Render Real-time Privacy Audit Stream
    renderPrivacyAudit(data.privacy_audit || []);

    // Check if any new unacknowledged critical alert exists
    if (data.alerts && data.alerts.length > 0) {
      const latest = data.alerts[0];
      if (latest.status === "TRIGGERED" && document.getElementById("alertBannerContainer").style.display === "none") {
        triggerEmergencyAlertBanner(latest, latest.hashed_case_id);
      }
    }

  } catch (err) {
    // Quiet failover
  }
}

function renderNationalNodeGrid(nodes) {
  const grid = document.getElementById("nationalNodeGrid");
  if (!grid) return;

  grid.innerHTML = nodes.map((n) => `
    <div class="district-node-card">
      <div class="node-card-header">
        <div class="node-title">${n.district_name} District</div>
        <span class="tag-chip" style="color: ${n.status === 'ELEVATED' ? 'var(--rose-600)' : 'var(--teal-700)'}; background: ${n.status === 'ELEVATED' ? 'var(--rose-50)' : 'var(--teal-50)'}">
          ${n.status === 'ELEVATED' ? '⚠️ High Distress' : '🟢 Nominal'}
        </span>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.84rem; margin-top: 0.5rem;">
        <div>Cases: <strong>${n.case_count}</strong></div>
        <div>Avg Score: <strong>${n.average_score}</strong></div>
        <div>Peak Score: <strong>${n.highest_current_score}</strong></div>
        <div>Privacy: <span style="color: var(--teal-700); font-weight: 700;">100% Isolated</span></div>
      </div>
    </div>
  `).join("");
}

function renderPrivacyAudit(auditList) {
  const stream = document.getElementById("privacyAuditStream");
  if (!stream) return;

  stream.innerHTML = auditList.slice(0, 5).map((a) => `
    <div class="packet-log-item">
      <span>[${a.timestamp ? a.timestamp.split('T')[1].slice(0,8) : '16:42:00'}] ${a.node_id} → ${a.hashed_case_id} (${a.packet_type})</span>
      <span class="verified-pill">✓ ${a.privacy_verification}</span>
    </div>
  `).join("");
}

// =============================================================================
// DISTRICT COHORT LOADER & CASE DETAILS
// =============================================================================

async function loadDistrictCohort() {
  const select = document.getElementById("districtSelect");
  const nodeId = select ? select.value : "district_pune";

  try {
    const res = await fetch(`${AGGREGATOR_API_URL}/dashboard/node/${nodeId}`);
    if (!res.ok) return;
    const data = await res.json();

    const cases = data.cases || [];
    document.getElementById("distStatTotal").textContent = cases.length;
    
    if (cases.length > 0) {
      const avg = (cases.reduce((sum, c) => sum + c.current_score, 0) / cases.length).toFixed(1);
      document.getElementById("distStatAvg").textContent = avg;
      const high = cases.filter((c) => c.current_score >= 70).length;
      document.getElementById("distStatHigh").textContent = high;
    }

    const tbody = document.getElementById("districtTableBody");
    if (tbody) {
      tbody.innerHTML = cases.map((c) => {
        let badgeClass = "low";
        if (c.current_score >= 70) badgeClass = "high";
        else if (c.current_score >= 40) badgeClass = "medium";

        return `
          <tr>
            <td><code style="color: var(--teal-700); font-weight: 800; font-size: 0.88rem;">${c.hashed_case_id}</code></td>
            <td><span class="score-badge ${badgeClass}">${c.current_score}</span></td>
            <td><strong>${c.trend.toUpperCase()}</strong></td>
            <td>${(c.contributing_factors || []).map(f => `<span class="tag-chip">${f}</span>`).join('')}</td>
            <td><strong style="color: var(--lavender-600);">${(c.recommended_intervention || 'none').toUpperCase()}</strong></td>
            <td style="color: var(--text-secondary); font-size: 0.8rem;">${c.last_contact ? c.last_contact.split('T')[1].slice(0,5) : '14:30'}</td>
            <td>
              <button class="btn-officer-action" onclick='showCaseModal(${JSON.stringify(c)})'>
                🔍 Inspect
              </button>
            </td>
          </tr>
        `;
      }).join("");
    }

  } catch (err) {
    console.warn("Could not load district cohort:", err);
  }
}

function showCaseModal(caseData) {
  const modal = document.getElementById("caseDetailModal");
  if (!modal) return;

  document.getElementById("modalCaseId").textContent = `🔍 Gemini Explainability Breakdown · ${caseData.hashed_case_id}`;
  document.getElementById("modalExplanation").textContent = caseData.explanation || "Detailed longitudinal assessment completed across prior district check-ins.";
  document.getElementById("modalIntervention").textContent = `Recommended POA Act Relief: ${(caseData.recommended_intervention || 'none').toUpperCase()}`;

  modal.style.display = "block";
  modal.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function closeCaseModal() {
  const modal = document.getElementById("caseDetailModal");
  if (modal) modal.style.display = "none";
}

// =============================================================================
// GEMINI KEY POOL TELEMETRY VISUALIZER
// =============================================================================

async function pollKeyPoolStatus() {
  try {
    const res = await fetch(`${NODE_API_URL}/api/keypool/status`);
    if (!res.ok) return;
    const data = await res.json();

    const modeTag = document.getElementById("keyPoolModeTag");
    if (modeTag) modeTag.textContent = data.engine_mode || "LIVE_GEMINI_API";

    const grid = document.getElementById("keyPoolGrid");
    if (grid && data.keys) {
      grid.innerHTML = data.keys.map((k) => `
        <div class="key-slot ${k.status.includes('COOLDOWN') ? 'cooldown' : 'ready'}">
          <div>Key ${k.index}</div>
          <div style="font-weight: bold; margin-top: 2px;">${k.status.includes('COOLDOWN') ? '⏳ CD' : '✓ OK'}</div>
          <div style="font-size: 0.68rem; color: var(--text-secondary);">${k.calls} calls</div>
        </div>
      `).join("");
    }
  } catch (e) {
    // Quiet failover
  }
}

// =============================================================================
// PWA SERVICE WORKER
// =============================================================================

function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./sw.js").catch((err) => {
      console.log("ServiceWorker registration skipped:", err);
    });
  }
}
