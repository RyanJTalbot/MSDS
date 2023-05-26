# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# C Chart -----------------------------------------------------------------
c.Chart <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 5 - Control Charts for Discrete Data/c Chart.dat")
View(c.Chart)

# Barplot of Poisson Probability Distribution -----------------------------
lambda<-9
x<-0

data<-dpois(x = 1:18, lambda = lambda)
names(data)<-1:18
barplot(data, xlab = "Units Per Interval", ylab = "P(X)", ylim = c(0, 1.2 * max(data)))


spc.c.chart<-spc.chart.attributes.counts.c.poissondistribution.simple(counts = c.Chart$count
                                                                      ,chart1.point.cex = 1.3
                                                                      ,chart1.line.lwd=2
                                                                      ,chart1.main = "c chart - # Breaks per 200 Linear Yard")
# Control Limits and Centerline
unique(spc.c.chart$chart1.center.line)


# Poisson Table -----------------------------------------------------------
ro(table.dist.poisson(lambda = 21.36)[1:43,],4)


# Control Limits and Centerline -------------------------------------------
(c.UCL<-unique(spc.c.chart$chart1.control.limits.ucl))
(c.center<-unique(spc.c.chart$chart1.center.line))
(c.LCL<-unique(spc.c.chart$chart1.control.limits.lcl))


# Evaluate Chart for Control ----------------------------------------------
any(spc.c.chart$chart1.is.control.violation$overall.results)



# Determine which rules were violated -------------------------------------
lapply(spc.c.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )



# Determine which points  -------------------------------------------------
lapply(spc.c.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )



# Control Charts by Set ---------------------------------------------------
# Split data by Set
c.set1<-subset(x = c.Chart, subset = c.Chart$set==1)
c.set2<-subset(x = c.Chart, subset = c.Chart$set==2)

# Chart both side by side
par(mfrow=c(1,2))
spc.c.set1<-spc.chart.attributes.counts.c.poissondistribution.simple(counts = c.set1$count, combine.charts="leave.par.alone", chart1.ylim=c(0,50), chart1.main = "C Chart - Set 1")
spc.c.set2<-spc.chart.attributes.counts.c.poissondistribution.simple(counts = c.set2$count, combine.charts="leave.par.alone", chart1.ylim=c(0,50), chart1.main = "C Chart - Set 2")
par(mfrow=c(1,1))


# Pull out information
(set1.c.ucl<-unique(spc.c.set1$chart1.control.limits.ucl))
(set1.c.center<-unique(spc.c.set1$chart1.center.line))
(set1.c.lcl<-unique(spc.c.set1$chart1.control.limits.lcl))

(set2.c.ucl<-unique(spc.c.set2$chart1.control.limits.ucl))
(set2.c.center<-unique(spc.c.set2$chart1.center.line))
(set2.c.lcl<-unique(spc.c.set2$chart1.control.limits.lcl))



# Capability (if the process was in control) ------------------------------
# Use the centerline as the estimate for lambda
unique(spc.c.chart$chart1.center.line)

# Calculate the proportion above the industry standard
ro(table.dist.poisson(lambda = 21.36)[7:43,],4)

# Probability of getting 28 or more
0.0958

ppois(q = 27.5, lambda = 21.36, lower.tail = F)

# Convert to Z Score
(Z<-qnorm(p = 0.09575363, lower.tail = F))

# Convert Z to Cpk_eq
(Cpk.eq<-Z/3)
