require(lolcat)

# Import File
Rules <- read.delim("G:/My Drive/EMEN 5042/Lecture Powerpoint and Pdf/Lecture 3 - Process Control and Control Charts/Rules.txt")
View(Rules)

# Rule 1 - Outside Limits
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$OOC, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9)

# Rule 2 - Run Above or Below the Mean
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Run, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9)

# Change Run Rule to 8 points instead of 9
rules <- spc.rulesets.nelson.1984.test.1.2.3.4()
rules$runs <- spc.controlviolation.nelson.1984.test2.runs.create(
  point.count = 8
)

# Make new chart specifying rules
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Run, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9, chart1.control.rules = rules)

# Rule 3 - Trends 
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Trend, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9)

# Rule 4 - Alternating
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Alternate, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9)

# Rule 5 - 2 of 3
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$X2of3, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9, chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

# Rule 6 - 4 of 5
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$X4of5, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9, chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

# Rule 7 - Lack of Variability
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Lackofvar, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9, chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

# Rule 8 - Mixture
spc.chart.variables.individual.and.movingrange.normal.simple(Rules$Mixture, chart1.center.line = 12, chart1.control.limits.ucl = 15, chart1.control.limits.lcl = 9, chart1.control.rules = spc.rulesets.nelson.1984.test.1.2.3.4.5.6.7.8())

