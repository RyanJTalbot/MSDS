# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# *** The Food Distributor Delivery Problem *** ---------------------------
Delivery <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/Delivery.dat", sep="")
View(Delivery)

# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(Delivery$Temp), 5)
summary(Delivery$Temp)
hist.grouped(Delivery$Temp
             ,xlim=c(min(Delivery$Temp)-1,max(Delivery$Temp))
             ,anchor.value = min(Delivery$Temp)
             ,stat.lsl = 37
             ,stat.target = 43
             ,stat.usl = 49
             ,main = "Original Temperature Data")

# When data are slightly positively skewed, and kurtosis
# is ok, the lognormal transformation may be used

# Lognormal Transformation ------------------------------------------------
Delivery$lntemp<-log(Delivery$Temp)


# Check transformed data for normality ------------------------------------
nqtr(summary.continuous(Delivery$lntemp),5)
hist.grouped(Delivery$lntemp
             ,interval.size = .03
             ,stat.lsl= log(37)
             ,stat.target = log(43)
             ,stat.usl = log(49)
             ,main = "Transformed Temperature Data"
             ,freq = F)
hist.add.distribution.curve.normal(x = Delivery$lntemp
                                   ,lwd = 2    
                                   ,freq = F)

# Find the UNPL and LNPL on the transformed data --------------------------
natural.tolerance.normal(x = Delivery$lntemp)
Delivery.ln<-natural.tolerance.normal(x = Delivery$lntemp)
(LNPL.ln<-Delivery.ln$lower.limit)
(UNPL.ln<-Delivery.ln$upper.limit)


# Transform UNPL and LNPL back to original data ---------------------------
(LNPL<-exp(LNPL.ln))
(UNPL<-exp(UNPL.ln))


# Overall natural tolerance -----------------------------------------------
UNPL-LNPL


# Create control chart with UNPL and LNPL limits for the original  --------
spc.chart.variables.individual.and.movingrange.generic.simple(individuals = Delivery$Temp
                                                              ,chart1.center.line = median(Delivery$Temp)
                                                              ,chart1.control.limits.lcl = LNPL
                                                              ,chart1.control.limits.ucl = UNPL
                                                              ,chart1.main = "Truck Temperature")


# Capability Assessment -------------------------------------
# Now we can evaluate capability
data<-Delivery$Temp


# Define function for natural tolerance -----------------------------------
# Get natural tolerance for Lognormal Distribution for the individual values
f<-function(p,lower.tail) 
  
{
  qlnorm(p = p, meanlog = mean(log(data)), sdlog = sd(log(data)), lower.tail = lower.tail)
  }

natural.tolerance(f)


# Define inputs -----------------------------------------------------------
LSL       <- 37
Target    <- 43
USL       <- 49
l.out     <- plnorm(q = LSL, meanlog = mean(log(data)),sdlog = sd(log(data)),lower.tail = T)
u.out     <- plnorm(q = USL, meanlog = mean(log(data)),sdlog = sd(log(data)),lower.tail = F)
total.out <- l.out + u.out
median    <- median(data)
mean      <- mean(data)
nt_est    <- natural.tolerance(f)$natural.tolerance
s         <- sd(data)
obs.above.spec <- sum(data > USL)
obs.below.spec <- sum(data < LSL)
totaln         <- length(data)


# Capability and Performance Indices --------------------------------------
cap.ln<-spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL
                                                    ,stat.target = Target
                                                    ,stat.usl = USL
                                                    ,process.center.capability = median
                                                    ,process.center.performance = mean
                                                    ,process.variability = s^2
                                                    ,process.n.upper = obs.above.spec
                                                    ,process.n.lower = obs.below.spec
                                                    ,process.n       = totaln
                                                    ,natural.tolerance = nt_est
                                                    ,p.lower           = l.out
                                                    ,p.upper           = u.out)
ro(formattable(cap.ln),4)


# Cp Only ----------------------------------------------
cap.ln[1,1:4]

# Cpk Calculation ---------------------------------------------
# Calculate Cpk using est % OOS
# Determine % OOS using LogNormal curve
(l.out<-plnorm(q = LSL, meanlog = mean(log(data)), sdlog = sd(log(data)), lower.tail = T))
(u.out<-plnorm(q = USL, meanlog = mean(log(data)), sdlog = sd(log(data)), lower.tail = F))
(total.out<-l.out + u.out)

# Make a visualization
# Check to see if these calculations make sense
hist.grouped(Delivery$Temp
             ,stat.lsl = LSL
             ,stat.usl = USL
             ,stat.target = Target
             ,main = "Delivery Temp (LogNormal)"
             ,freq = F)
plot(function(x)dlnorm(x = x, meanlog = mean(log(data)), sdlog = sd(log(data))),35,55, add=TRUE)

# Equivalent Cpk
(Zl<-qnorm(0.004736549, lower.tail=T))
(Zu<-qnorm(0.02024086, lower.tail=F))

(Cpk.lower<-abs(Zl/3))
(Cpk.upper<-Zu/3)

# Cpk Only ----------------------------------------------------------------
cap.ln[2,1:4]

# Cpm Only ----------------------------------------------------------------
cap.ln[3,1:4]

# Capability Indices ------------------------------------------------------
cap.ln[c(1:3,10:12),1:4]

# Pp only -----------------------------------------------------------------
cap.ln[4,1:4]

# Ppk Only ----------------------------------------------------------------
cap.ln[5,1:4]

# Ppm only ----------------------------------------------------------------
cap.ln[6,1:4]

# Performance Indices -----------------------------------------------------
cap.ln[4:9,1:4]

