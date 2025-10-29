# Study 2: Distance Proximity Effects on Trust

## Overview

This study investigates how spatial proximity between humans and AI agents influences trust dynamics in collaborative virtual reality environments. We examine the effects of distance proximity (1.8m vs. 5.4m) on multiple dimensions of trust, including trust development patterns, behavioral compliance, decision-making confidence, and learning outcomes.

## Research Questions

1. **Distance Proximity Effects**: How does spatial distance between humans and AI agents influence trust development?
2. **Trust Development Patterns**: How do trust attitudes change over time with different proximity conditions?
3. **Behavioral Trust**: How does proximity affect behavioral compliance and decision-making?
4. **Learning and Performance**: How does proximity influence learning outcomes and task performance?
5. **Agent Perceptions**: How does proximity affect how humans perceive AI agents?

## Experimental Design

- **Design**: Between-subjects design
- **Factor**: Distance Proximity
  - High Distance: 5.4 meters (social/public zone)
  - Low Distance: 1.8 meters (personal/social zone)
- **Sample Size**: 92 participants (46 per condition)
- **Task**: VR maze navigation with AI agent guidance
- **Duration**: ~60 minutes per session

## Theoretical Framework

### Proxemics Theory
Based on Hall's proxemics theory, we examine how spatial relationships influence human-AI interaction:
- **Personal Zone (0.45m-1.2m)**: Intimate interaction
- **Social Zone (1.2m-3.6m)**: Casual interaction
- **Public Zone (>3.6m)**: Formal interaction

### VR Distance Perception
Accounted for VR distance underestimation (50% reduction):
- **High Distance**: 5.4m (perceived as ~2.7m)
- **Low Distance**: 1.8m (perceived as ~0.9m)

## Key Findings

### Trust Development (Core Finding)
- **Trust Difference**: High distance (-8.4) vs. Low distance (+2.1), d = -0.578, p = .007
- **Trust Deterioration**: Distant agents lead to trust loss over time
- **Trust Building**: Close agents facilitate positive trust development

### Behavioral Trust
- **Decision Time**: Significant effects in Phase 2 (d = 0.449, p = .034) and error corners (d = 0.465, p = .028)
- **Compliance**: Significant effects on overall compliance (d = -0.578, p = .007) and overcompliance (d = -0.649, p = .002)
- **Trust Calibration**: Distant agents show better trust calibration (lower overcompliance)

### Agent Perceptions
- **Safety Perception**: Significant effect (d = -0.471, p = .027)
- **Communication**: Close agents perceived as more communicative
- **Social Processing**: Proximity affects social dimensions of agent perception

### Learning and Performance
- **Learning Improvement**: Significant effect (d = -0.717, p = .001)
- **Performance**: Close agents facilitate better learning outcomes

## Data Structure

### Main Dataset
- **File**: `task_final2.xlsx`
- **Participants**: 92 participants
- **Variables**: 120+ variables including demographics, trust measures, behavioral data, and qualitative responses

### Key Variables
- **Trust Measures**: Pre-task trust, post-task trust, trust difference
- **Behavioral Data**: Decision times by phase, compliance rates, navigation efficiency
- **Agent Perceptions**: Safety, intelligence, likeability, anthropomorphism
- **Distance Condition**: High distance (5.4m) vs. Low distance (1.8m)
- **Risk Propensity**: Pre-task, post-task, and difference measures

## Analysis Scripts

### Main Analysis
- **`main_analysis.py`**: Complete statistical analysis pipeline
- **`distance_proximity_analysis.py`**: Distance-specific analysis functions
- **`compliance_calculation.py`**: Compliance type calculations and analysis
- **`statistical_tests.py`**: Statistical testing and effect size calculations

### Key Analyses
1. **Trust Development**: Pre-post trust analysis and trust difference calculations
2. **Behavioral Trust**: Decision time analysis across phases and error situations
3. **Compliance Analysis**: Overall, appropriate, overcompliance, and undercompliance
4. **Agent Perceptions**: Multi-dimensional perception analysis
5. **Learning Analysis**: Performance improvement and learning outcomes
6. **Risk Propensity**: Baseline risk-taking tendencies

## Results

### Manuscript
Complete LaTeX manuscript in `results/manuscript/`:
- **Research Design**: Experimental setup and VR environment details
- **Methodology**: Detailed procedures and distance manipulation
- **Results**: Comprehensive statistical findings with 8 significant effects
- **Discussion**: Theoretical implications and practical applications

### Supplementary Figures
20+ high-quality figures in `results/figures_supplementary/`:
- **Trust Development**: Trust difference patterns by distance condition
- **Decision Time Analysis**: Phase-specific and error corner decision patterns
- **Compliance Behaviors**: Overall, appropriate, overcompliance, and undercompliance
- **Agent Perceptions**: Safety, intelligence, likeability, anthropomorphism
- **Learning Performance**: Learning improvement and outcomes
- **Qualitative Insights**: Word clouds, topic modeling, sentiment analysis

### Key Statistical Findings
- **Trust Development**: Significant effect on trust difference (d = -0.578, p = .007)
- **Learning Improvement**: Large effect size (d = -0.717, p = .001)
- **Overcompliance**: Significant effect (d = -0.649, p = .002)
- **Safety Perception**: Significant effect (d = -0.471, p = .027)
- **Decision Time**: Significant effects in Phase 2 and error corners
- **8 Significant Findings**: Across multiple trust dimensions

## Usage Instructions

1. **Data Preparation**: Run `data_preparation.py` to process raw data
2. **Main Analysis**: Execute `main_analysis.py` for complete statistical analysis
3. **Distance Analysis**: Use `distance_proximity_analysis.py` for proximity-specific analysis
4. **Compliance Analysis**: Run `compliance_calculation.py` for compliance type analysis
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
- Risk propensity assessment

## Theoretical Implications

### Proxemics Theory Extension
- Extends Hall's proxemics theory to human-AI interaction
- Demonstrates that spatial relationships influence trust formation
- Shows that proximity affects social processing of AI agents

### Trust Development Models
- Supports Lee's trust in automation model
- Demonstrates importance of spatial factors in trust formation
- Shows that proximity affects trust calibration mechanisms

### Social Processing of AI
- Supports Nass's Computers Are Social Actors paradigm
- Demonstrates that humans apply spatial social rules to AI agents
- Shows that proximity affects social dimensions of agent perception

## Practical Implications

### VR and Mixed Reality Design
- Optimize agent positioning for proximity
- Consider spatial relationships in interface design
- Balance proximity with trust calibration needs

### Human-AI Collaboration Systems
- Design for appropriate proximity in collaborative tasks
- Consider proximity effects on trust and performance
- Implement proximity-aware trust calibration mechanisms

## Citation

```bibtex
@article{study2_distance_proximity_trust_2024,
  title={Distance Proximity Effects on Trust in Human-AI Collaboration: A Virtual Reality Study},
  author={[Author Names]},
  journal={[Journal Name]},
  year={2024}
}
```

## Contact

For questions about Study 2, please contact [Contact Information].

