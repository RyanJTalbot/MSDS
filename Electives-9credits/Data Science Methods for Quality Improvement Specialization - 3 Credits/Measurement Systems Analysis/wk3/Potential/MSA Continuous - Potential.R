# Startup Code
require(lolcat)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999, digits = 10)
options(show.signif.stars=FALSE)   # Turn off * to indicate significance

# Potential Study (Gauge R&R) ---------------------------------------------
potential <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 3 MSA Continuous Part 1/potential.dat")
View(potential)

# Potential Study: ANOVA Method -------------------------------------------
# Review structure of file
str(potential)

# Change Part and Operator to Factors
potential$Repetition<-factor(potential$Repetition)
potential$Part<-factor(potential$Part)
potential$Operator<-factor(potential$Operator
                           ,labels = c("Operator 1", "Operator 2"))

(pot.out<-ro(msa.continuous.repeatability.reproducibility(measurement = potential$Value
                                                      ,part = potential$Part
                                                      ,appraiser = potential$Operator
                                                      ,stat.lsl = 67
                                                      ,stat.usl = 76),5))
(anova.out<-data.frame(pot.out$summary.aov.full[[1]]))

# Add rownames to ANOVA Table
anova.out$Source<-rownames(anova.out)
anova.out<-anova.out[c(6,1,2,3,4,5)]

# ANOVA Source Table ------------------------------------------------------
anova.out %>%
  flextable() %>%
  add_header_lines(values = "ANOVA Source Table") %>%
  colformat_double(j=c('Sum.Sq','Mean.Sq', 'F.value', 'Pr..F.'), digits=4, na_str = '') %>%
  theme_box()

# Components of Variance --------------------------------------------------
# Expected Mean Squares
require(EMSaov)
(anova.result<-EMSanova(formula = Value~Operator*Part, data = potential, type = c("R", "R")))
anova.result$EMS

(comp.var<-data.frame(pot.out$ev.full))
comp.var.out<-comp.var[1:2]

# Add rownames to Variance Component Table
comp.var.out$Source<-rownames(comp.var.out)
comp.var.out<-comp.var.out[c(3,1,2)]

comp.var.out %>%
  flextable() %>%
  add_header_lines(values = "Components of Variance") %>%
  colformat_double(j=c('Component'), digits=4) %>%
  theme_box

# Study Variation ---------------------------------------------------------
study.var<-data.frame(pot.out$ev.full)
(study.var.out<-study.var[3:6])

# Add rownames to Study Variation Table
study.var.out$Source<-rownames(study.var.out)
study.var.out<-study.var.out[c(5,1,2,3,4)]

study.var.out %>%
  flextable() %>%
  add_header_lines(values = "Study Variability") %>%
  colformat_double(j=c('StdDev','StudyVar'), digits=4) %>%
  theme_box

# Number of distinct categories (NDC) -------------------------------------
# Should be greater than 5
pot.out$ev.reduced.number.distinct.categories

# Discrimination Ratio
pot.out$ev.reduced.discrimination.ratio

# Data Visualization ------------------------------------------------------

# Barplot - Components of Variance ----------------------------------------

# Subset data for barplot
bp.compvar<-comp.var.out[c(1:3,6),]

barplot(height = bp.compvar$Pct_Cont
        , names.arg = c("GR&R", "Repeat", "Reprod","Part")
        , main = "Components of Variation"
        , ylab = "Percent Contribution"
        , col = "light blue")
        
abline(h=0)
abline(h=9, lty=2)

# Xbar and R Chart --------------------------------------------------------
# Split Data by Operator
Op1<-potential[which(potential$Operator=="Operator 1"),]
Op1<-Op1[order(Op1$Part),]

Op2<-potential[which(potential$Operator=="Operator 2"),]
Op2<-Op2[order(Op2$Part),]

# Extract data
op1.chart <- spc.chart.variables.mean.and.meanrange(
  data = Op1$Value,
  sample = as.numeric(Op1$Part),
  combine.charts = "separate",
  chart1.display = F,
  chart2.display = F)

op2.chart <- spc.chart.variables.mean.and.meanrange(
  data = Op2$Value,
  sample = as.numeric(Op2$Part),
  combine.charts = "separate",
  chart1.display = F,
  chart2.display = F)

# Combine means and ranges
means<-c(op1.chart$parameter.means
         ,op2.chart$parameter.means)

ranges<-c(op1.chart$parameter.ranges
          ,op2.chart$parameter.ranges)

# Create combined chart
spc.chart.variables.mean.and.meanrange.simple(
  means = means,
  ranges = ranges,
  sample.size = 2,
  combine.charts = "separate",
  x = c(1:10, 1:10),
  chart1.main = "Mean Chart by Operator",
  chart1.xlab = "Part",
  chart2.main = "R Chart by Operator",
  chart2.xlab = "Part",
  chart1.line.col = "white",
  chart2.line.col = "white",
  chart1.after.plot = function() {
    abline(v = 10.5
           , lty = "longdash")
    
    mtext("Operator 1", side = 3
          , at = 3)
    mtext("Operator 2", side = 3
          , at = 13)
  }
  ,
  chart2.after.plot = function() {
    abline(v = 10.5
           , lty = "longdash")
    
    mtext("Operator 1", side = 3
          , at = 3)
    mtext("Operator 2", side = 3
          , at = 13)
  }
  
)

# Boxplot - Value by Operator ---------------------------------------------
boxplot(Value ~ Operator,
        data = potential,
        col = "red",
        main = "Value by Operator")

# Boxplot - Value by Part -------------------------------------------------
boxplot(Value ~ Part,
        data = potential,
        col = "goldenrod",
        main = "Value by Part")

# Line / Point Chart - Value by Part --------------------------------------
lc <-aggregate(potential$Value
               ,by = list(as.numeric(potential$Part))
               ,FUN = mean)

spc.run.chart(
  x = lc$x,
  type = "p",
  main = "Value by Part",
  xlab = "Part",
  ylab = "Value"
)
points(
  x    = potential$Part,
  y   = potential$Value,
  pch = 19,
  col = " grey",
  cex = 0.8,
  bty = "n"
)

# Part Operator Interaction -----------------------------------------------
plot(op1.chart$parameter.means,
  type = "o",
  pch = 19,
  col = "red",
  xlab = "Part",
  ylab = "Value"  ,
  main = "Part - Operator Interaction",
  ylim = c(min(op1.chart$parameter.means, op2.chart$parameter.means),
    max(op1.chart$parameter.means, op2.chart$parameter.means)
  )
)
lines(
  op2.chart$parameter.means,
  type = "o",
  pch = 19,
  col = "blue",
  lty = 2
)
legend("bottomright",inset = c(0, 1),
  xpd = TRUE,
  legend = c("Op 1", "Op 2"),
  col = c("red", "blue"),
  horiz = T,
  lty = 1:2,
  cex = 0.8,
  bty = "n"
)
