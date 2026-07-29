# Shared Methodology

## Problem Definition
The project is a supervised regression task aimed at predicting crop yield.

## Target Variable
- Yield

## Predictor Variables
- Rainfall
- Temperature
- Fertilizer
- Nitrogen
- Phosphorous
- Potassium
- Crop Type

## Model Strategy
- Baseline model: Multiple Linear Regression
- Advanced models: Random Forest Regressor and XGBoost Regressor

## Data Split
- Test size: 20%
- Random seed: 42

## Evaluation Metrics
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)

## Model Selection
The final model will be selected based on:
- Validation performance
- Test performance
- Generalisation
- Interpretability
- Stability
- Ease of deployment

## Shared Rules
- Use the same cleaned dataset.
- Use the same train-test split.
- Use the same random seed.
- Use the same evaluation metrics.
- Do not modify the raw dataset.
- Document every major preprocessing and modelling decision.