# Final Results Summary

## Dataset
- Raw dataset size: 1,000 observations and 8 variables
- Cleaned dataset size: 999 observations
- Target variable: Crop yield (`yield`), measured in quintals per acre
- Original predictors:
  - Crop type
  - Rainfall
  - Temperature
  - Fertiliser
  - Nitrogen
  - Phosphorus
  - Potassium
- Engineered predictors considered:
  - Total NPK
  - Nitrogen proportion
  - Phosphorus proportion
  - Temperature squared
  - Rainfall–fertiliser interaction

## Modelling Setup
- Train-test split: 80% training and 20% testing
- Random seed: 42
- Baseline model: Multiple Linear Regression
- Advanced models:
  - Random Forest Regressor
  - XGBoost Regressor
- Feature sets compared:
  - Original features
  - Engineered features
- Cross-validation strategy: 5-fold cross-validation with shuffled folds and random seed 42
- Evaluation metrics:
  - Mean Absolute Error
  - Root Mean Squared Error
  - R-squared

## Model Comparison

| Model | Feature Set | Test MAE | Test RMSE | Test R² | CV MAE | CV RMSE | CV R² |
|---|---|---:|---:|---:|---:|---:|---:|
| Multiple Linear Regression | Original | 2.5342 | 2.9391 | -0.0026 | 2.3841 | 2.7926 | 0.0014 |
| Multiple Linear Regression | Engineered | 2.5525 | 2.9453 | -0.0068 | 2.3780 | 2.7892 | 0.0039 |
| Random Forest | Original | Pending | Pending | Pending | Pending | Pending | Pending |
| Random Forest | Engineered | Pending | Pending | Pending | Pending | Pending | Pending |
| XGBoost | Original | Pending | Pending | Pending | Pending | Pending | Pending |
| XGBoost | Engineered | Pending | Pending | Pending | Pending | Pending | Pending |

### Baseline interpretation

The engineered linear model produced slightly better mean cross-validation results but performed marginally worse on the held-out test set. The differences were too small to indicate a meaningful improvement. The original feature model was therefore retained as the simpler linear baseline.

## Final Model
- Selected model: Pending completion of Random Forest and XGBoost evaluation
- Selected feature set: Pending
- Reason for selection:
  - Cross-validation performance
  - Held-out test performance
  - Stability across folds
  - Train-test performance gap
  - Interpretability
  - Suitability for deployment
- Final MAE: Pending
- Final RMSE: Pending
- Final R²: Pending

The final model should not be selected only because it performs better than Multiple Linear Regression. Its absolute performance, generalisation ability and cross-validation stability must also be considered.

## Exploratory Data Analysis

### Yield distribution
Crop yield was approximately symmetrically distributed, with a mean of 9.86, a median of 9.90 and a skewness of 0.059. Yield values ranged from 5.00 to 15.00, and no apparent yield outliers were identified using the 1.5 × IQR rule.

### Crop-type differences
Yield distributions overlapped substantially across crop types. A one-way ANOVA found no statistically significant difference in mean yield across the six crop categories:

- ANOVA: \(F(5,993) = 0.6494\), \(p = 0.6621\)
- Eta-squared: \(\eta^2 = 0.0033\)

Crop type explained only approximately 0.33% of total yield variation.

Levene’s test showed no evidence of unequal variances across crop types:

- Levene statistic: 0.7264
- \(p = 0.6037\)

### Crop representation
The crop categories were reasonably balanced, with observations ranging from 156 for corn to 174 for sorghum. No major imbalance was identified.

### Rainfall
Rainfall showed a statistically significant but weak positive relationship with yield:

- Pearson \(r = 0.1027\), \(p = 0.0012\)
- Spearman \(\rho = 0.1065\), \(p = 0.0007\)

Rainfall alone explained approximately 1.05% of yield variation.

### Temperature
Temperature showed a weak negative relationship with yield. The LOWESS curve suggested mild nonlinearity, with yield declining more noticeably at higher temperatures.

A quadratic temperature model fitted slightly better than a linear temperature model:

- Linear model \(R^2 = 0.0171\)
- Quadratic model \(R^2 = 0.0225\)
- Linear model AIC = 4881.16
- Quadratic model AIC = 4877.57
- Squared temperature term \(p = 0.0183\)

This provided justification for considering a nonlinear temperature term during feature engineering, although temperature alone still explained little yield variation.

### Fertiliser
Fertiliser showed a very weak and statistically non-significant standalone relationship with yield:

- Pearson \(r = 0.0527\), \(p = 0.0960\)
- Spearman \(\rho = 0.0530\), \(p = 0.0944\)

This supported exploring whether fertiliser becomes more informative when considered jointly with rainfall.

### Nitrogen, phosphorus and potassium
The individual nutrients showed negligible and statistically non-significant standalone associations with yield.

| Nutrient | Pearson correlation | Pearson p-value | Spearman correlation | Spearman p-value |
|---|---:|---:|---:|---:|
| Nitrogen | 0.0127 | 0.6884 | 0.0112 | 0.7247 |
| Phosphorus | 0.0221 | 0.4858 | 0.0244 | 0.4419 |
| Potassium | -0.0022 | 0.9441 | -0.0006 | 0.9842 |

These findings motivated testing whether total nutrient quantity and nutrient composition were more informative than the individual nutrient variables.

### Multicollinearity
The correlation heatmap showed low correlations among the original numerical predictors. No serious pairwise multicollinearity was identified in the original feature set.

Multicollinearity should be reassessed after feature engineering because polynomial, interaction and composite variables can be mathematically related to their original variables.

### Outliers
The box plots for rainfall, temperature, fertiliser, nitrogen, phosphorus, potassium and yield showed no apparent extreme outliers. No additional outlier treatment was required during EDA.

## Interpretation
- Top predictive factors:
  - To be confirmed using feature importance or SHAP values from the selected advanced model
  - Among individual EDA relationships, temperature and rainfall showed the largest associations with yield, although both were weak
- Main nonlinear relationships:
  - Temperature showed mild curvature, particularly at higher temperatures
  - Other nonlinear relationships will be assessed using Random Forest and XGBoost
- Crop-specific patterns:
  - Crop types showed substantial overlap in yield distributions
  - Crop type had a negligible effect size and did not significantly explain yield differences
- Overall data signal:
  - Most predictors had weak standalone relationships with yield
  - The linear models explained almost none of the variation in the held-out data
  - Advanced models will determine whether useful nonlinear patterns or interactions remain

## Key Findings
1. Most original predictors had weak standalone relationships with crop yield, and crop type explained only approximately 0.33% of yield variation.
2. Multiple Linear Regression substantially underfit the data, with test and cross-validation \(R^2\) values close to zero.
3. Feature engineering was supported by EDA and domain reasoning, but it did not meaningfully improve the linear baseline.
4. Temperature showed mild nonlinear behaviour, while the weak standalone fertiliser relationship justified examining a rainfall–fertiliser interaction.
5. The advanced-model results will determine whether model simplicity or limited predictive information is the main constraint.

## Recommendations
1. Compare Random Forest and XGBoost using both the original and engineered feature sets under the same train-test split and cross-validation strategy.
2. Collect additional agronomic variables such as soil properties, irrigation, crop variety, planting season, geographical location, pest pressure and farm-management practices.
3. Add reliable geographic and temporal identifiers so external climate and soil data can be integrated accurately.
4. Evaluate model errors separately by crop type to determine whether performance varies across crops.
5. Deploy the model only if its absolute performance and generalisation ability are adequate, not merely because it performs better than the baseline.

## Limitations
1. The available predictors explained only a small proportion of crop-yield variation.
2. Important agronomic, spatial, temporal and management variables were absent from the supplied dataset.
3. External data could not be reliably merged at observation level because geographic and temporal identifiers were unavailable.
4. The dataset contains only 999 observations, which may limit the ability of flexible models to learn stable complex relationships.
5. Statistical significance in some relationships did not imply strong practical importance because the effect sizes were small.
6. The model should not be assumed to generalise to farms, regions or seasons not represented in the supplied data.

## Deployment
- Deployment platform: Streamlit
- Streamlit link: Pending
- GitHub repository: `https://github.com/Ronkecrown/gamma2-crop-yield-prediction`
- Deployed pipeline should include:
  - Feature engineering
  - Categorical encoding
  - Required numerical preprocessing
  - Fitted final model
  - Input validation
  - Yield prediction output