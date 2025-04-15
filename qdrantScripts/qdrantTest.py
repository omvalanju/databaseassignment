import pandas as pd
import numpy as np
import wfdb
import ast
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance

# === Config ===
base_dir = Path("/root/advanceddatabses/databaseassignment/physionet.org/files/ptb-xl/1.0.3")
collection_name = "ecg_embeddings"
sampling_rate_folder = "records100"  # using 100Hz version
vector_dim = 128  # must match collection config
max_signal_length = 100  # time steps to keep per lead

# === Load metadata ===
df = pd.read_csv(base_dir / "ptbxl_database.csv")

# Use low-res filenames
df['filename_hr'] = df['filename_lr']

# Parse scp_codes from string to dict
df['scp_codes'] = df['scp_codes'].apply(ast.literal_eval)

# Classify as normal if 'NORM' appears
df['is_normal'] = df['scp_codes'].apply(lambda codes: 'NORM' in codes)

# Sample balanced dataset: 5k normal + 5k abnormal
df_normal = df[df['is_normal']].sample(5000, random_state=42)
df_abnormal = df[~df['is_normal']].sample(5000, random_state=42)
df_balanced = pd.concat([df_normal, df_abnormal]).sample(frac=1, random_state=42).reset_index(drop=True)

# Split into train (8000) and test (2000)
df_train = df_balanced.iloc[:8000].copy()
df_test = df_balanced.iloc[8000:].copy()

# Remove repeated folder from paths
df_train['filename_hr'] = df_train['filename_hr'].str.replace(r'^records100/', '', regex=True)
df_test['filename_hr'] = df_test['filename_hr'].str.replace(r'^records100/', '', regex=True)

print("✅ Loaded and balanced 10,000 ECGs")
print(f"Train: {len(df_train)} | Test: {len(df_test)}")

# === Load ECG signal ===
def load_ecg_signal(record_path, base_dir):
    base_path = base_dir / sampling_rate_folder
    record = wfdb.rdrecord(base_path / record_path)
    return record.p_signal  # shape: (time, 12)

# === Preprocess: truncate/pad + flatten ===
def preprocess_signal(signal, max_length=max_signal_length):
    signal = signal[:, :max_length] if signal.shape[1] >= max_length else np.pad(signal, ((0, 0), (0, max_length - signal.shape[1])))
    flat = signal.flatten()
    return flat[:vector_dim]  # simple vector, can be replaced with model

# === Qdrant Setup ===
client = QdrantClient("localhost", port=6333)


print("\n🔍 Running similarity search on 2000 test ECGs...\n")
for idx, row in df_test.iterrows():
    try:
        signal = load_ecg_signal(row['filename_hr'], base_dir)
        vector = preprocess_signal(signal.T, max_length=max_signal_length)

        results = client.search(
            collection_name=collection_name,
            query_vector=vector.tolist(),
            limit=3
        )

        print(f"🧪 Query ECG ID {row['ecg_id']} (is_normal: {row['is_normal']}) — Top matches:")
        for hit in results:
            print(f"   → Match ID: {hit.id}, Score: {hit.score:.4f}, Normal: {hit.payload.get('is_normal')}, Label: {hit.payload.get('label')}")
        print("-" * 50)
    except Exception as e:
        print(f"⚠️ Query error on ECG ID {row['ecg_id']}: {e}")
