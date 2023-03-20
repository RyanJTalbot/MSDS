# Two Independent Sample Tests for Poisson Counts
# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Sample Independent Tests for Poisson Rates (Counts) -----------------

# Descriptive Summary
summary.impl(Eddycur$Before, stat.n = T, stat.mean = T)
summary.impl(Eddycur$After, stat.n = T, stat.mean = T)

# Test for Poisson distribution
poisson.dist.test(Eddycur$Before)
poisson.dist.test(Eddycur$After)

# Poisson test
# Remember that sample count has to be 
# n times lambda
(count_before<-sum(Eddycur$Before))
(n_before<-length(Eddycur$Before))

(count_after<-sum(Eddycur$After))
(n_after<-length(Eddycur$After))

poisson.test.twosample.simple(sample.count.g1 = 112
                              ,sample.size.g1 = 130
                              ,sample.count.g2 = 260
                              ,sample.size.g2 = 130)


