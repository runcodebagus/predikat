# model.py
import os
import pickle
import numpy as np

_model = None
_scaler = None

MODEL_PATH = os.path.join("model", "model.pkl")
SCALER_PATH = os.path.join("model", "scaler.pkl")

def load_artifacts():
    """Load model & scaler sekali di startup."""
    global _model, _scaler
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    if _scaler is None:
        with open(SCALER_PATH, "rb") as f:
            _scaler = pickle.load(f)
    return _model, _scaler

def _map_label(label):
    """Map label model ke teks manusiawi."""
    # Kalau label sudah berupa huruf
    if isinstance(label, str):
        mapping = {
            "A": "Excellent",
            "B": "Good",
            "C": "Fair",
            "D": "Poor",
        }
        return mapping.get(label, f"Label tidak dikenali: {label}")

    # Kalau label berupa angka (0/1/2/3)
    mapping_num = {0: "Sangat Baik", 1: "Baik", 2: "Cukup", 3: "Buruk"}
    return mapping_num.get(label, f"Label tidak dikenali: {label}")

def predict_grade(data_row):
    """
    data_row: list[float] panjang 8, contoh: [3.21, 3.12, 3.00, 2.95, 3.40, 3.20, 3.15, 3.25]
    return: string hasil (mis. 'Baik')
    """
    model, scaler = load_artifacts()

    X = np.array([data_row], dtype=float)  # (1, 8)
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    label = y_pred[0]
    return _map_label(label)
