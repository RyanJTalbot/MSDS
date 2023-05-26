# Using the RSD to solve probability problems
# Example 1
# Define the variables in the problem
mu1<-1.325
sigma1<-0.045
n1<-25
xbar1<-1.433
stderror1<-sigma1/sqrt(n1)

# Calculate the area under the normal curve using the pnorm function
pnorm(q = xbar1, mean = mu1,sd = stderror1, lower.tail = F)

# Create the normal curve
x=seq(1.28,1.45,length=200)
y=dnorm(x,mean=mu1,sd=stderror1)
plot(x,y,type="l")

# Indicate the location of the xbar of 1.433
abline(v=1.433)

# Example 2
# Define the variables in the problem
mu2<-50
sigma2<-14.4
n2<-25
xbar2<-55
stderror2<-sigma2/sqrt(n2)

# Calculate the area under the normal curve using the pnorm function
pnorm(q = xbar2, mean = mu2,sd = stderror2, lower.tail = F)

# Create the normal curve
x=seq(30,70,length=200)
y=dnorm(x,mean=mu2,sd=stderror2)
plot(x,y,type="l")

# Shade the upper tail area
x=seq(55,70,length=100)
y=dnorm(x,mean=mu2,sd=stderror2)
polygon(c(55,x,70),c(0,y,0),col="red")

# Indicate the location of the xbar of 55
abline(v=55)