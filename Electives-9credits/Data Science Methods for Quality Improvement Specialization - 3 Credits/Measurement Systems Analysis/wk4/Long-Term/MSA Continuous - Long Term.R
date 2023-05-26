# Startup Code
require(lolcat)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999, digits = 10)
options(show.signif.stars=FALSE)   # Turn off * to indicate significance

# Long Term MSA -----------------------------------------------------------
Longterm.MSA <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 4 MSA Continuous Part 2/Longterm MSA.txt")
View(Longterm.MSA)
lt<-Longterm.MSA

# Review structure of file ------------------------------------------------
str(lt)

# Change Part and Operator to Factors -------------------------------------
lt$Part<-factor(lt$Part)
lt$Operator<-rep(1, each=200)
lt$Operator<-factor(lt$Operator
                    ,labels = "Operator 1")


# Summary - Measurement Error should be normally distributed 
# for most parts --------
norm <- ro(summary.continuous(fx = Value ~ Part, data = lt), 4)
norm<-norm[-c(3,4,5)]

norm %>%
  flextable %>%
  add_header_lines(values = "Normality Test by Part") %>%
  color(~g3test.p < 0.05, ~g3test.p, color = "red") %>%
  color(~g4test.p < 0.05, ~g4test.p, color = "red") %>%
  theme_box()

# Control Charts by Part --------------------------------------------------
rules<-spc.rulesets.nelson.1984.test.1.2.3.4()
rules$alternating<-NULL

par(mfrow=c(2,2))

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 1],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 1",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 2],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 2",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 3],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 3",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 4],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 4",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 5],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 5",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 6],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 6",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 7],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 7",
  chart2.display = F)

spc.chart.variables.individual.and.movingrange.generic.simple(
  individuals = lt$Value[lt$Part == 8],
  combine.charts = "leave.par.alone",
  chart1.control.rules = rules,
  chart1.ylab = "Voltage",
  chart1.main = "Part 8",
  chart2.display = F)

graphics.off()

# Calculate Mean and Standard Deviations by Repetition ----------------------------------
(lt.mean<-aggregate(lt$Value, by = list(lt$Rep), FUN=mean))
(lt.sd<-aggregate(lt$Value, by = list(lt$Rep), FUN=sd))

# Create Data Frame
lt.data<-cbind(lt.mean$x, lt.sd$x)
lt.data<-as.data.frame(lt.data)
names(lt.data)<-c("Mean", "Std_Dev")

# Individuals Chart for Standard Deviation --------------------------------
spc.chart.variables.individual.and.movingrange.normal.simple(
  individuals = lt.data$Std_Dev,
  chart2.display = F,
  chart1.main = "Individual Chart for Std. Dev.")

# Individuals Chart for Means ---------------------------------------------
spc.chart.variables.individual.and.movingrange.normal.simple(
  individuals = lt.data$Mean,
  chart2.display =  F,
  chart1.main = "Individual Chart for Means")

# Part Size Mean vs Variation ----------------------
(lt.part.mean <-aggregate(
     x = lt$Value,
     by = list(lt$Part),
     FUN = mean
   ))

(lt.part.sd <- aggregate(
  x = lt$Value,
  by = list(lt$Part),
  FUN = sd
))

lt.data.part<-cbind(lt.part.mean$x, lt.part.sd$x)
lt.data.part<-as.data.frame(lt.data.part)
names(lt.data.part)<-c("Mean", "Std_Dev")
View(lt.data.part)


# Pearson Product Moment Correlation Coefficient --------------------------
(r.lt <- ro(cor(x = lt.data.part$Mean
              , y = lt.data.part$Std_Dev), 3))


# Scatterplot of Mean vs Standard Deviation of Parts ----------------------
graphics.off()
plot(
  x = lt.data.part$Mean,
  y = lt.data.part$Std_Dev,
  pch = 19,
  xlab = "Mean",
  ylab = "Standard Deviation",
  main = "Correlation of Mean and Std. Dev."
)
abline(lm(Std_Dev ~ Mean, data = lt.data.part), col = "blue")
mtext(bquote(paste("r =", .(r.lt), side = 3)))

# See if r is significantly different than zero
cor.pearson.r.onesample(x = lt.data.part$Mean
                      , y = lt.data.part$Std_Dev)



# Long Term MSA ANOVA ----------------------------------------------------
lt.out <-
  ro(msa.continuous.repeatability.reproducibility(
      measurement = lt$Value,
      part = lt$Part,
      appraiser = lt$Operator,
      stat.lsl = 1.3116,
      stat.usl = 1.5084),5)

(anova.lt.out<-data.frame(lt.out$summary.aov.full[[1]]))

# Add rownames to ANOVA Table
anova.lt.out$Source<-c("Part", "Repeatability", "Total")
anova.lt.out<-anova.lt.out[c(6,1,2,3,4,5)]

# ANOVA Source Table ------------------------------------------------------
anova.lt.out %>%
  flextable() %>%
  add_header_lines(values = "ANOVA Source Table") %>%
  colformat_double(j=c('Sum.Sq','Mean.Sq', 'F.value', 'Pr..F.'), digits=4, na_str = '') %>%
  theme_box()


# Components of Variance --------------------------------------------------
comp.lt.var<-data.frame(lt.out$ev.full)
comp.var.lt.out<-comp.lt.var[1:2]

# Add rownames to Variance Component Table
comp.var.lt.out$Source<-rownames(comp.var.lt.out)
comp.var.lt.out<-comp.var.lt.out[c(3,1,2)]

comp.var.lt.out %>%
  flextable() %>%
  add_header_lines(values = "Components of Variance") %>%
  colformat_double(j=c('Component'), digits=4) %>%
  theme_box

# Study Variation ---------------------------------------------------------
study.lt.var<-data.frame(lt.out$ev.full)
study.var.lt.out<-study.lt.var[3:6]

# Add rownames to Study Variation Table
study.var.lt.out$Source<-rownames(study.var.lt.out)
study.var.lt.out<-study.var.lt.out[c(5,1,2,3,4)]

study.var.lt.out %>%
  flextable() %>%
  add_header_lines(values = "Study Variability") %>%
  colformat_double(j=c('StdDev','StudyVar'), digits=4) %>%
  theme_box

# Number of distinct categories (NDC) -------------------------------------
# Should be greater than 5
lt.out$ev.reduced.number.distinct.categories

# Discrimination Ratio
lt.out$ev.reduced.discrimination.ratio


# Data Visualization ------------------------------------------------------
# Barplot - Components of Variance ----------------------------------------

# Subset data for barplot
bp.compvar<-comp.var.lt.out[c(1:3,6),]

barplot(height = bp.compvar$Pct_Cont
        , names.arg = c("GR&R", "Repeat", "Reprod","Part")
        , main = "Components of Variation"
        , ylab = "Percent Contribution"
        , col = "light blue")

abline(h=0)
abline(h=9, lty=2)

# Boxplot - Value by Part -------------------------------------------------
boxplot(Value ~ Part,
        data = lt,
        col = "goldenrod",
        main = "Value by Part")

