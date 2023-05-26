# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Import data file
Tank6 <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 4 - Process Capability/Tank6.dat", sep="")
View(Tank6)

# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(Tank6$Concentration),5)
hist.ungrouped(Tank6$Concentration
               ,stat.lsl = 29
               ,stat.usl = 35
               ,stat.target = 32
               ,main = "Histogram of Concentration"
               ,freq = F)
hist.add.distribution.curve.normal(Tank6$Concentration
                                   ,lwd=2
                                   ,freq=F)


# Create Control Chart ----------------------------------------------------
spcx.mr<-spc.chart.variables.individual.and.movingrange.normal.simple(individuals = Tank6$Concentration
                                                                      ,stat.lsl = 29
                                                                      ,stat.target = 32
                                                                      ,stat.usl = 35)

# Calculate estimate of sigma from control chart
mrbar<-mean(abs(diff(Tank6$Concentration)))
d2<-spc.constant.calculation.d2(2)
(sig_est.mr<-mrbar/d2)

# **** Capability Indices using mrbar/d2 ****
# Calculate the natural tolerance 
# If normally distributed, this is 6*sig_est
(nt_est<-6*sig_est.mr)

#  **** Capability and Performance Indices **** ---------------------------
(cap.x.mr<-ro(spcx.mr$capability,4))
formattable(cap.x.mr)

# Cp only
spcx.mr$capability[1,1:4]

# Cpk only
spcx.mr$capability[2,1:4]

# Cpm only
spcx.mr$capability[3,1:4]

# Capability only
cap.x.mr[c(1,2,3,10,11,12),]

# Pp only
spcx.mr$capability[4,1:4]

# Ppk only
spcx.mr$capability[5,1:4]

# Ppm only
spcx.mr$capability[6,1:4]

# Performance only
cap.x.mr[c(4:9),]

