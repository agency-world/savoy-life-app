import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

# --- CONFIG & THEME ---
st.set_page_config(page_title="Savoy Nexus v4", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .agent-box { background: #0f172a; color: #38bdf8; font-family: 'Courier New'; padding: 15px; border-radius: 10px; font-size: 0.85rem; }
    .wellness-card { background: white; padding: 25px; border-radius: 20px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .handoff-box { background: #eff6ff; border-left: 5px solid #3b82f6; padding: 20px; border-radius: 10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- SYNTHETIC DATA ENGINE ---
def generate_market_data():
    residents = [
        {"id": "MC402", "name": "Margaret Chen", "age": 84, "meds": ["Furosemide", "Lisinopril"], "poa": "Jane Chen", "social_baseline": 4.5},
        {"id": "AM112", "name": "Arthur Miller", "age": 89, "meds": ["Donepezil", "Metformin"], "poa": "Robert Miller", "social_baseline": 2.2}
    ]
    times = [datetime.now() - timedelta(hours=x) for x in range(24)]
    sensors = pd.DataFrame({
        "Time": times,
        "Heart_Rate": [random.randint(72, 88) for _ in range(24)],
        "Social_Engagement": [random.uniform(0, 1.2) for _ in range(24)], # Hrs out of room
        "Mobility_Index": [random.randint(40, 95) for _ in range(24)]
    })
    return residents, sensors

RESIDENTS, SENSORS = generate_market_data()

# --- SIDEBAR & PERSONA ROUTING ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.title("Savoy Nexus v4")
    persona = st.selectbox("Switch Workspace", ["CareGiver (Shift View)", "POA (Family Portal)", "Executive (Facility Admin)"])
    st.divider()
    st.metric("Admin Burden Reduced", "142 mins", "Today", delta_color="normal")
    st.success("QHIN Pipeline: Active")
    st.info("Agent Swarm: 4 Bots Online")

# --- AGENTIC ORCHESTRATION ---
def run_agent_swarm(persona_type):
    logs = [
        "Synthesizer: Merging Sensor_ID_402 with EHR_Med_History...",
        "Clinical_Reasoner: High Nocturia correlated with new Diuretic (82% confidence)",
        "Social_Analyst: Detected 25% drop in communal dining participation",
        f"Architect: Formatting output for {persona_type}..."
    ]
    return logs

# --- MAIN INTERFACE ---
st.title(f"📍 {persona} Command Center")

if persona == "CareGiver (Shift View)":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📋 Virtual Rounding & AI Handoff")
        res = RESIDENTS[0]
        st.markdown("**AI-Generated Shift Summary (Handoff Bot):**")
        st.markdown(f"""<div class="handoff-box">
            "Margaret had a restless night (3 bathroom trips). Vitals remain stable, but her morning mobility is sluggish. 
            <b>SDoH Alert:</b> She skipped breakfast in the hall. Suggest 1:1 interaction during lunch pass."
            </div>""", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Ambient Clinical Notes")
        note = st.text_area("Dictate or type observation:", "Margaret seems withdrawn and tired. Refused walk.")
        if st.button("Sync to Care Plan"):
            st.success("Note Analyzed: Added 'Social Withdrawal' and 'Fatigue' to Clinical Dashboard.")

    with col2:
        st.subheader("Agent Swarm Logs")
        st.markdown(f'<div class="agent-log">{"<br>".join(run_agent_swarm("Nurse"))}</div>', unsafe_allow_html=True)
        st.divider()
        st.write("### Care Tasks")
        st.checkbox("Check Orthostatic BP", value=False)
        st.checkbox("Medication Pass: Complete", value=True)

elif persona == "POA (Family Portal)":
    res = RESIDENTS[0]
    st.header(f"Wellness for {res['name']}")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown(f"""<div class="wellness-card">
            <p style="color: #64748b; font-weight: bold;">OVERALL WELLNESS</p>
            <h1 style="color: #3b82f6; font-size: 4rem; margin: 0;">82</h1>
            <p style="color: #10b981;">Target: 85+</p>
            </div>""", unsafe_allow_html=True)
    
    with col_b:
        st.subheader("Discovery Bot: Wellness FAQ")
        q = st.text_input("Ask about Margaret's day:", "Is she eating well?")
        if q:
            st.info("Margaret enjoyed her lunch but skipped breakfast today. Her care team is monitoring her hydration.")
    
    st.divider()
    st.subheader("Legal & POA Vault")
    st.write(f"Authorized POA: **{res['poa']}**")
    st.button("Review Medical Power of Attorney Documents")

else: # Executive Admin
    st.subheader("Facility Efficiency & Risk Heatmap")
    st.metric("ER Transfer Avoidance", "$18,400", "This Month")
    st.bar_chart(SENSORS.set_index("Time")["Mobility_Index"])
    st.error("High Risk: Margaret Chen (Room 402) - 88% probability of fall within 48h.")

# --- FOOTER ---
st.divider()
st.caption("Savoy Nexus // Founding Technical Strategy Prototype v4 // HIPAA-Safe Simulated Environment")
