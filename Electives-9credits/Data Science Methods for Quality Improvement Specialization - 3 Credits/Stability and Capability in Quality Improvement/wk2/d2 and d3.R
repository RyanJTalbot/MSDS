# Derivation of d2 and d3

# Startup Code
require(lolcat)
nqtr<-function(x,d){noquote(t(round.object(x, d)))}

# First, set seed so we will get the same results
set.seed(150)

# Create a standard normal distribution with mean
# of 10, and standard deviation of 2.
ind<-rnorm(n = 1000, mean = 10, sd = 2)
  
# Next, create / simulate a random sampling distribution
# Set the sample size equal to 4
n<-4

# Create the number of repetitions 
# (number of times we will take a sample of size 4)
reps<-5000

# Take the random samples from a population with a mean of 10 and 
# standard deviation of 2
sample<-replicate(reps, rnorm(n, mean = 10, sd = 2))

# Calculate the averages of each sample of 4
xbars<-colMeans(sample)


# Calculate the ranges of each sample of 4
(max_sample<-apply(X = sample, MARGIN = 2, FUN = max))
(min_sample<-apply(X = sample, MARGIN = 2, FUN = min))
(ranges<-max_sample-min_sample)


# Create 2 histograms of the population and sample averages 
# using the same axis to compare

# Create a 1 x 2 matrix
dev.off() # turns off the default
layout(matrix(1:3, nrow=3)) 

# Create 3 histograms
hist.grouped(ind, xlim=c(0,20), main = "Individual Values",xaxt='n', width.consider = 1)
axis(side = 1, at = seq(0,20,2), labels = seq(0,20,2))

hist.grouped(xbars, xlim=c(0,20), main="Subgroup Averages", xaxt='n', width.consider = 1)
axis(side = 1, at = seq(0,20,2), labels = seq(0,20,2))

hist.grouped(ranges, xlim=c(0,20), main="Subgroup Ranges", xaxt='n', width.consider = 1)
axis(side = 1, at = seq(0,20,2), labels = seq(0,20,2))

# Descriptive Statistics
(stat.ind<-summary.impl(ind, stat.mean = T, stat.sd = T))
(stat.xbars<-summary.impl(xbars, stat.mean = T, stat.sd = T))
(stat.range<-summary.impl(ranges, stat.mean = T, stat.sd = T))

# Average Range divided by d2
(avg.range<-stat.range$mean)
(d2<-spc.constant.calculation.d2(sample.size = 4))

avg.range/d2 # unbiased estimate of the standard deviation

# Standard Deviation of the Range divided by d3
(sd.range<-stat.range$sd)
(d3<-spc.constant.calculation.d3(sample.size = 4))

sd.range/d3 # unbiased estimate of the standard deviation



