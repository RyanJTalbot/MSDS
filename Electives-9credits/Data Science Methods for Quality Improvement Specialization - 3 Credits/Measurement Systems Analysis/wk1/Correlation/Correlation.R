# Startup Code
require(lolcat)
require(car)
require(PerformanceAnalytics)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Rivet Example -----------------------------------------------------------
Rivet <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 Correlation and Association/Rivet.dat")
View(Rivet)

# Scatterplot example
plot(x = Rivet$paint, y = Rivet$rivet, pch = 19)
abline(lm(rivet~paint, data = Rivet), col = "blue") # lm = linear model

# Using companion to applied regression (car)
scatterplot(rivet~paint, Rivet)
scatterplotMatrix(Rivet)

# Pearson Product Moment Correlation Coefficient --------------------------
cor(Rivet)
cor(x = Rivet$paint, y = Rivet$rivet)

# t test for Correlation when rho = 0 -------------------------------------
# t test for Correlation (Correlation)
(cor.pearson<-cor.pearson.r.onesample.simple(sample.r = 0.30
                               ,sample.size = 70
                               ,null.hypothesis.rho = 0
                               ,alternative = "two.sided"
                               ,conf.level = 0.95))

# For use with a data file 
cor.pearson.r.onesample()

# Importance - r^2 --------------------------------------------------------
str(cor.pearson)
View(cor.pearson)
cor.pearson$estimate
cor.pearson$estimate[4]
(imp.pearson<-cor.pearson$estimate[4]*100)

# Fisher's Z F (Approximate Normal) Test for Correlation rho = rho0 -------
# Same as above, but rho > 0
n<-40
rho<-0.62
r<-0.75

cor.pearson.r.onesample.simple(sample.r = r
                               ,sample.size = n
                               ,null.hypothesis.rho = rho
                               ,alternative = "two.sided"
                               ,conf.level=0.95)

# Using Performance Analytics
chart.Correlation(Rivet)
