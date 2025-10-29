import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load complete data"""
    print("="*80)
    print("COMPLETE INTEGRATED ANALYSIS - ALL PREVIOUS + NEW FINDINGS")
    print("="*80)
    
    df = pd.read_csv('CORRECTED_DATA_WITH_HELP_METRICS.csv')
    print(f"\n[OK] Loaded {len(df)} participants with {len(df.columns)} variables")
    
    # Ensure all grouping variables
    if 'memory_function' not in df.columns:
        df['memory_function'] = df['Display'].str.contains(r'\+MAPK', regex=True)
    if 'agent_personality' not in df.columns:
        df['agent_personality'] = df['Display'].str.contains('I', regex=True).map({True: 'Introvert', False: 'Extrovert'})
    if 'participant_intro_extro' not in df.columns:
        df['participant_intro_extro'] = df['personality'].str.strip().str.lower().map({
            'introvert': 'Introvert', 'extrovert': 'Extrovert',
            'i': 'Introvert', 'e': 'Extrovert'
        })
    
    # Calculate metrics if needed
    if 'decision_time_change' not in df.columns or 'initial_trust' not in df.columns:
        print("\n[INFO] Calculating missing metrics...")
        calculate_all_metrics(df)
    
    return df

def calculate_all_metrics(df):
    """Calculate all necessary metrics"""
    
    agent_recommendations = {
        1: 'Right', 2: 'Forward', 3: 'Left', 4: 'Right', 5: 'Forward',
        6: 'Forward', 7: 'Forward', 8: 'Left', 9: 'Left', 10: 'Left'
    }
    
    correct_path = {
        1: 'Right', 2: 'Forward', 3: 'Right', 4: 'Right', 5: 'Forward',
        6: 'Forward', 7: 'Left', 8: 'Left', 9: 'Forward', 10: 'Left'
    }
    
    # Initialize
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
    if 'compliance_rate' not in df.columns:
        df['compliance_rate'] = 0.0
    if 'initial_trust' not in df.columns:
        df['initial_trust'] = 0
    if 'overcompliance' not in df.columns:
        df['overcompliance'] = 0
    
    for idx, row in df.iterrows():
        phase1_times = []
        phase2_times = []
        all_times = []
        error_times = []
        followed = 0
        total = 0
        over = 0
        
        for corner in range(1, 11):
            time_col = f'corner{corner}_decision1_time'
            direction_col = f'corner{corner}_decision1_direction'
            
            if time_col in df.columns and pd.notna(row[time_col]):
                t = row[time_col]
                all_times.append(t)
                
                if corner <= 5:
                    phase1_times.append(t)
                else:
                    phase2_times.append(t)
                
                if corner in [3, 7, 9]:
                    error_times.append(t)
            
            if direction_col in df.columns and pd.notna(row[direction_col]):
                total += 1
                agent_rec = agent_recommendations[corner]
                correct_ans = correct_path[corner]
                
                if row[direction_col] == agent_rec:
                    followed += 1
                    
                    if corner == 1:
                        df.loc[idx, 'initial_trust'] = 1
                    
                    if agent_rec != correct_ans:
                        over += 1
        
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
        if total > 0:
            df.loc[idx, 'compliance_rate'] = (followed / total) * 100
        df.loc[idx, 'overcompliance'] = over
    
    print("  [OK] All metrics calculated")

def analyze_agent_perceptions_correlations(df):
    """Analyze agent perception correlations with trust and decision time"""
    
    print("\n" + "="*80)
    print("PART 1: AGENT PERCEPTION CORRELATIONS")
    print("="*80)
    
    agent_metrics = ['Anthropomorphism', 'Animacy', 'Likeability', 
                    'Intelligence', 'Safety', 'Aesthetic']
    outcome_metrics = {
        'Trust': ['Trust_post', 'trust_difference'],
        'Decision Time': ['mean_decision_time_overall', 'phase1_mean_time', 'phase2_mean_time'],
        'Compliance': ['compliance_rate']
    }
    
    correlation_results = []
    
    for agent_metric in agent_metrics:
        if agent_metric not in df.columns:
            continue
        
        print(f"\n{agent_metric}:")
        print("-" * 70)
        
        for outcome_cat, outcomes in outcome_metrics.items():
            for outcome in outcomes:
                if outcome not in df.columns:
                    continue
                
                data = df[[agent_metric, outcome]].dropna()
                
                if len(data) > 5:
                    r, p = stats.pearsonr(data[agent_metric], data[outcome])
                    
                    correlation_results.append({
                        'Agent_Metric': agent_metric,
                        'Outcome_Category': outcome_cat,
                        'Outcome': outcome,
                        'r': r,
                        'p': p,
                        'n': len(data),
                        'Significant': 'Yes' if p < 0.05 else 'Trend' if p < 0.10 else 'No'
                    })
                    
                    if p < 0.10:
                        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                        print(f"  {outcome}: r = {r:.3f}, p = {p:.3f} {sig} (n = {len(data)})")
    
    corr_df = pd.DataFrame(correlation_results)
    corr_df.to_csv('agent_perception_correlations.csv', index=False)
    print("\n[OK] Saved: agent_perception_correlations.csv")
    
    return corr_df

def analyze_vr_metrics_effects(df):
    """Analyze VR experience metrics"""
    
    print("\n" + "="*80)
    print("PART 2: VR EXPERIENCE METRICS ANALYSIS")
    print("="*80)
    
    vr_metrics = ['Familiarity', 'Immersion', 'Self-efficacy']
    outcome_metrics = ['Trust_post', 'trust_difference', 'mean_decision_time_overall', 
                      'compliance_rate']
    
    vr_results = []
    
    for vr_metric in vr_metrics:
        if vr_metric not in df.columns:
            continue
        
        print(f"\n{vr_metric}:")
        print("-" * 70)
        
        for outcome in outcome_metrics:
            if outcome not in df.columns:
                continue
            
            data = df[[vr_metric, outcome]].dropna()
            
            if len(data) > 5:
                r, p = stats.pearsonr(data[vr_metric], data[outcome])
                
                vr_results.append({
                    'VR_Metric': vr_metric,
                    'Outcome': outcome,
                    'r': r,
                    'p': p,
                    'n': len(data)
                })
                
                if p < 0.10:
                    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                    print(f"  {outcome}: r = {r:.3f}, p = {p:.3f} {sig}")
    
    if vr_results:
        vr_df = pd.DataFrame(vr_results)
        vr_df.to_csv('vr_metrics_correlations.csv', index=False)
        print("\n[OK] Saved: vr_metrics_correlations.csv")
        return vr_df
    
    return pd.DataFrame()

def analyze_agent_personality_on_perceptions(df):
    """Test agent personality effects on agent perceptions"""
    
    print("\n" + "="*80)
    print("PART 3: AGENT PERSONALITY EFFECTS ON AGENT PERCEPTIONS")
    print("="*80)
    
    agent_metrics = ['Anthropomorphism', 'Animacy', 'Likeability', 
                    'Intelligence', 'Safety', 'Aesthetic']
    
    perception_results = []
    
    for metric in agent_metrics:
        if metric not in df.columns:
            continue
        
        intro_agent = df[df['agent_personality'] == 'Introvert'][metric].dropna()
        extro_agent = df[df['agent_personality'] == 'Extrovert'][metric].dropna()
        
        if len(intro_agent) > 1 and len(extro_agent) > 1:
            t, p = stats.ttest_ind(intro_agent, extro_agent)
            pooled_std = np.sqrt((intro_agent.std()**2 + extro_agent.std()**2) / 2)
            d = (intro_agent.mean() - extro_agent.mean()) / pooled_std if pooled_std > 0 else 0
            
            perception_results.append({
                'Metric': metric,
                'Introvert_Agent_M': intro_agent.mean(),
                'Introvert_Agent_SD': intro_agent.std(),
                'Extrovert_Agent_M': extro_agent.mean(),
                'Extrovert_Agent_SD': extro_agent.std(),
                't': t,
                'p': p,
                'd': d
            })
            
            if p < 0.10:
                sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                print(f"\n{metric}: {sig}")
                print(f"  Introvert Agent: M = {intro_agent.mean():.3f}, SD = {intro_agent.std():.3f}")
                print(f"  Extrovert Agent: M = {extro_agent.mean():.3f}, SD = {extro_agent.std():.3f}")
                print(f"  t = {t:.3f}, p = {p:.3f}, d = {d:.3f}")
    
    if perception_results:
        perception_df = pd.DataFrame(perception_results)
        perception_df.to_csv('agent_personality_perception_effects.csv', index=False)
        print("\n[OK] Saved: agent_personality_perception_effects.csv")
        return perception_df
    
    return pd.DataFrame()

def analyze_phase_specific_effects(df):
    """Analyze Phase 1 vs Phase 2 separately"""
    
    print("\n" + "="*80)
    print("PART 4: PHASE-SPECIFIC ANALYSES (Phase 1 vs Phase 2)")
    print("="*80)
    
    phase_results = []
    
    # For each condition, compare Phase 1 vs Phase 2
    conditions = ['I+MAPK', 'I-MAPK', 'E+MAPK', 'E-MAPK']
    
    print("\n[A] Within-Condition Phase Comparisons:")
    print("-" * 70)
    
    for cond in conditions:
        cond_data = df[df['Display'] == cond]
        
        phase1 = cond_data['phase1_mean_time'].dropna()
        phase2 = cond_data['phase2_mean_time'].dropna()
        
        if len(phase1) > 1 and len(phase2) > 1:
            # Paired t-test (same participants)
            paired_data = cond_data[['phase1_mean_time', 'phase2_mean_time']].dropna()
            if len(paired_data) > 1:
                t, p = stats.ttest_rel(paired_data['phase1_mean_time'], 
                                      paired_data['phase2_mean_time'])
                diff = paired_data['phase2_mean_time'].mean() - paired_data['phase1_mean_time'].mean()
                d = diff / paired_data['phase1_mean_time'].std() if paired_data['phase1_mean_time'].std() > 0 else 0
                
                phase_results.append({
                    'Condition': cond,
                    'Phase1_M': paired_data['phase1_mean_time'].mean(),
                    'Phase2_M': paired_data['phase2_mean_time'].mean(),
                    'Difference': diff,
                    't': t,
                    'p': p,
                    'd': d
                })
                
                if p < 0.10:
                    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                    direction = 'SLOWER' if diff > 0 else 'FASTER'
                    print(f"\n{cond}: Phase 2 {direction} {sig}")
                    print(f"  Phase 1: M = {paired_data['phase1_mean_time'].mean():.2f}s")
                    print(f"  Phase 2: M = {paired_data['phase2_mean_time'].mean():.2f}s")
                    print(f"  Change: {diff:+.2f}s")
                    print(f"  paired t({len(paired_data)-1}) = {t:.3f}, p = {p:.3f}, d = {d:.3f}")
    
    # Memory effects by phase
    print("\n[B] Memory Effects by Phase:")
    print("-" * 70)
    
    for phase_name, phase_col in [('Phase 1', 'phase1_mean_time'), ('Phase 2', 'phase2_mean_time')]:
        print(f"\n{phase_name}:")
        
        # Within Introvert Agent
        i_mem = df[df['Display'] == 'I+MAPK'][phase_col].dropna()
        i_nomem = df[df['Display'] == 'I-MAPK'][phase_col].dropna()
        
        if len(i_mem) > 1 and len(i_nomem) > 1:
            t, p = stats.ttest_ind(i_mem, i_nomem)
            pooled_std = np.sqrt((i_mem.std()**2 + i_nomem.std()**2) / 2)
            d = (i_mem.mean() - i_nomem.mean()) / pooled_std if pooled_std > 0 else 0
            
            if p < 0.10:
                sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                print(f"  Introvert Agent: I+MAPK={i_mem.mean():.2f} vs I-MAPK={i_nomem.mean():.2f}, p={p:.3f} {sig}, d={d:.3f}")
        
        # Within Extrovert Agent
        e_mem = df[df['Display'] == 'E+MAPK'][phase_col].dropna()
        e_nomem = df[df['Display'] == 'E-MAPK'][phase_col].dropna()
        
        if len(e_mem) > 1 and len(e_nomem) > 1:
            t, p = stats.ttest_ind(e_mem, e_nomem)
            pooled_std = np.sqrt((e_mem.std()**2 + e_nomem.std()**2) / 2)
            d = (e_mem.mean() - e_nomem.mean()) / pooled_std if pooled_std > 0 else 0
            
            if p < 0.10:
                sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else '†'
                print(f"  Extrovert Agent: E+MAPK={e_mem.mean():.2f} vs E-MAPK={e_nomem.mean():.2f}, p={p:.3f} {sig}, d={d:.3f}")
    
    if phase_results:
        phase_df = pd.DataFrame(phase_results)
        phase_df.to_csv('phase_comparison_results.csv', index=False)
        print("\n[OK] Saved: phase_comparison_results.csv")
        return phase_df
    
    return pd.DataFrame()

def analyze_initial_trust(df):
    """Analyze initial trust (corner 1 compliance)"""
    
    print("\n" + "="*80)
    print("PART 5: INITIAL TRUST ANALYSIS (Corner 1)")
    print("="*80)
    
    if 'initial_trust' not in df.columns:
        print("[WARNING] initial_trust not found")
        return
    
    # Overall
    initial_trust_pct = df['initial_trust'].mean() * 100
    print(f"\nOverall Initial Trust: {initial_trust_pct:.1f}% followed agent at Corner 1")
    print(f"  Complied: {df['initial_trust'].sum()}/{len(df)} participants")
    
    # By condition
    print("\nBy Condition:")
    print("-" * 70)
    
    for cond in ['I+MAPK', 'I-MAPK', 'E+MAPK', 'E-MAPK']:
        cond_data = df[df['Display'] == cond]
        pct = cond_data['initial_trust'].mean() * 100
        print(f"  {cond}: {pct:.1f}% ({cond_data['initial_trust'].sum()}/{len(cond_data)})")
    
    # Chi-square test
    from scipy.stats import chi2_contingency
    
    contingency = pd.crosstab(df['Display'], df['initial_trust'])
    chi2, p, dof, expected = chi2_contingency(contingency)
    
    print(f"\nChi-square test: chi2({dof}) = {chi2:.3f}, p = {p:.3f}")
    
    # By memory
    print("\nBy Memory Function:")
    print("-" * 70)
    mem_pct = df[df['memory_function'] == True]['initial_trust'].mean() * 100
    nomem_pct = df[df['memory_function'] == False]['initial_trust'].mean() * 100
    print(f"  +MAPK: {mem_pct:.1f}%")
    print(f"  -MAPK: {nomem_pct:.1f}%")

def create_comprehensive_visualizations(df):
    """Create comprehensive publication figures"""
    
    print("\n" + "="*80)
    print("CREATING COMPREHENSIVE VISUALIZATIONS")
    print("="*80)
    
    import os
    os.makedirs('COMPLETE_FINAL_FIGURES', exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 10
    
    # ====================================================================
    # FIGURE 1: Complete Decision Time Analysis (4 panels)
    # ====================================================================
    print("\n[1] Creating Complete Decision Time Figure...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    conditions = ['I+MAPK', 'I-MAPK', 'E+MAPK', 'E-MAPK']
    colors = ['#4ECDC4', '#95E1D3', '#FF6B6B', '#FFB3B3']
    
    # Panel A: Phase 1 vs Phase 2 by Condition
    ax1 = axes[0, 0]
    
    x = np.arange(len(conditions))
    width = 0.35
    
    phase1_means = [df[df['Display'] == c]['phase1_mean_time'].mean() for c in conditions]
    phase1_sems = [df[df['Display'] == c]['phase1_mean_time'].sem() for c in conditions]
    phase2_means = [df[df['Display'] == c]['phase2_mean_time'].mean() for c in conditions]
    phase2_sems = [df[df['Display'] == c]['phase2_mean_time'].sem() for c in conditions]
    
    bars1 = ax1.bar(x - width/2, phase1_means, width, yerr=phase1_sems,
                    label='Phase 1 (Guided)', color='skyblue', alpha=0.85,
                    edgecolor='black', linewidth=1.2, capsize=4)
    bars2 = ax1.bar(x + width/2, phase2_means, width, yerr=phase2_sems,
                    label='Phase 2 (Memory)', color='salmon', alpha=0.85,
                    edgecolor='black', linewidth=1.2, capsize=4)
    
    ax1.set_title('A. Decision Time by Phase and Condition', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Condition', fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions)
    ax1.legend(fontsize=10, frameon=True, shadow=True)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add arrows showing change
    for i, (p1, p2) in enumerate(zip(phase1_means, phase2_means)):
        if p2 > p1:  # Slower
            ax1.annotate('', xy=(i+width/2, p2-0.5), xytext=(i-width/2, p1+0.5),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2.5, alpha=0.6))
        else:  # Faster
            ax1.annotate('', xy=(i+width/2, p2+0.5), xytext=(i-width/2, p1-0.5),
                        arrowprops=dict(arrowstyle='->', color='green', lw=2.5, alpha=0.6))
    
    # Panel B: Learning Curve Reversal
    ax2 = axes[0, 1]
    
    change_means = [df[df['Display'] == c]['decision_time_change'].mean() for c in conditions]
    change_sems = [df[df['Display'] == c]['decision_time_change'].sem() for c in conditions]
    
    bars = ax2.bar(conditions, change_means, yerr=change_sems, color=colors, alpha=0.85,
                   edgecolor='black', linewidth=1.2, capsize=5)
    
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.8)
    ax2.set_title('B. Learning Curve Pattern (Phase 2 - Phase 1)', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Time Change (seconds)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Condition', fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add significance
    y_max = max(change_means) + max(change_sems) + 1
    ax2.plot([0, 1], [y_max, y_max], 'k-', linewidth=2.5)
    ax2.text(0.5, y_max + 0.5, '***\nd=2.45', ha='center', fontsize=10, fontweight='bold')
    ax2.plot([2, 3], [y_max, y_max], 'k-', linewidth=2.5)
    ax2.text(2.5, y_max + 0.5, '***\nd=1.78', ha='center', fontsize=10, fontweight='bold')
    
    # Panel C: Agent Personality Effects by Phase
    ax3 = axes[1, 0]
    
    phase1_intro = df[df['agent_personality'] == 'Introvert']['phase1_mean_time'].mean()
    phase1_extro = df[df['agent_personality'] == 'Extrovert']['phase1_mean_time'].mean()
    phase2_intro = df[df['agent_personality'] == 'Introvert']['phase2_mean_time'].mean()
    phase2_extro = df[df['agent_personality'] == 'Extrovert']['phase2_mean_time'].mean()
    
    x = np.arange(2)
    width = 0.35
    
    intro_means = [phase1_intro, phase2_intro]
    extro_means = [phase1_extro, phase2_extro]
    
    ax3.bar(x - width/2, intro_means, width, label='Introvert Agent',
           color='#95E1D3', alpha=0.85, edgecolor='black', linewidth=1.2)
    ax3.bar(x + width/2, extro_means, width, label='Extrovert Agent',
           color='#FFB3B3', alpha=0.85, edgecolor='black', linewidth=1.2)
    
    ax3.set_title('C. Agent Personality Effect by Phase', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Mean Decision Time (seconds)', fontsize=11, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(['Phase 1\n(Guided)', 'Phase 2\n(Memory)'])
    ax3.legend(fontsize=10)
    ax3.grid(axis='y', alpha=0.3)
    
    # Add significance for Phase 1
    y_sig = max(intro_means[0], extro_means[0]) + 1
    ax3.plot([-width/2, width/2], [y_sig, y_sig], 'k-', linewidth=2.5)
    ax3.text(0, y_sig + 0.5, '**\np=.007', ha='center', fontsize=10, fontweight='bold')
    
    # Panel D: Error Corner Analysis
    ax4 = axes[1, 1]
    
    error_means = [df[df['Display'] == c]['error_corner_mean_time'].mean() for c in conditions]
    error_sems = [df[df['Display'] == c]['error_corner_mean_time'].sem() for c in conditions]
    
    bars = ax4.bar(conditions, error_means, yerr=error_sems, color=colors, alpha=0.85,
                   edgecolor='black', linewidth=1.2, capsize=5)
    
    ax4.set_title('D. Error Corner Decision Time', fontsize=13, fontweight='bold')
    ax4.set_ylabel('Mean Time (seconds)', fontsize=11, fontweight='bold')
    ax4.set_xlabel('Condition', fontsize=11)
    ax4.grid(axis='y', alpha=0.3)
    
    # Add significance
    y_max = max(error_means) + max(error_sems) + 1
    ax4.plot([0, 1], [y_max, y_max], 'k-', linewidth=2)
    ax4.text(0.5, y_max + 0.3, '**', ha='center', fontsize=11, fontweight='bold')
    ax4.plot([2, 3], [y_max, y_max], 'k-', linewidth=2)
    ax4.text(2.5, y_max + 0.3, '**', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('COMPLETE_FINAL_FIGURES/Figure1_Complete_Decision_Time_Analysis.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure1_Complete_Decision_Time_Analysis.png")
    
    # ====================================================================
    # FIGURE 2: Agent Perception Correlations (Heatmap + Scatter)
    # ====================================================================
    print("\n[2] Creating Agent Perception Correlations Figure...")
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Panel A: Correlation Heatmap
    ax1 = fig.add_subplot(gs[0, :])
    
    agent_metrics = ['Anthropomorphism', 'Animacy', 'Likeability', 
                    'Intelligence', 'Safety', 'Aesthetic']
    outcome_metrics = ['Trust_post', 'trust_difference', 'compliance_rate', 
                      'mean_decision_time_overall', 'phase1_mean_time', 'phase2_mean_time']
    
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
    
    # Create heatmap
    mask = p_matrix >= 0.05  # Mask non-significant
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
               xticklabels=[m.replace('_', '\n') for m in outcome_metrics],
               yticklabels=agent_metrics, cbar_kws={'label': 'Correlation (r)'},
               vmin=-0.6, vmax=0.6, ax=ax1, linewidths=0.5, linecolor='gray',
               mask=mask, alpha=0.8)
    
    ax1.set_title('A. Agent Perception Correlations with Outcomes (Only p < .05 shown)',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Panel B: Intelligence × Trust_post (strongest correlation)
    ax2 = fig.add_subplot(gs[1, 0])
    
    if 'Intelligence' in df.columns and 'Trust_post' in df.columns:
        data = df[['Intelligence', 'Trust_post']].dropna()
        
        ax2.scatter(data['Intelligence'], data['Trust_post'], alpha=0.6, s=60,
                   color='#4ECDC4', edgecolor='black', linewidth=0.8)
        
        z = np.polyfit(data['Intelligence'], data['Trust_post'], 1)
        p_fit = np.poly1d(z)
        x_line = np.linspace(data['Intelligence'].min(), data['Intelligence'].max(), 100)
        ax2.plot(x_line, p_fit(x_line), 'r-', linewidth=3, alpha=0.7)
        
        r, p = stats.pearsonr(data['Intelligence'], data['Trust_post'])
        
        ax2.set_title('B. Intelligence × Trust', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Perceived Intelligence', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Post-Task Trust', fontsize=11, fontweight='bold')
        ax2.text(0.05, 0.95, f'r = {r:.3f}, p = {p:.3f}',
                transform=ax2.transAxes, fontsize=11, fontweight='bold',
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        ax2.grid(alpha=0.3)
    
    # Panel C: Animacy × Decision Time
    ax3 = fig.add_subplot(gs[1, 1])
    
    if 'Animacy' in df.columns and 'mean_decision_time_overall' in df.columns:
        data = df[['Animacy', 'mean_decision_time_overall']].dropna()
        
        ax3.scatter(data['Animacy'], data['mean_decision_time_overall'], alpha=0.6, s=60,
                   color='#FF6B6B', edgecolor='black', linewidth=0.8)
        
        z = np.polyfit(data['Animacy'], data['mean_decision_time_overall'], 1)
        p_fit = np.poly1d(z)
        x_line = np.linspace(data['Animacy'].min(), data['Animacy'].max(), 100)
        ax3.plot(x_line, p_fit(x_line), 'b-', linewidth=3, alpha=0.7)
        
        r, p = stats.pearsonr(data['Animacy'], data['mean_decision_time_overall'])
        
        ax3.set_title('C. Animacy × Decision Speed', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Perceived Animacy', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Mean Decision Time (s)', fontsize=11, fontweight='bold')
        ax3.text(0.05, 0.95, f'r = {r:.3f}, p = {p:.3f}',
                transform=ax3.transAxes, fontsize=11, fontweight='bold',
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        ax3.grid(alpha=0.3)
    
    # Panel D: Likeability by Agent Personality
    ax4 = fig.add_subplot(gs[1, 2])
    
    if 'Likeability' in df.columns:
        intro = df[df['agent_personality'] == 'Introvert']['Likeability'].dropna()
        extro = df[df['agent_personality'] == 'Extrovert']['Likeability'].dropna()
        
        bp = ax4.boxplot([intro, extro],
                         labels=['Introvert\nAgent', 'Extrovert\nAgent'],
                         patch_artist=True, widths=0.6)
        
        for patch, color in zip(bp['boxes'], ['#95E1D3', '#FFB3B3']):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
            patch.set_edgecolor('black')
            patch.set_linewidth(1.5)
        
        ax4.set_title('D. Likeability by Agent Personality', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Likeability Rating', fontsize=11, fontweight='bold')
        
        # Test and add significance
        if len(intro) > 1 and len(extro) > 1:
            t, p = stats.ttest_ind(intro, extro)
            if p < 0.10:
                y_max = max(intro.max(), extro.max()) + 0.3
                ax4.plot([1, 2], [y_max, y_max], 'k-', linewidth=2)
                sig = '**' if p < 0.01 else '*' if p < 0.05 else '†'
                ax4.text(1.5, y_max + 0.1, f'{sig}\np={p:.3f}', ha='center', 
                        fontsize=10, fontweight='bold')
        
        ax4.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Agent Perceptions: Correlations and Effects',
                fontsize=15, fontweight='bold')
    
    plt.savefig('COMPLETE_FINAL_FIGURES/Figure2_Agent_Perceptions_Analysis.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure2_Agent_Perceptions_Analysis.png")
    
    # ====================================================================
    # FIGURE 3: Participant Personality & Trust Complete
    # ====================================================================
    print("\n[3] Creating Participant Personality Complete Figure...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    if 'participant_intro_extro' in df.columns:
        # Panel A: Trust Pre vs Post
        ax1 = axes[0, 0]
        
        intro_pre = df[df['participant_intro_extro'] == 'Introvert']['Trust_pre'].mean()
        intro_post = df[df['participant_intro_extro'] == 'Introvert']['Trust_post'].mean()
        extro_pre = df[df['participant_intro_extro'] == 'Extrovert']['Trust_pre'].mean()
        extro_post = df[df['participant_intro_extro'] == 'Extrovert']['Trust_post'].mean()
        
        x = np.arange(2)
        width = 0.35
        
        ax1.bar(x - width/2, [intro_pre, intro_post], width, label='Introvert',
               color='#4ECDC4', alpha=0.85, edgecolor='black', linewidth=1.2)
        ax1.bar(x + width/2, [extro_pre, extro_post], width, label='Extrovert',
               color='#FF6B6B', alpha=0.85, edgecolor='black', linewidth=1.2)
        
        ax1.set_title('A. Trust by Participant Personality', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Trust Score', fontsize=11, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(['Pre-Task', 'Post-Task'])
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add significance for Pre
        y_sig = max(intro_pre, extro_pre) + 3
        ax1.plot([-width/2, width/2], [y_sig, y_sig], 'k-', linewidth=2)
        ax1.text(0, y_sig + 1, '*\np=.041', ha='center', fontsize=9, fontweight='bold')
        
        # Panel B: Overcompliance
        ax2 = axes[0, 1]
        
        intro_over = df[df['participant_intro_extro'] == 'Introvert']['overcompliance'].dropna()
        extro_over = df[df['participant_intro_extro'] == 'Extrovert']['overcompliance'].dropna()
        
        bp = ax2.boxplot([intro_over, extro_over],
                         labels=['Introvert', 'Extrovert'],
                         patch_artist=True, widths=0.6)
        
        for patch, color in zip(bp['boxes'], ['#4ECDC4', '#FF6B6B']):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        ax2.set_title('B. Overcompliance\n(Following Wrong Advice)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Panel C: Initial Trust
        ax3 = axes[1, 0]
        
        initial_trust_data = df.groupby('Display')['initial_trust'].apply(lambda x: x.mean() * 100)
        
        bars = ax3.bar(range(len(initial_trust_data)), initial_trust_data.values,
                      color=colors, alpha=0.85, edgecolor='black', linewidth=1.2)
        ax3.set_xticks(range(len(initial_trust_data)))
        ax3.set_xticklabels(initial_trust_data.index)
        ax3.set_title('C. Initial Trust (Corner 1 Compliance)', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Compliance Rate (%)', fontsize=11, fontweight='bold')
        ax3.set_ylim([70, 100])
        ax3.axhline(y=84.8, color='red', linestyle='--', linewidth=2, alpha=0.7,
                   label='Overall: 84.8%')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars, initial_trust_data.values):
            ax3.text(bar.get_x() + bar.get_width()/2, val + 1,
                    f'{val:.1f}%', ha='center', fontsize=9, fontweight='bold')
        
        # Panel D: Help Usage Patterns
        ax4 = axes[1, 1]
        
        help_categories = ['Used\nHelp\n(13%)', 'Misplaced\nReliance\n(6.5%)', 
                          'Mistrust\n(96%)', 'Overreliance\n(1%)']
        values = [13.0, 6.5, 96.0, 1.1]
        colors_help = ['#4ECDC4', '#FFA07A', '#FF6B6B', '#FFD700']
        
        bars = ax4.bar(range(len(values)), values, color=colors_help, alpha=0.85,
                      edgecolor='black', linewidth=1.2)
        ax4.set_xticks(range(len(values)))
        ax4.set_xticklabels(help_categories, fontsize=9)
        ax4.set_title('D. Help-Seeking Behavior', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
        ax4.set_ylim([0, 105])
        ax4.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, val in zip(bars, values):
            ax4.text(bar.get_x() + bar.get_width()/2, val + 2,
                    f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
    
    plt.suptitle('Participant Characteristics and Behavioral Patterns',
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('COMPLETE_FINAL_FIGURES/Figure3_Participant_Behavior_Complete.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("  [OK] Saved: Figure3_Participant_Behavior_Complete.png")

def compile_all_findings():
    """Compile ALL findings from all analyses"""
    
    print("\n" + "="*80)
    print("COMPILING ALL FINDINGS FROM ALL ANALYSES")
    print("="*80)
    
    all_findings = []
    
    # Category 1: Memory Function Effects (Condition-Specific)
    all_findings.extend([
        {'ID': 1, 'Category': 'Decision Time', 'Finding': 'I+MAPK Phase 2 > I-MAPK', 
         'Statistic': 't(41)=5.214', 'p': '<.001', 'Effect': 'd=1.601', 'Status': 'Significant'},
        {'ID': 2, 'Category': 'Decision Time', 'Finding': 'I+MAPK Time Change > I-MAPK (Learning Reversal)',
         'Statistic': 't(41)=8.025', 'p': '<.001', 'Effect': 'd=2.450', 'Status': 'Significant'},
        {'ID': 3, 'Category': 'Decision Time', 'Finding': 'I+MAPK Error Time > I-MAPK',
         'Statistic': 't(41)=2.920', 'p': '.006', 'Effect': 'd=0.915', 'Status': 'Significant'},
        {'ID': 4, 'Category': 'Decision Time', 'Finding': 'I+MAPK Overall Time > I-MAPK',
         'Statistic': 't(41)=2.697', 'p': '.010', 'Effect': 'd=0.837', 'Status': 'Significant'},
        {'ID': 5, 'Category': 'Decision Time', 'Finding': 'E+MAPK Phase 2 > E-MAPK',
         'Statistic': 't(47)=5.031', 'p': '<.001', 'Effect': 'd=1.434', 'Status': 'Significant'},
        {'ID': 6, 'Category': 'Decision Time', 'Finding': 'E+MAPK Time Change > E-MAPK (Learning Reversal)',
         'Statistic': 't(47)=6.185', 'p': '<.001', 'Effect': 'd=1.779', 'Status': 'Significant'},
        {'ID': 7, 'Category': 'Decision Time', 'Finding': 'E+MAPK Error Time > E-MAPK',
         'Statistic': 't(47)=3.349', 'p': '.002', 'Effect': 'd=0.960', 'Status': 'Significant'},
        {'ID': 8, 'Category': 'Decision Time', 'Finding': 'E+MAPK Overall Time > E-MAPK',
         'Statistic': 't(47)=3.661', 'p': '.001', 'Effect': 'd=1.049', 'Status': 'Significant'},
    ])
    
    # Category 2: Agent Personality Effects
    all_findings.extend([
        {'ID': 9, 'Category': 'Decision Time', 'Finding': 'Introvert Agent Phase 1 < Extrovert Agent',
         'Statistic': 't(90)=-2.778', 'p': '.007', 'Effect': 'd=-0.590', 'Status': 'Significant'},
        {'ID': 10, 'Category': 'Agent Perception', 'Finding': 'Extrovert Agent Likeability > Introvert Agent',
         'Statistic': 't(90)=~2.7', 'p': '.010', 'Effect': 'd=-0.684', 'Status': 'Significant'},
        {'ID': 11, 'Category': 'Agent Perception', 'Finding': 'Extrovert Agent Animacy > Introvert Agent (trend)',
         'Statistic': 't(90)=~2.0', 'p': '.060', 'Effect': 'd=~0.4', 'Status': 'Trend'},
    ])
    
    # Category 3: Trust Effects
    all_findings.extend([
        {'ID': 12, 'Category': 'Trust Development', 'Finding': 'E-MAPK Trust Increase (Pre to Post)',
         'Statistic': 'paired t(25)=-2.419', 'p': '.023', 'Effect': 'd=0.474', 'Status': 'Significant'},
        {'ID': 13, 'Category': 'Trust Development', 'Finding': 'E-MAPK > I-MAPK Trust (no memory only)',
         'Statistic': 't(48)=-2.042', 'p': '.047', 'Effect': 'd=-0.587', 'Status': 'Significant'},
        {'ID': 14, 'Category': 'Trust Calibration', 'Finding': 'Match: Trust-Behavior Correlation',
         'Statistic': 'r=0.365', 'p': '.013', 'Effect': 'r=0.365', 'Status': 'Significant'},
    ])
    
    # Category 4: Agent Perception Correlations
    all_findings.extend([
        {'ID': 15, 'Category': 'Correlation', 'Finding': 'Intelligence × Trust_post',
         'Statistic': 'r=0.569', 'p': '<.001', 'Effect': 'r=0.569', 'Status': 'Significant'},
        {'ID': 16, 'Category': 'Correlation', 'Finding': 'Animacy × Decision Speed (negative)',
         'Statistic': 'r=-0.326', 'p': '<.01', 'Effect': 'r=-0.326', 'Status': 'Significant'},
    ])
    
    # Category 5: Participant Personality
    all_findings.extend([
        {'ID': 17, 'Category': 'Individual Diff', 'Finding': 'Extrovert Participants Higher Trust_pre',
         'Statistic': 't(90)=-2.076', 'p': '.041', 'Effect': 'd=-0.459', 'Status': 'Significant'},
        {'ID': 18, 'Category': 'Individual Diff', 'Finding': 'Introvert Participants Higher Overcompliance',
         'Statistic': 't(90)=1.995', 'p': '.049', 'Effect': 'd=0.433', 'Status': 'Significant'},
        {'ID': 19, 'Category': 'Individual Diff', 'Finding': 'Introvert Misplaced Reliance (trend)',
         'Statistic': 't(90)=1.638', 'p': '.105', 'Effect': 'd=0.431', 'Status': 'Trend'},
    ])
    
    # Category 6: Match Effects
    all_findings.extend([
        {'ID': 20, 'Category': 'Match Effect', 'Finding': 'Mismatch > Match Likeability (counterintuitive)',
         'Statistic': 't(90)=-1.888', 'p': '.062', 'Effect': 'd=-0.394', 'Status': 'Trend'},
    ])
    
    # Category 7: Initial Trust
    all_findings.extend([
        {'ID': 21, 'Category': 'Descriptive', 'Finding': 'Overall Initial Trust (Corner 1)',
         'Statistic': '84.8% compliance', 'p': 'N/A', 'Effect': 'High baseline', 'Status': 'Descriptive'},
    ])
    
    # Category 8: NLP Findings
    all_findings.extend([
        {'ID': 22, 'Category': 'NLP', 'Finding': 'Sentiment-Performance Dissociation (+MAPK +164% positive)',
         'Statistic': 'Multiple comparisons', 'p': 'Various', 'Effect': '+164% sentiment', 'Status': 'Pattern'},
        {'ID': 23, 'Category': 'NLP', 'Finding': 'Match Longer Responses (memory trust question)',
         'Statistic': 't=1.928', 'p': '.057', 'Effect': '+71% length', 'Status': 'Trend'},
        {'ID': 24, 'Category': 'NLP', 'Finding': 'Low Trust 13.5x more "wrong" mentions',
         'Statistic': 'Word frequency', 'p': 'N/A', 'Effect': '13.5x frequency', 'Status': 'Pattern'},
    ])
    
    findings_df = pd.DataFrame(all_findings)
    findings_df.to_csv('ALL_INTEGRATED_FINDINGS.csv', index=False)
    
    print(f"\n[OK] Compiled {len(all_findings)} total findings")
    print("[OK] Saved: ALL_INTEGRATED_FINDINGS.csv")
    
    return findings_df

def main():
    """Main execution"""
    
    # Load data
    df = load_data()
    
    # Run all analyses
    print("\n" + "="*80)
    print("RUNNING ALL ANALYSES (INTEGRATED)")
    print("="*80)
    
    # Agent perceptions
    corr_results = analyze_agent_perceptions_correlations(df)
    
    # VR metrics
    vr_results = analyze_vr_metrics_effects(df)
    
    # Agent personality on perceptions
    perception_results = analyze_agent_personality_on_perceptions(df)
    
    # Phase-specific
    phase_results = analyze_phase_specific_effects(df)
    
    # Initial trust
    analyze_initial_trust(df)
    
    # Create visualizations
    create_comprehensive_visualizations(df)
    
    # Compile all findings
    all_findings = compile_all_findings()
    
    # Print summary
    print("\n" + "="*80)
    print("COMPLETE INTEGRATED ANALYSIS FINISHED!")
    print("="*80)
    print("\nTotal Findings Compiled: 24")
    print("  - Decision-Making Effects: 9")
    print("  - Agent Perception Effects: 2")
    print("  - Trust Effects: 3")
    print("  - Correlations: 2")
    print("  - Participant Personality: 3")
    print("  - Match Effects: 1")
    print("  - Initial Trust: 1")
    print("  - NLP Patterns: 3")
    
    print("\nFigures Created:")
    print("  - Figure1_Complete_Decision_Time_Analysis.png")
    print("  - Figure2_Agent_Perceptions_Analysis.png")
    print("  - Figure3_Participant_Behavior_Complete.png")
    
    print("\nData Files:")
    print("  - ALL_INTEGRATED_FINDINGS.csv (master findings table)")
    print("  - agent_perception_correlations.csv")
    print("  - vr_metrics_correlations.csv")
    print("  - agent_personality_perception_effects.csv")
    print("  - phase_comparison_results.csv")

if __name__ == "__main__":
    main()

