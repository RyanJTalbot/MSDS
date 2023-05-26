# Startup Code
require(lolcat)

# **** Xbar and S Charts ****
# Import Data -------------------------------------------------------------
xbar.s <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 2 -  Xbar and R S charts X and MR charts/xbar-s.dat")
View(xbar.s)

# Transpose data ----------------------------------------------------------
xbar.s.new<-transform.dependent.format.to.independent.format(data = xbar.s)
View(xbar.s.new)

# Create a sample column
xbar.s.new$sample<-rep(1:32) 

# Drop the Cell column
xbar.s.new<-xbar.s.new[-1]

# Sort by sample
xbar.s.column<-xbar.s.new[order(xbar.s.new$sample),]
View(xbar.s.column)

# Create the Xbar and s Chart ---------------------------------------------
spc.chart.variables.mean.and.meanstandarddeviation(data = xbar.s.column$measure
                                                   , sample = xbar.s.column$sample
                                                   , chart1.main="Mean Chart"
                                                   , chart2.main="S Chart"
                                                   , chart1.ylab="Amps"
                                                   , chart2.ylab="Std. Dev.")

# Extract Control Limits and Centerline for each chart --------------------
xbar.s.eval<-spc.chart.variables.mean.and.meanstandarddeviation(data = xbar.s.column$measure
                                                                , sample = xbar.s.column$sample
                                                                , chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

lims.chart.1 <- unique(data.frame(
  lcl     = xbar.s.eval$chart1.control.limits.lcl
  ,center = xbar.s.eval$chart1.center.line
  ,ucl    = xbar.s.eval$chart1.control.limits.ucl
))

lims.chart.1

lims.chart.2 <- unique(data.frame(
  lcl     = xbar.s.eval$chart2.control.limits.lcl
  ,center = xbar.s.eval$chart2.center.line
  ,ucl    = xbar.s.eval$chart2.control.limits.ucl
))

lims.chart.2

# Evaluate Chart for Control ----------------------------------------------
xbar.s.eval<-spc.chart.variables.mean.and.meanstandarddeviation(data = xbar.s.column$measure, sample = xbar.s.column$sample, chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

any(xbar.s.eval$chart1.is.control.violation$overall.results)
any(xbar.s.eval$chart2.is.control.violation$overall.results)

# Determine which rules were violated -------------------------------------
lapply(xbar.s.eval$chart1.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )
lapply(xbar.s.eval$chart2.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )

# Determine which points are out of control -------------------------------
lapply(xbar.s.eval$chart1.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )
lapply(xbar.s.eval$chart2.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )

# Estimate the standard deviation from the control chart ------------------
(sig.est<-unique(xbar.s.eval$chart2.center.line)/spc.constant.calculation.c4(8))

