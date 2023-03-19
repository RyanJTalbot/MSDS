cfm<-c(68,72,72,74,72,69,75,75,72,73,70,71,71,72,73,72,70,72,73,74)
fans<-data.frame(cfm)
View(fans)

require(lolcat)
spc.run.chart(chart.series = fans$cfm, main = "Run Chart: Computer Fans"
              ,ylab = "CFM",pch = 19, cex=1.5, col="blue", lty=1, lwd=2
              ,type = "o")
mean(fans$cfm)
abline(h=72)
