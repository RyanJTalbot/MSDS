# Poisson Example - manual calculation
lambda<-25
X<-10

(lambda^X/factorial(X))*exp(-lambda)

# Poisson Example - dpois
dpois(x = 10, lambda = 25)

# Poisson Example - table
round.object(table.dist.poisson(lambda = 25),5)
round.object(table.dist.poisson(lambda = 25)[7:51,],5)

# Barplot of Poisson Probability Distribution
lambda<-25
X<-10

data<-dpois(x = 6:50, lambda = lambda)
names(data)<-6:50
barplot(data, xlab = "Parts per Hour", ylab = "P(X)", ylim = c(0, 0.10))

# Poisson Probability of 10 or fewer 
ppois(q = 10, lambda = 25, lower.tail = T)

# Poisson Probability of at least 20, but no more than 30?
data<-dpois(x = 6:50, lambda = lambda)
names(data)<-6:50
barplot(data, xlab = "Parts per Hour", ylab = "P(X)", ylim = c(0, 0.10))
cols <- rep("grey", n + 1)
cols[15:25] <- "red"
barplot(data, col=cols, xlab = "Parts per Hour", ylab = "P(X)", ylim = c(0, 0.10))

(ft20<-ppois(q = 19, lambda = 25, lower.tail = T))
(ft30<-ppois(q = 30, lambda = 25, lower.tail = T))

ft30-ft20

# Poisson distribution testing
poisdist<-rpois(n = 100, lambda = 25)
poisson.dist.test(poisdist)
