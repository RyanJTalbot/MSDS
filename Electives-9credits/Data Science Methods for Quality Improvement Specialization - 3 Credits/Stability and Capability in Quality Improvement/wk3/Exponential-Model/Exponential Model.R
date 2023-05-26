# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# *** Known Mathematical Models ***
# *** Exponential Distribution ***
# *** Branding Agency RFP Problem ***
RFP_Response_Time <- read.csv("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 3 - X and MR charts Non Normal/RFP_Response_Time.dat", sep="")
View(RFP_Response_Time)

# Make chart first (not recommended without first testing for shape!)
spc.chart.variables.individual.and.movingrange.normal.simple(RFP_Response_Time$Time)


# Test for shape - include minimum value for Omicron
nqtr(summary.continuous(RFP_Response_Time$Time, stat.min=T),5)

# Histogram
hist.grouped(RFP_Response_Time$Time, stat.target=36, stat.usl = 48, ylim = c(0,0.12), main = "RFP Response Time", freq=F)
hist.add.distribution.curve.exp.low(x = RFP_Response_Time$Time, low = min(RFP_Response_Time$Time), freq = F)

# Test for Exponentiality
shapiro.wilk.exponentiality.test(x = RFP_Response_Time$Time)

# Generate 3 sigma chart limits for the X chart
(nt.exp.low<-ro(natural.tolerance.exp.low(x = RFP_Response_Time$Time
                                         ,low = min(RFP_Response_Time)),5))

(LNPL.exp.low<-nt.exp.low$lower.limit)
(UNPL.exp.low<-nt.exp.low$upper.limit)
formattable(nt.exp.low)


# Create chart to get control limits for the Individuals Chart
exp.low<-spc.chart.variables.individual.and.movingrange.exponential.low.simple(individuals = RFP_Response_Time$Time
                                                                               ,low = min(RFP_Response_Time))
cl<-ro(unique(data.frame(exp.low$chart1.control.limits.ucl
                         ,exp.low$chart1.center.line
                         ,exp.low$chart1.control.limits.lcl)),5)

rownames(cl)<-"Control Limits"
formattable(cl)
t(cl)
View(t(cl))


# Exponential Moving Range Chart
# Monte Carlo Simulation
# Simulation of values anticipated from a standard exponential function with an 
# Omicron of 6.76 and a mean of 15.84:
mc<-rexp.low(n = 100000, low = 6.76, mean = mean(RFP_Response_Time$Time))

# Calculate Moving Range from simulated distribution
mr.exp.low<- c(abs(diff(mc)))
mr.exp.low

# Calculate descriptive statistics
nqtr(summary.continuous(mr.exp.low, stat.min=T),5)
hist.grouped(mr.exp.low, main = "Histogram of Moving Ranges")

# Test for exponentiality
shapetest.exp.epps.pulley.1986(mr.exp.low)

# Calculate natural tolerance
(nt.mr.exp   <-ro(natural.tolerance.exp(x = mr.exp.low),5))
(LNPL.mr.exp <-nt.mr.exp$lower.limit)
(UNPL.mr.exp <-nt.mr.exp$upper.limit)
hist.grouped(mr.exp.low
             ,main = "Histogram of Moving Ranges"
             ,xlim = c(0,100)
             ,anchor.value = 0
             ,interval.size = 5
             ,stat.lsl = LNPL.mr.exp
             ,stat.lsl.label = "LNPL"
             ,stat.usl = UNPL.mr.exp
             ,stat.usl.label = "UNPL"
             ,freq = F)


# Create chart using the generic control chart
exp.low<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = RFP_Response_Time$Time
                                                                       ,chart1.control.limits.lcl = LNPL.exp.low
                                                                       ,chart1.center.line = mean(RFP_Response_Time$Time)
                                                                       ,chart1.control.limits.ucl = UNPL.exp.low
                                                                       ,chart2.control.limits.lcl = LNPL.mr.exp
                                                                       ,chart2.center.line = mean(mr.exp.low)
                                                                       ,chart2.control.limits.ucl = UNPL.mr.exp)
# Changing rules
rules            <- spc.rulesets.nelson.1984.test.1.2.3.4()

# Turn off the lower control limit rule
rules$outside.limits <- spc.controlviolation.nelson.1984.test1.outside.zone.a.upper

# If using the mean for the X chart, adjust the run rules
rules$runs       <- NULL
rules$runs.above <- spc.controlviolation.nelson.1984.test2.runs.above.create(point.count = 6)
rules$runs.below <- spc.controlviolation.nelson.1984.test2.runs.below.create(point.count = 13)




# Recreate chart
exp.chart<-spc.chart.variables.individual.and.movingrange.generic.simple(individuals = RFP_Response_Time$Time
                                                                       ,chart1.control.limits.lcl = LNPL.exp.low                                                                       ,chart1.center.line = mean(RFP_Response_Time$Time)
                                                                       ,chart1.control.limits.ucl = UNPL.exp.low
                                                                       ,chart2.control.limits.lcl = LNPL.mr.exp
                                                                       ,chart2.center.line = mean(mr.exp.low)
                                                                       ,chart2.control.limits.ucl = UNPL.mr.exp
                                                                       ,chart1.control.rules = rules)
# Test for run rules
runs.overall <- unique(exp.chart$chart1.is.control.violation$rule.results$runs.above | exp.chart$chart1.is.control.violation$rule.results$runs.below)
runs.overall
