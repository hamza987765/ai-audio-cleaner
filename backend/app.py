import ffmpeg
import os

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-9.0.1-essentials_build\bin"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO = os.path.join(BASE_DIR, "input", "video.mp4")
AUDIO = os.path.join(BASE_DIR, "temp", "audio.wav")
OUTPUT = os.path.join(BASE_DIR, "output", "result.mp4")

os.makedirs(os.path.join(BASE_DIR, "temp"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)

print("Extracting audio...")

(
    ffmpeg
    .input(VIDEO)
    .output(AUDIO)
    .run(overwrite_output=True)
)

print("Merging audio back into video...")

(
    ffmpeg
    .output(
        ffmpeg.input(VIDEO).video,
        ffmpeg.input(AUDIO).audio,
        OUTPUT,
        vcodec="copy"
    )
    .run(overwrite_output=True)
)

print("Done!")