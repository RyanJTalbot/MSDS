# Startup Code
require(lolcat)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999, digits = 10)
options(show.signif.stars=FALSE)   # Turn off * to indicate significance

# Short Term MSA ----------------------------------------------------------
Short.Term.Study.Data <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 4 MSA Continuous Part 2/Short Term Study Data.txt")
View(Short.Term.Study.Data)
st<-Short.Term.Study.Data

# Review structure of file ------------------------------------------------
str(st)

# Change Part and Operator to Factors -------------------------------------
st$Part<-factor(st$Part)
st$Operator<-factor(st$Operator
                    ,labels = c("Op 1", "Op 2", "Op 3"))


# Random Sequence Generator -----------------------------------------------
sample.int(n = 25)

# Summary - Measurement Error should be normally distributed 
# for most parts --------
norm<-ro(summary.continuous(fx = Value~Part*Operator, data = st),4)
norm<-norm[-c(4,5,6)]

norm %>%
  flextable %>%
  add_header_lines(values = "Normality Test by Part / Operator") %>%
  color(~adtest.p < 0.05, ~adtest.p, color = "red") %>%
  color(~swtest.p < 0.05, ~swtest.p, color = "red") %>%
  theme_box()

# Xbar and R Chart --------------------------------------------------------
# Split Data by Operator
Op1<-st[which(st$Operator=="Op 1"),]
Op1<-Op1[order(Op1$Part),]

Op2<-st[which(st$Operator=="Op 2"),]
Op2<-Op2[order(Op2$Part),]

Op3<-st[which(st$Operator=="Op 3"),]
Op3<-Op3[order(Op3$Part),]

# Extract data
op1.chart<-spc.chart.variables.mean.and.meanrange(data = Op1$Value
                                                  , sample = as.numeric(Op1$Part)
                                                  , combine.charts="separate"
                                                  , chart1.display=F
                                                  , chart2.display=F)


op2.chart<-spc.chart.variables.mean.and.meanrange(data = Op2$Value
                                                  , sample = as.numeric(Op1$Part)
                                                  , combine.charts="separate"
                                                  , chart1.display=F
                                                  , chart2.display=F)

op3.chart<-spc.chart.variables.mean.and.meanrange(data = Op3$Value
                                                  , sample = as.numeric(Op1$Part)
                                                  , combine.charts="separate"
                                                  , chart1.display=F
                                                  , chart2.display=F)

# Combine means and ranges
means<-c(op1.chart$parameter.means
         , op2.chart$parameter.means
         , op3.chart$parameter.means)

ranges<-c(op1.chart$parameter.ranges
          , op2.chart$parameter.ranges
          , op3.chart$parameter.ranges)

# Create combined chart
spc.cc<-spc.chart.variables.mean.and.meanrange.simple(
  means = means,
  ranges = ranges,
  sample.size = 5,
  combine.charts = "separate",
  x = c(1:25, 1:25, 1:25),
  chart1.main = "Mean Chart by Operator",
  chart1.xlab = "Part",
  chart2.main = "R Chart by Operator",
  chart2.xlab = "Part",
  chart1.line.col = "white",
  chart2.line.col = "white",
  chart1.after.plot = function() {
    abline(v = c(25.5, 50.5)
           , lty = "longdash")
    
    mtext("Operator 1", side = 3
          , at = 3)
    mtext("Operator 2", side = 3
          , at = 30)
    mtext("Operator 3", side = 3
          , at = 55)
  }
  ,
  chart2.after.plot = function() {
    abline(v = c(25.5, 50.5)
           , lty = "longdash")
    
    mtext("Operator 1", side = 3
          , at = 3)
    mtext("Operator 2", side = 3
          , at = 30)
    mtext("Operator 3", side = 3
          , at = 55)
  }
  
)

# Part Size Mean vs Variation (within each Operator) ----------------------

# Operator 1 --------------------------------------------------------------
op1.mean <- aggregate(
  x = Op1$Value,
  by = list(Op1$Part),
  FUN = mean);op1.mean

op1.sd <- aggregate(
  x = Op1$Value,
  by = list(Op1$Part),
  FUN = sd);op1.sd

op1.data<-cbind(op1.mean$x, op1.sd$x)
op1.data<-as.data.frame(op1.data)
names(op1.data)<-c("Mean", "Std_Dev")
op1.data

# Pearson Product Moment Correlation Coefficient
(r.op1 <- round(cor(x = op1.data$Mean
                    , y = op1.data$Std_Dev), 3))

# Scatterplot of Mean vs Standard deviation
plot(
  x = op1.data$Mean,
  y = op1.data$Std_Dev,
  pch = 19,
  xlab = "Mean",
  ylab = "Standard Deviation",
  main = "Correlation of Mean and Std. Dev.")
abline(lm(Std_Dev ~ Mean, data = op1.data), col = "blue")
mtext(bquote(paste("r =", .(r.op1), side = 3)))

# Test to see if r is different from zero
cor.pearson.r.onesample(x = op1.data$Mean
                       ,y = op1.data$Std_Dev)


# Operator 2 --------------------------------------------------------------
op2.mean <- aggregate(
  x = Op2$Value,
  by = list(Op2$Part),
  FUN = mean);op2.mean

op2.sd <- aggregate(
  x = Op2$Value,
  by = list(Op2$Part),
  FUN = sd);op2.sd

op2.data<-cbind(op2.mean$x, op2.sd$x)
op2.data<-as.data.frame(op2.data)
names(op2.data)<-c("Mean", "Std_Dev")
op2.data

# Pearson Product Moment Correlation Coefficient
(r.op2<-round(cor(x = op2.data$Mean
                 ,y = op2.data$Std_Dev),3))

# Scatterplot of Mean vs Standard deviation
plot(
  x = op2.data$Mean,
  y = op2.data$Std_Dev,
  pch = 19,
  xlab = "Mean",
  ylab = "Standard Deviation",
  main = "Correlation of Mean and Std. Dev.")
abline(lm(Std_Dev ~ Mean, data = op2.data), col = "blue")
mtext(bquote(paste("r =", .(r.op2), side = 3)))

# See if r is significantly different than zero
cor.pearson.r.onesample(x = op2.data$Mean
                       ,y = op2.data$Std_Dev)

# Operator 3
op3.mean <- aggregate(
  x = Op3$Value,
  by = list(Op3$Part),
  FUN = mean);op3.mean
  
op3.sd <- aggregate(
  x = Op3$Value,
  by = list(Op3$Part),
  FUN = sd);op3.sd

op3.data<-cbind(op3.mean$x, op3.sd$x)
op3.data<-as.data.frame(op3.data)
names(op3.data)<-c("Mean", "Std_Dev")
op3.data

# Pearson Product Moment Correlation Coefficient
(r.op3<-round(cor(x = op3.data$Mean
                 ,y = op3.data$Std_Dev),3))

# Scatterplot of Mean vs Standard deviation
plot(
  x = op3.data$Mean,
  y = op3.data$Std_Dev,
  pch = 19,
  xlab = "Mean",
  ylab = "Standard Deviation",
  main = "Correlation of Mean and Std. Dev.")
abline(lm(Std_Dev ~ Mean, data = op3.data), col = "blue")
mtext(bquote(paste("r =", .(r.op3), side = 3)))

# See if r is significantly different than zero
cor.pearson.r.onesample(x = op3.data$Mean
                       ,y = op3.data$Std_Dev)

# Short Term MSA ANOVA ----------------------------------------------------
st.out <-ro(
    msa.continuous.repeatability.reproducibility(
      measurement = st$Value,
      part        = st$Part,
      appraiser   = st$Operator,
      stat.lsl    = 180,
      stat.usl    = 220),5)

(anova.st.out <- data.frame(st.out$summary.aov.full[[1]]))

# Add rownames to ANOVA Table
anova.st.out$Source<-rownames(anova.st.out)
anova.st.out<-anova.st.out[c(6,1,2,3,4,5)]

# ANOVA Source Table ------------------------------------------------------
anova.st.out %>%
  flextable() %>%
  add_header_lines(values = "ANOVA Source Table") %>%
  colformat_double(j=c('Sum.Sq','Mean.Sq', 'F.value', 'Pr..F.'), digits=4, na_str = '') %>%
  theme_box()

# Components of Variance --------------------------------------------------
comp.st.var<-data.frame(st.out$ev.full)
comp.var.st.out<-comp.st.var[1:2]

# Add rownames to Variance Component Table
comp.var.st.out$Source<-rownames(comp.var.st.out)
comp.var.st.out<-comp.var.st.out[c(3,1,2)]

comp.var.st.out %>%
  flextable() %>%
  add_header_lines(values = "Components of Variance") %>%
  colformat_double(j=c('Component'), digits=4) %>%
  theme_box

# Study Variation ---------------------------------------------------------
study.st.var<-data.frame(st.out$ev.full)
study.var.st.out<-study.st.var[3:6]

# Add rownames to Study Variation Table
study.var.st.out$Source<-rownames(study.var.st.out)
study.var.st.out<-study.var.st.out[c(5,1,2,3,4)]

study.var.st.out %>%
  flextable() %>%
  add_header_lines(values = "Study Variability") %>%
  colformat_double(j=c('StdDev','StudyVar'), digits=4) %>%
  theme_box

# Number of distinct categories (NDC) -------------------------------------
# Should be greater than 5
st.out$ev.reduced.number.distinct.categories

# Discrimination Ratio
st.out$ev.reduced.discrimination.ratio

# Data Visualization ------------------------------------------------------
# Barplot - Components of Variance ----------------------------------------

# Subset data for barplot
bp.compvar<-comp.var.st.out[c(1:3,6),]

barplot(height = bp.compvar$Pct_Cont
        , names.arg = c("GR&R", "Repeat", "Reprod","Part")
        , main = "Components of Variation"
        , ylab = "Percent Contribution"
        , col = "light blue")

abline(h=0)
abline(h=9, lty=2)

# Boxplot - Value by Operator ---------------------------------------------
boxplot(Value ~ Operator,
        data = st,
        col = "red",
        main = "Value by Operator")

# Boxplot - Value by Part -------------------------------------------------
boxplot(Value ~ Part,
        data = st,
        col = "goldenrod",
        main = "Value by Part")

# Line / Point Chart - Value by Part --------------------------------------
lc <-aggregate(st$Value
               ,by = list(as.numeric(st$Part))
               ,FUN = mean)

spc.run.chart(
  x = lc$x,
  type = "p",
  main = "Value by Part",
  xlab = "Part",
  ylab = "Value"
)

points(
  x   = st$Part,
  y   = st$Value,
  pch = 19,
  col = " grey",
  cex = 0.6,
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
     ylim = c(min(op1.chart$parameter.means, op2.chart$parameter.means,op3.chart$parameter.means),
              max(op1.chart$parameter.means, op2.chart$parameter.means,op3.chart$parameter.means)
     )
)
lines(
  op2.chart$parameter.means,
  type = "o",
  pch = 19,
  col = "blue",
  lty = 2
)

lines(
  op3.chart$parameter.means,
  type = "o",
  pch = 19,
  col = "forest green",
  lty = 2
)
legend("bottomright",inset = c(0, 1),
       xpd = TRUE,
       legend = c("Op 1", "Op 2","Op 3"),
       col = c("red", "blue","forest green"),
       horiz = T,
       lty = 1:2,
       cex = 0.8,
       bty = "n"
)
