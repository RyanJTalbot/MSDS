# Startup Code
require(lolcat)
require(car)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Testing for Validity ----------------------------------------------------
Inspector.A.vs.B.Radios <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Inspector A vs B Radios.dat")
radios<-Inspector.A.vs.B.Radios
View(radios)

# Inspector A vs Actual
addmargins(table(radios$Actual, radios$Inspector_A))

# Inspector B vs Actual
addmargins(table(radios$Actual, radios$Inspector_B))

msa.validity<-msa.nominal.concordance(radios$Inspector_A, radios$Inspector_B, standard = radios$Actual)
ro(summary(msa.validity),4)

# Light's G calculation ---------------------------------------------------
radios_validity <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/radios_validity.txt")
View(radios_validity)
rv<-radios_validity

cor.light.g.onesample(subject = rv$Subject
                      ,rater = rv$Appraiser
                      ,rating = rv$Rating
                      ,rater.standard = 3)
