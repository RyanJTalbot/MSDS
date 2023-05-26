# Calculate skewness for the castings data
skewness(castings$weight)
round.object(skewness(castings$weight),3)

# Calculate kurtosis for the castings data
kurtosis(castings$weight)
round.object(kurtosis(castings$weight),3)

# Calculate descriptive statistics using the summary.continuous command
summary.continuous(castings$weight, stat.sd=T)
round.object(summary.continuous(castings$weight, stat.sd=T),3)

# Transpose the output and remove the quotes
t(round.object(summary.continuous(castings$weight, stat.sd=T),3))
noquote(t(round.object(summary.continuous(castings$weight, stat.sd=T),3)))

# Create a function to round, transpose and remove the quotes
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
nqtr(summary.continuous(castings$weight),3)
