# ValueLens: RFM Business Segmentation Rules

This document outlines the heuristic business rules used to segment our customer base, detailing the mathematical conditions and the strategic marketing rationale behind each segment.

## 1. Champions
- **Rule**: `R >= 4` AND `F >= 4`
- **Behavior**: These customers bought very recently and they buy very often. They are the core drivers of revenue and word-of-mouth.
- **Marketing Perspective**: Do not bombard them with deep discount margins (they will buy anyway). Instead, reward their loyalty. Give them early access to new products, invite them to VIP events, or ask them for reviews and referrals. 

## 2. Loyal Customers
- **Rule**: `R >= 3` AND `F >= 3` (but not qualifying as Champions)
- **Behavior**: Solid, reliable customers who purchase with decent frequency and recency.
- **Marketing Perspective**: The goal here is upselling and cross-selling. Recommend higher-value items based on their past purchases to increase their Average Order Value (AOV) and nudge them toward becoming Champions.

## 3. At Risk (High Value)
- **Rule**: `R <= 2` AND `F >= 4`
- **Behavior**: These are customers who *used* to buy very frequently, but haven't made a purchase in a long time. 
- **Marketing Perspective**: This is a critical segment. Losing them means losing guaranteed, high-frequency revenue. Marketing should deploy aggressive win-back campaigns here—personalized emails, deep "we miss you" discounts, or phone calls from account managers to investigate why they stopped buying.

## 4. Lost
- **Rule**: `R <= 2` AND `F <= 2`
- **Behavior**: They bought a long time ago and only bought once or twice. 
- **Marketing Perspective**: Do not waste expensive marketing budget (like retargeting ads or direct mail) on this segment. If you communicate with them, stick to cheap, automated channels (like a standard newsletter blast) or ignore them entirely to preserve Return on Ad Spend (ROAS).

## 5. Potential Loyalist
- **Rule**: Everything else (e.g., `R=4, F=2` or `R=3, F=1`)
- **Behavior**: These are typically recent customers with lower frequency (new customers), or mid-tier customers who haven't fully committed to the brand yet.
- **Marketing Perspective**: The primary goal is retention and habit-building. Offer them onboarding support, recommend top-selling starter items, or provide a limited-time second-purchase discount to incentivize them to return quickly.
