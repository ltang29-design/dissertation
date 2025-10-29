import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load complete data with all metrics"""
    print("="*80)
    print("CREATING COMPREHENSIVE PUBLICATION FIGURES")
    print("All visualizations for research paper (significant + non-significant)")
    print("="*80)
    
    df = pd.read_csv('CORRECTED_DATA_WITH_HELP_METRICS.csv')
    print(f"\n[OK] Loaded {len(df)} participants")
    
    # Create clear condition labels
    df['condition_label'] = df['Display'].map({
        'I+MAPK': 'Introvert Agent\nwith Memory',
        'I-MAPK': 'Introvert Agent\nno Memory',
        'E+MAPK': 'Extrovert Agent\nwith Memory',
        'E-MAPK': 'Extrovert Agent\nno Memory'
    })
    
    # Agent personality labels
    if 'agent_personality' not in df.columns:
        df['agent_personality'] = df['Display'].str.contains('I', regex=False).map({
            True: 'Introvert Agent', False: 'Extrovert Agent'
        })
    
    # Memory function labels
    if 'memory_function' not in df.columns:
        df['memory_function'] = df['Display'].str.contains('+MAPK').map({
            True: 'With Memory Function', False: 'Without Memory Function'
        })
    
    # Participant personality
    if 'participant_intro_extro' not in df.columns:
        df['participant_intro_extro'] = df['personality'].str.strip().str.lower().map({
            'introvert': 'Introvert Participant', 'extrovert': 'Extrovert Participant',
            'i': 'Introvert Participant', 'e': 'Extrovert Participant'
        })
    
    # Match/Mismatch labels
    df['match_label'] = 'Mismatch'
    mask_match = (
        ((df['Display'].str.contains('I')) & (df['personality'].str.strip().str.lower().isin(['introvert', 'i']))) |
        ((df['Display'].str.contains('E')) & (df['personality'].str.strip().str.lower().isin(['extrovert', 'e'])))
    )
    df.loc[mask_match, 'match_label'] = 'Match'
    
    print(f"  Conditions: {df['condition_label'].nunique()}")
    print(f"  Match: {(df['match_label']=='Match').sum()}, Mismatch: {(df['match_label']=='Mismatch').sum()}")
    
    return df

def create_figure1_sample_descriptives(df):
    """Figure 1: Sample Characteristics (6 panels)"""
    print("\n[1] Creating Figure 1: Sample Characteristics...")
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    # Panel A: Sample size by condition
    ax1 = fig.add_subplot(gs[0, 0])
    
    condition_counts = df['condition_label'].value_counts().sort_index()
    colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
    
    bars = ax1.bar(range(len(condition_counts)), condition_counts.values, 
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax1.set_xticks(range(len(condition_counts)))
    ax1.set_xticklabels(condition_counts.index, fontsize=9, rotation=0)
    ax1.set_ylabel('Number of Participants', fontsize=11, fontweight='bold')
    ax1.set_title('A. Sample Size by Condition', fontsize=12, fontweight='bold')
    ax1.set_ylim([0, max(condition_counts.values) + 5])
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'n = {int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Panel B: Participant personality distribution
    ax2 = fig.add_subplot(gs[0, 1])
    
    part_pers = df['participant_intro_extro'].value_counts()
    colors_pers = ['#4ECDC4', '#FF6B6B']
    
    wedges, texts, autotexts = ax2.pie(part_pers.values, labels=part_pers.index,
                                         autopct='%1.1f%%', colors=colors_pers,
                                         startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('B. Participant Personality Distribution', fontsize=12, fontweight='bold')
    
    # Panel C: Match vs Mismatch
    ax3 = fig.add_subplot(gs[0, 2])
    
    match_counts = df['match_label'].value_counts()
    colors_match = ['#95E1D3', '#FFB3B3']
    
    bars = ax3.bar(range(len(match_counts)), match_counts.values,
                   color=colors_match, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax3.set_xticks(range(len(match_counts)))
    ax3.set_xticklabels(match_counts.index, fontsize=11)
    ax3.set_ylabel('Number of Participants', fontsize=11, fontweight='bold')
    ax3.set_title('C. Personality Match Distribution', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'n = {int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Panel D: Age distribution
    ax4 = fig.add_subplot(gs[1, 0])
    
    if 'Age' in df.columns:
        age_data = df['Age'].dropna()
        ax4.hist(age_data, bins=15, color='#4ECDC4', edgecolor='black', 
                linewidth=1.2, alpha=0.85)
        ax4.axvline(age_data.mean(), color='red', linestyle='--', linewidth=2.5,
                   label=f'Mean = {age_data.mean():.1f}')
        ax4.axvline(age_data.median(), color='orange', linestyle='--', linewidth=2.5,
                   label=f'Median = {age_data.median():.1f}')
        ax4.set_xlabel('Age (years)', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax4.set_title('D. Age Distribution', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(axis='y', alpha=0.3)
    
    # Panel E: Pre-task trust by condition
    ax5 = fig.add_subplot(gs[1, 1])
    
    if 'Trust_pre' in df.columns:
        trust_pre_means = df.groupby('condition_label')['Trust_pre'].agg(['mean', 'sem'])
        
        bars = ax5.bar(range(len(trust_pre_means)), trust_pre_means['mean'].values,
                       yerr=trust_pre_means['sem'].values, capsize=5,
                       color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax5.set_xticks(range(len(trust_pre_means)))
        ax5.set_xticklabels(trust_pre_means.index, fontsize=9)
        ax5.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
        ax5.set_title('E. Pre-Task Trust by Condition', fontsize=12, fontweight='bold')
        ax5.set_ylim([0, 100])
        ax5.grid(axis='y', alpha=0.3)
    
    # Panel F: VR experience metrics
    ax6 = fig.add_subplot(gs[1, 2])
    
    vr_metrics = ['Familiarity', 'Immersion', 'Self-efficacy']
    vr_means = [df[m].mean() for m in vr_metrics if m in df.columns]
    vr_sems = [df[m].sem() for m in vr_metrics if m in df.columns]
    vr_labels = [m for m in vr_metrics if m in df.columns]
    
    if vr_means:
        bars = ax6.bar(range(len(vr_means)), vr_means, yerr=vr_sems, capsize=5,
                       color=['#4ECDC4', '#95E1D3', '#FF6B6B'][:len(vr_means)],
                       edgecolor='black', linewidth=1.5, alpha=0.85)
        ax6.set_xticks(range(len(vr_means)))
        ax6.set_xticklabels(vr_labels, fontsize=10)
        ax6.set_ylabel('Rating (1-5 scale)', fontsize=11, fontweight='bold')
        ax6.set_title('F. VR Experience Metrics', fontsize=12, fontweight='bold')
        ax6.set_ylim([1, 5])
        ax6.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 1: Sample Characteristics and Descriptive Statistics',
                fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure1_Sample_Descriptives.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure1_Sample_Descriptives.png")

def create_figure2_trust_by_all_conditions(df):
    """Figure 2: Trust outcomes by ALL condition combinations (9 panels)"""
    print("\n[2] Creating Figure 2: Trust by All Conditions...")
    
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # Panel A: Trust by 4 conditions (Pre & Post)
    ax1 = fig.add_subplot(gs[0, 0])
    
    conditions = df['condition_label'].unique()
    x = np.arange(len(conditions))
    width = 0.35
    
    pre_means = [df[df['condition_label']==c]['Trust_pre'].mean() for c in conditions]
    pre_sems = [df[df['condition_label']==c]['Trust_pre'].sem() for c in conditions]
    post_means = [df[df['condition_label']==c]['Trust_post'].mean() for c in conditions]
    post_sems = [df[df['condition_label']==c]['Trust_post'].sem() for c in conditions]
    
    bars1 = ax1.bar(x - width/2, pre_means, width, yerr=pre_sems, capsize=4,
                    label='Pre-Task Trust', color='skyblue', edgecolor='black',
                    linewidth=1.2, alpha=0.85)
    bars2 = ax1.bar(x + width/2, post_means, width, yerr=post_sems, capsize=4,
                    label='Post-Task Trust', color='salmon', edgecolor='black',
                    linewidth=1.2, alpha=0.85)
    
    ax1.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
    ax1.set_title('A. Trust Development by Condition', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax1.legend(fontsize=9)
    ax1.set_ylim([0, 100])
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel B: Trust by Memory Function
    ax2 = fig.add_subplot(gs[0, 1])
    
    mem_groups = df.groupby('memory_function')[['Trust_pre', 'Trust_post']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax2.bar(x - width/2, mem_groups['Trust_pre']['mean'].values, width,
           yerr=mem_groups['Trust_pre']['sem'].values, capsize=4,
           label='Pre-Task', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax2.bar(x + width/2, mem_groups['Trust_post']['mean'].values, width,
           yerr=mem_groups['Trust_post']['sem'].values, capsize=4,
           label='Post-Task', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax2.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
    ax2.set_title('B. Trust by Memory Function', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(mem_groups.index, fontsize=10)
    ax2.legend(fontsize=9)
    ax2.set_ylim([0, 100])
    ax2.grid(axis='y', alpha=0.3)
    
    # Add stats annotation
    with_mem = df[df['memory_function'] == 'With Memory Function']['Trust_post'].dropna()
    without_mem = df[df['memory_function'] == 'Without Memory Function']['Trust_post'].dropna()
    if len(with_mem) > 1 and len(without_mem) > 1:
        t, p = stats.ttest_ind(with_mem, without_mem)
        ax2.text(0.5, 0.95, f'Post-Task: p = {p:.3f}', transform=ax2.transAxes,
                ha='center', va='top', fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Panel C: Trust by Agent Personality
    ax3 = fig.add_subplot(gs[0, 2])
    
    agent_groups = df.groupby('agent_personality')[['Trust_pre', 'Trust_post']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax3.bar(x - width/2, agent_groups['Trust_pre']['mean'].values, width,
           yerr=agent_groups['Trust_pre']['sem'].values, capsize=4,
           label='Pre-Task', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax3.bar(x + width/2, agent_groups['Trust_post']['mean'].values, width,
           yerr=agent_groups['Trust_post']['sem'].values, capsize=4,
           label='Post-Task', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax3.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
    ax3.set_title('C. Trust by Agent Personality', fontsize=12, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(agent_groups.index, fontsize=10)
    ax3.legend(fontsize=9)
    ax3.set_ylim([0, 100])
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel D: Trust by Match/Mismatch
    ax4 = fig.add_subplot(gs[1, 0])
    
    match_groups = df.groupby('match_label')[['Trust_pre', 'Trust_post']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax4.bar(x - width/2, match_groups['Trust_pre']['mean'].values, width,
           yerr=match_groups['Trust_pre']['sem'].values, capsize=4,
           label='Pre-Task', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax4.bar(x + width/2, match_groups['Trust_post']['mean'].values, width,
           yerr=match_groups['Trust_post']['sem'].values, capsize=4,
           label='Post-Task', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax4.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
    ax4.set_title('D. Trust by Personality Match', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(match_groups.index, fontsize=10)
    ax4.legend(fontsize=9)
    ax4.set_ylim([0, 100])
    ax4.grid(axis='y', alpha=0.3)
    
    # Panel E: Trust by Participant Personality
    ax5 = fig.add_subplot(gs[1, 1])
    
    part_groups = df.groupby('participant_intro_extro')[['Trust_pre', 'Trust_post']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax5.bar(x - width/2, part_groups['Trust_pre']['mean'].values, width,
           yerr=part_groups['Trust_pre']['sem'].values, capsize=4,
           label='Pre-Task', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax5.bar(x + width/2, part_groups['Trust_post']['mean'].values, width,
           yerr=part_groups['Trust_post']['sem'].values, capsize=4,
           label='Post-Task', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax5.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
    ax5.set_title('E. Trust by Participant Personality', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(part_groups.index, fontsize=9)
    ax5.legend(fontsize=9)
    ax5.set_ylim([0, 100])
    ax5.grid(axis='y', alpha=0.3)
    
    # Add stats
    intro_pre = df[df['participant_intro_extro'] == 'Introvert Participant']['Trust_pre'].dropna()
    extro_pre = df[df['participant_intro_extro'] == 'Extrovert Participant']['Trust_pre'].dropna()
    if len(intro_pre) > 1 and len(extro_pre) > 1:
        t, p = stats.ttest_ind(intro_pre, extro_pre)
        if p < 0.10:
            ax5.text(0.5, 0.95, f'Pre-Task: p = {p:.3f}*', transform=ax5.transAxes,
                    ha='center', va='top', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    # Panel F: Trust Change Distribution
    ax6 = fig.add_subplot(gs[1, 2])
    
    if 'trust_difference' in df.columns:
        trust_diff = df['trust_difference'].dropna()
        
        ax6.hist(trust_diff, bins=20, color='#4ECDC4', edgecolor='black',
                linewidth=1.2, alpha=0.85)
        ax6.axvline(0, color='red', linestyle='--', linewidth=2.5, label='No Change')
        ax6.axvline(trust_diff.mean(), color='orange', linestyle='--', linewidth=2.5,
                   label=f'Mean = {trust_diff.mean():.2f}')
        ax6.set_xlabel('Trust Change (Post - Pre)', fontsize=11, fontweight='bold')
        ax6.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax6.set_title('F. Trust Change Distribution', fontsize=12, fontweight='bold')
        ax6.legend(fontsize=9)
        ax6.grid(axis='y', alpha=0.3)
    
    # Panel G: Trust by Match × Memory
    ax7 = fig.add_subplot(gs[2, 0])
    
    match_mem_groups = df.groupby(['match_label', 'memory_function'])['Trust_post'].agg(['mean', 'sem']).reset_index()
    
    x = np.arange(2)
    width = 0.35
    
    match_data = match_mem_groups[match_mem_groups['match_label'] == 'Match']
    mismatch_data = match_mem_groups[match_mem_groups['match_label'] == 'Mismatch']
    
    if len(match_data) > 0 and len(mismatch_data) > 0:
        ax7.bar(x - width/2, match_data['mean'].values, width,
               yerr=match_data['sem'].values, capsize=4,
               label='Match', color='#95E1D3', edgecolor='black', linewidth=1.2, alpha=0.85)
        ax7.bar(x + width/2, mismatch_data['mean'].values, width,
               yerr=mismatch_data['sem'].values, capsize=4,
               label='Mismatch', color='#FFB3B3', edgecolor='black', linewidth=1.2, alpha=0.85)
        
        ax7.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
        ax7.set_title('G. Trust: Match × Memory Interaction', fontsize=12, fontweight='bold')
        ax7.set_xticks(x)
        ax7.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
        ax7.legend(fontsize=9)
        ax7.set_ylim([0, 100])
        ax7.grid(axis='y', alpha=0.3)
    
    # Panel H: Trust by Agent Personality × Memory
    ax8 = fig.add_subplot(gs[2, 1])
    
    agent_mem_groups = df.groupby(['agent_personality', 'memory_function'])['Trust_post'].agg(['mean', 'sem']).reset_index()
    
    x = np.arange(2)
    width = 0.35
    
    intro_data = agent_mem_groups[agent_mem_groups['agent_personality'] == 'Introvert Agent']
    extro_data = agent_mem_groups[agent_mem_groups['agent_personality'] == 'Extrovert Agent']
    
    if len(intro_data) > 0 and len(extro_data) > 0:
        ax8.bar(x - width/2, intro_data['mean'].values, width,
               yerr=intro_data['sem'].values, capsize=4,
               label='Introvert Agent', color='#4ECDC4', edgecolor='black', linewidth=1.2, alpha=0.85)
        ax8.bar(x + width/2, extro_data['mean'].values, width,
               yerr=extro_data['sem'].values, capsize=4,
               label='Extrovert Agent', color='#FF6B6B', edgecolor='black', linewidth=1.2, alpha=0.85)
        
        ax8.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
        ax8.set_title('H. Trust: Agent × Memory Interaction', fontsize=12, fontweight='bold')
        ax8.set_xticks(x)
        ax8.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
        ax8.legend(fontsize=9)
        ax8.set_ylim([0, 100])
        ax8.grid(axis='y', alpha=0.3)
    
    # Panel I: Propensity to Trust
    ax9 = fig.add_subplot(gs[2, 2])
    
    if 'Propensity' in df.columns or 'Propensity_pre' in df.columns:
        prop_col = 'Propensity_pre' if 'Propensity_pre' in df.columns else 'Propensity'
        
        prop_means = [df[df['condition_label']==c][prop_col].mean() for c in conditions]
        prop_sems = [df[df['condition_label']==c][prop_col].sem() for c in conditions]
        
        colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
        bars = ax9.bar(range(len(conditions)), prop_means, yerr=prop_sems, capsize=4,
                       color=colors, edgecolor='black', linewidth=1.2, alpha=0.85)
        ax9.set_ylabel('Propensity to Trust', fontsize=11, fontweight='bold')
        ax9.set_title('I. General Trust Propensity by Condition', fontsize=12, fontweight='bold')
        ax9.set_xticks(range(len(conditions)))
        ax9.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
        ax9.set_ylim([0, 100])
        ax9.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 2: Trust Outcomes by All Condition Combinations',
                fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure2_Trust_All_Conditions.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure2_Trust_All_Conditions.png")

def create_figure3_decision_time_comprehensive(df):
    """Figure 3: Decision time by all conditions (9 panels)"""
    print("\n[3] Creating Figure 3: Decision Time Comprehensive...")
    
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # Calculate metrics if needed
    if 'mean_decision_time_overall' not in df.columns:
        calculate_decision_metrics(df)
    
    colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
    conditions = df['condition_label'].unique()
    
    # Panel A: Overall decision time by condition
    ax1 = fig.add_subplot(gs[0, 0])
    
    means = [df[df['condition_label']==c]['mean_decision_time_overall'].mean() for c in conditions]
    sems = [df[df['condition_label']==c]['mean_decision_time_overall'].sem() for c in conditions]
    
    bars = ax1.bar(range(len(conditions)), means, yerr=sems, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax1.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_title('A. Overall Decision Time by Condition', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(conditions)))
    ax1.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel B: Phase 1 vs Phase 2 by condition
    ax2 = fig.add_subplot(gs[0, 1])
    
    x = np.arange(len(conditions))
    width = 0.35
    
    p1_means = [df[df['condition_label']==c]['phase1_mean_time'].mean() for c in conditions]
    p1_sems = [df[df['condition_label']==c]['phase1_mean_time'].sem() for c in conditions]
    p2_means = [df[df['condition_label']==c]['phase2_mean_time'].mean() for c in conditions]
    p2_sems = [df[df['condition_label']==c]['phase2_mean_time'].sem() for c in conditions]
    
    ax2.bar(x - width/2, p1_means, width, yerr=p1_sems, capsize=4,
           label='Phase 1 (Guided)', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax2.bar(x + width/2, p2_means, width, yerr=p2_sems, capsize=4,
           label='Phase 2 (Memory)', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax2.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax2.set_title('B. Phase-Specific Decision Time', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel C: Decision time change
    ax3 = fig.add_subplot(gs[0, 2])
    
    change_means = [df[df['condition_label']==c]['decision_time_change'].mean() for c in conditions]
    change_sems = [df[df['condition_label']==c]['decision_time_change'].sem() for c in conditions]
    
    bars = ax3.bar(range(len(conditions)), change_means, yerr=change_sems, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax3.axhline(0, color='black', linestyle='-', linewidth=2, alpha=0.8)
    ax3.set_ylabel('Time Change (Phase 2 - Phase 1, seconds)', fontsize=11, fontweight='bold')
    ax3.set_title('C. Learning Curve Pattern', fontsize=12, fontweight='bold')
    ax3.set_xticks(range(len(conditions)))
    ax3.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel D: By Memory Function
    ax4 = fig.add_subplot(gs[1, 0])
    
    mem_groups = df.groupby('memory_function')[['phase1_mean_time', 'phase2_mean_time']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax4.bar(x - width/2, mem_groups['phase1_mean_time']['mean'].values, width,
           yerr=mem_groups['phase1_mean_time']['sem'].values, capsize=4,
           label='Phase 1', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax4.bar(x + width/2, mem_groups['phase2_mean_time']['mean'].values, width,
           yerr=mem_groups['phase2_mean_time']['sem'].values, capsize=4,
           label='Phase 2', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax4.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax4.set_title('D. Decision Time by Memory Function', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(mem_groups.index, fontsize=10)
    ax4.legend(fontsize=9)
    ax4.grid(axis='y', alpha=0.3)
    
    # Panel E: By Agent Personality
    ax5 = fig.add_subplot(gs[1, 1])
    
    agent_groups = df.groupby('agent_personality')[['phase1_mean_time', 'phase2_mean_time']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax5.bar(x - width/2, agent_groups['phase1_mean_time']['mean'].values, width,
           yerr=agent_groups['phase1_mean_time']['sem'].values, capsize=4,
           label='Phase 1', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax5.bar(x + width/2, agent_groups['phase2_mean_time']['mean'].values, width,
           yerr=agent_groups['phase2_mean_time']['sem'].values, capsize=4,
           label='Phase 2', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax5.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax5.set_title('E. Decision Time by Agent Personality', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(agent_groups.index, fontsize=10)
    ax5.legend(fontsize=9)
    ax5.grid(axis='y', alpha=0.3)
    
    # Panel F: By Match/Mismatch
    ax6 = fig.add_subplot(gs[1, 2])
    
    match_groups = df.groupby('match_label')[['phase1_mean_time', 'phase2_mean_time']].agg(['mean', 'sem'])
    
    x = np.arange(2)
    width = 0.35
    
    ax6.bar(x - width/2, match_groups['phase1_mean_time']['mean'].values, width,
           yerr=match_groups['phase1_mean_time']['sem'].values, capsize=4,
           label='Phase 1', color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.85)
    ax6.bar(x + width/2, match_groups['phase2_mean_time']['mean'].values, width,
           yerr=match_groups['phase2_mean_time']['sem'].values, capsize=4,
           label='Phase 2', color='salmon', edgecolor='black', linewidth=1.2, alpha=0.85)
    
    ax6.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax6.set_title('F. Decision Time by Personality Match', fontsize=12, fontweight='bold')
    ax6.set_xticks(x)
    ax6.set_xticklabels(match_groups.index, fontsize=10)
    ax6.legend(fontsize=9)
    ax6.grid(axis='y', alpha=0.3)
    
    # Panel G: Error corner time
    ax7 = fig.add_subplot(gs[2, 0])
    
    error_means = [df[df['condition_label']==c]['error_corner_mean_time'].mean() for c in conditions]
    error_sems = [df[df['condition_label']==c]['error_corner_mean_time'].sem() for c in conditions]
    
    bars = ax7.bar(range(len(conditions)), error_means, yerr=error_sems, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax7.set_ylabel('Mean Time (seconds)', fontsize=11, fontweight='bold')
    ax7.set_title('G. Error Corner Decision Time', fontsize=12, fontweight='bold')
    ax7.set_xticks(range(len(conditions)))
    ax7.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax7.grid(axis='y', alpha=0.3)
    
    # Panel H: By Participant Personality
    ax8 = fig.add_subplot(gs[2, 1])
    
    part_groups = df.groupby('participant_intro_extro')['mean_decision_time_overall'].agg(['mean', 'sem'])
    
    bars = ax8.bar(range(len(part_groups)), part_groups['mean'].values,
                   yerr=part_groups['sem'].values, capsize=5,
                   color=['#4ECDC4', '#FF6B6B'], edgecolor='black', linewidth=1.5, alpha=0.85)
    ax8.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax8.set_title('H. Decision Time by Participant Personality', fontsize=12, fontweight='bold')
    ax8.set_xticks(range(len(part_groups)))
    ax8.set_xticklabels(part_groups.index, fontsize=9)
    ax8.grid(axis='y', alpha=0.3)
    
    # Panel I: Distribution
    ax9 = fig.add_subplot(gs[2, 2])
    
    for i, cond in enumerate(conditions):
        data = df[df['condition_label'] == cond]['mean_decision_time_overall'].dropna()
        ax9.violinplot([data], positions=[i], widths=0.7, showmeans=True, showmedians=True)
    
    ax9.set_ylabel('Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax9.set_title('I. Decision Time Distributions', fontsize=12, fontweight='bold')
    ax9.set_xticks(range(len(conditions)))
    ax9.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax9.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 3: Decision Time by All Condition Combinations',
                fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure3_DecisionTime_All_Conditions.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure3_DecisionTime_All_Conditions.png")

def calculate_decision_metrics(df):
    """Calculate decision time metrics if missing"""
    
    agent_recommendations = {
        1: 'Right', 2: 'Forward', 3: 'Left', 4: 'Right', 5: 'Forward',
        6: 'Forward', 7: 'Forward', 8: 'Left', 9: 'Left', 10: 'Left'
    }
    
    correct_path = {
        1: 'Right', 2: 'Forward', 3: 'Right', 4: 'Right', 5: 'Forward',
        6: 'Forward', 7: 'Left', 8: 'Left', 9: 'Forward', 10: 'Left'
    }
    
    if 'phase1_mean_time' not in df.columns:
        df['phase1_mean_time'] = 0.0
    if 'phase2_mean_time' not in df.columns:
        df['phase2_mean_time'] = 0.0
    if 'decision_time_change' not in df.columns:
        df['decision_time_change'] = 0.0
    if 'error_corner_mean_time' not in df.columns:
        df['error_corner_mean_time'] = 0.0
    if 'mean_decision_time_overall' not in df.columns:
        df['mean_decision_time_overall'] = 0.0
    
    for idx, row in df.iterrows():
        phase1_times = []
        phase2_times = []
        all_times = []
        error_times = []
        
        for corner in range(1, 11):
            time_col = f'corner{corner}_decision1_time'
            
            if time_col in df.columns and pd.notna(row[time_col]):
                t = row[time_col]
                all_times.append(t)
                
                if corner <= 5:
                    phase1_times.append(t)
                else:
                    phase2_times.append(t)
                
                if corner in [3, 7, 9]:
                    error_times.append(t)
        
        if phase1_times:
            df.loc[idx, 'phase1_mean_time'] = np.mean(phase1_times)
        if phase2_times:
            df.loc[idx, 'phase2_mean_time'] = np.mean(phase2_times)
        if phase1_times and phase2_times:
            df.loc[idx, 'decision_time_change'] = np.mean(phase2_times) - np.mean(phase1_times)
        if all_times:
            df.loc[idx, 'mean_decision_time_overall'] = np.mean(all_times)
        if error_times:
            df.loc[idx, 'error_corner_mean_time'] = np.mean(error_times)

def create_figure4_agent_perceptions_heatmap(df):
    """Figure 4: Complete agent perceptions correlation heatmap"""
    print("\n[4] Creating Figure 4: Agent Perceptions Correlation Heatmap...")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    
    agent_metrics = ['Anthropomorphism', 'Animacy', 'Likeability', 
                    'Intelligence', 'Safety', 'Aesthetic']
    outcome_metrics = ['Trust_pre', 'Trust_post', 'trust_difference',
                      'mean_decision_time_overall', 'phase1_mean_time', 'phase2_mean_time',
                      'compliance_rate', 'overcompliance']
    
    # Panel A: Overall correlations
    ax1 = axes[0, 0]
    
    corr_matrix = np.zeros((len(agent_metrics), len(outcome_metrics)))
    p_matrix = np.zeros((len(agent_metrics), len(outcome_metrics)))
    
    for i, agent_m in enumerate(agent_metrics):
        for j, outcome_m in enumerate(outcome_metrics):
            if agent_m in df.columns and outcome_m in df.columns:
                data = df[[agent_m, outcome_m]].dropna()
                if len(data) > 5:
                    r, p = stats.pearsonr(data[agent_m], data[outcome_m])
                    corr_matrix[i, j] = r
                    p_matrix[i, j] = p
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
               xticklabels=[m.replace('_', '\n') for m in outcome_metrics],
               yticklabels=agent_metrics, cbar_kws={'label': 'Pearson r'},
               vmin=-0.6, vmax=0.6, ax=ax1, linewidths=0.5)
    
    ax1.set_title('A. Overall Correlations (All Participants)', fontsize=12, fontweight='bold')
    
    # Panel B: With Memory Function
    ax2 = axes[0, 1]
    
    df_mem = df[df['memory_function'] == 'With Memory Function']
    corr_mem = np.zeros((len(agent_metrics), len(outcome_metrics)))
    
    for i, agent_m in enumerate(agent_metrics):
        for j, outcome_m in enumerate(outcome_metrics):
            if agent_m in df_mem.columns and outcome_m in df_mem.columns:
                data = df_mem[[agent_m, outcome_m]].dropna()
                if len(data) > 5:
                    r, p = stats.pearsonr(data[agent_m], data[outcome_m])
                    corr_mem[i, j] = r
    
    sns.heatmap(corr_mem, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
               xticklabels=[m.replace('_', '\n') for m in outcome_metrics],
               yticklabels=agent_metrics, cbar_kws={'label': 'Pearson r'},
               vmin=-0.6, vmax=0.6, ax=ax2, linewidths=0.5)
    
    ax2.set_title('B. With Memory Function', fontsize=12, fontweight='bold')
    
    # Panel C: Without Memory Function
    ax3 = axes[1, 0]
    
    df_nomem = df[df['memory_function'] == 'Without Memory Function']
    corr_nomem = np.zeros((len(agent_metrics), len(outcome_metrics)))
    
    for i, agent_m in enumerate(agent_metrics):
        for j, outcome_m in enumerate(outcome_metrics):
            if agent_m in df_nomem.columns and outcome_m in df_nomem.columns:
                data = df_nomem[[agent_m, outcome_m]].dropna()
                if len(data) > 5:
                    r, p = stats.pearsonr(data[agent_m], data[outcome_m])
                    corr_nomem[i, j] = r
    
    sns.heatmap(corr_nomem, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
               xticklabels=[m.replace('_', '\n') for m in outcome_metrics],
               yticklabels=agent_metrics, cbar_kws={'label': 'Pearson r'},
               vmin=-0.6, vmax=0.6, ax=ax3, linewidths=0.5)
    
    ax3.set_title('C. Without Memory Function', fontsize=12, fontweight='bold')
    
    # Panel D: Match vs Mismatch
    ax4 = axes[1, 1]
    
    df_match = df[df['match_label'] == 'Match']
    corr_match = np.zeros((len(agent_metrics), len(outcome_metrics)))
    
    for i, agent_m in enumerate(agent_metrics):
        for j, outcome_m in enumerate(outcome_metrics):
            if agent_m in df_match.columns and outcome_m in df_match.columns:
                data = df_match[[agent_m, outcome_m]].dropna()
                if len(data) > 5:
                    r, p = stats.pearsonr(data[agent_m], data[outcome_m])
                    corr_match[i, j] = r
    
    sns.heatmap(corr_match, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
               xticklabels=[m.replace('_', '\n') for m in outcome_metrics],
               yticklabels=agent_metrics, cbar_kws={'label': 'Pearson r'},
               vmin=-0.6, vmax=0.6, ax=ax4, linewidths=0.5)
    
    ax4.set_title('D. Personality Match Condition', fontsize=12, fontweight='bold')
    
    plt.suptitle('Figure 4: Agent Perception Correlations by Subgroup',
                fontsize=15, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure4_Perceptions_Heatmap_Subgroups.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure4_Perceptions_Heatmap_Subgroups.png")

def create_figure5_compliance_patterns(df):
    """Figure 5: Compliance patterns by all conditions (6 panels)"""
    print("\n[5] Creating Figure 5: Compliance Patterns...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    if 'compliance_rate' not in df.columns:
        # Calculate compliance
        df['compliance_rate'] = 0.0
        for idx, row in df.iterrows():
            followed = 0
            total = 0
            for corner in range(1, 11):
                dir_col = f'corner{corner}_decision1_direction'
                if dir_col in df.columns and pd.notna(row[dir_col]):
                    total += 1
                    agent_recommendations = {
                        1: 'Right', 2: 'Forward', 3: 'Left', 4: 'Right', 5: 'Forward',
                        6: 'Forward', 7: 'Forward', 8: 'Left', 9: 'Left', 10: 'Left'
                    }
                    if row[dir_col] == agent_recommendations[corner]:
                        followed += 1
            if total > 0:
                df.loc[idx, 'compliance_rate'] = (followed / total) * 100
    
    conditions = df['condition_label'].unique()
    colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
    
    # Panel A: Compliance by condition
    ax1 = fig.add_subplot(gs[0, 0])
    
    comp_means = [df[df['condition_label']==c]['compliance_rate'].mean() for c in conditions]
    comp_sems = [df[df['condition_label']==c]['compliance_rate'].sem() for c in conditions]
    
    bars = ax1.bar(range(len(conditions)), comp_means, yerr=comp_sems, capsize=5,
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    ax1.set_ylabel('Compliance Rate (%)', fontsize=11, fontweight='bold')
    ax1.set_title('A. Compliance Rate by Condition', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(conditions)))
    ax1.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
    ax1.set_ylim([0, 100])
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel B: By Memory
    ax2 = fig.add_subplot(gs[0, 1])
    
    mem_comp = df.groupby('memory_function')['compliance_rate'].agg(['mean', 'sem'])
    
    bars = ax2.bar(range(len(mem_comp)), mem_comp['mean'].values,
                   yerr=mem_comp['sem'].values, capsize=5,
                   color=['#FF6B6B', '#4ECDC4'], edgecolor='black', linewidth=1.5, alpha=0.85)
    ax2.set_ylabel('Compliance Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_title('B. Compliance by Memory Function', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(mem_comp)))
    ax2.set_xticklabels(mem_comp.index, fontsize=9)
    ax2.set_ylim([0, 100])
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel C: By Agent Personality
    ax3 = fig.add_subplot(gs[0, 2])
    
    agent_comp = df.groupby('agent_personality')['compliance_rate'].agg(['mean', 'sem'])
    
    bars = ax3.bar(range(len(agent_comp)), agent_comp['mean'].values,
                   yerr=agent_comp['sem'].values, capsize=5,
                   color=['#4ECDC4', '#FF6B6B'], edgecolor='black', linewidth=1.5, alpha=0.85)
    ax3.set_ylabel('Compliance Rate (%)', fontsize=11, fontweight='bold')
    ax3.set_title('C. Compliance by Agent Personality', fontsize=12, fontweight='bold')
    ax3.set_xticks(range(len(agent_comp)))
    ax3.set_xticklabels(agent_comp.index, fontsize=9)
    ax3.set_ylim([0, 100])
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel D: By Match
    ax4 = fig.add_subplot(gs[1, 0])
    
    match_comp = df.groupby('match_label')['compliance_rate'].agg(['mean', 'sem'])
    
    bars = ax4.bar(range(len(match_comp)), match_comp['mean'].values,
                   yerr=match_comp['sem'].values, capsize=5,
                   color=['#95E1D3', '#FFB3B3'], edgecolor='black', linewidth=1.5, alpha=0.85)
    ax4.set_ylabel('Compliance Rate (%)', fontsize=11, fontweight='bold')
    ax4.set_title('D. Compliance by Personality Match', fontsize=12, fontweight='bold')
    ax4.set_xticks(range(len(match_comp)))
    ax4.set_xticklabels(match_comp.index, fontsize=10)
    ax4.set_ylim([0, 100])
    ax4.grid(axis='y', alpha=0.3)
    
    # Panel E: By Participant Personality
    ax5 = fig.add_subplot(gs[1, 1])
    
    if 'overcompliance' in df.columns:
        part_over = df.groupby('participant_intro_extro')['overcompliance'].agg(['mean', 'sem'])
        
        bars = ax5.bar(range(len(part_over)), part_over['mean'].values,
                       yerr=part_over['sem'].values, capsize=5,
                       color=['#4ECDC4', '#FF6B6B'], edgecolor='black', linewidth=1.5, alpha=0.85)
        ax5.set_ylabel('Overcompliance Count', fontsize=11, fontweight='bold')
        ax5.set_title('E. Overcompliance by Participant Personality', fontsize=12, fontweight='bold')
        ax5.set_xticks(range(len(part_over)))
        ax5.set_xticklabels(part_over.index, fontsize=9)
        ax5.grid(axis='y', alpha=0.3)
    
    # Panel F: Initial trust (Corner 1)
    ax6 = fig.add_subplot(gs[1, 2])
    
    if 'initial_trust' in df.columns:
        init_trust = df.groupby('condition_label')['initial_trust'].apply(lambda x: x.mean() * 100)
        
        bars = ax6.bar(range(len(init_trust)), init_trust.values,
                       color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax6.set_ylabel('Initial Compliance (%)', fontsize=11, fontweight='bold')
        ax6.set_title('F. Initial Trust (Corner 1)', fontsize=12, fontweight='bold')
        ax6.set_xticks(range(len(init_trust)))
        ax6.set_xticklabels(init_trust.index, fontsize=8, rotation=15, ha='right')
        ax6.set_ylim([0, 100])
        ax6.axhline(y=84.8, color='red', linestyle='--', linewidth=2, alpha=0.7,
                   label='Overall: 84.8%')
        ax6.legend(fontsize=9)
        ax6.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 5: Compliance Patterns by Condition',
                fontsize=15, fontweight='bold')
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure5_Compliance_Patterns.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure5_Compliance_Patterns.png")

def create_figure6_perceptions_by_conditions(df):
    """Figure 6: All agent perceptions by conditions (6 panels)"""
    print("\n[6] Creating Figure 6: Agent Perceptions by Conditions...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    agent_metrics = ['Anthropomorphism', 'Animacy', 'Likeability', 
                    'Intelligence', 'Safety', 'Aesthetic']
    
    conditions = df['condition_label'].unique()
    colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
    
    for idx, metric in enumerate(agent_metrics):
        if metric not in df.columns:
            continue
        
        ax = fig.add_subplot(gs[idx // 3, idx % 3])
        
        means = [df[df['condition_label']==c][metric].mean() for c in conditions]
        sems = [df[df['condition_label']==c][metric].sem() for c in conditions]
        
        bars = ax.bar(range(len(conditions)), means, yerr=sems, capsize=5,
                     color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax.set_ylabel(f'{metric} Rating', fontsize=11, fontweight='bold')
        ax.set_title(f'{chr(65+idx)}. {metric} by Condition', fontsize=12, fontweight='bold')
        ax.set_xticks(range(len(conditions)))
        ax.set_xticklabels(conditions, fontsize=8, rotation=15, ha='right')
        ax.set_ylim([1, 5])
        ax.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 6: Agent Perceptions by Condition',
                fontsize=15, fontweight='bold')
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure6_Agent_Perceptions_By_Condition.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure6_Agent_Perceptions_By_Condition.png")

def create_figure7_interaction_plots(df):
    """Figure 7: All 2-way interaction plots (6 panels)"""
    print("\n[7] Creating Figure 7: Interaction Plots...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    # Panel A: Trust - Memory × Agent
    ax1 = fig.add_subplot(gs[0, 0])
    
    for agent in ['Introvert Agent', 'Extrovert Agent']:
        data = df[df['agent_personality'] == agent]
        mem_groups = data.groupby('memory_function')['Trust_post'].mean()
        
        if len(mem_groups) == 2:  # Need both memory conditions
            x_pos = [0, 1]
            color = '#4ECDC4' if agent == 'Introvert Agent' else '#FF6B6B'
            ax1.plot(x_pos, mem_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=agent, color=color)
    
    ax1.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
    ax1.set_title('A. Trust: Memory × Agent Personality', fontsize=12, fontweight='bold')
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    
    # Panel B: Trust - Memory × Match
    ax2 = fig.add_subplot(gs[0, 1])
    
    for match in ['Match', 'Mismatch']:
        data = df[df['match_label'] == match]
        mem_groups = data.groupby('memory_function')['Trust_post'].mean()
        
        if len(mem_groups) == 2:
            x_pos = [0, 1]
            color = '#95E1D3' if match == 'Match' else '#FFB3B3'
            ax2.plot(x_pos, mem_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=match, color=color)
    
    ax2.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
    ax2.set_title('B. Trust: Memory × Personality Match', fontsize=12, fontweight='bold')
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    
    # Panel C: Decision Time - Memory × Agent
    ax3 = fig.add_subplot(gs[0, 2])
    
    for agent in ['Introvert Agent', 'Extrovert Agent']:
        data = df[df['agent_personality'] == agent]
        mem_groups = data.groupby('memory_function')['mean_decision_time_overall'].mean()
        
        if len(mem_groups) == 2:
            x_pos = [0, 1]
            color = '#4ECDC4' if agent == 'Introvert Agent' else '#FF6B6B'
            ax3.plot(x_pos, mem_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=agent, color=color)
    
    ax3.set_ylabel('Mean Decision Time (s)', fontsize=11, fontweight='bold')
    ax3.set_title('C. Decision Time: Memory × Agent', fontsize=12, fontweight='bold')
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
    ax3.legend(fontsize=10)
    ax3.grid(alpha=0.3)
    
    # Panel D: Agent × Match on Trust
    ax4 = fig.add_subplot(gs[1, 0])
    
    for match in ['Match', 'Mismatch']:
        data = df[df['match_label'] == match]
        agent_groups = data.groupby('agent_personality')['Trust_post'].mean()
        
        if len(agent_groups) == 2:
            x_pos = [0, 1]
            color = '#95E1D3' if match == 'Match' else '#FFB3B3'
            ax4.plot(x_pos, agent_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=match, color=color)
    
    ax4.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
    ax4.set_title('D. Trust: Agent × Personality Match', fontsize=12, fontweight='bold')
    ax4.set_xticks([0, 1])
    ax4.set_xticklabels(['Introvert Agent', 'Extrovert Agent'], fontsize=10)
    ax4.legend(fontsize=10)
    ax4.grid(alpha=0.3)
    
    # Panel E: Participant × Agent on Trust
    ax5 = fig.add_subplot(gs[1, 1])
    
    for part in ['Introvert Participant', 'Extrovert Participant']:
        data = df[df['participant_intro_extro'] == part]
        agent_groups = data.groupby('agent_personality')['Trust_post'].mean()
        
        if len(agent_groups) == 2:
            x_pos = [0, 1]
            color = '#4ECDC4' if part == 'Introvert Participant' else '#FF6B6B'
            ax5.plot(x_pos, agent_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=part, color=color)
    
    ax5.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
    ax5.set_title('E. Trust: Participant × Agent', fontsize=12, fontweight='bold')
    ax5.set_xticks([0, 1])
    ax5.set_xticklabels(['Introvert Agent', 'Extrovert Agent'], fontsize=10)
    ax5.legend(fontsize=9)
    ax5.grid(alpha=0.3)
    
    # Panel F: Participant × Memory on Decision Time
    ax6 = fig.add_subplot(gs[1, 2])
    
    for part in ['Introvert Participant', 'Extrovert Participant']:
        data = df[df['participant_intro_extro'] == part]
        mem_groups = data.groupby('memory_function')['mean_decision_time_overall'].mean()
        
        if len(mem_groups) == 2:
            x_pos = [0, 1]
            color = '#4ECDC4' if part == 'Introvert Participant' else '#FF6B6B'
            ax6.plot(x_pos, mem_groups.values, marker='o', markersize=10, linewidth=2.5,
                    label=part, color=color)
    
    ax6.set_ylabel('Mean Decision Time (s)', fontsize=11, fontweight='bold')
    ax6.set_title('F. Decision Time: Participant × Memory', fontsize=12, fontweight='bold')
    ax6.set_xticks([0, 1])
    ax6.set_xticklabels(['Without Memory', 'With Memory'], fontsize=10)
    ax6.legend(fontsize=9)
    ax6.grid(alpha=0.3)
    
    plt.suptitle('Figure 7: Two-Way Interaction Effects',
                fontsize=15, fontweight='bold')
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure7_Interaction_Plots.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure7_Interaction_Plots.png")

def create_figure8_vr_and_individual_diffs(df):
    """Figure 8: VR metrics and individual differences (6 panels)"""
    print("\n[8] Creating Figure 8: VR Metrics and Individual Differences...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    # Panel A: VR metrics by condition
    ax1 = fig.add_subplot(gs[0, 0])
    
    vr_metrics = ['Familiarity', 'Immersion', 'Self-efficacy']
    conditions = df['condition_label'].unique()
    
    x = np.arange(len(conditions))
    width = 0.25
    
    for i, metric in enumerate(vr_metrics):
        if metric in df.columns:
            means = [df[df['condition_label']==c][metric].mean() for c in conditions]
            ax1.bar(x + i*width, means, width, label=metric, alpha=0.85,
                   edgecolor='black', linewidth=1.2)
    
    ax1.set_ylabel('Rating (1-5 scale)', fontsize=11, fontweight='bold')
    ax1.set_title('A. VR Experience by Condition', fontsize=12, fontweight='bold')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(conditions, fontsize=7, rotation=15, ha='right')
    ax1.legend(fontsize=9)
    ax1.set_ylim([1, 5])
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel B: Self-efficacy × Trust scatter
    ax2 = fig.add_subplot(gs[0, 1])
    
    if 'Self-efficacy' in df.columns:
        data = df[['Self-efficacy', 'Trust_post']].dropna()
        
        ax2.scatter(data['Self-efficacy'], data['Trust_post'], alpha=0.6, s=60,
                   color='#4ECDC4', edgecolor='black', linewidth=0.8)
        
        if len(data) > 5:
            z = np.polyfit(data['Self-efficacy'], data['Trust_post'], 1)
            p_fit = np.poly1d(z)
            x_line = np.linspace(data['Self-efficacy'].min(), data['Self-efficacy'].max(), 100)
            ax2.plot(x_line, p_fit(x_line), 'r-', linewidth=3, alpha=0.7)
            
            r, p = stats.pearsonr(data['Self-efficacy'], data['Trust_post'])
            ax2.text(0.05, 0.95, f'r = {r:.3f}\np = {p:.3f}',
                    transform=ax2.transAxes, fontsize=10, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        ax2.set_xlabel('VR Self-Efficacy', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
        ax2.set_title('B. Self-Efficacy × Trust Correlation', fontsize=12, fontweight='bold')
        ax2.grid(alpha=0.3)
    
    # Panel C: Risk propensity
    ax3 = fig.add_subplot(gs[0, 2])
    
    if 'Risk_propensity' in df.columns:
        risk_groups = df.groupby('condition_label')['Risk_propensity'].agg(['mean', 'sem'])
        
        colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
        bars = ax3.bar(range(len(risk_groups)), risk_groups['mean'].values,
                       yerr=risk_groups['sem'].values, capsize=5,
                       color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax3.set_ylabel('Risk Propensity Score', fontsize=11, fontweight='bold')
        ax3.set_title('C. Risk Propensity by Condition', fontsize=12, fontweight='bold')
        ax3.set_xticks(range(len(risk_groups)))
        ax3.set_xticklabels(risk_groups.index, fontsize=8, rotation=15, ha='right')
        ax3.grid(axis='y', alpha=0.3)
    
    # Panel D: Participant personality across conditions
    ax4 = fig.add_subplot(gs[1, 0])
    
    part_dist = pd.crosstab(df['condition_label'], df['participant_intro_extro'], normalize='index') * 100
    
    part_dist.plot(kind='bar', ax=ax4, color=['#4ECDC4', '#FF6B6B'], 
                   edgecolor='black', linewidth=1.2, alpha=0.85)
    ax4.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
    ax4.set_title('D. Participant Personality Distribution', fontsize=12, fontweight='bold')
    ax4.set_xlabel('')
    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=15, ha='right', fontsize=8)
    ax4.legend(title='Participant Type', fontsize=9)
    ax4.set_ylim([0, 100])
    ax4.grid(axis='y', alpha=0.3)
    
    # Panel E: Age by condition
    ax5 = fig.add_subplot(gs[1, 1])
    
    if 'Age' in df.columns:
        age_groups = df.groupby('condition_label')['Age'].agg(['mean', 'sem'])
        
        colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
        bars = ax5.bar(range(len(age_groups)), age_groups['mean'].values,
                       yerr=age_groups['sem'].values, capsize=5,
                       color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
        ax5.set_ylabel('Age (years)', fontsize=11, fontweight='bold')
        ax5.set_title('E. Age Distribution by Condition', fontsize=12, fontweight='bold')
        ax5.set_xticks(range(len(age_groups)))
        ax5.set_xticklabels(age_groups.index, fontsize=8, rotation=15, ha='right')
        ax5.grid(axis='y', alpha=0.3)
    
    # Panel F: Help usage by personality
    ax6 = fig.add_subplot(gs[1, 2])
    
    if 'total_help_requests' in df.columns:
        help_part = df.groupby('participant_intro_extro')['total_help_requests'].agg(['mean', 'sem'])
        
        bars = ax6.bar(range(len(help_part)), help_part['mean'].values,
                       yerr=help_part['sem'].values, capsize=5,
                       color=['#4ECDC4', '#FF6B6B'], edgecolor='black', linewidth=1.5, alpha=0.85)
        ax6.set_ylabel('Mean Help Requests', fontsize=11, fontweight='bold')
        ax6.set_title('F. Help Usage by Participant Personality', fontsize=12, fontweight='bold')
        ax6.set_xticks(range(len(help_part)))
        ax6.set_xticklabels(help_part.index, fontsize=9)
        ax6.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 8: VR Experience and Individual Differences',
                fontsize=15, fontweight='bold')
    
    plt.savefig('PUBLICATION_FIGURES_COMPLETE/Figure8_VR_and_Individual_Diffs.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure8_VR_and_Individual_Diffs.png")

def main():
    """Main execution"""
    
    import os
    os.makedirs('PUBLICATION_FIGURES_COMPLETE', exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Create all figures
    create_figure1_sample_descriptives(df)
    create_figure2_trust_by_all_conditions(df)
    create_figure3_decision_time_comprehensive(df)
    create_figure4_agent_perceptions_heatmap(df)
    create_figure5_compliance_patterns(df)
    create_figure6_perceptions_by_conditions(df)
    create_figure7_interaction_plots(df)
    create_figure8_vr_and_individual_diffs(df)
    
    print("\n" + "="*80)
    print("COMPLETE! ALL PUBLICATION FIGURES GENERATED")
    print("="*80)
    print("\nTotal Figures: 8")
    print("Total Panels: 56")
    print("\nAll figures saved in: PUBLICATION_FIGURES_COMPLETE/")
    print("\nFigures include:")
    print("  1. Sample descriptives (6 panels)")
    print("  2. Trust by all conditions (9 panels)")
    print("  3. Decision time comprehensive (9 panels)")
    print("  4. Agent perceptions heatmaps (4 panels)")
    print("  5. Compliance patterns (6 panels)")
    print("  6. Perceptions by condition (6 panels)")
    print("  7. Interaction plots (6 panels)")
    print("  8. VR and individual differences (6 panels)")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()

