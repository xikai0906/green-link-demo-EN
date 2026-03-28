"""
PDF报告生成模块
用于生成ESG合规报告
支持上游供应商（FGV/IOI）和中游加工商（COFCO）的不同数据结构
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import datetime


def generate_pdf_report(data):
    """
    生成ESG合规报告PDF
    
    参数:
        data: 包含公司ESG数据的字典
    
    返回:
        BytesIO: PDF文件的字节流
    """
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # 设置页边距
    margin_left = 2 * cm
    margin_right = width - 2 * cm
    
    # 判断数据类型
    company_name = data.get('company', '未知公司')
    is_cofco = 'COFCO' in company_name or '中粮' in company_name
    is_ioi = 'IOI' in company_name
    
    # ========== 第一页：封面 ==========
    
    # 顶部logo区域（绿色背景）
    c.setFillColorRGB(0.15, 0.68, 0.38)
    c.rect(0, height - 5*cm, width, 5*cm, fill=True, stroke=False)
    
    # 标题（白色文字）
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 3*cm, "GreenLink")
    
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 4*cm, "ESG Risk Assessment Report")
    
    # 公司名称
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 8*cm, company_name)
    
    # 公司描述
    if 'description' in data:
        c.setFont("Helvetica", 11)
        c.drawCentredString(width/2, height - 8.8*cm, data['description'][:80])
    
    # 报告信息框
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(1)
    c.rect(margin_left, height - 12*cm, margin_right - margin_left, 3.5*cm, fill=False, stroke=True)
    
    c.setFont("Helvetica", 11)
    c.drawString(margin_left + 0.5*cm, height - 10*cm, f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    c.drawString(margin_left + 0.5*cm, height - 10.7*cm, f"Report Type: Supply Chain ESG Compliance")
    
    # 根据公司类型显示不同信息
    if is_cofco:
        c.drawString(margin_left + 0.5*cm, height - 11.4*cm, f"Company Type: Midstream Processor / Buyer")
    else:
        c.drawString(margin_left + 0.5*cm, height - 11.4*cm, f"Company Type: Upstream Supplier / Plantation")
    
    # 获取分析周期
    analysis_period = "2018 - 2024"
    if 'environment' in data and 'analysis' in data['environment']:
        period = data['environment']['analysis'].get('period', '2018 - 2024')
        analysis_period = period
    
    c.drawString(margin_left + 0.5*cm, height - 12.1*cm, f"Assessment Period: {analysis_period}")
    
    # 风险等级概览
    y_pos = height - 15*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y_pos, "Risk Level Overview")
    
    y_pos -= 1*cm
    
    # 环境风险
    c.setFont("Helvetica", 11)
    c.drawString(margin_left + 0.5*cm, y_pos, "Environmental Risk (E):")
    c.setFont("Helvetica-Bold", 11)
    
    e_score = data['environment'].get('risk_score', 0)
    e_level = data['environment'].get('risk_level', '未知')
    
    if e_score < 40 or "低" in e_level or "Low" in e_level:
        c.setFillColorRGB(0.15, 0.68, 0.38)  # 绿色
    elif e_score < 70:
        c.setFillColorRGB(0.95, 0.61, 0.07)  # 橙色
    else:
        c.setFillColorRGB(0.91, 0.30, 0.24)  # 红色
    
    c.drawString(margin_left + 6*cm, y_pos, f"{e_level} ({e_score}/100)")
    
    # 社会风险
    y_pos -= 0.8*cm
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    c.drawString(margin_left + 0.5*cm, y_pos, "Social Risk (S):")
    c.setFont("Helvetica-Bold", 11)
    
    s_score = data['social'].get('risk_score', 0)
    s_level = data['social'].get('risk_level', '未知')
    
    if s_score < 40 or "低" in s_level or "Low" in s_level:
        c.setFillColorRGB(0.15, 0.68, 0.38)  # 绿色
    elif s_score < 70:
        c.setFillColorRGB(0.95, 0.61, 0.07)  # 橙色
    else:
        c.setFillColorRGB(0.91, 0.30, 0.24)  # 红色
    
    c.drawString(margin_left + 6*cm, y_pos, f"{s_level} ({s_score}/100)")
    
    # 治理风险（如果有）
    if 'governance' in data:
        y_pos -= 0.8*cm
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Governance Risk (G):")
        c.setFont("Helvetica-Bold", 11)
        
        g_score = data['governance'].get('risk_score', 0)
        g_level = data['governance'].get('risk_level', '低风险')
        
        if g_score < 40:
            c.setFillColorRGB(0.15, 0.68, 0.38)
        else:
            c.setFillColorRGB(0.95, 0.61, 0.07)
        
        c.drawString(margin_left + 6*cm, y_pos, f"{g_level} ({g_score}/100)")
    
    # GreenLink优势说明
    y_pos -= 1.5*cm
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin_left, y_pos, "GreenLink Assessment Advantage:")
    
    y_pos -= 0.7*cm
    c.setFont("Helvetica", 9)
    c.drawString(margin_left + 0.5*cm, y_pos, "✓ Real-time satellite monitoring (weekly updates)")
    y_pos -= 0.5*cm
    c.drawString(margin_left + 0.5*cm, y_pos, "✓ AI-powered sentiment analysis")
    y_pos -= 0.5*cm
    c.drawString(margin_left + 0.5*cm, y_pos, "✓ Separated E/S risk scoring (not aggregated like MSCI)")
    y_pos -= 0.5*cm
    c.drawString(margin_left + 0.5*cm, y_pos, "✓ 90% cost reduction vs traditional ESG ratings")
    
    # 页脚
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 2*cm, "Page 1 | Confidential")
    c.drawCentredString(width/2, 1.5*cm, "Generated by GreenLink Platform | Based on Satellite & AI Analysis")
    
    c.showPage()
    
    # ========== 第二页：环境风险详细分析 ==========
    
    y_pos = height - 3*cm
    
    # 页眉
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(margin_left, y_pos, "Environmental Risk Analysis (E)")
    
    y_pos -= 0.3*cm
    c.setStrokeColorRGB(0.15, 0.68, 0.38)
    c.setLineWidth(2)
    c.line(margin_left, y_pos, margin_right, y_pos)
    
    y_pos -= 1.2*cm
    
    # 分析方法
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_left + 0.5*cm, y_pos, "Analysis Method:")
    c.setFont("Helvetica", 10)
    
    env_analysis = data['environment'].get('analysis', {})
    method = env_analysis.get('method', 'N/A')
    c.drawString(margin_left + 4*cm, y_pos, method[:60])
    
    y_pos -= 0.6*cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_left + 0.5*cm, y_pos, "Analysis Period:")
    c.setFont("Helvetica", 10)
    period = env_analysis.get('period', 'N/A')
    c.drawString(margin_left + 4*cm, y_pos, period)
    
    y_pos -= 0.8*cm
    
    # COFCO特殊处理
    if is_cofco:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Key Findings:")
        y_pos -= 0.6*cm
        
        key_findings = env_analysis.get('key_findings', [])
        c.setFont("Helvetica", 10)
        for finding in key_findings[:4]:
            if y_pos < 5*cm:
                c.showPage()
                y_pos = height - 3*cm
            c.drawString(margin_left + 1*cm, y_pos, f"• {finding}")
            y_pos -= 0.5*cm
        
        y_pos -= 0.5*cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Conclusion:")
        y_pos -= 0.6*cm
        
        conclusion = env_analysis.get('conclusion', '')
    else:
        # FGV/IOI的数据结构
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Conclusion:")
        y_pos -= 0.6*cm
        
        evidence = env_analysis.get('evidence', {})
        conclusion = evidence.get('conclusion', env_analysis.get('result', ''))
        
        # IOI特有的观察记录
        if is_ioi:
            observations = evidence.get('observation', [])
            if observations:
                c.setFont("Helvetica-Bold", 11)
                c.drawString(margin_left + 0.5*cm, y_pos, "Satellite Observations:")
                y_pos -= 0.6*cm
                
                c.setFont("Helvetica", 9)
                for obs in observations[:3]:
                    if y_pos < 5*cm:
                        c.showPage()
                        y_pos = height - 3*cm
                    
                    # 文本换行
                    words = obs.split()
                    line = ""
                    for word in words:
                        test_line = line + word + " "
                        if c.stringWidth(test_line, "Helvetica", 9) > 15*cm:
                            c.drawString(margin_left + 1*cm, y_pos, line)
                            y_pos -= 0.4*cm
                            line = word + " "
                        else:
                            line = test_line
                    if line:
                        c.drawString(margin_left + 1*cm, y_pos, line)
                    y_pos -= 0.6*cm
                
                y_pos -= 0.5*cm
    
    # 打印结论（通用）
    c.setFont("Helvetica", 10)
    words = conclusion.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if c.stringWidth(test_line, "Helvetica", 10) > 16*cm:
            c.drawString(margin_left + 1*cm, y_pos, line)
            y_pos -= 0.5*cm
            if y_pos < 5*cm:
                c.showPage()
                y_pos = height - 3*cm
            line = word + " "
        else:
            line = test_line
    if line:
        c.drawString(margin_left + 1*cm, y_pos, line)
    
    y_pos -= 1*cm
    
    # 合规状态
    if 'compliance' in data['environment']:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Regulatory Compliance:")
        y_pos -= 0.6*cm
        
        compliance = data['environment']['compliance']
        c.setFont("Helvetica", 10)
        for key, value in compliance.items():
            if y_pos < 5*cm:
                c.showPage()
                y_pos = height - 3*cm
            c.drawString(margin_left + 1*cm, y_pos, f"{value}")
            y_pos -= 0.5*cm
    
    # 页脚
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 2*cm, "Page 2 | Confidential")
    
    c.showPage()
    
    # ========== 第三页：社会风险详细分析 ==========
    
    y_pos = height - 3*cm
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(margin_left, y_pos, "Social Risk Analysis (S)")
    
    y_pos -= 0.3*cm
    c.setStrokeColorRGB(0.91, 0.30, 0.24)
    c.setLineWidth(2)
    c.line(margin_left, y_pos, margin_right, y_pos)
    
    y_pos -= 1.2*cm
    
    # COFCO特殊说明
    if is_cofco:
        social_analysis = data['social'].get('analysis', {})
        if social_analysis:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin_left + 0.5*cm, y_pos, "Risk Source:")
            c.setFont("Helvetica", 10)
            c.drawString(margin_left + 4*cm, y_pos, social_analysis.get('risk_source', 'N/A'))
            
            y_pos -= 0.6*cm
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin_left + 0.5*cm, y_pos, "Key Concern:")
            y_pos -= 0.5*cm
            
            concern = social_analysis.get('key_concern', '')
            c.setFont("Helvetica", 10)
            words = concern.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if c.stringWidth(test_line, "Helvetica", 10) > 15*cm:
                    c.drawString(margin_left + 1*cm, y_pos, line)
                    y_pos -= 0.5*cm
                    line = word + " "
                else:
                    line = test_line
            if line:
                c.drawString(margin_left + 1*cm, y_pos, line)
            
            y_pos -= 1*cm
    
    # 关键事件
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_left + 0.5*cm, y_pos, "Key Risk Events:")
    
    y_pos -= 0.7*cm
    
    # 显示最多5个关键事件
    key_events = data['social'].get('key_events', [])
    c.setFont("Helvetica", 9)
    
    for idx, event in enumerate(key_events[:5]):
        if y_pos < 6*cm:
            c.showPage()
            y_pos = height - 3*cm
        
        # 事件日期和标题
        c.setFont("Helvetica-Bold", 10)
        event_date = event.get('date', event.get('year', 'N/A'))
        c.drawString(margin_left + 1*cm, y_pos, f"Event {idx+1}: {event_date}")
        
        y_pos -= 0.5*cm
        
        # 事件描述
        c.setFont("Helvetica", 9)
        event_text = event.get('event', 'N/A')
        if len(event_text) > 100:
            event_text = event_text[:100] + "..."
        
        words = event_text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, "Helvetica", 9) > 15*cm:
                c.drawString(margin_left + 1.5*cm, y_pos, line)
                y_pos -= 0.4*cm
                line = word + " "
            else:
                line = test_line
        if line:
            c.drawString(margin_left + 1.5*cm, y_pos, line)
        
        # 影响说明
        y_pos -= 0.4*cm
        impact_text = event.get('impact', 'N/A')
        if len(impact_text) > 80:
            impact_text = impact_text[:80] + "..."
        c.drawString(margin_left + 1.5*cm, y_pos, f"Impact: {impact_text}")
        
        # 严重程度（如果有）
        if 'severity' in event:
            y_pos -= 0.4*cm
            severity = event['severity']
            if severity in ['严重', '高', 'High', 'Severe']:
                c.setFillColorRGB(0.91, 0.30, 0.24)
            elif severity in ['中', '中等', 'Medium']:
                c.setFillColorRGB(0.95, 0.61, 0.07)
            else:
                c.setFillColorRGB(0.15, 0.68, 0.38)
            c.drawString(margin_left + 1.5*cm, y_pos, f"Severity: {severity}")
            c.setFillColorRGB(0, 0, 0)
        
        y_pos -= 0.8*cm
    
    # 风险缓解措施（COFCO/IOI）
    if 'risk_mitigation' in data['social']:
        if y_pos < 8*cm:
            c.showPage()
            y_pos = height - 3*cm
        
        y_pos -= 0.5*cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "Risk Mitigation Actions:")
        y_pos -= 0.6*cm
        
        c.setFont("Helvetica", 9)
        for action in data['social']['risk_mitigation'][:4]:
            if y_pos < 5*cm:
                c.showPage()
                y_pos = height - 3*cm
            c.drawString(margin_left + 1*cm, y_pos, f"• {action}")
            y_pos -= 0.5*cm
    
    # 页脚
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width/2, 2*cm, "Page 3 | Confidential")
    
    c.showPage()
    
    # ========== 第四页：供应链分析（如果有）==========
    
    if 'supply_chain' in data:
        y_pos = height - 3*cm
        
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(margin_left, y_pos, "Supply Chain Risk Analysis")
        
        y_pos -= 0.3*cm
        c.setStrokeColorRGB(0.15, 0.68, 0.38)
        c.setLineWidth(2)
        c.line(margin_left, y_pos, margin_right, y_pos)
        
        y_pos -= 1.2*cm
        
        supply_chain = data['supply_chain']
        
        if is_cofco:
            # COFCO视角：展示上游供应商
            if 'upstream' in supply_chain:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin_left, y_pos, "Upstream Suppliers Risk Assessment:")
                y_pos -= 0.8*cm
                
                upstream = supply_chain['upstream']
                suppliers = upstream.get('suppliers', [])
                
                c.setFont("Helvetica", 10)
                for supplier in suppliers[:3]:
                    if y_pos < 6*cm:
                        c.showPage()
                        y_pos = height - 3*cm
                    
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(margin_left + 0.5*cm, y_pos, supplier.get('name', 'N/A'))
                    y_pos -= 0.5*cm
                    
                    c.setFont("Helvetica", 9)
                    c.drawString(margin_left + 1*cm, y_pos, f"Location: {supplier.get('country', 'N/A')}")
                    y_pos -= 0.4*cm
                    c.drawString(margin_left + 1*cm, y_pos, f"Product: {supplier.get('product', 'N/A')}")
                    y_pos -= 0.4*cm
                    
                    risk_status = supplier.get('risk_status', 'N/A')
                    if '高' in risk_status or 'High' in risk_status:
                        c.setFillColorRGB(0.91, 0.30, 0.24)
                    elif '低' in risk_status or 'Low' in risk_status:
                        c.setFillColorRGB(0.15, 0.68, 0.38)
                    else:
                        c.setFillColorRGB(0.95, 0.61, 0.07)
                    
                    c.drawString(margin_left + 1*cm, y_pos, f"Risk Status: {risk_status}")
                    c.setFillColorRGB(0, 0, 0)
                    
                    if supplier.get('note'):
                        y_pos -= 0.4*cm
                        c.setFont("Helvetica-Oblique", 8)
                        c.drawString(margin_left + 1*cm, y_pos, supplier['note'][:70])
                    
                    y_pos -= 0.8*cm
                
                # 风险传导路径
                risk_paths = upstream.get('risk_transmission_path', [])
                if risk_paths:
                    y_pos -= 0.5*cm
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(margin_left, y_pos, "Risk Transmission Pathways:")
                    y_pos -= 0.6*cm
                    
                    c.setFont("Helvetica", 9)
                    for path in risk_paths:
                        if y_pos < 5*cm:
                            c.showPage()
                            y_pos = height - 3*cm
                        c.drawString(margin_left + 0.5*cm, y_pos, f"→ {path}")
                        y_pos -= 0.5*cm
        
        else:
            # FGV/IOI视角：展示下游影响
            if 'downstream' in supply_chain:
                downstream = supply_chain['downstream']
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margin_left, y_pos, "Downstream Market Impact:")
                y_pos -= 0.8*cm
                
                # 主要客户（IOI）
                major_customers = downstream.get('major_customers', [])
                if major_customers:
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(margin_left + 0.5*cm, y_pos, "Major Customers:")
                    y_pos -= 0.5*cm
                    
                    c.setFont("Helvetica", 9)
                    for customer in major_customers[:8]:
                        if y_pos < 5*cm:
                            c.showPage()
                            y_pos = height - 3*cm
                        c.drawString(margin_left + 1*cm, y_pos, f"• {customer}")
                        y_pos -= 0.4*cm
                    
                    y_pos -= 0.5*cm
                
                # 市场
                markets = downstream.get('markets', [])
                if markets:
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(margin_left + 0.5*cm, y_pos, "Target Markets:")
                    y_pos -= 0.5*cm
                    
                    c.setFont("Helvetica", 9)
                    for market in markets[:5]:
                        if isinstance(market, dict):
                            region = market.get('region', market)
                            c.drawString(margin_left + 1*cm, y_pos, f"• {region}")
                        else:
                            c.drawString(margin_left + 1*cm, y_pos, f"• {market}")
                        y_pos -= 0.4*cm
        
        # 页脚
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, 2*cm, "Page 4 | Confidential")
        
        c.showPage()
    
    # ========== 最后一页：建议措施 ==========
    
    y_pos = height - 3*cm
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(margin_left, y_pos, "Recommended Actions")
    
    y_pos -= 0.3*cm
    c.setStrokeColorRGB(0.15, 0.68, 0.38)
    c.setLineWidth(2)
    c.line(margin_left, y_pos, margin_right, y_pos)
    
    y_pos -= 1.5*cm
    
    # 如果数据中有recommendations，使用它
    if 'recommendations' in data:
        recommendations = data['recommendations']
        
        if 'immediate' in recommendations:
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_left, y_pos, "Immediate Actions:")
            y_pos -= 0.8*cm
            
            c.setFont("Helvetica", 10)
            for idx, rec in enumerate(recommendations['immediate'][:4], 1):
                c.drawString(margin_left + 0.5*cm, y_pos, f"{idx}. {rec}")
                y_pos -= 0.6*cm
            
            y_pos -= 0.5*cm
        
        if 'medium_term' in recommendations:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_left, y_pos, "Medium-term Actions:")
            y_pos -= 0.8*cm
            
            c.setFont("Helvetica", 10)
            for idx, rec in enumerate(recommendations['medium_term'][:4], 1):
                if y_pos < 5*cm:
                    c.showPage()
                    y_pos = height - 3*cm
                c.drawString(margin_left + 0.5*cm, y_pos, f"{idx}. {rec}")
                y_pos -= 0.6*cm
    
    else:
        # 默认建议
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_left, y_pos, "Immediate Actions:")
        
        y_pos -= 0.8*cm
        
        if is_cofco:
            recommendations_list = [
                "1. Complete on-site audit of high-risk suppliers (FGV, IOI)",
                "2. Prepare EUDR compliance documentation package",
                "3. Communicate supply chain improvement progress to EU/US customers",
                "4. Increase procurement from low-risk suppliers to >50%"
            ]
        else:
            recommendations_list = [
                "1. Conduct comprehensive supplier ESG audit within 30 days",
                "2. Engage with downstream customers on ESG improvement plans",
                "3. Implement real-time monitoring system for high-risk indicators",
                "4. Obtain third-party certification (RSPO, EUDR compliance)"
            ]
        
        c.setFont("Helvetica", 11)
        for rec in recommendations_list:
            c.drawString(margin_left + 0.5*cm, y_pos, rec)
            y_pos -= 0.7*cm
        
        y_pos -= 0.5*cm
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin_left, y_pos, "Long-term Strategy:")
        y_pos -= 0.8*cm
        
        c.setFont("Helvetica", 11)
        c.drawString(margin_left + 0.5*cm, y_pos, "• Establish comprehensive supply chain ESG monitoring system")
        y_pos -= 0.7*cm
        c.drawString(margin_left + 0.5*cm, y_pos, "• Diversify supply chain to reduce concentration risk")
        y_pos -= 0.7*cm
        c.drawString(margin_left + 0.5*cm, y_pos, "• Increase supply chain transparency and traceability")
        y_pos -= 0.7*cm
        c.drawString(margin_left + 0.5*cm, y_pos, "• Obtain GreenLink certification to enhance competitiveness")
    
    # 联系信息
    y_pos -= 1.5*cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin_left, y_pos, "For More Information:")
    y_pos -= 0.6*cm
    
    c.setFont("Helvetica", 10)
    c.drawString(margin_left + 0.5*cm, y_pos, "GreenLink ESG Platform")
    y_pos -= 0.5*cm
    c.drawString(margin_left + 0.5*cm, y_pos, "Email: support@greenlink.com")
    y_pos -= 0.5*cm
    c.drawString(margin_left + 0.5*cm, y_pos, "Website: www.greenlink.com")
    
    # 页脚
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    page_num = 5 if 'supply_chain' in data else 4
    c.drawCentredString(width/2, 2*cm, f"Page {page_num} | Confidential")
    c.drawCentredString(width/2, 1.5*cm, "End of Report")
    
    c.save()
    
    buffer.seek(0)
    return buffer
