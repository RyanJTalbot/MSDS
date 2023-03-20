hist.grouped(castings$weight, xlab="Weight", freq=F)
lines(density(castings$weight))

plot(density(castings$weight), main="Density Plot of Casting Weight", xlab="Weight")

dp<-density(castings$weight)
plot(dp, main="Density Plot of Casting Weight", xlab="Weight")
polygon(dp, col="red", border="black")
