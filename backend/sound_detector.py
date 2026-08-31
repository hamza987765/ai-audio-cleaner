import os
import json
import csv

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

print("\nLoading YAMNET model...")

model = hub.load(
    "https://tfhub.dev/google/yamnet/1"
)

# ============================================================
# LOAD AUDIO
# ============================================================

print("Loading audio...")

waveform, sr = librosa.load(
    AUDIO_FILE,
    sr=16000
)

print(f"Sample rate   : {sr}")
print(f"Samples       : {len(waveform)}")
print(f"Duration      : {len(waveform) / sr:.2f} sec")

# ============================================================
# RUN MODEL
# ============================================================

print("\nRunning detection...")

scores, embeddings, spectrogram = model(waveform)

scores_np = scores.numpy()

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