# Startup Code
require(lolcat)
require(car)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Appraisers, Two Categories ------------------------------------------
Inspector.A.vs.B.Radios <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Inspector A vs B Radios.dat")
View(Inspector.A.vs.B.Radios)
radios<-Inspector.A.vs.B.Radios
str(radios)

# Concordance Between Two Appraisers --------------------------------------
# Create a contingency table of observed values
(ct.radios.obs<-table(radios$Inspector_A, radios$Inspector_B))
(ct.radios.obs <- matrix(
  data = ct.radios.obs,
  nrow = 2, byrow = F,
  dimnames = list(
    "Inspector A" = c("Pass", "Fail"),
    "Inspector B" = c("Pass", "Fail"))))

View(ct.radios.obs)

radios.msa <-
  msa.nominal.concordance(radios$Inspector_A
                        , radios$Inspector_B)
sum.radios <- summary(radios.msa)
nqtr(sum.radios$BetweenOperators, 5)

# Stacked Bar Chart - Proportions
(pc<-sum.radios$BetweenOperators$p.chance)
(po<-sum.radios$BetweenOperators$p.agree)
(po.pc<-po-pc)
(denom<-1-pc)
(pom.po<-(sum.radios$BetweenOperators$kappa.max*denom)-po.pc)
(top.pom<-1-(pom.po+po.pc+pc))

# Create stacked bar chart
# Stacked Bar Plot with Colors and Legend
bar.chart<-as.table(rbind(pc, po.pc, pom.po, top.pom))
colnames(bar.chart)<-"Proportions"
(counts<-bar.chart)
barplot(counts, main="Proportion Agreement",
        col=c("lightskyblue4","lightgoldenrod3", "snow3","lavenderblush"), ylim = c(0,1)
        ,legend.text = c("Chance","Agreement","Item Loss","Scale Loss")
        ,args.legend = list(x = "bottomright"))
        

# Colors Summary
http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf

# Internal Consistency----------------------------------------------------
# Inspector A
Inspector.A.Internal.Consistency <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Inspector A Internal Consistency.txt")
View(Inspector.A.Internal.Consistency)
ICA<-Inspector.A.Internal.Consistency

# Create a contingency table of observed values
(ct.A<-table(ICA$Measure_1, ICA$Measure_2))
(ct.A <- matrix(
  data = ct.A,
  nrow = 2, byrow = F,
  dimnames = list(
    "Measure 1" = c("Pass", "Fail"),
    "Measure 2" = c("Pass", "Fail"))))

View(ct.A)

# Use MSA Nominal Internal Consistency
msa.ic.A <-
  msa.nominal.internalconsistency(ICA$Measure_1
                                , ICA$Measure_2)
msa.ic.A$comparisons

sum.msa.ic.A<-as.data.frame(ro(summary(msa.ic.A),4))
sum.msa.ic.A$Description<-"Statistic"

sum.msa.ic.A %>%
  t() %>% 
  as.data.frame() %>% 
  add_rownames() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Int. Cons. Inspector A") %>%
  theme_box()

# Inspector B
Inspector.B.Internal.Consistency <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Inspector B Internal Consistency.txt")
View(Inspector.B.Internal.Consistency)
ICB<-Inspector.B.Internal.Consistency

# Create a contingency table of observed values
(ct.B<-table(ICB$Measure_1, ICB$Measure_2))
(ct.B <- matrix(
  data = ct.B,
  nrow = 2, byrow = F,
  dimnames = list(
    "Measure 1" = c("Pass", "Fail"),
    "Measure 2" = c("Pass", "Fail"))))

View(ct.B)

# Use MSA Nominal Internal Consistency
msa.ic.B <-
  msa.nominal.internalconsistency(ICB$Measure_1
                                , ICB$Measure_2)
msa.ic.B$comparisons

sum.msa.ic.B<-as.data.frame(ro(summary(msa.ic.B),4))
sum.msa.ic.B$Description<-"Statistic"

sum.msa.ic.B %>%
  t() %>% 
  as.data.frame() %>% 
  add_rownames() %>%
  flextable() %>%
  delete_part(part = "header") %>%
  add_header_lines(values = "Int. Cons. Inspector B") %>%
  theme_box()
