import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class RFMSegmenter(BaseEstimator, TransformerMixin):
    """
    A scikit-learn compatible transformer that assigns RFM scores (1-5) and 
    business segments based on Recency, Frequency, and Monetary values.
    
    This allows new, unseen transaction data to be scored consistently 
    against the original historical quintile thresholds without retraining.
    """
    
    def __init__(self, num_quintiles=5):
        self.num_quintiles = num_quintiles
        self.r_bins_ = None
        self.f_bins_ = None
        self.m_bins_ = None
        
    def _compute_bins(self, series, reverse=False):
        """Computes bin edges for qcut, ensuring unique edges."""
        # Rank the data first to handle many identical values (like Frequency=1)
        # method='first' assigns unique ranks so qcut never fails with "Bin edges must be unique"
        ranked = series.rank(method='first')
        
        # Calculate thresholds
        # If reverse=True (for Recency, where lower is better), we want the lowest values to get score 5
        # pd.qcut assigns labels 0 to n-1. 
        # If reverse=True, we use labels [5, 4, 3, 2, 1]
        # Otherwise, [1, 2, 3, 4, 5]
        
        # We just need to fit the qcut and return the bin edges
        _, bins = pd.qcut(ranked, q=self.num_quintiles, retbins=True)
        
        # Map the ranked bins back to original value thresholds
        # Actually, if we just store the quantiles of the original series, it's easier to apply via pd.cut
        quantiles = np.linspace(0, 1, self.num_quintiles + 1)
        edges = series.quantile(quantiles).values
        
        # Ensure edges are strictly increasing to avoid pd.cut errors on transform
        # If many customers have Frequency=1, the 0th, 1st, 2nd quantiles might all be 1.0.
        # To make it strictly increasing, we can add a tiny epsilon or use rank-based transform.
        # For a truly robust production transform on NEW data, saving the exact quantile edges 
        # and using `np.digitize` or `pd.cut(duplicates='drop')` is safer.
        edges[0] = -np.inf
        edges[-1] = np.inf
        
        # Make edges unique. If unique edges < num_quintiles+1, 
        # some scores won't be assigned, which matches SQL NTILE behavior loosely.
        unique_edges = np.unique(edges)
        return unique_edges
        
    def fit(self, X, y=None):
        """
        Fits the quintile thresholds on the training data.
        X must be a DataFrame containing 'Recency', 'Frequency', and 'Monetary'.
        """
        # Ensure we have the right columns
        required_cols = ['Recency', 'Frequency', 'Monetary']
        for col in required_cols:
            if col not in X.columns:
                raise ValueError(f"Missing required column: {col}")
                
        self.r_bins_ = self._compute_bins(X['Recency'])
        self.f_bins_ = self._compute_bins(X['Frequency'])
        self.m_bins_ = self._compute_bins(X['Monetary'])
        
        return self
        
    def _assign_scores(self, series, bins, reverse=False):
        """Assigns 1-5 scores based on pre-fitted bins."""
        labels = list(range(1, len(bins)))
        if reverse:
            labels = labels[::-1] # e.g. [5, 4, 3, 2, 1] if len(bins)==6
            
        scores = pd.cut(series, bins=bins, labels=labels, include_lowest=True, duplicates='drop')
        
        # If dropping duplicates resulted in fewer bins than labels, pd.cut handles it poorly if labels length doesn't match bins-1.
        # So we construct labels dynamically based on unique bins.
        actual_labels = list(range(1, len(bins)))
        if reverse:
            actual_labels = actual_labels[::-1]
            
        return pd.cut(series, bins=bins, labels=actual_labels, include_lowest=True)

    def transform(self, X):
        """
        Transforms new data by applying the fitted quintile thresholds and assigning business segments.
        """
        if self.r_bins_ is None:
            raise NotFittedError("This RFMSegmenter instance is not fitted yet. Call 'fit' first.")
            
        X_out = X.copy()
        
        # Recency: Lower is better (score 5)
        X_out['R_Score'] = self._assign_scores(X_out['Recency'], self.r_bins_, reverse=True).astype(float).fillna(1.0).astype(int)
        
        # Frequency and Monetary: Higher is better (score 5)
        X_out['F_Score'] = self._assign_scores(X_out['Frequency'], self.f_bins_, reverse=False).astype(float).fillna(1.0).astype(int)
        X_out['M_Score'] = self._assign_scores(X_out['Monetary'], self.m_bins_, reverse=False).astype(float).fillna(1.0).astype(int)
        
        X_out['RFM_Score'] = X_out['R_Score'].astype(str) + X_out['F_Score'].astype(str) + X_out['M_Score'].astype(str)
        
        # Apply Segmentation Rules
        X_out['Segment'] = X_out.apply(self._assign_segment_rule, axis=1)
        
        return X_out
        
    def _assign_segment_rule(self, row):
        """Internal heuristic segmentation rule."""
        r = row['R_Score']
        f = row['F_Score']
        
        if r >= 4 and f >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r <= 2 and f >= 4:
            return 'At Risk (High Value)'
        elif r <= 2 and f <= 2:
            return 'Lost'
        else:
            return 'Potential Loyalist'
