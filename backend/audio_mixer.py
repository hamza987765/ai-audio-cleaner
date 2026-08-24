from pydub import AudioSegment
import json
import os

FFMPEG_DIR = r"C:\ffmpeg-9.0.1-essentials_build\bin"

AudioSegment.converter = os.path.join(
    FFMPEG_DIR,
    "ffmpeg.exe"
)
# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LAYERS_DIR = os.path.join(
    BASE_DIR,
    "layers"
)

SELECTION_FILE = os.path.join(
    BASE_DIR,
    "user_selection.json"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

OUTPUT_AUDIO = os.path.join(
    OUTPUT_DIR,
    "final_audio.wav"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD USER SELECTION
# ============================================================

print("========================================")
print("Audio Mixer")
print("========================================")

print(f"Selection file : {SELECTION_FILE}")
print(f"Layers folder  : {LAYERS_DIR}")
print(f"Output audio   : {OUTPUT_AUDIO}")


with open(SELECTION_FILE, "r") as f:
    selection = json.load(f)


print("\nSelected layers:")

for layer in selection["keep"]:
    print(f"  - {layer}")


# ============================================================
# MIX AUDIO
# ============================================================

audio = None

for layer in selection["keep"]:

    layer_path = os.path.join(
        LAYERS_DIR,
        layer
    )

    if not os.path.exists(layer_path):
        raise FileNotFoundError(
            f"Layer not found: {layer_path}"
        )

    print(f"\nLoading: {layer}")

    track = AudioSegment.from_wav(
        layer_path
    )

    if audio is None:
        audio = track
    else:
        audio = audio.overlay(track)


# ============================================================
# EXPORT
# ============================================================

if audio is None:
    raise ValueError(
        "No audio layers selected."
    )


audio.export(
    OUTPUT_AUDIO,
    format="wav"
)

print("\nAudio mixing completed.")
print(f"Created: {OUTPUT_AUDIO}")