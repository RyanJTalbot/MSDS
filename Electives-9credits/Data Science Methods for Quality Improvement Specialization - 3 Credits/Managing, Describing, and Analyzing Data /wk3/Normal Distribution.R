require(lolcat)

#Example 1
# Calculate the area under the normal curve using the Z Score
pnorm(q = -1.6, mean = 0, sd = 1, lower.tail = T)

# Calculate the area under the normal curve using the pnorm function
pnorm(q = 172, mean = 180, sd = 5, lower.tail = TRUE)

#Example 2
# Calculate the area under the normal curve using the Z Score
pnorm(q = -1.0, mean = 0, sd = 1, lower.tail = T)
pnorm(q = 3, mean = 0, sd = 1, lower.tail = F)

# Calculate the area under the normal curve using the pnorm function
pnorm(q = 5.15, mean = 5.20, sd = .05, lower.tail = T)
pnorm(q = 5.35, mean = 5.20, sd = .05, lower.tail = F)

#Create output variables
(lower<-pnorm(q = 5.15, mean = 5.20, sd = .05, lower.tail = T))
(upper<-pnorm(q = 5.35, mean = 5.20, sd = .05, lower.tail = F))

#Add together for total area under the normal curve
(total=lower+upper)
(totalpercent=total*100)
round.object(totalpercent,2)

# Shade areas under the normal curve
# Create the normal curve
x=seq(5,5.45,length=200)
y=dnorm(x,mean=5.22,sd=.05)
plot(x,y,type="l")

# Shade the lower tail area
x=seq(5,5.15,length=100)
y=dnorm(x,mean=5.22,sd=.05)
polygon(c(5,x,5.15),c(0,y,0),col="red")

# Shade the upper tail area
x=seq(5.35,5.45,length=100)
y=dnorm(x,mean=5.22,sd=.05)
polygon(c(5.35,x,5.45),c(0,y,0),col="red")

# Add line at mean
abline(v = 5.22)

# Test for normality when n < 25
normdata<-rnorm(n = 24, mean = 10, sd = 2)
anderson.darling.normality.test(normdata)
shapiro.wilk.normality.test(normdata)
summary.continuous(normdata)

# Test for normality when n >= 25
normdata<-rnorm(n = 25, mean = 10, sd = 2)
(normout<-dagostino.normality.omnibus.test(normdata))
(skkupvals<-c(normout$estimate[6], normout$estimate[12]))
summary.continuous(normdata)
