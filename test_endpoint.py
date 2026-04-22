import requests

data = {
    "age": 25,
    "sex": 0,
    "cp": 0,
    "trestbps": 120,
    "chol": 150,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 0.0,
    "slope": 0,
    "ca": 0,
    "thal": 1
}

print("Testing /api/predict_data...")
res1 = requests.post("http://127.0.0.1:5000/api/predict_data", data=data)
print(res1.status_code)
try:
    print(res1.json())
except Exception as e:
    print(res1.text)

print("\nTesting /api/predict_final...")
json_data = {
    "prediction": 0,
    "prediction_text": "Low likelihood of heart disease",
    "risk_score": 10,
    "patient_data": data
}

res2 = requests.post("http://127.0.0.1:5000/api/predict_final", json=json_data)
print(res2.status_code)
try:
    print(res2.json())
except Exception as e:
    print(res2.text)
