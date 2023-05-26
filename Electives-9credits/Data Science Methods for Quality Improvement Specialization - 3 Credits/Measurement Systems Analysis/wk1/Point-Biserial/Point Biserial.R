# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Point Biserial Correlation between Continuous and Nominal ---------------
PolyThk <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 Correlation and Association/PolyThk.dat")
View(PolyThk)

# Test for normality within each dichotomous variable
ro(summary.continuous(EOLThick~Line, PolyThk),4)

# Correlation Coefficient, rpbi
cor.point.biserial(discrete_var = PolyThk$Line
                   ,continuous_var = PolyThk$EOLThick
                   ,conf.level = 0.90, ordered = TRUE)

# "ordered = TRUE" is needed to get a signed correlation 
# coefficient for the point-biserial correlation by 
# forcing the routine to order the values of the 
# dichotomous variable.

plot(PolyThk$Line, PolyThk$EOLThick)
abline(lm(PolyThk$EOLThick ~ PolyThk$Line), col = "purple", lwd = 2, lty = 1)

t.test.twosample.independent.fx(fx = EOLThick~Line
                                ,data = PolyThk)
