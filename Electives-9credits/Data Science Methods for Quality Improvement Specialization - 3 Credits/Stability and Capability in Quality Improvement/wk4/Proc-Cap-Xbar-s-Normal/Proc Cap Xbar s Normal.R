# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999, digits=5)

# Assessing Capability Xbar and s
# Import data file
pcb <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 4 - Process Capability/pcb.dat")
View(pcb)

# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(pcb$amps),5)
hist.grouped(pcb$amps, stat.lsl = 1.5, stat.usl = 3.5, stat.target = 2.5, main = "Histogram of Circuit Board Amps",freq = F)
hist.add.distribution.curve.normal(pcb$amps
                                   ,lwd=2
                                   ,freq=F)


# Test for normality within subgroups -------------------------------------
subgroup_norm<-ro(summary.continuous(fx = amps~sample, data = pcb, stat.mean = F, stat.var = F, stat.miss = F),4)
require(formattable)
formattable(subgroup_norm)
View(subgroup_norm)


# Create the Control Chart ------------------------------------------------
spcxbar.s<-spc.chart.variables.mean.and.meanstandarddeviation(data = pcb$amps
                                                              ,sample = pcb$sample
                                                              ,stat.lsl = 1.5
                                                              ,stat.target = 2.5
                                                              ,stat.usl = 3.5
                                                              ,chart1.main = "Mean Chart of Amps"
                                                              ,chart2.main = "Standard Deviation Chart")


# Calculate estimate of sigma from control chart --------------------------
(sbar<-mean(spcxbar.s$parameter.standard.deviations))
(c4<-spc.constant.calculation.c4(8))
(sig_est.s<-sbar/c4)

#  **** Capability and Performance Indices **** ---------------------------
(cap.xbar.s<-ro(spcxbar.s$capability,4))
formattable(cap.xbar.s)

# Cp only
spcxbar.s$capability[1,1:4]

# Cpk only
spcxbar.s$capability[2,1:4]

# Z-score example for Cpk
LSL<-1.5
USL<-3.5
xbar<-mean(pcb$amps)
Zu<-(USL-xbar)/sig_est.s
ro(pnorm(Zu, lower.tail = F),4)
Zl<-(LSL-xbar)/sig_est.s
pnorm(Zl, lower.tail = T)

Zu/3
abs(Zl/3)

spc.capability.cpU.simple(upper.specification = USL
                          ,process.center = xbar
                          ,process.variability = sig_est.s^2
                          ,n.sigma = 6)
                          

spc.capability.cpL.simple(lower.specification = LSL
                          ,process.center = xbar
                          ,process.variability = sig_est.s^2
                          ,n.sigma = 6)


# Cpm only
spcxbar.s$capability[3,1:4]

# Capability only
cap.xbar.s[c(1,2,3,10,11,12),]

# Pp only
spcxbar.s$capability[4,1:4]

# Ppk only
spcxbar.s$capability[5,1:4]

# Ppm only
spcxbar.s$capability[6,1:4]

# Performance only
cap.xbar.s[c(4:9),]

