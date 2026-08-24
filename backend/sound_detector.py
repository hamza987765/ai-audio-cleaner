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

try:
    import pkg_resources
    print("pkg_resources OK")
except Exception as e:
    print(f"pkg_resources ERROR: {e}")

import os
import json
import csv

import tensorflow_hub as hub
import tensorflow as tf
import librosa


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
# DEBUG / PATH CHECK
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
# LOAD YAMNET MODEL
# ============================================================

print("\nLoading model...")

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

print(f"Sample rate       : {sr}")
print(f"Audio samples     : {len(waveform)}")
print(f"Duration          : {len(waveform) / sr:.2f} seconds")


# ============================================================
# RUN YAMNET
# ============================================================

print("\nRunning sound detection...")

scores, embeddings, spectrogram = model(waveform)

scores_np = scores.numpy()


# ============================================================
# LOAD CLASS NAMES
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
# CALCULATE MEAN SCORES
# ============================================================

mean_scores = scores_np.mean(axis=0)

detected = []


# ============================================================
# SELECT TOP DETECTIONS
# ============================================================

for i in mean_scores.argsort()[-20:][::-1]:

    label = class_names[i]

    confidence = float(
        mean_scores[i]
    )

    if confidence > 0.03:

        detected.append({
            "label": label,
            "confidence": round(
                confidence,
                3
            )
        })


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nDetected Sounds:\n")

for item in detected:

    print(
        f"{item['label']} : "
        f"{item['confidence']}"
    )


print("\nRaw Detection List:\n")

print(detected)


# ============================================================
# SAVE RESULTS
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