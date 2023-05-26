# Create data file
weight<-c(65,67,36,37,36,57,53,39,38,58)
preform<-data.frame(weight)
View(preform)

# Find the range of values in the data set
range(preform$weight)
rng<-range(preform$weight)
rng[2]-rng[1]

# Find the Interquartile Range of the data set
IQR(preform$weight)

# Find the standard deviation of the data set
sd(preform$weight)
round.object(sd(preform$weight),2)

# Find the variance of the data set
var(preform$weight)
round.object(var(preform$weight),2)
