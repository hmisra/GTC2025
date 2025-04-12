from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_gtc_documentation():
    # Create PDF document
    doc = SimpleDocTemplate(
        "GTC_2025_Documentation.pdf",
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
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Story elements
    story = []
    
    # Title page
    story.append(Paragraph("NVIDIA GTC 2025", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Global Technology Conference", heading_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("March 2025", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Comprehensive Documentation", body_style))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph("""
    NVIDIA GTC 2025 was a landmark event showcasing the latest advancements in AI, 
    accelerated computing, and digital twins. The conference brought together industry 
    leaders, researchers, and developers to explore cutting-edge technologies and their 
    real-world applications.
    """, body_style))
    story.append(PageBreak())
    
    # Key Themes
    story.append(Paragraph("Key Themes", heading_style))
    themes = [
        ["Theme", "Description"],
        ["AI & Machine Learning", "601 sessions covering foundational models, LLMs, and AI applications"],
        ["Digital Twins & Simulation", "Advanced simulation and digital twin technologies"],
        ["Hardware & Infrastructure", "142 sessions on next-gen computing infrastructure"],
        ["Industry Applications", "33 sessions on real-world AI implementations"],
        ["Robotics & Autonomous Systems", "31 sessions on autonomous technologies"]
    ]
    
    t = Table(themes, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # Digital Twins Focus
    story.append(Paragraph("Digital Twins: Transforming Industries", heading_style))
    story.append(Paragraph("""
    Digital twins emerged as a key focus area at GTC 2025, with applications spanning 
    multiple industries including manufacturing, automotive, construction, and retail. 
    These virtual representations enable real-time monitoring, simulation, and optimization 
    of physical systems and processes.
    """, body_style))
    
    # Applications table
    apps = [
        ["Industry", "Application", "Benefits"],
        ["Manufacturing", "Factory Planning & Optimization", "Process optimization, predictive maintenance"],
        ["Automotive", "Production Line Simulation", "Quality control, efficiency improvement"],
        ["Construction", "Infrastructure Planning", "Resource management, design validation"],
        ["Retail", "Store Layout & Merchandising", "Customer experience enhancement"],
        ["Logistics", "Warehouse Optimization", "Efficiency improvement, resource allocation"]
    ]
    
    t = Table(apps, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # Conclusion
    story.append(Paragraph("Conclusion", heading_style))
    story.append(Paragraph("""
    GTC 2025 demonstrated the rapid evolution of AI and digital twin technologies, 
    showcasing their transformative potential across industries. The conference highlighted 
    NVIDIA's commitment to advancing these technologies and their real-world applications, 
    setting the stage for continued innovation in the years to come.
    """, body_style))
    
    # Build PDF
    doc.build(story)

if __name__ == "__main__":
    create_gtc_documentation() 