# Rescaled Range Analysis

Implementation of *Rescaled Range*, which is a statistical method that measures the variablity of a time series.

The method was used on Abbott's stock data (10 years).

The result is used to estimate the *Hurst* exponent, which measures a long-term memory of a time series.
Using the *Hurst* exponent, it's possible to classify the time series and get some insights into their dynamics.

## Interpreting the Hurst exponent (H)

* When H is **close to 0.5**, it's a *Brownian* time series.
* When H is **close to 0**, it's an *anti-persistent* time series.
* When H is **close to 1**, it's a *persistent* time series.

### Brownian time series
In a *Brownian* time series there is **no correlation** between the observations and a future observation;
being higher or lower than the current observation are equally likely

Series of this kind are hard to predict.

### Anti-persistent time series
In an *anti-persistent* time series an **increase** will most likely be **followed by** a **decrease** or **vice-versa**.

This means that the future value has a tendency to return to a long-term mean.

### Persistent time series
In an *persistent* time series an **increase** in values will most likely be **followed by** an **increase** in the **short term**
and a **decrease** will most likely be **followed by** a **decrease** in the **short term**.

# Hurst exponent of Abbott's stock data
The *Hurst* exponent estimated of Abbott's stock data, in the last 10 years, is 0.504, which means that Abbott's stock data
can be seen as a *Brownian* time series and it has no correlation between the observations and a future observation.

It is a difficult stock to predict.

