# Two Sample Tests for Proportions
# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Sample Tests for Proportions ----------------------------------------

# Fisher's Exact Test
proportion.test.twosample.exact.simple(sample.proportion.g1 = 0.18
                                       ,sample.size.g1 = 750
                                       ,sample.proportion.g2 = 0.12
                                       ,sample.size.g2 = 750
                                       ,conf.level = 0.99)

# McNemar's Test for Change - Dependent Proportions -----------------------
# Contingency table format = ct<-(a,c,b,d)
ct<-c(56,56,4,4)

# Create Contingency Table
(ct.new<-matrix(ct,nrow = 2
                , dimnames = list("Before Maint" = c("Pass", "Fail"),
                                  "After Maint" = c("Pass", "Fail"))))

# Perform McNemar's Test
(mcnemar.out<-proportion.test.mcnemar.simple(b = 4, c = 56))

mcnemar.test(ct.new)
