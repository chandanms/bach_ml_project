# plotting the histograms (easier than Python)
setwd("~/Documents/Master/Blok 2/Machine learning")

library(readr)
library(dplyr)
library(tidyverse)

# Load and modify data
U <- read_table2("F.csv")
colnames(U) <- c("S", "A", "T", "B")
S <- U$S[U$S>0]
A <- U$A[U$A>0]
T <- U$T[U$T>0]
B <- U$B[U$B>0]

# Histogram of pitches without note length
library(rle)

S.wn<-rle(S)$values
hist(S.wn, main = "Soprano without note lengths", xlab = "Pitch", freq = F) 
lines(density(S.wn), col="red") # empirical density line
xfit.S.wn <- seq(min(S.wn), max(S.wn), length = length(S.wn)) # normal density line 
lines(xfit.S.wn, dnorm(xfit.S.wn, mean(S.wn), sd(S.wn)), col="blue")
legend("topright", c("emp distr.", "normal distr."), fill=c("red", "blue"))

A.wn<-rle(A)$values
hist(A.wn, main = "Alto without note lengths", xlab = "Pitch", freq = F)
lines(density(A.wn), col="red")
xfit.A.wn <- seq(min(A.wn), max(A.wn), length = length(A.wn))
lines(xfit.A.wn, dnorm(xfit.A.wn, mean(A.wn), sd(A.wn)), col="blue")
legend("topright", c("emp distr.", "normal distr."), fill=c("red", "blue"))

T.wn <- rle(T)$values
hist(T.wn, main = "Tenor without note lengths", xlab = "Pitch", freq = F)
lines(density(T.wn), col="red")
xfit.T.wn <- seq(min(T.wn), max(T.wn), length = length(T.wn))
lines(xfit.T.wn, dnorm(xfit.T.wn, mean(T.wn), sd(T.wn)), col="blue")
legend("topright", c("emp distr.", "normal distr."), fill=c("red", "blue"))

B.wn <- rle(B)$values
hist(B.wn, main = "Bass without note lengths", xlab = "Pitch", freq = F, ylim = c(0,0.09))
lines(density(B.wn), col="red")
xfit.B.wn <- seq(min(B.wn), max(B.wn), length = length(B.wn))
lines(xfit.B.wn, dnorm(xfit.B.wn, mean(B.wn), sd(B.wn)), col="blue")
legend("topright", c("emp distr.", "normal distr."), fill=c("red", "blue"))

# Histogram of note lengths seem roughly Poisson distributed
library(MASS)
S.d <- rle(S)$lengths
hist(S.d, freq = F, main = 'Duration of soprano')
lines(density(S.d), col="red")
xfit.S.d <- seq(min(S.d), max(S.d)) # normal density line 
lines(xfit.S.d, dpois(xfit.S.d, mean(S.d)), col="blue")
legend("topright", c("emp distr.", "Pois distr."), fill=c("red", "blue"))

A.d <- rle(A)$lengths
hist(A.d, freq = F, main = "Duration of alto", ylim = c(0,0.3))
lines(density(A.d), col="red")
xfit.A.d <- seq(min(A.d), max(A.d)) # normal density line 
lines(xfit.A.d, dpois(xfit.A.d, mean(A.d)), col="blue")
legend("topright", c("emp distr.", "Pois distr."), fill=c("red", "blue"))

T.d <- rle(T)$lengths
hist(T.d, freq = F, main = 'Duration of tenor', ylim = c(0,0.3))
lines(density(T.d), col="red")
xfit.T.d <- seq(min(T.d), max(T.d)) # normal density line 
lines(xfit.T.d, dpois(xfit.T.d, mean(T.d)), col="blue")
legend("topright", c("emp distr.", "Pois distr."), fill=c("red", "blue"))

B.d <- rle(B)$lengths
hist(B.d, freq = F, main = 'Duration of bass', ylim = c(0, 0.2))
lines(density(B.d), col="red")
xfit.B.d <- seq(min(B.d), max(B.d)) # normal density line 
lines(xfit.B.d, dpois(xfit.B.d, mean(B.d)), col="blue")
legend("topright", c("emp distr.", "Pois distr."), fill=c("red", "blue"))

lambda.S <- fitdistr(rle(S)$lengths, densfun = 'poisson')$estimate
sd.S <- fitdistr(rle(S)$lengths, densfun = 'poisson')$sd
lambda.A <- fitdistr(rle(A)$lengths, densfun = 'poisson')$estimate
sd.A <- fitdistr(rle(A)$lengths, densfun = 'poisson')$sd
lambda.T <- fitdistr(rle(T)$lengths, densfun = 'poisson')$estimate
sd.T <- fitdistr(rle(T)$lengths, densfun = 'poisson')$sd
lambda.B <- fitdistr(rle(B)$lengths, densfun = 'poisson')$estimate
sd.B <- fitdistr(rle(B)$lengths, densfun = 'poisson')$sd
df.pois<-matrix(data = c(lambda.A, lambda.B, lambda.S, lambda.T, sd.A, sd.B, sd.S, sd.T), ncol = 2)
colnames(df.pois) <- c('lambda', 'sd')
rownames(df.pois) <- c('A', 'B', 'S', 'T')

# Whether rest or not is Bernouilli distributed
p.A <- rle(U$A)
p.A <- length(rle(U$A)$values[p.A$values == 0])/length(rle(U$A)$values)
p.B <- rle(U$B)
p.B <- length(rle(U$B)$values[p.B$values == 0])/length(rle(U$B)$values)
p.S <- rle(U$S)
p.S <- length(rle(U$S)$values[p.S$values == 0])/length(rle(U$S)$values)
p.T <- rle(U$T)
p.T <- length(rle(U$T)$values[p.T$values == 0])/length(rle(U$T)$values)
A.zeros <- rle(U$A)
A.zeros <- A.zeros$length[A.zeros$values == 0]
B.zeros <- rle(U$B)
B.zeros <- B.zeros$length[B.zeros$values == 0]
S.zeros <- rle(U$S)
S.zeros <- S.zeros$length[S.zeros$values == 0]
T.zeros <- rle(U$T)
T.zeros <- T.zeros$length[T.zeros$values == 0]


