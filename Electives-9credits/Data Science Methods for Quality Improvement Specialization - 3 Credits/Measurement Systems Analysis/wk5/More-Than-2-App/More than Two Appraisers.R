# Startup Code
require(lolcat)
require(car)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# More than 2 Appraisers --------------------------------------------------
welds <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/welds.txt")
View(welds)

msa.welds<-msa.nominal.concordance(welds$Ray
                                   , welds$Abhishek
                                   , welds$Katrina)

sum.msa.welds <- ro(summary(msa.welds), 4)
sum.msa.welds$BetweenOperators$Description <- c("Ray vs Abhi"
                                                , "Ray vs Kat"
                                                , "Abhi vs Kat")
welds.out<-as.data.frame(sum.msa.welds$BetweenOperators)

welds.out %>%
  t() %>% 
  as.data.frame() %>% 
  tibble::rownames_to_column() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Concordance Results") %>%
  theme_box()

require(irr)
(overall.kappa<-kappam.light(welds))
overall.kappa$value
