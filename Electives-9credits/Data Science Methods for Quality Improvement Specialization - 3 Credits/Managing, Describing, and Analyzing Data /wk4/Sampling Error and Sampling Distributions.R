# Create four random samples of size n=30 with Mu = 100, sigma = 10
d1<-rnorm(n = 30,mean = 100, sd = 10)
d2<-rnorm(n = 30,mean = 100, sd = 10)
d3<-rnorm(n = 30,mean = 100, sd = 10)
d4<-rnorm(n = 30,mean = 100, sd = 10)

# Create a dataframe of all variables
normdata<-data.frame(d1,d2,d3,d4)
View(normdata)

# Review summary statistics of all variables
summary.all.variables(normdata, stat.sd=T)

# Make output easier to read
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
nqtr(summary.all.variables(normdata, stat.sd=T),3)

# Create histograms of each variable in one plot
# Set parameters for graphical output, and create a matrix of nrows x ncols 
par(mfrow=c(2,2))
hist.grouped(normdata$d1)
hist.grouped(normdata$d2)
hist.grouped(normdata$d3)
hist.grouped(normdata$d4)

# Set parameters back to one graph
par(mfrow=c(1,1))
randoexp<-rexp(n = 100, rate = 1/10)
hist.grouped(randoexp)
