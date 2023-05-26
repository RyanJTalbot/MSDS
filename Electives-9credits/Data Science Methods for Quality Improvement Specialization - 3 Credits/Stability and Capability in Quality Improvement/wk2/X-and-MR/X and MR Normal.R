# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Concentration Example
Chrome <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 2 -  Xbar and R S charts X and MR charts/Chrome.dat", sep="")
View(Chrome)


# View Summary Statistics -------------------------------------------------
nqtr(summary.continuous(Chrome$Concentration),5)
hist.ungrouped(Chrome$Concentration)
hist.add.distribution.curve.normal(x = Chrome$Concentration)

# Create the Chart
spc.chart.variables.individual.and.movingrange.normal.simple(Chrome$Concentration)

# Create Chart using Method 1 - Average Moving Range
# 3 sigma limits
spc.out<-spc.chart.variables.individual.and.movingrange.normal.simple(Chrome$Concentration)

# 2 sigma limits
(uclx.2<-unique(spc.out$chart1.center.line)+2/3*((3/spc.constant.calculation.d2(2))*unique(spc.out$chart2.center.line)))
(lclx.2<-unique(spc.out$chart1.center.line)-2/3*((3/spc.constant.calculation.d2(2))*unique(spc.out$chart2.center.line)))

# Put in 2 sigma limits
spc.chart.variables.individual.and.movingrange.normal.simple(Chrome$Concentration
                                                             ,chart1.control.limits.ucl = uclx.2
                                                             ,chart1.control.limits.lcl = lclx.2)

# Create Chart using Method 2 - Standard Deviation
# Estimate standard deviation from process
(sd.cc<-sd(Chrome$Concentration))
(uclx.sd<-unique(spc.out$chart1.center.line)+ 3*sd.cc)
(lclx.sd<-unique(spc.out$chart1.center.line)- 3*sd.cc)

spc.chart.variables.individual.and.movingrange.normal.simple(Chrome$Concentration
                                                             ,chart1.control.limits.ucl = uclx.sd
                                                             ,chart1.control.limits.lcl = lclx.sd)

# Create Chart using Method 3 - Median Moving Range
# Calculate the Median Moving Range
(mmr<-median(abs(diff(Chrome$Concentration))))
(uclx.mmr<-unique(spc.out$chart1.center.line)+((3/spc.constant.calculation.d4(2))*mmr))
(lclx.mmr<-unique(spc.out$chart1.center.line)-((3/spc.constant.calculation.d4(2))*mmr))
(uclmr.mmr<-(spc.constant.calculation.d2(2)+3*spc.constant.calculation.d3(2))/spc.constant.calculation.d4(2))

# Put in new limits
chrome.out<-spc.chart.variables.individual.and.movingrange.normal.simple(Chrome$Concentration
                                                             ,chart1.control.limits.ucl = uclx.mmr
                                                             ,chart1.center.line = median(Chrome$Concentration)
                                                             ,chart1.control.limits.lcl = lclx.mmr
                                                             ,chart2.control.limits.ucl = uclmr.mmr
                                                             ,chart2.center.line = mmr)


# View control limits
lims.chart.2 <- unique(data.frame(lcl=chrome.out$chart2.control.limits.lcl
                                  ,center=chrome.out$chart2.center.line
                                  ,ucl=chrome.out$chart2.control.limits.ucl))
lims.chart.2
                       
lims.chart.1 <- unique(data.frame(lcl=chrome.out$chart1.control.limits.lcl
                                  ,center=chrome.out$chart1.center.line
                                  ,ucl=chrome.out$chart1.control.limits.ucl))
lims.chart.1


# Estimate standard deviation from control chart --------------------------
chrome.out<-spc.chart.variables.individual.and.movingrange.normal.simple(individuals = Chrome$Concentration)
(MR.bar<-unique(chrome.out$chart2.center.line))
(d2<-spc.constant.calculation.d2(sample.size = 2))
(sigma.cc<-MR.bar/d2)


# *** Process Capability ****
# *** Requires Control ****
# Using sigma estimate of MRbar/d2 (Cp)
spc.capability.cp.simple(lower.specification = 29, upper.specification = 35, process.natural.tolerance = 6*sigma.cc)

# Using sigma estimate of overall standard deviation (Pp)
spc.capability.cp.simple(lower.specification = 29, upper.specification = 35, process.natural.tolerance = 6*sd(Chrome$Concentration))
