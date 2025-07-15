# utils/scoring.py
import numpy as np

def calculate_credit_scores(wallet_features):
    """Calculate credit scores (0-1000) based on wallet features"""
    # Normalize features
    features = wallet_features.copy()
    
    # Activity score (weight: 30%)
    features['activity_score'] = (
        0.4 * np.log1p(features['tx_count']) +
        0.3 * np.log1p(features['active_days']) +
        0.3 * np.clip(features['tx_frequency'], 0, 10)
    
    # Volume score (weight: 25%)
    features['volume_score'] = (
        0.6 * np.log1p(features['total_volume']) +
        0.4 * np.log1p(features['avg_tx_size']))
    
    # Risk score (weight: 35%)
    features['risk_score'] = (
        -0.4 * np.log1p(features['borrow_repay_ratio']) +
        -0.3 * features['liquidation_count'] +
        -0.2 * features['recent_activity'] +
        0.1 * (1 - features['asset_concentration']))
    
    # Behavior score (weight: 10%)
    features['behavior_score'] = (
        0.5 * (features['deposit_count'] / features['tx_count']) +
        0.3 * (features['repay_count'] / max(1, features['borrow_count'])) +
        0.2 * np.log1p(features['collateral_turnover']))
    
    # Combine scores with weights
    features['raw_score'] = (
        0.30 * features['activity_score'] +
        0.25 * features['volume_score'] +
        0.35 * features['risk_score'] +
        0.10 * features['behavior_score'])
    
    # Normalize to 0-1000 range
    min_score = features['raw_score'].min()
    max_score = features['raw_score'].max()
    features['credit_score'] = 1000 * (features['raw_score'] - min_score) / (max_score - min_score)
    
    # Round to nearest integer
    features['credit_score'] = features['credit_score'].round().astype(int)
    
    return features[['wallet', 'credit_score'] + [col for col in features.columns if col.endswith('_score')]]