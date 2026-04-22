import pandas as pd
import numpy as np
import os
import glob

# Indices for 25 features and 1 target (0-indexed)
# Based on heart-disease.names
# target: 57 (attribute num 58)
feature_indices = [
    2, # age
    3, # sex
    4, # painloc
    5, # painexer
    6, # relrest
    8, # cp
    9, # trestbps
    11, # chol
    12, # smoke
    13, # cigs
    14, # years
    15, # fbs
    16, # dm
    17, # famhist
    18, # restecg
    28, # thaldur
    31, # thalach
    32, # thalrest
    33, # tpeakbps
    36, # trestbpd
    37, # exang
    39, # oldpeak
    40, # slope
    43, # ca
    50, # thal
]
target_index = 57

col_names = [
    'age', 'sex', 'painloc', 'painexer', 'relrest', 'cp', 'trestbps',
    'chol', 'smoke', 'cigs', 'years', 'fbs', 'dm', 'famhist', 'restecg',
    'thaldur', 'thalach', 'thalrest', 'tpeakbps', 'trestbpd', 'exang',
    'oldpeak', 'slope', 'ca', 'thal', 'target'
]

def parse_data_file(filepath):
    # The data files have 10 values per line, multiple lines per instance.
    # An instance ends with the 'name' attribute which was replaced with 'name'.
    # We will read everything block by block.
    with open(filepath, 'r', encoding='latin-1') as f:
        content = f.read().split()
    
    instances = []
    current_instance = []
    for token in content:
        if token == 'name':
            if len(current_instance) == 75:  # 75 numeric features + 1 name = 76
                instances.append(current_instance)
            current_instance = []
        else:
            try:
                current_instance.append(float(token))
            except ValueError:
                pass
    return instances

def main():
    data_dir = os.path.join(os.path.dirname(__file__), 'heart_disease')
    data_files = ['cleveland.data', 'hungarian.data', 'switzerland.data', 'long-beach-va.data']
    
    all_instances = []
    for file in data_files:
        filepath = os.path.join(data_dir, file)
        if os.path.exists(filepath):
            instances = parse_data_file(filepath)
            all_instances.extend(instances)
    
    print(f"Total instances parsed: {len(all_instances)}")
    
    extracted_data = []
    for inst in all_instances:
        # Extract features and target
        row = [inst[i] for i in feature_indices]
        # Target needs to be binary
        target_val = inst[target_index]
        binary_target = 1 if target_val > 0 else 0
        row.append(binary_target)
        extracted_data.append(row)
        
    df = pd.DataFrame(extracted_data, columns=col_names)
    
    # Handle missing values: denoted as -9.0
    df.replace(-9.0, np.nan, inplace=True)
    
    # Impute missing values with median for simplicity
    df.fillna(df.median(), inplace=True)
    
    output_path = os.path.join(os.path.dirname(__file__), 'heart_25_features.csv')
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == '__main__':
    main()
