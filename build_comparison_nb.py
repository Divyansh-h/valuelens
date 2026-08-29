import json
import os

nb = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# K-Means vs Gaussian Mixture Model (GMM)\n",
    "\n",
    "This notebook evaluates if allowing soft assignments and ellipsoidal clusters (via GMM) provides a better segmentation of our customers compared to the strict spherical boundaries of K-Means. We will use the Adjusted Rand Index (ARI) to measure how similarly they segment the customer base."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import os\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.mixture import GaussianMixture\n",
    "from sklearn.metrics import adjusted_rand_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "import sys\n",
    "sys.path.append(os.path.join(os.getcwd(), '../src'))\n",
    "from clustering import load_and_preprocess_rfm\n",
    "\n",
    "# Set visualization style\n",
    "sns.set_theme(style=\"whitegrid\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Load and Prepare Data\n",
    "We load the log-transformed RFM features and split the data, maintaining the pipeline architecture developed earlier."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load data\n",
    "df, rfm_log = load_and_preprocess_rfm()\n",
    "\n",
    "# Split to prevent data leakage in standardizer\n",
    "X_train, X_test = train_test_split(rfm_log, test_size=0.2, random_state=42)\n",
    "print(f\"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Fit K-Means Pipeline\n",
    "We use K=4 for a granular business segmentation based on earlier silhouette evaluations."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "k = 4\n",
    "\n",
    "kmeans_pipeline = Pipeline([\n",
    "    ('scaler', StandardScaler()),\n",
    "    ('kmeans', KMeans(n_clusters=k, random_state=42, n_init=10))\n",
    "])\n",
    "\n",
    "kmeans_pipeline.fit(X_train)\n",
    "kmeans_labels = kmeans_pipeline.predict(rfm_log)\n",
    "df['KMeans_Cluster'] = kmeans_labels"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Fit Gaussian Mixture Model Pipeline\n",
    "GMM allows for covariance estimation, meaning clusters can be elliptical rather than strictly spherical, potentially capturing skewed customer distributions better."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "gmm_pipeline = Pipeline([\n",
    "    ('scaler', StandardScaler()),\n",
    "    ('gmm', GaussianMixture(n_components=k, random_state=42, n_init=10))\n",
    "])\n",
    "\n",
    "gmm_pipeline.fit(X_train)\n",
    "gmm_labels = gmm_pipeline.predict(rfm_log)\n",
    "df['GMM_Cluster'] = gmm_labels"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Compare using Adjusted Rand Index (ARI)\n",
    "The ARI measures the similarity between two cluster assignments, ignoring permutations and normalizing against random chance. 1.0 indicates identical clustering."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "ari_score = adjusted_rand_score(kmeans_labels, gmm_labels)\n",
    "print(f\"Adjusted Rand Index between K-Means and GMM: {ari_score:.4f}\")\n",
    "\n",
    "if ari_score > 0.8:\n",
    "    print(\"Conclusion: K-Means and GMM produced highly similar clusters. The spherical assumption of K-Means is sufficient.\")\n",
    "else:\n",
    "    print(\"Conclusion: GMM produced significantly different clusters, suggesting the covariance structure captured non-spherical shapes that K-Means missed.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Visual Comparison\n",
    "Plotting the resulting segments against Recency and Monetary values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))\n",
    "\n",
    "sns.scatterplot(data=df, x='Recency', y='Monetary', hue='KMeans_Cluster', palette='viridis', alpha=0.6, ax=ax1)\n",
    "ax1.set_title('K-Means Assignments', fontsize=14)\n",
    "ax1.set_yscale('log')\n",
    "ax1.set_xscale('log')\n",
    "\n",
    "sns.scatterplot(data=df, x='Recency', y='Monetary', hue='GMM_Cluster', palette='viridis', alpha=0.6, ax=ax2)\n",
    "ax2.set_title('GMM Assignments', fontsize=14)\n",
    "ax2.set_yscale('log')\n",
    "ax2.set_xscale('log')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/clustering_comparison.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
print("Notebook written to notebooks/clustering_comparison.ipynb")
