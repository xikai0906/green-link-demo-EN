#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import json
import pandas as pd
import numpy as np
import os
from PIL import Image

# Base path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 1. Page Configuration and High-Contrast CSS (White + Green Tech Style)
# ==========================================
st.set_page_config(
    page_title="GreenLink | Intelligent ESG Risk & Finance Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-definition tech-style CSS (White primary + Green accents)
st.markdown("""
<style>
    /* 1. Global background and fonts - White primary + Green accents */
    .stApp {
        background-color: #f8fff8 !important;
        color: #1a3c1a !important;
    }
    .stMarkdown, .stText, p, div, label {
        color: #1a3c1a !important;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    /* 2. Headers - More prominent green tech style */
    .main-header {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00b140 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 177, 64, 0.4);
        letter-spacing: -2px;
        text-transform: uppercase;
    }
    .sub-header {
        font-family: sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        color: #00c8a0 !important;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 2px;
        border-bottom: 2px solid #e0f0e0;
        padding-bottom: 20px;
    }

    /* 3. Card style - White cards + Green left border */
    .tech-card {
        background-color: #ffffff !important;
        border: 1px solid #d0e8d0 !important;
        border-left: 6px solid #00b140 !important;
        padding: 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 20px rgba(0, 177, 64, 0.12);
    }
    .tech-card h3 {
        color: #00b140 !important;
        margin-top: 0;
        font-weight: 800;
    }

    /* 4. Sidebar - Light green */
    section[data-testid="stSidebar"] {
        background-color: #f0f9f0 !important;
        border-right: 1px solid #c0e0c0;
    }
    section[data-testid="stSidebar"] * {
        color: #1a3c1a !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a3c1a !important;
        border: 1px solid #a0d0a0 !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #ffffff !important;
        border-color: #c0e0c0 !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #00b140 !important;
        color: #ffffff !important;
    }

    /* 5. Score legend - Adapted for light theme */
    .score-legend-compact {
        background: #f8fff8;
        border: 1px solid #c0e0c0;
        padding: 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        height: 100%;
    }
    .legend-row {
        display: flex;
        align-items: center;
        margin-bottom: 3px;
        color: #1a3c1a;
    }

    /* 6. Metric indicators */
    div[data-testid="stMetricLabel"] {
        color: #006633 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #00b140 !important;
        font-family: 'Courier New', monospace;
        font-size: 1.8rem !important;
    }

    /* 7. Product traceability card & protocol box - Adapted for light theme */
    .product-trace-card {
        background: linear-gradient(145deg, #ffffff, #f0fff0);
        border: 2px solid #00b140;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 177, 64, 0.15);
    }
    .protocol-box {
        background: #f8fff8;
        border: 1px solid #a0d0a0;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .protocol-title {
        color: #00b140;
        font-weight: bold;
        border-bottom: 1px solid #c0e0c0;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }

    /* 8. Supply chain arrow box */
    .chain-box {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin: 5px;
        background: #ffffff;
        border: 2px solid #00b140;
    }

    /* 9. Expander panels */
    details[data-testid="stExpander"], div[data-testid="stExpander"] {
        background-color: #f8fff8 !important;
        border: 1px solid #c0e0c0 !important;
        border-radius: 8px !important;
    }
    details[data-testid="stExpander"] summary {
        color: #00b140 !important;
        background-color: #f0f9f0 !important;
    }

    /* 10. Buttons - Green tech style */
    button[kind="primary"] {
        background-color: #00b140 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
    }
    button[kind="primary"]:hover {
        background-color: #00c8a0 !important;
        box-shadow: 0 0 15px rgba(0, 200, 160, 0.5) !important;
    }

    /* Extra small optimizations */
    .source-link-btn {
        color: #00b140 !important;
        border: 1px solid #00b140;
    }
    
    /* New: Make E/S cards more breathable */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #00b140;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0f0e0;
        padding-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Title area
st.markdown('<div class="main-header">GREENLINK_OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">>> SATELLITE · INTELLIGENCE · FINANCE <<</div>', unsafe_allow_html=True)

# ==========================================
# 2. Data Loading
# ==========================================
companies = {
    "FGV Holdings Berhad": {"filename": "FGV.json", "type": "Upstream Supplier", "position": "Plantation Owner", "code": "FGV"},
    "IOI Corporation": {"filename": "IOI.json", "type": "Upstream Supplier", "position": "Plantation Owner", "code": "IOI"},
    "COFCO Group": {"filename": "COFCO.json", "type": "Midstream Processor", "position": "Core Enterprise", "code": "COFCO"}
}

st.sidebar.markdown("### 📡 Target Lock (TARGET)")
selected_company = st.sidebar.selectbox("Select Target Company", list(companies.keys()))
company_info = companies[selected_company]

@st.cache_data
def load_data(filename):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    if not os.path.exists(file_path): 
        return get_sample_data(), False
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data, 'COFCO' in filename

def get_sample_data():
    return {"company": "Demo Company", "environment": {"risk_score": 25}, "social": {"risk_score": 75}, "supply_chain": {}}

try:
    data, is_cofco = load_data(company_info['filename'])
except:
    data, is_cofco = get_sample_data(), False

env_score = data.get('environment', {}).get('risk_score', 50)
soc_score = data.get('social', {}).get('risk_score', 50)
total_score = (env_score + soc_score) / 2

# ==========================================
# 3. Main Interface Tabs
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Risk Monitoring (MONITOR)",
    "🔗 Chain Penetration (CHAIN)",
    "💰 Green Finance (FINANCE)",
    "📱 Consumer Terminal (CONSUMER)"
])

# ---------- TAB 1: Risk Monitoring ----------
with tab1:
    col_header, col_chart = st.columns([3, 2])
    
    with col_header:
        st.markdown(f"""
        <div class="tech-card">
            <h3>{data.get('company')}</h3>
            <p style="color:#666;"><strong>ID:</strong> {company_info['code']}_9928 &nbsp;|&nbsp; <strong>Role:</strong> {company_info['position']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##### ⚔️ Rating System Comparison (VS Traditional)")
        
        trad_data = data.get('traditional_rating') or data.get('social', {}).get('traditional_rating')
        rating_val = trad_data.get('rating', trad_data.get('msci', 'N/A')) if isinstance(trad_data, dict) else (trad_data if isinstance(trad_data, str) else 'N/A')
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#ffffff; padding:18px; border:1px solid #d0e8d0; border-left:6px solid #666; border-radius:10px; box-shadow:0 4px 12px rgba(0,177,64,0.1);">
                <div style="color:#006633; font-size:0.85rem;">🏢 Traditional Rating (MSCI)</div>
                <div style="font-size: 2.4rem; font-weight:bold; color: #1a3c1a;">{rating_val}</div>
                <div style="color:#d32f2f; font-size:0.85rem;">❌ Vague Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div style="background:#ffffff; padding:18px; border:1px solid #d0e8d0; border-left:6px solid #00b140; border-radius:10px; box-shadow:0 4px 12px rgba(0,177,64,0.1);">
                <div style="color:#006633; font-size:0.85rem;">🌿 GreenLink</div>
                <div style="font-size: 1.15rem; font-weight:bold; color: #00b140;">E/S Separated Scoring</div>
                <div style="color:#1a3c1a; font-size:0.9rem;">Env: {env_score} | Soc: {soc_score}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_chart:
        st.markdown("##### Core Metrics (Core Metrics)")
        c_metrics, c_legend = st.columns([1.2, 1])
        with c_metrics:
            st.metric("E-Score", f"{env_score}", delta="-2.5", delta_color="inverse")
            st.metric("S-Score", f"{soc_score}", delta="+5.1", delta_color="inverse")
        with c_legend:
            st.markdown("""
            <div class="score-legend-compact">
                <div style="color: #006633; margin-bottom: 5px; border-bottom:1px solid #c0e0c0;"><strong>📏 Scoring Standard</strong></div>
                <div class="legend-row"><span class="color-dot" style="background:#00FF41;"></span>0-25: Excellent</div>
                <div class="legend-row"><span class="color-dot" style="background:#ADFF2F;"></span>25-50: Good</div>
                <div class="legend-row"><span class="color-dot" style="background:#FFFF00;"></span>50-75: Medium</div>
                <div class="legend-row"><span class="color-dot" style="background:#FF3333;"></span>75+: Poor</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 2) + [env_score/10, soc_score/10], columns=['Env', 'Soc'])
        st.line_chart(chart_data, color=["#00FF41", "#00F2FF"], height=120)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">🌍 SATELLITE_LINK // Environmental Risk (E)</div>', unsafe_allow_html=True)
    col_env, col_soc = st.columns([1, 1.15])
    
    with col_env:
        env_analysis = data.get('environment', {}).get('analysis', {})
        st.markdown(f"""
        <div class="tech-card">
            <p><strong>Analysis Method:</strong> {env_analysis.get('method', 'AI Remote Sensing Inversion')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_cofco:
            st.markdown("**🛰️ Historical Imagery Comparison (Evidence):**")
            evidence = env_analysis.get('evidence', {})
            img_before = os.path.join(BASE_DIR, evidence.get('satellite_image_before', ''))
            img_after = os.path.join(BASE_DIR, evidence.get('satellite_image_after', ''))
            
            if os.path.exists(img_before) and os.path.exists(img_after):
                c_img1, c_img2 = st.columns(2)
                with c_img1: st.image(img_before, caption="📸 Baseline Year (Before)", use_container_width=True)
                with c_img2: st.image(img_after, caption="📸 Recent Year (After)", use_container_width=True)
                st.success(f"✅ AI Analysis Conclusion: {evidence.get('conclusion', '')}")
            else:
                st.info("⚠️ Satellite data loading...")
        else:
            st.code("# COFCO Environmental Status: COMPLIANT", language="python")
    
    with col_soc:
        st.markdown('<div class="section-header">📢 SOCIAL_LISTENING // Social Evidence Chain (S)</div>', unsafe_allow_html=True)
        social = data.get('social', {})
        events = social.get('key_events', [])
        
        if events:
            for i, event in enumerate(events[:3]):
                border_color = "#FF3333" if event.get('severity', 'Medium') in ['High', 'Severe'] else "#FFCC00"
                st.markdown(f"""
                <div class="tech-card" style="padding: 18px; border-left: 5px solid {border_color}; margin-bottom: 18px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <span style="color:{border_color}; font-weight:bold; font-size:0.9rem;">RISK EVENT #{i+1}</span>
                        <span style="color:#666; font-family:monospace; font-size:0.9rem;">{event.get('date', 'N/A')}</span>
                    </div>
                    <div style="color: #1a3c1a; font-size: 1.15rem; font-weight: bold; margin-bottom: 14px; line-height: 1.4;">{event.get('event', '')}</div>
                    <div style="background:#f8fff8; padding:14px; border-radius:6px; margin-bottom:12px; border:1px dashed #a0d0a0;">
                        <div style="color:#00b140; font-size:0.85rem; margin-bottom:6px;">🤖 AI Intelligent Analysis:</div>
                        <div style="color:#1a3c1a; font-size:0.95rem;">{event.get('impact', 'AI identified potential risks, recommend review.')}</div>
                    </div>
                    <div style="text-align:right;"><a href="#" class="source-link-btn">📂 Source Download (DOC_{202400+i}.PDF)</a></div>
                </div>
                """, unsafe_allow_html=True)
            
            st.success("✅ Evidence Chain Completeness: 100% (3/3 Verified)")
            st.markdown("---")
            with st.expander("💡 Why only these 3 events? (AI Scoring Logic)", expanded=False):
                st.markdown("""
                <div style="font-size: 0.95rem;">
                    <p><strong>1. Key Risk Attribution (Pareto Principle):</strong><br>
                    In ESG risk assessment, a few <strong>major compliance events</strong> often have "veto power" over corporate credit. The system selects the Top 3 key events.</p>
                    <p><strong>2. Time Window & Activity (Time Window):</strong><br>
                    The AI model prioritizes displaying <strong>currently active</strong> or <strong>unresolved</strong> risk events.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No major risk events found")

# ---------- TAB 2: Supply Chain ----------
with tab2:
    st.header("🔗 Supply Chain Risk Transmission Network")
    if is_cofco:
        st.info("💡 Core Enterprise Perspective: Monitor how upstream risks transmit to itself and the market")
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #ffffff; padding: 20px; border-radius: 10px; border: 1px dashed #c0e0c0; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FF3333; color: #FF3333; padding: 10px; border-radius: 5px;">FGV Holdings<br><small>Upstream/High Risk</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">COFCO Group<br><small>Core Enterprise</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #00F2FF; color: #00F2FF; padding: 10px; border-radius: 5px;">EU/US Markets<br><small>Compliance Barriers</small></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🚨 Upstream Risk Sources")
            suppliers = data.get('supply_chain', {}).get('upstream', {}).get('suppliers', [])
            for s in suppliers:
                is_high = "High" in s.get('risk_status', '') or "75" in s.get('risk_status', '')
                status_html = f'<span style="color: #FF3333;">[High Risk]</span>' if is_high else f'<span style="color: #00FF41;">[Low Risk]</span>'
                st.markdown(f"""<div class="tech-card" style="padding: 12px; margin-bottom: 10px;"><div style="font-size: 1rem; font-weight: bold;">{s['name']}</div><div style="font-size: 0.9rem; margin-top:5px;">Status: {status_html} {s.get('risk_status','')}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("### 🛡️ Blocking Strategy Recommendations")
            st.markdown("""<div class="tech-card"><ul style="margin: 0; padding-left: 20px; color: #1a3c1a;"><li style="margin-bottom: 10px;"><strong>Dynamic Adjustment:</strong> Immediately reduce FGV procurement share to below 10%.</li><li style="margin-bottom: 10px;"><strong>Alternatives:</strong> Activate IOI Corporation (low risk) backup channel.</li><li><strong>Physical Isolation:</strong> Establish independent warehousing for U.S. CBP requirements.</li></ul></div>""", unsafe_allow_html=True)
    else:
        st.info(f"💡 Supplier Perspective: How your ESG risks lead to downstream customer loss")
        my_risk_color = "#FF3333" if total_score > 50 else "#00FF41"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; align-items: stretch; background: #ffffff; padding: 20px; border-radius: 10px; border: 1px dashed #c0e0c0; margin-bottom: 20px;">
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid {my_risk_color}; color: {my_risk_color}; padding: 10px; border-radius: 5px;">{data.get('company')}<br><small>You (Supplier)</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FFCC00; color: #FFCC00; padding: 10px; border-radius: 5px;">Core Processor<br><small>Buyer</small></div></div>
            <div class="arrow">➜</div>
            <div style="flex:1;" class="chain-box"><div style="border: 2px solid #FF0000; color: #FF0000; padding: 10px; border-radius: 5px; background: rgba(255,0,0,0.05);">Market Ban<br><small>CBP/EUDR Interception</small></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📉 Business Impact Forecast")
            st.markdown(f"""<div class="tech-card" style="border-left-color: #FF3333;"><div style="margin-bottom:10px;"><strong>⚠️ Major Customer Loss Risk:</strong></div><div style="font-size:2rem; color:#FF3333; font-weight:bold;">HIGH</div><p style="color:#666; font-size:0.9rem;">Due to your high social risk score ({soc_score}), downstream customers face compliance pressure, expected to cut 70% of orders.</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("### ✅ Remediation Recommendations (To-Do)")
            st.markdown("""<div class="tech-card" style="border-left-color: #00FF41;"><ul style="margin: 0; padding-left: 20px; color: #1a3c1a;"><li style="margin-bottom: 10px;"><strong>Immediate Action:</strong> Submit third-party audit report for CBP WRO.</li><li><strong>Transparency:</strong> Upload labor compliance certificates.</li></ul></div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("## 💰 Green Finance & Risk Pricing")
    fin_col1, fin_col2 = st.columns([1, 1])
    
    with fin_col1:
        st.markdown("### 🏦 ESG-Linked Loan Simulator")
        st.markdown("""<div class="tech-card" style="border-left-color: #00F2FF;"><strong>Algorithm Logic:</strong> Based on the company's real-time ESG score, calculate the green loan interest rate discount (Basis Points) available.</div>""", unsafe_allow_html=True)
        
        loan_amount = st.number_input("Loan Amount (10k RMB)", min_value=100, value=5000, step=100)
        
        if 'show_loan_result' not in st.session_state:
            st.session_state.show_loan_result = False
        
        if st.button("🚀 Start AI Rating Calculation (START RATING)", type="primary", use_container_width=True):
            st.session_state.show_loan_result = True
           
        if st.session_state.show_loan_result:
            base_rate = 4.35
            discount_bp = 50 if total_score <= 30 else (20 if total_score <= 50 else 0)
            rating_color = "#00FF41" if total_score <= 30 else ("#ADFF2F" if total_score <= 50 else "#FFA500")
            rating_label = "🌿 Deep Green Enterprise" if total_score <= 30 else ("🍃 Light Green Enterprise" if total_score <= 50 else "🍂 Brown Enterprise")
            final_rate = base_rate - (discount_bp / 100)
            annual_saving = loan_amount * (discount_bp / 10000)
            
            st.markdown("---")
            st.markdown(f'<div style="font-size: 1.1rem; font-weight: bold; color: {rating_color}; margin: 10px 0;">Rating Result: {rating_label}</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Base Rate", f"{base_rate}%")
            c2.metric("ESG Discount", f"-{discount_bp} bp")
            c3.metric("Effective Rate", f"{final_rate:.2f}%")
            st.markdown(f"""<div style="background: #f8fff8; border: 1px solid #00b140; padding: 15px; border-radius: 6px; text-align: center; margin-top: 15px;"><span style="color: #006633; font-size: 0.9rem;">Estimated Annual Interest Savings</span><br><span style="font-size: 1.8rem; color: #00b140; font-weight: bold; font-family: monospace;">¥ {annual_saving:,.0f}</span></div>""", unsafe_allow_html=True)
        else:
            st.info("💡 Enter loan amount and click the button above to start calculation")
       
    with fin_col2:
        st.markdown("### 📉 Financial Risk Quantification")
        if total_score > 60:
            potential_loss = loan_amount * 0.15
            st.error("⚠️ Extremely High Risk Exposure")
            st.markdown("""<div class="tech-card" style="border-left-color: #FF3333;"><p style="color: #FF3333 !important;"><strong>Main Risk Sources:</strong></p><ul style="color: #1a3c1a;"><li>🇪🇺 <strong>EU EUDR Fine:</strong> 4% of revenue</li><li>🇺🇸 <strong>Goods Detention Cost:</strong> ~2M USD</li></ul></div>""", unsafe_allow_html=True)
            st.metric("Potential Financial Loss Estimate", f"¥ {potential_loss/10000:,.1f} Billion", delta="-15% Revenue", delta_color="inverse")
        else:
            st.success("✅ Financial Risk Controllable")
            st.metric("Green Premium (Greenium)", "+ 2.5%", "Financing Cost Advantage")
    st.markdown("---")
    st.subheader("⛓️ Supply Chain Finance Credit Model")
    scf_df = pd.DataFrame({"Supplier": ["FGV", "IOI", "Sime Darby", "Wilmar"], "ESG Risk Score": [75, 25, 30, 40], "Base Credit (10k)": [1000, 1000, 1000, 1000]})
    scf_df["Adjustment Factor"] = scf_df["ESG Risk Score"].apply(lambda x: 0.5 if x > 60 else (1.2 if x < 30 else 1.0))
    scf_df["Dynamic Credit (10k)"] = (scf_df["Base Credit (10k)"] * scf_df["Adjustment Factor"]).astype(int)
    st.dataframe(scf_df, use_container_width=True, hide_index=True)

# ---------- TAB 4: B2C（已修改二维码链接） ----------
with tab4:
    st.markdown("### 📱 Product Digital Twin & Trust Traceability (B2C)")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # ==================== 已更新为英文仓库链接 ====================
        st.markdown(f"""
        <div style="background: #FFF; padding: 15px; border-radius: 10px; display: inline-block;">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://xikai0906.github.io/green-link-demo-EN/" width="100%" />
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; margin-top:10px; color:#00F2FF;">SCAN TO VERIFY</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="product-trace-card">
            <h2 style="color: #1a3c1a; margin-bottom: 20px;">🌿 Fortune Edible Oil <span style="font-size:0.6em; color:#00FF41; border:1px solid #00FF41; padding:2px 8px; border-radius:4px;">VERIFIED</span></h2>
            <div style="display: flex; justify-content: space-between; text-align: left; margin-bottom: 20px;">
                <div style="width: 30%;"><div style="color: #666; font-size: 0.8rem;">CARBON FOOTPRINT</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">1.2kg</div><div style="color: #555; font-size: 0.7rem;">CO2e / Bottle</div></div>
                <div style="width: 30%;"><div style="color: #666; font-size: 0.8rem;">ORIGIN</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">Johor, MY</div><div style="color: #555; font-size: 0.7rem;">Satellite Checked</div></div>
                <div style="width: 30%;"><div style="color: #666; font-size: 0.8rem;">LABOR</div><div style="color: #00F2FF; font-size: 1.2rem; font-weight: bold;">ILO Compliant</div><div style="color: #555; font-size: 0.7rem;">Audit Passed</div></div>
            </div>
            <div style="background: rgba(0, 255, 65, 0.1); border: 1px dashed #00FF41; padding: 10px; border-radius: 8px;">
                <p style="color: #00FF41; margin: 0; font-size: 0.9rem;">
                    ✅ <strong>Blockchain Evidence Hash:</strong> 0x7f83...9a2b<br>
                    This product's supply chain fully complies with GreenLink sustainability standards
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📜 Underlying Compliance Protocols & International Standards (COMPLIANCE PROTOCOLS)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("""<div class="protocol-box"><div class="protocol-title">ISO 14067 (Carbon Footprint)</div><div style="color:#1a3c1a; font-size:0.85rem;">• <strong>Standard:</strong> LCA Method<br>• <strong>Advantage:</strong> 68% Carbon Reduction</div></div>""", unsafe_allow_html=True)
        with c2: st.markdown("""<div class="protocol-box"><div class="protocol-title">EUDR (Zero Deforestation)</div><div style="color:#1a3c1a; font-size:0.85rem;">• <strong>Red Line:</strong> No deforestation after 2020<br>• <strong>Verification:</strong> Sentinel-2 Satellite</div></div>""", unsafe_allow_html=True)
        with c3: st.markdown("""<div class="protocol-box"><div class="protocol-title">ILO (Labor Conventions)</div><div style="color:#1a3c1a; font-size:0.85rem;">• <strong>Focus:</strong> Avoid U.S. CBP Ban<br>• <strong>Audit:</strong> SA8000 Certification</div></div>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""<div style="font-size: 0.8rem; color: #666;">POWERED BY <strong style="color: #00b140;">GREENLINK TECH</strong><br>v3.7.0 (White-Green Layout)</div>""", unsafe_allow_html=True)
