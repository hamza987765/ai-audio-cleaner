import os
import shutil


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LAYERS_DIR = os.path.join(
    BASE_DIR,
    "layers"
)

SOURCE_DIR = os.path.join(
    BASE_DIR,
    "separated",
    "htdemucs",
    "audio"
)

os.makedirs(
    LAYERS_DIR,
    exist_ok=True
)


# ============================================================
# DEMUCS OUTPUT → APPLICATION LAYERS
# ============================================================

mapping = {
    "vocals.wav": "Speech.wav",
    "other.wav": "Music.wav",
    "drums.wav": "Drums.wav",
    "bass.wav": "Bass.wav"
}


print("========================================")
print("Layer Manager")
print("========================================")

print(f"Source directory : {SOURCE_DIR}")
print(f"Layers directory : {LAYERS_DIR}")


# ============================================================
# CREATE LAYERS
# ============================================================

for src, dst in mapping.items():

    source_file = os.path.join(
        SOURCE_DIR,
        src
    )

    destination_file = os.path.join(
        LAYERS_DIR,
        dst
    )

    if os.path.exists(source_file):

        shutil.copy2(
            source_file,
            destination_file
        )

        print(f"Created: {dst}")

    else:

        print(
            f"Missing source: {source_file}"
        )


print("Layer generation complete.")