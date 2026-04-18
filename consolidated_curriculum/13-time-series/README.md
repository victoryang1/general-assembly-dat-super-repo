---
title: Time Series Analysis and Modeling
duration: "3:00"
creator:
    name: Arun Ahuja
    city: NYC
---

# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Time Series Analysis and Modeling
DS | Lesson 13

### LEARNING OBJECTIVES
*After this lesson, you will be able to:*
- Understand the properties of time series data: stationarity, autocorrelation, seasonality
- Identify and apply detrending and differencing techniques
- Model and predict from time series data using AR, ARMA, and ARIMA models
- Implement those models in `statsmodels`
- Evaluate time series model quality using residual analysis

### STUDENT PRE-WORK
*Before this lesson, you should already be able to:*
- Use pandas for data manipulation (especially datetime indexing)
- Understand the concept of moving averages and autocorrelation
- Apply linear regression with discussion of coefficients and residuals
- `pip install statsmodels` (included with Anaconda)

### INSTRUCTOR PREP
*Before this lesson, instructors will need to:*
- `pip install statsmodels` (included with Anaconda)
- Review the datasets in `assets/dataset/`
- Read through starter/solution code notebooks
- Copy and modify the lesson slide deck in `assets/slides/`

### LESSON GUIDE
| TIMING  | TYPE  | TOPIC  |
|:-:|---|---|
| 5 min   | [Opening](#opening)          | Lesson Objectives |
| 30 min  | [Introduction](#introduction) | Time Series Properties: Stationarity, Autocorrelation |
| 45 min  | [Introduction](#introduction2) | AR, MA, ARMA, and ARIMA Models |
| 75 min  | [Demo/Codealong](#demo1)     | Time Series Models in Statsmodels (Rossmann Sales) |
| 50 min  | [Independent Practice](#ind-practice) | Walmart Sales Data: Time Series Modeling |
| 5 min   | [Conclusion](#conclusion)    | Review & Recap |

---

## Resources

- [Demo Notebook](L13-Demo.ipynb)
- [Starter Code](code/starter-code/starter-code-13.ipynb)
- [Solution Code](code/solution-code/solution-code-13.ipynb)
- [Slides](assets/slides/slides-16.md)
- [Reference: Time Series Analysis (DS_HK_15)](reference/DS_HK_15_15-time-series-analysis.pdf)
- [Reference: Time Series Modeling (DS_HK_15)](reference/DS_HK_15_16-time-series-modeling.pdf)
- [Reference: Slides (DS-SF-36)](reference/DS-SF-36_slides-19-time-series.pdf)

---

<a name="opening"></a>
## Opening (5 min)

In this lesson we will advance time series exploration techniques to forecasting. If we have a sequence of values (a time series), we will use techniques in this class to predict a future value — for example, predicting the number of sales in a future month.

<a name="introduction"></a>
## Intro: Time Series Properties (30 min)

### Stationarity

Many time series models assume *stationarity* — that the mean and variance of values are constant throughout the series.

Real-world data is often non-stationary (e.g., stock prices, sales with seasonality). Two common methods to address this:

- **Detrending**: Fit a line to the trend, then model the residual difference.
- **Differencing**: Model the difference between consecutive values (the `diff` function in pandas). The ARIMA model incorporates this automatically.

### Autocorrelation

*Autocorrelation* measures how correlated a variable is with itself at prior time points. A high autocorrelation implies previous values are predictive of future values.

Use `pandas.tools.plotting.autocorrelation_plot` or `statsmodels.graphics.tsaplots.plot_acf` to visualize.

<a name="introduction2"></a>
## Intro: Time Series Models (45 min)

### AR Models (Autoregressive)

**AR(p)** models predict the next value from the previous *p* values. Similar to regression, but the inputs are the lagged outcome values.

    y_i = intercept + β₁·y_(i-1) + β₂·y_(i-2) + ... + βₚ·y_(i-p) + error

Useful for capturing gradual trends (slowly shifting demand, preferences).

### MA Models (Moving Average)

**MA(q)** models predict from the last *q* error terms (not lagged values). Useful for capturing sudden, abrupt changes (supply shocks, popularity spikes).

    y_i = mean + β₁·ε_(i-1) + ... + βq·ε_(i-q)

### ARMA Models

**ARMA(p, q)** combines both AR(p) and MA(q) to account for gradual changes and sudden shifts simultaneously.

### ARIMA Models

**ARIMA(p, d, q)** — AutoRegressive Integrated Moving Average — applies an ARMA(p, q) model to the *differenced* series (differentiated *d* times). This removes the need to manually detrend non-stationary data.

- `p` = order of the autoregressive component
- `d` = degree of differencing
- `q` = order of the moving average component

<a name="demo1"></a>
## Demo/Codealong: Time Series Models in statsmodels (75 min)

See [L13-Demo.ipynb](L13-Demo.ipynb) for the full walkthrough using the Rossmann pharmacy sales dataset.

Key steps:
1. Load and datetime-index the data
2. Filter to a single store; plot sales over time
3. Compute autocorrelation at multiple lags with `plot_acf`
4. Fit AR(1), AR(2), ARMA(1,1) models using `statsmodels.tsa.arima_model.ARMA`
5. Fit ARIMA(p, d, q) models and interpret `model.summary()`
6. Diagnose using residual plots and autocorrelation of residuals
7. Forecast with `model.plot_predict`

<a name="ind-practice"></a>
## Practice: Walmart Sales Data (50 min)

Use [code/starter-code/starter-code-13.ipynb](code/starter-code/starter-code-13.ipynb) with the Walmart weekly sales data (`assets/dataset/train.csv`).

1. Filter to Store 1 and aggregate total weekly sales across departments.
2. Plot the rolling mean — what general trends do you observe?
3. Compute autocorrelations at lags 1, 2, and 52 and create an autocorrelation plot.
4. What does the autocorrelation plot suggest about the best model type?
5. Split into training (75%) and test sets — keeping temporal order.
6. Fit an AR(1) model; compute mean absolute error on the test set.
7. Plot the residuals — where are the largest errors?
8. Fit AR(2) and ARMA(2, 2) models — does MAE improve?
9. Fit ARIMA models, iterating on p, d, q to minimize test error.

Solutions in [code/solution-code/solution-code-13.ipynb](code/solution-code/solution-code-13.ipynb).

<a name="conclusion"></a>
## Conclusion (5 min)

- Time series models use previous values (and errors) to forecast future values.
- AR models capture gradual shifts; MA models capture abrupt changes.
- ARMA combines both approaches.
- ARIMA adds differencing to handle non-stationary data automatically.
- Models perform poorly when data has strong seasonality not captured by p/q/d — consider Seasonal ARIMA (SARIMA) in those cases.

---

### ADDITIONAL RESOURCES
- [ARIMA model overview](https://www.quantstart.com/articles/Autoregressive-Integrated-Moving-Average-ARIMA-p-d-q-Models-for-Time-Series-Analysis)
- [Time Series Analysis in Python with statsmodels](http://conference.scipy.org/proceedings/scipy2011/pdfs/statsmodels.pdf)
- [Investopedia: Stationarity](http://www.investopedia.com/articles/trading/07/stationary.asp)
- [First Place Entry in Walmart Sales Prediction](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/forums/t/8125/first-place-entry)
- [Google Search Terms predict market movements](https://www.quantopian.com/posts/google-search-terms-predict-market-movements)

### VARIATIONS
This lesson consolidates content from multiple GA Data Science cohorts:
- **DAT-BOS-16 Lesson 15** (`variations/DAT-BOS-16_lesson-15/`): Time series analysis (exploration, moving averages, autocorrelation)
- **DAT-BOS-16 Lesson 16** (`variations/DAT-BOS-16_lesson-16/`): Time series modeling (AR, ARMA, ARIMA) — primary source for this lesson
- **DS_HK_15 Lesson 16** (`variations/DS_HK_15_lesson-16/`): Alternative version from Hong Kong cohort
- **DS-SF-36 Class 19** (`variations/DS-SF-36_class-19/`): San Francisco cohort notebooks and slides
