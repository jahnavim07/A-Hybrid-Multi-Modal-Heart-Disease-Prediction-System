"""
Heart Disease Prediction Flask Application
Production-ready structure with XGBoost and CNN models
"""
from flask import Flask, render_template, request, jsonify
from config import SECRET_KEY, MAX_CONTENT_LENGTH, UPLOAD_FOLDER, DEBUG
from database import init_db
from routes import api
from model_loader import load_models

# -------------------------
# Initialize Flask App
# -------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------
# Initialize Database
# -------------------------
init_db()

# -------------------------
# Load Models
# -------------------------
print("Initializing models...")
load_models()


# -------------------------
# Register API Blueprint
# -------------------------
app.register_blueprint(api, url_prefix="/api")

# -------------------------
# Main Route (Template Rendering)
# -------------------------
@app.route("/", methods=["GET"])
def home():
    """Render the main prediction interface."""
    return render_template("index.html")


# -------------------------
# Health Check Endpoint
# -------------------------
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "xgboost_model": "heart_xgboost_model.pkl",
        "ecg_model": "ecg_model.h5"
    })


# -------------------------
# Run Application
# -------------------------
if __name__ == "__main__":
    app.run(debug=DEBUG)
