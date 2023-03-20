# Two Sample Tests for Variances 
# (Assuming a Normally Distributed Population)

# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Independent Sample F Test for Variances -----------------------------------------

ro(variance.test.twosample.independent.simple(sample.variance.g1 = 0.0015^2
                                              ,sample.size.g1 = 25
                                              ,sample.variance.g2 = 0.0013^2
                                              ,sample.size.g2 = 30),7)

# Compare results to t test
ro(t.test.twosample.independent.simple(sample.mean.g1 = 0.0060
                                       ,sample.variance.g1 = 0.0015^2
                                       ,sample.size.g1 = 25
                                       ,sample.mean.g2 = 0.0090
                                       ,sample.variance.g2 = 0.0013^2
                                       ,sample.size.g2 = 30
                                       ,conf.level = 0.95),7)

# Matched Pairs t test for Variances --------------------------------------
cor.pearson.r.onesample.simple(sample.r = 0.60, sample.size = 30)

variance.test.twosample.dependent.simple(sample.variance.g1 = 5.18^2
                                         ,sample.variance.g2 = 5.63^2
                                         ,sample.size = 30
                                         ,rho.estimate = 0.60
                                         ,conf.level = 0.95)



