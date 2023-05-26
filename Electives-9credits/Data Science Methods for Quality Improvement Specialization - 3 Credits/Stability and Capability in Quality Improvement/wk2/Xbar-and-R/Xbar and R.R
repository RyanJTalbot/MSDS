# Startup Code
require(lolcat)

# **** Xbar and R Charts ****

# Import Data -------------------------------------------------------------
xbar.r <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 2 -  Xbar and R S charts X and MR charts/xbar-r.dat")
View(xbar.r)

# Drop first 2 columns
xbar.r <- xbar.r[-c(1:2)]

# Transpose Data ----------------------------------------------------------
xbar.r.new<-transform.dependent.format.to.independent.format(data = xbar.r)
View(xbar.r.new)

# Create a sample column
xbar.r.new$sample<-rep(1:26) 

# Drop the Cell column
xbar.r.new<-xbar.r.new[-1]

# Sort by sample
xbar.r.column<-xbar.r.new[order(xbar.r.new$sample),]
View(xbar.r.column)

# Create the X Bar and R Chart --------------------------------------------
spc.chart.variables.mean.and.meanrange(data = xbar.r.column$measure
                                       ,sample = xbar.r.column$sample
                                       ,chart1.main="Xbar Chart"
                                       ,chart2.main="R Chart")

# Extract Control Limits and Centerline for each chart --------------------
xbar.r.eval<-spc.chart.variables.mean.and.meanrange(data = xbar.r.column$measure
                                                    ,sample = xbar.r.column$sample)

lims.chart.1 <- unique(data.frame(
  lcl     = xbar.r.eval$chart1.control.limits.lcl
  ,center = xbar.r.eval$chart1.center.line
  ,ucl    = xbar.r.eval$chart1.control.limits.ucl
))

lims.chart.1

lims.chart.2 <- unique(data.frame(
  lcl     = xbar.r.eval$chart2.control.limits.lcl
  ,center = xbar.r.eval$chart2.center.line
  ,ucl    = xbar.r.eval$chart2.control.limits.ucl
))

lims.chart.2

# Evaluate Chart for Control ----------------------------------------------
xbar.r.eval<-spc.chart.variables.mean.and.meanrange(data = xbar.r.column$measure
                                                    ,sample = xbar.r.column$sample
                                                    ,chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8()
                                                    ,chart2.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4())
                                                    

any(xbar.r.eval$chart1.is.control.violation$overall.results)
any(xbar.r.eval$chart2.is.control.violation$overall.results)

# Determine which rules were violated -------------------------------------
lapply(xbar.r.eval$chart1.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )
lapply(xbar.r.eval$chart2.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )

# Determine which points are out of control -------------------------------
lapply(xbar.r.eval$chart1.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )
lapply(xbar.r.eval$chart2.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )

# Estimate the standard deviation from the control chart ------------------
(sig.est<-unique(xbar.r.eval$chart2.center.line)/spc.constant.calculation.d2(5))
