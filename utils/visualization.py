# utils/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_score_distribution(scores):
    """Plot distribution of credit scores"""
    plt.figure(figsize=(12, 6))
    
    # Create bins for visualization
    bins = list(range(0, 1001, 100))
    score_bins = pd.cut(scores['credit_score'], bins=bins)
    bin_counts = score_bins.value_counts().sort_index()
    
    # Plot
    ax = sns.barplot(x=bin_counts.index.astype(str), y=bin_counts.values, palette="viridis")
    ax.set_title('Wallet Credit Score Distribution')
    ax.set_xlabel('Credit Score Range')
    ax.set_ylabel('Number of Wallets')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('score_distribution.png')
    plt.close()

def analyze_score_ranges(scores, transactions):
    """Analyze wallet behavior in different score ranges"""
    # Define score ranges
    ranges = [(0, 200), (200, 400), (400, 600), (600, 800), (800, 1000)]
    analysis = []
    
    for low, high in ranges:
        wallets = scores[(scores['credit_score'] >= low) & (scores['credit_score'] < high)]['wallet']
        subset = transactions[transactions['userWallet'].isin(wallets)]
        
        # Calculate metrics for this range
        metrics = {
            'score_range': f"{low}-{high}",
            'wallet_count': len(wallets),
            'avg_tx_count': subset.groupby('userWallet').size().mean(),
            'deposit_ratio': len(subset[subset['action'] == 'deposit']) / len(subset),
            'borrow_ratio': len(subset[subset['action'] == 'borrow']) / len(subset),
            'liquidation_rate': len(subset[subset['action'] == 'liquidationcall']) / len(subset),
            'avg_usd_value': subset['usd_value'].mean()
        }
        analysis.append(metrics)
    
    # Convert to DataFrame and save
    analysis_df = pd.DataFrame(analysis)
    analysis_df.to_markdown('score_range_analysis.md', index=False)
    
    # Plot behavioral patterns
    plt.figure(figsize=(14, 8))
    for metric in ['deposit_ratio', 'borrow_ratio', 'liquidation_rate']:
        sns.lineplot(x='score_range', y=metric, data=analysis_df, marker='o', label=metric)
    plt.title('Behavioral Patterns by Credit Score Range')
    plt.xlabel('Credit Score Range')
    plt.ylabel('Ratio')
    plt.legend()
    plt.tight_layout()
    plt.savefig('behavior_patterns.png')
    plt.close()