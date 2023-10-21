---
title: "Ch11-surv-lab"
jupyter:
  jupytext:
    formats: ipynb,Rmd
    text_representation:
      extension: .Rmd
      format_name: rmarkdown
      format_version: '1.2'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: R
    language: R
    name: ir
---





# Lab: Survival Analysis

In this lab, we perform survival analyses on three separate data sets. In Section 11.8.1 we analyze the `BrainCancer` data that was  first described in Section 11.3.
 In Section 11.8.2, we examine the `Publication` data from Section 11.5.4. Finally, Section 11.8.3 explores a simulated call center data set.

## Brain Cancer Data
We begin with the `BrainCancer` data set, which is part of the  `ISLR2` package.

```{r chunk1}
library(ISLR2)
```

The rows index the 88 patients, while the columns contain the 8 predictors.

```{r chunk2}
names(BrainCancer)
```

We first briefly examine the data.

```{r chunk3}
attach(BrainCancer)
table(sex)
table(diagnosis)
table(status)
```

Before beginning an analysis, it is important to know how the `status` variable has been coded.  Most software, including `R`, uses the convention that `status = 1` indicates an uncensored observation,  and `status = 0` indicates a censored observation. But some scientists might use the opposite coding. For the `BrainCancer` data set $35$ patients died before the end of the study.

To begin the analysis, we re-create  the Kaplan-Meier survival curve  shown in  Figure 11.2, using the `survfit()` function within the `R` `survival` library. Here `time` corresponds to $y_i$, the time to the $i$th event (either censoring or death).

```{r chunk4}
library(survival)
fit.surv <- survfit(Surv(time, status) ~ 1)
plot(fit.surv, xlab = "Months",
    ylab = "Estimated Probability of Survival")
```

Next we create Kaplan-Meier survival curves that are stratified by `sex`, in order to reproduce Figure 11.3.

```{r chunk5}
fit.sex <- survfit(Surv(time, status) ~ sex)
plot(fit.sex, xlab = "Months",
    ylab = "Estimated Probability of Survival", col = c(2,4))
legend("bottomleft", levels(sex), col = c(2,4), lty = 1)
```


As discussed in Section 11.4, we can perform a log-rank test to compare the survival of males to females, using the `survdiff()` function.

```{r chunk6}
logrank.test <- survdiff(Surv(time, status) ~ sex)
logrank.test
```

The resulting $p$-value is $0.23$, indicating  no evidence of a difference in survival between the two sexes.


Next, we fit  Cox proportional hazards models using the `coxph()`  function.
To begin, we consider a model that uses `sex` as the only predictor.

```{r chunk7}
fit.cox <- coxph(Surv(time, status) ~ sex)
summary(fit.cox)
```

Note that the values of the likelihood ratio, Wald, and score tests have been rounded.  It is possible to display additional digits.

```{r chunk8}
summary(fit.cox)$logtest[1]
summary(fit.cox)$waldtest[1]
summary(fit.cox)$sctest[1]
```

Regardless of which test we use, we see that there is no clear evidence for a difference in survival between males and females.

```{r chunk9}
logrank.test$chisq
```

As we learned in this chapter, the score test from the Cox model is exactly equal to the log rank test statistic!

Now we fit a  model that makes use of additional predictors. 

```{r chunk10}
fit.all <- coxph(
Surv(time, status) ~ sex + diagnosis + loc + ki + gtv +
   stereo)
fit.all
```

The `diagnosis` variable has been coded so that the baseline
corresponds to meningioma. The results indicate that the risk associated with HG glioma is more than eight times (i.e. $e^{2.15}=8.62$) the risk associated with meningioma. In other words, after adjusting for the other predictors, patients with HG glioma have much worse survival
compared to those with meningioma.  In addition, larger values of the Karnofsky index, `ki`, are associated with lower risk, i.e. longer survival.

Finally, we plot survival curves for each diagnosis category,  adjusting for the other predictors.
To make these plots, we set the values of the other predictors equal
to the mean for quantitative variables, and the modal value for
factors. We first create a data frame with four rows, one for each
level of diagnosis. The `survfit()` function will produce a curve for each of the rows in this data frame,
and one call to `plot()` will display them all in the same plot.


```{r chunk11}
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
```




## Publication Data



\normalsize

The `Publication` data presented in Section 11.5.4 can be found in the `ISLR2` library. We first reproduce Figure 11.5 by plotting the Kaplan-Meier curves stratified on the `posres` variable, which records whether the study had a positive or negative result.

```{r chunk12}
fit.posres <- survfit(
    Surv(time, status) ~ posres, data = Publication
  )
plot(fit.posres, xlab = "Months",
    ylab = "Probability of Not Being Published", col = 3:4)
legend("topright", c("Negative Result", "Positive Result"),
    col = 3:4, lty = 1)
```


As discussed previously, the $p$-values from fitting Cox's proportional hazards model to the `posres` variable are quite large, providing no evidence of a difference in time-to-publication between studies with positive versus negative results.

```{r chunk13}
fit.pub <- coxph(Surv(time, status) ~ posres,
    data = Publication)
fit.pub
```


As expected, the log-rank test provides an identical conclusion.

```{r chunk14}
logrank.test <- survdiff(Surv(time, status) ~ posres,
    data = Publication)
logrank.test
```


However, the results change dramatically when we include other  predictors in the model. Here we have excluded the funding mechanism variable.

```{r chunk15}
fit.pub2 <- coxph(Surv(time, status) ~ . - mech,
    data = Publication)
fit.pub2
```

We see that there are a number of  statistically significant variables, including whether the trial focused on a clinical endpoint, the impact of the study, and whether the study had positive or negative results.

## Call Center Data

In this section, we will simulate survival data using the `sim.survdata()` function, which is part of the `coxed` library. Our simulated data will represent the observed wait times (in seconds) for 2,000 customers who have phoned  a call center.
In this context, censoring occurs if a customer hangs up before his or her call is answered.

There are three covariates: `Operators` (the number of call center operators available at the time of the call, which can range from $5$ to $15$), `Center` (either A, B, or C), and `Time` of day (Morning, Afternoon, or Evening). We generate data for these covariates so that all possibilities are equally likely: for instance, morning, afternoon and evening calls are equally likely, and any number of operators from $5$ to $15$ is equally likely.

```{r chunk16}
set.seed(4)
N <- 2000
Operators <- sample(5:15, N, replace = T)
Center <- sample(c("A", "B", "C"), N, replace = T)
Time <- sample(c("Morn.", "After.", "Even."), N, replace = T)
X <- model.matrix( ~ Operators + Center + Time)[, -1]
```

It is worthwhile to take a peek at the design matrix `X`},  so that we can be sure that we understand how the
variables have been coded.

```{r chunk17}
X[1:5, ]
```

Next,  we specify the coefficients and the hazard function.

```{r chunk18}
true.beta <- c(0.04, -0.3, 0, 0.2, -0.2)
h.fn <- function(x) return(0.00001 * x)
```

Here, we have set the coefficient associated with `Operators` to equal $0.04$; in other words, each additional operator leads to a $e^{0.04}=1.041$-fold increase in the
  "risk" that the call will be answered,
given the `Center` and `Time` covariates. This makes sense: the greater the number of operators at hand, the shorter the wait time! The coefficient associated with `Center = B`
is $-0.3$, and `Center = A` is treated as the baseline. This means that the risk of a call being
answered at Center B is $0.74$ times the risk that it will be answered at Center A; in other words,
the wait times are a bit longer at Center B.

We are now ready to  generate data under the  Cox proportional hazards model. The `sim.survdata()` function allows us to specify the maximum possible failure time, which in this case corresponds to the longest possible wait time for a customer; we set this to equal $1{,}000$ seconds.

```{r chunk19}
library(coxed)
queuing <- sim.survdata(N = N, T = 1000, X = X,
    beta = true.beta, hazard.fun = h.fn)
names(queuing)
```



The "observed" data is stored in `queuing$data`, with `y` corresponding to the event time and `failed` an indicator of whether the call was answered (`failed = T`) or the customer hung up before the call was answered (`failed = F`). We see that almost $90\%$ of calls were answered.

```{r chunk20}
head(queuing$data)
mean(queuing$data$failed)
```





We now plot  Kaplan-Meier survival curves. First, we stratify by `Center`.

```{r chunk21}
fit.Center <- survfit(Surv(y, failed) ~ Center,
    data = queuing$data)
plot(fit.Center, xlab = "Seconds",
    ylab = "Probability of Still Being on Hold",
    col = c(2, 4, 5))
legend("topright",
     c("Call Center A", "Call Center B", "Call Center C"),
     col = c(2, 4, 5), lty = 1)
```

Next, we stratify by `Time`.

```{r chunk22}
fit.Time <- survfit(Surv(y, failed) ~ Time,
   data = queuing$data)
plot(fit.Time, xlab = "Seconds",
    ylab = "Probability of Still Being on Hold",
    col = c(2, 4, 5))
legend("topright", c("Morning", "Afternoon", "Evening"),
    col = c(5, 2, 4), lty = 1)
```

It seems that calls at Call Center B
  take longer to be answered than calls at Centers A and C. Similarly, it appears that wait times are longest in the morning and shortest in the evening hours. We can use a log-rank test to determine whether these differences are statistically significant.

```{r chunk23}
survdiff(Surv(y, failed) ~ Center, data = queuing$data)
survdiff(Surv(y, failed) ~ Time, data = queuing$data)
```



We find that  differences between centers are highly significant, as are differences between times of day.


Finally, we fit Cox's proportional hazards model to the data.

```{r chunk24}
fit.queuing <- coxph(Surv(y, failed) ~ .,
    data = queuing$data)
fit.queuing
```

The $p$-values for `Center = B`, `Time = Even.` and `Time = Morn.` are very small. It is also clear that the hazard --- that is, the instantaneous risk that a call will be answered --- increases with the number of operators. Since we generated the data ourselves, we know that the true coefficients for `Operators`, `Center = B`, `Center = C`, `Time = Even.` and `Time = Morn.` are  $0.04$, $-0.3$, $0$, $0.2$, and $-0.2$, respectively. The coefficient estimates resulting from the Cox model are fairly accurate.




