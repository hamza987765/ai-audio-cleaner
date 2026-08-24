import os
import sys
import subprocess


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_AUDIO = os.path.join(
    BASE_DIR,
    "temp",
    "audio.wav"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "separated"
)


# ============================================================
# CHECK INPUT
# ============================================================

print("========================================")
print("Demucs Audio Separation")
print("========================================")

print(f"Input audio : {INPUT_AUDIO}")
print(f"Input exists: {os.path.exists(INPUT_AUDIO)}")
print(f"Output dir  : {OUTPUT_DIR}")


if not os.path.exists(INPUT_AUDIO):
    raise FileNotFoundError(
        f"Audio file not found: {INPUT_AUDIO}"
    )


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# RUN DEMUCS
# ============================================================

print("\nStarting Demucs separation...")

subprocess.run(
    [
        sys.executable,
        "-m",
        "demucs",
        INPUT_AUDIO,
        "-o",
        OUTPUT_DIR
    ],
    check=True
)


print("\nDemucs separation completed.")