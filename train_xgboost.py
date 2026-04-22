import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import pickle

def main():
    data_path = os.path.join(os.path.dirname(__file__), 'heart_25_features.csv')
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run prepare_data.py first.")
        return
        
    df = pd.DataFrame(pd.read_csv(data_path))
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training shapes: X_train={X_train.shape}, y_train={y_train.shape}")
    print(f"Testing shapes:  X_test={X_test.shape}, y_test={y_test.shape}")
    
    # Initialize XGBoost Classifier
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'heart_xgboost_25_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"\nModel saved to {model_path}")

if __name__ == '__main__':
    main()
