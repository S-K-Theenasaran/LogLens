
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler


def train_lof(
    train_features: pd.DataFrame,
    n_neighbors: int = 20,
    contamination: float = 0.05,
):
    """Train LOF for anomaly detection on unseen windows."""

    if len(train_features) < 3:
        raise ValueError("LOF requires at least 3 training samples.")

    if not all(
        pd.api.types.is_numeric_dtype(dtype)
        for dtype in train_features.dtypes
    ):
        raise ValueError("All training features must be numeric.")

    if train_features.isna().any().any():
        raise ValueError("Training features contain missing values.")

    scaler = StandardScaler()
    scaled_train = scaler.fit_transform(train_features)

    model = LocalOutlierFactor(
        n_neighbors=min(n_neighbors, len(train_features) - 1),
        contamination=contamination,
        novelty=True,
    )

    model.fit(scaled_train)
    return model, scaler


def predict_lof(
    model: LocalOutlierFactor,
    scaler: StandardScaler,
    features: pd.DataFrame,
) -> pd.DataFrame:
    """Predict anomalies in new log windows."""

    if features.empty:
        raise ValueError("Prediction features cannot be empty.")

    if list(features.columns) != list(scaler.feature_names_in_):
        raise ValueError("Feature columns must match training columns.")

    if features.isna().any().any():
        raise ValueError("Prediction features contain missing values.")

    scaled_features = scaler.transform(features)

    results = features.copy()
    predictions = model.predict(scaled_features)

    results["is_anomaly"] = (predictions == -1).astype(int)
    results["anomaly_score"] = -model.decision_function(
        scaled_features
    )

    return results
