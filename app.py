import streamlit as st
import pandas as pd
import json
import os
import datetime

# Import mock data configuration
from mock_data import (
    INITIAL_GATES,
    INITIAL_PITCH_ZONES,
    INITIAL_STAFF,
    INITIAL_CONCESSIONS,
    INITIAL_INFRASTRUCTURE,
    INITIAL_INCIDENTS,
    ROLE_CHECKLISTS
)

# Import Core AI agent logic from the engine
from engine.ai_agent import parse_incident_report

# Page configuration
st.set_page_config(
    page_title="Vanguard Pitch-Pilot | Stadium Ops Command",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path to local persistent storage for incidents
INCIDENTS_FILE = "stadium_incidents.json"

# State persistence helper functions
def load_incidents():
    if os.path.exists(INCIDENTS_FILE):
        try:
            with open(INCIDENTS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return INITIAL_INCIDENTS.copy()
    return INITIAL_INCIDENTS.copy()

def save_incidents(incidents):
    try:
        with open(INCIDENTS_FILE, "w") as f:
            json.dump(incidents, f, indent=4)
    except Exception as e:
        st.sidebar.error(f"Error saving incidents: {e}")

# Session State Initialization
if "gates" not in st.session_state:
    st.session_state.gates = INITIAL_GATES.copy()
if "pitch_zones" not in st.session_state:
    st.session_state.pitch_zones = INITIAL_PITCH_ZONES.copy()
if "staff" not in st.session_state:
    st.session_state.staff = INITIAL_STAFF.copy()
if "concessions" not in st.session_state:
    st.session_state.concessions = INITIAL_CONCESSIONS.copy()
if "infrastructure" not in st.session_state:
    st.session_state.infrastructure = INITIAL_INFRASTRUCTURE.copy()
if "incidents" not in st.session_state:
    st.session_state.incidents = load_incidents()
if "checklist_checked" not in st.session_state:
    st.session_state.checklist_checked = {}

# Custom CSS for styling
st.markdown("""
<style>
    /* Styling headers & metric cards */
    .stMetric {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 15px;
    }
    div[data-testid="stMetricValue"] {
        color: #10B981;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .main-title {
        font-size: 2.2rem;
        color: #F8FAFC;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        color: #E2E8F0;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
    }
    /* Alerts and custom boxes */
    .alert-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
    }
    .alert-critical {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid rgb(239, 68, 68);
    }
    .alert-warning {
        background-color: rgba(245, 158, 11, 0.15);
        border: 1px solid rgb(245, 158, 11);
    }
    .alert-info {
        background-color: rgba(59, 130, 246, 0.15);
        border: 1px solid rgb(59, 130, 246);
    }
    /* Heatmap styling */
    .heatmap-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
    }
    .heatmap-block {
        flex: 1;
        min-width: 140px;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .density-high {
        background-color: #7F1D1D;
        border: 2px solid #F87171;
        color: #FECACA;
    }
    .density-medium {
        background-color: #78350F;
        border: 2px solid #FBBF24;
        color: #FEF3C7;
    }
    .density-low {
        background-color: #064E3B;
        border: 2px solid #34D399;
        color: #D1FAE5;
    }
</style>
""", unsafe_allow_value=True)

# ----------------- GLOBAL METRICS CALCULATION -----------------
active_incidents_list = [inc for inc in st.session_state.incidents if inc["status"] == "Active"]
critical_count = sum(1 for inc in active_incidents_list if inc["severity"] in ["High", "Critical"])

total_gate_capacity = sum(gate["capacity"] for gate in st.session_state.gates)
total_gate_flow = sum(gate["current_flow"] for gate in st.session_state.gates)
avg_gate_congestion = int((total_gate_flow / total_gate_capacity) * 100) if total_gate_capacity > 0 else 0

avg_pitch_moisture = sum(zone["moisture"] for zone in st.session_state.pitch_zones) // len(st.session_state.pitch_zones)
avg_pitch_wear = sum(zone["turf_wear"] for zone in st.session_state.pitch_zones) // len(st.session_state.pitch_zones)
pitch_health_index = 100 - avg_pitch_wear  # Simple metric representing average grass condition

active_staff_count = sum(1 for staff in st.session_state.staff if staff["status"] == "On Duty")

# ----------------- APP HEADER -----------------
st.markdown("<div class='main-title'>🏟️ Vanguard Pitch-Pilot</div>", unsafe_allow_value=True)
st.markdown("<div class='subtitle'>FIFA World Cup 2026™ Stadium Operations Command & Dispatch Console</div>", unsafe_allow_value=True)

# Top Metric Cards (Professional layout matching accessibility guidelines)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Critical Alerts Active", f"{critical_count} Incidents", delta=None, help="Count of unresolved high/critical safety issues.")
with col_m2:
    st.metric("Average Gate Load", f"{avg_gate_congestion}%", delta="Normal Flow" if avg_gate_congestion < 80 else "Heavy Traffic", delta_color="inverse" if avg_gate_congestion >= 80 else "normal")
with col_m3:
    st.metric("Pitch Health Index", f"{pitch_health_index}%", delta=f"{avg_pitch_moisture}% Moisture", help="Overall calculated turf health (100% minus wear percentage).")
with col_m4:
    st.metric("On-Duty Crew", f"{active_staff_count} Stewards", delta="Fully Staffed" if active_staff_count >= 5 else "Shortage Warn", delta_color="normal" if active_staff_count >= 5 else "inverse")

st.markdown("<br>", unsafe_allow_value=True)

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("## 🕹️ Operations Access")
user_role = st.sidebar.radio(
    "Choose Console View Mode:",
    ["Operations Command Center", "Field Volunteer Input Mode"],
    help="Toggle between full stadium command center overview and localized field-volunteer reporter screens."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏟️ Venue Details")
st.sidebar.info("""
**Stadium**: Vanguard Arena (MetLife Stadium Site)
**Match**: Round of 16 - Match 52
**Capacity**: 82,500 Spectators
**Kick-off**: 20:00 Local Time
""")

# Actionable reset app state button
st.sidebar.markdown("### 🛠️ Maintenance")
if st.sidebar.button("Factory Reset App State"):
    if os.path.exists(INCIDENTS_FILE):
        os.remove(INCIDENTS_FILE)
    st.session_state.gates = INITIAL_GATES.copy()
    st.session_state.pitch_zones = INITIAL_PITCH_ZONES.copy()
    st.session_state.staff = INITIAL_STAFF.copy()
    st.session_state.concessions = INITIAL_CONCESSIONS.copy()
    st.session_state.infrastructure = INITIAL_INFRASTRUCTURE.copy()
    st.session_state.incidents = INITIAL_INCIDENTS.copy()
    st.session_state.checklist_checked = {}
    save_incidents(st.session_state.incidents)
    st.sidebar.success("App data has been reset to defaults!")
    st.rerun()

# ----------------- 1. FIELD VOLUNTEER VIEW -----------------
if user_role == "Field Volunteer Input Mode":
    st.markdown("<div class='section-header'>📱 Field Volunteer Input Console</div>", unsafe_allow_value=True)
    st.write("This view is optimized for mobile screens. Stewards and responders can submit real-time alerts, review active tasks, and report infrastructure anomalies directly from the stadium concourse.")

    col_vol1, col_vol2 = st.columns([1, 1])

    with col_vol1:
        st.subheader("💡 Select Field Position & Duty")
        selected_role = st.selectbox(
            "Select Your Assigned Steward/Volunteer Role:",
            list(ROLE_CHECKLISTS.keys())
        )

        st.markdown(f"#### 📋 Your Shift Checklist - {selected_role}")
        tasks = ROLE_CHECKLISTS[selected_role]
        for idx, task in enumerate(tasks):
            checkbox_key = f"chk_{selected_role}_{idx}"
            default_val = st.session_state.checklist_checked.get(checkbox_key, False)
            checked = st.checkbox(task, value=default_val, key=checkbox_key)
            st.session_state.checklist_checked[checkbox_key] = checked

        total_checked = sum(1 for idx in range(len(tasks)) if st.session_state.checklist_checked.get(f"chk_{selected_role}_{idx}", False))
        st.progress(total_checked / len(tasks))
        st.write(f"Completed: {total_checked} of {len(tasks)} checklist duties.")

        st.markdown("---")
        st.markdown("### ⚠️ Quick Infrastructure Issue Reporter")
        st.write("Use this form to flag accessibility escalators, elevators, or ramps offline.")
        
        infra_opts = [infra["name"] for infra in st.session_state.infrastructure]
        selected_infra_report = st.selectbox("Select Affected Infrastructure Item:", infra_opts)
        infra_new_status = st.selectbox("Current Operational Status:", ["Operational", "Under Maintenance", "Broken"])
        
        if st.button("Update Infrastructure Status"):
            # Update the state
            for infra in st.session_state.infrastructure:
                if infra["name"] == selected_infra_report:
                    infra["status"] = infra_new_status
                    st.success(f"Successfully updated status of {infra['name']} to '{infra_new_status}'!")
                    # Check if broken to display accessibility advice
                    if infra_new_status == "Broken":
                        st.warning(f"Accessibility Alert: {infra['name']} is offline. Alternative Route: {infra['alternative_route']}")
                    st.rerun()

    with col_vol2:
        st.subheader("🔮 Core AI Agent parsing (Structured JSON)")
        st.info("💡 **AI Agent Engine**: The system uses instructions configured in `engine/ai_agent.py` to translate input reports, extract categories, and generate structured JSON outputs.")
        
        user_input_text = st.text_area(
            "Describe the incident / crowd issue (Supports French/Spanish/English):",
            placeholder="e.g., 'Personne évanouie près de la porte B' or 'Pelea cerca de la seguridad en la puerta D'",
            height=110
        )

        if user_input_text.strip():
            # Trigger parsing using the AI agent
            parsed_json_str = parse_incident_report(user_input_text)
            parsed_data = json.loads(parsed_json_str)

            detected_lang = parsed_data.get("detected_language", "English 🇺🇸")
            parsed_category = parsed_data.get("category", "General")
            parsed_severity = parsed_data.get("severity", "Low")
            parsed_translation = parsed_data.get("english_translation", user_input_text)
            parsed_dispatch = parsed_data.get("recommended_crew", "Standard Duty Crew")
            needs_immediate_dispatch = parsed_data.get("needs_immediate_dispatch", False)

            # Display Incident Preview Card
            st.markdown(f"""
            <div class="alert-card alert-{'critical' if parsed_severity in ['High', 'Critical'] else 'warning' if parsed_severity == 'Medium' else 'info'}">
                <strong>🛰️ Vanguard AI Parsing Results</strong><br>
                <ul>
                    <li><strong>Detected Language:</strong> {detected_lang}</li>
                    <li><strong>Estimated Category:</strong> {parsed_category}</li>
                    <li><strong>Assigned Severity:</strong> {parsed_severity}</li>
                    <li><strong>English Translation:</strong> "{parsed_translation}"</li>
                    <li><strong>Proposed Dispatch Unit:</strong> {parsed_dispatch}</li>
                    <li><strong>Immediate Dispatch Required:</strong> {"Yes ✅" if needs_immediate_dispatch else "No ❌"}</li>
                </ul>
            </div>
            """, unsafe_allow_value=True)

            # Show raw structured JSON output for verification as a senior engineer
            with st.expander("🛠️ View Raw AI Agent Structured JSON Output"):
                st.code(parsed_json_str, language="json")

            col_sub1, col_sub2 = st.columns([1, 1])
            with col_sub1:
                reported_zone = st.selectbox("Confirm Incident Sector:", ["Gate A", "Gate B", "Gate C", "Gate D", "Stand North", "Stand South", "Stand East", "Stand West", "Concession Row", "Pitch-side"])
            with col_sub2:
                volunteer_name = st.text_input("Reporter Name:", "Steward Squad A")

            if st.button("🚨 Dispatch Team & Submit Log"):
                new_inc_id = f"INC-{len(st.session_state.incidents) + 1:03d}"
                timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                new_incident = {
                    "id": new_inc_id,
                    "timestamp": timestamp_str,
                    "zone": reported_zone,
                    "category": parsed_category,
                    "description": parsed_translation,
                    "severity": parsed_severity,
                    "status": "Active",
                    "reported_by": volunteer_name
                }
                
                st.session_state.incidents.append(new_incident)
                save_incidents(st.session_state.incidents)
                st.success(f"Incident {new_inc_id} successfully submitted and logged in Operations Command!")
                st.balloons()
                st.rerun()

        st.markdown("---")
        st.markdown("### 📝 Standard Manual Report Form")
        st.write("Submit reports manually if the AI command box is offline.")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            m_category = st.selectbox("Category:", ["Crowd Control", "Medical", "Security", "Infrastructure", "Pitch/Field", "Other"])
            m_severity = st.selectbox("Severity Level:", ["Low", "Medium", "High", "Critical"])
        with col_form2:
            m_zone = st.selectbox("Sector Zone:", ["Gate A", "Gate B", "Gate C", "Gate D", "Stand North", "Stand South", "Stand East", "Stand West", "Concession Row", "Pitch-side"], key="m_zone_key")
            m_reporter = st.text_input("Reporter Initials:", "F.V.")

        m_desc = st.text_area("Incident Description Detail:", key="m_desc_key")
        
        if st.button("Submit Manual Log"):
            new_inc_id = f"INC-{len(st.session_state.incidents) + 1:03d}"
            timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_incident = {
                "id": new_inc_id,
                "timestamp": timestamp_str,
                "zone": m_zone,
                "category": m_category,
                "description": m_desc,
                "severity": m_severity,
                "status": "Active",
                "reported_by": m_reporter
            }
            st.session_state.incidents.append(new_incident)
            save_incidents(st.session_state.incidents)
            st.success(f"Incident {new_inc_id} successfully logged manually.")
            st.rerun()

# ----------------- 2. OPERATIONS COMMAND CENTER -----------------
else:
    st.markdown("<div class='section-header'>🎛️ Operations Command Center</div>", unsafe_allow_value=True)
    
    # Create the Command Center tabs
    tab_crowd, tab_pitch, tab_incidents, tab_staff, tab_concessions, tab_infra = st.tabs([
        "🎟️ Crowd Flow & Gates",
        "🌱 Pitch & Turf Health",
        "🚨 Incident Command",
        "👥 Staffing & Deployment",
        "🍔 Concessions & Queue Stats",
        "🪜 Accessibility & Infrastructure"
    ])

    # ----------------- TAB 1: CROWD FLOW & GATES -----------------
    with tab_crowd:
        st.subheader("🎟️ Live Gate Traffic & Congestion Simulator")
        st.write("Simulate gate arrival bottlenecks in real-time. Use the sliders below to adjust crowds. Red alerts will trigger dynamic volunteer dispatch actions.")
        
        col_g1, col_g2 = st.columns([2, 1])
        
        with col_g1:
            # Table/Visual of gate loads
            gate_data = []
            for idx, gate in enumerate(st.session_state.gates):
                col_slider_lbl, col_slider_val = st.columns([1, 2])
                with col_slider_lbl:
                    st.write(f"**{gate['name']}**")
                    st.caption(f"Cap: {gate['capacity']:,} fans")
                with col_slider_val:
                    # Interactive simulator slider
                    new_flow = st.slider(
                        "Current Crowd Flow (spectators/hour):",
                        min_value=0,
                        max_value=int(gate["capacity"] * 1.2),
                        value=int(gate["current_flow"]),
                        step=500,
                        key=f"gate_slider_{gate['id']}"
                    )
                    st.session_state.gates[idx]["current_flow"] = new_flow
                
                load_pct = int((new_flow / gate["capacity"]) * 100)
                if load_pct >= 95:
                    status = "Critical"
                elif load_pct >= 80:
                    status = "Heavy"
                else:
                    status = "Normal"
                st.session_state.gates[idx]["status"] = status
                
                gate_data.append({
                    "Gate": gate["name"],
                    "Flow": f"{new_flow:,} / hr",
                    "Capacity": f"{gate['capacity']:,}",
                    "Load": f"{load_pct}%",
                    "Status": status,
                    "Reroute Direction": gate["recommended_reroute"]
                })
            
            st.table(pd.DataFrame(gate_data))

        with col_g2:
            st.markdown("### 🗺️ Gate Congestion Alerts")
            critical_gates = [g for g in st.session_state.gates if g["status"] in ["Critical", "Heavy"]]
            
            if critical_gates:
                for gate in critical_gates:
                    pct = int((gate["current_flow"] / gate["capacity"]) * 100)
                    if gate["status"] == "Critical":
                        st.markdown(f"""
                        <div class="alert-card alert-critical">
                            <strong>🔴 CRITICAL SURGE DETECTED: {gate['id']}</strong><br>
                            Gate is operating at {pct}% capacity. Turnstile bottleneck forming.<br>
                            <strong>Command Dispatch Recommendation:</strong> Reroute arriving spectators to <strong>{gate['recommended_reroute']}</strong> immediately. Dispatch 3 Stewards from lower-density zones to guide lines.
                        </div>
                        """, unsafe_allow_value=True)
                    else:
                        st.markdown(f"""
                        <div class="alert-card alert-warning">
                            <strong>⚠️ HEAVY FLOW: {gate['id']}</strong><br>
                            Gate is operating at {pct}% capacity.<br>
                            <strong>Command Dispatch Recommendation:</strong> Direct standby queue leads to open auxiliary channels. Monitor entry speeds.
                        </div>
                        """, unsafe_allow_value=True)
            else:
                st.success("✅ All gate access channels are flowing smoothly at normal operational thresholds.")

        st.markdown("### 🏟️ Stadium Seating Density Heatmap")
        st.write("Dynamic visual mapping of lower and upper stands based on crowd distribution logs.")
        
        # Grid representation of seating zones
        st.markdown("""
        <div class="heatmap-container">
            <div class="heatmap-block density-high">
                North Stand Lower<br>92% Capacity (Heavy)
            </div>
            <div class="heatmap-block density-medium">
                North Stand Upper<br>74% Capacity (Normal)
            </div>
            <div class="heatmap-block density-high">
                East Stand Lower<br>88% Capacity (Heavy)
            </div>
            <div class="heatmap-block density-low">
                East Stand Upper<br>41% Capacity (Light)
            </div>
            <div class="heatmap-block density-medium">
                South Stand Lower<br>79% Capacity (Normal)
            </div>
            <div class="heatmap-block density-low">
                South Stand Upper<br>35% Capacity (Light)
            </div>
            <div class="heatmap-block density-high">
                West Stand Lower<br>95% Capacity (Critical)
            </div>
            <div class="heatmap-block density-medium">
                West Stand Upper<br>68% Capacity (Normal)
            </div>
        </div>
        """, unsafe_allow_value=True)

    # ----------------- TAB 2: PITCH & TURF HEALTH -----------------
    with tab_pitch:
        st.subheader("🌱 Live Hybrid Turf Moisture & Wear Console")
        st.write("Pitch groundskeepers track individual zones to optimize turf recovery and drainage prior to tournament kickoff.")
        
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            st.markdown("### 📍 Pitch Zone Matrix")
            pitch_data = []
            for zone in st.session_state.pitch_zones:
                pitch_data.append({
                    "Zone Sector": zone["zone"],
                    "Moisture Level": f"{zone['moisture']}%",
                    "Hybrid Wear Index": f"{zone['turf_wear']}%",
                    "Watering Window": zone["watering_schedule"],
                    "UV Light Cycle": zone["lighting_schedule"],
                    "Overall Status": zone["status"]
                })
            st.dataframe(pd.DataFrame(pitch_data), use_container_width=True)

            st.write("🔍 *Note: Surface moisture must be maintained between 45% and 65% for FIFA regulatory play. Wear index above 40% triggers critical seed recovery actions.*")

        with col_p2:
            st.markdown("### 🚰 Groundskeeping Direct Actions")
            st.write("Perform maintenance actions on specific zones below to modify status and moisture levels dynamically:")
            
            selected_zone_action = st.selectbox("Select Target Pitch Zone:", [zone["zone"] for zone in st.session_state.pitch_zones])
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💧 Trigger 10-Min Irrigation Sprinklers"):
                    for zone in st.session_state.pitch_zones:
                        if zone["zone"] == selected_zone_action:
                            zone["moisture"] = min(zone["moisture"] + 8, 85)
                            zone["watering_schedule"] = "Irrigating Now"
                            if zone["moisture"] > 75:
                                zone["status"] = "Over-watered"
                            elif 45 <= zone["moisture"] <= 70:
                                zone["status"] = "Excellent"
                            st.success(f"Sprinklers activated for {zone['zone']}. Moisture increased to {zone['moisture']}%!")
                            st.rerun()
            with col_btn2:
                if st.button("☀️ Activate UV Grow-Light Rig"):
                    for zone in st.session_state.pitch_zones:
                        if zone["zone"] == selected_zone_action:
                            zone["moisture"] = max(zone["moisture"] - 4, 30)
                            zone["lighting_schedule"] = "UV Active (Manual)"
                            st.info(f"UV Grow Lights deployed over {zone['zone']}. Soil drying slightly, hybrid recovery initiated.")
                            st.rerun()

            st.markdown("---")
            st.markdown("#### 🏟️ Pitch Moisture Grid Visualizer")
            
            # Generate HTML grid representing parts of the pitch for a premium feel
            grid_cols = st.columns(len(st.session_state.pitch_zones))
            for i, zone in enumerate(st.session_state.pitch_zones):
                with grid_cols[i]:
                    moist = zone["moisture"]
                    wear = zone["turf_wear"]
                    # Color indicator for grass
                    color_bg = "#064E3B" if 45 <= moist <= 70 else "#78350F" if moist < 45 else "#1E3A8A"
                    st.markdown(f"""
                    <div style="background-color: {color_bg}; padding: 10px; border-radius: 5px; text-align: center; color: white;">
                        <span style="font-size:0.8rem; font-weight:bold;">{zone['zone'].split()[0]}</span><br>
                        <span style="font-size:1.1rem; font-weight:bold;">{moist}%</span><br>
                        <span style="font-size:0.75rem;">Wear: {wear}%</span>
                    </div>
                    """, unsafe_allow_value=True)

    # ----------------- TAB 3: INCIDENT COMMAND -----------------
    with tab_incidents:
        st.subheader("🚨 Real-Time Dispatch Desk")
        st.write("Manage active safety, security, and medical incidents reported by stewards on the ground.")
        
        # Incident Filter options
        col_filt1, col_filt2 = st.columns(2)
        with col_filt1:
            severity_filter = st.multiselect("Filter by Severity:", ["Low", "Medium", "High", "Critical"], default=["Low", "Medium", "High", "Critical"])
        with col_filt2:
            status_filter = st.multiselect("Filter by Status:", ["Active", "Dispatched", "Resolved"], default=["Active", "Dispatched"])

        # Compile matching incidents
        filtered_incidents = [
            inc for inc in st.session_state.incidents 
            if inc["severity"] in severity_filter and inc["status"] in status_filter
        ]

        if not filtered_incidents:
            st.success("✅ No matching incidents found in selected filter scope.")
        else:
            inc_df = pd.DataFrame(filtered_incidents)
            st.dataframe(
                inc_df[["id", "timestamp", "zone", "category", "description", "severity", "status", "reported_by"]],
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("### 🕹️ Incident Resolution & Dispatch Controls")
        
        active_ids = [inc["id"] for inc in st.session_state.incidents if inc["status"] in ["Active", "Dispatched"]]
        
        if not active_ids:
            st.write("No active incidents to dispatch or resolve.")
        else:
            col_disp1, col_disp2, col_disp3 = st.columns([1, 1, 1])
            with col_disp1:
                target_inc_id = st.selectbox("Select Incident to Manage:", active_ids)
                # Find details
                target_inc = next(inc for inc in st.session_state.incidents if inc["id"] == target_inc_id)
                st.markdown(f"""
                **Incident Details:**
                * **Type**: {target_inc['category']} ({target_inc['severity']} Severity)
                * **Zone**: {target_inc['zone']}
                * **Reported by**: {target_inc['reported_by']}
                * **Details**: *{target_inc['description']}*
                """)
            with col_disp2:
                dispatch_team = st.selectbox("Dispatch Crew / Unit:", ["Steward Patrol Unit A", "Stadium First Aid Unit 2", "VIP Escort Squad", "Sanitation Team 5", "Facilities Electrician 1"])
                if st.button("🚚 Dispatch Crew Team", use_container_width=True):
                    for inc in st.session_state.incidents:
                        if inc["id"] == target_inc_id:
                            inc["status"] = "Dispatched"
                            inc["description"] = f"{inc['description']} (Dispatched: {dispatch_team})"
                            save_incidents(st.session_state.incidents)
                            st.success(f"Crew '{dispatch_team}' dispatched to {inc['zone']}!")
                            st.rerun()
            with col_disp3:
                resolution_notes = st.text_input("Resolution Log Notes:", placeholder="All ticket errors fixed.")
                if st.button("✅ Mark Incident Resolved", use_container_width=True):
                    for inc in st.session_state.incidents:
                        if inc["id"] == target_inc_id:
                            inc["status"] = "Resolved"
                            inc["description"] = f"{inc['description']} (Resolved: {resolution_notes})"
                            save_incidents(st.session_state.incidents)
                            st.success(f"Incident {target_inc_id} marked as Resolved!")
                            st.rerun()

    # ----------------- TAB 4: STAFFING & DEPLOYMENT -----------------
    with tab_staff:
        st.subheader("👥 Active Crew Assignments & Zoning Hub")
        st.write("Review active personnel zones. Command managers can shift volunteers to gates experiencing peak surges dynamically.")
        
        col_s1, col_s2 = st.columns([2, 1])
        
        with col_s1:
            st.markdown("### 📋 Crew Personnel Roster")
            staff_df = pd.DataFrame(st.session_state.staff)
            st.dataframe(staff_df, use_container_width=True)

        with col_s2:
            st.markdown("### 🔄 Reassign Duty Zones")
            staff_names = [s["name"] for s in st.session_state.staff]
            target_staff_name = st.selectbox("Select Personnel Member:", staff_names)
            
            # Find current staff info
            staff_member = next(s for s in st.session_state.staff if s["name"] == target_staff_name)
            st.write(f"Current Zone: **{staff_member['assigned_zone']}** | Current Status: **{staff_member['status']}**")
            
            new_zone = st.selectbox("Select New Target Zone:", ["Gate A", "Gate B", "Gate C", "Gate D", "Stand East", "Stand West", "Stand North", "Stand South", "Concession Row", "Pitch-side"])
            new_status = st.selectbox("Set Duty Status:", ["On Duty", "On Break", "Off Duty"])
            
            if st.button("Confirm Crew Redeployment"):
                for staff in st.session_state.staff:
                    if staff["name"] == target_staff_name:
                        staff["assigned_zone"] = new_zone
                        staff["status"] = new_status
                        st.success(f"Redeployed {target_staff_name} to {new_zone} ({new_status}).")
                        st.rerun()

            st.markdown("---")
            st.markdown("#### 📊 Sector Density Allocation")
            # Calculate personnel counts in zones
            zone_counts = {}
            for staff in st.session_state.staff:
                zone_counts[staff["assigned_zone"]] = zone_counts.get(staff["assigned_zone"], 0) + 1
            
            zone_counts_df = pd.DataFrame([
                {"Zone": zone, "Stewards Count": count} for zone, count in zone_counts.items()
            ])
            st.bar_chart(zone_counts_df.set_index("Zone"))

    # ----------------- TAB 5: CONCESSIONS & QUEUE STATS -----------------
    with tab_concessions:
        st.subheader("🍔 Concession Sales & Queue Monitoring")
        st.write("Ensuring a seamless spectator fan experience by tracking inventory levels and average queue times.")
        
        col_c1, col_c2 = st.columns([2, 1])
        
        with col_c1:
            st.markdown("### 📈 Vendor Performance")
            concessions_data = []
            for vendor in st.session_state.concessions:
                concessions_data.append({
                    "Vendor Name": vendor["vendor"],
                    "Stock Level": f"{vendor['stock_level']}%",
                    "Queue Duration": f"{vendor['queue_time']} mins",
                    "Gross Revenue": f"${vendor['revenue']:,.2f}",
                    "Status": vendor["status"]
                })
            st.dataframe(pd.DataFrame(concessions_data), use_container_width=True)

        with col_c2:
            st.markdown("### ⚠️ Supply & Queue Alerts")
            
            warning_found = False
            for vendor in st.session_state.concessions:
                if vendor["stock_level"] <= 20:
                    st.markdown(f"""
                    <div class="alert-card alert-critical">
                        <strong>🚨 CRITICAL SUPPLY SHORTAGE: {vendor['vendor']}</strong><br>
                        Stock level has dropped to {vendor['stock_level']}%. Refill runners must be dispatched immediately.
                    </div>
                    """, unsafe_allow_value=True)
                    warning_found = True
                elif vendor["queue_time"] >= 15:
                    st.markdown(f"""
                    <div class="alert-card alert-warning">
                        <strong>⚠️ SEVERE QUEUE DETECTED: {vendor['vendor']}</strong><br>
                        Wait time is {vendor['queue_time']} minutes. Consider sending concession support to checkout terminal points.
                    </div>
                    """, unsafe_allow_value=True)
                    warning_found = True
            
            if not warning_found:
                st.success("✅ All vendor supply volumes are optimal and line wait times are under 10 minutes.")

    # ----------------- TAB 6: ACCESSIBILITY & INFRASTRUCTURE -----------------
    with tab_infra:
        st.subheader("🪜 Stadium Infrastructure & ADA Accessibility Routing")
        st.write("Real-time monitoring of escalators, stairs, elevators, and access ramps. Breaking one instantly modifies ADA accessibility routing alerts.")

        col_i1, col_i2 = st.columns([1, 1])
        
        with col_i1:
            st.markdown("### 🛗 Facilities Status Panel")
            infra_list = []
            for infra in st.session_state.infrastructure:
                infra_list.append({
                    "ID": infra["id"],
                    "Asset Name": infra["name"],
                    "Type": infra["type"],
                    "Operational Status": infra["status"],
                    "ADA Alternative Route": infra["alternative_route"]
                })
            st.dataframe(pd.DataFrame(infra_list), use_container_width=True)

        with col_i2:
            st.markdown("### ♿ Accessibility Routing Engines")
            st.write("Dynamic routing directives generated in real-time based on facilities outages:")
            
            broken_assets = [infra for infra in st.session_state.infrastructure if infra["status"] == "Broken"]
            
            if broken_assets:
                for asset in broken_assets:
                    st.markdown(f"""
                    <div class="alert-card alert-critical">
                        <strong>♿ ADA ACCESSIBILITY ALERT: {asset['name']} is OFFLINE</strong><br>
                        <strong>Outage Impact:</strong> Standard disabled route blocked.<br>
                        <strong>Alternative Pathway Action:</strong> Direct wheelchair users and VIP guests to <strong>{asset['alternative_route']}</strong>. Volunteers at nearby checkpoints have been notified.
                    </div>
                    """, unsafe_allow_value=True)
            else:
                st.success("✅ All accessibility elevators, ramps, and escalators are verified operational. Standard VIP and ADA routing active.")
            
            st.markdown("---")
            st.markdown("#### ⚙️ Toggle Asset Status (Manual Override)")
            override_asset = st.selectbox("Select Asset to Override:", [infra["name"] for infra in st.session_state.infrastructure], key="override_key")
            override_status = st.selectbox("Select Target Status Override:", ["Operational", "Under Maintenance", "Broken"], key="override_status_key")
            
            if st.button("Apply Facility Override"):
                for infra in st.session_state.infrastructure:
                    if infra["name"] == override_asset:
                        infra["status"] = override_status
                        st.success(f"Status of {infra['name']} overridden to '{override_status}'!")
                        st.rerun()
