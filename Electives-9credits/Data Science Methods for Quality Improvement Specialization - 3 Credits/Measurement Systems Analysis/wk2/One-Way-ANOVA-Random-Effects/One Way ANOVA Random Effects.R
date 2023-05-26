# Startup Code ------------------------------------------------------------
require(lolcat)          
require(car)
require(dplyr)
require(flextable)

options(scipen=99,digits = 10)
options(show.signif.stars=FALSE)   # Turn off * to indicate significance
nqtr <- function(x,d){noquote(t(round.object(x, d)))}
ro <- round.object

# Import Data File --------------------------------------------------------
Gear <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 One Way ANOVA/Gear.dat")
View(Gear)
str(Gear)

# Specify Factors with labels -------------------------------------------
group.labels<-c("Poly1","Poly2","Poly3","Poly4","Poly5")
Gear$material<-factor(Gear$material, labels = group.labels)
str(Gear)

# Descriptive Summary -----------------------------------------------------
(so <- ro(summary.continuous(ctf ~ material, Gear, stat.miss=F),4))
boxplot(ctf ~ material,data = Gear, 
        xlab="Polymer", 
        ylab="Cycles to Failure", 
        main="Cycles to Failure By Polymer", 
        col="red")

so %>%
  flextable() %>%
  add_header_lines(values = "Descriptive Summary") %>%
  theme_box()

# Create output object of the cell means
(means<-so$mean)

# Test for normality of cell means
summary.continuous(means)

# ANOVA Syntax ------------------------------------------------------------
gear.aov<-aov(formula = ctf~material, data = Gear)
(sourcetable.aov <- summary(gear.aov))

# Add Totals to ANOVA Table
(anova.temp<-sourcetable.aov[[1]])
totaldf<-sum(anova.temp$Df)
totalss<-sum(anova.temp$`Sum Sq`)
total<-data.frame(totaldf, totalss,"","","")
names(total)<-c("Df","Sum Sq","Mean Sq","F value","Pr(>F)")
(anova.out<-rbind(anova.temp,as.numeric(total)))
rownames(anova.out)<-c("Material","Residuals","Total")
anova.out$Source<-rownames(anova.out)
anova.out<-anova.out[c(6,1,2,3,4,5)]

# ANOVA Source Table ------------------------------------------------------
anova.out %>%
  flextable() %>%
  add_header_lines(values = "ANOVA Source Table") %>%
  colformat_double(j=c('Sum Sq','Mean Sq', 'F value', 'Pr(>F)'), digits=4, na_str = '') %>%
  theme_box()
  
# Random Effects Analysis --------------------------------------------------
require(EMSaov)
EMSanova(formula = ctf~material, data = Gear
         ,type = "R"
         ,level = 5)

# Calculate Treatment Variance
(subgroup.n<-(anova.out$Df[3]+1)/(anova.out$Df[1]+1))

(Treat.var<-(anova.out$`Mean Sq`[1]-anova.out$`Mean Sq`[2])/subgroup.n)

# Within Variance
(MSw<-anova.out$`Mean Sq`[2])

# Total Variance
(Total.var<-Treat.var + MSw)

# Intraclass Correlation Coefficient
Treat.var/Total.var


