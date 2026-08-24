import ffmpeg
import os


# ============================================================
# FFMPEG PATH
# ============================================================

FFMPEG_DIR = r"C:\ffmpeg-9.0.1-essentials_build\bin"

os.environ["PATH"] += os.pathsep + FFMPEG_DIR


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

print(f"FFmpeg directory: {FFMPEG_DIR}")
print(f"Video           : {VIDEO}")
print(f"Audio           : {AUDIO}")
print(f"Output          : {OUTPUT}")


FFMPEG_EXE = os.path.join(
    FFMPEG_DIR,
    "ffmpeg.exe"
)

if not os.path.exists(FFMPEG_EXE):
    raise FileNotFoundError(
        f"FFmpeg not found: {FFMPEG_EXE}"
    )

if not os.path.exists(VIDEO):
    raise FileNotFoundError(
        f"Video not found: {VIDEO}"
    )

if not os.path.exists(AUDIO):
    raise FileNotFoundError(
        f"Audio not found: {AUDIO}"
    )


print(f"FFmpeg executable: {FFMPEG_EXE}")


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
    .run(
        cmd=FFMPEG_EXE,
        overwrite_output=True
    )
)


# ============================================================
# COMPLETE
# ============================================================

print("\n========================================")
print("Rendering completed successfully")
print("========================================")

print(f"Final video: {OUTPUT}")