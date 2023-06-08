
# Lab: Survival Analysis


## Brain Cancer Data

###
library(ISLR2)
###
names(BrainCancer)
###
attach(BrainCancer)
table(sex)
table(diagnosis)
table(status)
###
library(survival)
fit.surv <- survfit(Surv(time, status) ~ 1)
plot(fit.surv, xlab = "Months",
    ylab = "Estimated Probability of Survival")
###
fit.sex <- survfit(Surv(time, status) ~ sex)
plot(fit.sex, xlab = "Months",
    ylab = "Estimated Probability of Survival", col = c(2,4))
legend("bottomleft", levels(sex), col = c(2,4), lty = 1)
###
logrank.test <- survdiff(Surv(time, status) ~ sex)
logrank.test
###
fit.cox <- coxph(Surv(time, status) ~ sex)
summary(fit.cox)
###
summary(fit.cox)$logtest[1]
summary(fit.cox)$waldtest[1]
summary(fit.cox)$sctest[1]
###
logrank.test$chisq
###
fit.all <- coxph(
Surv(time, status) ~ sex + diagnosis + loc + ki + gtv +
   stereo)
fit.all
###
modaldata <- data.frame(
     diagnosis = levels(diagnosis),
     sex = rep("Female", 4),
     loc = rep("Supratentorial", 4),
     ki = rep(mean(ki), 4),
     gtv = rep(mean(gtv), 4),
     stereo = rep("SRT", 4)
     )
survplots <- survfit(fit.all, newdata = modaldata)
plot(survplots, xlab = "Months",
    ylab = "Survival Probability", col = 2:5)
legend("bottomleft", levels(diagnosis), col = 2:5, lty = 1)

## Publication Data

###
fit.posres <- survfit(
    Surv(time, status) ~ posres, data = Publication
  )
plot(fit.posres, xlab = "Months",
    ylab = "Probability of Not Being Published", col = 3:4)
legend("topright", c("Negative Result", "Positive Result"),
    col = 3:4, lty = 1)
###
fit.pub <- coxph(Surv(time, status) ~ posres,
    data = Publication)
fit.pub
###
logrank.test <- survdiff(Surv(time, status) ~ posres,
    data = Publication)
logrank.test
###
fit.pub2 <- coxph(Surv(time, status) ~ . - mech,
    data = Publication)
fit.pub2

## Call Center Data

###
set.seed(4)
N <- 2000
Operators <- sample(5:15, N, replace = T)
Center <- sample(c("A", "B", "C"), N, replace = T)
Time <- sample(c("Morn.", "After.", "Even."), N, replace = T)
X <- model.matrix( ~ Operators + Center + Time)[, -1]
###
X[1:5, ]
###
true.beta <- c(0.04, -0.3, 0, 0.2, -0.2)
h.fn <- function(x) return(0.00001 * x)
###
library(coxed)
queuing <- sim.survdata(N = N, T = 1000, X = X,
    beta = true.beta, hazard.fun = h.fn)
names(queuing)
###
head(queuing$data)
mean(queuing$data$failed)
###
par(mfrow = c(1, 2))
fit.Center <- survfit(Surv(y, failed) ~ Center,
    data = queuing$data)
plot(fit.Center, xlab = "Seconds",
    ylab = "Probability of Still Being on Hold",
    col = c(2, 4, 5))
legend("topright",
     c("Call Center A", "Call Center B", "Call Center C"),
     col = c(2, 4, 5), lty = 1)
###
fit.Time <- survfit(Surv(y, failed) ~ Time,
   data = queuing$data)
plot(fit.Time, xlab = "Seconds",
    ylab = "Probability of Still Being on Hold",
    col = c(2, 4, 5))
legend("topright", c("Morning", "Afternoon", "Evening"),
    col = c(5, 2, 4), lty = 1)
###
survdiff(Surv(y, failed) ~ Center, data = queuing$data)
survdiff(Surv(y, failed) ~ Time, data = queuing$data)
###
fit.queuing <- coxph(Surv(y, failed) ~ .,
    data = queuing$data)
fit.queuing
###
