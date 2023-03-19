# Example of Binomial Probability Distribution
table.dist.binomial(n = 2, p = 0.2)

# Barplot of Binomal Probability Distribution
n<-2
P<-0.2
data<-dbinom(x = 0:n, size = n, prob = P)
names(data)<-0:n
barplot(data, xlab = "# of Defectives", ylab = "P(D)", ylim = c(0,1))

# Probability Distribtuion for Discrete Random Variable
(freqdistdp<-round.object(frequency.dist.grouped(Daily.Production$V1),3))
(probdistdp<-freqdistdp[,c("min","freq","rel.freq")])
colnames(probdistdp)<-c("Daily Production", "#of Days", "P(DP)")
View(probdistdp)

# Probability Distribution (Histogram)
hist.grouped(Daily.Production$V1, freq = F, anchor.value=50, ylim=c(0,0.20))

# Expected Value of a Discrete Random Variable
x<-probdistdp$`Daily Production`
y<-probdistdp$`P(DP)`
weighted.mean(x,y)

# Alternatively
mean(Daily.Production$V1)
