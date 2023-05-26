# Random Sampling Distribution Simulation
nqtr<-function(x,d){noquote(t(round.object(x, d)))}

# First, set seed so we will get the same results
set.seed(133)

# Create a distribution with mean of 10 and standard deviation of 2
pop<-rnorm(n = 50000, mean = 10, sd = 2)

# Create a histogram of the population distribution
hist.grouped(pop, anchor.value = 0)
Hist.grouped(pop, anchor.value=0)

# Calculate the descriptive statistics of the population distribution
nqtr(summary.continuous(pop, stat.sd=T),5)

# Next, create / simulate a random sampling distribution
# Set the sample size equal to 4
n<-4

# Create the number of repetitions 
# (number of times we will take a sample of size 4)
reps<-5000

# Take the random samples from a population with a mean of 10 and 
# standard deviation of 2
samples <- replicate(reps, rnorm(n, mean = 10, sd = 2))
View(samples)

# Calculate the averages of each sample of 4
sampleavgs <- colMeans(samples)

# Calculate the descriptive statistics of the RSD
nqtr(summary.continuous(sampleavgs, stat.sd=T),5)

# Create 2 histograms of the population and sample averages 
# using the same axis to compare

# Create a 1 x 2 matrix
dev.off() # turns off the default
layout(matrix(1:2, nrow=2)) 

# Create both histograms
hist.grouped(pop, xlim=c(0,22), xaxt='n', width.consider = 1)
axis(side = 1, at = seq(0,22,2), labels = seq(0,22,2))

hist.grouped(sampleavgs, xlim=c(0,22), xaxt='n', width.consider = 1)
axis(side = 1, at = seq(0,22,2), labels = seq(0,22,2))

