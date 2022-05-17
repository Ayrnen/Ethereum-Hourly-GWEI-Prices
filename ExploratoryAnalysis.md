Exploratory Data Analysis
================
Aymen Belakhoua
5/10/2022

# Final Report

## GWEI Prices over Time

------------------------------------------------------------------------

## Import Necessary Packages

``` r
library(ggplot2)
library(dplyr)
library(tidyverse)
library(ggpubr)
```

## Read CSV

    ##                     datetime safeLow average fast fastest
    ## 1 2021-06-17 00:27:51.975508    15.3    15.3   16      21
    ## 2 2021-06-17 17:02:53.047725    17.0    17.0   38      40
    ## 3 2021-06-17 17:02:54.629253    17.0    17.0   38      40
    ## 4 2021-06-17 18:02:55.955438    13.0    13.0   28      29
    ## 5 2021-06-17 19:02:28.719364     1.0     1.0   27      29

## Change Datetime to Hour

``` r
df$datetime <- format(as.POSIXct(df$datetime,
                                 format="%Y-%m-%d %H:%M:%S",
                                 tz="UTC"),
                      format = "%H")
names(df)[names(df)== 'datetime'] <- "hour"
df <- rename_with(df, toupper)
head(df, 5)
```

    ##   HOUR SAFELOW AVERAGE FAST FASTEST
    ## 1   00    15.3    15.3   16      21
    ## 2   17    17.0    17.0   38      40
    ## 3   17    17.0    17.0   38      40
    ## 4   18    13.0    13.0   28      29
    ## 5   19     1.0     1.0   27      29

------------------------------------------------------------------------

## Plot Density Plot

``` r
ggplot(df, aes(x=AVERAGE)) + 
  geom_histogram(aes(y=..density..), colour="blue", fill="white", binwidth = 10)+
  geom_density(alpha=.2, fill="#FF6666") +
  xlim(c(0,200)) + 
  xlab("Average") +
  ylab("Density")
```

![](ExploratoryAnalysis_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

The histogram is right skewed, meaning the user will pay more than the
mode (most common) price on average.

------------------------------------------------------------------------

### Get Mean Median Mode and Standard Deviation of “Average” Gas Price.

``` r
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}
```

The calculations for the ‘Average’ Speed’s cost for the entire data set
are as follows-

-   Mean: 71

-   Median: 60

-   Mode: 30

-   STD: 51

``` r
df2 <- read.csv('GasGot.csv')
df2$datetime <- as.POSIXct(df2$datetime,
                                 format="%Y-%m-%d %H:%M:%S",
                                 tz="UTC")

#df2$datetime <- as.numeric(df2$datetime)
cor(x=as.numeric(df2$datetime), y=df2$average,  method = "pearson", use = "complete.obs")
```

    ## [1] 0.1617592

``` r
ggscatter(df2, x = 'datetime', y = 'average', 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Date", ylab = "Average Cost\nGWEI")
```

![](ExploratoryAnalysis_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

The trend line is sloped upwards, however there is a very low linear
correlation (.161) so this is not indicative of much.”)

------------------------------------------------------------------------

## Hourly STD Calculations and Visualization

``` r
hours = c()
std = c()
for (i in 0:23){
  hours <- c(hours, i)
  df2 <- filter(df, as.integer(HOUR) == i)
  deviation = sd(df2$AVERAGE)
  std <- c(std, deviation)
}
dfSTD <- data.frame(hours, std)
head(dfSTD)
```

    ##   hours      std
    ## 1     0 54.22553
    ## 2     1 54.91158
    ## 3     2 47.72470
    ## 4     3 45.41740
    ## 5     4 48.70654
    ## 6     5 45.23710

``` r
ggplot(dfSTD, aes(x = hours, y= std)) + geom_point() +
  geom_hline(yintercept = mean(std))
```

![](ExploratoryAnalysis_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

Average STD: 49

There is a significantly high deviation in GWEI Price.

------------------------------------------------------------------------

### Average GWEI Price Boxplot plotted hourly, ordered by median value, with outliers removed.

``` r
ggplot(df, aes(x=reorder(HOUR, AVERAGE), y=AVERAGE)) +
  geom_boxplot(outlier.shape = NA) +
  labs(y="Average Speed\n(GWEI)", x="Hour", 
       title="Boxplot: Hours Sorted by Mean") +
  ylim(0,250)
```

![](ExploratoryAnalysis_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

------------------------------------------------------------------------

## Hourly Linear Correlation

``` r
df$HOUR <- factor(df$HOUR)

averages <- c()
hours <-c()
for (hour in unique(df$HOUR)){
  hours <- append(hours, hour)
  averages <- append(x=averages,
                     value = mean(df[df$HOUR == hour,'AVERAGE']))
}
df3 <- list(average = averages, hours = hours)
df3 <- as.data.frame(df3)
df3 <- df3[order(averages),]

ggscatter(df3, x = "hours", y = 'average', 
          add = "reg.line", conf.int = TRUE, 
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "Hours", ylab = "Average")
```

![](ExploratoryAnalysis_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

### Correlation Test

``` r
cor.test(as.numeric(df3$hours), df3$average, method=c("pearson", "kendall", "spearman"))
```

    ## 
    ##  Pearson's product-moment correlation
    ## 
    ## data:  as.numeric(df3$hours) and df3$average
    ## t = 3.1074, df = 22, p-value = 0.005135
    ## alternative hypothesis: true correlation is not equal to 0
    ## 95 percent confidence interval:
    ##  0.1915805 0.7815636
    ## sample estimates:
    ##       cor 
    ## 0.5522943

With a correlation coefficient of \>.5 the model indicates that there is
a significant linear association.

------------------------------------------------------------------------

## Hourly Linear Regression

``` r
model <- lm(as.numeric(average)~as.numeric(hours), df3)
summary(model)
```

    ## 
    ## Call:
    ## lm(formula = as.numeric(average) ~ as.numeric(hours), data = df3)
    ## 
    ## Residuals:
    ##     Min      1Q  Median      3Q     Max 
    ## -17.871  -7.635   2.038   8.145  14.705 
    ## 
    ## Coefficients:
    ##                   Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)        60.2837     4.0420  14.914 5.51e-13 ***
    ## as.numeric(hours)   0.9357     0.3011   3.107  0.00514 ** 
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 10.21 on 22 degrees of freedom
    ## Multiple R-squared:  0.305,  Adjusted R-squared:  0.2734 
    ## F-statistic: 9.656 on 1 and 22 DF,  p-value: 0.005135

With an adjusted R-Squared of **.2734** we can see that the hour of the
day has a weak effect (low correlation) on the GWEI cost.

With a p value of **.0051** we can confidently reject the null
hypothesis.
