#!/usr/bin/env python3
"""
Study 1: Memory Function and Personality Matching Effects on Trust
Main Analysis Script

This script contains the core analysis for Study 1, examining how memory function
and personality matching between humans and AI agents influence trust development
in collaborative virtual reality environments.

Key Analyses:
1. Trust Development: Pre-post trust analysis and trust difference calculations
2. Behavioral Trust: Decision time analysis across phases and conditions
3. Compliance Analysis: Overall, appropriate, and overcompliance behaviors
4. Agent Perceptions: Multi-dimensional perception analysis
5. Learning Analysis: Performance improvement and learning curves
6. Qualitative Analysis: Text mining, sentiment analysis, and topic modeling

Usage:
    python main_analysis.py

Requirements:
    - task1_final.xlsx in data/ folder
    - pandas, numpy, scipy, matplotlib, seaborn, scikit-learn, nltk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    """Load and prepare the Study 1 dataset"""
    try:
        df = pd.read_excel('../data/task1_final.xlsx')
        print(f"✅ Loaded dataset with {len(df)} participants")
        print(f"📊 Dataset shape: {df.shape}")
        return df
    except FileNotFoundError:
        print("❌ Error: task1_final.xlsx not found in data/ folder")
        print("Please ensure the data file is in the correct location")
        return None

def calculate_trust_metrics(df):
    """Calculate key trust metrics"""
    print("\n🔍 Calculating Trust Metrics...")
    
    # Trust difference calculation
    df['trust_difference'] = df['trust_post'] - df['trust_pre']
    
    # Decision time metrics
    df['decision_time_phase1'] = df['decision_time_1'] + df['decision_time_2']
    df['decision_time_phase2'] = df['decision_time_3'] + df['decision_time_4'] + df['decision_time_5']
    
    # Compliance metrics
    df['overall_compliance'] = (df['follow_agent_1'] + df['follow_agent_2'] + 
                               df['follow_agent_3'] + df['follow_agent_4'] + df['follow_agent_5']) / 5
    
    print("✅ Trust metrics calculated")
    return df

def memory_function_analysis(df):
    """Analyze memory function effects on trust"""
    print("\n🧠 Memory Function Analysis...")
    
    # Group by memory function condition
    memory_groups = df.groupby('memory_function')
    
    results = {}
    for condition, group in memory_groups:
        print(f"\n📊 Memory Function: {condition}")
        print(f"   Trust Difference: M = {group['trust_difference'].mean():.2f}, SD = {group['trust_difference'].std():.2f}")
        print(f"   Post-task Trust: M = {group['trust_post'].mean():.2f}, SD = {group['trust_post'].std():.2f}")
        
        results[condition] = {
            'trust_difference': group['trust_difference'].mean(),
            'trust_post': group['trust_post'].mean(),
            'decision_time_phase1': group['decision_time_phase1'].mean(),
            'decision_time_phase2': group['decision_time_phase2'].mean(),
            'overall_compliance': group['overall_compliance'].mean()
        }
    
    # Statistical tests
    with_memory = df[df['memory_function'] == 'With Memory']
    without_memory = df[df['memory_function'] == 'Without Memory']
    
    # Trust difference t-test
    t_stat, p_val = ttest_ind(with_memory['trust_difference'], without_memory['trust_difference'])
    print(f"\n📈 Trust Difference t-test: t = {t_stat:.3f}, p = {p_val:.3f}")
    
    return results

def personality_matching_analysis(df):
    """Analyze personality matching effects on trust"""
    print("\n👥 Personality Matching Analysis...")
    
    # Group by personality matching condition
    matching_groups = df.groupby('personality_matching')
    
    results = {}
    for condition, group in matching_groups:
        print(f"\n📊 Personality Matching: {condition}")
        print(f"   Trust Difference: M = {group['trust_difference'].mean():.2f}, SD = {group['trust_difference'].std():.2f}")
        print(f"   Agent Likeability: M = {group['agent_likeability'].mean():.2f}, SD = {group['agent_likeability'].std():.2f}")
        
        results[condition] = {
            'trust_difference': group['trust_difference'].mean(),
            'trust_post': group['trust_post'].mean(),
            'agent_likeability': group['agent_likeability'].mean(),
            'agent_intelligence': group['agent_intelligence'].mean(),
            'overall_compliance': group['overall_compliance'].mean()
        }
    
    # Statistical tests
    matched = df[df['personality_matching'] == 'Matched']
    mismatched = df[df['personality_matching'] == 'Mismatched']
    
    # Trust difference t-test
    t_stat, p_val = ttest_ind(matched['trust_difference'], mismatched['trust_difference'])
    print(f"\n📈 Trust Difference t-test: t = {t_stat:.3f}, p = {p_val:.3f}")
    
    return results

def agent_perception_analysis(df):
    """Analyze agent perception effects"""
    print("\n🤖 Agent Perception Analysis...")
    
    # Group by agent personality
    agent_groups = df.groupby('agent_personality')
    
    results = {}
    for condition, group in agent_groups:
        print(f"\n📊 Agent Personality: {condition}")
        print(f"   Likeability: M = {group['agent_likeability'].mean():.2f}, SD = {group['agent_likeability'].std():.2f}")
        print(f"   Intelligence: M = {group['agent_intelligence'].mean():.2f}, SD = {group['agent_intelligence'].std():.2f}")
        
        results[condition] = {
            'likeability': group['agent_likeability'].mean(),
            'intelligence': group['agent_intelligence'].mean(),
            'anthropomorphism': group['agent_anthropomorphism'].mean(),
            'animacy': group['agent_animacy'].mean()
        }
    
    # Statistical tests
    extrovert = df[df['agent_personality'] == 'Extrovert']
    introvert = df[df['agent_personality'] == 'Introvert']
    
    # Likeability t-test
    t_stat, p_val = ttest_ind(extrovert['agent_likeability'], introvert['agent_likeability'])
    print(f"\n📈 Likeability t-test: t = {t_stat:.3f}, p = {p_val:.3f}")
    
    return results

def create_summary_plots(df):
    """Create summary visualization plots"""
    print("\n📊 Creating Summary Plots...")
    
    # Set up the plotting area
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Study 1: Memory Function and Personality Matching Effects on Trust', fontsize=16, fontweight='bold')
    
    # Plot 1: Trust Difference by Memory Function
    sns.boxplot(data=df, x='memory_function', y='trust_difference', ax=axes[0,0])
    axes[0,0].set_title('Trust Difference by Memory Function')
    axes[0,0].set_xlabel('Memory Function')
    axes[0,0].set_ylabel('Trust Difference (Post - Pre)')
    
    # Plot 2: Trust Difference by Personality Matching
    sns.boxplot(data=df, x='personality_matching', y='trust_difference', ax=axes[0,1])
    axes[0,1].set_title('Trust Difference by Personality Matching')
    axes[0,1].set_xlabel('Personality Matching')
    axes[0,1].set_ylabel('Trust Difference (Post - Pre)')
    
    # Plot 3: Agent Likeability by Agent Personality
    sns.boxplot(data=df, x='agent_personality', y='agent_likeability', ax=axes[1,0])
    axes[1,0].set_title('Agent Likeability by Agent Personality')
    axes[1,0].set_xlabel('Agent Personality')
    axes[1,0].set_ylabel('Agent Likeability Rating')
    
    # Plot 4: Decision Time by Phase and Memory Function
    memory_phase1 = df.groupby('memory_function')['decision_time_phase1'].mean()
    memory_phase2 = df.groupby('memory_function')['decision_time_phase2'].mean()
    
    x = np.arange(len(memory_phase1.index))
    width = 0.35
    
    axes[1,1].bar(x - width/2, memory_phase1.values, width, label='Phase 1', alpha=0.8)
    axes[1,1].bar(x + width/2, memory_phase2.values, width, label='Phase 2', alpha=0.8)
    axes[1,1].set_title('Decision Time by Memory Function and Phase')
    axes[1,1].set_xlabel('Memory Function')
    axes[1,1].set_ylabel('Decision Time (seconds)')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(memory_phase1.index, rotation=45)
    axes[1,1].legend()
    
    plt.tight_layout()
    plt.savefig('../results/figures_supplementary/Study1_Summary_Plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Summary plots created and saved")

def main():
    """Main analysis function"""
    print("🚀 Study 1: Memory Function and Personality Matching Effects on Trust")
    print("=" * 70)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Calculate trust metrics
    df = calculate_trust_metrics(df)
    
    # Run analyses
    memory_results = memory_function_analysis(df)
    personality_results = personality_matching_analysis(df)
    agent_results = agent_perception_analysis(df)
    
    # Create visualizations
    create_summary_plots(df)
    
    # Print summary
    print("\n" + "="*70)
    print("📋 ANALYSIS SUMMARY")
    print("="*70)
    print(f"📊 Total participants: {len(df)}")
    print(f"🧠 Memory function conditions: {df['memory_function'].nunique()}")
    print(f"👥 Personality matching conditions: {df['personality_matching'].nunique()}")
    print(f"🤖 Agent personality types: {df['agent_personality'].nunique()}")
    
    print("\n✅ Analysis complete! Check results/ folder for outputs.")
    print("\nNext steps:")
    print("  1. Review generated plots in results/figures_supplementary/")
    print("  2. Examine LaTeX manuscript files in results/manuscript/")
    print("  3. Run qualitative analysis script for text insights")

if __name__ == "__main__":
    main()

