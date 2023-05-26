# **** Averages as Individuals - Spindle Example ****
#      Large range within
require(lolcat)

spindle <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 2 -  Xbar and R S charts X and MR charts/spindle.dat")
View(spindle)

# Save the column with the mean as its own file
spindle.mean<-spindle$Spindle_Mean
View(spindle.mean)

# Drop the mean column from the dataset
spindle<-spindle[-7]

# Transpose data
xbar.r.new<-transform.dependent.format.to.independent.format(data = spindle)
View(xbar.r.new)

# Create a sample column
xbar.r.new$sample<-rep(1:25) 

# Drop the Cell column
xbar.r.new<-xbar.r.new[-1]

# Sort by sample
xbar.r.column<-xbar.r.new[order(xbar.r.new$sample),]
View(xbar.r.column)

# Create the Xbar and R Chart
spc.chart.variables.mean.and.meanrange(data = xbar.r.column$measure, sample = xbar.r.column$sample, chart1.main="Xbar Chart", chart2.main="R Chart", chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

# Create Summary Statistics
nqtr(summary.continuous(xbar.r.column$measure), 5) #Overall
nqtr(summary.all.variables(spindle),5)

# Create Histogram
hist.grouped(xbar.r.column$measure) #Overall

par(mfrow=c(2,3))
hist.grouped(spindle$Spindle.1, main = "Spindle 1", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
hist.grouped(spindle$Spindle.2, main = "Spindle 2", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
hist.grouped(spindle$Spindle.3, main = "Spindle 3", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
hist.grouped(spindle$Spindle.4, main = "Spindle 4", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
hist.grouped(spindle$Spindle.5, main = "Spindle 5", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
hist.grouped(spindle$Spindle.6, main = "Spindle 6", xlim = c(87,107), anchor.value = 87, interval.size = 1, freq = F)
par(mfrow = c(1,1))

# Create 2 Overall Control Charts
spc.out<-spc.chart.variables.mean.and.meanrange(data = xbar.r.column$measure, sample = xbar.r.column$sample, chart1.main="Xbar Chart", chart2.main="R Chart", chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

# 1. X and MR chart of the Means - All Spindles
spc.chart.variables.individual.and.movingrange.normal.simple(spc.out$parameter.means
                                                             ,chart1.main = "X and MR of Means")

# 2. X and MR chart of the Ranges within - All Spindles
spc.chart.variables.individual.and.movingrange.normal.simple(spc.out$parameter.ranges
                                                             ,chart1.main = "X and MR of Ranges")

# Create 6 Individual Charts by Spindle
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.1, chart1.main = "X Chart - Spindle 1")
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.2, chart1.main = "X Chart - Spindle 2")
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.3, chart1.main = "X Chart - Spindle 3")
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.4, chart1.main = "X Chart - Spindle 4")
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.5, chart1.main = "X Chart - Spindle 5")
spc.chart.variables.individual.and.movingrange.normal.simple(spindle$Spindle.6, chart1.main = "X Chart - Spindle 6")

# *** Random Effects ANOVA ****
# View structure of data file
str(xbar.r.column) 

# Make sample a factor
xbar.r.column$sample<-as.factor(xbar.r.column$sample)

# The ANOVA Execution command 
raov.out <- aov(measure ~ sample, data = xbar.r.column) 

# Store and Display the results of the ANOVA
sum.raov.out <- summary(raov.out)

# View the structure of the Summary ANOVA output object
str(sum.raov.out) 

# Note low F value
sum.raov.out[[1]]

