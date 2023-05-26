# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# u Chart -----------------------------------------------------------------
u.Chart <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 5 - Control Charts for Discrete Data/u Chart.dat")
View(u.Chart)


# Centerline Calculation ------------------------------------------------
sum(u.Chart$Count)/sum(u.Chart$Boxes)



# Create Control Chart ----------------------------------------------------
spc.u.chart<-spc.chart.attributes.counts.u.poissondistribution.simple(rates = u.Chart$Count/u.Chart$Boxes
                                                                      ,sample.size = u.Chart$Boxes
                                                                      ,chart1.point.cex = 1.3
                                                                      ,chart1.line.lwd=2
                                                                      ,chart1.main = "u chart - # Defects per Box")

# Centerline
(u.center<-unique(spc.u.chart$chart1.center.line))


# Control Limits ----------------------------------------------------------
# Control limits for point 1 - Example
ro(table.dist.poisson(lambda = u.center * 6)[1:24,],4)

# Control Limits for Chart
(ucl.u<-spc.u.chart$chart1.control.limits.ucl)
(lcl.u<-spc.u.chart$chart1.control.limits.lcl)



# Evaluate Chart for Control ----------------------------------------------
any(spc.u.chart$chart1.is.control.violation$overall.results)



# Determine which rules were violated -------------------------------------
lapply(spc.u.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )



# Determine which points --------------------------------------------------
lapply(spc.u.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )

