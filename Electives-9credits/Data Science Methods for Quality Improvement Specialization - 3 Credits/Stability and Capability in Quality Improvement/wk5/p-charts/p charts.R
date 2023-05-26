# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)


# p Chart -----------------------------------------------------------------
p.Chart <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 5 - Control Charts for Discrete Data/p Chart.dat")
View(p.Chart)


# Create proportions column -----------------------------------------------
p.Chart$prop<-p.Chart$count/p.Chart$n

# Average proportion (centerline) -----------------------------------------
mean(p.Chart$prop)

# Exact Binomial Limits ---------------------------------------------------
ro(table.dist.binomial(n = 200, p = 0.031),4)[1:20,]


# Create p chart ----------------------------------------------------------
spc.p.chart<-spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.Chart$prop, sample.size = p.Chart$n)

# Make points bigger and line thicker (optional)
spc.p.chart<-spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.Chart$prop
                                                                           ,sample.size = p.Chart$n
                                                                           ,chart1.point.cex = 1.3
                                                                           ,chart1.line.lwd = 2
                                                                           ,chart1.main = "p chart - Proportion of Defective Coils")


# Control Limits and Centerline -------------------------------------------
(p.UCL<-unique(spc.p.chart$chart1.control.limits.ucl))
(p.center<-unique(spc.p.chart$chart1.center.line))
(p.LCL<-unique(spc.p.chart$chart1.control.limits.lcl))

climits<-as.data.frame(c(p.UCL, p.center, p.LCL))
names(climits)<-"Limits"
rownames(climits)<-c("UCL", "Center", "LCL")
formattable(climits)


# Evaluate Chart for Control ----------------------------------------------
any(spc.p.chart$chart1.is.control.violation$overall.results)


# Determine which rules were violated -------------------------------------
lapply(spc.p.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { any(v) } )



# Determine which points  -------------------------------------------------
lapply(spc.p.chart$chart1.is.control.violation$rule.results
       ,FUN = function(v) { which(v) } )


# Split data by Set -------------------------------------------------------
p.set1<-subset(x = p.Chart, subset = p.Chart$Set==1)
p.set2<-subset(x = p.Chart, subset = p.Chart$Set==2)


# Proportion Chart by Set -------------------------------------------------
spc.p.set1<-spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.set1$prop, sample.size = p.set1$n, chart1.main = "p Chart Before")
spc.p.set2<-spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.set2$prop, sample.size = p.set2$n, chart1.main = "p Chart After")


# Chart both side by side -------------------------------------------------
par(mfrow=c(1,2))
spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.set1$prop, sample.size = p.set1$n, chart1.ylim=c(0,0.12), combine.charts="leave.par.alone", chart1.main = "p Chart - Set 1")
spc.chart.attributes.proportion.p.binomialdistribution.simple(proportions = p.set2$prop, sample.size = p.set2$n, chart1.ylim=c(0,0.12), combine.charts="leave.par.alone", chart1.main = "p Chart - Set 2")


# Pull out control limit information --------------------------------------
(set1.ucl<-unique(spc.p.set1$chart1.control.limits.ucl))
(set1.center<-unique(spc.p.set1$chart1.center.line))
(set1.lcl<-unique(spc.p.set1$chart1.control.limits.lcl))

(set2.ucl<-unique(spc.p.set2$chart1.control.limits.ucl))
(set2.center<-unique(spc.p.set2$chart1.center.line))
(set2.lcl<-unique(spc.p.set2$chart1.control.limits.lcl))


# Has anything changed between set 1 and set 2? ---------------------------
proportion.test.twosample.exact.simple(sample.proportion.g1 = set1.center
                                       ,sample.size.g1 = 200
                                       ,sample.proportion.g2 = set2.center
                                       ,sample.size.g2 = 200
                                       ,alternative = "two.sided")



# Capability --------------------------------------------------------------

# Get average proportion defective
set2.center

# Convert to Z Score
(Z<-qnorm(p = 0.0171875, lower.tail = F))

# Convert Z to Cpk_eq
(Cpk.eq<-Z/3)

