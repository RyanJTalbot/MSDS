# Create data file
weight<-c(65,67,36,37,36,57,53,39,38,58)
preform<-data.frame(weight)
View(preform)

# Find the minimum (lowest) value in the data set
min(preform$weight)

# Find the maximum (highest) value in the data set
max(preform$weight)

# Find the minimum and maximum in the data set
summary(preform$weight)

# Find the 30th percentile of the preform data
quantile(x = preform$weight, probs = 0.30)

# Find the 1st Quartile of the preform data
quantile(x = preform$weight, probs = 0.25)

# Find the 1st and 3rd  Quartile of the preform data
quantile(x = preform$weight, probs = c(0.25,0.75))
