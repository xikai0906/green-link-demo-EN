from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- 1. Font and Color Configuration ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# For English version, we use standard Helvetica fonts (no Chinese font dependency)
FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_LOADED = False

# Attempt to load Chinese fonts if available (optional for bilingual support)
try:
    FONT_REGULAR_PATH = os.path.join(BASE_DIR, 'fonts', 'AlibabaPuHuiTi-3-55-Regular.ttf')
    FONT_BOLD_PATH = os.path.join(BASE_DIR, 'fonts', 'AlibabaPuHuiTi-3-85-Bold.ttf')
    if os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH):
        pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Regular', FONT_REGULAR_PATH))
        pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi-Bold', FONT_BOLD_PATH))
        FONT_REG = "AlibabaPuHuiTi-Regular"
        FONT_BOLD = "AlibabaPuHuiTi-Bold"
        FONT_LOADED = True
        print("✓ Chinese fonts loaded successfully (Alibaba PuHuiTi)")
except Exception as e:
    print(f"Note: Using standard Helvetica fonts. Chinese characters may not render correctly if present.")


COLOR_PRIMARY = HexColor("#27ae60")
COLOR_TITLE = HexColor("#2c3e50")
COLOR_TEXT = HexColor("#333333")
COLOR_SUBTLE = HexColor("#7f8c8d")
RISK_LOW = HexColor("#27ae60")
RISK_MEDIUM = HexColor("#f39c12")
RISK_HIGH = HexColor("#e74c3c")

WIDTH, HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = WIDTH - 2 * cm
Y_START = HEIGHT - 2.5 * cm

# --- 2. Core Drawing Functions ---

def check_page_break(c, y, needed_space=4*cm):
    """Check if page break is needed, return new Y coordinate if so"""
    if y < needed_space:
        c.showPage()
        draw_footer(c, c.getPageNumber())
        return Y_START
    return y

def draw_wrapped_text(c, x, y, text, font_name, font_size, max_width):
    """
    Draw wrapped text at specified coordinates (x, y)
    Returns the new Y coordinate after drawing
    """
    c.setFont(font_name, font_size)
    text = str(text)
    
    line = ""
    line_height = (font_size * 1.3) / 72 * cm
    
    for char in text:
        test_line = line + char
        is_bullet = (char in ['•', '✓', '1.', '2.', '3.']) and line == ""
        
        current_x = x
        current_max_width = max_width
        
        if is_bullet:
            c.drawString(current_x, y, char)
            current_x += 0.6*cm
            current_max_width -= 0.6*cm
        else:
            if c.stringWidth(test_line, font_name, font_size) > current_max_width:
                c.drawString(current_x, y, line)
                y -= line_height
                line = char
            else:
                line = test_line
                
    c.drawString(current_x, y, line)
    y -= line_height
    
    return y

def draw_section_header(c, y, title, subtitle, color):
    """Draw section header with title and English subtitle"""
    y = check_page_break(c, y, 6*cm)
    
    c.setFont(FONT_BOLD, 14)
    c.setFillColor(color)
    c.drawString(MARGIN_LEFT, y, title)
    
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT, y - 0.5*cm, subtitle)
    
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.line(MARGIN_LEFT, y - 0.8*cm, MARGIN_RIGHT, y - 0.8*cm)
    
    return y - 1.8*cm

def draw_bilingual_field(c, y, label_cn, label_en, value_text, value_color=COLOR_TEXT):
    """Draw bilingual field (Chinese label + English subtitle)"""
    y = check_page_break(c, y, 4*cm)
    
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, label_cn)
    
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, label_en)
    
    label_bottom_y = y - 0.4*cm - (9 * 1.3) / 72 * cm
    
    c.setFillColor(value_color)
    value_x = MARGIN_LEFT + 5.5*cm
    max_width = MARGIN_RIGHT - value_x
    
    if isinstance(value_text, (list, tuple)):
        current_y = y
        for item in value_text:
            current_y = draw_wrapped_text(c, value_x, current_y, str(item), FONT_REG, 10, max_width)
        value_bottom_y = current_y
    else:
        value_bottom_y = draw_wrapped_text(c, value_x, y, str(value_text), FONT_REG, 10, max_width)
    
    return min(label_bottom_y, value_bottom_y) - 0.3*cm

def draw_wrapped_block(c, y, text_list, font_name=None, font_size=10, indent=1.0*cm):
    """Draw text block"""
    if font_name is None:
        font_name = FONT_REG
    
    c.setFillColor(COLOR_TEXT)
    
    base_x = MARGIN_LEFT + indent
    max_width = MARGIN_RIGHT - base_x
    
    for text in text_list:
        y = check_page_break(c, y, 4*cm)
        y = draw_wrapped_text(c, base_x, y, str(text), font_name, font_size, max_width)
    
    return y - 0.3*cm

def set_risk_color(c, level, score):
    """Set risk color based on level or score"""
    level_str = str(level).lower()
    
    if "low" in level_str or score < 40:
        c.setFillColor(RISK_LOW)
        return RISK_LOW
    elif "medium" in level_str or score < 70:
        c.setFillColor(RISK_MEDIUM)
        return RISK_MEDIUM
    else:
        c.setFillColor(RISK_HIGH)
        return RISK_HIGH

def draw_footer(c, page_num):
    """Draw page footer"""
    c.setFont(FONT_REG, 8)
    c.setFillColor(COLOR_SUBTLE)
    c.drawCentredString(WIDTH/2, 1.5*cm, 
                       f"Page {page_num} | Confidential")
    c.drawCentredString(WIDTH/2, 1*cm, 
                       "Generated by GreenLink Platform | Based on Satellite & AI Analysis")

# ============================================================
# Main PDF Generation Function
# ============================================================

def generate_pdf_report(data):
    """Generate ESG Report PDF"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(f"{data.get('company', 'Report')} - ESG Report")
    
    company_name = data.get('company', 'Unknown Company')
    is_cofco = 'COFCO' in company_name or '中粮' in company_name
    env_data = data.get('environment', {})
    social_data = data.get('social', {})
    supply_chain_data = data.get('supply_chain', {})
    page_num = 1
    
    # ==================================================
    # Page 1: Cover
    # ==================================================
    
    c.setFillColor(COLOR_PRIMARY)
    c.rect(0, HEIGHT - 5*cm, WIDTH, 5*cm, fill=True, stroke=False)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(FONT_BOLD, 32)
    c.drawCentredString(WIDTH/2, HEIGHT - 2.8*cm, "GreenLink")
    
    c.setFont(FONT_REG, 16)
    c.drawCentredString(WIDTH/2, HEIGHT - 3.8*cm, 
                       "ESG Risk Assessment Report")
    
    c.setFillColor(COLOR_TITLE)
    c.setFont(FONT_BOLD, 22)
    c.drawCentredString(WIDTH/2, HEIGHT - 7.5*cm, company_name)
    
    y = HEIGHT - 10*cm
    c.setFont(FONT_REG, 11)
    c.drawCentredString(WIDTH/2, y, 
                       f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
    y -= 0.6*cm
    
    if is_cofco:
        company_type = "Midstream Processor / Buyer"
    else:
        company_type = "Upstream Supplier / Plantation Owner"
    
    c.drawCentredString(WIDTH/2, y, 
                       f"Company Type: {company_type}")
    y -= 0.6*cm
    
    period = env_data.get('analysis', {}).get('period', 'N/A')
    c.drawCentredString(WIDTH/2, y, 
                       f"Assessment Period: {period}")
    
    # Risk Overview
    y = HEIGHT - 15*cm
    y = draw_section_header(c, y, "Risk Level Overview", "Risk Level Overview", COLOR_PRIMARY)
    
    e_level = env_data.get('risk_level', 'Unknown')
    e_score = env_data.get('risk_score', 0)
    e_color = set_risk_color(c, e_level, e_score)
    y = draw_bilingual_field(c, y, "Environmental Risk (E)", "Environmental Risk (E)", 
                             f"{e_level} ({e_score}/100)", value_color=e_color)
    
    s_level = social_data.get('risk_level', 'Unknown')
    s_score = social_data.get('risk_score', 0)
    s_color = set_risk_color(c, s_level, s_score)
    y = draw_bilingual_field(c, y, "Social Risk (S)", "Social Risk (S)", 
                             f"{s_level} ({s_score}/100)", value_color=s_color)
    
    # Platform Advantages
    y -= 1*cm
    y = draw_section_header(c, y, "GreenLink Assessment Advantages", "GreenLink Advantage", COLOR_TITLE)
    
    advantages = [
        "✓ Real-time Satellite Monitoring (E)",
        "✓ AI-Powered Sentiment Analysis (S)",
        "✓ E/S Separated Risk Scoring",
        "✓ EU EUDR Compliance Validation"
    ]
    
    c.setFont(FONT_REG, 10)
    current_y = y
    for adv in advantages:
        c.setFillColor(COLOR_TEXT)
        c.drawString(MARGIN_LEFT + 0.5*cm, current_y, adv)
        current_y -= 0.6*cm
    y = current_y
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # Page 2: Environmental Risk
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "Environmental Risk Analysis (E)", 
                           "Environmental Risk Analysis (E)", COLOR_PRIMARY)
    
    env_analysis = env_data.get('analysis', {})
    
    y = draw_bilingual_field(c, y, "Analysis Method", "Analysis Method", 
                             env_analysis.get('method', 'N/A'))
    y = draw_bilingual_field(c, y, "Analysis Period", "Analysis Period", 
                             env_analysis.get('period', 'N/A'))
    
    y -= 0.5*cm
    y = check_page_break(c, y, 1*cm)
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "Key Findings / Conclusion")
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Findings / Conclusion")
    y -= 1*cm
    
    if is_cofco:
        findings = env_analysis.get('key_findings', ['N/A'])
        y = draw_wrapped_block(c, y, [f"• {f}" for f in findings])
        y -= 0.5*cm
        y = draw_wrapped_block(c, y, [f"Conclusion: {env_analysis.get('conclusion', 'N/A')}"], FONT_BOLD, 10)
    else:
        evidence = env_analysis.get('evidence', {})
        conclusion = evidence.get('conclusion', env_analysis.get('result', 'N/A'))
        y = draw_wrapped_block(c, y, [conclusion])
    
    # Regulatory Compliance
    y -= 1*cm
    
    compliance = env_data.get('compliance', {})
    if compliance:
        compliance_items = [f"• {v}" for v in compliance.values()]
    else:
        compliance_items = ["• No data available"]
        
    y = draw_bilingual_field(c, y, "Regulatory Compliance", "Regulatory Compliance", compliance_items)
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # Page 3: Social Risk
    # ==================================================
    
    y = Y_START
    y = draw_section_header(c, y, "Social Risk Analysis (S)", 
                           "Social Risk Analysis (S)", RISK_HIGH)
    
    if is_cofco:
        social_analysis = social_data.get('analysis', {})
        y = draw_bilingual_field(c, y, "Risk Source", "Risk Source", 
                                 social_analysis.get('risk_source', 'N/A'))
        y = draw_bilingual_field(c, y, "Key Concern", "Key Concern", 
                                 social_analysis.get('key_concern', 'N/A'))
        y -= 1*cm
    
    y = check_page_break(c, y, 1*cm)
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "Key Risk Events")
    c.setFont(FONT_REG, 9)
    c.setFillColor(COLOR_SUBTLE)
    c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Risk Events")
    y -= 1*cm
    
    key_events = social_data.get('key_events', [])
    if not key_events:
        y = draw_wrapped_block(c, y, 
                             ["No significant negative sentiment events found"])
    
    for event in key_events[:4]:
        y = check_page_break(c, y, 6*cm)
        if y == Y_START:
            y = draw_section_header(c, y, "Social Risk Analysis (S) - Continued", 
                                  "Social Risk Analysis (S) - Cont.", RISK_HIGH)
            y = check_page_break(c, y, 1*cm)
            c.setFont(FONT_BOLD, 10)
            c.setFillColor(COLOR_TITLE)
            c.drawString(MARGIN_LEFT + 0.5*cm, y, "Key Risk Events (Continued)")
            c.setFont(FONT_REG, 9)
            c.setFillColor(COLOR_SUBTLE)
            c.drawString(MARGIN_LEFT + 0.5*cm, y - 0.4*cm, "Key Risk Events (Cont.)")
            y -= 1*cm
        
        event_date = event.get('date', event.get('year', 'N/A'))
        event_text = event.get('event', 'N/A')
        event_impact = event.get('impact', 'N/A')
        
        y = draw_bilingual_field(c, y, "Date", "", event_date)
        y = draw_bilingual_field(c, y, "Event", "", event_text)
        y = draw_bilingual_field(c, y, "Impact", "", event_impact)
        
        c.line(MARGIN_LEFT, y + 0.2*cm, MARGIN_RIGHT, y + 0.2*cm)
        y -= 0.5*cm
    
    draw_footer(c, page_num)
    c.showPage()
    page_num += 1
    
    # ==================================================
    # Page 4: Supply Chain & Recommendations
    # ==================================================
    
    y = Y_START
    
    if supply_chain_data:
        y = draw_section_header(c, y, "Supply Chain Analysis", "Supply Chain Analysis", COLOR_TITLE)
        
        if is_cofco:
            suppliers = supply_chain_data.get('upstream', {}).get('suppliers', [])
            y = draw_wrapped_block(c, y, 
                                 ["Identified high-risk upstream suppliers:"], 
                                 FONT_BOLD, 10, indent=0.5*cm)
            
            for supplier in suppliers[:3]:
                name = supplier.get('name', 'N/A')
                status = supplier.get('risk_status', 'N/A')
                color = set_risk_color(c, status, 100 if 'High' in status else 30)
                y = draw_bilingual_field(c, y, f"• {name}", "", status, value_color=color)
        else:
            markets = supply_chain_data.get('downstream', {}).get('markets', [])
            y = draw_wrapped_block(c, y, 
                                 ["Downstream Market Compliance Risks:"], 
                                 FONT_BOLD, 10, indent=0.5*cm)
            y = draw_wrapped_block(c, y, 
                                 [f"• Target Markets: {', '.join(markets)}"])
            y = draw_wrapped_block(c, y, 
                                 [f"• Key Risks: EU EUDR and U.S. CBP Regulations"])
        
        y -= 1*cm
    
    y = check_page_break(c, y, 8*cm)
    
    y = draw_section_header(c, y, "Recommended Actions", "Recommended Actions", COLOR_PRIMARY)
    
    if is_cofco:
        recs = [
            "1. Initiate detailed due diligence on high-risk suppliers.",
            "2. Prepare EUDR compliance documentation and ensure traceability.",
            "3. Increase procurement proportion from low-risk suppliers."
        ]
    else:
        recs = [
            "1. Immediately submit remediation report to CBP (labor issues) or EUDR (deforestation).",
            "2. Implement and disclose labor/environmental remediation measures.",
            "3. Establish a transparent grievance mechanism."
        ]
    
    y = draw_wrapped_block(c, y, recs)
    
    y = check_page_break(c, y, 4*cm)
    
    # --- Report End ---
    y -= 2*cm
    c.setFont(FONT_BOLD, 11)
    c.setFillColor(COLOR_TITLE)
    c.drawString(MARGIN_LEFT, y, "Contact Us:")
    y -= 0.6*cm
    
    c.setFont(FONT_REG, 10)
    c.setFillColor(COLOR_TEXT)
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "GreenLink ESG Platform")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "Email: support@greenlink.com")
    y -= 0.5*cm
    c.drawString(MARGIN_LEFT + 0.5*cm, y, "Website: www.greenlink.com")
    
    draw_footer(c, page_num)
    
    c.save()
    buffer.seek(0)
    
    return buffer
