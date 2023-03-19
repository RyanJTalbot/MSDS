# Create data file
weight<-c(65,67,36,37,36,57,53,39,38,58)
preform<-data.frame(weight)
View(preform)

# Calculate the mean of the ungrouped data
mean(preform$weight)

# Calculate the mean from grouped data
# Assign the output of the grouped frequency distribution
# to a variable called "fdcast"
(fdcast<-frequency.dist.grouped(castings$weight))

# Look at the structure of fdcast
str(fdcast)

# Create a vector of the midpoints of each class
# interval in the frequency distribution
# (put in parentheses to view output)
(midpts<-fdcast$midpoint)

# Create a vector of the frequency of each class
# interval in the frequency distribution
# (put in parentheses to view output)
(freq<-fdcast$freq)

# Use the weighted mean command in the base package
# to calculate the  mean of the grouped data
weighted.mean(x = midpts, w = freq)

# For comparison, calculate the ungrouped mean of the 
# Casting Weight data
mean(castings$weight)

# Weighted Mean
wt<-c(0.2, 0.4, 0.4)
x<-c(88, 85, 92)
weighted.mean(x = x, w = wt)

# Median
median(preform$weight)

# Mode 
table(preform$weight)
sample.mode(preform$weight)


# What if there are 2 modes? Add in another 57
weight<-c(65,67,36,37,36,57,53,39,38,58,57)
preform<-data.frame(weight)
View(preform)

# Calculate the Mode
sample.mode(preform$weight)
