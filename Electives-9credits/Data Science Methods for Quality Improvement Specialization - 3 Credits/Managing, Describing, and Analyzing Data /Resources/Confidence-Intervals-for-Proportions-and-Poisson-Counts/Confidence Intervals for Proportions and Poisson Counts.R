# Confidence Intervals for Proportions and Poisson Counts

# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Confidence Interval for a Proportion -----------------------
# Example 1
ro(proportion.test.onesample.exact.simple(sample.proportion = 0.12
                                       ,sample.size = 100
                                       , conf.level = 0.95),4)

# Using the Point Estimate File, calculate the 90% confidence interval for the 
# Proportion

(prop<-mean(Point_Estimates$Proportion)) # average proportion
(n<-length(Point_Estimates$Proportion)) # sample size

# Proportion (Exact) 
ro(proportion.test.onesample.exact.simple(sample.proportion = 0.03525
                                       ,sample.size = 20
                                       ,conf.level = 0.90),4)


# Confidence Interval for Poisson Counts ---------------------
# Using the Point Estimate File, calculate the 99% confidence interval for the 
# Poisson Counts

# Make sure data are Poisson distributed
poisson.dist.test(Point_Estimates$Count)

# Get Total Counts in the Sample
(counts<-sum(Point_Estimates$Count))

# Get Sample Size
(n<-length(Point_Estimates$Count))

poisson.test.onesample.simple(sample.count = 501
                               ,sample.size = 20
                               ,conf.level = 0.90)

