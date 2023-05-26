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

# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(mapsensor$z_axis, stat.min=T),5)
hist.grouped(mapsensor$z_axis
             ,stat.lsl = 0.55
             ,stat.target = 0.95
             ,stat.usl = 1.35
             , freq=F)

# Capability Assessment -------------------------------------
# Now we can evaluate capability
data<-mapsensor$z_axis


# Define function for natural tolerance -----------------------------------
# Goodness of fit for the Gamma
(fit.g<-fitdist(data = mapsensor$z_axis, distr = "gamma"))
(shape<-fit.g$estimate[1])
(rate<-fit.g$estimate[2])

p<-.00135 
lower.tail<-FALSE 
f<-function(p,lower.tail) 
{qgamma(p, shape = shape, rate = rate, lower.tail = lower.tail)
} 
(nt.gamma<-natural.tolerance(f))


# Define inputs -----------------------------------------------------------
LSL       <- 0.55
Target    <- 0.95
USL       <- 1.35
l.out     <- pgamma(q = LSL, shape = shape, rate = rate, lower.tail = T)
u.out     <- pgamma(q = USL, shape = shape, rate = rate, lower.tail = F)
total.out <- l.out + u.out
median    <- median(data)
mean      <- mean(data)
nt_est    <- nt.gamma$natural.tolerance
s         <- sd(data)
obs.above.spec <- sum(data > USL)
obs.below.spec <- sum(data < LSL)
totaln         <- length(data)


# Capability and Performance Indices --------------------------------------
cap.gamma<-spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL
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
ro(formattable(cap.gamma),4)


# Cp Only ----------------------------------------------
cap.gamma[1,1:4]

# Cpk Calculation ---------------------------------------------
# Calculate Cpk using est % OOS
# Determine % OOS using Gamma curve
l.out     <- pgamma(q = LSL, shape = shape, rate = rate, lower.tail = T)
u.out     <- pgamma(q = USL, shape = shape, rate = rate, lower.tail = F)

# Make a visualization
# Check to see if these calculations make sense
hist.grouped(mapsensor$z_axis
             ,stat.lsl = 0.55
             ,stat.target = 0.95
             ,stat.usl = 1.35
             ,main = "Map Sensor - Gamma Distribution"
             ,freq = F)
plot(function(x)dgamma(x = x, shape = shape, rate = rate),-0.5,8, add=TRUE)

# Equivalent Cpk
(Zu<-qnorm(0.4344965, lower.tail=F))

(Cpk.upper<-Zu/3)

# Cpk Only ----------------------------------------------------------------
cap.gamma[2,1:4]

# Cpm Only ----------------------------------------------------------------
cap.gamma[3,1:4] 


# Capability Indices ------------------------------------------------------
cap.gamma[c(1:3,10:12),1:4]

# Pp only -----------------------------------------------------------------
cap.gamma[4,1:4]

# Ppk Only ----------------------------------------------------------------
cap.gamma[5,1:4]

# Ppm only ----------------------------------------------------------------
cap.gamma[6,1:4]

# Performance Indices -----------------------------------------------------
cap.gamma[4:9,1:4]

