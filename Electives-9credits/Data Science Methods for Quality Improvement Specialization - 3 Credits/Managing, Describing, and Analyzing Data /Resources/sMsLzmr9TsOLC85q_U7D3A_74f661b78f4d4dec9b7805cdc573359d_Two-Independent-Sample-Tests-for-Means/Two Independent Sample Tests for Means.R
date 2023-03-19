# Two Independent Sample Tests for Means

# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Sample t Test, Equal Variance ---------------------------------------

# Use simple when all parameter estimates are given
ro(t.test.twosample.independent.simple(sample.mean.g1 = 0.0060
                                    ,sample.variance.g1 = 0.0015^2
                                    ,sample.size.g1 = 25
                                    ,sample.mean.g2 = 0.0090
                                    ,sample.variance.g2 = 0.0013^2
                                    ,sample.size.g2 = 30
                                    ,conf.level = 0.95),6)

# CapPull2.dat file

# Use when you have a data file available
t.test.twosample.independent(g1 = CapPull2$pull[CapPull2$mold==1]
                             ,g2 = CapPull2$pull[CapPull2$mold==2])

# Make factors
str(CapPull2)
CapPull2$mold<-as.factor(CapPull2$mold)
str(CapPull2)

# Descriptive Summary
summary.continuous(fx = pull~mold, data = CapPull2)

# Use when you want to use a formula of y~x and have 
# a data file with factors
t.test.twosample.independent.fx(fx = pull~mold
                                ,data = CapPull2)
# Data visualization
boxplot(pull~mold, data = CapPull2, col="red")

process.group.plot(fx = pull~mold,data = CapPull2)

# Two Sample t Test, Unequal Variance ---------------------------------------

ro(t.test.twosample.independent.simple(sample.mean.g1 = 75
                                       ,sample.variance.g1 = 20^2
                                       ,sample.size.g1 = 12
                                       ,sample.mean.g2 = 82
                                       ,sample.variance.g2 = 9^2
                                       ,sample.size.g2 = 12
                                       ,conf.level = 0.90),4)

