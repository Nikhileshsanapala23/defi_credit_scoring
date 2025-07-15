# DeFi Wallet Credit Scoring System

This system calculates credit scores (0-1000) for cryptocurrency wallets based on their historical transactions with Aave V2 protocol.

## Methodology

### Feature Engineering
1. **Activity Metrics**: Transaction count, active days, frequency
2. **Volume Metrics**: Total USD volume, average transaction size
3. **Risk Indicators**: Borrow/repay ratio, liquidation events, recent activity
4. **Behavior Patterns**: Deposit/withdrawal patterns, collateral turnover

### Scoring Model
- **Weighted Approach**:
  - Activity (30%): Measures engagement with protocol
  - Volume (25%): Reflects economic significance
  - Risk (35%): Assesses financial responsibility
  - Behavior (10%): Evaluates usage patterns

- **Normalization**: Raw scores are scaled to 0-1000 range

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
Run scoring:

bash
python score_wallets.py
Outputs:

wallet_credit_scores.csv: Wallet addresses with credit scores

score_distribution.png: Histogram of score distribution

behavior_patterns.png: Behavioral patterns by score range

score_range_analysis.md: Detailed metrics by score range

Interpretation
800-1000: Highly reliable, long-term users with responsible borrowing

600-800: Regular users with good repayment history

400-600: Moderate risk, some borrowing but inconsistent repayment

200-400: High risk, potential over-leverage or liquidation history

0-200: Very high risk, possible bot-like or exploitative behavior

text

### 4. analysis.md

```markdown
# Credit Score Analysis

## Score Distribution
![Score Distribution](score_distribution.png)

## Behavioral Patterns by Score Range
![Behavior Patterns](behavior_patterns.png)

## Key Findings

### High-Score Wallets (800-1000)
- Long history of protocol interaction
- High deposit-to-borrow ratio
- Rare liquidations
- Consistent repayment behavior
- Diversified asset usage

### Medium-Score Wallets (400-800)
- Moderate transaction frequency
- Some borrowing activity
- Occasional late repayments
- Limited liquidation history

### Low-Score Wallets (0-400)
- High borrow/repay ratios
- Frequent liquidations
- Short interaction history
- Concentrated asset usage
- Potential bot-like behavior (high-frequency, small transactions)

## Recommendations
1. **Risk Management**: Use scores to set borrowing limits
2. **Incentivization**: Reward high-score wallets with better rates
3. **Monitoring**: Flag low-score wallets for potential risks