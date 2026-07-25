# Final Results Report

## 1. Project Objective

The objective of this project is to develop and evaluate machine-learning models for predicting crop yield, measured in quintals per acre. The analysis compares models trained using:

1. The original predictor set.
2. The original predictors combined with engineered features.

Multiple Linear Regression was used as the baseline model, while Random Forest and XGBoost were selected as advanced nonlinear models. The project also includes an impact analysis to examine the relationships learned by the fitted models.

---

## 2. Dataset

### 2.1 Dataset Size

- Raw dataset: 1,000 observations and 8 variables
- Cleaned dataset: 999 observations and 8 variables
- Target variable: crop yield (`yield`), measured in quintals per acre

One observation was removed during data cleaning. All final models were trained and evaluated using the cleaned dataset to ensure consistency.

### 2.2 Original Predictors

The original predictor set contains:

- Crop type
- Rainfall
- Temperature
- Fertilizer
- Nitrogen
- Phosphorus
- Potassium

### 2.3 Engineered Predictors

The following engineered predictors were considered:

- Total NPK
- Nitrogen proportion
- Phosphorus proportion
- Temperature squared
- Rainfall–fertilizer interaction

The engineered Random Forest therefore combines the seven original predictors with five engineered variables.

---

## 3. Data Consistency and Train-Test Split

The cleaned dataset was divided into:

- 80% training data
- 20% testing data
- Random seed: 42

Although the raw and cleaned datasets differed by only one observation, applying `train_test_split` separately produced substantially different test samples. Only 84 of the 200 test observations were shared between the two splits, representing a 42% overlap.

Therefore, results produced from the raw 1,000-row dataset are not directly comparable with results produced from the cleaned 999-row dataset. All final models use the cleaned dataset and the same train-test split.

---

## 4. Exploratory Data Analysis

### 4.1 Yield Distribution

Crop yield was approximately symmetrically distributed, with:

- Mean: 9.86
- Median: 9.90
- Skewness: 0.059
- Minimum: 5.00
- Maximum: 15.00

No apparent yield outliers were identified using the 1.5 × IQR rule.

### 4.2 Crop-Type Differences

Yield distributions overlapped substantially across the six crop types.

A one-way ANOVA found no statistically significant difference in mean yield across crop categories:

**F(5, 993) = 0.6494, p = 0.6621**

The eta-squared effect size was:

**η² = 0.0033**

This indicates that crop type explained approximately 0.33% of the total variation in crop yield.

Levene’s test showed no evidence of unequal variances across crop types:

- Levene statistic: 0.7264
- p = 0.6037

### 4.3 Crop Representation

The crop categories were reasonably balanced. The number of observations ranged from 156 for corn to 174 for sorghum. No substantial imbalance was identified.

### 4.4 Rainfall

Rainfall showed a statistically significant but weak positive association with crop yield:

- Pearson correlation: r = 0.1027, p = 0.0012
- Spearman correlation: ρ = 0.1065, p = 0.0007

Rainfall alone explained approximately 1.05% of the variation in yield.

### 4.5 Temperature

Temperature showed a weak negative relationship with yield. The LOWESS curve suggested mild nonlinearity, with yield declining more noticeably at higher temperatures.

A quadratic temperature model fitted slightly better than a linear model:

<table>
  <thead>
    <tr>
      <th>Statistic</th>
      <th align="right">Linear model</th>
      <th align="right">Quadratic model</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>R²</td>
      <td align="right">0.0171</td>
      <td align="right">0.0225</td>
    </tr>
    <tr>
      <td>AIC</td>
      <td align="right">4881.16</td>
      <td align="right">4877.57</td>
    </tr>
  </tbody>
</table>

The squared temperature term was statistically significant:

**p = 0.0183**

This supported the inclusion of temperature squared during feature engineering. However, temperature alone still explained only a small proportion of yield variation.

### 4.6 Fertilizer

Fertilizer showed a very weak and statistically non-significant standalone relationship with yield:

- Pearson correlation: r = 0.0527, p = 0.0960
- Spearman correlation: ρ = 0.0530, p = 0.0944

This supported investigating whether fertilizer became more informative when considered jointly with rainfall.

### 4.7 Nitrogen, Phosphorus and Potassium

The individual nutrient variables showed negligible and statistically non-significant associations with yield.

<table>
  <thead>
    <tr>
      <th>Nutrient</th>
      <th align="right">Pearson correlation</th>
      <th align="right">Pearson p-value</th>
      <th align="right">Spearman correlation</th>
      <th align="right">Spearman p-value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Nitrogen</td>
      <td align="right">0.0127</td>
      <td align="right">0.6884</td>
      <td align="right">0.0112</td>
      <td align="right">0.7247</td>
    </tr>
    <tr>
      <td>Phosphorus</td>
      <td align="right">0.0221</td>
      <td align="right">0.4858</td>
      <td align="right">0.0244</td>
      <td align="right">0.4419</td>
    </tr>
    <tr>
      <td>Potassium</td>
      <td align="right">-0.0022</td>
      <td align="right">0.9441</td>
      <td align="right">-0.0006</td>
      <td align="right">0.9842</td>
    </tr>
  </tbody>
</table>

These results motivated testing whether total nutrient quantity and nutrient composition were more informative than the individual nutrient values.

### 4.8 Multicollinearity

The original numerical predictors had low pairwise correlations, indicating no serious multicollinearity in the original feature set.

Initial polynomial, interaction and composite variables introduced mathematical relationships with the original predictors. In particular, temperature squared was highly correlated with temperature, while the rainfall–fertilizer interaction was strongly related to rainfall.

Centering the relevant variables before constructing the engineered terms reduced this multicollinearity.

### 4.9 Outliers

The box plots for rainfall, temperature, fertilizer, nitrogen, phosphorus, potassium and yield showed no apparent extreme outliers. No additional outlier treatment was required.

---

## 5. Feature Engineering

The engineered feature set was designed to represent nutrient composition, nonlinear temperature behaviour and the interaction between rainfall and fertilizer.

### 5.1 Total NPK

**Total NPK = N + P + K**

This represents the total quantity of the three recorded macronutrients.

### 5.2 Nutrient Proportions

**Nitrogen proportion = N / (N + P + K)**

**Phosphorus proportion = P / (N + P + K)**

These variables represent nutrient composition rather than only the absolute nutrient quantities.

### 5.3 Temperature Squared

The squared temperature term was included to represent the mild curvature observed during exploratory analysis.

### 5.4 Rainfall–Fertilizer Interaction

The rainfall–fertilizer interaction was included to represent the possibility that the relationship between fertilizer and crop yield depends on rainfall conditions.

---

## 6. Modelling Setup

### 6.1 Models

The following models were considered:

- Multiple Linear Regression
- Random Forest Regressor
- XGBoost Regressor

### 6.2 Feature Sets

Each model was evaluated using:

- Original features
- Original and engineered features

### 6.3 Validation Strategy

The following validation procedures were used:

- A 20% hold-out test set for final evaluation
- Five-fold cross-validation
- Shuffled cross-validation folds
- Random seed of 42

For Random Forest, `GridSearchCV` was used to select hyperparameters based on negative root mean squared error. The pipeline applied one-hot encoding to crop type and passed the numerical predictors directly to the model.

The Random Forest hyperparameter grid considered:

<table>
  <thead>
    <tr>
      <th>Hyperparameter</th>
      <th>Values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Number of trees</td>
      <td>100, 200</td>
    </tr>
    <tr>
      <td>Maximum tree depth</td>
      <td>5, 10, None</td>
    </tr>
    <tr>
      <td>Minimum observations per leaf</td>
      <td>1, 2</td>
    </tr>
    <tr>
      <td>Features considered per split</td>
      <td>Square root</td>
    </tr>
  </tbody>
</table>

The grid therefore evaluated 12 hyperparameter combinations using five-fold cross-validation.

### 6.4 Evaluation Metrics

Model performance was evaluated using:

- Mean Absolute Error
- Root Mean Squared Error
- R-squared

Lower MAE and RMSE values indicate better predictive accuracy. Higher R² values indicate that the model explains a greater proportion of variation in crop yield.

A negative test R² means that the model performed worse than predicting the average test-set yield for every observation.

---

## 7. Model Results

### 7.1 Model Comparison

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>Feature Set</th>
      <th align="right">Test MAE</th>
      <th align="right">Test RMSE</th>
      <th align="right">Test R²</th>
      <th align="right">Five-Fold CV RMSE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Multiple Linear Regression</td>
      <td>Original</td>
      <td align="right">2.5342</td>
      <td align="right">2.9391</td>
      <td align="right">-0.0026</td>
      <td align="right">2.7926</td>
    </tr>
    <tr>
      <td>Multiple Linear Regression</td>
      <td>Engineered</td>
      <td align="right">2.5525</td>
      <td align="right">2.9453</td>
      <td align="right">-0.0068</td>
      <td align="right">2.7892</td>
    </tr>
    <tr>
      <td>Random Forest</td>
      <td>Original</td>
      <td align="right">2.546</td>
      <td align="right">2.939</td>
      <td align="right">-0.003</td>
      <td align="right">2.762 ± 0.136</td>
    </tr>
    <tr>
      <td><strong>Random Forest</strong></td>
      <td><strong>Engineered</strong></td>
      <td align="right"><strong>2.525</strong></td>
      <td align="right"><strong>2.926</strong></td>
      <td align="right"><strong>0.006</strong></td>
      <td align="right"><strong>2.762 ± 0.125</strong></td>
    </tr>
    <tr>
      <td>XGBoost</td>
      <td>Original</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
    </tr>
    <tr>
      <td>XGBoost</td>
      <td>Engineered</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
      <td align="right">Pending</td>
    </tr>
  </tbody>
</table>

> **Note:** XGBoost results will be added after model training and evaluation are completed.

For the linear models, additional five-fold cross-validation results were:

<table>
  <thead>
    <tr>
      <th>Feature Set</th>
      <th align="right">CV MAE</th>
      <th align="right">CV RMSE</th>
      <th align="right">CV R²</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Original</td>
      <td align="right">2.3841</td>
      <td align="right">2.7926</td>
      <td align="right">0.0014</td>
    </tr>
    <tr>
      <td>Engineered</td>
      <td align="right">2.3780</td>
      <td align="right">2.7892</td>
      <td align="right">0.0039</td>
    </tr>
  </tbody>
</table>

---

## 8. Multiple Linear Regression Results

### 8.1 Original Features

The original-feature Multiple Linear Regression model achieved:

- Test MAE: 2.5342
- Test RMSE: 2.9391
- Test R²: -0.0026
- Five-fold CV RMSE: 2.7926
- Five-fold CV R²: 0.0014

The test R² was slightly negative, showing that the model did not outperform a mean-yield prediction on the hold-out test set.

### 8.2 Engineered Features

The engineered linear model achieved:

- Test MAE: 2.5525
- Test RMSE: 2.9453
- Test R²: -0.0068
- Five-fold CV RMSE: 2.7892
- Five-fold CV R²: 0.0039

The engineered model produced slightly better average cross-validation results but performed marginally worse on the held-out test set.

The differences between the original and engineered models were too small to indicate a meaningful improvement. The original-feature model was therefore retained as the simpler linear baseline.

---

## 9. Random Forest Results

### 9.1 Original Feature Set

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th align="right">Train</th>
      <th align="right">Test</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MAE</td>
      <td align="right">2.113</td>
      <td align="right">2.546</td>
    </tr>
    <tr>
      <td>RMSE</td>
      <td align="right">2.491</td>
      <td align="right">2.939</td>
    </tr>
    <tr>
      <td>R²</td>
      <td align="right">0.190</td>
      <td align="right">-0.003</td>
    </tr>
  </tbody>
</table>

Five-fold cross-validation RMSE: **2.762 ± 0.136**

The model explained approximately 19% of the variation in the training data but failed to generalise to the test data. The negative test R² indicates performance marginally worse than the mean-prediction benchmark.

### 9.2 Engineered Feature Set

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th align="right">Train</th>
      <th align="right">Test</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MAE</td>
      <td align="right">2.093</td>
      <td align="right">2.525</td>
    </tr>
    <tr>
      <td>RMSE</td>
      <td align="right">2.480</td>
      <td align="right">2.926</td>
    </tr>
    <tr>
      <td>R²</td>
      <td align="right">0.197</td>
      <td align="right">0.006</td>
    </tr>
  </tbody>
</table>

Five-fold cross-validation RMSE: **2.762 ± 0.125**

The engineered Random Forest produced the strongest held-out results among the completed models.

Compared with the original-feature Random Forest:

- Test MAE decreased from 2.546 to 2.525
- Test RMSE decreased from 2.939 to 2.926
- Test R² increased from -0.003 to 0.006
- Cross-validation RMSE remained 2.762
- Cross-validation variability decreased from 0.136 to 0.125

However, these changes are negligible in practical terms. A test R² of 0.006 means that the model explained only approximately 0.6% of the variation in unseen crop yields.

The engineered variables therefore did not produce a meaningful improvement in model generalisation.

---

## 10. Impact Analysis

The impact analysis combined:

- Impurity-based feature importance
- Permutation importance
- Partial dependence analysis
- Crop-type scenario analysis

The engineered Random Forest impact analysis examined the original predictors and engineered variables, including total NPK, nutrient proportions, temperature squared and the rainfall–fertilizer interaction.

### 10.1 Permutation Importance

For the original-feature Random Forest, rainfall and temperature had the largest positive permutation importance values.

This means that randomly shuffling either variable produced the largest increase in test RMSE relative to the other predictors. They were therefore the most useful variables within the fitted model.

Phosphorus showed a small but uncertain positive contribution. Nitrogen and fertilizer had importance values close to zero.

Potassium and crop type produced negative mean permutation importance values, suggesting that they did not improve test-set generalisation and may have introduced noise or instability.

These findings do not mean that rainfall and temperature were strong predictors in absolute terms. They were only more useful relative to the remaining available variables.

### 10.2 Partial Dependence Analysis

Partial dependence plots were used to examine how the Random Forest’s average predicted yield changed across different values of each numerical predictor.

The engineered-feature analysis included partial dependence plots for:

- Rainfall
- Temperature
- Fertilizer
- Nitrogen
- Phosphorus
- Potassium
- Total NPK
- Nitrogen proportion
- Phosphorus proportion
- Temperature squared
- Rainfall–fertilizer interaction

These plots illustrate patterns learned by the fitted Random Forest. They do not establish that changing a predictor would cause a corresponding change in actual crop yield.

### 10.3 Crop-Type Analysis

Crop-type impact was assessed by assigning each crop category to all test observations in turn while keeping the remaining predictors unchanged.

The resulting average predicted yields differed only slightly across crop types. This agrees with the exploratory analysis, which found substantial overlap in yield distributions and a negligible crop-type effect size.

The crop-type scenario analysis describes model-based associations and should not be interpreted as a causal comparison between crops.

### 10.4 Impact Analysis Interpretation

The impact analysis suggests that rainfall and temperature were the most useful original predictors relative to the other available variables.

However:

- Their absolute predictive contribution remained small.
- Most permutation-importance error bars crossed or approached zero.
- Crop type contributed little.
- Several nutrient variables showed weak or unstable contributions.
- The overall model explained almost none of the variation in unseen yields.

Therefore, the impact-analysis results should be treated as descriptions of model behaviour rather than reliable agronomic conclusions.

---

## 11. Current Model Selection

### 11.1 Best Completed Model

The current best completed model is:

**Random Forest with engineered features**

Its performance was:

- Test MAE: 2.525
- Test RMSE: 2.926
- Test R²: 0.006
- Five-fold CV RMSE: 2.762 ± 0.125

### 11.2 Selection Interpretation

The engineered Random Forest currently has the lowest test MAE and RMSE and the highest test R² among the completed models.

However, it should not yet be described as a strong predictive model because:

- Its test R² remains close to zero.
- It explains less than 1% of unseen yield variation.
- Its improvement over the other models is extremely small.
- Its cross-validation RMSE is identical to that of the original-feature Random Forest.
- The training and test performance gap indicates that some learned patterns did not generalise.

Final model selection remains pending completion of the XGBoost evaluation.

---

## 12. Overall Interpretation

The completed results show that neither linear nor nonlinear models extracted substantial predictive information from the available variables.

Multiple Linear Regression performed poorly because the relationships between the available predictors and yield were weak.

Random Forest captured more variation in the training data, but this did not translate into meaningful test performance. This shows that the poor results were not simply caused by the restrictive assumptions of a linear model.

Feature engineering was supported by exploratory analysis and domain reasoning. However, mathematically transforming the existing predictors could not introduce important agronomic information that was absent from the dataset.

Rainfall and temperature were the most useful variables relative to the others, but their contributions remained weak. Crop type, fertilizer and the nutrient variables provided little stable predictive value.

The main constraint therefore appears to be limited information in the available predictors rather than the choice between linear and nonlinear algorithms.

---

## 13. Key Findings

1. Most original predictors had weak standalone relationships with crop yield.
2. Crop type explained only approximately 0.33% of total yield variation and did not significantly distinguish mean yield across crop categories.
3. Rainfall had a statistically significant but weak positive association with yield.
4. Temperature showed a weak negative and mildly nonlinear relationship with yield.
5. Multiple Linear Regression produced test and cross-validation R² values close to zero.
6. The original-feature Random Forest explained approximately 19% of training variation but produced a negative test R².
7. The engineered Random Forest produced the strongest completed test results, with a test MAE of 2.525, RMSE of 2.926 and R² of 0.006.
8. The improvement produced by the engineered Random Forest was negligible and did not indicate meaningful generalisation.
9. Feature engineering did not overcome the weak predictive signal in the dataset.
10. Rainfall and temperature were the most useful predictors relative to the other variables, although neither was strongly predictive.
11. Both linear and nonlinear models indicate that important explanatory variables are missing.
12. None of the completed models is currently strong enough to support reliable agronomic decisions.

---

## 14. Recommendations

1. Complete the XGBoost evaluation using the same cleaned dataset, split and validation strategy.
2. Compare the final models with a dummy mean regressor to establish whether they provide a meaningful predictive improvement.
3. Collect additional agronomic predictors, including:
   - Soil type
   - Soil pH
   - Soil moisture
   - Organic matter
   - Irrigation practices
   - Crop variety
   - Planting date
   - Harvesting date
   - Pest and disease pressure
   - Farm-management practices
4. Include reliable geographic identifiers such as latitude, longitude, district or region.
5. Include temporal identifiers such as year, month, season and planting cycle.
6. Integrate external climate, soil and remote-sensing data only when observations can be matched reliably using geographic and temporal identifiers.
7. Evaluate errors separately by crop type to determine whether model performance differs across crop categories.
8. Use larger and more informative datasets when investigating nonlinear relationships and interactions.
9. Treat the current Streamlit application as a technical prototype rather than a validated decision-support system.
10. Avoid presenting permutation importance or partial dependence as evidence of causal agronomic effects.

---

## 15. Limitations

1. The available predictors explained only a small proportion of crop-yield variation.
2. Important agronomic, spatial, temporal and farm-management variables were absent.
3. External data could not be reliably merged because geographic and temporal identifiers were unavailable.
4. The cleaned dataset contains only 999 observations, limiting the ability of flexible models to learn stable complex relationships.
5. Some statistically significant relationships had very small effect sizes and limited practical importance.
6. The engineered variables were derived from the existing predictors and could not introduce information absent from the original dataset.
7. Polynomial, composite and interaction features introduced mathematical dependence that required additional multicollinearity control.
8. Permutation importance and partial dependence describe fitted model behaviour rather than causal effects.
9. The hold-out result was sensitive to the composition of the test sample.
10. The model should not be assumed to generalise to farms, regions, seasons or crop varieties not represented in the supplied data.

---

## 16. Deployment

- Deployment platform: Streamlit
- Streamlit link: pending
- GitHub repository: [Gamma 2 Crop Yield Prediction](https://github.com/Ronkecrown/gamma2-crop-yield-prediction)
- Current deployment status: prototype only

The deployed pipeline should include:

- Input validation
- Categorical encoding
- Required numerical preprocessing
- Feature engineering
- Fitted final model
- Crop-yield prediction output
- Clear measurement units
- Error handling
- A disclaimer describing the model’s limited validated predictive performance

The model should only be presented as production-ready if the final evaluation demonstrates adequate absolute accuracy, stable cross-validation performance and meaningful improvement over the mean-prediction baseline.

---

## 17. Supporting Files

The report can be linked to the saved project outputs using relative paths such as:

- [`tables/rf_original_results.csv`](tables/rf_original_results.csv)
- [`tables/rf_engineered_results.csv`](tables/rf_engineered_results.csv)
- [`tables/rf_original_cv_results.csv`](tables/rf_original_cv_results.csv)
- [`tables/rf_engineered_cv_results.csv`](tables/rf_engineered_cv_results.csv)
- [`figures/rf_original_permutation_importance.png`](figures/rf_original_permutation_importance.png)
- [`figures/rf_engineered_permutation_importance.png`](figures/rf_engineered_permutation_importance.png)

Additional partial dependence and crop-type impact figures may be linked from the `reports/figures/` directory.
