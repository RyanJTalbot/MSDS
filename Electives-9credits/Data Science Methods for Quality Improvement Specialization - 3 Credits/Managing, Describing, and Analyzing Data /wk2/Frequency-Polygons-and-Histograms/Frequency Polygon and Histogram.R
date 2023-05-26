cfm<-c(68,72,72,74,72,69,75,75,72,73,70,71,71,72,73,72,70,72,73,74)
fans<-data.frame(cfm)
View(fans)

frequency.polygon.ungrouped(fans$cfm, main="Ungrouped Freq Polygon: Fans Data",xlab="CFM")
frequency.polygon.grouped(castings$weight, main="Grouped Frequency Polygon: Casting Weight",xlab="Casting Weight")

hist.ungrouped(fans$cfm, main="Ungrouped Histogram",xlab="CFM")
hist.grouped(castings$weight, main="Grouped Histogram: Castings",xlab="Weight")
