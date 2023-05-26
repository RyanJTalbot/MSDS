# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# *** Branding Agency RFP Problem ***
RFP_Response_Time <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/RFP_Response_Time.dat", sep="")
View(RFP_Response_Time)
RFP<-RFP_Response_Time

# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(RFP$Time, stat.min=T), 5)
summary(Delivery$Temp)
hist.grouped(RFP$Time
             ,xlim=c(min(RFP$Time)-1,max(RFP$Time))
             ,ylim=c(0,0.12)
             ,anchor.value = min(RFP$Time)
             ,stat.target = 36
             ,stat.usl = 48
             ,main = "RFP Response Time"
             ,freq=F)
hist.add.distribution.curve.exp.low(x = RFP$Time
                                    ,low = min(RFP$Time)
                                    ,lwd=2
                                    ,freq = F)

# Exponential Test ------------------------------------------------
shapiro.wilk.exponentiality.test(x = RFP$Time)


# Generate 3 sigma chart limits for the X chart ------------------------------------
(nt.exp.low<-ro(natural.tolerance.exp.low(x = RFP$Time
                                          ,low = min(RFP$Time)),5))

# Find the UNPL and LNPL --------------------------
(LNPL.exp.low<-nt.exp.low$lower.limit)
(UNPL.exp.low<-nt.exp.low$upper.limit)

# Exponential Moving Range Chart --------------------------
# Monte Carlo Simulation
# Simulation of values anticipated from a standard exponential function with an 
# Omicron of 6.76 and a mean of 15.84:
mc<-rexp.low(n = 100000, low = 6.76, mean = mean(RFP$Time))

# Calculate Moving Range from simulated distribution
mr.exp.low<- c(abs(diff(mc)))


# Calculate natural tolerance for moving ranges ---------------------------
(nt.mr.exp   <-ro(natural.tolerance.exp(x = mr.exp.low),5))
(LNPL.mr.exp <-nt.mr.exp$lower.limit)
(UNPL.mr.exp <-nt.mr.exp$upper.limit)


# Create chart using the generic control chart ---------------------------
exp.low<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = RFP$Time
                                                                       ,chart1.control.limits.lcl = LNPL.exp.low
                                                                       ,chart1.center.line = mean(RFP$Time)
                                                                       ,chart1.control.limits.ucl = UNPL.exp.low
                                                                       ,chart1.main = "RFP Response Time"
                                                                       ,chart2.control.limits.lcl = LNPL.mr.exp
                                                                       ,chart2.center.line = mean(mr.exp.low)
                                                                       ,chart2.control.limits.ucl = UNPL.mr.exp)


# Changing rules -----------------------------------------------
rules <- spc.rulesets.nelson.1984.test.1.2.3.4()

# Turn off the lower control limit rule
rules$outside.limits <- spc.controlviolation.nelson.1984.test1.outside.zone.a.upper

# If using the mean for the X chart, adjust the run rules
rules$runs       <- NULL
rules$runs.above <- spc.controlviolation.nelson.1984.test2.runs.above.create(point.count = 6)
rules$runs.below <- spc.controlviolation.nelson.1984.test2.runs.below.create(point.count = 13)


# Recreate Control Chart after rule adjustments ---------------------------
exp.low<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = RFP$Time
                                                                       ,chart1.control.limits.lcl = LNPL.exp.low
                                                                       ,chart1.center.line = mean(RFP$Time)
                                                                       ,chart1.control.limits.ucl = UNPL.exp.low
                                                                       ,chart1.main = "RFP Response Time"
                                                                       ,chart1.control.rules = rules
                                                                       ,chart2.control.limits.lcl = LNPL.mr.exp
                                                                       ,chart2.center.line = mean(mr.exp.low)
                                                                       ,chart2.control.limits.ucl = UNPL.mr.exp)






# Capability Assessment -------------------------------------
# Now we can evaluate capability
data<-RFP$Time


# Define function for natural tolerance -----------------------------------
# Get natural tolerance for Exponential Low Distribution for the individual values
nt.exp.low<-natural.tolerance.exp.low(x = RFP$Time,low = min(RFP$Time))

# Define inputs -----------------------------------------------------------
LSL       <- NA
Target    <- 36
USL       <- 48
l.out     <- pexp.low(q = LSL, low = min(data), mean = mean(data), lower.tail = T)
u.out     <- pexp.low(q = USL, low = min(data), mean = mean(data), lower.tail = F)
total.out <- l.out + u.out
median    <- median(data)
mean      <- mean(data)
nt_est    <- nt.exp.low$natural.tolerance
s         <- sd(data)
obs.above.spec <- sum(data > USL)
obs.below.spec <- sum(data < LSL)
totaln         <- length(data)


# Capability and Performance Indices --------------------------------------
cap.exp<-spc.capability.summary.ungrouped.nonnormal.simple.R(stat.lsl = LSL
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
ro(formattable(cap.exp),4)


# Cp Only ----------------------------------------------
cap.exp[1,1:4]

# Cpk Calculation ---------------------------------------------
# Calculate Cpk using est % OOS
# Determine % OOS using Exponential Low curve
(l.out     <- pexp.low(q = LSL, low = min(data), mean = mean, lower.tail = T))
(u.out     <- pexp.low(q = USL, low = min(data), mean = mean, lower.tail = F))

# Make a visualization
# Check to see if these calculations make sense
hist.grouped(RFP$Time
             ,xlim=c(min(RFP$Time)-1,max(RFP$Time))
             ,ylim=c(0,0.12)
             ,anchor.value = min(RFP$Time)
             ,stat.target = 36
             ,stat.usl = 48
             ,main = "RFP Response Time"
             ,freq=F)
hist.add.distribution.curve.exp.low(x = RFP$Time
                                    ,low = min(RFP$Time)
                                    ,lwd=2
                                    ,freq = F)

# Equivalent Cpk
(Zu<-qnorm(0.01066834, lower.tail=F))

(Cpk.upper<-Zu/3)

# Cpk Only ----------------------------------------------------------------
cap.exp[2,1:4]

# Cpm Only ----------------------------------------------------------------
cap.exp[3,1:4] 


# Capability Indices ------------------------------------------------------
cap.exp[c(1:3,10:12),1:4]

# Pp only -----------------------------------------------------------------
cap.exp[4,1:4]

# Ppk Only ----------------------------------------------------------------
cap.exp[5,1:4]

# Ppm only ----------------------------------------------------------------
cap.exp[6,1:4]

# Performance Indices -----------------------------------------------------
cap.exp[4:9,1:4]

