# ValueLens: K-Means Cluster Interpretation

By feeding the log-transformed, standardized RFM variables into a K-Means algorithm (K=4), the machine independently identified natural groupings within the customer base. Without providing the algorithm any of our prior business rules, we can profile its output to see what mathematical boundaries it discovered.

## Cluster 1: The "Whales" (Algorithmic Champions)
- **Size**: 630 customers (16.1% of base)
- **Revenue**: £4.54M (62.7% of total revenue)
- **Averages**: Recency: 11.5 days | Frequency: 13.7 | Monetary: £7,204
- **Interpretation**: This is the ultra-high-value segment. The algorithm correctly identified the extreme right-tail of our dataset (the B2B wholesale buyers). They buy incredibly often, spend massive amounts, and purchased very recently. Interestingly, the algorithm restricted this group to just 16% of the base (compared to the 25% our heuristic rules identified as Champions), suggesting our manual rules were slightly too lenient in defining top-tier status.

## Cluster 0: The "Core Middle" (Loyal & At-Risk Blend)
- **Size**: 1,055 customers (26.9% of base)
- **Revenue**: £1.82M (25.2% of total revenue)
- **Averages**: Recency: 68.3 days | Frequency: 4.2 | Monetary: £1,727
- **Interpretation**: This represents the solid, reliable middle-tier of the business. They have decent frequency (4 purchases) and respectable spend, but their Recency is slightly elevated (~2 months ago). This algorithmic cluster likely absorbed the majority of our heuristic "Loyal Customers" and the highly valuable "At Risk" segment. They are crucial to the business's stability.

## Cluster 2: The "New Arrivals" (Potential Loyalists)
- **Size**: 771 customers (19.7% of base)
- **Revenue**: £400k (5.5% of total revenue)
- **Averages**: Recency: 19.2 days | Frequency: 2.1 | Monetary: £519
- **Interpretation**: This cluster is defined by exceptionally low Recency (they bought just 19 days ago on average) but very low Frequency (2 purchases) and Monetary value. The algorithm perfectly identified our "Potential Loyalists"—recent acqusitions who have not yet established a deep buying habit. 

## Cluster 3: The "Churned Tail" (Lost Customers)
- **Size**: 1,461 customers (37.3% of base)
- **Revenue**: £483k (6.7% of total revenue)
- **Averages**: Recency: 183.2 days | Frequency: 1.3 | Monetary: £330
- **Interpretation**: The algorithm dumped the vast majority of low-value, inactive accounts into this massive bucket. They haven't purchased in half a year (183 days), and only bought ~1 time ever. Despite being the largest group by headcount (37%), they are financially irrelevant to the business's bottom line.
