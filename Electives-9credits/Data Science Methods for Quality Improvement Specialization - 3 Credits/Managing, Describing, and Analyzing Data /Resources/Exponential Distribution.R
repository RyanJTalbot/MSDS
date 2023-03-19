require(lolcat)
nqtr<-function(x,d){noquote(t(round.object(x, d)))}

# Example 1
pexp(q = 60, rate = 1/100, lower.tail = F)

# Shade areas under the exponential curve
# Create the exponential curve
x=seq(0,800,length=200)
y=dexp(x, rate = 1/100)
plot(x,y,type="l")

# Shade the upper tail area
x=seq(60,800,length=100)
y=dexp(x, rate = 1/100)
polygon(c(60,x,800),c(0,y,0),col="red")

# Example 2
pexp(q = (20-5),rate = 1/(50-5), lower.tail = T)
pexp.low(q = 20, low = 5, mean = 50, lower.tail = T)

# Shade areas under the exponential curve
# Create the exponential curve
x=seq(0,400,length=200)
y=dexp(x, rate = 1/50)
plot(x,y,type="l")

# Shade the lower tail area from xmin to 20
x=seq(5,20,length=100)
y=dexp(x, rate = 1/50)
polygon(c(5,x,20),c(0,y,0),col="red")

# Test for Exponentiality when n <= 100
expdata<-rexp(n = 100, rate = 1/50)
shapiro.wilk.exponentiality.test(expdata)

# Test for Exponentiality when n > 100
expdata<-rexp(n = 101, rate = 1/50)
shapiro.wilk.exponentiality.test(expdata) # note it doesn't work!
shapetest.exp.epps.pulley.1986(expdata)
