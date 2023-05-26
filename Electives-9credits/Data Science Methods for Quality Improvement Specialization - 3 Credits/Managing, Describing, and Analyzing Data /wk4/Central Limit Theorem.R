# Random Sampling Distribution Simulation
nqtr<-function(x,d){noquote(t(round.object(x, d)))}

# First, set seed so we will get the same results
set.seed(101)

# Create an exponential distribution with mean of 10
popexp<-rexp(n = 50000, rate = 1/10)

# Create a histogram of the population distribution
hist.grouped(popexp)

# Calculate the descriptive statistics of the population distribution
nqtr(summary.continuous(popexp, stat.sd=T),5)

# Next, create / simulate a random sampling distribution
set.seed(102)

# Set the sample size equal to 100
n<-100

# Create the number of repetitions 
# (number of times we will take a sample of size 100)
reps<-1000

# Take the random samples from an exponential population with a  
# mean of 10 (lambda = 1/10)
samplesexp <- replicate(reps, rexp(n, rate = 1/10))
View(samplesexp)

# Calculate the averages of each sample of 100
sampleavgsexp <- colMeans(samplesexp)

# Calculate the descriptive statistics of the RSD of the means
nqtr(summary.continuous(sampleavgsexp, stat.sd=T),5)

# Create a histogram for the RSD of the means from the
# exponential population
hist.grouped(sampleavgsexp)

# Create 2 histograms of the population and sample averages 
# using the same axis to compare

# Create a 1 x 2 matrix
dev.off() # turns off the default
layout(matrix(1:2, nrow=2)) 

# Create both histograms
hist.grouped(popexp, xlim=c(0,50), xaxt='n', width.consider = 2)
axis(side = 1, at = seq(0,50,5), labels = seq(0,50,5))

hist.grouped(sampleavgsexp, xlim=c(0,50), xaxt='n', width.consider = 2)
axis(side = 1, at = seq(0,50,5), labels = seq(0,50,5))
