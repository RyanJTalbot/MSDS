# Startup Code
require(lolcat)
require(car)
require(dplyr)
require(flextable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# Two Appraisers, More Than 2 Categories ----------------------------------
Operator.1.vs.Operator.2 <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Operator 1 vs Operator 2.txt")
View(Operator.1.vs.Operator.2)
ops<-Operator.1.vs.Operator.2

# 1 = OK
# 2 = Chunky
# 3 = Streak
# 4 = Light

# Create contingency table of observed values
(ct.ops.obs<-table(ops$Op_1, ops$Op_2))

# Acceptable vs Unacceptable

# Group unacceptable categories together
# Create new file 
ops.new<-ops
View(ops.new)
ops.new[ops.new==1]<-0 # any value equal to 1 becomes a zero
ops.new[ops.new > 1]<-1 # any value greater than 1 becomes a 1

View(ops.new)

# Create Contingency Table with Collapsed Table
(ct.new.obs<-table(ops.new$Op_1, ops.new$Op_2))


# Concordance Summary
msa.new.out<-msa.nominal.concordance(ops.new$Op_1, ops.new$Op_2)
msa.new.out$comp.operators

sum.msa.new.out<-ro(summary(msa.new.out),4)
nqtr(sum.msa.new.out$BetweenOperators,4)


# Review Unacceptable Reasons

# Make Acceptable an "NA"
ops.un<-ops
ops.un[ops.un==1]<-NA # any value equal to 1 becomes NA
View(ops.un)

# Contingency Table of Unacceptable Observed Values
(ct.un.obs<-table(ops.un$Op_1, ops.un$Op_2))

# Concordance Summary
msa.un.out<-msa.nominal.concordance(measurement1 = ops.un$Op_1
                                    , measurement2 = ops.un$Op_2)

msa.un.out$comp.operators$`measurement1 v measurement2`

sum.msa.un.out<-summary(msa.un.out)
nqtr(sum.msa.un.out$BetweenOperators,4)


# Post Hoc Analysis - Two Appraisers, More than Two Categories ------------
# "Collapse" across cells

# Chunky (2) vs the Others
ops.chunky<-ops.un
ops.chunky[ops.chunky==2]<-0 # any value equal to 2 becomes a zero
ops.chunky[ops.chunky > 2]<-1 # any value greater than 1 becomes a 1
View(ops.chunky)

# Contingency Table of Unacceptable Observed Values
(ct.chunky.obs<-table(ops.chunky$Op_1, ops.chunky$Op_2))

# Concordance Summary
msa.chunky.out<-msa.nominal.concordance(measurement1 = ops.chunky$Op_1
                                        ,measurement2 = ops.chunky$Op_2)

sum.chunky<-summary(msa.chunky.out)
nqtr(sum.chunky$BetweenOperators,4)

# Streak (3) vs the Others
ops.streak<-ops.un
ops.streak[ops.streak==3]<-0 # any value equal to 3 becomes a zero
ops.streak[ops.streak!=0]<-1 # any value not =0 becomes a 1
View(ops.streak)

# Contingency Table of Unacceptable Observed Values
(ct.streak.obs<-table(ops.streak$Op_1, ops.streak$Op_2))

# Concordance Summary
msa.streak.out<-msa.nominal.concordance(measurement1 = ops.streak$Op_1
                                               ,measurement2 = ops.streak$Op_2)

sum.streak<-summary(msa.streak.out)
nqtr(sum.streak$BetweenOperators,4)

# Light (4) vs the Others
ops.light<-ops.un
ops.light[ops.light==4]<-0 # any value equal to 3 becomes a zero
ops.light[ops.light!=0]<-1 # any value not =0 becomes a 1
View(ops.light)

# Contingency Table of Unacceptable Observed Values
(ct.light.obs<-table(ops.light$Op_1, ops.light$Op_2))

# Concordance Summary
msa.light.out<-msa.nominal.concordance(measurement1 = ops.light$Op_1
                                       ,measurement2 = ops.light$Op_2)

sum.light<-summary(msa.light.out)
nqtr(sum.light$BetweenOperators,4)

# Internal Consistency - More than 2 Categories ---------------------------
Op2.Internal.Consistency <- read.delim("G:/My Drive/Coursera/Course 3 - Methods for Quality Improvement - Measurement Systems Analysis/Module 5 Discrete MSA/Op2 Internal Consistency.txt")
View(Op2.Internal.Consistency)
Op2.ic<-Op2.Internal.Consistency

# Contingency Table of Observed Values
(ct.Op2.ic.obs<-table(Op2.ic$Trial_1, Op2.ic$Trial_2))
mcnemar.test(ct.Op2.ic.obs) # Only works for 2x2

# Use MSA Nominal Internal Consistency
msa.ic.Op2<-ro(msa.nominal.internalconsistency(Op2.ic$Trial_1, Op2.ic$Trial_2),4)
sum.msa.ic.op2<-summary(msa.ic.Op2)
nqtr(sum.msa.ic.op2,4)
