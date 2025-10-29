# Trust Metrics Calculation Guide
## Complete Technical Documentation for Research Publication

**Document Purpose**: Provide precise mathematical definitions and calculation procedures for all trust metrics used in the VR navigation study.

**For**: Methods section, supplementary materials, and replication studies

---

## Table of Contents

1. [Self-Reported Trust Measures](#1-self-reported-trust-measures)
2. [Behavioral Trust: Compliance Metrics](#2-behavioral-trust-compliance-metrics)
3. [Behavioral Trust: Decision Time Metrics](#3-behavioral-trust-decision-time-metrics)
4. [Trust Calibration Metrics](#4-trust-calibration-metrics)
5. [Help-Seeking and Reliance Metrics](#5-help-seeking-and-reliance-metrics)
6. [Agent Perception Metrics](#6-agent-perception-metrics)
7. [VR Experience Metrics](#7-vr-experience-metrics)

---

## 1. Self-Reported Trust Measures

### 1.1 Pre-Task Trust (Trust_pre)

**Definition**: Initial dispositional trust in the AI agent before task interaction.

**Calculation**:
```
Trust_pre = Σ(item_i) / n_items × 100
```

Where:
- *item_i* = Likert scale response (1-7) for trust questionnaire item *i*
- *n_items* = 7 (number of trust scale items)
- Multiplied by 100 to convert to 0-100 scale

**Scale Items** (7-point Likert: 1 = Strongly Disagree, 7 = Strongly Agree):
1. "I will trust the robot's recommendations"
2. "The robot will be reliable"
3. "I feel confident in the robot's abilities"
4. "The robot will act in my best interest"
5. "I believe the robot is competent"
6. "I can depend on the robot"
7. "The robot is trustworthy"

**Range**: 0-100  
**Interpretation**: Higher scores indicate greater initial trust disposition  
**Sample Statistics**: M = 71.96, SD = 20.71

---

### 1.2 Post-Task Trust (Trust_post)

**Definition**: Trust in the AI agent after completing the navigation task.

**Calculation**:
```
Trust_post = Σ(item_i) / n_items × 100
```

**Same scale items as Trust_pre, administered post-task**

**Range**: 0-100  
**Interpretation**: Higher scores indicate greater learned trust  
**Sample Statistics**: M = 72.73, SD = 18.20

---

### 1.3 Trust Change (Trust_difference)

**Definition**: Change in trust from pre-task to post-task, indicating trust development through interaction.

**Calculation**:
```
Trust_difference = Trust_post - Trust_pre
```

**Range**: -100 to +100  
**Interpretation**:
- Positive values = Trust increased
- Negative values = Trust decreased
- Zero = Trust unchanged

**Sample Statistics**: M = +0.77, SD = 16.37

---

### 1.4 Trust Improvement Indicator

**Definition**: Binary indicator of whether trust increased from pre to post.

**Calculation**:
```
Trust_improved = {
    1, if Trust_difference > 0
    0, otherwise
}
```

**Range**: 0 (no improvement) or 1 (improved)  
**Sample Statistics**: 45.7% of participants showed trust improvement

---

### 1.5 General Trust Propensity

**Definition**: Baseline trust disposition across all agents and contexts.

**Calculation**:
```
Propensity = Σ(item_i) / n_items × 100
```

**Scale Items** (5-point Likert: 1 = Strongly Disagree, 5 = Strongly Agree):
1. "Most people can be trusted"
2. "I generally trust others until given reason not to"
3. "People are generally reliable"

**Range**: 0-100  
**Sample Statistics**: M = 66.48, SD = 18.05

---

## 2. Behavioral Trust: Compliance Metrics

### 2.1 Overall Compliance Rate

**Definition**: Percentage of navigation decisions where participant followed agent's recommendation.

**Calculation**:
```
Compliance_rate = (n_followed / n_total) × 100%

Where:
n_followed = Σ(I(decision_i = recommendation_i))
n_total = 10 (total corners)
```

**Detailed Formula**:
```
For each corner i ∈ {1, 2, ..., 10}:
    I_i = {
        1, if participant_direction_i = agent_recommendation_i
        0, otherwise
    }

Compliance_rate = (Σ I_i / 10) × 100%
```

**Range**: 0-100%  
**Interpretation**: Higher percentage indicates greater reliance on agent  
**Sample Statistics**: M = 72.92%, SD = 14.24%

---

### 2.2 Appropriate Compliance

**Definition**: Following agent recommendations **when agent provides correct guidance**.

**Calculation**:
```
Appropriate_compliance = Σ I(follow_i AND correct_i)

Where:
i ∈ {1, 3, 5, 7, 9}  (corners where agent was correct)

I(follow_i AND correct_i) = {
    1, if participant followed agent at correct corner i
    0, otherwise
}
```

**Mathematical Formula**:
```
Appropriate_compliance = |{c ∈ C_correct : decision(c) = recommendation(c)}|

Where:
C_correct = {1, 3, 5, 7, 9}  (set of correct-guidance corners)
decision(c) = participant's chosen direction at corner c
recommendation(c) = agent's recommended direction at corner c
```

**Range**: 0-5  
**Percentage Form**: (Appropriate_compliance / 5) × 100%  
**Sample Statistics**: M = 1.07, SD = 0.55 (21.3% rate)  
**Theoretical Importance**: Measures **calibrated trust**—following when agent is reliable

---

### 2.3 Overcompliance

**Definition**: Following agent recommendations **when agent provides incorrect guidance**.

**Calculation**:
```
Overcompliance = Σ I(follow_i AND incorrect_i)

Where:
i ∈ {2, 4, 6, 8, 10}  (corners where agent was incorrect)

I(follow_i AND incorrect_i) = {
    1, if participant followed agent at incorrect corner i
    0, otherwise
}
```

**Mathematical Formula**:
```
Overcompliance = |{c ∈ C_error : decision(c) = recommendation(c)}|

Where:
C_error = {2, 4, 6, 8, 10}  (set of error-guidance corners)
```

**Range**: 0-5  
**Percentage Form**: (Overcompliance / 5) × 100%  
**Sample Statistics**: M = 2.08, SD = 0.65 (41.6% rate)  
**Theoretical Importance**: Indicates **over-reliance** or **blind trust**—failing to detect agent errors

---

### 2.4 Undercompliance

**Definition**: **Not** following agent recommendations **when agent provides correct guidance**.

**Calculation**:
```
Undercompliance = Σ I(NOT follow_i AND correct_i)

Where:
i ∈ {1, 3, 5, 7, 9}  (corners where agent was correct)

I(NOT follow_i AND correct_i) = {
    1, if participant did NOT follow agent at correct corner i
    0, otherwise
}
```

**Mathematical Formula**:
```
Undercompliance = |{c ∈ C_correct : decision(c) ≠ recommendation(c)}|

Or equivalently:
Undercompliance = 5 - Appropriate_compliance
```

**Range**: 0-5  
**Percentage Form**: (Undercompliance / 5) × 100%  
**Sample Statistics**: M = 3.93, SD = 0.55 (78.7% rate)  
**Theoretical Importance**: Indicates **under-reliance** or **mistrust**—rejecting valid agent guidance

---

### 2.5 Initial Trust (Corner 1 Compliance)

**Definition**: Agent-following behavior at the very first navigation decision, indicating initial trust before performance feedback.

**Calculation**:
```
Initial_trust = {
    1, if decision_corner1 = recommendation_corner1
    0, otherwise
}
```

**Range**: 0 (did not follow) or 1 (followed)  
**Sample Statistics**: 84.8% followed agent at Corner 1  
**Theoretical Importance**: Measures **default trust**—trust prior to performance evidence

---

### 2.6 Phase-Specific Compliance

**Definition**: Compliance calculated separately for Phase 1 (guided navigation) and Phase 2 (memory-based navigation).

**Phase 1 Calculation** (Corners 1-5):
```
Compliance_Phase1 = (Σ(i=1 to 5) I(follow_i)) / 5 × 100%
```

**Phase 2 Calculation** (Corners 6-10):
```
Compliance_Phase2 = (Σ(i=6 to 10) I(follow_i)) / 5 × 100%
```

**Compliance Change**:
```
Compliance_change = Compliance_Phase2 - Compliance_Phase1
```

**Sample Statistics**:
- Phase 1: M = 75.22%, SD = 16.96%
- Phase 2: M = 70.65%, SD = 18.53%
- Change: M = -4.57%, SD = 18.63%

**Theoretical Importance**: Examines **trust dynamics**—whether compliance increases (learning) or decreases (disillusionment) over time

---

## 3. Behavioral Trust: Decision Time Metrics

### 3.1 Overall Mean Decision Time

**Definition**: Average time taken to make navigation decisions across all corners.

**Calculation**:
```
Decision_time_overall = (Σ(i=1 to 10) time_i) / 10

Where:
time_i = time (seconds) from decision prompt to direction selection at corner i
```

**Data Cleaning**:
```
Excluded: time_i > 60 seconds (outliers indicating distraction)
Missing data: Imputed with participant's mean if < 20% missing
```

**Range**: Typically 5-30 seconds  
**Sample Statistics**: M = 13.23s, SD = 6.30s  
**Theoretical Importance**: Implicit measure of **decision confidence**—longer times indicate hesitation/uncertainty

---

### 3.2 Phase-Specific Decision Time

**Phase 1 Decision Time** (Corners 1-5):
```
Time_Phase1 = (Σ(i=1 to 5) time_i) / 5
```

**Phase 2 Decision Time** (Corners 6-10):
```
Time_Phase2 = (Σ(i=6 to 10) time_i) / 5
```

**Sample Statistics**:
- Phase 1: M = 11.72s, SD = 4.49s
- Phase 2: M = 14.71s, SD = 9.56s

---

### 3.3 Learning Curve (Decision Time Change)

**Definition**: Change in decision speed from Phase 1 to Phase 2, indicating learning efficiency.

**Calculation**:
```
Learning_curve = Time_Phase2 - Time_Phase1

Or as percentage change:
Learning_curve_% = ((Time_Phase2 - Time_Phase1) / Time_Phase1) × 100%
```

**Interpretation**:
- **Negative values**: Faster in Phase 2 (learning/confidence gain)
- **Positive values**: Slower in Phase 2 (increased uncertainty)

**Sample Statistics**: M = +2.99s, SD = 7.15s  
**Theoretical Importance**: **Learning reversal** with memory function (d = 1.53) revealed memory impaired rather than aided decision-making

---

### 3.4 Error Corner Decision Time

**Definition**: Average decision time at corners where agent provided incorrect guidance, indicating sensitivity to agent errors.

**Calculation**:
```
Time_error = (Σ(i ∈ {2,4,6,8,10}) time_i) / 5
```

**Theoretically Important Variant** - Subset of Error Corners (3, 7, 9):
```
Time_error_subset = (time_3 + time_7 + time_9) / 3

Where corners 3, 7, 9 selected for specific error conditions
```

**Sample Statistics**: M = 13.70s, SD = 6.79s  
**Theoretical Importance**: Longer times at error corners indicate **error detection** or **suspicion**

---

## 4. Trust Calibration Metrics

### 4.1 Trust-Compliance Alignment

**Definition**: Correlation between self-reported trust and actual compliance behavior, indicating trust calibration accuracy.

**Calculation**:
```
Alignment_i = r(Trust_post_i, Compliance_rate_i)

Where:
r = Pearson correlation coefficient
Calculated within experimental condition or overall
```

**Formula**:
```
r = Σ((Trust_i - Trust_mean)(Compliance_i - Compliance_mean)) / 
    √(Σ(Trust_i - Trust_mean)²) × √(Σ(Compliance_i - Compliance_mean)²)
```

**Range**: -1 to +1  
**Interpretation**:
- High positive *r*: Well-calibrated (trust attitudes match behaviors)
- Low *r*: Poorly calibrated (attitude-behavior dissociation)

**Sample Statistics**:
- Matched condition: r = .365, p < .01
- Mismatched condition: r = .058, p = .695

**Theoretical Importance**: Distinguishes **felt trust** from **behavioral trust**

---

### 4.2 Appropriate Compliance Ratio

**Definition**: Ratio of appropriate compliance to overcompliance, indicating discrimination ability.

**Calculation**:
```
Discrimination_ratio = Appropriate_compliance / (Overcompliance + 1)

Note: +1 in denominator prevents division by zero
```

**Alternative Formula** (Signal Detection Theory):
```
Discrimination_index = (Appropriate_compliance - Overcompliance) / 5

Range: -1 (always follow when wrong) to +1 (always follow when right)
```

**Sample Statistics**: Mean ratio = 0.51 (more overcompliance than appropriate)  
**Theoretical Importance**: Measures **trust calibration quality**—ability to discriminate agent reliability

---

## 5. Help-Seeking and Reliance Metrics

### 5.1 Total Help Requests

**Definition**: Number of times participant requested agent assistance.

**Calculation**:
```
Total_help = Σ(i=1 to 50) I(help_requested_i)

Where:
i = decision point (10 corners × 5 decisions each = 50 opportunities)
I(help_requested_i) = {1 if help requested, 0 otherwise}
```

**Range**: 0-50  
**Sample Statistics**: M = 0.39, SD = 1.62 (very low usage: 13% of participants used help)

---

### 5.2 Cumulative Help Cost

**Definition**: Total cognitive cost of help-seeking, assuming each help request has associated cost.

**Calculation**:
```
Help_cost = Total_help × cost_per_help

Assuming: cost_per_help = 1 unit
Therefore: Help_cost = Total_help
```

**Alternative Weighted Cost**:
```
Help_cost_weighted = Σ(i=1 to n_help) (time_remaining_i × difficulty_i)

Where time pressure and task difficulty modulate cost
```

**Sample Statistics**: M = 0.39, SD = 1.62

---

### 5.3 Overreliance

**Definition**: Excessive help-seeking beyond what is optimal.

**Calculation**:
```
Overreliance = {
    1, if Total_help > threshold
    0, otherwise
}

Where threshold = 2 (based on task difficulty)
```

**Alternative Continuous Measure**:
```
Overreliance_score = max(0, Total_help - optimal_help)

Where optimal_help estimated from expert performance
```

**Sample Statistics**: 1.1% showed overreliance  
**Theoretical Importance**: Indicates **over-dependence** on agent

---

### 5.4 Underreliance

**Definition**: Insufficient help-seeking when facing difficulty.

**Calculation**:
```
Underreliance = {
    1, if (decision_time > 60s OR error_occurred) AND Total_help = 0
    0, otherwise
}
```

**Formula**:
```
Underreliance = I(struggling) × I(no_help_sought)

Where:
I(struggling) = 1 if decision_time > threshold OR error made
I(no_help_sought) = 1 if Total_help = 0
```

**Sample Statistics**: 3.3% showed underreliance  
**Theoretical Importance**: Indicates **under-trust** or **excessive self-reliance**

---

### 5.5 Misplaced Reliance

**Definition**: Seeking help when agent provided correct guidance (unnecessary verification).

**Calculation**:
```
Misplaced_reliance = (n_help_when_correct / n_correct_corners) × 100%

Where:
n_help_when_correct = |{c ∈ C_correct : help_requested(c) = 1}|
n_correct_corners = 5
```

**Sample Statistics**: M = 1.09%, SD = 4.36%  
**Theoretical Importance**: **Paradoxical** help-seeking—seeking verification when agent is reliable

---

### 5.6 Mistrust Rate

**Definition**: Failing to seek help when agent provided incorrect guidance (missed error detection).

**Calculation**:
```
Mistrust_rate = (n_no_help_when_wrong / n_error_corners) × 100%

Where:
n_no_help_when_wrong = |{c ∈ C_error : help_requested(c) = 0}|
n_error_corners = 5
```

**Sample Statistics**: M = 98.91%, SD = 4.36% (very high—most didn't seek help when wrong)  
**Theoretical Importance**: Indicates failure to **detect agent unreliability**

---

## 6. Agent Perception Metrics

### 6.1 Godspeed Questionnaire Scales

All agent perception metrics calculated from Godspeed Questionnaire (Bartneck et al., 2009).

**General Calculation Formula**:
```
Scale_score = Σ(item_i) / n_items

Where items rated on 5-point semantic differential scales
```

---

#### 6.1.1 Perceived Intelligence

**Items** (5-point scale):
- Incompetent ←→ Competent
- Ignorant ←→ Knowledgeable
- Irresponsible ←→ Responsible
- Unintelligent ←→ Intelligent
- Foolish ←→ Sensible

**Calculation**:
```
Intelligence = (Σ(i=1 to 5) item_i) / 5
```

**Range**: 1-5  
**Sample Statistics**: M = 3.42, SD = 0.85  
**Theoretical Importance**: **Strongest predictor** of trust (r = .569)

---

#### 6.1.2 Perceived Animacy

**Items**:
- Dead ←→ Alive
- Stagnant ←→ Lively
- Mechanical ←→ Organic
- Artificial ←→ Lifelike
- Inert ←→ Interactive

**Calculation**: Same as Intelligence  
**Range**: 1-5  
**Sample Statistics**: M = 2.51, SD = 0.76  
**Theoretical Importance**: Predicted Phase 1 decision speed (r = -.26)

---

#### 6.1.3 Perceived Likeability

**Items**:
- Dislike ←→ Like
- Unfriendly ←→ Friendly
- Unkind ←→ Kind
- Unpleasant ←→ Pleasant
- Awful ←→ Nice

**Calculation**: Same as Intelligence  
**Range**: 1-5  
**Sample Statistics**: M = 3.76, SD = 0.79  
**Theoretical Importance**: Second-strongest trust predictor (r = .458)

---

#### 6.1.4 Anthropomorphism

**Items**:
- Fake ←→ Natural
- Machine-like ←→ Human-like
- Unconscious ←→ Conscious
- Artificial ←→ Lifelike
- Moving rigidly ←→ Moving elegantly

**Range**: 1-5  
**Sample Statistics**: M = 2.48, SD = 0.66

---

#### 6.1.5 Perceived Safety

**Items**:
- Anxious ←→ Relaxed
- Agitated ←→ Calm
- Surprised ←→ Quiescent

**Range**: 1-5  
**Sample Statistics**: M = 2.52, SD = 0.52

---

#### 6.1.6 Aesthetic Appeal

**Items**:
- Ugly ←→ Beautiful
- Unpleasant ←→ Pleasant

**Range**: 1-5  
**Sample Statistics**: M = 3.13, SD = 0.72

---

## 7. VR Experience Metrics

### 7.1 VR Familiarity

**Definition**: Prior experience with VR technology.

**Calculation**:
```
Familiarity = Σ(item_i) / n_items

Items (5-point scale):
1. "I am familiar with VR technology"
2. "I have used VR before"
3. "I feel comfortable in VR environments"
```

**Range**: 1-5  
**Sample Statistics**: M = 2.87, SD = 1.15

---

### 7.2 VR Immersion

**Definition**: Subjective sense of presence in the virtual environment.

**Calculation**:
```
Immersion = Σ(item_i) / n_items

Items (7-point scale):
1. "I felt like I was really in the maze"
2. "The VR environment seemed real"
3. "I forgot I was in a virtual world"
4. "I felt present in the environment"
```

**Range**: 1-7  
**Sample Statistics**: M = 4.92, SD = 1.23

---

### 7.3 VR Self-Efficacy

**Definition**: Confidence in one's ability to navigate in VR.

**Calculation**:
```
Self_efficacy = Σ(item_i) / n_items

Items (7-point scale):
1. "I feel confident navigating in VR"
2. "I can effectively interact in VR"
3. "I am good at VR tasks"
```

**Range**: 1-7  
**Sample Statistics**: M = 5.24, SD = 1.18  
**Theoretical Importance**: Predicted post-task trust (r = .272)

---

## Summary Table: All Metrics

| Metric Category | Metric Name | Formula | Range | M (SD) |
|----------------|-------------|---------|-------|--------|
| **Self-Report Trust** |
| | Pre-task trust | Σ(items)/7 × 100 | 0-100 | 71.96 (20.71) |
| | Post-task trust | Σ(items)/7 × 100 | 0-100 | 72.73 (18.20) |
| | Trust change | Post - Pre | -100 to +100 | +0.77 (16.37) |
| **Compliance** |
| | Overall rate | (followed/10) × 100% | 0-100% | 72.92% (14.24%) |
| | Appropriate | Σ(follow at correct) | 0-5 | 1.07 (0.55) |
| | Overcompliance | Σ(follow at wrong) | 0-5 | 2.08 (0.65) |
| | Undercompliance | 5 - Appropriate | 0-5 | 3.93 (0.55) |
| **Decision Time** |
| | Overall mean | Σ(times)/10 | 5-30s | 13.23s (6.30s) |
| | Phase 1 | Σ(times 1-5)/5 | - | 11.72s (4.49s) |
| | Phase 2 | Σ(times 6-10)/5 | - | 14.71s (9.56s) |
| | Learning curve | Phase2 - Phase1 | - | +2.99s (7.15s) |
| **Agent Perception** |
| | Intelligence | Σ(5 items)/5 | 1-5 | 3.42 (0.85) |
| | Likeability | Σ(5 items)/5 | 1-5 | 3.76 (0.79) |
| | Animacy | Σ(5 items)/5 | 1-5 | 2.51 (0.76) |

---

## References

Bartneck, C., Kulić, D., Croft, E., & Zoghbi, S. (2009). Measurement instruments for the anthropomorphism, animacy, likeability, perceived intelligence, and perceived safety of robots. *International Journal of Social Robotics, 1*(1), 71-81.

Mayer, R. C., Davis, J. H., & Schoorman, F. D. (1995). An integrative model of organizational trust. *Academy of Management Review, 20*(3), 709-734.

Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors, 39*(2), 230-253.

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-12  
**For Questions**: Contact research team




