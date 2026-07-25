"""Feature-engineering utilities for crop-yield modelling."""

from __future__ import annotations

import numpy as np
import pandas as pd


ORIGINAL_FEATURES = [
    "crop_type",
    "rainfall",
    "temperature",
    "fertilizer",
    "nitrogen",
    "phosphorus",
    "potassium",
]

ENGINEERED_FEATURES = [
    "total_npk",
    "n_proportion",
    "p_proportion",
    "temperature_squared",
    "rainfall_fertilizer_interaction",
]

MODEL_FEATURES = ORIGINAL_FEATURES + ENGINEERED_FEATURES

REQUIRED_COLUMNS = set(ORIGINAL_FEATURES)


def validate_feature_columns(data: pd.DataFrame) -> None:
    """Confirm that all columns required for feature engineering are present."""
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)

    if missing_columns:
        raise KeyError(
            "Missing required columns: "
            f"{sorted(missing_columns)}"
        )


def create_crop_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create the engineered variables used for crop-yield modelling.

    The function preserves all existing columns, including the target
    variable when it is present.

    Parameters
    ----------
    data:
        DataFrame containing the seven original model predictors.

    Returns
    -------
    pd.DataFrame
        Copy of the input data containing the engineered variables.
    """
    validate_feature_columns(data)

    df_feat = data.copy()

    numeric_features = [
        "rainfall",
        "temperature",
        "fertilizer",
        "nitrogen",
        "phosphorus",
        "potassium",
    ]

    df_feat[numeric_features] = (
        df_feat[numeric_features]
        .apply(pd.to_numeric, errors="raise")
        .astype(float)
    )

    df_feat["crop_type"] = (
        df_feat["crop_type"]
        .astype(str)
        .str.strip()
    )

    # Total nutrient level
    df_feat["total_npk"] = (
        df_feat["nitrogen"]
        + df_feat["phosphorus"]
        + df_feat["potassium"]
    )

    # Nutrient proportions cannot be calculated when total NPK is zero.
    zero_total_npk = df_feat["total_npk"].eq(0)

    if zero_total_npk.any():
        affected_rows = df_feat.index[zero_total_npk].tolist()

        raise ValueError(
            "Total NPK is zero for the following row indices: "
            f"{affected_rows}. At least one of nitrogen, "
            "phosphorus or potassium must be greater than zero."
        )

    df_feat["n_proportion"] = (
        df_feat["nitrogen"]
        / df_feat["total_npk"]
    )

    df_feat["p_proportion"] = (
        df_feat["phosphorus"]
        / df_feat["total_npk"]
    )

    # Nonlinear temperature term
    df_feat["temperature_squared"] = (
        df_feat["temperature"] ** 2
    )

    # Rainfall and fertilizer interaction
    df_feat["rainfall_fertilizer_interaction"] = (
        df_feat["rainfall"]
        * df_feat["fertilizer"]
    )

    engineered_values = df_feat[ENGINEERED_FEATURES]

    invalid_values = ~np.isfinite(
        engineered_values.to_numpy(dtype=float)
    )

    if invalid_values.any():
        raise ValueError(
            "Feature engineering produced missing or infinite values."
        )

    return df_feat


def prepare_model_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create and return the 12 predictors expected by the deployed model.

    This function is suitable for model training, evaluation and
    Streamlit prediction.
    """
    engineered_data = create_crop_features(data)

    return engineered_data[MODEL_FEATURES].copy()
