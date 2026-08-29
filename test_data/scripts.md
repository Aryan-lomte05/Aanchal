# Synthetic Test Scripts for Multilingual Check-ins

These scripts are strictly synthetic and designed to test the Gemini scoring engine across various distress severity levels and languages without using any real victim data.

---

## Script 1: Routine Follow-up (Low Distress / Stable)
- **Channel**: WhatsApp
- **Language**: English
- **Expected Distress Score**: 10–25 / 100
- **Expected Intervention**: `none`
- **Trend**: `stable` / `improving`
- **Message Content**:
  > "Hello, just checking in. I was able to collect the ration support provided by the welfare officer yesterday. The local police station also conducted the routine patrol on our street. Feeling much calmer today, thank you."

---

## Script 2: Mild Procedural Anxiety (Low-to-Medium Distress)
- **Channel**: WhatsApp
- **Language**: Hindi (Devanagari)
- **Expected Distress Score**: 30–45 / 100
- **Expected Intervention**: `legal_aid` or `counselling`
- **Trend**: `stable`
- **Message Content**:
  > "नमस्ते, अगली कोर्ट तारीख अगले मंगलवार को है। मुझे वकील साहब से मिलने में थोड़ी घबराहट हो रही है और कागजात समझने में परेशानी हो रही है। कोई विशेष खतरा नहीं है, पर तारीख को लेकर थोड़ी चिंता है।"

---

## Script 3: Social Ostracism & Economic Pressure (Medium Distress)
- **Channel**: Voice / Transcribed Speech
- **Language**: Hinglish
- **Expected Distress Score**: 50–65 / 100
- **Expected Intervention**: `financial_assistance` or `counselling`
- **Trend**: `worsening`
- **Message Content**:
  > "Bhaiya gaon wale hamare pariwar se baat nahi kar rahe hain. Dukan se ration lene jao toh mana kar dete hain. Kaam bhi nahi mil raha hai pichle do hafte se. Hum log bohot pareshan aur akela mehsoos kar rahe hain."

---

## Script 4: Active Intimidation & Imminent Threat (High Distress / Alert Trigger)
- **Channel**: Voice / Transcribed Speech (Twilio Inbound)
- **Language**: Hindi (Devanagari / Transcribed)
- **Expected Distress Score**: 80–95 / 100 (`DISTRESS_ALERT_THRESHOLD` = 70 breached)
- **Expected Intervention**: `witness_protection` or `relocation`
- **Expected Action**: Fires `trigger_alert` function calling with `urgency: critical`
- **Message Content**:
  > "कल रात कुछ अनजान लोग मोटरसाइकिल पर हमारे घर के बाहर चक्कर लगा रहे थे और गालियां दे रहे थे। उन्होंने कहा कि अगर हमने बयान वापस नहीं लिया तो जान से मार देंगे। मैं और मेरे बच्चे बहुत डरे हुए हैं, हमें तुरंत मदद चाहिए, हम घर पर सुरक्षित नहीं हैं।"

---

## Script 5: Extreme Helplessness & Mental Breakdown (High Distress / Alert Trigger)
- **Channel**: WhatsApp
- **Language**: English
- **Expected Distress Score**: 85–98 / 100
- **Expected Intervention**: `counselling` / `medical`
- **Expected Action**: Fires `trigger_alert` function calling with `urgency: critical`
- **Message Content**:
  > "I cannot take this anymore. The trial has been delayed for the third time, the accused are out on bail walking past our door, and I haven't slept for four days. I feel completely broken, hopeless, and terrified for my children's lives."
