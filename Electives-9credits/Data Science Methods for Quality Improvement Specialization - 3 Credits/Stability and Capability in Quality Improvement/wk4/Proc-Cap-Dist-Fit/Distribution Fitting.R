# Startup Code
require(lolcat)
require(formattable)
require(fitdistrplus) # For distribution fitting
require(SuppDists) # For Johnson distribution
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# **** Distribution Fitting ****
mapsensor <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/mapsensor.dat", sep="")
View(mapsensor)

# Make chart (not recommend without first looking at shape!)
spc.chart.variables.individual.and.movingrange.normal.simple(mapsensor$z_axis)


# Descriptive Summary -----------------------------------------------------

# Descriptive Statistics
nqtr(summary.continuous(mapsensor$z_axis, stat.min=T),5)

# Histogram
hist.grouped(mapsensor$z_axis, freq=F)

# Test for exponentiality
shapiro.wilk.exponentiality.test(mapsensor$z_axis)


# Goodness of Fit Testing for One Distribution -------------------------------------------------

# Goodness of fit for the Exponential
(fit.exp<-fitdist(data = mapsensor$z_axis, distr = "exp"))

# https://cran.r-project.org/web/views/Distributions.html

# Goodness of fit statistics
(gof.exp<-gofstat(fit.exp, fitnames = "Exponential"))

# Goodness of fit p values
(chisquare.exp<-gof.exp$chisqpvalue)
(ad.exp<-gof.exp$adtest)
(aic.out<-gof.exp$aic) # Lower is best - Akaike information criterion

# View cumulative distribution function
cdfcomp(fit.exp, legendtext = "Exponential")

# View density function
denscomp(fit.exp, legendtext = "Exponential")

# View Quantile-Quantile plot (Q-Q Plot)
qqcomp(fit.exp, legendtext = "Exponential")

# View Probability-Probability plot(P-P Plot)
ppcomp(fit.exp, legendtext = "Exponential")


# Goodness of Fit Testing for Multiple Distributions ----------------------

# Let's review several options at once ....
# Goodness of fit for the Weibull
(fit.w<-fitdist(data = mapsensor$z_axis, distr = "weibull"))
# Goodness of fit for the Gamma
(fit.g<-fitdist(data = mapsensor$z_axis, distr = "gamma"))
# Goodness of fit for the Log-Normal
(fit.ln<-fitdist(data = mapsensor$z_axis, distr = "lnorm"))

# Goodness of fit statistics
(gof.out<-gofstat(list(fit.exp, fit.w, fit.g, fit.ln)
                  , fitnames = c("Exponential","Weibull", "Gamma", "Log-Normal")))

# Goodness of fit p values
(chisquare.out<-gof.out$chisqpvalue)
(ad.out<-gof.out$adtest)
(aic.out<-gof.out$aic) # Lower is best - Akaike information criterion

# View cumulative distribution function
cdfcomp(list(fit.exp,fit.w, fit.g, fit.ln), legendtext = c("Exponential","Weibull", "Gamma", "Log-Normal"))

# View density function
denscomp(list(fit.exp,fit.w, fit.g, fit.ln), legendtext = c("Exponential","Weibull", "Gamma", "Log-Normal"))

# View Quantile-Quantile plot (Q-Q Plot)
qqcomp(list(fit.exp,fit.w, fit.g, fit.ln), legendtext = c("Exponential","Weibull", "Gamma", "Log-Normal"))

# View Probability-Probability plot(P-P Plot)
ppcomp(list(fit.exp,fit.w, fit.g, fit.ln), legendtext = c("Exponential","Weibull", "Gamma", "Log-Normal"))

# Goodness of fit for the Johnson family ----------------------------------

# Goodness of fit for the Johnson Distribution
(parms<-JohnsonFit(t = mapsensor$z_axis)) # get starting parameters

# Call the Johnson Function
source("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/Johnson Function.R")

# Fit the Johnson SU Distribution
(fit.john<-fitdist(
  data = mapsensor$z_axis, 
  distr = "john", 
  start = list(gamma = parms$gamma, 
               delta = parms$delta, 
               xi = parms$xi, 
               lambda = parms$lambda 
  )
  ,method="qme"
  ,probs = c(0.25, 0.5, 0.75, 0.99)
))

# Goodness of fit statistics
(gof.john<-gofstat(fit.john))

# Goodness of fit p values
(chisquare.john<-gof.john$chisqpvalue)
(ad.john<-gof.john$adtest)
(aic.john<-gof.john$aic) # Lower is best - Akaike information criterion

# View cumulative distribution function
cdfcomp(fit.john, legendtext = "Johnson SU")

# View density function
denscomp(fit.john, legendtext = "Johnson SU", xlim = c(-2,6))

# View Quantile-Quantile plot (Q-Q Plot)
qqcomp(fit.john, legendtext = "Johnson SU")

# View Probability-Probability plot(P-P Plot)
ppcomp(fit.john, legendtext = "Johhnson SU")

# Calculate the Natural Tolerance to get Control Limits -------------------

# Get natural tolerance of Johnson distribution
p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qJohnson(p = p, parms = parms, lower.tail = lower.tail)
} 
(nt.john<-natural.tolerance(f))
(LNPL.john<-nt.john$lower.limit)
(UNPL.john<-nt.john$upper.limit)

# Check to see if these limits make sense
hist.grouped(mapsensor$z_axis
             ,stat.lsl = LNPL.john
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.john
             ,stat.usl.label = "UNPL"
             ,xlim = c(-3,15)
             ,ylim = c(0, 0.7)
             ,anchor.value = 0
             ,main = "Johnson Distribution"
             ,freq = F)
plot(function(x)dJohnson(x = x, parms = parms),-2,10, add=TRUE)

# Calculate the Natural Tolerance for the Gamma Distribution
# Goodness of fit for the Gamma
(fit.g<-fitdist(data = mapsensor$z_axis, distr = "gamma"))
(shape<-fit.g$estimate[1])
(rate<-fit.g$estimate[2])

# Get natural tolerance of Gamma distribution
p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qgamma(p, shape = shape, rate = rate, lower.tail = lower.tail)
} 
(nt.gamma<-natural.tolerance(f))
(LNPL.gamma<-nt.gamma$lower.limit)
(UNPL.gamma<-nt.gamma$upper.limit)

# Do these limits make sense?
hist.grouped(mapsensor$z_axis
             ,stat.lsl = LNPL.gamma
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.gamma
             ,stat.usl.label = "UNPL"
             ,xlim = c(0,8)
             ,anchor.value = 0
             ,main = "Gamma Distribution"
             ,freq = F)
plot(function(x)dgamma(x = x, shape = shape, rate = rate),-0.5,8, add=TRUE)

# Get natural tolerance of Exponential distribution
# Goodness of fit for the Exponential
(fit.exp<-fitdist(data = mapsensor$z_axis, distr = "exp"))
(rate.exp<-fit.exp$estimate[1])

# Get natural tolerance of Exponential distribution
p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qexp(p = p, rate = rate.exp, lower.tail = lower.tail)
} 
(nt.exp<-natural.tolerance(f))
(LNPL.exp<-nt.exp$lower.limit)
(UNPL.exp<-nt.exp$upper.limit)

# OR
natural.tolerance.exp(x = mapsensor$z_axis)

# Do these limits make sense?
hist.grouped(mapsensor$z_axis
             ,stat.lsl = LNPL.exp
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.exp
             ,stat.usl.label = "UNPL"
             ,xlim = c(0,10)
             ,ylim = c(0, 0.7)
             ,anchor.value = 0
             ,main = "Exponential Distribution"
             ,freq = F)
plot(function(x)dexp(x = x, rate = rate.exp),-0.5,10, add=TRUE)

# Get natural tolerance of Weibull distribution
# Goodness of fit for the Weibull
(fit.w<-fitdist(data = mapsensor$z_axis, distr = "weibull"))
(shape.w<-fit.w$estimate[1])
(scale.w<-fit.w$estimate[2])

# Get natural tolerance of Weibull distribution
p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qweibull(p = p, shape = shape.w, scale = scale.w, lower.tail = lower.tail)
} 
(nt.w<-natural.tolerance(f))
(LNPL.w<-nt.w$lower.limit)
(UNPL.w<-nt.w$upper.limit)

# Do these limits make sense?
hist.grouped(mapsensor$z_axis
             ,stat.lsl = LNPL.w
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.w
             ,stat.usl.label = "UNPL"
             ,xlim = c(0,8)
             ,ylim = c(0, 0.7)
             ,anchor.value = 0
             ,main = "Weibull Distribution"
             ,freq = F)
plot(function(x)dweibull(x = x, shape = shape.w, scale = scale.w),-0.5,10, add=TRUE)

# Get natural tolerance of LogNormal distribution
# Goodness of fit for the LogNormal
(fit.ln<-fitdist(data = mapsensor$z_axis, distr = "lnorm"))
(meanlog<-fit.ln$estimate[1])
(sdlog<-fit.ln$estimate[2])

# Get natural tolerance of LogNormal distribution
p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qlnorm(p = p, meanlog = meanlog, sdlog = sdlog, lower.tail = lower.tail)
} 
(nt.ln<-natural.tolerance(f))
(LNPL.ln<-nt.ln$lower.limit)
(UNPL.ln<-nt.ln$upper.limit)

# Do these limits make sense?
hist.grouped(mapsensor$z_axis
             ,stat.lsl = LNPL.ln
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.ln
             ,stat.usl.label = "UNPL"
             ,xlim = c(0,15)
             ,ylim = c(0, 0.7)
             ,anchor.value = 0
             ,main = "LogNormal Distribution"
             ,freq = F)
plot(function(x)dlnorm(x = x, meanlog = meanlog, sdlog = sdlog),-0.5,10, add=TRUE)

# Make Chart with Gamma Distribution for the individuals
spc.map<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = mapsensor$z_axis
                                                                       ,chart1.center.line = median(mapsensor$z_axis)
                                                                       ,chart1.control.limits.lcl = LNPL.gamma
                                                                       ,chart1.control.limits.ucl = UNPL.gamma)



# Determine underlying distribution of the moving ranges
mr.ms<-abs(diff(mapsensor$z_axis))

summary.continuous(mr.ms)
hist.grouped(mr.ms)
shapiro.wilk.exponentiality.test(mr.ms)
# Use exponential limits for the moving range

# Get natural tolerance of exponential distribution
nt.mr.exp<-natural.tolerance.exp(mr.ms)
(LNPL.mr.exp<-nt.mr.exp$lower.limit)
(UNPL.mr.exp<-nt.mr.exp$upper.limit)

# Do these limits make sense?
hist.grouped(mr.ms
             ,stat.lsl = LNPL.mr.exp
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.mr.exp
             ,stat.usl.label = "UNPL"
             ,xlim = c(0,9)
             ,ylim = c(0,0.8)
             ,anchor.value = 0
             ,main = "Exponential Distribution"
             ,freq = F)
hist.add.distribution.curve.exp(x = mr.ms, freq = F)


# Make Chart with Gamma Distribution for the individuals
# and exponential distribution for the moving range
spc.chart.variables.individual.and.movingrange.generic.simple(individuals = mapsensor$z_axis
                                                              ,chart1.center.line = median(mapsensor$z_axis)
                                                              ,chart1.control.limits.lcl = LNPL.gamma
                                                              ,chart1.control.limits.ucl = UNPL.gamma
                                                              ,chart2.control.limits.lcl = LNPL.mr.exp
                                                              ,chart2.control.limits.ucl = UNPL.mr.exp)




# Change rules
rules            <- spc.rulesets.nelson.1984.test.1.2.3.4()
rules$runs       <- NULL
rules$runs.above <- spc.controlviolation.nelson.1984.test2.runs.above.create(point.count = 6)
rules$runs.below <- spc.controlviolation.nelson.1984.test2.runs.below.create(point.count = 13)


xmr<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = mapsensor$z_axis                                                                                                                 ,chart1.control.limits.lcl = LNPL.gamma
                                                              ,chart1.control.limits.ucl = UNPL.gamma
                                                              ,chart2.control.limits.lcl = LNPL.mr.exp
                                                              ,chart2.control.limits.ucl = UNPL.mr.exp
                                                              ,chart1.control.rules = rules)


runs.overall <- xmr$chart1.is.control.violation$rule.results$runs.above | xmr$chart1.is.control.violation$rule.results$runs.below
runs.overall
