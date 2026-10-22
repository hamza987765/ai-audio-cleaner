import pkg_resources
import os
import sys
from scipy.signal import resample_poly
from fractions import Fraction
import numpy as np
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
print("pkg_resources imported successfully")
import tensorflow_hub as hub
print("tensorflow_hub imported successfully")
print("SOUND DETECTOR VERSION 999")
import setuptools
print("SETUPTOOLS VERSION:", setuptools.__version__)

import pkg_resources
print("PKG_RESOURCES OK")
import os
import json
import csv
import time
import soundfile as sf
import librosa

# ============================================================
# IMPORT TESTS
# ============================================================

print("IMPORT 1")

try:
    import tensorflow_hub as hub
    print("IMPORT HUB OK")
except Exception as e:
    print("IMPORT HUB FAILED:", e)
    raise

print("IMPORT 2")

try:
    import tensorflow as tf
    print("IMPORT TF OK")
except Exception as e:
    print("IMPORT TF FAILED:", e)
    raise

print("IMPORT 3")

try:
    import librosa
    print("IMPORT LIBROSA OK")
except Exception as e:
    print("IMPORT LIBROSA FAILED:", e)
    raise

print("IMPORTS COMPLETE")

# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_FILE = os.path.join(
    BASE_DIR,
    "temp",
    "audio.wav"
)

DETECTED_SOUNDS_FILE = os.path.join(
    BASE_DIR,
    "detected_sounds.json"
)

# ============================================================
# DEBUG
# ============================================================

print("========================================")
print("Sound Detector")
print("========================================")

print(f"Backend directory : {BASE_DIR}")
print(f"Audio file        : {AUDIO_FILE}")
print(f"Audio exists      : {os.path.exists(AUDIO_FILE)}")

if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(
        f"Audio file not found: {AUDIO_FILE}"
    )

# ============================================================
# LOAD YAMNET
# ============================================================

print("\nLoading YAMNET model...", flush=True)

try:
    model = hub.load(
        "https://tfhub.dev/google/yamnet/1"
    )
    print("YAMNET model loaded successfully.", flush=True)

except Exception as exc:
    print(
        f"YAMNET model loading failed: {exc!r}",
        flush=True
    )
    raise
# ============================================================
# LOAD AUDIO
# ============================================================

print("Loading audio...")

print("Checking audio file metadata...", flush=True)
print(f"Audio file size: {os.path.getsize(AUDIO_FILE)} bytes", flush=True)

info = sf.info(AUDIO_FILE)
print(f"Audio metadata: {info}", flush=True)

print("Starting librosa.load()...", flush=True)
load_start = time.time()

print("Reading WAV file with soundfile...", flush=True)
load_start = time.time()

audio_data, original_sr = sf.read(
    AUDIO_FILE,
    dtype="float32",
    always_2d=True
)

print(
    f"WAV decoded in {time.time() - load_start:.2f} seconds",
    flush=True
)
print(f"Original sample rate: {original_sr}", flush=True)
print(f"Original audio shape: {audio_data.shape}", flush=True)

# Convert stereo audio to mono, as librosa.load() did by default.
waveform = np.mean(audio_data, axis=1, dtype=np.float32)
sr = int(original_sr)

# Resample to 16 kHz for YAMNet.
if sr != 16000:
    print(f"Resampling {sr} Hz to 16000 Hz...", flush=True)

    resample_start = time.time()
    ratio = Fraction(16000, sr)

    waveform = resample_poly(
        waveform,
        up=ratio.numerator,
        down=ratio.denominator
    ).astype(np.float32)

    sr = 16000

    print(
        f"Resampling completed in "
        f"{time.time() - resample_start:.2f} seconds",
        flush=True
    )

print(f"Final sample rate: {sr}", flush=True)
print(f"Final waveform shape: {waveform.shape}", flush=True)

print(
    f"Audio loaded successfully in {time.time() - load_start:.2f} seconds",
    flush=True
)
print(f"Sample rate: {sr}", flush=True)
print(f"Waveform shape: {waveform.shape}", flush=True)

print(f"Sample rate   : {sr}")
print(f"Samples       : {len(waveform)}")
print(f"Duration      : {len(waveform) / sr:.2f} sec")

# ============================================================
# RUN MODEL - CHUNKED INFERENCE
# ============================================================

print("\nRunning detection...", flush=True)
print("Starting chunked YAMNet inference...", flush=True)

inference_start = time.time()

chunk_samples = 8 * 16000  # 8 seconds at 16 kHz
minimum_chunk_samples = 16000  # 1 second

score_parts = []
start = 0
chunk_number = 1

while start < len(waveform):
    end = min(start + chunk_samples, len(waveform))

    # Avoid creating a tiny final chunk.
    remaining = len(waveform) - end
    if 0 < remaining < minimum_chunk_samples:
        end = len(waveform)

    audio_chunk = waveform[start:end]

    print(
        f"YAMNet chunk {chunk_number}: "
        f"{start / 16000:.2f}s to {end / 16000:.2f}s",
        flush=True
    )

    scores, embeddings, spectrogram = model(audio_chunk)

    chunk_scores = scores.numpy()

    if chunk_scores.size > 0:
        score_parts.append(chunk_scores)

    print(
        f"Chunk {chunk_number} completed. "
        f"Scores shape: {chunk_scores.shape}",
        flush=True
    )

    del scores, embeddings, spectrogram, chunk_scores, audio_chunk

    start = end
    chunk_number += 1

if not score_parts:
    raise RuntimeError(
        "YAMNet returned no scores. Check the audio duration and model input."
    )

scores_np = np.concatenate(score_parts, axis=0)

print(
    f"All YAMNet chunks completed in "
    f"{time.time() - inference_start:.2f} seconds",
    flush=True
)
print(f"Combined scores shape: {scores_np.shape}", flush=True)
# ============================================================
# CLASS LABELS
# ============================================================

class_map_path = model.class_map_path().numpy().decode("utf-8")

class_names = []

with open(
    class_map_path,
    encoding="utf-8"
) as csv_file:

    reader = csv.DictReader(csv_file)

    for row in reader:
        class_names.append(
            row["display_name"]
        )

# ============================================================
# TOP DETECTIONS
# ============================================================

mean_scores = scores_np.mean(axis=0)

detected = []

for i in mean_scores.argsort()[-20:][::-1]:

    confidence = float(mean_scores[i])

    if confidence > 0.03:

        detected.append({
            "label": class_names[i],
            "confidence": round(confidence, 3)
        })

# ============================================================
# PRINT RESULTS
# ============================================================

print("\nDetected Sounds:\n")

for item in detected:

    print(
        f"{item['label']} : "
        f"{item['confidence']}"
    )

# ============================================================
# SAVE JSON
# ============================================================

with open(
    DETECTED_SOUNDS_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        detected,
        f,
        indent=4
    )

print(
    f"\nDetected sounds saved to:\n"
    f"{DETECTED_SOUNDS_FILE}"
)

print("\nSound detection completed.")