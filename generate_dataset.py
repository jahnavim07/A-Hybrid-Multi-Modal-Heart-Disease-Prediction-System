import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of records to generate
num_records = 15000

# Generate synthetic data based on the original heart.csv distributions
# Columns: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target

data = {
    'age': np.random.randint(29, 78, num_records),  # Age range based on typical dataset
    'sex': np.random.choice([0, 1], num_records, p=[0.32, 0.68]),  # Approx 68% male
    'cp': np.random.choice([0, 1, 2, 3], num_records, p=[0.48, 0.16, 0.28, 0.08]), # Chest pain type
    'trestbps': np.random.randint(94, 200, num_records), # Resting blood pressure
    'chol': np.random.randint(126, 564, num_records), # Cholesterol
    'fbs': np.random.choice([0, 1], num_records, p=[0.85, 0.15]), # Fasting blood sugar > 120
    'restecg': np.random.choice([0, 1, 2], num_records, p=[0.49, 0.50, 0.01]), # Resting ECG results
    'thalach': np.random.randint(71, 202, num_records), # Max heart rate
    'exang': np.random.choice([0, 1], num_records, p=[0.67, 0.33]), # Exercise induced angina
    'oldpeak': np.round(np.random.uniform(0, 6.2, num_records), 1), # ST depression
    'slope': np.random.choice([0, 1, 2], num_records, p=[0.07, 0.46, 0.47]), # Slope of peak exercise ST segment
    'ca': np.random.choice([0, 1, 2, 3, 4], num_records), # Number of major vessels (0-3 normally, 4 is sometimes seen as null/error but present in processed sets)
    'thal': np.random.choice([0, 1, 2, 3], num_records), # Thalassemia
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate target based on some logic to reproduce correlations (simplified)
# This is a heuristic to make the "prediction" somewhat learnable, rather than purely random noise
# Higher age, higher cp (0 is typical angina), higher thalach (lower is better?), exang=1, oldpeak>0 -> higher risk
# Note: In original dataset, target=1 implies presence of disease.

# Let's create a probability score
prob = (
    (df['age'] > 50).astype(int) * 0.2 +
    (df['sex'] == 1).astype(int) * 0.1 +
    (df['cp'] == 0).astype(int) * 0.3 + 
    (df['thalach'] < 150).astype(int) * 0.2 +
    (df['exang'] == 1).astype(int) * 0.2 +
    (df['oldpeak'] > 1.0).astype(int) * 0.2 +
    (df['ca'] > 0).astype(int) * 0.2 + 
    (df['thal'] == 2).astype(int) * 0.2
)
# Normalize prob roughly
prob = prob / prob.max()
# Add some noise
prob += np.random.normal(0, 0.1, num_records)
# Clip
prob = np.clip(prob, 0, 1)

# Assign target based on probability cutoff
df['target'] = (prob > 0.55).astype(int)

# Save to CSV
output_file = "heart_large.csv"
df.to_csv(output_file, index=False)

print(f"Generated {num_records} records and saved to {output_file}")
print(df.head())
print("\nTarget distribution:")
print(df['target'].value_counts(normalize=True))
