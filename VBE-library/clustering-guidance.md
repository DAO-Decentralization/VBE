# Clustering Guidance
The below information should be used to guide which clustering methods, as well as hyperparameters, are selected to calculate VBE.

Clustering methods may be selected following data best practices, and depend on the shape of the input data and cluster expectations. The methods introduced in the VBE library include K-Means, Hierarchical, Gaussian Mixture Model (GMM), Spectral, and DBSCAN. K-means can handle large datasets where clusters are evenly sized and is sensitive to outliers in data. Hierarchical clustering is better for smaller datasets where a dendrogram is useful, or clusters are expected at different levels of granularity. The Gaussian Mixture Model, Spectral, and DBSCAN are better for handling complex cluster shapes, non-linear relationships, varying densities, and noise in data. 

We additionally follow data best practices for use of entropy functions, optimization methods, and distance methods. Min entropy minimizes uncertainty in decision-making, max entropy ensures more fairness by exploring all possibilities, and Shannon entropy measures overall information content or cluster variability. Selection of optimization methods depends on intra-cluster variance, cluster definition, compactness and separation. For distance methods, Euclidean is preferred when a straight-line distance metric is preferred, Manhattan when data is sparse or when reducing sensitivity to outliers, Cosine for high-dimensional data, and Cityblock for grid-like or ordinal data.

| Category | Methods | When to Use |
|----------|----------|-------------|
| Clustering | K-Means | Use for large datasets when clusters are approximately spherical and evenly sized. Sensitive to outliers. |
| | Hierarchical | Use for small-to-medium datasets when a tree-like structure (dendrogram) is useful, or you expect clusters at different levels of granularity. |
| | Gaussian Mixture Model (GMM) | Use when clusters are ellipsoidal or overlap, and you want to model the probability of data belonging to each cluster. |
| | Spectral Clustering | Use for complex cluster shapes or when relationships between points are nonlinear. Works well with graph data. |
| | DBSCAN | Use for datasets with noise and varying cluster densities. Does not require predefining the number of clusters. |
| Entropy Functions | Min Entropy | Use when minimizing the uncertainty in decision-making (e.g., identifying the most confident clustering). |
| | Max Entropy | Use for applications that require exploring all possibilities or ensuring fairness. |
| | Shannon Entropy | Use for measuring overall information content or variability within the clusters. |
| Optimization Method | Silhouette Score | Use to assess cluster compactness and separation when the dataset has well-defined clusters. |
| | Gap Statistic | Use to determine the optimal number of clusters by comparing intra-cluster variance to random reference datasets. |
| | Davies-Bouldin Index | Use when you want a score that considers both cluster compactness and separation (lower is better). |
| | Calinski-Harabasz Index | Use for a fast and efficient way to evaluate clusters based on their compactness and separation (higher is better). |
| Distance Method | Euclidean (L2) | Use for numerical data when the notion of straight-line distance is meaningful. |
| | Manhattan (L1) | Use when data is sparse or you want to reduce sensitivity to outliers. |
| | Cosine | Use for high-dimensional data (e.g., text or documents) to measure similarity based on direction rather than magnitude. |
| | Cityblock | Equivalent to Manhattan distance, suitable for grid-like or ordinal data. |
| | L1 Norm | Equivalent to Manhattan distance; use for sparse data or absolute deviations. |
| | L2 Norm | Equivalent to Euclidean distance; use when a straight-line distance metric is preferred. |