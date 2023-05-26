# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999, digits=7)


# Assessing Capability Xbar and R -----------------------------------------
# Import data file
bearing <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 4 - Process Capability/bearing.dat")
View(bearing)


# Descriptive Statistics and Histogram ------------------------------------
nqtr(summary.continuous(bearing$diameter),5)
hist.grouped(bearing$diameter
             ,stat.lsl = 1.035
             ,stat.usl = 1.047
             ,stat.target = 1.041
             ,main = "Histogram of Cartridge Bearing Data"
             ,freq = F)
hist.add.distribution.curve.normal(bearing$diameter, freq=F, lwd = 2)


# Xbar and R Control Chart ------------------------------------------------
spcxbar.r<-spc.chart.variables.mean.and.meanrange(data = bearing$diameter
                                                ,sample = bearing$sample
                                                ,stat.lsl = 1.035
                                                ,stat.target = 1.041
                                                ,stat.usl = 1.047
                                                ,chart1.main = "Mean Chart - Diameter"
                                                ,chart2.main = "Range Chart")

# Calculate estimate of sigma from control chart
(rbar<-unique(spcxbar.r$chart2.center.line))
(d2<-spc.constant.calculation.d2(5))
(sig_est<-rbar/d2)

#  **** Capability and Performance Indices **** ---------------------------
cap.xbar.r<-ro(spcxbar.r$capability,5)
formattable(cap.xbar.r)

# Cp only
spcxbar.r$capability[1,1:4]

# Cpk only
spcxbar.r$capability[2,1:4]

# Cpm only
spcxbar.r$capability[3,1:4]

# Capability only
formattable(cap.xbar.r[c(1,2,3,10,11,12),])

# Calculate estimate of sigma overall
(s<-sd(bearing$diameter))

# Pp only
spcxbar.r$capability[4,1:4]

# Ppk only
spcxbar.r$capability[5,1:4]

# Ppm only
spcxbar.r$capability[6,1:4]

# Performance only
formattable(cap.xbar.r[c(4:9),])

