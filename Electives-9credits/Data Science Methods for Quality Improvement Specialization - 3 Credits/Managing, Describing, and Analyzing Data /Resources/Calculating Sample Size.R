# Calculating Sample Size
# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)


# Calculating Sample Size -------------------------------------------------
# Sample Size Calculations for Changes in Means ---------------------------

alpha<-0.05
beta<-0.02
deltamu<-1
sd<-2

# Sigma unknown, non-directional, one sample
sample.size.mean.t.onesample(effect.size = 1
                             , variance.est = 2^2
                             , alpha = 0.05
                             , beta = 0.02
                             , alternative = "two.sided")


# Sample Size Calculations for Changes in Variance ---------------------------
# Sample Size, one sample
sigma0<-2 # 4 variance
sigma1<-3 # 9 variance
sigma2<-1 # 1 variance
alpha<-0.05
beta<-0.02

# Two sided, one sample (testing for a change in either direction)
# In this situation, I use the two.sided test for both the larger and smaller variance,
# and take the larger sample size of the two.
sample.size.variance.onesample(null.hypothesis.variance = sigma0^2
                               ,alternative.hypothesis.variance = sigma1^2
                               ,alpha = alpha
                               ,beta = beta
                               ,alternative = "two.sided")

sample.size.variance.onesample(null.hypothesis.variance = sigma0^2
                               ,alternative.hypothesis.variance = sigma2^2
                               ,alpha = alpha
                               ,beta = beta
                               ,alternative = "two.sided")

# Sample Size Calculations for Changes in Proportions ---------------------------
# Sample size for Proportions
pi0<-0.2
pi1<-0.3
pi2<-0.1
alpha<-0.05
beta<-0.10

# One sided, one sample
nqtr(sample.size.proportion.test.onesample.exact(null.hypothesis.proportion = pi0
                                                 ,alternative.hypothesis.proportion = pi2
                                                 ,alpha = alpha
                                                 ,beta = beta
                                                 ,alternative = "less"),4)

nqtr(sample.size.proportion.test.onesample.exact(null.hypothesis.proportion = pi0
                                                 ,alternative.hypothesis.proportion = pi1
                                                 ,alpha = alpha
                                                 ,beta = beta
                                                 ,alternative = "greater"),4)

# Two sided, one sample (testing for a change in either direction)
# In this situation, I use the two.sided test for both the larger and smaller proportion,
# and take the larger sample size of the two.

nqtr(sample.size.proportion.test.onesample.exact(null.hypothesis.proportion = pi0
                                                 ,alternative.hypothesis.proportion = pi1
                                                 ,alpha = alpha
                                                 ,beta = beta
                                                 ,alternative = "two.sided"),4)

nqtr(sample.size.proportion.test.onesample.exact(null.hypothesis.proportion = pi0
                                                 ,alternative.hypothesis.proportion = pi2
                                                 ,alpha = alpha
                                                 ,beta = beta
                                                 ,alternative = "two.sided"),4)





