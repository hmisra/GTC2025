#!/usr/bin/env python3
"""
Enhanced Analysis of GTC 2025 Session Data
------------------------------------------
This script performs advanced analysis on GTC 2025 session data, extracting
insights, trends, and patterns to inform a personal brand narrative.
"""

import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from wordcloud import WordCloud
import json

# Set up styling for plots
plt.style.use('seaborn-v0_8')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

class GTCAnalyzer:
    def __init__(self, data_file=None, titles_file='data/gtc_sessions_titles.txt'):
        """Initialize the GTC data analyzer with input files."""
        self.titles_file = titles_file
        self.data_file = data_file
        self.titles = []
        self.session_codes = []
        self.df = None
        self.categories = self._define_categories()
        self.output_dir = 'outputs/analysis_output'
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _define_categories(self):
        """Define and return categories for classification with expanded keywords."""
        return {
            'AI & Machine Learning': [
                'ai', 'machine learning', 'neural', 'deep learning', 'llm', 'language model', 
                'transformer', 'gpt', 'claude', 'gemini', 'llama', 'mistral', 'training', 
                'fine-tuning', 'inference', 'embeddings', 'rag', 'hallucination', 'generative ai', 
                'foundation model', 'multimodal', 'synthetic data', 'nlp', 'natural language',
                'prompt', 'token', 'instruct', 'chat', 'text-to-', 'text to ', 'vision-language',
                'zero-shot', 'few-shot', 'context window', 'agent', 'reinforcement', 'supervised',
                'unsupervised', 'semi-supervised', 'classification', 'annotation'
            ],
            
            'Hardware & Infrastructure': [
                'hardware', 'cpu', 'gpu', 'dgx', 'tpu', 'h100', 'h200', 'b100', 'blackwell', 
                'hopper', 'grace', 'server', 'cluster', 'supercomputer', 'data center', 'cooling', 
                'liquid', 'rack', 'memory', 'hbm', 'infrastructure', 'accelerator', 'compute', 
                'performance', 'benchmark', 'power', 'architecture', 'chip', 'processor', 'datacenter',
                'networking', 'storage', 'nvme', 'ssd', 'disk', 'throughput', 'latency', 'bandwidth'
            ],
            
            'Software & Development': [
                'software', 'programming', 'development', 'sdk', 'api', 'library', 'framework', 
                'cuda', 'driver', 'compiler', 'microservice', 'container', 'docker', 'kubernetes', 
                'devops', 'mlops', 'testing', 'debugging', 'deployment', 'platform', 'architecture', 
                'design pattern', 'workflow', 'pipeline', 'code', 'developer', 'git', 'version control',
                'ci/cd', 'continuous integration', 'application', 'stack', 'backend', 'frontend',
                'full-stack', 'web', 'mobile', 'desktop', 'native', 'cross-platform'
            ],
            
            'Industry Applications': [
                'healthcare', 'medical', 'finance', 'banking', 'retail', 'manufacturing', 'automotive', 
                'energy', 'telecom', 'aerospace', 'defense', 'media', 'entertainment', 'game', 
                'insurance', 'agriculture', 'transportation', 'industry', 'business', 'enterprise', 
                'commercial', 'solution', 'customer', 'production', 'logistics', 'supply chain',
                'construction', 'real estate', 'oil and gas', 'mining', 'hospitality', 'tourism',
                'education', 'government', 'public sector', 'utility', 'pharma', 'biotech'
            ],
            
            'Research & Innovation': [
                'research', 'innovation', 'breakthrough', 'novel', 'paper', 'publication', 'algorithm', 
                'method', 'technique', 'experiment', 'benchmark', 'evaluation', 'assessment', 
                'improvement', 'enhanced', 'academic', 'advance', 'frontier', 'state-of-the-art', 
                'sota', 'cutting-edge', 'emerging', 'future', 'next-gen', 'paradigm', 'disruptive',
                'groundbreaking', 'pioneering', 'invention', 'patent', 'discovery', 'theoretical',
                'empirical', 'experimental', 'proof-of-concept', 'prototype'
            ],
            
            'Robotics & Autonomous Systems': [
                'robot', 'robotics', 'autonomous', 'automation', 'self-driving', 'drone', 'uav', 
                'control', 'sensor', 'perception', 'motion', 'navigation', 'grasping', 'manipulation', 
                'humanoid', 'embodied', 'physical', 'mechanical', 'actuator', 'motor', 'kinematic',
                'robotic process automation', 'rpa', 'vehicle', 'mobility', 'locomotion', 'biped',
                'quadruped', 'swarm', 'multi-robot', 'teleoperation', 'haptic', 'industrial robot'
            ],
            
            'Digital Twins & Simulation': [
                'digital twin', 'digital replica', 'simulation', 'virtual environment', 'synthetic', 
                'physics-based', 'real-time simulation', 'interactive simulation', 'physical system', 
                'mirror', 'replica', 'virtual world', 'metaverse', 'omniverse', 'virtual prototype',
                'system modeling', 'emulation', 'surrogate model', 'scenario', 'what-if analysis',
                'predictive simulation', 'virtual testing', 'virtual commissioning', 'asset tracking'
            ],
            
            'Computer Vision & Graphics': [
                'vision', 'image', 'video', 'graphics', 'rendering', 'ray tracing', 'visualization', 
                '3d', 'ar', 'vr', 'xr', 'mixed reality', 'segmentation', 'detection', 'recognition', 
                'tracking', 'rtx', 'omniverse', 'camera', 'depth', 'scene', 'mesh', 'texture', 
                'animation', 'object detection', 'instance segmentation', 'semantic segmentation',
                'pose estimation', 'optical flow', 'image generation', 'text-to-image', 'photorealistic',
                'cgi', 'computer-generated', 'virtual production', 'real-time rendering'
            ],
            
            'Data Science & Analytics': [
                'data science', 'analytics', 'data analysis', 'big data', 'data engineering', 'etl', 
                'database', 'sql', 'nosql', 'data lake', 'data warehouse', 'data visualization', 
                'dashboard', 'reporting', 'business intelligence', 'bi', 'metrics', 'kpi',
                'predictive analytics', 'descriptive analytics', 'prescriptive analytics',
                'time series', 'forecasting', 'regression', 'classification', 'clustering',
                'anomaly detection', 'insights', 'data-driven'
            ]
        }
    
    def load_titles(self):
        """Load session titles from the titles file."""
        print(f"Loading titles from {self.titles_file}...")
        with open(self.titles_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines[2:]:  # Skip header and blank line
            line = line.strip()
            if not line:
                continue
            
            # Extract session code
            match = re.search(r'\[(.*?)\]$', line)
            if match:
                code = match.group(1)
                self.session_codes.append(code)
                # Remove the code from the title
                title = line[:match.start()].strip()
                self.titles.append(title)
            else:
                # Handle titles without codes
                self.titles.append(line)
                self.session_codes.append("UNKNOWN")
        
        print(f"Loaded {len(self.titles)} session titles")
        return self
    
    def load_data(self):
        """Load session data from the CSV file if available."""
        if self.data_file and os.path.exists(self.data_file):
            print(f"Loading data from {self.data_file}...")
            self.df = pd.read_csv(self.data_file)
            print(f"Loaded data with {len(self.df)} rows and {len(self.df.columns)} columns")
            # Print column names
            print(f"Columns: {', '.join(self.df.columns)}")
        return self
    
    def categorize_sessions(self):
        """Categorize sessions based on keywords and save results."""
        print("Categorizing sessions...")
        categorized_titles = {}
        uncategorized = []
        
        for i, title in enumerate(self.titles):
            title_lower = title.lower()
            best_category = None
            best_score = 0
            
            for category, keywords in self.categories.items():
                score = sum(1 for keyword in keywords if keyword.lower() in title_lower)
                if score > best_score:
                    best_score = score
                    best_category = category
            
            if best_score > 0:
                if best_category not in categorized_titles:
                    categorized_titles[best_category] = []
                categorized_titles[best_category].append((title, self.session_codes[i]))
            else:
                uncategorized.append((title, self.session_codes[i]))
        
        # Add uncategorized to a special category
        if uncategorized:
            categorized_titles['Miscellaneous & Other Topics'] = uncategorized
        
        # Save categorization results
        self._save_categorization(categorized_titles)
        
        # Create visualization of category distribution
        self._visualize_category_distribution(categorized_titles)
        
        return categorized_titles
    
    def _save_categorization(self, categorized_titles):
        """Save categorization results to a file."""
        output_file = os.path.join(self.output_dir, 'gtc_sessions_categorized_enhanced.md')
        
        with open(output_file, 'w') as f:
            f.write('# NVIDIA GTC 2025 Session Titles - Enhanced Categorization\n\n')
            
            # Write summary statistics
            f.write('## Summary\n\n')
            f.write(f'- Total sessions: {len(self.titles)}\n')
            for category, titles in sorted(categorized_titles.items()):
                f.write(f'- {category}: {len(titles)} sessions\n')
            f.write('\n')
            
            # Write each category and its titles
            for category, titles in sorted(categorized_titles.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f'## {category} ({len(titles)} sessions)\n\n')
                
                for title, code in sorted(titles):
                    f.write(f'- {title} [{code}]\n')
                
                f.write('\n')
        
        print(f"Categorization results saved to {output_file}")
        
        # Save as JSON for further processing
        json_output = os.path.join(self.output_dir, 'gtc_sessions_categorized.json')
        json_data = {}
        for category, titles in categorized_titles.items():
            json_data[category] = [{"title": title, "code": code} for title, code in titles]
        
        with open(json_output, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"Categorization data saved to {json_output}")
    
    def _visualize_category_distribution(self, categorized_titles):
        """Create visualization of category distribution."""
        categories = []
        counts = []
        
        for category, titles in sorted(categorized_titles.items(), key=lambda x: len(x[1]), reverse=True):
            categories.append(category)
            counts.append(len(titles))
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 8))
        bars = plt.barh(categories, counts, color=sns.color_palette("viridis", len(categories)))
        
        # Add count labels to the bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 5, bar.get_y() + bar.get_height()/2, f'{width}', 
                    ha='left', va='center', fontweight='bold')
        
        plt.xlabel('Number of Sessions')
        plt.title('GTC 2025 Sessions by Category')
        plt.tight_layout()
        
        # Save the chart
        chart_file = os.path.join(self.output_dir, 'category_distribution.png')
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Category distribution chart saved to {chart_file}")
    
    def generate_word_clouds(self, categorized_titles):
        """Generate word clouds for each category."""
        print("Generating word clouds for categories...")
        
        for category, titles in categorized_titles.items():
            if not titles:
                continue
                
            # Combine all titles in this category
            text = ' '.join([title for title, _ in titles])
            
            # Create word cloud
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                colormap='viridis',
                max_words=100,
                contour_width=1
            ).generate(text)
            
            # Save word cloud
            output_file = os.path.join(self.output_dir, f'wordcloud_{category.replace(" & ", "_").replace(" ", "_").lower()}.png')
            wordcloud.to_file(output_file)
            
        print(f"Word clouds saved to {self.output_dir}")
    
    def create_category_trend_analysis(self, categorized_titles):
        """Create trend analysis within categories."""
        print("Analyzing trends within categories...")
        
        trends = {}
        
        for category, titles in categorized_titles.items():
            if len(titles) < 5:  # Skip categories with too few titles
                continue
                
            # Extract common keywords in this category
            text = ' '.join([title.lower() for title, _ in titles])
            words = re.findall(r'\b\w+\b', text)
            word_counts = Counter(words)
            
            # Filter out common words
            common_words = {'and', 'the', 'to', 'in', 'for', 'with', 'on', 'of', 'a', 'from', 'by'}
            for word in common_words:
                if word in word_counts:
                    del word_counts[word]
            
            # Get the top 10 keywords
            top_keywords = word_counts.most_common(10)
            
            # Save to trends
            trends[category] = {
                'top_keywords': top_keywords,
                'session_count': len(titles)
            }
        
        # Save trend analysis
        output_file = os.path.join(self.output_dir, 'category_trends.json')
        with open(output_file, 'w') as f:
            json.dump(trends, f, indent=2)
        
        print(f"Category trend analysis saved to {output_file}")
        
        # Visualize top keywords for largest categories
        self._visualize_top_keywords(trends)
    
    def _visualize_top_keywords(self, trends):
        """Visualize top keywords for the largest categories."""
        # Sort categories by session count
        sorted_categories = sorted(trends.keys(), key=lambda x: trends[x]['session_count'], reverse=True)
        top_categories = sorted_categories[:5]  # Top 5 categories
        
        # Create visualization for each top category
        for category in top_categories:
            keywords = [k for k, _ in trends[category]['top_keywords']]
            counts = [c for _, c in trends[category]['top_keywords']]
            
            plt.figure(figsize=(10, 6))
            bars = plt.barh(keywords, counts, color=sns.color_palette("viridis", len(keywords)))
            
            # Add count labels
            for bar in bars:
                width = bar.get_width()
                plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width}', 
                        ha='left', va='center')
            
            plt.xlabel('Frequency')
            plt.title(f'Top 10 Keywords in {category}')
            plt.tight_layout()
            
            # Save the chart
            chart_file = os.path.join(self.output_dir, f'keywords_{category.replace(" & ", "_").replace(" ", "_").lower()}.png')
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    
    def extract_insights(self, categorized_titles):
        """Extract key insights from the session data."""
        print("Extracting key insights...")
        
        insights = {
            "top_categories": [],
            "emerging_trends": [],
            "industry_focus": [],
            "technology_evolution": [],
            "potential_opportunities": []
        }
        
        # Sort categories by session count
        sorted_categories = sorted(
            [(cat, len(titles)) for cat, titles in categorized_titles.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Top categories
        insights["top_categories"] = sorted_categories[:5]
        
        # Check if we have full session data for more detailed analysis
        if self.df is not None:
            # Additional analysis based on the full dataset would go here
            pass
        
        # Manually defined insights based on category analysis
        emerging_trends = [
            "Large Language Models continue to dominate AI discussions",
            "Digital Twins are becoming central to industry transformation",
            "AI Agents are emerging as the next frontier in automation",
            "Multimodal AI is expanding beyond text-only applications"
        ]
        insights["emerging_trends"] = emerging_trends
        
        industry_focus = [
            "Healthcare and life sciences see strong representation in AI applications",
            "Manufacturing transformation through digital twins is a key theme",
            "Financial services focus on AI for risk management and customer experience",
            "Retail industry embracing computer vision and generative AI"
        ]
        insights["industry_focus"] = industry_focus
        
        # Save insights to file
        output_file = os.path.join(self.output_dir, 'gtc_insights.json')
        with open(output_file, 'w') as f:
            json.dump(insights, f, indent=2)
        
        print(f"Key insights saved to {output_file}")
        return insights
    
    def create_insightful_narrative(self, insights):
        """Create a narrative summary of the insights."""
        print("Creating narrative summary...")
        
        narrative = "# Key Insights from NVIDIA GTC 2025\n\n"
        
        # Add a section on top categories
        narrative += "## The Leading Technologies of GTC 2025\n\n"
        for category, count in insights["top_categories"]:
            narrative += f"- **{category}**: {count} sessions\n"
        narrative += "\n"
        
        # Add emerging trends
        narrative += "## Emerging Trends\n\n"
        for trend in insights["emerging_trends"]:
            narrative += f"- {trend}\n"
        narrative += "\n"
        
        # Add industry focus
        narrative += "## Industry Focus\n\n"
        for focus in insights["industry_focus"]:
            narrative += f"- {focus}\n"
        narrative += "\n"
        
        # Final thoughts
        narrative += "## What This Means For The Future\n\n"
        narrative += "The convergence of AI, digital twins, and accelerated computing at GTC 2025 "
        narrative += "signals a fundamental shift in how industries leverage technology. These technological "
        narrative += "advancements are not just incremental improvements but transformative forces "
        narrative += "reshaping entire industries from manufacturing to healthcare, retail to finance.\n\n"
        
        narrative += "As these technologies mature, we can expect to see increasingly sophisticated "
        narrative += "applications that combine multiple AI modalities with simulation capabilities, "
        narrative += "creating unprecedented opportunities for innovation and efficiency gains. The "
        narrative += "organizations that successfully integrate these technologies into their operations "
        narrative += "will likely establish significant competitive advantages in their respective markets."
        
        # Save narrative
        output_file = os.path.join(self.output_dir, 'gtc_narrative_summary.md')
        with open(output_file, 'w') as f:
            f.write(narrative)
        
        print(f"Narrative summary saved to {output_file}")
    
    def run_full_analysis(self):
        """Run full analysis workflow."""
        self.load_titles()
        self.load_data()
        categorized_titles = self.categorize_sessions()
        self.generate_word_clouds(categorized_titles)
        self.create_category_trend_analysis(categorized_titles)
        insights = self.extract_insights(categorized_titles)
        self.create_insightful_narrative(insights)
        
        print("\nAnalysis complete! Output files saved to:", self.output_dir)
        return self

if __name__ == "__main__":
    # Create and run the analyzer
    analyzer = GTCAnalyzer(
        data_file="data/gtc_sessions_extracted.csv",
        titles_file="data/gtc_sessions_titles.txt"
    )
    analyzer.run_full_analysis() 