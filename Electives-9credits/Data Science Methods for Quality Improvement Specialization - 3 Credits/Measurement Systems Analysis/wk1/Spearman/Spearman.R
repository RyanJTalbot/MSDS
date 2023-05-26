# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Spearman's Rank Order Correlation rs ------------------------------------
Spearman <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 Correlation and Association/Spearman.dat")
View(Spearman)

Spearman$Rank.Cracks<-rank(Spearman$Cracks
                           , ties.method = "average")

Spearman$Rank.Passes<-rank(Spearman$Passes
                           , ties.method = "average")

cor(Spearman$Cracks, Spearman$Passes, method = "spearman")
cor(Spearman$Rank.Cracks, Spearman$Rank.Passes)


cor.spearman.rank(x1 = Spearman$Cracks
                  ,x2 = Spearman$Passes)

plot(Spearman$Passes, Spearman$Cracks, pch=19) 
abline(lm(Spearman$Cracks ~ Spearman$Passes), col = "blue" , lwd = 1.5, lty = 1)
