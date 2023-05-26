# Startup Code ------------------------------------------------------------
require(lolcat)          
require(car)             
options(scipen=99,digits = 10)
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

# Basic Computations ------------------------------------------------------
# Calculate Summary Statistics for the Solder Data
(so <- summary.continuous(push ~ method, Solder))
str(so)
(means <- so$mean)     # Display the structure of the Solder data frame

# Compute the means of each of the 4 groups:
(means <- so$mean)

# Compute the variance for each of the 4 groups:
(vars<-so$var)

# Compute the variance between the 4 group means:
var(means)

# Compute the mean (average) of the 4 group variances:
(msw<-mean(vars))

# Multiply the variance between the means by the sample size, n
(n<-unique(so$n))

(msb<-ro(n*var(means),4))

# Divide the between variance from step 5 by the within variance from step 4:
(F.aov<-msb/msw)

