import wfdb
import matplotlib.pyplot as plt
import numpy as np

# Download record 101 (one of the samples)
wfdb.dl_database('mitdb', dl_dir='mit-bih-data', records=['101'])

# Load a record
record = wfdb.rdrecord('mit-bih-data/101')
annotation = wfdb.rdann('mit-bih-data/101', 'atr')

# Plot ECG signal
fig = wfdb.plot_wfdb(record=record, annotation=annotation, title='Record 101', return_fig=True)
fig.savefig('ecg_record_101.png')

# First lead (360Hz x 5s = 1800)
segment = record.p_signal[0:1800, 0]  # lead 0
normalized_segment = (segment - np.mean(segment)) / np.std(segment)

# 'N' = normal beat, 'V' = premature ventricular contraction, etc.
normal_indices = [i for i, symbol in enumerate(annotation.symbol) if symbol == 'N']
abnormal_indices = [i for i, symbol in enumerate(annotation.symbol) if symbol != 'N']
