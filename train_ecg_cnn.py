import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report
import os

def load_data():
    print("Loading MIT-BIH dataset...")
    # The last column is the class label
    train_data = pd.read_csv('archive (2)/mitbih_train.csv', header=None)
    test_data = pd.read_csv('archive (2)/mitbih_test.csv', header=None)
    
    # Split features and labels
    X_train = train_data.iloc[:, :-1].values
    y_train = train_data.iloc[:, -1].values
    
    X_test = test_data.iloc[:, :-1].values
    y_test = test_data.iloc[:, -1].values
    
    # Reshape for 1D CNN: (samples, time_steps, features)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    
    # One-hot encode the labels (5 classes in MIT-BIH)
    y_train = to_categorical(y_train, num_classes=5)
    y_test = to_categorical(y_test, num_classes=5)
    
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    
    return X_train, y_train, X_test, y_test

def build_model(input_shape):
    model = Sequential([
        Conv1D(filters=32, kernel_size=5, activation='relu', input_shape=input_shape),
        MaxPooling1D(pool_size=2),
        Conv1D(filters=64, kernel_size=3, activation='relu'),
        MaxPooling1D(pool_size=2),
        Conv1D(filters=128, kernel_size=3, activation='relu'),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(5, activation='softmax') # 5 classes
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    # Load dataset
    X_train, y_train, X_test, y_test = load_data()
    
    # Build model
    input_shape = (X_train.shape[1], 1)
    model = build_model(input_shape)
    model.summary()
    
    # Train model
    print("Training model...")
    # Training for 5 epochs for speed, typically 10-20 is good for this
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=128,
        validation_data=(X_test, y_test)
    )
    
    # Evaluate model
    print("Evaluating model...")
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model.save('models/ecg_cnn_model.keras')
    print("Model saved to models/ecg_cnn_model.keras")

if __name__ == "__main__":
    main()
