#!/usr/bin/env python3
"""
Organize GitHub Repository for Human-AI Trust Studies
Creates proper directory structure and copies important files
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the complete GitHub repository structure"""
    
    # Base paths
    base_path = Path(".")
    study1_path = base_path / "Study1_Memory_Personality_Trust"
    study2_path = base_path / "Study2_Distance_Proximity_Trust"
    shared_path = base_path / "Shared_Resources"
    
    # Create Study 1 structure
    study1_dirs = [
        "analysis",
        "data", 
        "results/manuscript",
        "results/figures_supplementary",
        "results/qualitative_analysis",
        "summaries",
        "surveys"
    ]
    
    for dir_path in study1_dirs:
        full_path = study1_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {full_path}")
    
    # Create Study 2 structure
    study2_dirs = [
        "analysis",
        "data",
        "results/manuscript", 
        "results/figures_supplementary",
        "results/qualitative_analysis",
        "summaries",
        "surveys"
    ]
    
    for dir_path in study2_dirs:
        full_path = study2_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {full_path}")
    
    # Create Shared Resources structure
    shared_dirs = [
        "common_functions",
        "references",
        "documentation"
    ]
    
    for dir_path in shared_dirs:
        full_path = shared_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {full_path}")

def copy_study1_files():
    """Copy Study 1 important files"""
    print("\n=== Copying Study 1 Files ===")
    
    # Copy data files
    data_files = [
        ("../task1_final.xlsx", "Study1_Memory_Personality_Trust/data/task1_final.xlsx")
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy analysis scripts
    analysis_files = [
        ("../COMPLETE_INTEGRATED_ANALYSIS.py", "Study1_Memory_Personality_Trust/analysis/main_analysis.py"),
        ("../COMPREHENSIVE_PUBLICATION_FIGURES.py", "Study1_Memory_Personality_Trust/analysis/create_figures.py"),
        ("../COMPREHENSIVE_QUALITATIVE_ANALYSIS.py", "Study1_Memory_Personality_Trust/analysis/qualitative_analysis.py"),
        ("../METRICS_CALCULATION_GUIDE.md", "Study1_Memory_Personality_Trust/analysis/trust_metrics_calculation.py")
    ]
    
    for src, dst in analysis_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy manuscript files
    manuscript_files = [
        ("../FINAL_PACKAGE_READY_FOR_PUBLICATION/01_FOR_JOURNAL_MANUSCRIPT/01_RESEARCH_DESIGN.tex", 
         "Study1_Memory_Personality_Trust/results/manuscript/01_RESEARCH_DESIGN.tex"),
        ("../FINAL_PACKAGE_READY_FOR_PUBLICATION/01_FOR_JOURNAL_MANUSCRIPT/02_METHODOLOGY.tex",
         "Study1_Memory_Personality_Trust/results/manuscript/02_METHODOLOGY.tex"),
        ("../FINAL_PACKAGE_READY_FOR_PUBLICATION/01_FOR_JOURNAL_MANUSCRIPT/03_RESULTS_FROM_MD.tex",
         "Study1_Memory_Personality_Trust/results/manuscript/03_RESULTS.tex"),
        ("../FINAL_PACKAGE_READY_FOR_PUBLICATION/01_FOR_JOURNAL_MANUSCRIPT/04_DISCUSSION_COMPLETE.tex",
         "Study1_Memory_Personality_Trust/results/manuscript/04_DISCUSSION.tex")
    ]
    
    for src, dst in manuscript_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy supplementary figures
    figures_source = "../FINAL_PACKAGE_READY_FOR_PUBLICATION/04_FIGURES_SUPPLEMENTARY/"
    figures_dest = "Study1_Memory_Personality_Trust/results/figures_supplementary/"
    
    if os.path.exists(figures_source):
        for file in os.listdir(figures_source):
            if file.endswith('.png'):
                src = figures_source + file
                dst = figures_dest + file
                shutil.copy2(src, dst)
                print(f"Copied figure: {file}")
    
    # Copy summary files
    summary_files = [
        ("../FINAL_COMPLETE_PACKAGE_README.md", "Study1_Memory_Personality_Trust/summaries/FINAL_SUMMARY.md"),
        ("../METRICS_CALCULATION_GUIDE.md", "Study1_Memory_Personality_Trust/summaries/METRICS_DOCUMENTATION.md"),
        ("../ADVANCED_NLP_INSIGHTS.md", "Study1_Memory_Personality_Trust/summaries/QUALITATIVE_INSIGHTS.md")
    ]
    
    for src, dst in summary_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")

def copy_study2_files():
    """Copy Study 2 important files"""
    print("\n=== Copying Study 2 Files ===")
    
    # Copy data files
    data_files = [
        ("../task2_final.xlsx", "Study2_Distance_Proximity_Trust/data/task2_final.xlsx")
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy analysis scripts
    analysis_files = [
        ("../Distance_Proximity_Analysis/CREATE_EXACT_STUDY1_MATCHING_FIGURES.py", 
         "Study2_Distance_Proximity_Trust/analysis/main_analysis.py"),
        ("../Distance_Proximity_Analysis/CALCULATE_DISTANCE_COMPLIANCE_TYPES.py",
         "Study2_Distance_Proximity_Trust/analysis/compliance_calculation.py"),
        ("../Distance_Proximity_Analysis/COMPLETE_DISTANCE_TRUST_ANALYSIS.py",
         "Study2_Distance_Proximity_Trust/analysis/distance_proximity_analysis.py")
    ]
    
    for src, dst in analysis_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy manuscript files
    manuscript_files = [
        ("../Distance_Proximity_Analysis/01_RESEARCH_DESIGN.tex",
         "Study2_Distance_Proximity_Trust/results/manuscript/01_RESEARCH_DESIGN.tex"),
        ("../Distance_Proximity_Analysis/02_METHODOLOGY.tex",
         "Study2_Distance_Proximity_Trust/results/manuscript/02_METHODOLOGY.tex"),
        ("../Distance_Proximity_Analysis/03_RESULTS.tex",
         "Study2_Distance_Proximity_Trust/results/manuscript/03_RESULTS.tex"),
        ("../Distance_Proximity_Analysis/04_DISCUSSION.tex",
         "Study2_Distance_Proximity_Trust/results/manuscript/04_DISCUSSION.tex")
    ]
    
    for src, dst in manuscript_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    
    # Copy supplementary figures
    figures_source = "../Distance_Proximity_Analysis/03_FIGURES_MAIN/"
    figures_dest = "Study2_Distance_Proximity_Trust/results/figures_supplementary/"
    
    if os.path.exists(figures_source):
        for file in os.listdir(figures_source):
            if file.endswith('.png'):
                src = figures_source + file
                dst = figures_dest + file
                shutil.copy2(src, dst)
                print(f"Copied figure: {file}")
    
    # Copy summary files
    summary_files = [
        ("../Distance_Proximity_Analysis/FINAL_COMPREHENSIVE_DISTANCE_ANALYSIS.md",
         "Study2_Distance_Proximity_Trust/summaries/FINAL_SUMMARY.md"),
        ("../Distance_Proximity_Analysis/DISTANCE_PROXIMITY_FINDINGS_REPORT.md",
         "Study2_Distance_Proximity_Trust/summaries/DISTANCE_PROXIMITY_FINDINGS.md")
    ]
    
    for src, dst in summary_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")

def copy_shared_files():
    """Copy shared resource files"""
    print("\n=== Copying Shared Resources ===")
    
    # Copy common functions
    common_files = [
        ("../METRICS_CALCULATION_GUIDE.md", "Shared_Resources/common_functions/trust_metrics.py"),
        ("../COMPLETE_REFERENCES_LIST.md", "Shared_Resources/references/references_list.md"),
        ("../COMPLETE_REFERENCES_BIBLIOGRAPHY.bib", "Shared_Resources/references/bibliography.bib")
    ]
    
    for src, dst in common_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        else:
            print(f"Not found: {src}")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements_content = """# Human-AI Trust Studies - Requirements
# Python packages required for analysis

# Data processing
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0

# Visualization
matplotlib>=3.4.0
seaborn>=0.11.0

# Machine Learning
scikit-learn>=1.0.0

# Text Analysis
nltk>=3.6.0
wordcloud>=1.8.0

# Statistical Analysis
statsmodels>=0.13.0

# File I/O
openpyxl>=3.0.0
xlsxwriter>=3.0.0

# Jupyter (optional)
jupyter>=1.0.0
ipykernel>=6.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    print("Created: requirements.txt")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Human-AI Trust Studies - .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data files (large datasets)
*.csv
*.xlsx
*.xls
!*_sample.csv
!*_sample.xlsx

# Large figure files (keep only essential ones)
*.png
!Fig_*.png

# Temporary files
*.tmp
*.temp
*.log

# LaTeX
*.aux
*.log
*.out
*.toc
*.fdb_latexmk
*.fls
*.synctex.gz
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("Created: .gitignore")

def main():
    """Main function to organize the GitHub repository"""
    print("🚀 Organizing GitHub Repository for Human-AI Trust Studies")
    print("=" * 60)
    
    # Create directory structure
    create_directory_structure()
    
    # Copy files
    copy_study1_files()
    copy_study2_files()
    copy_shared_files()
    
    # Create configuration files
    create_requirements_file()
    create_gitignore()
    
    print("\n✅ GitHub Repository organization complete!")
    print("\nRepository structure created with:")
    print("  - Study 1: Memory Function and Personality Matching")
    print("  - Study 2: Distance Proximity Effects")
    print("  - Shared Resources: Common functions and documentation")
    print("  - All manuscript files in LaTeX format")
    print("  - Supplementary figures organized")
    print("  - Analysis scripts and summaries")
    print("  - Survey folders ready for Qualtrics files")
    
    print("\nNext steps:")
    print("  1. Upload Qualtrics survey files to surveys/ folders")
    print("  2. Review and test analysis scripts")
    print("  3. Compile LaTeX manuscripts")
    print("  4. Initialize Git repository and push to GitHub")

if __name__ == "__main__":
    main()

