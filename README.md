# 🏟️ Vanguard Pitch-Pilot

**Vanguard Pitch-Pilot** is a lightweight, high-performance venue operations co-pilot designed for stadium management during the **FIFA World Cup 2026™**. Built using Python and Streamlit, it serves as a dual-role command dashboard and field volunteer assistant to ensure seamless matchday operations, crowd safety, and accessibility routing.

---

## 🎯 Chosen Vertical
**Venue Staff & Volunteer Operations Co-Pilot**  
Vanguard Pitch-Pilot bridges the gap between stadium operations command centers and stewards on the ground. It provides mobile-optimized checklists, real-time multilingual dispatch tools, and instant communications to coordinate stadium staff dynamically.

---

## 🚀 Core Features

1. **🔮 Multilingual Incident Dispatching**
   - Field stewards can type reports in their native language (e.g., French, Spanish, English).
   - The core AI engine translates the report, determines the emergency classification (Medical, Security, Crowd Control, Infrastructure), calculates severity tiers, and recommends immediate dispatch squads.
   - Operators can review the raw structured JSON payload before confirming dispatch orders.

2. **🎟️ Context-Aware Gate Routing**
   - Dynamic crowd capacity sliders simulate incoming gates (Gates A–D) bottlenecks.
   - When turnstile flow spikes, the co-pilot flashes critical warnings and auto-calculates alternative routing suggestions to redirect spectators to lower-congestion gates.

3. **♿ Accessibility Support & ADA Route Optimization**
   - Operators can track elevators, escalators, and access ramps.
   - Marking any asset as "Broken" triggers real-time rerouting notifications, automatically suggesting alternative step-free paths for VIPs and mobility-restricted spectators.

---

## 💻 Technical Approach

- **Frontend & UI Presentation**: Built using **Streamlit** to deliver an inclusive, high-contrast user interface that ensures clear readability for stadium staff walking around in bright daylight or crowded, dark stadium zones.
- **Lightweight State Management**: Utilizes `st.session_state` as the primary, in-memory data store. This guarantees real-time interactive updates across dashboards without database connection lags.
- **0 KB Local Persistence**: Serializes live incident logs into a lightweight `stadium_incidents.json` file inside the directory. This enables database-less persistent backups across server reboots.
- **Structured JSON Engine**: The core AI agent operates out of `engine/ai_agent.py`. It utilizes a robust, rule-based multilingual parsing framework, returning clean JSON representations that match standard LLM API structured output schemas.

---

## 📦 Repository & Size Optimization

> [!IMPORTANT]
> The Vanguard Pitch-Pilot repository is optimized to remain **strictly below the 10 MB size limit**.

We achieved this lightweight footprint through the following measures:
- **No Heavy Frameworks**: Avoided bulky backend frameworks, database servers, or node modules, relying strictly on Streamlit's native processing libraries.
- **No Binary Caches**: Configured `.gitignore` to strictly exclude all Python bytecodes (`__pycache__`), virtual environment wrappers (`.venv`, `venv`), and local logs.
- **Zero Large Assets**: Styled graphics, charts, maps, and matrices natively using custom HSL/CSS grids and progress bars in markdown rather than loading heavy static images or external map rendering engines.
- **Pre-seeded Lightweight Metadata**: Packaged all initial mock databases as tiny Python dictionary configurations in `mock_data.py`.
