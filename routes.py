"""
API Routes for Heart Disease Prediction
"""
import os
import numpy as np
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, ECG_CLASSES


# Create blueprint
api = Blueprint("api", __name__)

from model_loader import get_xgb_model
from ecg_predict import predict_ecg


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS





def generate_suggestions(data, prediction):
    """Generate health suggestions based on input data and prediction."""
    tips = []
    
    if data["age"] > 45:
        tips.append("Age-related risk: Schedule regular heart checkups.")
    if data["trestbps"] > 130:
        tips.append("High blood pressure: Reduce salt intake and monitor BP daily.")
    if data["chol"] > 200:
        tips.append("High cholesterol: Avoid fried food and eat fiber-rich foods.")
    if data["thalach"] < 140:
        tips.append("Low exercise tolerance: Start moderate cardio exercise.")
    if data["oldpeak"] > 1.5:
        tips.append("High ST depression: Immediate cardiology evaluation recommended.")
    if data["slope"] >= 1:
        tips.append("Abnormal ST slope: Avoid heavy exertion without medical supervision.")
    if data["exang"] == 1:
        tips.append("Exercise-induced angina: Limit physical stress and consult doctor.")
    if data["fbs"] == 1:
        tips.append("Elevated blood sugar: Control sugar intake and check glucose regularly.")
    
    if prediction == 1:
        tips.append("Follow medical treatment strictly and never ignore chest pain symptoms.")
    else:
        tips.append("Maintain a heart-healthy lifestyle and continue preventive care.")
    
    return tips[:5]


def determine_final_result(risk_score, prediction):
    """Determine final result based on risk score."""
    if risk_score is not None:
        if risk_score >= 66:
            return "HIGH CARDIAC RISK DETECTED", "high"
        elif risk_score >= 33:
            return "MODERATE CARDIAC RISK", "moderate"
        else:
            return "LOW CARDIAC RISK", "low"
    else:
        if prediction == 1:
            return "HIGH CARDIAC RISK DETECTED", "high"
        else:
            return "LOW CARDIAC RISK", "low"


@api.route("/predict_data", methods=["POST"])
def predict_data():
    """
    POST /predict_data
    Accept numerical features. Run XGBoost model for risk score.
    Returns JSON with risk level and score.
    """
    try:
        xgb_model = get_xgb_model()
        
        # Extract form data
        req_data = request.form if "age" in request.form else request.json
        if not req_data:
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        features = [
            float(req_data["age"]),
            float(req_data["sex"]),
            float(req_data["painloc"]),
            float(req_data["painexer"]),
            float(req_data["relrest"]),
            float(req_data["cp"]),
            float(req_data["trestbps"]),
            float(req_data["chol"]),
            float(req_data["smoke"]),
            float(req_data["cigs"]),
            float(req_data["years"]),
            1.0 if float(req_data["fbs"]) > 120 else 0.0,
            float(req_data["dm"]),
            float(req_data["famhist"]),
            float(req_data["restecg"]),
            float(req_data["thaldur"]),
            float(req_data["thalach"]),
            float(req_data["thalrest"]),
            float(req_data["tpeakbps"]),
            float(req_data["trestbpd"]),
            float(req_data["exang"]),
            float(req_data["oldpeak"]),
            float(req_data["slope"]),
            float(req_data["ca"]),
            float(req_data["thal"])
        ]
        final_input = np.array([features])
        
        prediction = int(xgb_model.predict(final_input)[0])
        try:
            proba = xgb_model.predict_proba(final_input)[0]
            risk_score = int(round(float(proba[1]) * 100))
        except Exception:
            risk_score = None
            
        prediction_text = "Patient has Heart Disease" if prediction == 1 else "Patient has No Heart Disease"

        return jsonify({
            "success": True,
            "prediction": prediction,
            "prediction_text": prediction_text,
            "risk_score": risk_score
        })
    except KeyError as e:
        return jsonify({"success": False, "error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/predict_ecg", methods=["POST"])
def predict_ecg_endpoint():
    """
    POST /predict_ecg
    Accepts a MIT-BIH format ECG CSV file (187 signal values per row).
    Runs 1D CNN model for ECG classification.
    Returns JSON with ECG label and flag.
    """
    if "ecg_file" not in request.files:
        return jsonify({"success": False, "error": "No ECG file provided."}), 400
        
    file = request.files["ecg_file"]
    if not file or file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    # Only accept CSV files for the ECG signal
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"success": False, "error": "ECG file must be a .csv file with 187 signal values."}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = secure_filename(f"{timestamp}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        ecg_result, ecg_flag = predict_ecg(filepath)
        return jsonify({
            "success": True,
            "ecg_result": ecg_result,
            "ecg_flag": ecg_flag,
            "ecg_file_path": filepath
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/predict_final", methods=["POST"])
def predict_final():
    """
    POST /predict_final
    Accepts patient demographics, numerical outcome, and ECG outcome.
    Applies fusion logic, saves to DB, returns final result and suggestions.
    """
    from database import save_patient_record
    try:
        req_data = request.json
        if not req_data:
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        # Extracted data
        xgb_prediction = int(req_data.get("prediction", 0))
        risk_score = req_data.get("risk_score")
        ecg_flag = int(req_data.get("ecg_flag", 0)) if "ecg_flag" in req_data else 0
        
        # Patient Data to save and generate suggestions
        data = req_data.get("patient_data", {})
        
        # Fusion Logic
        # Both indicate risk -> High Risk
        # One indicates risk -> Moderate Risk
        # Both normal -> Low Risk
        if xgb_prediction == 1 and ecg_flag == 1:
            final_result_text = "HIGH CARDIAC RISK DETECTED"
            risk_level = "high"
        elif xgb_prediction == 1 or ecg_flag == 1:
            final_result_text = "MODERATE CARDIAC RISK"
            risk_level = "moderate"
        else:
            final_result_text = "NO HEART DISEASE DETECTED"
            risk_level = "low"
            
        # Prepare data for database and suggestions
        db_data = data.copy() if data else {}
        db_data["name"] = db_data.get("name", "Anonymous")
        
        # Cast numeric fields to prevent TypeError in generate_suggestions
        if data:
            try:
                data["age"] = int(data.get("age", 0))
                data["trestbps"] = int(data.get("trestbps", 0))
                data["chol"] = int(data.get("chol", 0))
                data["thalach"] = int(data.get("thalach", 0))
                data["oldpeak"] = float(data.get("oldpeak", 0.0))
                data["slope"] = int(data.get("slope", 0))
                data["exang"] = int(data.get("exang", 0))
                data["fbs"] = int(data.get("fbs", 0))
                data["sex"] = int(data.get("sex", 0))
                data["cp"] = int(data.get("cp", 0))
                data["restecg"] = int(data.get("restecg", 0))
                data["ca"] = int(data.get("ca", 0))
                data["thal"] = int(data.get("thal", 0))
            except ValueError:
                pass # Proceed with whatever we have, though likely failing later

        # Ensure we always pass back a valid text overriding determine_final_result
        suggestions = generate_suggestions(data, xgb_prediction) if data else []
        
        # db_data receives the casted properties implicitly because they point to the same dict?
        # Actually it's a copy. Let's merge it:
        db_data.update(data)
        
        db_data["prediction"] = xgb_prediction
        db_data["risk_score"] = risk_score
        db_data["ecg_result"] = req_data.get("ecg_result")
        db_data["ecg_image_path"] = req_data.get("ecg_image_path")
        db_data["final_result"] = final_result_text
        
        patient_id = save_patient_record(db_data)
        
        return jsonify({
            "success": True,
            "patient_id": patient_id,
            "final_result": final_result_text,
            "risk_level": risk_level,
            "suggestions": suggestions
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/patients", methods=["GET"])
def get_patients():
    """GET /patients - Retrieve all patient records."""
    from database import get_all_patients
    
    try:
        patients = get_all_patients()
        return jsonify({
            "success": True,
            "count": len(patients),
            "patients": patients
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    """GET /patients/<id> - Retrieve a specific patient record."""
    from database import get_patient_by_id
    
    try:
        patient = get_patient_by_id(patient_id)
        if patient:
            return jsonify({
                "success": True,
                "patient": patient
            })
        else:
            return jsonify({
                "success": False,
                "error": "Patient not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -------------------------
# Cardiologist Routes
# -------------------------

@api.route("/cardiologists", methods=["GET"])
def get_cardiologists():
    """GET /cardiologists - Retrieve all cardiologists, optionally filtered by city."""
    from database import get_all_cardiologists
    
    try:
        city = request.args.get("city")
        cardiologists = get_all_cardiologists(city)
        return jsonify({
            "success": True,
            "count": len(cardiologists),
            "cardiologists": cardiologists
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api.route("/cardiologists/<int:cardiologist_id>", methods=["GET"])
def get_cardiologist(cardiologist_id):
    """GET /cardiologists/<id> - Retrieve a specific cardiologist."""
    from database import get_cardiologist_by_id
    
    try:
        cardiologist = get_cardiologist_by_id(cardiologist_id)
        if cardiologist:
            return jsonify({
                "success": True,
                "cardiologist": cardiologist
            })
        else:
            return jsonify({
                "success": False,
                "error": "Cardiologist not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -------------------------
# Appointment Routes
# -------------------------

@api.route("/appointments", methods=["POST"])
def book_appointment():
    """POST /appointments - Book an appointment with a cardiologist."""
    from database import save_appointment, get_cardiologist_by_id
    
    try:
        data = {
            "patient_name": request.form.get("patient_name") or request.json.get("patient_name"),
            "email": request.form.get("email") or request.json.get("email"),
            "phone": request.form.get("phone") or request.json.get("phone"),
            "cardiologist_id": request.form.get("cardiologist_id") or request.json.get("cardiologist_id"),
            "appointment_date": request.form.get("appointment_date") or request.json.get("appointment_date"),
            "appointment_time": request.form.get("appointment_time") or request.json.get("appointment_time"),
            "reason": request.form.get("reason") or request.json.get("reason")
        }
        
        if not data["patient_name"]:
            return jsonify({
                "success": False,
                "error": "Patient name is required"
            }), 400
        
        # Get cardiologist details for response
        cardiologist = None
        if data["cardiologist_id"]:
            cardiologist = get_cardiologist_by_id(int(data["cardiologist_id"]))
        
        appointment_id = save_appointment(data)
        
        return jsonify({
            "success": True,
            "message": "Appointment booked successfully!",
            "appointment_id": appointment_id,
            "doctor_name": cardiologist["name"] if cardiologist else None,
            "hospital": cardiologist["hospital"] if cardiologist else None
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api.route("/appointments", methods=["GET"])
def get_appointments():
    """GET /appointments - Retrieve all appointments."""
    from database import get_all_appointments
    
    try:
        appointments = get_all_appointments()
        return jsonify({
            "success": True,
            "count": len(appointments),
            "appointments": appointments
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -------------------------
# Contact Routes
# -------------------------

@api.route("/contact", methods=["POST"])
def submit_contact():
    """POST /contact - Submit a contact message."""
    from database import save_contact_message
    
    try:
        data = {
            "name": request.form.get("name") or request.json.get("name"),
            "email": request.form.get("email") or request.json.get("email"),
            "phone": request.form.get("phone") or request.json.get("phone"),
            "message": request.form.get("message") or request.json.get("message")
        }
        
        if not data["name"]:
            return jsonify({
                "success": False,
                "error": "Name is required"
            }), 400
        
        if not data["message"]:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        message_id = save_contact_message(data)
        
        return jsonify({
            "success": True,
            "message": "Thank you for your message! We'll get back to you soon.",
            "message_id": message_id
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

