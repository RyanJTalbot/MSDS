# Startup Code
require(lolcat)
require(formattable)
ro<-round.object
nqtr<-function(x,d){noquote(t(round.object(x, d)))}
options(scipen=999)

# np Chart ----------------------------------------------------------------
np.Chart <- read.delim("G:/My Drive/Coursera/Course 2 - Methods for Quality Improvement - Stability and Capability/Module 5 - Control Charts for Discrete Data/np Chart.dat")
View(np.Chart)


# Create chart for Total nonconforming ------------------------------------
spc.np.chart<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.Chart$Total
                                                               ,sample.size = np.Chart$n
                                                               ,chart1.point.cex = 1.3
                                                               ,chart1.line.lwd=2
                                                               ,chart1.main = "np chart - Total Number of Defective Units")


# Exact Binomial Limits ---------------------------------------------------
(pbar<-unique(spc.np.chart$chart1.center.line)/5000)

ro(table.dist.binomial(n = 5000, p = pbar)[1:22,])


# Control Limits and Centerline -------------------------------------------
(np.UCL<-unique(spc.np.chart$chart1.control.limits.ucl))
(np.center<-unique(spc.np.chart$chart1.center.line))
(np.LCL<-unique(spc.np.chart$chart1.control.limits.lcl))


# Create chart for Scratches ----------------------------------------------
spc.np.scratches<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.Chart$Scratches
                                                                             ,sample.size = np.Chart$n
                                                                             ,chart1.point.cex = 1.3
                                                                             ,chart1.line.lwd=2
                                                                             ,chart1.main = "np chart - Number of Scratches")

# Control Limits and Centerline
(np.scratches.UCL<-unique(spc.np.scratches$chart1.control.limits.ucl))
(np.scratches.center<-unique(spc.np.scratches$chart1.center.line))
(np.scratches.LCL<-unique(spc.np.scratches$chart1.control.limits.lcl))


# Create chart for Warp ---------------------------------------------------
spc.np.warp<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.Chart$Warp
                                                                            ,sample.size = np.Chart$n
                                                                            ,chart1.point.cex = 1.3
                                                                            ,chart1.line.lwd=2
                                                                            ,chart1.main = "np chart - End to End Warp")
# Control Limits and Centerline
(np.warp.UCL<-unique(spc.np.warp$chart1.control.limits.ucl))
(np.warp.center<-unique(spc.np.warp$chart1.center.line))
(np.warp.LCL<-unique(spc.np.warp$chart1.control.limits.lcl))


# Create chart for Flatness -----------------------------------------------
spc.np.flatness<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.Chart$Flatness
                                                                            ,sample.size = np.Chart$n
                                                                            ,chart1.point.cex = 1.3
                                                                            ,chart1.line.lwd=2
                                                                            ,chart1.main = "np chart - Bar Flatness")
# Control Limits and Centerline
(np.flatness.UCL<-unique(spc.np.flatness$chart1.control.limits.ucl))
(np.flatness.center<-unique(spc.np.flatness$chart1.center.line))
(np.flatness.LCL<-unique(spc.np.flatness$chart1.control.limits.lcl))


# Control Charts by Set ---------------------------------------------------
# Split data by Set
np.set1<-subset(x = np.Chart, subset = np.Chart$Set==1)
np.set2<-subset(x = np.Chart, subset = np.Chart$Set==2)

# Total np Chart by Set
spc.np.set1<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Total, sample.size = np.set1$n)
spc.np.set2<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Total, sample.size = np.set2$n)

# Chart both side by side
par(mfrow=c(1,2))
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Total, sample.size = np.set1$n, chart1.ylim=c(0,30), combine.charts="leave.par.alone", chart1.main = "np Chart - Set 1")
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Total, sample.size = np.set2$n, chart1.ylim=c(0,30), combine.charts="leave.par.alone", chart1.main = "np Chart - Set 2")

# Scratches np Chart by Set
spc.np.scratch.set1<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Scratches, sample.size = np.set1$n)
spc.np.scratch.set2<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Scratches, sample.size = np.set2$n)

# Chart both side by side
par(mfrow=c(1,2))
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Scratches, sample.size = np.set1$n, chart1.ylim=c(0,25), combine.charts="leave.par.alone", chart1.main = "Scratches - Set 1")
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Scratches, sample.size = np.set2$n, chart1.ylim=c(0,25), combine.charts="leave.par.alone", chart1.main = "Scratches - Set 2")

# Warp np Chart by Set
spc.np.warp.set1<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Warp, sample.size = np.set1$n)
spc.np.warp.set2<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Warp, sample.size = np.set2$n)

# Chart both side by side
par(mfrow=c(1,2))
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Warp, sample.size = np.set1$n, chart1.ylim=c(0,6), combine.charts="leave.par.alone", chart1.main = "Warp - Set 1")
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Warp, sample.size = np.set2$n, chart1.ylim=c(0,6), combine.charts="leave.par.alone", chart1.main = "Warp - Set 2")

# Flatness np Chart by Set
spc.np.flatness.set1<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Flatness, sample.size = np.set1$n)
spc.np.flatness.set2<-spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Flatness, sample.size = np.set2$n)

# Chart both side by side
par(mfrow=c(1,2))
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set1$Flatness, sample.size = np.set1$n, chart1.ylim=c(0,10), combine.charts="leave.par.alone", chart1.main = "Flatness - Set 1")
spc.chart.attributes.proportion.np.binomialdistribution.simple(nonconforming = np.set2$Flatness, sample.size = np.set2$n, chart1.ylim=c(0,10), combine.charts="leave.par.alone", chart1.main = "Flatness - Set 2")




# With the Total Control Chart, what is the overall proportion nonconforming, p-bar?
(pbar<-unique(spc.np.set2$chart1.center.line)/5000)


# Capability --------------------------------------------------------------
# Get average proportion defective
(set2.center<-unique(spc.np.set2$chart1.center.line)/5000)

# Convert to Z Score
(Z<-qnorm(p = 0.001093333, lower.tail = F))

# Convert Z to Cpk_eq
(Cpk.eq<-Z/3)

# Create Pareto Chart -----------------------------------------------------
(Scratches<-sum(spc.np.scratch.set2$parameter.nonconforming))
(Flatness<-sum(spc.np.flatness.set2$parameter.nonconforming))
(Warp<-sum(spc.np.warp.set2$parameter.nonconforming))

Category<-c("Scratches", "Flatness","Warp")
Pareto<-as.data.frame(Category)
Pareto$Defects<-c(Scratches, Flatness, Warp)
View(Pareto)
Pareto$Cumsum<-cumsum(Pareto$Defects)
Pareto$Prob<-round(Pareto$Defects/sum(Pareto$Defects),3)
Pareto$CumProb<-cumsum(Pareto$Prob)
Pareto$Percent<-Pareto$CumProb*100


# Create Pareto Chart
graphics.off()
pareto<-barplot(height = Pareto$Defects, names.arg = Pareto$Category
                ,ylim = c(0, 1.05 * max(Pareto$Defects, na.rm = T))
                ,main = "Pareto Chart", col = "red")
par(new=T)

# Add cumulative counts line
plot(x = pareto, y = Pareto$Percent, type = "b", pch=19, xaxt = "n", yaxt = "n",
     ylab = "", xlab = "", lty = 1, xlim = extendrange(pareto, f = 0.2), ylim=c(0,100))

y2<-seq(0, 100, by = 25)
axis(side = 4, at = y2, ylim = c(0,100))
text(x = pareto+.1, y = Pareto$Percent-6, labels = paste(Pareto$Percent ,"%",sep=""))
