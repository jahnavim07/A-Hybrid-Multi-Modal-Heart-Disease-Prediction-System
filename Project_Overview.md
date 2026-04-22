# Heart Disease Prediction: Multi-Modal System Overview

This document provides a comprehensive, "pin-to-pin" technical overview of the Heart Disease Prediction system, designed for a research paper's methodology and technical analysis sections.

---

## 1. System Abstract & Objective
The system is a clinical decision support tool that predicts the risk of heart disease by integrating **structured patient demographics** and **physiological data** with **electrocardiogram (ECG) signal analysis**. It employs a **dual-model architecture** consisting of an **XGBoost Classifier** for tabular data and a **1D Convolutional Neural Network (CNN)** for ECG arrhythmia classification.

---

## 2. Methodology: Dual-Model Framework

The system utilizes a **Late Fusion strategy**, where two independent machine learning models process distinct data modalities, and their outputs are combined using a predefined logical heuristic to determine the final clinical risk level.

### A. Tabular Data Classification (XGBoost)
The XGBoost model processes 25 clinical features to predict the likelihood of heart disease (binary classification) and provide a risk probability score (0.0–1.0).

### B. ECG Signal Classification (1D CNN)
The CNN architecture analyzes raw 1D temporal signals from the MIT-BIH dataset, classifying them into five distinct arrhythmia categories.

---

## 3. Data Description & Preprocessing

### 3.1 Structured Clinical Data (25 Features)
The system uses an expanded feature set (derived from the UCI Heart Disease dataset) consisting of:

| # | Feature | Description | # | Feature | Description |
|---|---------|-------------|---|---------|-------------|
| 1 | `age` | Patient's age | 14 | `famhist` | Family history of CHD |
| 2 | `sex` | Gender (1=M, 0=F) | 15 | `restecg` | Resting ECG results |
| 3 | `painloc` | Pain location | 16 | `thaldur` | Duration of exercise |
| 4 | `painexer` | Pain on exertion | 17 | `thalach` | Max HR achieved |
| 5 | `relrest` | Relief after rest | 18 | `thalrest` | Resting heart rate |
| 6 | `cp` | Chest pain type | 19 | `tpeakbps` | Peak exercise BP (Sys) |
| 7 | `trestbps` | Resting blood pressure | 20 | `trestbpd` | Resting BP (Dia) |
| 8 | `chol` | Serum cholesterol | 21 | `exang` | Exercise induced angina |
| 9 | `smoke` | Smoking status | 22 | `oldpeak` | ST depression |
| 10 | `cigs` | Cigarettes per day | 23 | `slope` | Slope of ST segment |
| 11 | `years` | Years of smoking | 24 | `ca` | # of major vessels |
| 12 | `fbs` | Fasting blood sugar | 25 | `thal` | Thalassemia type |
| 13 | `dm` | Diabetes status | | | |

### 3.2 ECG Signal Data
- **Format**: MIT-BIH Arrhythmia Dataset format.
- **Input Dimensions**: 187 signal values per heartbeat (normalized voltage).
- **Classes**:
  - Class 0: Normal (`N`)
  - Class 1: Supraventricular premature beat (`S`)
  - Class 2: Premature ventricular contraction (`V`)
  - Class 3: Fusion of ventricular and normal beat (`F`)
  - Class 4: Unclassifiable beat (`Q`)

---

## 4. Machine Learning Architecture

### 4.1 XGBoost Classifier Details
The tabular model is an optimized eXtreme Gradient Boosting (XGBoost) classifier.
- **Hyperparameters**:
  - `n_estimators`: 100
  - `learning_rate`: 0.1
  - `max_depth`: 4
  - `eval_metric`: 'logloss'
- **Training Strategy**: 80/20 train-test split on the 25-feature dataset.

### 4.2 1D Convolutional Neural Network (CNN) Architecture
Designed for temporal pattern extraction from sequence data.

### CNN Layers:
1. **Input**: (187, 1) temporal signal.
2. **Conv1D**: 32 filters, Kernel Size 5, Activation ReLU.
3. **MaxPooling1D**: Pool Size 2.
4. **Conv1D**: 64 filters, Kernel Size 3, Activation ReLU.
5. **MaxPooling1D**: Pool Size 2.
6. **Conv1D**: 128 filters, Kernel Size 3, Activation ReLU.
7. **MaxPooling1D**: Pool Size 2.
8. **Flatten**: Vectorization of feature maps.
9. **Dense**: 256 units, Activation ReLU.
10. **Dropout**: 0.5 (Regularization).
11. **Output**: 5 units, Activation Softmax.

---

## 5. System Workflow & Decision Logic

### 5.1 Pipeline Flow
1. **User Input Phase**: Numerical clinical data is entered via the web UI.
2. **Signal Upload Phase**: An ECG CSV file is uploaded for analysis.
3. **Prediction Execution**:
   - `predict_data()`: Generates XGBoost risk score.
   - `predict_ecg()`: Classifies signal into one of 5 MIT-BIH categories.
4. **Fusion Result**: Logic combines both model outcomes.

### 5.2 Fusion Logic (Clinical Risk Mapping)
The system maps the combined output to three risk levels:

| XGBoost Result | ECG Result (CNN) | Final Risk Level | Clinical Interpretation |
|----------------|------------------|------------------|-------------------------|
| **Disease (1)**| **Abnormal (!=0)** | **HIGH**         | Immediate medical intervention required. |
| **Disease (1)**| **Normal (0)**     | **MODERATE**     | Potential disease with normal rhythm. |
| **No Disease (0)**| **Abnormal (!=0)** | **MODERATE**     | Abnormal rhythm with low feature risk. |
| **No Disease (0)**| **Normal (0)**     | **LOW**          | Routine preventative care. |

---

## 6. Software Stack & Integration
- **Backend Framework**: Flask (Python)
- **Deep Learning Layer**: TensorFlow / Keras (CNN)
- **Classical ML Layer**: Scikit-Learn / XGBoost
- **Database**: SQLite3 (Stores patient records, doctor information, and appointments)
- **Data Persistence**: `patient_records.db` with primary tables:
    - `patients`: Demographics + risk outcomes.
    - `cardiologists`: Doctor profile and Hospital details.
    - `appointments`: Booking details linking patients and doctors.

---

## 7. Knowledge Recovery: Health Suggestions Mechanism
Based on the **25-feature input**, the system generates personalized clinical recommendations using an automated rule-based "Inference Engine":
- **Age (>45)**: "Schedule regular checkups."
- **BP (>130)**: "Reduce salt intake."
- **Cholesterol (>200)**: "Fiber-rich diet."
- **Exercise Angina**: "Limit physical stress."
- **Diabetes/PBS**: "Check sugar regularly."

---

*Generated for Research Documentation - 2026*
