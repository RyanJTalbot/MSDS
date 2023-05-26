# Natural Tolerance Functions
require(lolcat)
require(fitdistrplus)
require(SuppDists)

require(devtools)
install_github("burrm/lolcatext")
require(lolcatext) # New package for Johnson Su fit

# Normal ------------------------------------------------------------------
natural.tolerance.normal(x = data)

# LogNormal ---------------------------------------------------------------
p<-0.00135
lower.tail = F
f<-function(p,lower.tail) 
{qlnorm(p = p, meanlog = mean(log(data)), sdlog = sd(log(data)), lower.tail = lower.tail)
}
natural.tolerance(f)

# Exponential -------------------------------------------------------------
natural.tolerance.exp(x = data)


# Exponential Low ---------------------------------------------------------
natural.tolerance.exp.low(x = data, low = min(data))

# Weibull -----------------------------------------------------------------
(fit.w<-fitdist(data, "weibull"))
(shape.w<-fit.w$estimate[1])
(scale.w<-fit.w$estimate[2])

p<-0.00135
lower.tail = F
f<-function(p,lower.tail) 
{
  qweibull(p = p, shape = shape.w, scale = scale.w, lower.tail = lower.tail)
}
natural.tolerance(f)

# Gamma -------------------------------------------------------------------
(fit.g<-fitdist(data, "gamma"))
(shape.g<-fit.g$estimate[1])
(rate.g<-fit.g$estimate[2])

p<-0.00135
lower.tail = F
f<-function(p,lower.tail) 
{
  qgamma(p = p, shape = shape.g, rate = rate.g, lower.tail = lower.tail)
}
natural.tolerance(f)


# Johnson Su --------------------------------------------------------------
j.fit <- dist.fit.johnson.su(x =  data)

# Get natural tolerance of Johnson distribution
natural.tolerance(j.fit$q.fn)
