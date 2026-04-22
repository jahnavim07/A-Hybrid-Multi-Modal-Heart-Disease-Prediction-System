"""
ECG Prediction Module — MIT-BIH CSV Signal Format
Expects a CSV file with 187 signal values (one heartbeat row from MIT-BIH dataset).
"""
import numpy as np
import pandas as pd
from config import ECG_CLASSES
from model_loader import get_ecg_model


def predict_ecg(csv_path):
    """
    Predict ECG class from a MIT-BIH format CSV file.

    The CSV file should contain either:
    - A single row of 187 signal values (raw heartbeat)
    - Or a single row of 188 values where the last column is a label (which is ignored)

    Returns:
        tuple: (label, flag) where flag is 0 for Normal, 1 for any abnormality
    """
    model = get_ecg_model()

    # Read CSV — no header expected
    df = pd.read_csv(csv_path, header=None)

    # Take the first row
    row = df.iloc[0].values.astype(np.float32)

    # Accept 187 values (pure signal) or 188 values (signal + label column — drop label)
    if len(row) == 188:
        row = row[:187]
    elif len(row) == 187:
        pass  # already correct
    else:
        raise ValueError(
            f"ECG CSV must have 187 signal values (or 188 with label). "
            f"Got {len(row)} columns. "
            "Please export one heartbeat row from the MIT-BIH dataset."
        )

    # Reshape for 1D CNN: (1, 187, 1)
    signal = row.reshape(1, 187, 1)

    # Run prediction
    preds = model.predict(signal)
    idx = int(np.argmax(preds[0]))

    label = ECG_CLASSES[idx] if idx < len(ECG_CLASSES) else f"Class {idx}"

    # Class 0 = Normal → risk_flag 0, anything else → risk_flag 1
    risk_flag = 0 if idx == 0 else 1

    return label, risk_flag
