# Confidence Intervals for the Mean and Variance

# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Confidence Interval for the Mean (Sigma is Known) -----------------------
# Example 1
n<-150
xbar<-20
sd<-5
conf<-0.95

z.test.onesample.simple(sample.mean = 20
                        ,known.population.variance = 5^2
                        ,sample.size = 150
                        ,conf.level = 0.99)

# Round the output
ro(z.test.onesample.simple(sample.mean = 20
                        ,known.population.variance = 5^2
                        ,sample.size = 150
                        ,conf.level = 0.95),2)


# Confidence Interval for the Mean (Sigma is Unknown) ---------------------
# Example 2
n<-14
xbar<-15000
sd<-500
conf<-0.90

t.test.onesample.simple(sample.mean = xbar
                        ,sample.variance = sd^2
                        ,sample.size = n
                        ,conf.level = conf)


# Confidence Interval for the Variance ------------------------------------
# Example 3
sd<-10
n<-25
conf<-0.95

ci.var<-variance.test.onesample.simple(sample.variance = 10^2
                               ,sample.size = 25
                               ,conf.level = 0.95)

# Confidence Interval for the Variance
ci.var$conf.int

# Confidence Interval for the Standard Deviation
sqrt(ci.var$conf.int)

# Generate Confidence Intervals using a file
# Using the point estimate file, calculate the 95% confidence interval 
# estimates for the mean, variance and standard deviation for the Weight data

# Test for normality
summary.continuous(Point_Estimates$Weight)

# Calculate confidence intervals
t.test.onesample(Point_Estimates$Weight, conf.level = 0.95)

