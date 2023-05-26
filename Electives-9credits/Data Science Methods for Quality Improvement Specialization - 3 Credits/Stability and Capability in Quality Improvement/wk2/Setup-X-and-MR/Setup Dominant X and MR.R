# **** Multiple Setup X and Moving Range # ****
#      Small range within

require(lolcat)

# Import data set
setup <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 2 -  Xbar and R S charts X and MR charts/setup.dat")
View(setup)

# Create Xbar and R Chart 
nqtr(summary.continuous(setup$measure),5)
spc.chart.variables.mean.and.meanrange(data = setup$measure, sample = setup$sample)

# Histogram
hist.grouped(setup$measure,interval.size = 1, anchor.value=96, freq = F)
hist.add.distribution.curve.normal(x = setup$measure, freq = F)

# Calculate averages by group
averages<-aggregate(x = setup$measure, by=list(setup$sample), FUN=mean)
View(averages)

# Test averages for normality
nqtr(summary.continuous(averages$x),5)
hist.grouped(averages$x, interval.size = 1, anchor.value=96, xlim = c(96,105),freq = F)
hist.add.distribution.curve.normal(x = averages$x, freq = F)

# Create averages as individuals chart
spc.chart.variables.individual.and.movingrange.normal.simple(averages$x
                                                             ,chart1.main = "Averages (Mean) as Individuals"
                                                             ,chart2.main = "Moving Range of Mean")


# Create Range within as individuals chart
spc.ranges<-spc.chart.variables.mean.and.meanrange(data = setup$measure, 
                                       sample = setup$sample)
range.within<-spc.ranges$chart2.series
                                    
# Put Range within on an Individuals chart
spc.chart.variables.individual.and.movingrange.normal.simple(range.within
                                                             ,chart1.main = "Range Within"
                                                             ,chart2.main = "Moving Range of Ranges")



# *** Random Effects ANOVA ****
# View structure of data file
str(setup) 

# Make sample a factor
setup$sample<-as.factor(setup$sample)

# The ANOVA Execution command 
raov.out <- aov(measure ~ sample, data = setup) 

# Store and Display the results of the ANOVA
sum.raov.out <- summary(raov.out)

# View the structure of the Summary ANOVA output object
str(sum.raov.out) 

# View the source table
sum.raov.out[[1]]
# Note the difference between Mean Square between sample
# and Mean Square of the residuals (within)

# Importance Calculation
(MSB <- sum.raov.out[[1]]$"Mean Sq"[1]) # Retrieve MS Between
(MSW <- sum.raov.out[[1]]$"Mean Sq"[2]) # Retrieve MS Within
n <- 5 # n per group
n1 <- n-1 # (n - 1)
(bcv <- (MSB - MSW)/n) # Between Component Variance
(VarY <- (MSB + n1*MSW)/n) # Variance Total (aka Var(Y))
(rI <- bcv/(bcv+MSW)) # Compute Importance

