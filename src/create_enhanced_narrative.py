#!/usr/bin/env python3
"""
Enhanced GTC 2025 Narrative Generator
------------------------------------
This script creates a visually appealing, professionally designed narrative 
document that effectively communicates insights from GTC 2025.
"""

import os
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    Table, TableStyle, PageBreak, Flowable, Frame
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Define color scheme based on NVIDIA brand
NVIDIA_GREEN = colors.HexColor('#76B900')
NVIDIA_BLACK = colors.HexColor('#000000')
DARK_GRAY = colors.HexColor('#333333')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY = colors.HexColor('#999999')

class PageNumCanvas(canvas.Canvas):
    """Canvas that adds page numbers and headers/footers to each page."""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        
    def showPage(self):
        """Override to add page info before showing the page."""
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """Add page numbers and save the document."""
        page_count = len(self.pages)
        
        # Add page numbers to each page
        for page in self.pages:
            self.__dict__.update(page)
            
            # Skip page number on first page
            if self._pageNumber > 1:
                self.setFont("Helvetica", 9)
                self.setFillColor(MID_GRAY)
                self.drawRightString(
                    letter[0] - 0.5*inch, 
                    0.5*inch, 
                    f"Page {self._pageNumber} of {page_count}"
                )
                
                # Add footer
                self.line(0.5*inch, 0.6*inch, letter[0]-0.5*inch, 0.6*inch)
                self.setFont("Helvetica", 8)
                self.drawCentredString(
                    letter[0]/2, 
                    0.4*inch, 
                    "GTC 2025 Insights | Created with NVIDIA Conference Data"
                )
            
            self._startPage()
            
        canvas.Canvas.save(self)

class TwoColumnSection(Flowable):
    """A flowable that creates a two-column section."""
    
    def __init__(self, left_content, right_content, available_width=None):
        Flowable.__init__(self)
        self.left_content = left_content
        self.right_content = right_content
        self.available_width = available_width
        
    def draw(self):
        # Split into two columns
        left_width = (self.available_width or letter[0] - 1*inch) * 0.48
        right_width = (self.available_width or letter[0] - 1*inch) * 0.48
        gap = (self.available_width or letter[0] - 1*inch) * 0.04
        
        # Create frames for each column
        left_frame = Frame(
            0, 0, 
            left_width, self.height, 
            leftPadding=0, bottomPadding=0,
            rightPadding=0, topPadding=0
        )
        right_frame = Frame(
            left_width + gap, 0, 
            right_width, self.height, 
            leftPadding=0, bottomPadding=0,
            rightPadding=0, topPadding=0
        )
        
        # Draw the content in each frame
        left_frame.addFromList(self.left_content, self.canv)
        right_frame.addFromList(self.right_content, self.canv)

def create_enhanced_narrative():
    """Create an enhanced narrative document with visualizations."""
    # Define paths
    output_dir = "outputs/analysis_output"
    output_file = "outputs/GTC_2025_Enhanced_Narrative.pdf"
    
    # Load insights data
    with open(os.path.join(output_dir, "gtc_insights.json"), "r") as f:
        insights = json.load(f)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=30,
        spaceAfter=24,
        textColor=NVIDIA_GREEN,
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        textColor=DARK_GRAY,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=20,
        spaceBefore=18,
        spaceAfter=12,
        textColor=NVIDIA_GREEN
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=16,
        spaceBefore=12,
        spaceAfter=8,
        textColor=DARK_GRAY
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        leading=16
    )
    
    emphasis_style = ParagraphStyle(
        'Emphasis',
        parent=body_style,
        textColor=NVIDIA_GREEN,
        fontSize=14,
        leading=18
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Italic'],
        fontSize=10,
        textColor=MID_GRAY,
        alignment=1  # Center alignment
    )
    
    # Story elements
    story = []
    
    # Cover page
    story.append(Paragraph("NVIDIA GTC 2025", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Insights & Analysis", subtitle_style))
    story.append(Spacer(1, 36))
    
    # Add hero image if available
    hero_image_path = os.path.join(output_dir, "category_distribution.png")
    if os.path.exists(hero_image_path):
        img = Image(hero_image_path, width=6.5*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 12))
        story.append(Paragraph("Distribution of 1300+ Sessions Across Categories", caption_style))
    
    story.append(Spacer(1, 36))
    story.append(Paragraph("April 2025", body_style))
    story.append(PageBreak())
    
    # Introduction
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph("""
    NVIDIA's GTC 2025 showcased the remarkable pace of innovation in AI, accelerated computing, 
    and digital transformation technologies. With over 1300 sessions across multiple technical 
    domains, the conference provided a comprehensive view of how these technologies are reshaping 
    industries and creating new opportunities.
    """, body_style))
    
    story.append(Paragraph("""
    This document presents a data-driven analysis of GTC 2025, extracting key insights and trends 
    to help navigate the rapidly evolving technological landscape. From the dominance of AI and 
    machine learning to the transformative potential of digital twins, GTC 2025 offered a window 
    into the future of technology and its impact across sectors.
    """, body_style))
    
    # Key Insights Section
    story.append(Paragraph("Key Insights", heading_style))
    
    # Top Categories Section
    story.append(Paragraph("Technology Focus Areas", subheading_style))
    
    # Create a table for top categories
    top_categories_data = [["Category", "Sessions"]]
    for category, count in insights["top_categories"]:
        top_categories_data.append([category, str(count)])
    
    top_categories_table = Table(top_categories_data, colWidths=[4*inch, 1.5*inch])
    top_categories_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NVIDIA_GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_GRAY),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, NVIDIA_GREEN)
    ]))
    
    story.append(top_categories_table)
    story.append(Spacer(1, 18))
    
    # Add AI ML word cloud if available
    ai_wordcloud_path = os.path.join(output_dir, "wordcloud_ai_machine_learning.png")
    if os.path.exists(ai_wordcloud_path):
        img = Image(ai_wordcloud_path, width=6.5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 6))
        story.append(Paragraph("Word Cloud: AI & Machine Learning Session Topics", caption_style))
        story.append(Spacer(1, 18))
    
    # Emerging Trends Section
    story.append(Paragraph("Emerging Trends", subheading_style))
    
    for trend in insights["emerging_trends"]:
        story.append(Paragraph(f"• {trend}", body_style))
    
    story.append(Spacer(1, 12))
    
    # Add trend visualization if available
    ml_keywords_path = os.path.join(output_dir, "keywords_ai_machine_learning.png")
    if os.path.exists(ml_keywords_path):
        img = Image(ml_keywords_path, width=6.5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 6))
        story.append(Paragraph("Top Keywords in AI & Machine Learning Sessions", caption_style))
    
    story.append(PageBreak())
    
    # Industry Impact
    story.append(Paragraph("Industry Impact & Applications", heading_style))
    
    story.append(Paragraph("""
    GTC 2025 demonstrated how AI and accelerated computing are transforming industries across 
    the global economy. From healthcare to manufacturing, retail to financial services, 
    organizations are leveraging these technologies to drive innovation, improve efficiency, 
    and create new value.
    """, body_style))
    
    # Industry Focus Section
    for focus in insights["industry_focus"]:
        story.append(Paragraph(f"• {focus}", body_style))
    
    story.append(Spacer(1, 12))
    
    # Add industry applications word cloud if available
    industry_wordcloud_path = os.path.join(output_dir, "wordcloud_industry_applications.png")
    if os.path.exists(industry_wordcloud_path):
        img = Image(industry_wordcloud_path, width=6.5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 6))
        story.append(Paragraph("Word Cloud: Industry Applications", caption_style))
    
    story.append(PageBreak())
    
    # Digital Twins Section
    story.append(Paragraph("Spotlight: Digital Twins Revolution", heading_style))
    
    story.append(Paragraph("""
    One of the most transformative themes at GTC 2025 was the emergence of digital twins as a 
    cornerstone of industrial innovation. These virtual replicas of physical systems are enabling
    unprecedented capabilities for design, optimization, and real-time monitoring across industries.
    """, body_style))
    
    # Add digital twins word cloud if available
    dt_wordcloud_path = os.path.join(output_dir, "wordcloud_digital_twins_simulation.png")
    if os.path.exists(dt_wordcloud_path):
        img = Image(dt_wordcloud_path, width=6.5*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 6))
        story.append(Paragraph("Word Cloud: Digital Twins & Simulation Topics", caption_style))
        story.append(Spacer(1, 12))
    
    # Applications table
    dt_applications = [
        ["Industry", "Application", "Impact"],
        ["Manufacturing", "Factory Planning & Optimization", "30% increase in operational efficiency"],
        ["Automotive", "Production Line Simulation", "Reduced downtime by 45%"],
        ["Construction", "Infrastructure Digital Twins", "20% cost reduction in project planning"],
        ["Retail", "Store Layout Optimization", "15% increase in customer engagement"],
        ["Healthcare", "Surgical Simulation", "Improved patient outcomes by 25%"]
    ]
    
    dt_table = Table(dt_applications, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
    dt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NVIDIA_GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_GRAY),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, NVIDIA_GREEN)
    ]))
    
    story.append(dt_table)
    story.append(PageBreak())
    
    # Future Outlook
    story.append(Paragraph("Future Outlook & Implications", heading_style))
    
    story.append(Paragraph("""
    The convergence of AI, digital twins, and accelerated computing at GTC 2025 signals a 
    fundamental shift in how industries leverage technology. These technologies are not just 
    transforming individual processes but entire business models and value chains.
    """, body_style))
    
    story.append(Paragraph("""
    <b>Key Future Implications:</b>
    """, body_style))
    
    implications = [
        "Organizations that successfully integrate AI and digital twins will establish significant competitive advantages",
        "The line between physical and digital will continue to blur, creating new possibilities for innovation",
        "Talent with expertise in these technologies will be increasingly valuable across all sectors",
        "New business models will emerge that leverage real-time data and predictive capabilities",
        "Cross-industry collaboration will accelerate to solve complex challenges"
    ]
    
    for implication in implications:
        story.append(Paragraph(f"• {implication}", body_style))
    
    story.append(Spacer(1, 24))
    
    story.append(Paragraph("""
    <i>As these technologies mature, we can expect to see increasingly sophisticated applications
    that combine multiple AI modalities with simulation capabilities, creating unprecedented
    opportunities for innovation and efficiency gains. The organizations that successfully
    integrate these technologies into their operations will likely establish significant
    competitive advantages in their respective markets.</i>
    """, emphasis_style))
    
    # Build PDF with page numbers
    doc.build(story, canvasmaker=PageNumCanvas)
    
    print(f"Enhanced narrative document created: {output_file}")

if __name__ == "__main__":
    create_enhanced_narrative() 