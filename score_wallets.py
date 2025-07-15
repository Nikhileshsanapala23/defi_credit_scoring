# score_wallets.py
import json
import pandas as pd
from utils.feature_engineering import process_transactions, calculate_wallet_features
from utils.scoring import calculate_credit_scores
from utils.visualization import plot_score_distribution, analyze_score_ranges

def load_data(file_path):
    """Load JSON transaction data"""
    with open(file_path) as f:
        data = json.load(f)
    return pd.DataFrame(data)

def main(input_file):
    # Load and preprocess data
    df = load_data(input_file)
    
    # Process transactions and calculate features
    processed_df = process_transactions(df)
    wallet_features = calculate_wallet_features(processed_df)
    
    # Calculate credit scores
    wallet_scores = calculate_credit_scores(wallet_features)
    
    # Generate analysis and visualizations
    plot_score_distribution(wallet_scores)
    analyze_score_ranges(wallet_scores, processed_df)
    
    return wallet_scores

if __name__ == "__main__":
    input_file = "user-wallet-transactions.json"
    scores = main(input_file)
    scores.to_csv("wallet_credit_scores.csv", index=False)