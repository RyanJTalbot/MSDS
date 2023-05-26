# Startup Code ------------------------------------------------------------
require(lolcat)          
require(car)
require(dplyr)
require(sjstats)
require(flextable)
options(scipen=99,digits = 10)
options(show.signif.stars=FALSE)   # Turn off * to indicate significance
nqtr <- function(x,d){noquote(t(round.object(x, d)))}
ro <- round.object

# Import Data File --------------------------------------------------------
Solder <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 One Way ANOVA/Solder.dat")
View(Solder)
str(Solder)

# Specify Factors with labels -------------------------------------------
group.labels<-c("New1","New2","New3","Current")
Solder$method<-factor(Solder$method, labels = group.labels)
str(Solder)

# Descriptive Summary -----------------------------------------------------
(so <- ro(summary.continuous(push ~ method, Solder, stat.miss=F),4))
boxplot(push ~ method,data=Solder, 
        xlab="Soldering Method", 
        ylab="Criterion Measure Means", 
        main="Push Force Means By Soldering Method", 
        col="red")
so %>%
  flextable() %>%
  add_header_lines(values = "Descriptive Summary") %>%
  theme_box()

# Critical F for J-1 = 3, J(n-1) = 20 df, with alpha = 0.05
qf(p = 0.05, df1 = 3, df2 = 20, lower.tail = FALSE) # Reject if F > than this value

curve(df(x, df1=3, df2=20), from=0, to=7, xlab = "F", ylab="Density")
abline(v=qf(p = 0.05, df1 = 3, df2 = 20, lower.tail = FALSE),) 
text(x=5.1, y=0.4, "Critical Value of F")

# ANOVA Syntax ------------------------------------------------------------
solder.aov<-aov(formula = push~method, data = Solder)
(sourcetable.aov <- summary(solder.aov))  # Display and Save the ANOVA (Summary) Source Table 
View(sourcetable.aov)

# Add Totals to ANOVA Table
(anova.temp<-sourcetable.aov[[1]])
totaldf<-sum(anova.temp$Df)
totalss<-sum(anova.temp$`Sum Sq`)
total<-data.frame(totaldf, totalss,"","","")
names(total)<-c("Df","Sum Sq","Mean Sq","F value","Pr(>F)")
(anova.out<-rbind(anova.temp,as.numeric(total)))
rownames(anova.out)<-c("Method","Residuals","Total")
anova.out$Source<-rownames(anova.out)
anova.out<-anova.out[c(6,1,2,3,4,5)]

# ANOVA Source Table ------------------------------------------------------
anova.out %>%
  flextable() %>%
  add_header_lines(values = "ANOVA Source Table") %>%
  colformat_double(j=c('Sum Sq','Mean Sq', 'F value', 'Pr(>F)'), digits=4, na_str = '') %>%
  theme_box()
  

# Welch's ANOVA  ----------------------------------------------------------
#Use Welch ANOVA when there are unequal variances (From Dispersion analysis) 
# Does Welch by Default, Use "var.equal=TRUE" for equal var
(welch.out <- oneway.test(push ~ method, data = Solder))


# Statistical Importance --------------------------------------------------
# Define the Anova model
model<-lm(formula = push~method, data = Solder)
anova.stats<-anova_stats(model, digits = 4) #sjstats package
anova.stats$omegasq[1]


# Importance calculation using Welch ANOVA   
# View the structure to identify where to get 
# values for importance 
str(welch.out) 
(nTot <- nrow(Solder))  
(wF <- as.numeric(welch.out$statistic))    # The Welch F statistic
(dfEff<-as.numeric(welch.out$parameter[1]))# The degrees of freedom

(Imp.Welch <- (dfEff*(wF-1))/(dfEff*(wF-1)+nTot)) * 100 

# Post Hoc Analysis Prep -------------------------------------------------------

# After Significance is found ALWAYS do the following Preparation for Post Hoc analysis. 
# After Importance,  ALWAYS provide:  
# 1. Means Plot and 2. Table of Means (Both needed following a significant effect)

# Compute and save factor level n, means and variances  
(mean.var <- ro(summary.impl(fx = push ~ method, 
                             data = Solder, 
                             stat.n = TRUE,
                             stat.mean = TRUE, 
                             stat.var = TRUE),4))

# 1. Plot cell means and label the plot   
plot(mean.var$mean, xaxt="n", type = "o", 
     lty = 1, pch = 19, cex = 1.3, lwd= 1.7
     ,col="blue", xlab = "Method", 
     ylab = "Mean Push Force", main = "Push by Method")
axis(1, at=1:4, labels=group.labels)    # Add the axis labels

# 2. Table of cell n, means, and variances
mean.var %>%
  flextable() %>%
  add_header_lines(values = "Mean / Variance by Method") %>%
  theme_box()


# Calculating Dispersion ----------------------------------------------------
# Absolute Deviation from the Average (ADA)
Solder$ADA<-compute.group.dispersion.ADA(fx = push~method
                                         ,data = Solder)

# Absolute Deviation from the Median (ADM)
Solder$ADM<-compute.group.dispersion.ADM(fx = push~method
                                         ,data = Solder)

# Absolute Deviation from the Median, n-1 (ADMn1)
Solder$ADMn1<-compute.group.dispersion.ADMn1(fx = push~method
                                         ,data = Solder)

View(Solder)

# Note that since the results of the dispersion.ADMn1()
# function is a vector with one missing value due to 
# the discarded value, you must use the na.rm=TRUE 
# argument when you operate on the ADMn1 dispersion 
# values.

# ANOVA for Dispersion - ADA ----------------------------------------------
solderADA.aov<-aov(formula = ADA~method, data = Solder)
(sourcetableADA.aov <- summary(solderADA.aov))

# ANOVA for Dispersion - ADmn1 ----------------------------------------------
solderADMn1.aov<-aov(formula = ADMn1~method, data = Solder)
(sourcetableADAMn1.aov <- summary(solderADMn1.aov))

# 1. Table of ADA means by group
(ada.means.var <- summary.impl(fx = ADA ~ method, 
                                 data = Solder, 
                                 stat.n = TRUE,
                                 stat.mean = TRUE, 
                                 stat.var = TRUE))

# Table of Means and Variance of ADA
ADA.means.var %>%
  flextable() %>%
  add_header_lines(values = "ADA Mean / Variance by Method") %>%
  theme_box()
  
# 2. Line plot 
plot(ada.means.var$mean, xaxt="n", type = "o", lty = 1, pch = 19 
     , cex = 1.3, lwd= 1.7, col="blue" 
     , xlab = "Soldering Method" , ylab = "Mean ADA Values"
     , main = "Mean ADA by Method")
axis(1, at=1:4, labels=group.labels)

# Post Hoc Analysis for Means ---------------------------------------------

# Tukey HSD for Equal Variances -------------------------------------------
solder.aov<-aov(formula = push~method, data = Solder)
(tukey.out<-ro(TukeyHSD(solder.aov),4))
plot(tukey.out, las=2, cex.axis=0.5)

# Tukey HSD in lolcat -----------------------------------------------------
# To conduct the post hoc analysis, pull the
# following from the ANOVA source table
(anova.out<-sourcetable.aov[[1]])
  # Mean Square of the Error Term
  (MSE<-anova.out$`Mean Sq`[2])
  # Degrees of Freedom of the Error Term
  (dfe<-anova.out$Df[2])
  # Group / Factor level labels
  (so <- summary.continuous(fx = push ~ method, data = Solder))
  so$method
  # Sample Size (n)
  so$n
  # Means by Group / Factor level
  so$mean

tuk.out <- contrasts.tukey.kgroups.simple(group.label = so$method
, group.mean = so$mean
, group.sample.size = so$n
, conf.level.familywise = .95
, n.means = 4
, mean.squared.error = MSE
, df.mean.squared.error = dfe)

round.object(tuk.out$matrix.p.value)
tuk.out$matrix.decision

# Games & Howell for Unequal Variances -------------------------------------------

# This is the correct analysis of the Solder means because there are unequal 
# variances in the groups. The function call is very similar to that of Tukey 
# from above. Since we saved the summary output we have all of the elements
# that we need to do the tests, as you see next:  

str(so)
so                      

# Games and Howell {lolcat}  
gh.out <- contrasts.games.howell.kgroups.simple(group.label = so$method
                                                , group.mean = so$mean
                                                , group.variance = so$var
                                                , group.sample.size = so$n)

str(gh.out)
gh.pvals<-data.frame(ro(gh.out$matrix.p.value,4))
gh.pvals$Method<-rownames(gh.pvals)
gh.pvals<-gh.pvals[c(5,1,2,3,4)]

gh.decision<-data.frame(gh.out$matrix.decision)
gh.decision$Method<-rownames(gh.decision)
gh.decision<-gh.decision[c(5,1,2,3,4)]

gh.pvals %>%
  flextable() %>%
  add_header_lines(values = "p values for Means") %>%
  theme_box()

gh.decision %>%
  flextable() %>%
  add_header_lines(values = "Decision Matrix") %>%
  theme_box()

# Tukey HSD for Dispersion
so.ada<-summary.continuous(ADA~method, data = Solder)
(sourcetableADA.aov <- summary(solderADA.aov))
(ADA.out<-sourcetable.ADA.aov[[1]])
(MSE.ada<-ADA.out$`Mean Sq`[2])
(dfe.ada<-ADA.out$Df[2])

tuk.ada.out <- contrasts.tukey.kgroups.simple(group.label = so.ada$method
                                                ,group.mean = so.ada$mean
                                                ,group.sample.size = so.ada$n
                                                ,conf.level.familywise = 0.95
                                                ,n.means = 4
                                                ,mean.squared.error = MSE.ada
                                                ,df.mean.squared.error = dfe.ada)

tuk.ada.pvals<-data.frame(ro(tuk.ada.out$matrix.p.value,4))
tuk.ada.pvals$Method<-rownames(tuk.ada.pvals)
tuk.ada.pvals<-tuk.ada.pvals[c(5,1,2,3,4)]

tuk.ada.decision<-data.frame(tuk.ada.out$matrix.decision)
tuk.ada.decision$Method<-rownames(tuk.ada.decision)
tuk.ada.decision<-tuk.ada.decision[c(5,1,2,3,4)]

tuk.ada.pvals %>%
  flextable() %>%
  add_header_lines(values = "p values for ADA Means") %>%
  theme_box()

tuk.ada.decision %>%
  flextable() %>%
  add_header_lines(values = "ADA Decision Matrix") %>%
  theme_box()



      
      