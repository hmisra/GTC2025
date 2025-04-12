#!/usr/bin/env python3
import re
import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Read titles, skipping the header lines
with open('gtc_sessions_titles.txt', 'r') as f:
    lines = f.readlines()

titles = []
session_codes = []
for line in lines[2:]:  # Skip header and blank line
    line = line.strip()
    if not line:
        continue
    
    # Extract session code
    match = re.search(r'\[(.*?)\]$', line)
    if match:
        code = match.group(1)
        session_codes.append(code)
        # Remove the code from the title
        title = line[:match.start()].strip()
        titles.append(title)

print(f"Found {len(titles)} titles to categorize")

# Define major categories and their keywords
categories = {
    'AI & Machine Learning': ['ai', 'machine learning', 'neural', 'deep learning', 'llm', 'language model', 'transformer', 'gpt', 'claude', 'gemini', 'llama', 'mistral', 'training', 'fine-tuning', 'inference', 'embeddings', 'rag', 'hallucination', 'generative ai', 'foundation model', 'multimodal', 'synthetic data', 'nlp', 'natural language'],
    
    'Hardware & Infrastructure': ['hardware', 'cpu', 'gpu', 'dgx', 'tpu', 'h100', 'h200', 'b100', 'blackwell', 'hopper', 'grace', 'server', 'cluster', 'supercomputer', 'data center', 'cooling', 'liquid', 'rack', 'memory', 'hbm', 'infrastructure', 'accelerator', 'compute', 'performance', 'benchmark', 'power'],
    
    'Software & Development': ['software', 'programming', 'development', 'sdk', 'api', 'library', 'framework', 'cuda', 'driver', 'compiler', 'microservice', 'container', 'docker', 'kubernetes', 'devops', 'mlops', 'testing', 'debugging', 'deployment', 'platform', 'architecture', 'design pattern', 'workflow', 'pipeline', 'code', 'developer'],
    
    'Industry Applications': ['healthcare', 'medical', 'finance', 'banking', 'retail', 'manufacturing', 'automotive', 'energy', 'telecom', 'aerospace', 'defense', 'media', 'entertainment', 'game', 'insurance', 'agriculture', 'transportation', 'industry', 'business', 'enterprise', 'commercial', 'solution', 'customer', 'production'],
    
    'Research & Innovation': ['research', 'innovation', 'breakthrough', 'novel', 'paper', 'publication', 'algorithm', 'method', 'technique', 'experiment', 'benchmark', 'evaluation', 'assessment', 'improvement', 'enhanced', 'academic', 'advance', 'frontier', 'state-of-the-art', 'sota', 'cutting-edge'],
    
    'Robotics & Autonomous Systems': ['robot', 'robotics', 'autonomous', 'automation', 'self-driving', 'drone', 'uav', 'control', 'sensor', 'perception', 'motion', 'navigation', 'grasping', 'manipulation', 'humanoid', 'embodied', 'physical', 'mechanical', 'actuator', 'motor', 'kinematic'],
    
    'HPC & Scientific Computing': ['hpc', 'high performance', 'scientific', 'simulation', 'modeling', 'computational', 'physics', 'chemistry', 'biology', 'weather', 'climate', 'earth', 'astronomy', 'parallel', 'distributed', 'exascale', 'petascale', 'supercomputing', 'numerical', 'mathematical', 'equation', 'differential'],
    
    'Computer Vision & Graphics': ['vision', 'image', 'video', 'graphics', 'rendering', 'ray tracing', 'visualization', '3d', 'ar', 'vr', 'xr', 'mixed reality', 'segmentation', 'detection', 'recognition', 'tracking', 'rtx', 'omniverse', 'camera', 'depth', 'scene', 'mesh', 'texture', 'animation'],
    
    'Security & Privacy': ['security', 'privacy', 'encryption', 'secure', 'threat', 'vulnerabil', 'risk', 'attack', 'defense', 'protection', 'compliance', 'regulation', 'gdpr', 'authentication', 'authorization', 'identity', 'trusted', 'safe', 'reliable', 'robust'],
    
    'Networking & Communication': ['network', 'networking', 'communication', '5g', '6g', 'wifi', 'ethernet', 'protocol', 'bandwidth', 'latency', 'throughput', 'connection', 'internet', 'iot', 'edge', 'cloud', 'distributed', 'federated', 'connectivity', 'wireless', 'signal', 'transmission'],
    
    'Quantum Computing': ['quantum', 'qubit', 'quantum computing', 'quantum machine learning', 'quantum algorithm', 'quantum simulation', 'quantum error correction', 'superposition', 'entanglement', 'quantum supremacy', 'quantum advantage'],
    
    'Data Science & Analytics': ['data science', 'analytics', 'data analysis', 'big data', 'data engineering', 'etl', 'database', 'sql', 'nosql', 'data lake', 'data warehouse', 'data visualization', 'dashboard', 'reporting', 'business intelligence', 'bi', 'metrics', 'kpi'],
    
    'Drug Discovery & Healthcare': ['drug', 'pharmaceutical', 'medicine', 'therapeutic', 'clinical', 'patient', 'disease', 'diagnosis', 'treatment', 'protein', 'molecule', 'cell', 'gene', 'genomic', 'biological', 'medical imaging', 'healthcare', 'hospital', 'doctor', 'therapy'],
    
    'Digital Twins & Simulation': ['digital twin', 'digital replica', 'simulation', 'virtual environment', 'synthetic', 'physics-based', 'real-time simulation', 'interactive simulation', 'physical system', 'mirror', 'replica', 'virtual world', 'metaverse'],
    
    'Multi-Agent Systems': ['multi-agent', 'agent', 'autonomous agent', 'swarm', 'collective intelligence', 'distributed decision', 'collaboration', 'coordination', 'cooperative', 'emergent behavior'],
    
    'Education & Training': ['education', 'training', 'learning', 'teach', 'student', 'curriculum', 'course', 'classroom', 'certification', 'skill', 'knowledge', 'career', 'professional development'],
    
    'Financial Technology': ['finance', 'financial', 'trading', 'investment', 'portfolio', 'risk', 'banking', 'payment', 'transaction', 'stock', 'market', 'fintech', 'cryptocurrency', 'blockchain', 'economic']
}

# Categorize each title
categorized_titles = {}
uncategorized = []

for i, title in enumerate(titles):
    title_lower = title.lower()
    best_category = None
    best_score = 0
    
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in title_lower)
        if score > best_score:
            best_score = score
            best_category = category
    
    if best_score > 0:
        if best_category not in categorized_titles:
            categorized_titles[best_category] = []
        categorized_titles[best_category].append((title, session_codes[i]))
    else:
        uncategorized.append((title, session_codes[i]))

# Add uncategorized to a special category
if uncategorized:
    categorized_titles['Miscellaneous & Other Topics'] = uncategorized

# Write categorized titles to file
with open('gtc_sessions_categorized.md', 'w') as f:
    f.write('# NVIDIA GTC 2025 Session Titles - Categorized\n\n')
    
    # Write summary statistics
    f.write('## Summary\n\n')
    f.write(f'- Total sessions: {len(titles)}\n')
    for category, titles in sorted(categorized_titles.items()):
        f.write(f'- {category}: {len(titles)} sessions\n')
    f.write('\n')
    
    # Write each category and its titles
    for category, titles in sorted(categorized_titles.items()):
        f.write(f'## {category} ({len(titles)} sessions)\n\n')
        
        for title, code in sorted(titles):
            f.write(f'- {title} [{code}]\n')
        
        f.write('\n')

print(f'Categorization complete. Found {len(titles)} total sessions across {len(categorized_titles)} categories.')
