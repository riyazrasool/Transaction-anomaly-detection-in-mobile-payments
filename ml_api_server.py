"""
Minimal ML inference API for UPI fraud scoring.
Loads fraud_engine.pkl and scaler.pkl and exposes /api/assess-risk.
"""

from __future__ import annotations

import os
import sys
import importlib
import pickle
import pickletools
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import lightgbm as lgb
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

LOG_FEATURES = {
    "amount",
    "s_avg_amount_5",
    "s_max_amount_5",
    "s_amount_std_5",
    "r_amount_sum_24h",
    "geo_distance_km",
}

DEFAULTS = {
    "txn_type": 0.0,
    "channel": 1.0,
    "is_new_payee": 0.0,
    "is_collect_request": 0.0,
    "time_of_day": 12.0,
    "day_of_week": 0.0,
    "vpn_proxy_flag": 0.0,
}


def extract_booster_model_str(model_path: str) -> str:
    model_bytes = Path(model_path).read_bytes()
    for op, arg, _ in pickletools.genops(model_bytes):
        if op.name in ("BINUNICODE", "SHORT_BINUNICODE") and isinstance(arg, str):
            if arg.startswith("tree\nversion="):
                return arg
    raise RuntimeError("Could not extract LightGBM model string from fraud_engine.pkl")


def load_scale_feature_list(scaler_path: str) -> List[str]:
    # Compatibility aliases for scaler pickles saved with numpy._core module paths.
    sys.modules.setdefault("numpy._core", importlib.import_module("numpy.core"))
    sys.modules.setdefault("numpy._core.multiarray", importlib.import_module("numpy.core.multiarray"))

    with open(scaler_path, "rb") as scaler_file:
        scaler_obj = pickle.load(scaler_file)

    if isinstance(scaler_obj, np.ndarray):
        return [str(item) for item in scaler_obj.tolist()]

    if isinstance(scaler_obj, list):
        return [str(item) for item in scaler_obj]

    return []


class FraudModelService:
    def __init__(self, model_path: str, scaler_path: str, threshold: float = 0.98):
        self.threshold = threshold
        self.model_loaded = False
        self.model: Optional[lgb.Booster] = None
        self.feature_order: List[str] = []
        self.scale_feature_list: List[str] = []

        try:
            model_str = extract_booster_model_str(model_path)
            self.model = lgb.Booster(model_str=model_str)
            self.feature_order = self.model.feature_name()
            self.scale_feature_list = load_scale_feature_list(scaler_path)
            self.model_loaded = True
            print(f"Loaded LightGBM model from: {model_path}")
            print(f"Loaded scaler feature list from: {scaler_path}")
            print(f"Model expects {len(self.feature_order)} features.")
        except Exception as exc:
            print(f"Failed to load model artifacts: {exc}")

    def _build_feature_vector(self, features: Dict[str, float]) -> np.ndarray:
        if not self.feature_order:
            raise RuntimeError("Model feature schema is unavailable.")

        vector = np.array(
            [[float(features.get(name, DEFAULTS.get(name, 0.0))) for name in self.feature_order]],
            dtype=float,
        )

        for idx, name in enumerate(self.feature_order):
            if name in LOG_FEATURES:
                vector[0, idx] = np.log1p(max(vector[0, idx], 0.0))

        return vector

    def predict(self, features: Dict[str, float]) -> Tuple[float, bool]:
        if not self.model_loaded or self.model is None:
            raise RuntimeError("Model artifacts are not loaded.")

        vector = self._build_feature_vector(features)
        probability = float(self.model.predict(vector)[0])
        return probability, probability > self.threshold


def resolve_default_paths() -> Tuple[str, str]:
    root_dir = Path(__file__).resolve().parent
    model_path = os.getenv("FRAUD_MODEL_PATH", str(root_dir / "fraud_engine.pkl"))
    scaler_path = os.getenv("FRAUD_SCALER_PATH", str(root_dir / "scaler.pkl"))
    return model_path, scaler_path


app = Flask(__name__)
CORS(app)

default_model_path, default_scaler_path = resolve_default_paths()
engine = FraudModelService(default_model_path, default_scaler_path)


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "model_loaded": engine.model_loaded,
            "feature_order": engine.feature_order,
        }
    )


@app.post("/api/assess-risk")
def assess_risk():
    try:
        payload = request.get_json(force=True, silent=False) or {}
        features = payload.get("features", {})

        if not isinstance(features, dict):
            return jsonify({"error": "features must be an object"}), 400

        required = [
            "amount",
            "s_txn_count_10min",
            "s_txn_count_1h",
            "s_avg_amount_5",
            "s_max_amount_5",
            "s_amount_std_5",
            "s_time_gap_avg",
            "r_txn_count_1h",
            "r_txn_count_24h",
            "r_unique_senders_24h",
            "r_amount_sum_24h",
            "geo_distance_km",
        ]
        missing = [name for name in required if name not in features]
        if missing:
            return jsonify({"error": "missing_features", "fields": missing}), 400

        probability, is_fraud = engine.predict(features)
        return jsonify(
            {
                "fraud_probability": probability,
                "is_fraud": is_fraud,
                "threshold": engine.threshold,
                "model_loaded": engine.model_loaded,
                "feature_order": engine.feature_order,
            }
        )
    except Exception as exc:
        return jsonify({"error": "prediction_failed", "detail": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("ML_API_PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=False)
