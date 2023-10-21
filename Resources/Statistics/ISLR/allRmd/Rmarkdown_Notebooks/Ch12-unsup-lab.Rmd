---
title: "Ch12-unsup-lab"
jupyter:
  jupytext:
    formats: ipynb,Rmd
    text_representation:
      extension: .Rmd
      format_name: rmarkdown
      format_version: '1.2'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: R
    language: R
    name: ir
---


# Lab: Unsupervised Learning
## Principal Components Analysis

In this lab, we perform PCA on the `USArrests` data set, which is part of the base `R` package.
The rows of the data set contain the 50 states, in alphabetical order.

```{r chunk1}
states <- row.names(USArrests)
states
```

The columns of the data set contain the four variables.

```{r chunk2}
names(USArrests)
```

We first briefly examine the data. We notice that the variables have vastly different means.

```{r chunk3}
apply(USArrests, 2, mean)
```

Note that the `apply()` function allows us to apply a function---in this case, the `mean()` function---to each row or column of the data set. The second input here denotes whether we wish to compute the mean of the rows, $1$, or the columns, $2$. We see that there are on average three times as many rapes as murders, and more than eight times as many assaults as rapes.
We can also examine the variances of the four variables using the `apply()` function.

```{r chunk4}
apply(USArrests, 2, var)
```

Not surprisingly, the variables also have vastly different variances:
 the `UrbanPop` variable measures the percentage of the population in each state living in an urban area, which is not a comparable number to the number of rapes
in each state per 100,000 individuals.
If we failed to scale the variables before performing PCA, then most of the principal components that we observed would be driven by the `Assault` variable, since it has by far the largest mean and variance.
Thus, it is important to standardize the variables to have mean zero and standard deviation one before performing PCA.

We now perform principal components analysis using the `prcomp()` function, which is one of several functions in `R` that perform PCA.

```{r chunk5}
pr.out <- prcomp(USArrests, scale = TRUE)
```

By default, the `prcomp()` function centers the variables to have
mean zero. By using the option `scale = TRUE`, we scale the
variables to have standard deviation one. The output from
`prcomp()` contains a number of useful quantities.

```{r chunk6}
names(pr.out)
```

The `center` and `scale` components correspond to the means and standard deviations of the variables that were used for scaling prior to implementing PCA.

```{r chunk7}
pr.out$center
pr.out$scale
```

The `rotation` matrix provides the principal component loadings;
each column of `pr.out$rotation` contains the corresponding
principal component loading vector. ( *This function names it the rotation matrix, because when we matrix-multiply the $\bf X$   matrix by `pr.out$rotation`, it gives us the coordinates of the   data in the rotated coordinate system. These coordinates are the  principal component scores.* )


```{r chunk8}
pr.out$rotation
```

We see that there are four distinct principal components. This is to
be expected because there are in general $\min(n-1,p)$ informative
principal components in a data set with $n$ observations and $p$
variables.

Using the `prcomp()` function, we do not need to explicitly multiply the data by the principal component loading vectors  in order to obtain the principal component score vectors. Rather the $50 \times 4$ matrix `x` has as its columns the principal component score vectors. That is, the $k$th column is the $k$th principal component score vector.

```{r chunk9}
dim(pr.out$x)
```

We can plot the first two principal components as follows:

```{r chunk10}
biplot(pr.out, scale = 0)
```

The `scale = 0` argument to `biplot()` ensures that the arrows are scaled to represent the loadings; other values for `scale` give slightly different biplots with different interpretations.

Notice that this figure is a mirror image of Figure 12.1. Recall that the principal components are only unique up to a sign change, so we can reproduce Figure 12.1 by making a few small changes:

```{r chunk11}
pr.out$rotation = -pr.out$rotation
pr.out$x = -pr.out$x
biplot(pr.out, scale = 0)
```



The `prcomp()` function also outputs the standard deviation of each principal component. For instance, on the `USArrests` data set, we can access these standard deviations as follows:

```{r chunk12}
pr.out$sdev
```

The variance explained by each principal component is obtained by squaring these:

```{r chunk13}
pr.var <- pr.out$sdev^2
pr.var
```

To compute the proportion of variance explained by each principal component, we simply divide the variance explained by each principal component by the total variance explained by all four principal components:

```{r chunk14}
pve <- pr.var / sum(pr.var)
pve
```

We see that the first principal component explains $62.0\,\%$ of the variance in the data, the next principal component explains $24.7\,\%$ of the variance, and so forth.
 We can plot the PVE explained by each component, as well as the cumulative PVE, as follows:

```{r chunk15}
par(mfrow = c(1, 2))
plot(pve, xlab = "Principal Component",
    ylab = "Proportion of Variance Explained", ylim = c(0, 1),
    type = "b")
plot(cumsum(pve), xlab = "Principal Component",
    ylab = "Cumulative Proportion of Variance Explained",
    ylim = c(0, 1), type = "b")
```

 The result is shown in Figure 12.3.
Note that the function `cumsum()` computes the cumulative sum of the elements of  a numeric vector. For instance:

```{r chunk16}
a <- c(1, 2, 8, -3)
cumsum(a)
```



## Matrix Completion 
We now re-create the analysis carried out on the \USArrests\ data in
Section 12.3. We turn the data frame into a
matrix, after centering and scaling each column to have mean zero and
variance one.

```{r chunk17}
X <- data.matrix(scale(USArrests))
pcob <- prcomp(X)
summary(pcob)
```

We see that the first principal component explains $62\%$ of the
variance. 

We saw in Section 12.2.2 that solving the optimization
problem~(12.6)  on a centered data matrix $\bf X$ is
equivalent to computing the first $M$ principal
components of the data. The 
(SVD)  is a general algorithm for solving (12.6).

```{r chunk18}
sX <- svd(X)
names(sX)
round(sX$v, 3)
```

The `svd()` function returns three components, `u`, `d`, and `v`. The matrix `v` is equivalent to the
loading matrix from principal components (up to an unimportant sign flip).

```{r chunk19}
pcob$rotation
```

The matrix `u` is equivalent to the matrix of *standardized*
scores, and the standard deviations are in the vector `d`. We can recover the score vectors using the output of `svd()`.
They are identical to the score vectors output by `prcomp()`.

```{r chunk20}
t(sX$d * t(sX$u))
pcob$x
```

While it would be possible to carry out this lab using the `prcomp()` function,
here we use the `svd()` function in order to illustrate its use.


We now omit 20 entries in the $50\times 2$ data matrix at random. We do so
by first selecting 20 rows (states) at random, and then selecting one
of the four entries in each row at random. This ensures that every row has
at least three observed values.


```{r chunk21}
nomit <- 20
set.seed(15)
ina <- sample(seq(50), nomit)
inb <- sample(1:4, nomit, replace = TRUE)
Xna <- X
index.na <- cbind(ina, inb)
Xna[index.na] <- NA
```

Here, `ina`
contains 20 integers from 1 to 50; this represents the states that are selected to contain missing values. And `inb` contains
20 integers from 1 to 4, representing the features that contain the missing values for each of the selected states.
To perform the final indexing, we create `index.na`, a two-column
matrix whose columns are `ina` and `inb`. We have indexed a matrix with a
matrix of indices!

We now write some code to implement
Algorithm 12.1.
We first write a  function that takes in a matrix, and returns an approximation to the matrix using the `svd()` function.
  This will be needed in Step 2 of Algorithm 12.1.  As mentioned earlier, we could do this using the `prcomp()` function, but instead we use the `svd()` function for illustration.

```{r chunk22}
fit.svd <- function(X, M = 1) {
   svdob <- svd(X)
   with(svdob,
       u[, 1:M, drop = FALSE] %*%
       (d[1:M] * t(v[, 1:M, drop = FALSE]))
     )
}
```

Here, we did not bother to explicitly call the `return()` function to return a value from `fit.svd()`; however,
the computed quantity is automatically returned by `R`.  We use the `with()` function to
make it a little easier to index the elements of `svdob`. As an alternative to using `with()`, we could have written

```{r chunk23}

```

inside the `fit.svd()` function.

To conduct Step 1 of the algorithm, we initialize `Xhat` --- this is $\tilde{\bf X}$ in Algorithm 12.1 --- by replacing
the missing values with the column means of the non-missing entries.

```{r chunk24}
Xhat <- Xna
xbar <- colMeans(Xna, na.rm = TRUE)
Xhat[index.na] <- xbar[inb]
```


Before we begin Step 2, we set ourselves up to measure the progress of our
iterations:

```{r chunk25}
thresh <- 1e-7
rel_err <- 1
iter <- 0
ismiss <- is.na(Xna)
mssold <- mean((scale(Xna, xbar, FALSE)[!ismiss])^2)
mss0 <- mean(Xna[!ismiss]^2)
```

Here  `ismiss` is a new logical matrix with the same dimensions as `Xna`; a given element equals `TRUE` if the corresponding matrix element is missing. This is useful
because it allows us to access both the missing and non-missing entries. We store the mean of the squared non-missing elements in `mss0`.
We store the mean squared error  of the non-missing elements  of the old version of `Xhat` in `mssold`. We plan to store the mean squared error of the non-missing elements of the current version of `Xhat` in `mss`, and will then  iterate Step 2 of Algorithm 12.1 until the *relative error*, defined as 

`(mssold - mss) / mss0`, falls below `thresh = 1e-7`. ( *Algorithm 12.1  tells us to iterate Step 2 until (12.14) is no longer decreasing. Determining whether (12.14)  is decreasing requires us only to keep track of `mssold - mss`. However, in practice, we keep track of `(mssold - mss) / mss0` instead: this makes it so that the number of iterations required for Algorithm 12.1 to converge does not depend on whether we multiplied the raw data $\bf X$ by a constant factor.* )


In Step 2(a) of Algorithm 12.1, we  approximate `Xhat` using `fit.svd()`; we call this `Xapp`.   In Step 2(b), we  use `Xapp`  to update the estimates for elements in `Xhat` that are missing in `Xna`. Finally, in Step 2(c), we compute the relative error. These three steps are contained in this `while()` loop:

```{r chunk26}
while(rel_err > thresh) {
    iter <- iter + 1
    # Step 2(a)
    Xapp <- fit.svd(Xhat, M = 1)
    # Step 2(b)
    Xhat[ismiss] <- Xapp[ismiss]
    # Step 2(c)
    mss <- mean(((Xna - Xapp)[!ismiss])^2)
    rel_err <- (mssold - mss) / mss0
    mssold <- mss
    cat("Iter:", iter, "MSS:", mss,
      "Rel. Err:", rel_err, "\n")
    }
```

We see that after eight iterations, the relative error has fallen below `thresh = 1e-7`, and so the algorithm terminates. When this happens, the mean squared error of the non-missing elements equals $0.369$.

Finally, we compute the correlation between the 20 imputed values
and the actual values:

```{r chunk27}
cor(Xapp[ismiss], X[ismiss])
```



In this lab, we implemented Algorithm 12.1 ourselves for didactic purposes. However, a reader who wishes to apply matrix completion to their data should use the `softImpute` package on `CRAN`, which provides a very efficient implementation of a generalization of this algorithm.

## Clustering

### $K$-Means Clustering


The function `kmeans()` performs $K$-means clustering in
`R`.  We begin with a simple simulated example in which there
truly are two clusters in the data: the first 25 observations have a
mean shift relative to the next 25 observations.

```{r chunk28}
set.seed(2)
x <- matrix(rnorm(50 * 2), ncol = 2)
x[1:25, 1] <- x[1:25, 1] + 3
x[1:25, 2] <- x[1:25, 2] - 4
```




We now perform $K$-means clustering with $K=2$.

```{r chunk29}
km.out <- kmeans(x, 2, nstart = 20)
```

The cluster assignments of the 50 observations are contained in  `km.out$cluster`.

```{r chunk30}
km.out$cluster
```

The $K$-means clustering perfectly separated the observations into two clusters even though we did not supply any group information to `kmeans()`. We can plot the data, with each observation
colored according to its cluster assignment.

```{r chunk31}
plot(x, col = (km.out$cluster + 1),
    main = "K-Means Clustering Results with K = 2",
    xlab = "", ylab = "", pch = 20, cex = 2)
```

Here the observations can be easily plotted because they are two-dimensional. If there were more than two
variables then we could instead perform PCA and plot the first two principal components score vectors.

In this example, we knew that there really were two clusters because we generated the data. However, for real data, in general we do not
know the true number of clusters. We could instead have performed $K$-means clustering on this example with $K=3$.

```{r chunk32}
set.seed(4)
km.out <- kmeans(x, 3, nstart = 20)
km.out
plot(x, col = (km.out$cluster + 1),
    main = "K-Means Clustering Results with K = 3",
    xlab = "", ylab = "", pch = 20, cex = 2)
```

When $K=3$, $K$-means clustering  splits up the two clusters.

To run the `kmeans()` function in `R` with multiple initial cluster assignments, we use the
`nstart` argument. If a value of `nstart` greater than one is used, then $K$-means clustering will be performed using
multiple random assignments in Step~1 of Algorithm 12.2, and the `kmeans()` function will report only the best results. Here we compare using `nstart = 1` to `nstart = 20`.

```{r chunk33}
set.seed(4)
km.out <- kmeans(x, 3, nstart = 1)
km.out$tot.withinss
km.out <- kmeans(x, 3, nstart = 20)
km.out$tot.withinss
```

Note that `km.out$tot.withinss` is the total within-cluster sum of squares, which  we seek to minimize by performing $K$-means clustering (Equation 12.17). The individual within-cluster sum-of-squares are contained in the vector `km.out$withinss`.

We *strongly* recommend always running $K$-means clustering with
a large value of `nstart`, such as 20 or 50, since otherwise an
undesirable local optimum may be obtained.

When performing $K$-means clustering, in addition to using multiple initial cluster assignments, it is
also  important to set a random seed using the `set.seed()` function. This way, the
initial cluster assignments in Step~1 can
be replicated, and the $K$-means output will be fully reproducible.

### Hierarchical Clustering

The `hclust()` function implements  hierarchical clustering in `R`. In the following example we use the data from the previous lab to
 plot the hierarchical clustering dendrogram using complete, single, and average linkage clustering, with  Euclidean distance as the dissimilarity measure.
We begin by clustering observations using complete linkage. The `dist()` function is used to compute the $50 \times 50$ inter-observation Euclidean distance matrix.

```{r chunk34}
hc.complete <- hclust(dist(x), method = "complete")
```

We could just as easily perform hierarchical clustering with average or single linkage instead:

```{r chunk35}
hc.average <- hclust(dist(x), method = "average")
hc.single <- hclust(dist(x), method = "single")
```

We can now plot the dendrograms obtained using the usual `plot()` function. The numbers at the bottom of the plot identify each observation.

```{r chunk36}
par(mfrow = c(1, 3))
plot(hc.complete, main = "Complete Linkage",
    xlab = "", sub = "", cex = .9)
plot(hc.average, main = "Average Linkage",
    xlab = "", sub = "", cex = .9)
plot(hc.single, main = "Single Linkage",
    xlab = "", sub = "", cex = .9)
```


To determine the cluster labels for each observation associated with a given cut of the dendrogram, we can use the `cutree()` function:

```{r chunk37}
cutree(hc.complete, 2)
cutree(hc.average, 2)
cutree(hc.single, 2)
```

The second argument to `cutree()` is the number of clusters we wish to obtain.
For this data, complete and average linkage generally separate the observations into their correct groups. However, single linkage identifies one point as belonging to its own cluster. A more sensible answer is obtained when four clusters are selected, although there are still two singletons.

```{r chunk38}
cutree(hc.single, 4)
```


To scale the variables before performing hierarchical clustering of the observations, we use the `scale()` function:

```{r chunk39}
xsc <- scale(x)
plot(hclust(dist(xsc), method = "complete"),
    main = "Hierarchical Clustering with Scaled Features")
```


Correlation-based distance can be computed using the `as.dist()` function, which converts an arbitrary square symmetric matrix into a form that the `hclust()` function recognizes as a distance matrix. However, this only makes sense for data with at least three features since the absolute correlation between any two observations
with measurements on two features is always 1. Hence, we will cluster a three-dimensional data set. This data set does not contain any true clusters.

```{r chunk40}
x <- matrix(rnorm(30 * 3), ncol = 3)
dd <- as.dist(1 - cor(t(x)))
plot(hclust(dd, method = "complete"),
    main = "Complete Linkage with Correlation-Based Distance",
    xlab = "", sub = "")
```




## NCI60 Data Example


Unsupervised techniques are often used in the analysis of genomic data. In particular, PCA and hierarchical clustering are popular tools.
 We  illustrate these techniques on the `NCI` cancer cell line microarray data, which consists of $6{,}830$ gene expression measurements on $64$ cancer cell lines.

```{r chunk41}
library(ISLR2)
nci.labs <- NCI60$labs
nci.data <- NCI60$data
```

Each cell line is labeled with a cancer type, given in `nci.labs`. We do not make use of the cancer types in performing PCA and clustering, as these are unsupervised techniques. But
after performing PCA and clustering, we will
check to see the extent to which these cancer types agree with the results of these unsupervised techniques.

The data has $64$ rows and $6{,}830$ columns.

```{r chunk42}
dim(nci.data)
```


We begin by examining the cancer types for the cell lines.

```{r chunk43}
nci.labs[1:4]
table(nci.labs)
```


### PCA on the NCI60 Data

We first perform PCA on the data after scaling the variables (genes) to have standard deviation one, although one could reasonably argue that it is better not to scale the genes.

```{r chunk44}
pr.out <- prcomp(nci.data, scale = TRUE)
```

We now  plot the first few principal component score vectors, in order to visualize the data. The observations (cell lines) corresponding to a given cancer type will be plotted in the same color, so that we can see to what extent the observations within a cancer type are similar to each other. We first create a simple function that assigns a distinct color to each element of a numeric vector.
The function will be used to assign a  color to each of the $64$ cell lines, based on the cancer type to which it corresponds.

```{r chunk45}
Cols <- function(vec) {
   cols <- rainbow(length(unique(vec)))
   return(cols[as.numeric(as.factor(vec))])
 }
```

Note that the `rainbow()` function takes as its argument a positive integer, and returns a vector containing that number of distinct colors.  We now can plot the principal component score vectors.

```{r chunk46}
par(mfrow = c(1, 2))
plot(pr.out$x[, 1:2], col = Cols(nci.labs), pch = 19,
    xlab = "Z1", ylab = "Z2")
plot(pr.out$x[, c(1, 3)], col = Cols(nci.labs), pch = 19,
    xlab = "Z1", ylab = "Z3")
```

The resulting  plots are shown in Figure 12.17. On the whole, cell lines corresponding to a single cancer type do tend to have similar values on the first few
principal component score vectors. This indicates that cell lines from the same cancer type tend to have pretty similar gene expression levels.

\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{Figures/Chapter12/12_17.pdf} 
On the whole, observations belonging to a single cancer type tend to lie near each other
in this low-dimensional space. It would not have been possible to visualize the data without using a dimension reduction method such as PCA, since based on the full data set there are
 $6{,}830 \choose 2$ possible scatterplots, none of which would have
been particularly informative.}
\end{figure}

We can obtain a summary of the proportion of variance explained (PVE) of the first few principal components using the `summary()` method for a `prcomp` object (we have truncated the printout):

```{r chunk47}
summary(pr.out)
```

Using the `plot()` function, we can also plot the variance explained by the first few principal components.

```{r chunk48}
plot(pr.out)
```

Note that the height of each bar in the bar plot is given by squaring the corresponding element of `pr.out$sdev`.
However, it is more informative to plot the PVE of each principal component (i.e. a scree plot) and the cumulative PVE of each principal component. This can be done with just a little work.

```{r chunk49}
pve <- 100 * pr.out$sdev^2 / sum(pr.out$sdev^2)
par(mfrow = c(1, 2))
plot(pve,  type = "o", ylab = "PVE",
    xlab = "Principal Component", col = "blue")
plot(cumsum(pve), type = "o", ylab = "Cumulative PVE",
    xlab = "Principal Component", col = "brown3")
```

(Note that the elements of `pve` can also be computed directly from the summary, `summary(pr.out)$importance[2, ]`, and the elements of
`cumsum(pve)` are given by
`summary(pr.out)$importance[3, ]`.)
The resulting plots are shown in Figure 12.18.
\begin{figure}[t]
\centering
\includegraphics[width=\textwidth]{Figures/Chapter12/12_18.pdf}
*Right:* the cumulative PVE of the principal components is shown. Together, all principal components explain $100\,\%$ of the variance.}
\end{figure}
We see that together,
the first seven principal components explain around $40\,\%$ of the variance in the data. This is not a huge
amount of the variance. However, looking at the scree plot, we see that while each of the first seven principal components explain a substantial amount of  variance, there
is a marked decrease in the variance explained by further principal components. That is, there is an *elbow*   in the plot after approximately the seventh principal component.
This suggests that there may be little benefit to examining more than seven or so principal components (though even examining seven principal components may be difficult).



### Clustering the Observations of the NCI60 Data

We now proceed to hierarchically cluster the cell lines in the `NCI` data, with the goal of finding out whether or not the observations cluster into distinct types of cancer. To begin, we standardize the variables to have mean
 zero and standard deviation one. As mentioned earlier, this step is optional and should be performed only if we want each gene to be on the same *scale*.

```{r chunk50}
sd.data <- scale(nci.data)
```

We now perform hierarchical clustering of the observations using complete, single, and average linkage. Euclidean distance is used as the dissimilarity measure.

```{r chunk51}
par(mfrow = c(1, 3))
data.dist <- dist(sd.data)
plot(hclust(data.dist), xlab = "", sub = "", ylab = "",
    labels = nci.labs, main = "Complete Linkage")
plot(hclust(data.dist, method = "average"),
    labels = nci.labs, main = "Average Linkage",
    xlab = "", sub = "", ylab = "")
plot(hclust(data.dist, method = "single"),
    labels = nci.labs,  main = "Single Linkage",
    xlab = "", sub = "", ylab = "")
```

\begin{figure}[p]
\centering
\includegraphics[width=\textwidth]{Figures/Chapter12/12_19.pdf}
as the dissimilarity measure. Complete and average linkage tend to yield
evenly sized clusters whereas single linkage tends to yield extended clusters to which single leaves are fused one by one.}
\end{figure}
The results are shown in Figure 12.19.
We see that the choice of linkage certainly  does affect the results obtained. Typically, single linkage will tend to yield *trailing* clusters: very large clusters onto which
 individual observations attach  one-by-one. On the other hand, complete and average linkage tend to yield more balanced, attractive clusters. For this reason, complete
and average linkage are generally preferred to single linkage.
Clearly cell lines within a single cancer type do tend to cluster together, although the clustering is not perfect. We will use complete linkage hierarchical clustering for the analysis that follows.


We can cut the dendrogram at the height that will yield a particular number of clusters, say four:

```{r chunk52}
hc.out <- hclust(dist(sd.data))
hc.clusters <- cutree(hc.out, 4)
table(hc.clusters, nci.labs)
```

There are some clear patterns. All the leukemia cell lines fall in cluster $3$, while the breast cancer cell lines are spread out over three different clusters.  We can plot the cut on the dendrogram that produces these four clusters:

```{r chunk53}
par(mfrow = c(1, 1))
plot(hc.out, labels = nci.labs)
abline(h = 139, col = "red")
```

The `abline()` function draws a straight line on top of any existing plot in~`R`. The argument `h = 139` plots a horizontal line at height $139$ on the
dendrogram; this is the height that results in four distinct clusters. It is easy to verify that the resulting clusters are the same as the ones we obtained using `cutree(hc.out, 4)`.


Printing the output of `hclust` gives a useful brief summary of the object:

```{r chunk54}
hc.out
```


We claimed earlier in Section 12.4.2 that $K$-means clustering and hierarchical clustering with the dendrogram cut to obtain the same number of clusters can yield very different results.
How do these `NCI` hierarchical clustering results compare to what we  get if we perform $K$-means clustering with $K=4$?

```{r chunk55}
set.seed(2)
km.out <- kmeans(sd.data, 4, nstart = 20)
km.clusters <- km.out$cluster
table(km.clusters, hc.clusters)
```

We see that the four clusters obtained using hierarchical clustering and $K$-means clustering  are somewhat different. Cluster~$4$ in $K$-means clustering is identical to cluster~$3$
in hierarchical clustering. However, the other clusters differ: for instance, cluster~$2$ in $K$-means clustering contains a portion of the observations assigned to
cluster 1 by hierarchical clustering, as well as all of the observations assigned to cluster~$2$ by hierarchical clustering.

Rather than performing hierarchical clustering on the entire data matrix, we can simply perform hierarchical clustering on the first few principal component score vectors,
as follows:

```{r chunk56}
hc.out <- hclust(dist(pr.out$x[, 1:5]))
plot(hc.out, labels = nci.labs,
    main = "Hier. Clust. on First Five Score Vectors")
table(cutree(hc.out, 4), nci.labs)
```

 Not surprisingly, these results are different from the ones that we
 obtained when we performed hierarchical clustering on the full data
 set. Sometimes performing clustering on the first few principal
 component score vectors can give better results than performing
 clustering on the full data.  In this situation, we might view the principal
component step as one of denoising the data.
We could also perform $K$-means
 clustering on the first few principal component score vectors rather
 than the full data set.






