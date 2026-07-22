from pathlib import Path

import pandas as pd


def load_data(file_path: Path) -> pd.DataFrame:
    """Load an Excel or CSV dataset."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    file_extension = file_path.suffix.lower()

    if file_extension in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)

    if file_extension == ".csv":
        return pd.read_csv(file_path)

    raise ValueError(
        f"Unsupported file format: {file_extension}. "
        "Use an Excel or CSV file."
    )


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the dataset with standardised column names."""
    cleaned = df.copy()

    cleaned.columns = (
        cleaned.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    return cleaned


def standardise_crop_labels(
    df: pd.DataFrame,
    crop_column: str = "crop"
) -> pd.DataFrame:
    """Standardise crop labels while preserving missing values."""
    cleaned = df.copy()

    if crop_column not in cleaned.columns:
        raise KeyError(
            f"Crop column '{crop_column}' was not found in the dataset."
        )

    cleaned[crop_column] = (
        cleaned[crop_column]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )

    return cleaned


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove exact duplicate rows and return the number removed."""
    cleaned = df.copy()

    duplicate_count = int(cleaned.duplicated().sum())

    cleaned = (
        cleaned
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return cleaned, duplicate_count


def convert_numeric_columns(
    df: pd.DataFrame,
    numeric_columns: list[str]
) -> pd.DataFrame:
    """Convert specified columns to numeric values."""
    cleaned = df.copy()

    missing_columns = [
        column for column in numeric_columns
        if column not in cleaned.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Numeric columns not found: {missing_columns}"
        )

    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce"
        )

    return cleaned


def get_missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages."""
    summary = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percentage": df.isna().mean().mul(100)
    })

    return summary.sort_values(
        by="missing_count",
        ascending=False
    )


def get_outlier_summary(
    df: pd.DataFrame,
    numeric_columns: list[str]
) -> pd.DataFrame:
    """Identify potential outliers using the IQR method."""
    results = []

    for column in numeric_columns:
        if column not in df.columns:
            continue

        series = df[column].dropna()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_count = int(
            (
                (series < lower_bound) |
                (series > upper_bound)
            ).sum()
        )

        results.append({
            "variable": column,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": outlier_count
        })

    return pd.DataFrame(results)


def save_cleaned_data(
    df: pd.DataFrame,
    output_path: Path
) -> None:
    """Save the cleaned dataset as a CSV file."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(output_path, index=False)
