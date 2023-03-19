# ISO Plot Example for Variances
g1<-rnorm(n = 100, mean = 10, sd = 2)
g2<-g1+rnorm(n = 100, mean = 0, sd = runif(1,0,2))
plot(g1, g2, xlab = "Group 1", ylab = "Group 2")
abline(lm(g2~g1))

# Add ISO line
min <- min(range(g1), range(g2))
max <- max(range(g1), range(g2))
lines(x = min:max, y = min:max, lwd = 2, lty = 2, col = "blue")

