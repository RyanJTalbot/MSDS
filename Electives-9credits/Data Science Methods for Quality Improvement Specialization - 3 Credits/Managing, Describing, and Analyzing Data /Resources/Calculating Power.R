# Calculating Power
# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)


# Example 1 - Calculating Power for Changes in Means
power.mean.t.onesample(sample.size = 9
                       ,effect.size = 10
                       ,variance.est = 10^2
                       ,alpha = 0.05
                       ,alternative = "two.sided")

# Example 2 - Calculating Power for Changes in Variance

# Power to detect an increase in variance
power.variance.onesample(sample.size = 9
                         ,null.hypothesis.variance = 10^2
                         ,alternative.hypothesis.variance = 12^2
                         ,alpha = 0.05
                         ,alternative = "two.sided")

# Power to detect a decrease in variance
power.variance.onesample(sample.size = 9
                         ,null.hypothesis.variance = 10^2
                         ,alternative.hypothesis.variance = 8^2
                         ,alpha = 0.05
                         ,alternative = "two.sided")




