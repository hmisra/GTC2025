#!/usr/bin/env python3
"""
GTC 2025 Personal Brand Marketing Package Generator
--------------------------------------------------
This script creates a comprehensive marketing package for personal branding
based on insights from GTC 2025.
"""

import os
import json
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF

# Define colors for personal brand
PRIMARY_COLOR = colors.HexColor('#1E88E5')  # Blue
SECONDARY_COLOR = colors.HexColor('#43A047')  # Green
ACCENT_COLOR = colors.HexColor('#FF5722')  # Orange
DARK_GRAY = colors.HexColor('#333333')
LIGHT_GRAY = colors.HexColor('#F5F5F5')

class MarketingPackageGenerator:
    """Class to generate a marketing package based on GTC insights."""
    
    def __init__(self):
        self.output_dir = "outputs/marketing_package"
        self.analysis_dir = "outputs/analysis_output"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Load insights data
        insights_path = os.path.join(self.analysis_dir, "gtc_insights.json")
        if os.path.exists(insights_path):
            with open(insights_path, "r") as f:
                self.insights = json.load(f)
        else:
            self.insights = {
                "top_categories": [
                    ["AI & Machine Learning", 624],
                    ["Hardware & Infrastructure", 155],
                    ["Software & Development", 100],
                    ["Computer Vision & Graphics", 56],
                    ["Miscellaneous & Other Topics", 56]
                ],
                "emerging_trends": [
                    "Large Language Models continue to dominate AI discussions",
                    "Digital Twins are becoming central to industry transformation",
                    "AI Agents are emerging as the next frontier in automation",
                    "Multimodal AI is expanding beyond text-only applications"
                ],
                "industry_focus": [
                    "Healthcare and life sciences see strong representation in AI applications",
                    "Manufacturing transformation through digital twins is a key theme",
                    "Financial services focus on AI for risk management and customer experience",
                    "Retail industry embracing computer vision and generative AI"
                ]
            }
    
    def create_one_pager(self):
        """Create a one-page executive summary for personal branding."""
        output_file = os.path.join(self.output_dir, "GTC_2025_Executive_Insights.pdf")
        
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
            fontSize=24,
            spaceAfter=16,
            textColor=PRIMARY_COLOR,
            alignment=1  # Center alignment
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=DARK_GRAY,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=PRIMARY_COLOR
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leading=14
        )
        
        highlight_style = ParagraphStyle(
            'Highlight',
            parent=body_style,
            fontName='Helvetica-Bold',
            textColor=SECONDARY_COLOR
        )
        
        # Story elements
        story = []
        
        # Header with personal brand
        story.append(Paragraph("GTC 2025: Key Insights & Trends", title_style))
        story.append(Paragraph("A Technology Leadership Perspective", subtitle_style))
        story.append(Spacer(1, 10))
        
        # Introduction
        story.append(Paragraph("""
        As a technology leader focused on emerging technologies, I attended NVIDIA's 
        GTC 2025 to identify key trends and opportunities that will shape the future 
        of AI, digital twins, and accelerated computing. This executive summary highlights 
        the most significant insights from my analysis of over 1300 conference sessions.
        """, body_style))
        
        # Create horizontal bar chart for top categories
        drawing = Drawing(400, 150)
        data = [
            [cat[1] for cat in self.insights["top_categories"][:5]]
        ]
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 10
        bc.height = 115
        bc.width = 300
        bc.data = data
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max([cat[1] for cat in self.insights["top_categories"]]) + 50
        bc.valueAxis.gridStrokeColor = LIGHT_GRAY
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = -8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = [cat[0].replace(' & ', '\n') for cat in self.insights["top_categories"][:5]]
        bc.bars[0].fillColor = PRIMARY_COLOR
        
        drawing.add(bc)
        story.append(drawing)
        story.append(Spacer(1, 10))
        
        # Key insights in two columns
        story.append(Paragraph("Key Insights & Strategic Implications", heading_style))
        
        # Create two-column layout using a table
        left_col = []
        right_col = []
        
        # Left column: Emerging Trends
        left_col.append(Paragraph("<b>Emerging Trends</b>", highlight_style))
        for trend in self.insights["emerging_trends"]:
            left_col.append(Paragraph(f"• {trend}", body_style))
        
        # Right column: Industry Focus
        right_col.append(Paragraph("<b>Industry Applications</b>", highlight_style))
        for focus in self.insights["industry_focus"]:
            right_col.append(Paragraph(f"• {focus}", body_style))
        
        # Ensure both columns have the same number of items
        max_len = max(len(left_col), len(right_col))
        while len(left_col) < max_len:
            left_col.append(Paragraph("", body_style))
        while len(right_col) < max_len:
            right_col.append(Paragraph("", body_style))
        
        # Create a table for two-column layout
        col_data = []
        for i in range(max_len):
            col_data.append([left_col[i], right_col[i]])
        
        col_table = Table(col_data, colWidths=[3.25*inch, 3.25*inch])
        col_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('RIGHTPADDING', (0, 0), (0, -1), 10),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
        ]))
        
        story.append(col_table)
        story.append(Spacer(1, 10))
        
        # Strategic Recommendations
        story.append(Paragraph("Strategic Recommendations", heading_style))
        
        recommendations = [
            "Prioritize investments in AI and Machine Learning, especially Large Language Models and multimodal applications",
            "Explore Digital Twin applications for operational efficiency and predictive maintenance",
            "Develop talent strategies to address the growing need for AI expertise across all business functions",
            "Establish cross-functional teams to identify and implement AI-powered transformation opportunities",
            "Partner with technology providers to accelerate adoption of accelerated computing infrastructure"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", body_style))
        
        story.append(Spacer(1, 20))
        
        # Contact Information
        story.append(Paragraph("For more insights or to discuss these trends in detail:", body_style))
        story.append(Paragraph("Your Name | your.email@example.com | linkedin.com/in/yourprofile", body_style))
        
        # Build PDF
        doc.build(story)
        print(f"Created one-page executive summary: {output_file}")
    
    def create_social_media_content(self):
        """Create social media content based on GTC insights."""
        output_file = os.path.join(self.output_dir, "Social_Media_Content_Guide.pdf")
        
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
            fontSize=24,
            spaceAfter=16,
            textColor=PRIMARY_COLOR,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=12,
            spaceAfter=8,
            textColor=PRIMARY_COLOR
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=14,
            spaceBefore=8,
            spaceAfter=6,
            textColor=SECONDARY_COLOR
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leading=14
        )
        
        # Story elements
        story = []
        
        # Title
        story.append(Paragraph("GTC 2025 Social Media Content Guide", title_style))
        story.append(Spacer(1, 16))
        
        # Introduction
        story.append(Paragraph("Introduction", heading_style))
        story.append(Paragraph("""
        This guide provides templates and content ideas for sharing your GTC 2025 insights 
        across social media platforms. Position yourself as a thought leader by highlighting 
        key trends and their implications for industry transformation.
        """, body_style))
        
        # LinkedIn Posts
        story.append(Paragraph("LinkedIn Post Templates", heading_style))
        
        # Post 1: Overall Conference Summary
        story.append(Paragraph("Post 1: Overall Conference Summary", subheading_style))
        story.append(Paragraph("""
        <b>Just returned from #NVIDIGTC 2025</b> where the convergence of AI, digital twins, and 
        accelerated computing was on full display across 1300+ sessions. Here are my top 3 takeaways:
        
        1️⃣ <b>AI Evolution:</b> Large Language Models are evolving beyond text to become multimodal, 
        with applications spanning industries from healthcare to manufacturing
        
        2️⃣ <b>Digital Transformation:</b> Digital twins are revolutionizing how organizations design, 
        optimize, and maintain physical systems
        
        3️⃣ <b>Industry Impact:</b> The most compelling use cases combined AI with industry-specific 
        knowledge to solve previously intractable problems
        
        What technologies from GTC 2025 are you most excited about implementing?
        
        #AI #DigitalTwins #MachineLearning #TechTrends #DataScience
        """, body_style))
        
        # Post 2: Industry-Specific Insights
        story.append(Paragraph("Post 2: Industry-Specific Insights", subheading_style))
        story.append(Paragraph("""
        <b>Industry Transformation at #NVIDIGTC 2025</b>
        
        The conference revealed how specific industries are being revolutionized by AI and digital twins:
        
        🏥 <b>Healthcare:</b> AI models are improving diagnostics, drug discovery, and personalized medicine
        
        🏭 <b>Manufacturing:</b> Digital twins are reducing downtime by 45% through predictive maintenance
        
        💰 <b>Financial Services:</b> LLMs are transforming risk assessment and customer experience
        
        🛒 <b>Retail:</b> Computer vision and generative AI are creating new customer engagement opportunities
        
        Which industry do you think will see the biggest transformation from these technologies in the next year?
        
        #IndustryTransformation #AIinHealthcare #DigitalManufacturing #FinTech #RetailTech
        """, body_style))
        
        # Post 3: Technology Deep Dive
        story.append(Paragraph("Post 3: Technology Deep Dive", subheading_style))
        story.append(Paragraph("""
        <b>The Rise of AI Agents: My #NVIDIGTC 2025 Deep Dive</b>
        
        One of the most fascinating trends at GTC was the emergence of autonomous AI agents that can:
        
        📊 Process and analyze data from multiple sources
        🔄 Perform complex, multi-step tasks with minimal human intervention
        🔗 Coordinate with other agents to solve problems collaboratively
        🧠 Learn from their experiences and continuously improve
        
        The implications for business processes and decision-making are profound. We're moving from AI as a tool to AI as a teammate.
        
        What are your thoughts on the potential of AI agents? Opportunity or challenge?
        
        #AIAgents #FutureOfWork #BusinessTransformation #EmergingTech
        """, body_style))
        
        # Twitter Posts
        story.append(PageBreak())
        story.append(Paragraph("Twitter Post Templates", heading_style))
        
        twitter_posts = [
            """<b>My top insight from #NVIDIGTC 2025:</b> Digital twins aren't just simulations anymore—they're becoming the central operating system for industries from manufacturing to healthcare, enabling real-time optimization and predictive capabilities. #DigitalTransformation""",
            
            """Just wrapped up #NVIDIGTC 2025! The 600+ AI sessions made one thing clear: We're moving beyond foundation models to multimodal AI that combines text, vision, audio, and simulation for unprecedented capabilities. #AITrends #MachineLearning""",
            
            """#NVIDIGTC 2025 Insight: The line between physical and digital continues to blur, with digital twins showing 30% operational efficiency improvements in manufacturing. This is no longer experimental—it's mainstream. #DigitalTwins #IndustryTransformation""",
            
            """The most surprising trend at #NVIDIGTC 2025? The rise of AI agents that can autonomously coordinate to solve complex problems. We're moving from AI as a tool to AI as a teammate. #AIAgents #FutureOfWork"""
        ]
        
        for i, post in enumerate(twitter_posts, 1):
            story.append(Paragraph(f"Tweet {i}:", subheading_style))
            story.append(Paragraph(post, body_style))
            story.append(Spacer(1, 10))
        
        # Content Calendar
        story.append(PageBreak())
        story.append(Paragraph("Two-Week Content Calendar", heading_style))
        story.append(Paragraph("""
        To maximize engagement and position yourself as a thought leader, spread your GTC 2025 
        insights across platforms over a two-week period using this suggested calendar:
        """, body_style))
        
        calendar_data = [
            ["Week", "Day", "Platform", "Content"],
            ["Week 1", "Monday", "LinkedIn", "Post 1: Overall Conference Summary"],
            ["", "Wednesday", "Twitter", "Tweet 1: Digital Twins Insight"],
            ["", "Friday", "LinkedIn", "Share relevant session recording with your commentary"],
            ["Week 2", "Monday", "Twitter", "Tweet 3: AI Agents Insight"],
            ["", "Wednesday", "LinkedIn", "Post 2: Industry-Specific Insights"],
            ["", "Friday", "LinkedIn", "Post 3: Technology Deep Dive + One-page executive summary"]
        ]
        
        calendar_table = Table(calendar_data, colWidths=[0.75*inch, 0.9*inch, 1*inch, 3.75*inch])
        calendar_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (0, 3), LIGHT_GRAY),
            ('BACKGROUND', (0, 4), (0, 6), LIGHT_GRAY),
            ('SPAN', (0, 1), (0, 3)),
            ('SPAN', (0, 4), (0, 6)),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        story.append(calendar_table)
        
        # Visual Elements
        story.append(PageBreak())
        story.append(Paragraph("Visual Elements for Social Media", heading_style))
        story.append(Paragraph("""
        Enhance your social media posts with these visual element suggestions to increase engagement:
        """, body_style))
        
        visual_elements = [
            ["Element", "Description", "Usage"],
            ["Charts & Graphs", "Share the category distribution chart from your analysis", "LinkedIn posts about key trends"],
            ["Word Clouds", "Use word clouds to highlight key topics from specific categories", "Twitter to showcase technology clusters"],
            ["Quote Cards", "Create branded quote cards with key insights", "LinkedIn and Twitter for shareable content"],
            ["Session Screenshots", "Share screenshots from particularly insightful sessions", "All platforms to add credibility"],
            ["One-page summary", "Share your executive summary as a downloadable PDF", "LinkedIn to provide additional value"]
        ]
        
        visuals_table = Table(visual_elements, colWidths=[1.5*inch, 3*inch, 1.9*inch])
        visuals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        
        story.append(visuals_table)
        story.append(Spacer(1, 20))
        
        # Final tips
        story.append(Paragraph("Best Practices", heading_style))
        
        tips = [
            "Tag relevant companies and speakers in your posts to increase visibility",
            "Use the official conference hashtag #NVIDIGTC in all posts",
            "Respond to comments to foster engagement and build relationships",
            "Track which posts perform best and adapt your strategy accordingly",
            "Connect with other attendees who are sharing similar insights"
        ]
        
        for tip in tips:
            story.append(Paragraph(f"• {tip}", body_style))
        
        # Build PDF
        doc.build(story)
        print(f"Created social media content guide: {output_file}")
    
    def create_presentation_template(self):
        """Create a presentation template for sharing GTC insights."""
        output_file = os.path.join(self.output_dir, "GTC_2025_Presentation_Template.pdf")
        
        # Create PDF document in landscape orientation
        doc = SimpleDocTemplate(
            output_file,
            pagesize=landscape(letter),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=12,
            textColor=PRIMARY_COLOR,
            alignment=1  # Center alignment
        )
        
        slide_title_style = ParagraphStyle(
            'SlideTitle',
            parent=styles['Heading2'],
            fontSize=24,
            spaceAfter=12,
            textColor=PRIMARY_COLOR
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=20,
            spaceBefore=10,
            spaceAfter=8,
            textColor=DARK_GRAY
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=10,
            leading=20
        )
        
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=styles['Italic'],
            fontSize=10,
            textColor=DARK_GRAY,
            alignment=0
        )
        
        # Story elements
        story = []
        
        # Title Slide
        story.append(Paragraph("NVIDIA GTC 2025", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Key Insights & Industry Implications", subheading_style))
        story.append(Spacer(1, 100))
        story.append(Paragraph("Presented by: [Your Name]", body_style))
        story.append(Paragraph("[Your Title/Company]", body_style))
        story.append(Paragraph("April 2025", body_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("[Note: This is a slide template. Replace with your details.]", note_style))
        story.append(PageBreak())
        
        # Agenda Slide
        story.append(Paragraph("Agenda", slide_title_style))
        story.append(Spacer(1, 20))
        
        agenda_items = [
            "GTC 2025 Overview",
            "Key Technology Trends",
            "Industry Applications & Use Cases",
            "Strategic Implications",
            "Recommended Next Steps",
            "Q&A"
        ]
        
        for item in agenda_items:
            story.append(Paragraph(f"• {item}", body_style))
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Customize the agenda based on your audience and presentation focus.]", note_style))
        story.append(PageBreak())
        
        # Conference Overview Slide
        story.append(Paragraph("GTC 2025 Overview", slide_title_style))
        story.append(Spacer(1, 20))
        
        overview_points = [
            "NVIDIA's annual GPU Technology Conference",
            "1300+ sessions across multiple technology domains",
            "Focus areas: AI/ML, accelerated computing, digital twins",
            "Sessions from industry leaders, researchers, and developers",
            "Showcasing state-of-the-art technology applications"
        ]
        
        for point in overview_points:
            story.append(Paragraph(f"• {point}", body_style))
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Add specific numbers and notable speakers as appropriate.]", note_style))
        story.append(PageBreak())
        
        # Key Trends Slide
        story.append(Paragraph("Key Technology Trends", slide_title_style))
        story.append(Spacer(1, 20))
        
        # Create a table for presenting trends
        trends_data = [
            ["Technology Area", "Key Trends"],
            ["AI & Machine Learning", "LLMs evolving beyond text to multimodal applications"],
            ["", "AI agents emerging as the next frontier in automation"],
            ["Digital Twins", "Moving from simulation to real-time operational systems"],
            ["", "Enabling predictive maintenance and optimization"],
            ["Hardware", "Next-gen GPUs bringing significant performance improvements"],
            ["", "Infrastructure designed specifically for AI workloads"]
        ]
        
        trends_table = Table(trends_data, colWidths=[3*inch, 6*inch])
        trends_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 18),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('SPAN', (0, 1), (0, 2)),
            ('SPAN', (0, 3), (0, 4)),
            ('SPAN', (0, 5), (0, 6)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 16)
        ]))
        
        story.append(trends_table)
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Customize the trends based on your industry focus.]", note_style))
        story.append(PageBreak())
        
        # Industry Applications Slide
        story.append(Paragraph("Industry Applications & Use Cases", slide_title_style))
        story.append(Spacer(1, 10))
        
        # Create a two-column layout for industry applications
        industry_data = [
            ["Industry", "Use Cases", "Impact"],
            ["Healthcare", "AI-driven diagnostics, drug discovery", "Faster treatments, reduced costs"],
            ["Manufacturing", "Digital twins for production lines", "45% reduction in downtime"],
            ["Financial Services", "LLMs for risk assessment", "Improved accuracy, reduced fraud"],
            ["Retail", "Computer vision, generative AI", "Enhanced customer experiences"]
        ]
        
        industry_table = Table(industry_data, colWidths=[2*inch, 3.5*inch, 3.5*inch])
        industry_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 18),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 16)
        ]))
        
        story.append(industry_table)
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Focus on the industries most relevant to your audience.]", note_style))
        story.append(PageBreak())
        
        # Strategic Implications Slide
        story.append(Paragraph("Strategic Implications", slide_title_style))
        story.append(Spacer(1, 20))
        
        implications = [
            "AI is transitioning from experimental to mission-critical",
            "Organizations must develop AI literacy across all functions",
            "Digital twins offer unprecedented operational visibility",
            "Technology integration capabilities are becoming a key differentiator",
            "Cross-industry collaboration is accelerating innovation"
        ]
        
        for implication in implications:
            story.append(Paragraph(f"• {implication}", body_style))
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Tailor implications to your organization's specific context.]", note_style))
        story.append(PageBreak())
        
        # Recommended Next Steps Slide
        story.append(Paragraph("Recommended Next Steps", slide_title_style))
        story.append(Spacer(1, 20))
        
        next_steps = [
            "Evaluate current AI and digital twin capabilities",
            "Identify high-impact use cases for immediate implementation",
            "Develop a talent strategy to build necessary expertise",
            "Create cross-functional teams to drive technology adoption",
            "Establish partnerships with technology providers"
        ]
        
        for step in next_steps:
            story.append(Paragraph(f"• {step}", body_style))
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("[Note: Customize these steps based on your organization's maturity and goals.]", note_style))
        story.append(PageBreak())
        
        # Questions Slide
        story.append(Paragraph("Questions & Discussion", slide_title_style))
        story.append(Spacer(1, 100))
        
        story.append(Paragraph("Thank you!", body_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("[Your Name]", body_style))
        story.append(Paragraph("[Your Email]", body_style))
        story.append(Paragraph("[Your LinkedIn/Social Media]", body_style))
        
        # Build PDF
        doc.build(story)
        print(f"Created presentation template: {output_file}")
    
    def copy_visualization_assets(self):
        """Copy relevant visualization assets to the marketing package directory."""
        key_assets = [
            "category_distribution.png",
            "wordcloud_ai_machine_learning.png",
            "wordcloud_digital_twins_simulation.png",
            "wordcloud_industry_applications.png",
            "keywords_ai_machine_learning.png"
        ]
        
        # Create visualizations directory
        vis_dir = os.path.join(self.output_dir, "visualizations")
        if not os.path.exists(vis_dir):
            os.makedirs(vis_dir)
        
        # Copy assets
        for asset in key_assets:
            src_path = os.path.join(self.analysis_dir, asset)
            if os.path.exists(src_path):
                dst_path = os.path.join(vis_dir, asset)
                shutil.copy2(src_path, dst_path)
                print(f"Copied {asset} to marketing package")
    
    def create_full_package(self):
        """Create the complete marketing package."""
        print("Generating GTC 2025 Personal Brand Marketing Package...")
        
        self.create_one_pager()
        self.create_social_media_content()
        self.create_presentation_template()
        self.copy_visualization_assets()
        
        # Create a README file for the package
        readme_path = os.path.join(self.output_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write("""# GTC 2025 Personal Brand Marketing Package

This package contains materials to help you leverage your GTC 2025 insights for personal branding and thought leadership:

## Contents

1. **GTC_2025_Executive_Insights.pdf** - A one-page executive summary highlighting key insights and trends from GTC 2025.

2. **Social_Media_Content_Guide.pdf** - Templates and strategies for sharing your insights across LinkedIn, Twitter, and other platforms.

3. **GTC_2025_Presentation_Template.pdf** - A presentation template for sharing insights with your organization or at industry events.

4. **Visualizations/** - Key visual assets to use in your content creation, including charts, graphs, and word clouds.

## How to Use This Package

- Customize the executive summary with your contact information and specific expertise
- Use the social media templates as a starting point, adding your personal perspective
- Adapt the presentation template for your specific audience and industry focus
- Incorporate the visualizations into your content for greater engagement

## Contact Information

To update any of these materials or for further insights from GTC 2025, please contact:

[Your Name]
[Your Email]
[Your LinkedIn/Social Media]
""")
        
        print(f"\nMarketing package created successfully in the '{self.output_dir}' directory.")

if __name__ == "__main__":
    generator = MarketingPackageGenerator()
    generator.create_full_package() 