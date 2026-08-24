import os
import sys
import subprocess


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


def run_script(script_name):

    script_path = os.path.join(
        BASE_DIR,
        script_name
    )

    print(f"\nRunning: {script_name}")

    subprocess.run(
        [
            sys.executable,
            script_path
        ],
        check=True
    )


def process_video():

    print("\n========================================")
    print("VIDEO PROCESSING PIPELINE")
    print("========================================")

    # ==========================================
    # STEP 1 - EXTRACT AUDIO
    # ==========================================

    print("\nStep 1 - Extract Audio")

    run_script("app.py")

    # ==========================================
    # STEP 2 - DETECT SOUNDS
    # ==========================================

    print("\nStep 2 - Detect Sounds")

    run_script("sound_detector.py")

    # ==========================================
    # STEP 3 - SEPARATE AUDIO
    # ==========================================

    print("\nStep 3 - Separate Audio")

    run_script("separate_audio.py")

    # ==========================================
    # STEP 4 - CREATE LAYERS
    # ==========================================

    print("\nStep 4 - Create Layers")

    run_script("layer_manager.py")

    # ==========================================
    # RETURN AVAILABLE LAYERS
    # ==========================================

    return [
        "Speech.wav",
        "Music.wav",
        "Drums.wav",
        "Bass.wav"
    ]