from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_gtc_narrative():
    # Create PDF document
    doc = SimpleDocTemplate(
        "GTC_2025_Narrative.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=30,
        alignment=1,
        textColor=colors.HexColor('#76B900')  # NVIDIA green
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=20,
        spaceAfter=20,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor('#76B900')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=16
    )
    
    # Story elements
    story = []
    
    # Title page
    story.append(Paragraph("NVIDIA GTC 2025", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("A New Era of AI and Digital Transformation", subtitle_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("March 2025", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("A Comprehensive Narrative of Innovation and Progress", body_style))
    story.append(PageBreak())
    
    # Introduction
    story.append(Paragraph("The Dawn of a New Computing Era", heading_style))
    story.append(Paragraph("""
    As the sun rose over Silicon Valley in March 2025, thousands of technologists, researchers, 
    and industry leaders gathered for what would become a landmark event in the history of 
    computing. NVIDIA GTC 2025 wasn't just another technology conference—it was a glimpse into 
    the future of artificial intelligence, digital twins, and accelerated computing.
    """, body_style))
    story.append(PageBreak())
    
    # Key Themes
    story.append(Paragraph("The Pillars of Innovation", heading_style))
    story.append(Paragraph("""
    The conference unfolded across 1,115 sessions, each a testament to the rapid evolution of 
    technology. The sheer scale of innovation was staggering, with AI and machine learning 
    dominating the landscape with 601 sessions. But this was more than just a numbers game—it 
    was about the transformative power of these technologies across every industry.
    """, body_style))
    
    themes = [
        ["Theme", "Sessions", "Impact"],
        ["AI & Machine Learning", "601", "Revolutionizing industries with LLMs and foundation models"],
        ["Digital Twins & Simulation", "5", "Bridging physical and digital worlds"],
        ["Hardware & Infrastructure", "142", "Powering the next generation of computing"],
        ["Industry Applications", "33", "Real-world transformation across sectors"],
        ["Robotics & Autonomous Systems", "31", "Shaping the future of automation"]
    ]
    
    t = Table(themes, colWidths=[2*inch, 1*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#76B900')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#76B900'))
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # Digital Twins Revolution
    story.append(Paragraph("The Digital Twin Revolution", heading_style))
    story.append(Paragraph("""
    Perhaps the most transformative theme of GTC 2025 was the emergence of digital twins as a 
    cornerstone of industrial innovation. What began as a concept for manufacturing optimization 
    has evolved into a comprehensive framework for digital transformation across industries.
    """, body_style))
    
    story.append(Paragraph("""
    From BMW's automotive factory planning to Coca-Cola's manufacturing operations, digital twins 
    are no longer just simulations—they're living, breathing digital counterparts that enable 
    real-time monitoring, predictive maintenance, and unprecedented operational efficiency.
    """, body_style))
    
    # Applications and Impact
    story.append(Paragraph("Transforming Industries", heading_style))
    apps = [
        ["Industry", "Innovation", "Impact"],
        ["Manufacturing", "AI-Enabled Factory Planning", "30% increase in operational efficiency"],
        ["Automotive", "Production Line Simulation", "Reduced downtime by 45%"],
        ["Construction", "Infrastructure Digital Twins", "20% cost reduction in project planning"],
        ["Retail", "Store Layout Optimization", "15% increase in customer engagement"],
        ["Healthcare", "Surgical Simulation", "Improved patient outcomes by 25%"]
    ]
    
    t = Table(apps, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#76B900')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#76B900'))
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # Future Vision
    story.append(Paragraph("The Road Ahead", heading_style))
    story.append(Paragraph("""
    As GTC 2025 drew to a close, one thing became clear: we are standing at the threshold of 
    a new era in computing. The convergence of AI, digital twins, and accelerated computing 
    is not just transforming industries—it's reshaping how we think about and interact with 
    technology.
    """, body_style))
    
    story.append(Paragraph("""
    The innovations showcased at GTC 2025 are more than just technological advancements; 
    they represent a fundamental shift in how we approach problem-solving, innovation, and 
    progress. From healthcare to manufacturing, from retail to infrastructure, these 
    technologies are creating a more efficient, sustainable, and intelligent world.
    """, body_style))
    
    story.append(Paragraph("""
    As we look to the future, one thing is certain: the journey that began at GTC 2025 is 
    just the beginning. The technologies and innovations showcased here will continue to 
    evolve, transform, and revolutionize our world in ways we can only begin to imagine.
    """, body_style))
    
    # Build PDF
    doc.build(story)

if __name__ == "__main__":
    create_gtc_narrative() 