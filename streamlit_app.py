"""Streamlit application for crop-yield prediction."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from src.feature_engineering import prepare_model_features


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "deployment_model.joblib"
)


st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌱",
    layout="wide",
)


# ---------------------------------------------------------
# Load the deployment model
# ---------------------------------------------------------

@st.cache_resource(
    show_spinner="Loading prediction model..."
)
def load_model_bundle() -> dict:
    """Load the fitted deployment model and its metadata."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file was not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# Numeric input helper
# ---------------------------------------------------------

def create_numeric_input(
    feature: str,
    label: str,
    ranges: dict,
) -> float:
    """Create a numeric input using the training-data range."""

    feature_range = ranges[feature]

    minimum = float(feature_range["minimum"])
    maximum = float(feature_range["maximum"])
    median = float(feature_range["median"])

    return st.number_input(
        label=label,
        min_value=minimum,
        max_value=maximum,
        value=median,
        format="%.2f",
        help=(
            "Enter a value using the same unit as the "
            "training dataset. "
            f"Observed range: {minimum:.2f} to "
            f"{maximum:.2f}."
        ),
    )


# ---------------------------------------------------------
# Load model safely
# ---------------------------------------------------------

try:
    bundle = load_model_bundle()

except Exception as error:
    st.error(
        "The crop-yield prediction model could not be loaded."
    )

    st.exception(error)
    st.stop()


model = bundle["model"]
input_ranges = bundle["input_ranges"]
performance = bundle["performance"]


# ---------------------------------------------------------
# Application heading
# ---------------------------------------------------------

st.title("🌱 Crop Yield Prediction")

st.write(
    "Enter the crop, weather, fertilizer and nutrient "
    "information below to generate an estimated crop yield."
)

st.info(
    f"Current deployment model: **{bundle['model_name']}**"
)

st.warning(
    "This application is a technical prototype. "
    f"The current model has a test R² of "
    f"{performance['test_r2']:.3f}, which indicates limited "
    "predictive performance on unseen observations. "
    "The prediction should not be treated as agronomic advice."
)


# ---------------------------------------------------------
# Prediction form
# ---------------------------------------------------------

with st.form("crop_yield_prediction_form"):

    st.subheader("Crop and environmental information")

    left_column, right_column = st.columns(2)

    with left_column:

        crop_type = st.selectbox(
            label="Crop type",
            options=bundle["crop_types"],
        )

        rainfall = create_numeric_input(
            feature="rainfall",
            label="Rainfall",
            ranges=input_ranges,
        )

        temperature = create_numeric_input(
            feature="temperature",
            label="Temperature",
            ranges=input_ranges,
        )

        fertilizer = create_numeric_input(
            feature="fertilizer",
            label="Fertilizer",
            ranges=input_ranges,
        )

    with right_column:

        nitrogen = create_numeric_input(
            feature="nitrogen",
            label="Nitrogen",
            ranges=input_ranges,
        )

        phosphorus = create_numeric_input(
            feature="phosphorus",
            label="Phosphorus",
            ranges=input_ranges,
        )

        potassium = create_numeric_input(
            feature="potassium",
            label="Potassium",
            ranges=input_ranges,
        )

    submitted = st.form_submit_button(
        label="Predict crop yield",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Generate prediction
# ---------------------------------------------------------

if submitted:

    original_input = pd.DataFrame(
        [
            {
                "crop_type": crop_type,
                "rainfall": rainfall,
                "temperature": temperature,
                "fertilizer": fertilizer,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
            }
        ]
    )

    try:
        model_input = prepare_model_features(
            original_input
        )

        expected_features = bundle["model_features"]

        model_input = model_input[
            expected_features
        ]

        prediction = float(
            model.predict(model_input)[0]
        )

    except Exception as error:
        st.error(
            "The prediction could not be generated."
        )

        st.exception(error)
        st.stop()

    st.success(
        "Crop-yield prediction generated successfully."
    )

    st.metric(
        label="Estimated crop yield",
        value=(
            f"{prediction:.2f} "
            f"{bundle['target_unit']}"
        ),
    )

    target_minimum = float(
        bundle["target_range"]["minimum"]
    )

    target_maximum = float(
        bundle["target_range"]["maximum"]
    )

    if (
        prediction < target_minimum
        or prediction > target_maximum
    ):
        st.warning(
            "The prediction is outside the crop-yield "
            "range observed in the training dataset."
        )

    with st.expander(
        "View the generated model features"
    ):
        st.dataframe(
            model_input.T.rename(
                columns={0: "Value"}
            ),
            use_container_width=True,
        )


# ---------------------------------------------------------
# Model performance
# ---------------------------------------------------------

st.divider()

st.subheader("Model performance")

metric_column_1, metric_column_2, metric_column_3 = (
    st.columns(3)
)

metric_column_1.metric(
    label="Test MAE",
    value=f"{performance['test_mae']:.3f}",
)

metric_column_2.metric(
    label="Test RMSE",
    value=f"{performance['test_rmse']:.3f}",
)

metric_column_3.metric(
    label="Test R²",
    value=f"{performance['test_r2']:.3f}",
)


st.caption(
    "Before prediction, the application automatically "
    "creates Total NPK, nitrogen proportion, phosphorus "
    "proportion, temperature squared and the "
    "rainfall–fertilizer interaction."
)
