# Two Dependent Sample Tests for Means

# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Paired t test for Means (Dependent by Nature) -------------------------------------------------
summary.continuous(Noise)[-1,]

# Calculate difference between Old and New
Noise$Diff<-Noise$Old-Noise$New

summary.continuous(Noise)[-1,]

# Drop first and fourth column
Noise<-Noise[-c(1,4)]

# Transpose data
Noise.I<-transform.dependent.format.to.independent.format(data = Noise)
Noise.I
str(Noise.I)
Noise.I$cell<-as.factor(Noise.I$cell)

# Paired t test
t.test.twosample.dependent(x1 = Noise$Old
                           ,x2 = Noise$New)

# Calculate difference between Old and New
Noise$Diff<-Noise$Old-Noise$New

# Dbar method
t.test.twosample.dependent.simple.dbar(pair.differences.mean = mean(Noise$Diff)
                                       ,pair.differences.variance = var(Noise$Diff)
                                       ,sample.size = 10)

# Calculate the Pearson Product Moment Correlation Coefficient
cor(Noise$Old, Noise$New)

cor.pearson.r.onesample(x = Noise$Old, y = Noise$New)


# Matched Pairs t test (Dependendent by Design) ---------------------------
cor.pearson.r.onesample.simple(sample.r = 0.60, sample.size = 30)

ro(t.test.twosample.dependent.simple.meandiff(sample.mean.g1 = 35.24
                                              ,sample.mean.g2 = 38.02
                                              ,sample.variance.g1 = 5.18^2
                                              ,sample.variance.g2 = 5.63^2
                                              ,sample.size = 30
                                              ,rho.estimate = 0.60),4)

