"""
Script to extract sample ECG rows from MIT-BIH dataset for testing.
Generates:
  - sample_ecg_normal.csv    (class 0 = Normal heartbeat)
  - sample_ecg_abnormal.csv  (class 1 = Supraventricular Ectopy)
"""
import pandas as pd
import os

DATA_PATH = "archive (2)/mitbih_test.csv"
OUT_DIR = "sample_ecg_files"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH, header=None)
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# Class is the last column (column index 187)
LABEL_COL = 187

# --- Normal (class 0) ---
normal_rows = df[df[LABEL_COL] == 0.0]
if len(normal_rows) > 0:
    row = normal_rows.iloc[0, :187]  # only the 187 signal values, no label
    row.to_csv(os.path.join(OUT_DIR, "sample_ecg_normal.csv"), header=False, index=False)
    print(f"Saved sample_ecg_normal.csv  ({len(row)} values, class=Normal)")
else:
    print("WARNING: No Normal rows found")

# --- Supraventricular Ectopy (class 1) ---
sv_rows = df[df[LABEL_COL] == 1.0]
if len(sv_rows) > 0:
    row = sv_rows.iloc[0, :187]
    row.to_csv(os.path.join(OUT_DIR, "sample_ecg_sv_ectopy.csv"), header=False, index=False)
    print(f"Saved sample_ecg_sv_ectopy.csv  ({len(row)} values, class=Supraventricular Ectopy)")
else:
    print("WARNING: No SVE rows found")

# --- Ventricular Ectopy (class 2) ---
ve_rows = df[df[LABEL_COL] == 2.0]
if len(ve_rows) > 0:
    row = ve_rows.iloc[0, :187]
    row.to_csv(os.path.join(OUT_DIR, "sample_ecg_v_ectopy.csv"), header=False, index=False)
    print(f"Saved sample_ecg_v_ectopy.csv  ({len(row)} values, class=Ventricular Ectopy)")
else:
    print("WARNING: No VE rows found")

print(f"\nDone! Sample ECG CSV files saved to: {OUT_DIR}/")
print("You can upload any of these files via the ECG upload field in the frontend.")
