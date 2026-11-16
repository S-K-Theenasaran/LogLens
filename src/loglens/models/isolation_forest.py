
import pandas as pd
from sklearn.ensemble import IsolationForest


def train_isolation_forest(
    train_features: pd.DataFrame,
    contamination: float = 0.05,
    random_state: int = 42,
) -> IsolationForest:
    """Train an Isolation Forest on numerical window features."""

    if train_features.empty:
        raise ValueError("Training features cannot be empty.")

    if not all(pd.api.types.is_numeric_dtype(dtype)
               for dtype in train_features.dtypes):
        raise ValueError("All training features must be numeric.")

    if train_features.isna().any().any():
        raise ValueError("Training features contain missing values.")

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
    )

    model.fit(train_features)
    return model


def predict_anomalies(
    model: IsolationForest,
    features: pd.DataFrame,
) -> pd.DataFrame:
    """Return anomaly predictions and anomaly scores."""

    if features.empty:
        raise ValueError("Prediction features cannot be empty.")

    results = features.copy()

    predictions = model.predict(features)
    results["is_anomaly"] = (predictions == -1).astype(int)
    results["anomaly_score"] = -model.decision_function(features)

    return results
