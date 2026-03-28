<DOCUMENT filename="app.py">
#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import json
import pandas as pd
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="GreenLink - ESG Risk Assessment Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #27ae60;
    }
    .risk-high {
        color: #e74c3c;
        font-weight: bold;
    }
    .risk-low {
        color: #27ae60;
        font-weight: bold;
    }
    .supply-chain-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🌿 GreenLink</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Supply Chain ESG Risk Assessment Platform Based on Alternative Data</p>', unsafe_allow_html=True)

# Sidebar: select company
st.sidebar.header("🎯 Select Analysis Target")
st.sidebar.markdown("---")

# Define company list and supply chain relationships
companies = {
    "FGV Holdings Berhad": {
        "filename": "FGV.json",
        "type": "Upstream Supplier",
        "position": "Planter"
    },
    "IOI Corporation": {
        "filename": "IOI.json", 
        "type": "Upstream Supplier",
        "position": "Planter"
    },
    "COFCO Group (COFCO)": {
        "filename": "COFCO.json",
        "type": "Midstream Processor",
        "position": "Buyer/Processor"
    }
}

selected_company = st.sidebar.selectbox(
    "Select Company",
    list(companies.keys()),
    help="Select the supply chain enterprise to analyze"
)

# Display current company's position in the supply chain
company_info = companies[selected_company]
st.sidebar.info(f"**Supply Chain Position**: {company_info['type']}\n\n**Role**: {company_info['position']}")

# Load data
@st.cache_data
def load_data(filename):
    file_path = f'data/{filename}'
    if not os.path.exists(file_path):
        st.warning(f"Data file {filename} not found, displaying sample data")
        return get_sample_data(), False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Determine data type (upstream supplier vs midstream processor)
        is_cofco = 'COFCO' in filename
        return data, is_cofco

def get_sample_data():
    """Return sample data structure"""
    return {
        "company": "Sample Company",
        "environment": {
            "risk_level": "Low Risk",
            "risk_score": 25,
            "analysis": {
                "method": "Sentinel-2 Satellite Image Analysis",
                "period": "2014-2022",
                "evidence": {
                    "satellite_image_before": "",
                    "satellite_image_after": "",
                    "conclusion": "Plantation boundary is stable, no evidence of new deforestation"
                }
            },
            "compliance": {
                "eudr": "✅ Compliant with EU EUDR Regulations",
                "rspo": "⚠️ Some certifications suspended"
            }
        },
        "social": {
            "risk_level": "High Risk",
            "risk_score": 75,
            "key_events": [],
            "traditional_rating": {
                "msci": "BB",
                "description": "Traditional rating is vague"
            }
        }
    }

try:
    data, is_cofco = load_data(company_info['filename'])
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    data, is_cofco = get_sample_data(), False

# Create three tabs
tab1, tab2, tab3 = st.tabs([
    "🎯 Risk Assessment Dashboard", 
    "🔗 Supply Chain Impact Analysis", 
    "📱 B2C Product Traceability"
])

# ========== Tab 1: Risk Assessment Dashboard ==========
with tab1:
    st.header(f"📊 {data.get('company', 'Unknown Company')} - ESG Risk Assessment")
    
    # Compare with traditional rating
    col_compare1, col_compare2 = st.columns(2)
    
    with col_compare1:
        traditional_rating = data.get('traditional_rating', {}) or data.get('social', {}).get('traditional_rating', {})
        rating_value = traditional_rating.get('rating', traditional_rating.get('msci', 'N/A'))
        rating_desc = traditional_rating.get('limitation', traditional_rating.get('description', 'Traditional rating is vague'))
        
        st.info(f"**🏢 Traditional Rating (MSCI)**: {rating_value}\n\n{rating_desc}")
    
    with col_compare2:
        st.success("**🌿 GreenLink Rating**: Uses E/S Separate Scoring\n\n"
                   "✅ Accurately locates risk sources\n\n"
                   "✅ Based on objective alternative data")
    
    st.markdown("---")
    
    # Two-column layout: Environment vs Social
    col1, col2 = st.columns(2)
    
    # ===== Environment Module =====
    with col1:
        st.subheader("🌍 Environmental Risk Assessment (E)")
        
        env = data.get('environment', {})
        e_score = env.get('risk_score', 0)
        e_level = env.get('risk_level', 'Unknown')
        
        # Display large metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                label="Risk Level",
                value=e_level,
                delta=f"Score: {e_score}/100",
                delta_color="normal" if e_score < 50 else "inverse"
            )
        with metric_col2:
            analysis_method = env.get('analysis', {}).get('method', 'Satellite Remote Sensing')
            if '卫星' in analysis_method or 'Sentinel' in analysis_method:
                st.metric(label="Analysis Method", value="Satellite Remote Sensing", delta="Sentinel-2")
            else:
                st.metric(label="Analysis Method", value="Report Review", delta="Enterprise Disclosure")
        
        # Analysis details
        st.markdown("**📊 Analysis Details**")
        analysis = env.get('analysis', {})
        
        if is_cofco:
            # COFCO data structure
            st.write(f"- **Analysis Period**: {analysis.get('period', 'N/A')}")
            st.write(f"- **Analysis Method**: {analysis.get('method', 'N/A')}")
            key_findings = analysis.get('key_findings', [])
            if key_findings:
                st.write("**Key Findings**:")
                for finding in key_findings:
                    st.write(f"  - {finding}")
            st.write(f"- **Conclusion**: {analysis.get('conclusion', 'N/A')}")
        else:
            # FGV/IOI data structure
            st.write(f"- **Analysis Period**: {analysis.get('period', 'N/A')}")
            st.write(f"- **Analysis Method**: {analysis.get('method', 'N/A')}")
            st.write(f"- **Key Indicator**: {analysis.get('indicator', 'N/A')}")
            st.write(f"- **Analysis Result**: {analysis.get('result', 'N/A')}")
        
        # Display satellite image comparison (only for upstream suppliers)
        if not is_cofco:
            st.markdown("**🛰️ Satellite Image Comparison**")
            
            evidence = analysis.get('evidence', {})
            img_before = evidence.get('satellite_image_before', '')
            img_after = evidence.get('satellite_image_after', '')
            
            if img_before and img_after and os.path.exists(img_before):
                col_img1, col_img2 = st.columns(2)
                with col_img1:
                    st.image(img_before, caption="Baseline Year", use_column_width=True)
                with col_img2:
                    st.image(img_after, caption="Recent Year", use_column_width=True)
                
                # Display observation records (IOI specific)
                observations = evidence.get('observation', [])
                if observations:
                    with st.expander("📝 Detailed Observation Records"):
                        for obs in observations:
                            st.write(f"- {obs}")
            else:
                st.info("💡 Satellite image files not uploaded. Please place the image files in the `assets/satellite_images/` directory")
            
            # Conclusion
            conclusion = evidence.get('conclusion', analysis.get('conclusion', ''))
            if conclusion:
                st.success(f"✅ **Conclusion**: {conclusion}")
        else:
            # COFCO environmental performance
            positive_actions = env.get('positive_actions', [])
            if positive_actions:
                st.markdown("**✅ Positive Actions**")
                for action in positive_actions:
                    st.write(f"- {action}")
        
        # Compliance status
        st.markdown("**📋 Regulatory Compliance**")
        compliance = env.get('compliance', {})
        if compliance:
            st.write(compliance.get('eudr', ''))
            st.write(compliance.get('rspo', ''))
        
        # Certification information (IOI specific)
        certifications = env.get('certifications', {})
        if certifications:
            rspo = certifications.get('RSPO', {})
            if rspo:
                with st.expander("🏆 RSPO Certification Status"):
                    st.write(f"**Status**: {rspo.get('status', 'N/A')}")
                    st.write(f"**Certified Area Percentage**: {rspo.get('certified_area_percentage', 'N/A')}")
                    if rspo.get('suspension_period'):
                        st.warning(f"⚠️ Certification was suspended: {rspo.get('suspension_period')}")
    
    # ===== Social Module =====
    with col2:
        st.subheader("👥 Social Risk Assessment (S)")
        
        social = data.get('social', {})
        s_score = social.get('risk_score', 0)
        s_level = social.get('risk_level', 'Unknown')
        
        # Display large metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                label="Risk Level",
                value=s_level,
                delta=f"Score: {s_score}/100",
                delta_color="normal" if s_score < 50 else "inverse"
            )
        with metric_col2:
            st.metric(label="Analysis Method", value="Public Opinion Analysis", delta="AI Crawler")
        
        # COFCO-specific risk source explanation
        if is_cofco:
            analysis = social.get('analysis', {})
            if analysis:
                st.warning(f"""
                **⚠️ Risk Source Analysis**
                
                **Method**: {analysis.get('method', 'N/A')}
                
                **Main Risk**: {analysis.get('key_concern', 'N/A')}
                
                **Risk Type**: {analysis.get('risk_source', 'Upstream supplier transmission')}
                """)
        
        # Key event list
        st.markdown("**📰 Key Public Opinion Events**")
        
        key_events = social.get('key_events', [])
        if not key_events:
            st.info("No major public opinion events recorded")
        else:
            for idx, event in enumerate(key_events[:5], 1):  # Show only first 5
                event_title = event.get('event', 'Unknown Event')
                event_date = event.get('date', event.get('year', 'N/A'))
                
                with st.expander(f"Event {idx}: {event_title[:50]}...", expanded=(idx == 1)):
                    st.write(f"**Date**: {event_date}")
                    
                    # Handle different data structures
                    if 'source' in event:
                        st.write(f"**Source**: {event['source']}")
                    if 'impact' in event:
                        st.write(f"**Impact**: {event['impact']}")
                    if 'severity' in event:
                        severity = event['severity']
                        if severity == '严重' or severity == 'High':
                            st.error(f"**Severity**: {severity}")
                        elif severity == '中' or severity == 'Medium':
                            st.warning(f"**Severity**: {severity}")
                        else:
                            st.info(f"**Severity**: {severity}")
                    
                    # IOI detailed information
                    if 'details' in event:
                        details = event['details']
                        if isinstance(details, list):
                            st.write("**Detailed Information**:")
                            for detail in details:
                                st.write(f"- {detail}")
                        else:
                            st.write(f"**Detailed Information**: {details}")
                    
                    if 'url' in event and event['url'] != "#":
                        st.markdown(f"[📎 View Original Article]({event['url']})")
        
        # Risk mitigation measures (COFCO/IOI)
        risk_mitigation = social.get('risk_mitigation', [])
        improvement_actions = social.get('improvement_actions', [])
        
        if risk_mitigation:
            with st.expander("✅ Risk Mitigation Measures"):
                for action in risk_mitigation:
                    st.write(f"- {action}")
        
        if improvement_actions:
            with st.expander("📈 Improvement Actions"):
                for action in improvement_actions:
                    if isinstance(action, dict):
                        st.write(f"**{action.get('year', 'N/A')}**: {action.get('action', 'N/A')}")
                    else:
                        st.write(f"- {action}")
        
        # Traditional rating comparison
        st.markdown("**🔍 Limitations of Traditional Ratings**")
        traditional_rating = social.get('traditional_rating', {})
        
        st.warning(f"""
        **MSCI Rating**: {traditional_rating.get('msci', traditional_rating.get('rating', 'N/A'))}
        
        {traditional_rating.get('description', 'Traditional rating is vague and cannot accurately identify specific risks')}
        
        ❌ Ratings are lagging and cannot reflect newly occurring major events in time
        ❌ Ratings are generic and cannot accurately locate risk sources
        """)
        
        st.success("""
        **✅ GreenLink Advantages**
        
        - Real-time monitoring of public opinion changes
        - Accurately locate social risk events
        - Provide detailed evidence chains
        - Traceable to original news sources
        """)

# ========== Tab 2: Supply Chain Impact Analysis ==========
with tab2:
    st.header("🔗 Supply Chain Risk Impact Analysis")
    
    st.markdown("""
    This module demonstrates GreenLink's **Innovation Point 2**: Supply Chain Transparency.
    When upstream suppliers face ESG risks, how they affect midstream processors and downstream markets.
    """)
    
    st.markdown("---")
    
    # Show different supply chain views based on selected company
    if is_cofco:
        # ========== COFCO perspective: show full upstream-midstream-downstream ==========
        st.subheader("🏭 COFCO Group Supply Chain Risk Panorama")
        
        supply_chain = data.get('supply_chain', {})
        
        # Three-column layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🌱 Upstream Suppliers")
            
            upstream = supply_chain.get('upstream', {})
            suppliers = upstream.get('suppliers', [])
            
            for supplier in suppliers:
                risk_status = supplier.get('risk_status', 'Unknown')
                
                # Choose color based on risk status
                if 'High' in risk_status or '75' in risk_status:
                    st.error(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"⚠️ {risk_status}")
                elif 'Low' in risk_status:
                    st.success(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"✅ {risk_status}")
                else:
                    st.info(f"**{supplier.get('name', 'N/A')}**")
                    st.write(f"📍 {supplier.get('country', 'N/A')}")
                    st.write(f"🌾 {supplier.get('product', 'N/A')}")
                    st.write(f"ℹ️ {risk_status}")
                
                if supplier.get('note'):
                    st.caption(supplier['note'])
                
                st.markdown("---")
        
        with col2:
            st.markdown("### 🏭 Midstream Processor (Current)")
            
            st.markdown('<div class="supply-chain-box"><h3>COFCO Group</h3><p>China\'s Largest Agricultural Product Processor</p></div>', 
                       unsafe_allow_html=True)
            
            st.write(f"**Environmental Risk**: {data['environment']['risk_score']} points ({data['environment']['risk_level']})")
            st.write(f"**Social Risk**: {data['social']['risk_score']} points ({data['social']['risk_level']})")
            
            st.info("""
            **Supply Chain Exposure**
            
            High dependence on high-risk suppliers such as FGV
            
            ⚠️ Need to adopt diversified procurement strategy
            """)
        
        with col3:
            st.markdown("### 🌍 Downstream Markets")
            
            downstream = supply_chain.get('downstream', {})
            markets = downstream.get('markets', [])
            
            for market in markets:
                if isinstance(market, dict):
                    region = market.get('region', 'N/A')
                    regulation = market.get('regulation', 'N/A')
                    risk = market.get('risk', 'N/A')
                    
                    with st.expander(f"🌐 {region}"):
                        st.write(f"**Products**: {', '.join(market.get('products', []))}")
                        st.write(f"**Regulation**: {regulation}")
                        if market.get('compliance_deadline'):
                            st.warning(f"⏰ Deadline: {market['compliance_deadline']}")
                        st.write(f"**Risk**: {risk}")
                else:
                    st.write(f"- 🌐 {market}")
        
        # Risk transmission paths
        st.markdown("---")
        st.markdown("#### 🔴 Risk Transmission Paths")
        
        risk_paths = upstream.get('risk_transmission_path', [])
        if risk_paths:
            for path in risk_paths:
                st.error(f"⚠️ {path}")
        
        # Mitigation strategies
        st.markdown("---")
        st.subheader("💡 Supply Chain Risk Mitigation Strategies")
        
        mitigation = supply_chain.get('mitigation_strategy', {})
        
        col_strat1, col_strat2 = st.columns(2)
        
        with col_strat1:
            st.markdown("**⚡ Short-term Measures**")
            short_term = mitigation.get('short_term', [])
            for action in short_term:
                st.write(f"- {action}")
        
        with col_strat2:
            st.markdown("**🎯 Long-term Strategies**")
            long_term = mitigation.get('long_term', [])
            for action in long_term:
                st.write(f"- {action}")
        
        # Compliance status
        st.markdown("---")
        st.subheader("📋 Regulatory Compliance Status")
        
        regulatory = data.get('regulatory_compliance', {})
        
        if regulatory:
            col_reg1, col_reg2 = st.columns(2)
            
            with col_reg1:
                eudr = regulatory.get('EUDR', {})
                if eudr:
                    st.markdown("**🇪🇺 EU EUDR**")
                    st.write(f"**Status**: {eudr.get('status', 'N/A')}")
                    st.write(f"**Deadline**: {eudr.get('deadline', 'N/A')}")
                    st.write(f"**Progress**: {eudr.get('progress', 'N/A')}")
            
            with col_reg2:
                cbp = regulatory.get('US_CBP', {})
                if cbp:
                    st.markdown("**🇺🇸 US CBP**")
                    st.write(f"**Status**: {cbp.get('status', 'N/A')}")
                    st.write(f"**Risk**: {cbp.get('risk', 'N/A')}")
                    st.write(f"**Action**: {cbp.get('action', 'N/A')}")
    
    else:
        # ========== Upstream supplier perspective (FGV/IOI) ==========
        st.subheader(f"🌱 {data.get('company', 'Supplier')}'s Supply Chain Impact")
        
        supply_chain_data = data.get('supply_chain', {})
        
        # If data contains complete supply chain structure
        if 'upstream' in supply_chain_data or 'midstream' in supply_chain_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🌱 Upstream (Current)")
                
                st.markdown(f'<div class="supply-chain-box"><h3>{data.get("company", "Supplier")}</h3><p>{data.get("industry", "Palm Oil Production")}</p></div>', 
                           unsafe_allow_html=True)
                
                st.write(f"**Environmental Risk**: {data['environment']['risk_score']} points")
                st.write(f"**Social Risk**: {data['social']['risk_score']} points")
                
                if data['environment']['risk_score'] > 60 or data['social']['risk_score'] > 60:
                    st.error("⚠️ High Risk Alert")
            
            with col2:
                st.markdown("### 🏭 Midstream Processor")
                
                midstream = supply_chain_data.get('midstream', {})
                
                if midstream:
                    if isinstance(midstream, dict):
                        st.write(f"**Company**: {midstream.get('name', 'N/A')}")
                        st.write(f"**Location**: 📍 {midstream.get('location', 'N/A')}")
                        products = midstream.get('products', [])
                        if products:
                            st.write(f"**Products**: {', '.join(products)}")
                        
                        exposure = midstream.get('exposure', '')
                        if exposure:
                            st.info(f"**Supply Chain Exposure**: {exposure}")
                    else:
                        st.write(midstream)
                else:
                    st.info("**Main Customers**: COFCO Group and other international processors")
            
            with col3:
                st.markdown("### 🌍 Downstream Markets")
                
                downstream = supply_chain_data.get('downstream', {})
                
                if downstream:
                    if isinstance(downstream, dict):
                        markets = downstream.get('markets', [])
                        for market in markets:
                            st.write(f"- 🌐 {market}")
                        
                        # Display major customers (IOI specific)
                        major_customers = downstream.get('major_customers', [])
                        if major_customers:
                            with st.expander("🏢 Major Customers"):
                                for customer in major_customers:
                                    st.write(f"- {customer}")
                    else:
                        for market in downstream:
                            st.write(f"- 🌐 {market}")
        
        # Risk transmission analysis
        st.markdown("---")
        st.markdown("#### 🔴 Risk Transmission Impact")
        
        # IOI/FGV risk transmission
        if 'risk_transmission' in supply_chain_data:
            transmission = supply_chain_data['risk_transmission']
            st.write(transmission.get('description', ''))
            
            pathways = transmission.get('pathway', [])
            for pathway in pathways:
                st.error(f"⚠️ {pathway}")
        else:
            # Default display
            st.warning(f"""
            **Risk Transmission Path**:
            
            {data.get('company', 'Supplier')} ({data['social']['risk_level']})
            ⬇️
            Midstream Processor (Affected)
            ⬇️
            EU/US/China Markets (Compliance Pressure)
            """)
        
        # Recommendations for downstream
        st.markdown("---")
        st.subheader("💼 Recommendations for Downstream Customers")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("**🔍 Immediate Actions**")
            st.markdown("""
            1. ✅ Assess supply chain exposure
            2. ✅ Find alternative suppliers
            3. ✅ Monitor supplier remediation progress
            4. ✅ Prepare compliance documents
            """)
        
        with col_rec2:
            st.markdown("**📊 Long-term Strategies**")
            st.markdown("""
            1. 🌿 Establish supplier grading system
            2. 🌿 Diversify supply chain layout
            3. 🌿 Conduct regular ESG audits
            4. 🌿 Transparency commitment
            """)
    
    # PDF report download (common to all companies)
    st.markdown("---")
    st.subheader("📥 Generate and Download Compliance Report")
    
    st.info("💡 Click the button below to generate a detailed ESG compliance report in PDF format, which can be used for internal risk control or to present to clients.")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button("📄 Generate PDF Compliance Report", type="primary", use_container_width=True):
            try:
                from utils.pdf_generator import generate_pdf_report
                
                with st.spinner('Generating PDF report...'):
                    pdf_buffer = generate_pdf_report(data)
                
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"{selected_company.replace(' ', '_')}_ESG_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("✅ Report generated successfully! Click the button above to download")
                
            except ImportError:
                st.warning("PDF generation module not found. Please ensure `utils/pdf_generator.py` exists")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

# ========== Tab 3: B2C Product Traceability ==========
with tab3:
    st.header("📱 B2C Traceable Trust Label")
    
    st.markdown("""
    This module demonstrates GreenLink's **Innovation Point 3**: B2B2C Value Closed Loop.
    Convert B-side supply chain compliance into C-side consumer-perceptible "trust labels".
    """)
    
    st.markdown("---")
    
    if is_cofco:
        # COFCO perspective: show terminal product
        st.info("💡 **Demo Scenario**: Consumers purchase Fortune edible oil in the supermarket, scan the 'GreenLink Certified' QR code on the bottle to view complete product traceability information.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🏺 Physical Demo Prop")
            
            st.markdown("""
            **Product**: Fortune Edible Oil (5L)
            
            **Features**:
            - ✅ Labeled with "GreenLink Certified" tag
            - ✅ Printed with QR code
            - ✅ Marked "Sustainable Sourcing"
            """)
            
            # Generate QR code
            try:
                import qrcode
                from io import BytesIO
                
                qr_url = "https://xikai0906.github.io/green-link-demo/"
                
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="green", back_color="white")
                
                buf = BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                
                st.image(buf, caption="Scan to view product traceability", width=250)
                
                st.caption(f"🔗 Link: {qr_url}")
                
            except ImportError:
                st.warning("qrcode library required: `pip install qrcode`")
                st.markdown("```\n[QR Code Placeholder]\nScan to view traceability information\n```")
        
        with col2:
            st.subheader("📲 Consumer Mobile Preview")
            
            st.markdown("""
            <div style="border: 3px solid #333; border-radius: 20px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h2 style="text-align: center; margin-bottom: 20px;">🌿 The Green Journey of a Bottle of Oil</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display supply chain traceability
            supply_chain = data.get('supply_chain', {})
            upstream = supply_chain.get('upstream', {})
            suppliers = upstream.get('suppliers', [])
            
            # Raw material origin
            with st.container():
                st.markdown("### 🌍 Raw Material Origin")
                
                if suppliers:
                    for idx, supplier in enumerate(suppliers[:2], 1):  # Show first 2 suppliers
                        col_info1, col_info2 = st.columns([1, 1])
                        
                        with col_info1:
                            st.write(f"**Supplier {idx}**")
                            st.write(f"📍 {supplier.get('country', 'N/A')}")
                            st.write(f"🏭 {supplier.get('name', 'N/A')}")
                        
                        with col_info2:
                            st.write("**Risk Assessment**")
                            risk_status = supplier.get('risk_status', '')
                            if 'Low' in risk_status:
                                st.success(f"✅ {risk_status}")
                            elif 'High' in risk_status:
                                st.warning(f"⚠️ {risk_status}")
                            else:
                                st.info(risk_status)
                        
                        st.markdown("---")
            
            # Processing factory
            with st.container():
                st.markdown("### 🏭 Processing Factory")
                
                st.write(f"**Manufacturer**: {data.get('company', 'N/A')}")
                st.write(f"**Factory Location**: 📍 {data.get('headquarters', 'N/A')}")
                
                st.success("""
                **Quality Certifications**:
                - ✅ ISO 22000 Food Safety Management
                - ✅ HACCP Hazard Analysis
                - ✅ GreenLink ESG Certification
                """)
            
            st.markdown("---")
            
            # Sustainable certification
            with st.container():
                st.markdown("### 📋 Sustainable Certifications")
                
                st.write(f"✅ GreenLink ESG Environmental Risk Assessment: {data['environment']['risk_level']} ({data['environment']['risk_score']} points)")
                st.write(f"✅ GreenLink ESG Social Risk Assessment: {data['social']['risk_level']} ({data['social']['risk_score']} points)")
                st.write("✅ Supply Chain Transparency Certification")
            
            st.markdown("---")
            
            # Thank you message
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;">
                <h3>❤️ Thank You for Your Choice</h3>
                <p>Every purchase of a GreenLink certified product is support for sustainable development!</p>
                <p><small>Powered by GreenLink Technology | Based on Satellite Remote Sensing and AI Analysis</small></p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Upstream supplier perspective: show B2B value
        st.info(f"💡 As an upstream supplier, {data.get('company', 'Supplier')} can enhance brand value through GreenLink certification and gain trust from downstream customers.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 B2B Value")
            
            b2b_value = data.get('b2b_value', {})
            
            for_buyers = b2b_value.get('for_buyers', [])
            if for_buyers:
                st.markdown("**Value for Buyers**")
                for value in for_buyers:
                    st.write(f"✅ {value}")
            
            for_investors = b2b_value.get('for_investors', [])
            if for_investors:
                st.markdown("**Value for Investors**")
                for value in for_investors:
                    st.write(f"📊 {value}")
        
        with col2:
            st.markdown("### 👥 B2C Value")
            
            b2c_value = data.get('b2c_value', {})
            
            st.write(f"**Trust Label**: {b2c_value.get('consumer_trust_label', 'GreenLink ESG Certification')}")
            st.write(f"**Traceability Method**: {b2c_value.get('qr_code_traceability', 'QR Code Scanning')}")
            
            messaging = b2c_value.get('messaging', '')
            if messaging:
                st.info(messaging)

# Sidebar bottom information
st.sidebar.markdown("---")
st.sidebar.subheader("📚 About GreenLink")

st.sidebar.markdown("""
**🎯 Three Innovation Points**

1️⃣ **Alternative Data + AI Analysis**
- 🛰️ Sentinel-2 Satellite Remote Sensing
- 📰 Public Opinion Data Mining
- 🤖 Python Automated Analysis

2️⃣ **E/S Separate Scoring**
- Environment (E): Satellite Verification
- Social (S): Public Opinion Analysis
- Accurately locate risk sources

3️⃣ **B2B2C Value Closed Loop**
- B-side: Risk Early Warning
- B-side: Compliance Report
- C-side: Trust Label
""")

st.sidebar.markdown("---")

# GreenLink advantage display
if 'greenlink_advantage' in data:
    advantage = data['greenlink_advantage']
    
    with st.sidebar.expander("🌟 GreenLink Advantages"):
        vs_traditional = advantage.get('vs_traditional_rating', [])
        for item in vs_traditional:
            st.write(f"- {item}")
        
        real_time = advantage.get('real_time_monitoring', [])
        if real_time:
            st.markdown("**Real-time Monitoring**:")
            for item in real_time:
                st.write(f"- {item}")

st.sidebar.info("""
**💻 Tech Stack**
- Streamlit: Web Application Framework
- Python: Data Analysis
- Sentinel-2: Satellite Data
- ReportLab: PDF Generation
- GitHub Pages: B2C Deployment

**📊 Data Update**
Weekly automatic update
""")

st.sidebar.markdown("---")
st.sidebar.caption("© 2024 GreenLink | Innovation and Entrepreneurship Competition DEMO")
</DOCUMENT>
