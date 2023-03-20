# Transform castings3 data from independent to dependent format
castnew<-transform.independent.format.to.dependent.format(fx = weight~mold, data = castings3)

# View current column names
colnames(castnew)

# Rename column headings
colnames(castnew)[1:3] <-c("Mold_1","Mold_2", "Mold_3")

# View new column heading names
View(castnew)

# Calculate Pearson Product-Moment Correlation Coefficient
cor(x = castnew$Mold_1, y = castnew$Mold_2, method = "pearson")

# Create scatterplot
plot(x = castnew$Mold_1, y =castnew$Mold_2,pch=19, cex=1, xlab="Mold 2", ylab="Mold 1")
abline(lm(castnew$Mold_2~castnew$Mold_1),col="blue",lwd=2)
