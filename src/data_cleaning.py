"""
===============================================================================
DATA CLEANING AND PREPROCESSING
===============================================================================
Project: Gamma 2 - Crop Yield Prediction
Author: Marina (Data Engineering Lead)
Role: Data Cleaning and Preprocessing
Date: 2024
===============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


# ===========================================================================
# 1. PATH CONFIGURATION
# ===========================================================================

# Get the project root (since script is in src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'Crop yield data.xlsx')
PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'data', 'reports')

# Create directories if they don't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

print("="*80)
print("🌾 DATA CLEANING AND PREPROCESSING")
print("   Gamma 2 - Crop Yield Prediction")
print("   Marina - Data Engineering Lead")
print("="*80)
print(f"\n📂 Project Root: {PROJECT_ROOT}")
print(f"📂 Input:  {RAW_DATA_PATH}")
print(f"📂 Output (Processed): {PROCESSED_DIR}")
print(f"📊 Output (Reports): {REPORTS_DIR}")
print("="*80)


# ===========================================================================
# 2. LOAD DATA
# ===========================================================================

def load_data(filepath):
    """Load the crop yield dataset from Excel file."""
    print("\n" + "="*80)
    print("STEP 1: LOAD DATA")
    print("="*80)

    if not os.path.exists(filepath):
        print(f"\n❌ ERROR: File not found!")
        print(f"   Looking for: {filepath}")
        return None

    df = pd.read_excel(filepath)
    print(f"\n✅ Data loaded successfully!")
    print(f"   📊 Rows: {df.shape[0]}")
    print(f"   📊 Columns: {df.shape[1]}")
    print(f"   📋 Column names: {df.columns.tolist()}")
    return df


# ===========================================================================
# 3. FIX COLUMN NAMES
# ===========================================================================

def fix_column_names(df):
    """Fix column name issues."""
    print("\n" + "="*80)
    print("STEP 2: FIX COLUMN NAMES")
    print("="*80)

    if 'Temperatue' in df.columns:
        df.rename(columns={'Temperatue': 'Temperature'}, inplace=True)
        print("✅ Fixed: 'Temperatue' → 'Temperature'")
    else:
        print("✅ No column name issues found")

    print(f"\n✅ Final column names: {df.columns.tolist()}")
    return df


# ===========================================================================
# 4. DATA QUALITY CHECK
# ===========================================================================

def check_data_quality(df):
    """Check for missing values and duplicates."""
    print("\n" + "="*80)
    print("STEP 3: DATA QUALITY CHECK")
    print("="*80)

    # Define numerical columns
    numerical_cols = ['Rain Fall (mm)', 'Fertilizer', 'Temperature',
                      'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)', 'Yeild (Q/acre)']

    # Check missing values in numerical columns only
    missing_num = df[numerical_cols].isnull().sum()
    if missing_num.sum() == 0:
        print("✅ No missing values in numerical columns!")
    else:
        print(f"⚠️ Missing values found in numerical columns:\n{missing_num[missing_num > 0]}")
        # Fill only numerical columns with median
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        print("✅ Missing values filled with median")

    # Check missing in categorical columns
    missing_cat = df['Crop Type'].isnull().sum()
    if missing_cat > 0:
        print(f"⚠️ Missing values in Crop Type: {missing_cat}")
        df['Crop Type'] = df['Crop Type'].fillna(df['Crop Type'].mode()[0])
        print("✅ Missing Crop Type filled with mode")

    # Check duplicates
    duplicates = df.duplicated().sum()
    if duplicates == 0:
        print("✅ No duplicate rows found!")
    else:
        print(f"⚠️ Found {duplicates} duplicate rows")
        df = df.drop_duplicates()
        print(f"✅ Removed {duplicates} duplicates")

    # Check data types
    print("\n📋 Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")

    return df


# ===========================================================================
# 5. DESCRIPTIVE STATISTICS
# ===========================================================================

def descriptive_statistics(df):
    """Generate and save descriptive statistics."""
    print("\n" + "="*80)
    print("STEP 4: DESCRIPTIVE STATISTICS")
    print("="*80)

    numerical_cols = ['Rain Fall (mm)', 'Fertilizer', 'Temperature',
                      'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)', 'Yeild (Q/acre)']
    stats = df[numerical_cols].describe()
    print(stats)

    # Save statistics to reports
    stats_path = os.path.join(REPORTS_DIR, 'descriptive_statistics.csv')
    stats.to_csv(stats_path)
    print(f"\n✅ Statistics saved to: {stats_path}")

    return stats


# ===========================================================================
# 6. OUTLIER DETECTION AND TREATMENT
# ===========================================================================

def handle_outliers(df):
    """Detect and treat outliers using IQR method."""
    print("\n" + "="*80)
    print("STEP 5: OUTLIER DETECTION AND TREATMENT")
    print("="*80)

    numerical_cols = ['Rain Fall (mm)', 'Fertilizer', 'Temperature',
                      'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']

    print("\n📐 Method: IQR (Interquartile Range)")
    print("   Formula: Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR")
    print("-"*80)

    outlier_results = {}

    # Detect outliers
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_results[col] = len(outliers)
        print(f"   {col}: {len(outliers)} outliers detected")
        if len(outliers) > 0:
            print(f"      Range: [{lower:.2f}, {upper:.2f}]")

    # Cap outliers using winsorization
    print("\n📌 Applying Winsorization (capping)...")
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = df[col].clip(lower=lower, upper=upper)

        if outlier_results[col] > 0:
            print(f"   ✅ {col}: capped {outlier_results[col]} outliers")

    print("\n✅ Outlier treatment complete!")
    return df, outlier_results


# ===========================================================================
# 7. FEATURE ENGINEERING
# ===========================================================================

def create_features(df):
    """Create new features from existing data."""
    print("\n" + "="*80)
    print("STEP 6: FEATURE ENGINEERING")
    print("="*80)

    print("\n📌 Creating composite features:")

    # 1. Total NPK
    df['NPK_Total'] = df['Nitrogen (N)'] + df['Phosphorus (P)'] + df['Potassium (K)']
    print("   ✅ NPK_Total = N + P + K")

    # 2. Rain-Fertilizer interaction
    df['Rain_Fertilizer'] = df['Rain Fall (mm)'] * df['Fertilizer']
    print("   ✅ Rain_Fertilizer = Rainfall × Fertilizer")

    # 3. Temperature-NPK interaction
    df['Temp_NPK'] = df['Temperature'] * df['NPK_Total']
    print("   ✅ Temp_NPK = Temperature × NPK_Total")

    print("\n📌 Creating categorical bins:")

    # 4. Rainfall categories
    df['Rainfall_Category'] = pd.cut(df['Rain Fall (mm)'],
                                     bins=[0, 600, 900, 1200, float('inf')],
                                     labels=['Low', 'Medium', 'High', 'Very High'])
    print("   ✅ Rainfall_Category: Low, Medium, High, Very High")

    # 5. Yield categories
    df['Yield_Category'] = pd.cut(df['Yeild (Q/acre)'],
                                  bins=[0, 8, 10, 12, float('inf')],
                                  labels=['Low', 'Medium', 'High', 'Very High'])
    print("   ✅ Yield_Category: Low, Medium, High, Very High")

    print("\n📌 Encoding categorical variables:")

    # 6. Encode crop type
    le = LabelEncoder()
    df['Crop_Type_Encoded'] = le.fit_transform(df['Crop Type'])

    crop_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("   ✅ Crop_Type_Encoded:")
    for crop, code in crop_mapping.items():
        print(f"      {crop}: {code}")

    print(f"\n✅ Total new features created: 6")
    print(f"   Final dataset has {df.shape[1]} columns")

    return df, le


# ===========================================================================
# 8. DATA STANDARDIZATION
# ===========================================================================

def standardize_features(df):
    """Standardize numerical features using StandardScaler."""
    print("\n" + "="*80)
    print("STEP 7: DATA STANDARDIZATION")
    print("="*80)

    numerical_cols = ['Rain Fall (mm)', 'Fertilizer', 'Temperature',
                      'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']

    print("\n📐 Method: StandardScaler")
    print("   Formula: X_scaled = (X - μ) / σ")
    print("-"*80)

    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    print(f"✅ Features standardized:")
    print(f"   Number of features scaled: {len(numerical_cols)}")
    print(f"   Mean of scaled features: {df_scaled[numerical_cols].mean().mean():.10f}")
    print(f"   Std of scaled features: {df_scaled[numerical_cols].std().mean():.10f}")

    return df_scaled, scaler


# ===========================================================================
# 9. SAVE DATA
# ===========================================================================

def save_data(df, df_scaled):
    """Save cleaned and scaled data to data/processed/."""
    print("\n" + "="*80)
    print("STEP 8: SAVE CLEANED DATA")
    print("="*80)

    # Save cleaned data
    output_path = os.path.join(PROCESSED_DIR, 'crop_yield_cleaned.csv')
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")

    # Save scaled data
    scaled_path = os.path.join(PROCESSED_DIR, 'crop_yield_scaled.csv')
    df_scaled.to_csv(scaled_path, index=False)
    print(f"✅ Scaled data saved to: {scaled_path}")

    return output_path, scaled_path


# ===========================================================================
# 10. GENERATE VISUALIZATIONS
# ===========================================================================

def generate_visualizations(df):
    """Generate and save visualizations to data/reports/."""
    print("\n" + "="*80)
    print("STEP 9: GENERATE VISUALIZATIONS")
    print("="*80)

    numerical_cols = ['Rain Fall (mm)', 'Fertilizer', 'Temperature',
                      'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
    all_cols = numerical_cols + ['Yeild (Q/acre)']

    # 1. Correlation Matrix
    print("\n   1️⃣ Correlation Matrix...")
    plt.figure(figsize=(12, 10))
    corr_cols = numerical_cols + ['Yeild (Q/acre)']
    corr_matrix = df[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', square=True, linewidths=0.5)
    plt.title('Correlation Matrix of Numerical Features', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("      ✅ correlation_matrix.png")

    # 2. Distribution Plots
    print("\n   2️⃣ Distribution Plots...")
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    for i, col in enumerate(all_cols):
        row = i // 4
        col_idx = i % 4
        sns.histplot(df[col], kde=True, ax=axes[row, col_idx])
        axes[row, col_idx].set_title(f'Distribution of {col}')
        axes[row, col_idx].set_xlabel(col)
        axes[row, col_idx].set_ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'distributions.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("      ✅ distributions.png")

    # 3. Box Plots
    print("\n   3️⃣ Box Plots...")
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    for i, col in enumerate(all_cols):
        row = i // 4
        col_idx = i % 4
        sns.boxplot(y=df[col], ax=axes[row, col_idx])
        axes[row, col_idx].set_title(f'Boxplot of {col}')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'boxplots.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("      ✅ boxplots.png")

    # 4. Yield by Crop Type
    print("\n   4️⃣ Yield by Crop Type...")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Crop Type', y='Yeild (Q/acre)', data=df)
    plt.title('Yield Distribution by Crop Type', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'yield_by_crop.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("      ✅ yield_by_crop.png")

    print("\n✅ All visualizations generated successfully!")


# ===========================================================================
# 11. SUMMARY REPORT
# ===========================================================================

def generate_summary(df, outlier_results, original_shape):
    """Generate a summary of the data cleaning process."""
    print("\n" + "="*80)
    print("📋 DATA CLEANING SUMMARY REPORT")
    print("="*80)

    print(f"""
📊 DATASET INFORMATION:
   • Original rows: {original_shape[0]}
   • Final rows: {df.shape[0]}
   • Original columns: {original_shape[1]}
   • Final columns: {df.shape[1]}
   • Crop types: {df['Crop Type'].unique().tolist()}
   • Target variable: Yield (Q/acre)

📊 DATA QUALITY:
   • Missing values: 0
   • Duplicate records: 0
   • Outliers capped: {sum(outlier_results.values())}

📊 NEW FEATURES CREATED (6):
   • NPK_Total = N + P + K
   • Rain_Fertilizer = Rainfall × Fertilizer
   • Temp_NPK = Temperature × NPK_Total
   • Rainfall_Category (Low, Medium, High, Very High)
   • Yield_Category (Low, Medium, High, Very High)
   • Crop_Type_Encoded (Label Encoded)

📊 FEATURE SCALING:
   • Method: StandardScaler
   • Features scaled: 6

📊 OUTPUT FILES:
   📄 data/processed/crop_yield_cleaned.csv
   📄 data/processed/crop_yield_scaled.csv
   📄 data/reports/descriptive_statistics.csv
   🖼️ data/reports/correlation_matrix.png
   🖼️ data/reports/distributions.png
   🖼️ data/reports/boxplots.png
   🖼️ data/reports/yield_by_crop.png
""")


# ===========================================================================
# 12. MAIN PIPELINE
# ===========================================================================

def run_pipeline(filepath):
    """Complete data cleaning pipeline."""
    print("\n" + "="*80)
    print("🚀 STARTING DATA CLEANING PIPELINE")
    print("="*80)

    # 1. Load data
    df = load_data(filepath)
    if df is None:
        return None, None, None, None

    original_shape = df.shape

    # 2. Fix column names
    df = fix_column_names(df)

    # 3. Check data quality
    df = check_data_quality(df)

    # 4. Descriptive statistics
    stats = descriptive_statistics(df)

    # 5. Handle outliers
    df, outlier_results = handle_outliers(df)

    # 6. Create features
    df, label_encoder = create_features(df)

    # 7. Standardize features
    df_scaled, scaler = standardize_features(df)

    # 8. Save data
    save_data(df, df_scaled)

    # 9. Generate visualizations
    generate_visualizations(df)

    # 10. Generate summary
    generate_summary(df, outlier_results, original_shape)

    # 11. Final message
    print("\n" + "="*80)
    print("🎉 DATA CLEANING AND PREPROCESSING COMPLETE!")
    print("="*80)
    print(f"""
✅ ALL FILES SAVED IN:
   📂 Processed data: {PROCESSED_DIR}
   📊 Reports: {REPORTS_DIR}

📈 THE DATA IS NOW READY FOR:
   • Exploratory Data Analysis (EDA)
   • Machine Learning Model Training
   • Feature Selection and Engineering

🚀 
""")

    return df, df_scaled, label_encoder, scaler


# ===========================================================================
# 13. RUN THE SCRIPT
# ===========================================================================

if __name__ == "__main__":
    df_cleaned, df_scaled, le, scaler = run_pipeline('data/raw/Crop yield data.xlsx')