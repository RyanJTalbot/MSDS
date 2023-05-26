# Binomial Example - manual calculation
p<-0.80
q<-0.20
r<-45
n<-50

factorial(n)/(factorial(r)*factorial(n-r))*(p^r)*(q^(n-r))

# Binomial Example - dbinom
dbinom(x = 45, size = 50, prob = 0.8)

# Binomial Example - table
round.object(table.dist.binomial(n = 50, p = 0.80),5)

# Barplot of Binomal Probability Distribution
n<-50
P<-0.8
data<-dbinom(x = 26:n, size = n, prob = P)
names(data)<-26:n
barplot(data, xlab = "# of Good Parts", ylab = "P(G)", ylim = c(0,0.15))
cols <- rep("grey", n + 1)
cols[20:25] <- "red"
barplot(data, col=cols,xlab = "# of Good Parts", ylab = "P(G)", ylim = c(0,0.15))

# Binomial Probability of >=45 
# Note that pbinom gives P[X>x] for upper tail probabilities
pbinom(q = 44, size = 50, prob = 0.80, lower.tail = F)
