# Study 1: Memory Function and Personality Matching Effects on Trust

## Overview

This study investigates how memory function and personality matching between humans and AI agents influence trust development in collaborative virtual reality environments. We examine the effects of memory assistance and agent personality (extrovert vs. introvert) on multiple dimensions of trust, including self-reported attitudes, behavioral compliance, decision-making patterns, and learning outcomes.

## Research Questions

1. **Memory Function Effects**: How does memory assistance influence trust development and behavioral compliance?
2. **Personality Matching Effects**: How does matching/mismatching human and agent personalities affect trust and collaboration?
3. **Interaction Effects**: Do memory function and personality matching interact to influence trust outcomes?
4. **Trust Development Patterns**: How do trust attitudes change over the course of interaction?

## Experimental Design

- **Design**: 2 × 2 between-subjects factorial design
- **Factors**: 
  - Memory Function: With Memory vs. Without Memory
  - Agent Personality: Extrovert vs. Introvert
- **Sample Size**: 92 participants (23 per condition)
- **Task**: VR maze navigation with AI agent guidance
- **Duration**: ~60 minutes per session

## Key Findings

### Memory Function Effects
- **Trust Development**: Memory function significantly affects trust change over time
- **Decision Time**: Participants with memory assistance show different decision patterns
- **Learning**: Memory function influences learning curves and improvement
- **Compliance**: Memory affects behavioral compliance with agent recommendations

### Personality Matching Effects
- **Agent Perceptions**: Personality matching influences likeability and intelligence ratings
- **Trust Attitudes**: Matching affects pre-task and post-task trust levels
- **Compliance Behaviors**: Personality matching influences compliance patterns
- **Decision Making**: Matching affects decision confidence and timing

### Trust Development Patterns
- **Phase Differences**: Trust development varies across navigation phases
- **Learning Curves**: Trust patterns change as participants gain experience
- **Error Handling**: Trust responses to agent errors vary by condition

## Data Structure

### Main Dataset
- **File**: `task1_final.xlsx`
- **Participants**: 92 participants
- **Variables**: 150+ variables including demographics, trust measures, behavioral data, and qualitative responses

### Key Variables
- **Trust Measures**: Pre-task trust, post-task trust, trust difference
- **Behavioral Data**: Decision times, compliance rates, navigation efficiency
- **Agent Perceptions**: Safety, intelligence, likeability, anthropomorphism
- **Memory Function**: With/without memory assistance condition
- **Personality**: Agent personality type and participant personality measures

## Analysis Scripts

### Main Analysis
- **`main_analysis.py`**: Complete statistical analysis pipeline
- **`trust_metrics_calculation.py`**: Trust measurement and calculation functions
- **`statistical_tests.py`**: Statistical testing and effect size calculations
- **`qualitative_analysis.py`**: Text analysis and qualitative insights

### Key Analyses
1. **Trust Development**: Pre-post trust analysis and trust difference calculations
2. **Behavioral Trust**: Decision time analysis across phases and conditions
3. **Compliance Analysis**: Overall, appropriate, and overcompliance behaviors
4. **Agent Perceptions**: Multi-dimensional perception analysis
5. **Learning Analysis**: Performance improvement and learning curves
6. **Qualitative Analysis**: Text mining, sentiment analysis, and topic modeling

## Results

### Manuscript
Complete LaTeX manuscript in `results/manuscript/`:
- **Research Design**: Experimental setup and methodology
- **Methodology**: Detailed procedures and measures
- **Results**: Comprehensive statistical findings
- **Discussion**: Theoretical implications and practical applications

### Supplementary Figures
54 high-quality figures in `results/figures_supplementary/`:
- **Trust Distributions**: Pre-task, post-task, and trust change patterns
- **Decision Time Analysis**: Phase-specific and overall decision patterns
- **Compliance Behaviors**: Overall, appropriate, and overcompliance rates
- **Agent Perceptions**: Multi-dimensional perception comparisons
- **Learning Curves**: Performance improvement over time
- **Qualitative Insights**: Word clouds, topic modeling, sentiment analysis

### Key Statistical Findings
- **Memory Function**: Significant effects on trust development (d = 0.92)
- **Personality Matching**: Significant effects on agent perceptions (d = -0.684)
- **Trust Development**: Differential patterns across conditions
- **Behavioral Trust**: Significant effects on decision time and compliance
- **Learning**: Memory function affects learning improvement

## Usage Instructions

1. **Data Preparation**: Run `data_preparation.py` to process raw data
2. **Main Analysis**: Execute `main_analysis.py` for complete statistical analysis
3. **Trust Metrics**: Use `trust_metrics_calculation.py` for trust calculations
4. **Qualitative Analysis**: Run `qualitative_analysis.py` for text analysis
5. **Results**: Review LaTeX manuscript and supplementary figures

## Requirements

- Python 3.8+
- Required packages: pandas, numpy, scipy, matplotlib, seaborn, scikit-learn, nltk
- LaTeX (for manuscript compilation)

## Survey Files

Upload Qualtrics survey files to the `surveys/` folder:
- Pre-task questionnaire
- Post-task questionnaire
- Demographics survey
- Personality assessment

## Citation

```bibtex
@article{study1_memory_personality_trust_2024,
  title={Memory Function and Personality Matching Effects on Trust in Human-AI Collaboration},
  author={[Author Names]},
  journal={[Journal Name]},
  year={2024}
}
```

## Contact

For questions about Study 1, please contact [Contact Information].

