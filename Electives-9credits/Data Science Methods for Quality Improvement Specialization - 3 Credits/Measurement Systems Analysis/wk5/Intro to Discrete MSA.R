# Startup Code
require(lolcat)
require(car)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Independent Sample Proportion Test ----------------------------------
ro(
  proportion.test.twosample.exact.simple(
    sample.proportion.g1 = 0.46,
    sample.size.g1 = 100,
    sample.proportion.g2 = 0.40,
    sample.size.g2 = 100),4)

# Chi-Square Test of Association ------------------------------------------
# Create vector in format ct<-c(a,c,b,d)
ct<-c(33,13, 7,47)

# Create Contingency Table
(ct.obs <- matrix(
  ct,
  nrow = 2,
  dimnames = list(
    "Inspector A" = c("Pass", "Fail"),
    "Inspector B" = c("Pass", "Fail"))))

# Conduct Fisher's test
fisher.test(ct.obs, conf.level = 0.95)

# Pearson's Phi
cor.pearson.phi(ct.obs)

# McNemar's Test of Change ------------------------------------------------
(mcnemar.out<-
   proportion.test.mcnemar.simple(b = 7, c = 13))

# Kappa Statistic ---------------------------------------------------------
# Contingency Table
# Chi Square test
(chisq.out<-chisq.test(ct.obs))
(ct.exp<-chisq.out$expected)

(kappa.out<-cor.cohen.kappa.onesample.1969.fleiss(observed.frequencies = ct.obs
                                                  ,expected.frequencies = ct.exp))

df.kappa<-data.frame(kappa.out$estimate)
View(df.kappa)

