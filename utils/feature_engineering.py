# utils/feature_engineering.py
import pandas as pd
import numpy as np
from datetime import datetime

def process_transactions(df):
    """Process raw transaction data into structured format"""
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Extract action data
    action_data = pd.json_normalize(df['actionData'])
    df = pd.concat([df.drop(['actionData'], axis=1), action_data], axis=1)
    
    # Convert amounts to numeric values
    df['amount'] = pd.to_numeric(df['amount'])
    df['assetPriceUSD'] = pd.to_numeric(df['assetPriceUSD'])
    
    # Calculate USD value of each transaction
    df['usd_value'] = df['amount'] * df['assetPriceUSD']
    
    return df

def calculate_wallet_features(df):
    """Calculate wallet-level features from transactions"""
    features = []
    
    for wallet, group in df.groupby('userWallet'):
        # Basic activity metrics
        first_tx = group['timestamp'].min()
        last_tx = group['timestamp'].max()
        tx_count = len(group)
        active_days = (last_tx - first_tx).days + 1
        
        # Transaction type distribution
        action_counts = group['action'].value_counts().to_dict()
        
        # Asset concentration
        asset_counts = group['assetSymbol'].value_counts().to_dict()
        
        # Volume metrics
        total_volume = group['usd_value'].sum()
        avg_tx_size = group['usd_value'].mean()
        
        # Risk indicators
        borrow_repay_ratio = action_counts.get('borrow', 0) / max(1, action_counts.get('repay', 0))
        liquidation_count = action_counts.get('liquidationcall', 0)
        
        # Time-based metrics
        recent_activity = (datetime.now() - last_tx).days
        
        # Collateralization behavior
        collateral_actions = group[group['action'].isin(['deposit', 'redeemunderlying'])]
        collateral_turnover = collateral_actions['usd_value'].sum() / max(1, collateral_actions['usd_value'].mean())
        
        features.append({
            'wallet': wallet,
            'tx_count': tx_count,
            'active_days': active_days,
            'tx_frequency': tx_count / max(1, active_days),
            'deposit_count': action_counts.get('deposit', 0),
            'borrow_count': action_counts.get('borrow', 0),
            'repay_count': action_counts.get('repay', 0),
            'redeem_count': action_counts.get('redeemunderlying', 0),
            'liquidation_count': liquidation_count,
            'unique_assets': len(asset_counts),
            'total_volume': total_volume,
            'avg_tx_size': avg_tx_size,
            'borrow_repay_ratio': borrow_repay_ratio,
            'recent_activity': recent_activity,
            'collateral_turnover': collateral_turnover,
            'asset_concentration': max(asset_counts.values()) / sum(asset_counts.values()) if asset_counts else 0
        })
    
    return pd.DataFrame(features)