# GTC 2025 Insights and Analysis

This project analyzes data from NVIDIA's GTC 2025 conference, extracting insights, trends, and patterns from over 1300 sessions to create visually appealing reports and marketing materials.

## Overview

The GTC 2025 Insights project takes raw data extracted from the NVIDIA GTC conference website and transforms it into actionable insights and professional-quality materials for personal branding and knowledge sharing. The project includes:

1. **Enhanced Data Analysis**: Advanced analysis of session data, including categorization, trend identification, and visual representation.
2. **Professional Documentation**: Visually appealing PDF reports that effectively communicate key insights from the conference.
3. **Personal Branding Package**: A comprehensive set of marketing materials to leverage GTC insights for personal brand building.

## Project Structure

```
project/
├── src/                           # Source code directory
│   ├── extract_sessions.py        # Extracts session data from the conference HTML
│   ├── cluster_titles.py          # Basic session categorization
│   ├── enhanced_analysis.py       # Advanced analysis with visualizations
│   ├── create_enhanced_narrative.py # Generates enhanced narrative PDF
│   ├── create_marketing_package.py  # Creates marketing package materials
│   └── create_gtc_*.py            # Original PDF generation scripts
│
├── outputs/                       # Output files
│   ├── GTC_2025_*.pdf             # Generated PDF documents
│   ├── analysis_output/           # Analysis results and visualizations
│   ├── marketing_package/         # Personal branding materials
│   └── readable_versions/         # Alternative formats of PDFs
│
├── docs/                          # Documentation
│   └── readable_versions_guide.md # Guide for using readable versions
│
├── data/                          # Input data files 
│   ├── gtc_sessions_extracted.csv # Extracted session data
│   ├── gtc_sessions_titles.txt    # Session titles
│   └── GTCDATA/                   # Presentation PDFs from the conference
│
└── README.md                      # Project documentation
```

## Key Features

### Enhanced Analysis

- Improved session categorization with expanded keywords
- Visual representations of data through charts and word clouds
- Trend analysis within technology categories
- Key insights extraction based on data patterns

### Professional Documentation

- Modern, visually appealing design with NVIDIA brand colors
- Data-driven narratives that tell a compelling story
- Professional-quality PDF with proper typography and layout
- Integration of data visualizations for better understanding

### Marketing Package

- One-page executive summary for quick sharing
- Social media content templates for LinkedIn and Twitter
- Presentation slides for knowledge sharing
- Visual assets to enhance content engagement

## Usage

### Running the Analysis

```bash
python src/enhanced_analysis.py
```

This will analyze the GTC session data and generate visualizations and insights in the `outputs/analysis_output` directory.

### Creating the Enhanced Narrative

```bash
python src/create_enhanced_narrative.py
```

This will generate a professionally designed PDF narrative document that incorporates the analysis results.

### Generating the Marketing Package

```bash
python src/create_marketing_package.py
```

This will create a comprehensive marketing package in the `outputs/marketing_package` directory, including executive summary, social media content guide, and presentation template.

## Results

The project produces several key outputs:

1. **Data Analysis**: Category distribution, word clouds, keyword frequency charts, and more visual representations of the GTC data.
2. **Enhanced Narrative**: A visually appealing PDF document that tells the story of GTC 2025 through data-driven insights.
3. **Marketing Materials**: A complete package for leveraging GTC insights in personal branding efforts.

## Alternative Formats

If you encounter issues with PDF files, you can access readable versions of all content in the `outputs/readable_versions` directory, available in both Markdown and HTML formats.

## Requirements

- Python 3.6+
- Required packages:
  - reportlab
  - matplotlib
  - seaborn
  - pandas
  - scikit-learn
  - wordcloud

Install all required packages:

```bash
pip install -r requirements.txt
```

## License

This project is for personal use only. Conference data is owned by NVIDIA.

## Acknowledgments

- NVIDIA for organizing GTC 2025
- The open-source Python visualization community
