# Simple estimation of the future variance of a financial asset

Objective
---------
Show how to build features from high-frequency historical data (5-min frequency) and predict future variance.
This is an exercise, not a production-ready model.

Data
----
Instrument: Apple stock, with 5 min frequecy.

Processing:
- Resampled to hourly data
- Computed variance of log returns using the Parkinson method
- Created features (previous hour variance, daily variance, weekly variance)

Model used
----------
HAR Model (Corsi) implemented with Linear Regression (sklearn)

Steps:
- Train/test split
- Normalisation of features
- Evaluation tools: MSE&MAE

Comparison: Linear Regression vs Ridge on the same HAR features to assess coefficient stability via repeated resampling. Computed the mean and standard deviation of the coefficient distribution.


Difficulties
------------
1. EURUSD initially used: log-return variance too low for linear regression (G10 FX pairs too stable)
2. Data discontinuities: weekends and national holidays → introduced session_id
3. MLP attempt: completely overfitted due to highly correlated features, small dataset (6 months), low dimension. Literature (Medeiros 2010-2011) suggests adding exogenous features to improve HAR models.

Results
-------
Regression seems to understand clearly link between past and future variances.
Prediction performance:
- MSE = 1e-13
- Graph between prediction and true values follows the graph x=y

Coefficients are not stable enough. Coefficient stability:
- Standard deviations of the coefficients is about the same order as the mean (ratio between 0.25 and 0.9)
- Regularization L2 of Ridge did not improve significantly the standard deviations.
Explanation: variance of log returns is very low (1e-6) and the dataset is small. Ridge could be useful if we add more uncorrelated features