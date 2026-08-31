import ffmpeg
import os


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

VIDEO = os.path.join(
    BASE_DIR,
    "input",
    "video.mp4"
)

AUDIO = os.path.join(
    BASE_DIR,
    "output",
    "final_audio.wav"
)

OUTPUT = os.path.join(
    BASE_DIR,
    "output",
    "final_video.mp4"
)


# ============================================================
# CHECK FILES
# ============================================================

print("========================================")
print("Final Video Renderer")
print("========================================")


print(f"Video           : {VIDEO}")
print(f"Audio           : {AUDIO}")
print(f"Output          : {OUTPUT}")


if not os.path.exists(VIDEO):
    raise FileNotFoundError(
        f"Video not found: {VIDEO}"
    )

if not os.path.exists(AUDIO):
    raise FileNotFoundError(
        f"Audio not found: {AUDIO}"
    )





# ============================================================
# RENDER
# ============================================================

print("\nRendering final video...")


video = ffmpeg.input(VIDEO).video

audio = ffmpeg.input(AUDIO).audio


(
    ffmpeg
    .output(
        video,
        audio,
        OUTPUT,
        vcodec="copy",
        acodec="aac"
    )
    .run(overwrite_output=True)
)


# ============================================================
# COMPLETE
# ============================================================

print("\n========================================")
print("Rendering completed successfully")
print("========================================")

print(f"Final video: {OUTPUT}")