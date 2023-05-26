# Startup Code
require(lolcat)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Association for Nominal Data --------------------------------------------
# Contingency Table Format
(tbl.fmt <- matrix(c(2,1,2,1,2,3),nrow=2, ncol=3, byrow=TRUE,
                   dimnames=list(c("J1","J2"), c("K1", "K2", "K3"))))

# Frequency Format
(J <- c(1,1,1,2,2,2))
(K <- c(1,2,3,1,2,3))
(freq <- c(2,1,2,1,2,3))
(freq.fmt <-data.frame(J,K,freq))

# Freq format to cross tabulation
(tbl.from.freq <- transform.individual.format.to.xt(x_row = freq.fmt$J
                                                    ,x_col = freq.fmt$K
                                                    ,weight = freq.fmt$freq
                                                    ,x_row_name ="J"
                                                    ,x_col_name ="K"))
xtabs(freq~J+K, freq.fmt)

# Individual Format
(J <- c(1,1,1,1,1,2,2,2,2,2,2)) 
(K <- c(1,1,2,3,3,1,2,2,3,3,3)) 
(ind.fmt <- data.frame(J, K))

# Individual format to cross tabulation
transform.individual.format.to.xt(x_row = ind.fmt$J
                                  ,x_col = ind.fmt$K
                                  ,x_row_name ="J"
                                  ,x_col_name ="K")
xtabs(~J+K, ind.fmt)

# Other available transformations
transform.xt.to.independent.format()
transform.xt.to.individual.format()

# Casting.dat Example
Casting <- read.delim("G:/My Drive/Coursera/Course 3 -  Methods for Quality Improvement - Measurement Systems Analysis/Module 1 Correlation and Association/Casting.dat")
View(Casting)


# Converts from Freq format to Table
castxt<-transform.independent.format.to.xt(x_row = Casting$Filter
                                           ,x_col = Casting$Cracked
                                           ,weight = Casting$Count
                                           ,x_row_name = "Filter"
                                           ,x_col_name = "Cracked")
castxt

(cast.out<-chisq.test(castxt, correct = F))
cast.out$observed
cast.out$expected

# Conduct test (Pearson Phi, Cramer's V)
cor.pearson.phi(castxt)
cor.cramer.v(castxt)

# Contingency Table Example
# 3 by 4 table 
(vec.cus.def <- c(25, 20, 4, 6, 10, 7, 12, 10, 41, 33, 25, 13))
(cust.def <- matrix(vec.cus.def, ncol = 4
                    ,dimnames = list(c("Automotive", "Appliance", "Internal"),c("Blister", "Crack", "Pit", "Scratch"))))

cor.cramer.v(cust.def)
