"""
Application Configuration
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
DATABASE_PATH = os.path.join(BASE_DIR, "patient_records.db")

# Uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "csv"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Models
MODELS_FOLDER = os.path.join(BASE_DIR, "models")
XGBOOST_MODEL_PATH = os.path.join(MODELS_FOLDER, "heart_xgboost_25_model.pkl")
ECG_MODEL_PATH = os.path.join(MODELS_FOLDER, "ecg_cnn_model.keras")

# ECG Classes (same order as training)
# MIT-BIH class labels (must match training order: 0,1,2,3,4)
ECG_CLASSES = [
    "Normal",
    "Supraventricular Ectopy",
    "Ventricular Ectopy",
    "Fusion Beat",
    "Unknown"
]

# Flask settings
DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
