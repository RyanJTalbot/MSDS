# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# *** Data Transformations ***

# *** The Food Distributor Delivery Problem ***
Delivery <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/Delivery.dat", sep="")
View(Delivery)

# Summary and Histogram
nqtr(summary.continuous(Delivery$Temp), 5)
summary(Delivery$Temp)
hist.grouped(Delivery$Temp, anchor.value = 38)
hist.grouped(Delivery$Temp, xlim=c(min(Delivery$Temp),max(Delivery$Temp)), anchor.value = min(Delivery$Temp),main = "Original Temperature Data")
hist.add.distribution.curve.normal(x = Delivery$Temp)

spc.individuals.chart(Delivery$Temp)

# When data are slightly positively skewed, and kurtosis
# is ok, the lognormal transformation may be used

# Lognormal Transformation
Delivery$lntemp<-log(Delivery$Temp)

# Check transformed data for normality
nqtr(summary.continuous(Delivery$lntemp),5)
hist.grouped(Delivery$lntemp, anchor.value = 3.61, interval.size = 0.03, freq = F)
hist.add.distribution.curve.normal(x = Delivery$lntemp, freq = F)

# Find the Upper Natural Process Limit and 
# Lower Natural Process Limit on the transformed data
natural.tolerance.normal(x = Delivery$lntemp)
Delivery.ln<-natural.tolerance.normal(x = Delivery$lntemp)
(LNPL.ln<-Delivery.ln$lower.limit)
(UNPL.ln<-Delivery.ln$upper.limit)

# Transform UNPL and LNPL back to original data
(LNPL<-exp(LNPL.ln))
(UNPL<-exp(UNPL.ln))

# Overall natural tolerance
UNPL-LNPL

# Create X and moving range chart with new limits for X chart
spc.chart.variables.individual.and.movingrange.generic.simple(individuals = Delivery$Temp
                                                              ,chart1.center.line = median(Delivery$Temp)
                                                              ,chart1.control.limits.lcl = LNPL
                                                              ,chart1.control.limits.ucl = UNPL)

