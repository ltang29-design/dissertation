import pandas as pd
import numpy as np
from collections import Counter
import re
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Try to import NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    SKLEARN_AVAILABLE = True
except:
    SKLEARN_AVAILABLE = False
    print("[WARNING] sklearn not available, some analyses will be skipped")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except:
    TEXTBLOB_AVAILABLE = False
    print("[WARNING] TextBlob not available, sentiment analysis will be skipped")

def load_data():
    """Load data with all text responses"""
    print("="*80)
    print("COMPREHENSIVE QUALITATIVE ANALYSIS BY CONDITION")
    print("="*80)
    
    df = pd.read_csv('CORRECTED_DATA_WITH_HELP_METRICS.csv')
    print(f"\n[OK] Loaded {len(df)} participants")
    
    # Create condition labels
    df['condition_label'] = df['Display'].map({
        'I+MAPK': 'Introvert Agent with Memory',
        'I-MAPK': 'Introvert Agent no Memory',
        'E+MAPK': 'Extrovert Agent with Memory',
        'E-MAPK': 'Extrovert Agent no Memory'
    })
    
    # Create grouping variables
    df['memory_function'] = df['Display'].str.contains(r'\+MAPK', regex=True).map({
        True: 'With Memory', False: 'Without Memory'
    })
    
    df['agent_personality'] = df['Display'].str.contains('I', regex=False).map({
        True: 'Introvert Agent', False: 'Extrovert Agent'
    })
    
    df['participant_personality'] = df['personality'].str.strip().str.lower().map({
        'introvert': 'Introvert', 'extrovert': 'Extrovert',
        'i': 'Introvert', 'e': 'Extrovert'
    })
    
    # Match/Mismatch
    df['match_label'] = 'Mismatch'
    mask_match = (
        ((df['Display'].str.contains('I')) & (df['personality'].str.strip().str.lower().isin(['introvert', 'i']))) |
        ((df['Display'].str.contains('E')) & (df['personality'].str.strip().str.lower().isin(['extrovert', 'e'])))
    )
    df.loc[mask_match, 'match_label'] = 'Match'
    
    print(f"  Conditions: {df['condition_label'].nunique()}")
    print(f"  Memory: {df['memory_function'].value_counts().to_dict()}")
    print(f"  Agent: {df['agent_personality'].value_counts().to_dict()}")
    print(f"  Match: {df['match_label'].value_counts().to_dict()}")
    
    return df

def analyze_question(df, question_col, question_name, output_file):
    """Comprehensive analysis for one question"""
    
    print("\n" + "="*80)
    print(f"ANALYZING: {question_name}")
    print("="*80)
    
    results = []
    results.append(f"\n{'='*80}")
    results.append(f"QUESTION: {question_name}")
    results.append(f"{'='*80}\n")
    results.append(f"Column: {question_col}\n")
    
    # Check if column exists
    if question_col not in df.columns:
        results.append(f"[ERROR] Column not found: {question_col}\n")
        return results
    
    # Clean and prepare text
    df_clean = df[[question_col, 'Display', 'condition_label', 'memory_function', 
                   'agent_personality', 'participant_personality', 'match_label']].copy()
    df_clean[question_col] = df_clean[question_col].fillna('')
    df_clean[question_col] = df_clean[question_col].astype(str)
    
    # Remove very short responses
    df_clean['text_length'] = df_clean[question_col].str.len()
    df_clean['word_count'] = df_clean[question_col].str.split().str.len()
    df_analysis = df_clean[df_clean['text_length'] > 10].copy()
    
    results.append(f"Total responses: {len(df_clean)}")
    results.append(f"Valid responses (>10 chars): {len(df_analysis)}")
    results.append(f"Response rate: {len(df_analysis)/len(df_clean)*100:.1f}%\n")
    
    if len(df_analysis) < 5:
        results.append("[WARNING] Too few responses for analysis\n")
        return results
    
    # =================================================================
    # ANALYSIS 1: Text Length by Condition
    # =================================================================
    results.append("\n" + "-"*80)
    results.append("ANALYSIS 1: RESPONSE LENGTH BY CONDITION")
    results.append("-"*80 + "\n")
    
    for grouping, var_name in [('condition_label', 'Specific Condition'),
                                ('memory_function', 'Memory Function'),
                                ('agent_personality', 'Agent Personality'),
                                ('match_label', 'Personality Match'),
                                ('participant_personality', 'Participant Personality')]:
        
        results.append(f"\nBy {var_name}:")
        results.append("-" * 60)
        
        group_stats = df_analysis.groupby(grouping)['word_count'].agg(['count', 'mean', 'std', 'median'])
        
        for idx, row in group_stats.iterrows():
            results.append(f"  {idx}: M = {row['mean']:.1f} words (SD = {row['std']:.1f}, "
                          f"Mdn = {row['median']:.0f}, n = {row['count']:.0f})")
        
        # Statistical test
        groups = df_analysis[grouping].unique()
        if len(groups) == 2:
            g1 = df_analysis[df_analysis[grouping] == groups[0]]['word_count'].dropna()
            g2 = df_analysis[df_analysis[grouping] == groups[1]]['word_count'].dropna()
            
            if len(g1) > 1 and len(g2) > 1:
                t, p = stats.ttest_ind(g1, g2)
                d = (g1.mean() - g2.mean()) / np.sqrt((g1.std()**2 + g2.std()**2) / 2)
                
                sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else '†' if p < .10 else ''
                results.append(f"  t-test: t = {t:.3f}, p = {p:.3f} {sig}, d = {d:.3f}")
                
                if p < 0.10:
                    pct_diff = ((g1.mean() - g2.mean()) / g2.mean()) * 100
                    results.append(f"  → {groups[0]} wrote {abs(pct_diff):.1f}% {'more' if pct_diff > 0 else 'less'} than {groups[1]}")
    
    # =================================================================
    # ANALYSIS 2: Key Themes and Keywords by Condition
    # =================================================================
    results.append("\n" + "-"*80)
    results.append("ANALYSIS 2: KEY THEMES AND KEYWORDS")
    results.append("-"*80 + "\n")
    
    # Define key themes to look for
    themes = {
        'Trust': ['trust', 'confidence', 'reliable', 'depend', 'believe'],
        'Memory': ['memory', 'remember', 'recall', 'past', 'previous', 'experience'],
        'Accuracy': ['correct', 'accurate', 'right', 'wrong', 'mistake', 'error', 'incorrect'],
        'Personality': ['personality', 'similar', 'like me', 'different', 'introvert', 'extrovert'],
        'Helpfulness': ['helpful', 'guidance', 'assist', 'support', 'useful'],
        'Hesitation': ['hesitant', 'doubt', 'uncertain', 'confused', 'unsure', 'question'],
        'Consistency': ['consistent', 'inconsistent', 'reliable', 'unreliable', 'predictable'],
        'Human-like': ['human', 'friendly', 'warm', 'personal', 'connection', 'relate']
    }
    
    for grouping, var_name in [('memory_function', 'Memory Function'),
                                ('agent_personality', 'Agent Personality'),
                                ('match_label', 'Personality Match')]:
        
        results.append(f"\nTheme Frequency by {var_name}:")
        results.append("-" * 60)
        
        groups = df_analysis[grouping].unique()
        
        for theme_name, keywords in themes.items():
            theme_counts = {}
            
            for group in groups:
                group_texts = df_analysis[df_analysis[grouping] == group][question_col]
                combined_text = ' '.join(group_texts).lower()
                
                # Count theme mentions
                count = sum(combined_text.count(kw) for kw in keywords)
                theme_counts[group] = count
            
            # Only report if theme appears
            if sum(theme_counts.values()) > 0:
                results.append(f"\n  {theme_name}:")
                for group, count in theme_counts.items():
                    group_size = len(df_analysis[df_analysis[grouping] == group])
                    rate = count / group_size if group_size > 0 else 0
                    results.append(f"    {group}: {count} mentions ({rate:.2f} per participant)")
                
                # Chi-square if possible
                if len(theme_counts) == 2 and sum(theme_counts.values()) >= 5:
                    vals = list(theme_counts.values())
                    sizes = [len(df_analysis[df_analysis[grouping] == g]) for g in groups]
                    expected = [s / sum(sizes) * sum(vals) for s in sizes]
                    
                    if all(e > 0 for e in expected):
                        chi2 = sum((o - e)**2 / e for o, e in zip(vals, expected))
                        p = stats.chi2.sf(chi2, 1)
                        
                        if p < 0.10:
                            sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else '†'
                            results.append(f"    → Significant difference: χ²(1) = {chi2:.3f}, p = {p:.3f} {sig}")
    
    # =================================================================
    # ANALYSIS 3: Sentiment Analysis (if available)
    # =================================================================
    if TEXTBLOB_AVAILABLE:
        results.append("\n" + "-"*80)
        results.append("ANALYSIS 3: SENTIMENT ANALYSIS")
        results.append("-"*80 + "\n")
        
        # Calculate sentiment
        df_analysis['sentiment'] = df_analysis[question_col].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity if len(str(x)) > 10 else 0
        )
        
        df_analysis['sentiment_category'] = pd.cut(df_analysis['sentiment'], 
                                                     bins=[-1, -0.1, 0.1, 1],
                                                     labels=['Negative', 'Neutral', 'Positive'])
        
        for grouping, var_name in [('memory_function', 'Memory Function'),
                                    ('agent_personality', 'Agent Personality'),
                                    ('match_label', 'Personality Match')]:
            
            results.append(f"\nSentiment by {var_name}:")
            results.append("-" * 60)
            
            # Continuous sentiment
            sent_stats = df_analysis.groupby(grouping)['sentiment'].agg(['count', 'mean', 'std'])
            
            for idx, row in sent_stats.iterrows():
                results.append(f"  {idx}: M = {row['mean']:.3f} (SD = {row['std']:.3f}, n = {row['count']:.0f})")
            
            # Test
            groups = df_analysis[grouping].unique()
            if len(groups) == 2:
                g1 = df_analysis[df_analysis[grouping] == groups[0]]['sentiment'].dropna()
                g2 = df_analysis[df_analysis[grouping] == groups[1]]['sentiment'].dropna()
                
                if len(g1) > 1 and len(g2) > 1:
                    t, p = stats.ttest_ind(g1, g2)
                    sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else '†' if p < .10 else ''
                    results.append(f"  t-test: t = {t:.3f}, p = {p:.3f} {sig}")
            
            # Categorical sentiment
            results.append(f"\n  Sentiment Distribution:")
            sent_dist = pd.crosstab(df_analysis[grouping], 
                                     df_analysis['sentiment_category'], 
                                     normalize='index') * 100
            
            for idx, row in sent_dist.iterrows():
                results.append(f"    {idx}:")
                for cat in ['Negative', 'Neutral', 'Positive']:
                    if cat in sent_dist.columns:
                        results.append(f"      {cat}: {row[cat]:.1f}%")
            
            # Chi-square
            contingency = pd.crosstab(df_analysis[grouping], df_analysis['sentiment_category'])
            if len(groups) == 2 and contingency.size >= 4:
                try:
                    chi2, p, dof, expected = stats.chi2_contingency(contingency)
                    sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else '†' if p < .10 else ''
                    results.append(f"  χ²({dof}) = {chi2:.3f}, p = {p:.3f} {sig}")
                except:
                    pass
    
    # =================================================================
    # ANALYSIS 4: Distinctive Words by Condition
    # =================================================================
    results.append("\n" + "-"*80)
    results.append("ANALYSIS 4: DISTINCTIVE WORDS BY CONDITION")
    results.append("-"*80 + "\n")
    
    # Function to get top words
    def get_top_words(texts, n=15):
        all_text = ' '.join(texts).lower()
        # Remove common words
        stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'can', 'it', 'its', 'that', 'this',
                     'i', 'me', 'my', 'you', 'your', 'n/a', 'na', 'not', 'applicable']
        
        words = re.findall(r'\b[a-z]{3,}\b', all_text)
        words = [w for w in words if w not in stop_words]
        
        word_counts = Counter(words)
        return word_counts.most_common(n)
    
    for grouping, var_name in [('memory_function', 'Memory Function'),
                                ('agent_personality', 'Agent Personality'),
                                ('match_label', 'Personality Match')]:
        
        results.append(f"\nTop Words by {var_name}:")
        results.append("-" * 60)
        
        groups = df_analysis[grouping].unique()
        
        for group in groups:
            group_texts = df_analysis[df_analysis[grouping] == group][question_col].tolist()
            top_words = get_top_words(group_texts, n=10)
            
            results.append(f"\n  {group}:")
            for word, count in top_words:
                results.append(f"    {word}: {count}x")
    
    # =================================================================
    # ANALYSIS 5: Response Patterns
    # =================================================================
    results.append("\n" + "-"*80)
    results.append("ANALYSIS 5: RESPONSE PATTERNS")
    results.append("-"*80 + "\n")
    
    # Check for N/A responses
    na_patterns = ['n/a', 'na', 'not applicable', 'none', 'no similarities', 
                   'i did not notice', 'did not observe']
    
    df_analysis['is_na_response'] = df_analysis[question_col].str.lower().apply(
        lambda x: any(pattern in str(x).lower() for pattern in na_patterns)
    )
    
    results.append("N/A or Null Response Rates:")
    results.append("-" * 60)
    
    for grouping in ['memory_function', 'agent_personality', 'match_label']:
        na_rate = df_analysis.groupby(grouping)['is_na_response'].mean() * 100
        
        results.append(f"\nBy {grouping}:")
        for idx, val in na_rate.items():
            n_total = len(df_analysis[df_analysis[grouping] == idx])
            n_na = int(val * n_total / 100)
            results.append(f"  {idx}: {val:.1f}% ({n_na}/{n_total})")
    
    # Check for first-person vs third-person
    df_analysis['uses_first_person'] = df_analysis[question_col].str.lower().apply(
        lambda x: ' i ' in f' {str(x).lower()} ' or x.lower().startswith('i ')
    )
    
    results.append("\n\nFirst-Person Usage (\"I\"):")
    results.append("-" * 60)
    
    for grouping in ['memory_function', 'agent_personality', 'match_label']:
        fp_rate = df_analysis.groupby(grouping)['uses_first_person'].mean() * 100
        
        results.append(f"\nBy {grouping}:")
        for idx, val in fp_rate.items():
            results.append(f"  {idx}: {val:.1f}%")
    
    return results

def main():
    """Main execution"""
    
    import os
    os.makedirs('QUALITATIVE_ANALYSIS_RESULTS', exist_ok=True)
    
    # Load data
    df = load_data()
    
    # Define all questions to analyze
    questions = [
        ("In Task 1, Did you notice any similarities between yourself and the virtual agent in Task 1? If so, what similarities did you observe?",
         "Q1_Similarities_Observed"),
        
        ("If you do observe similarities, how did these similarities affect your interaction with the virtual agent?\n\nYou can leave N/A if you do not observe.",
         "Q2_Similarity_Effect"),
        
        ("In Task 1, the virtual agent sometimes referred to shared experiences (memory). How did this affect your trust in the virtual agent?\n\nYou can leave N/A if you do not observe any shared experiences.",
         "Q3_Memory_Trust_Effect"),
        
        ("In Task 1, we designed the agent's personality with certain characteristics. How would you describe the agent's personality in relation to your own? Did this affect your sense of connection or trust with the agent? Please explain your experience.",
         "Q4_Personality_Description"),
        
        ("During Task 1, what aspects of the interaction or the agent did you find most trustworthy? Can you explain why?",
         "Q5_Most_Trustworthy"),
        
        ("Conversely, were there any elements of the interaction or the agent in Task 1 that made you feel hesitant to trust the agent? If so, what were they and why did they affect your trust?",
         "Q6_Hesitant_Elements"),
        
        ("For Task 1, what factors did you consider when making decisions during the experiment?",
         "Q7_Decision_Factors"),
        
        ("For Task 1, Can you walk me through your thought process when deciding whether to follow or ignore the virtual agent's recommendations?",
         "Q8_Thought_Process")
    ]
    
    # Analyze each question
    all_results = []
    
    for question_col, question_name in questions:
        print(f"\n[Processing] {question_name}...")
        
        results = analyze_question(df, question_col, question_name, 
                                   f'QUALITATIVE_ANALYSIS_RESULTS/{question_name}_analysis.txt')
        
        all_results.extend(results)
        all_results.append("\n" + "="*80 + "\n")
        
        # Save individual question results
        with open(f'QUALITATIVE_ANALYSIS_RESULTS/{question_name}_analysis.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        
        print(f"  [OK] Saved: {question_name}_analysis.txt")
    
    # Save complete results
    with open('QUALITATIVE_ANALYSIS_RESULTS/COMPLETE_QUALITATIVE_ANALYSIS.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_results))
    
    print("\n" + "="*80)
    print("COMPLETE QUALITATIVE ANALYSIS FINISHED!")
    print("="*80)
    print(f"\nTotal Questions Analyzed: {len(questions)}")
    print(f"Output Files: {len(questions) + 1}")
    print("\nAll results saved in: QUALITATIVE_ANALYSIS_RESULTS/")
    print("\nGenerated Files:")
    print("  1. COMPLETE_QUALITATIVE_ANALYSIS.txt (all questions)")
    for i, (_, name) in enumerate(questions, 2):
        print(f"  {i}. {name}_analysis.txt")

if __name__ == "__main__":
    main()

