from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse
import json
import subprocess
import shutil
import os

from backend.process_video import process_video

app = FastAPI()

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LAYERS_DIR = os.path.join(BASE_DIR, "layers")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LAYERS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "status": "running"
    }

# ==========================================
# UPLOAD VIDEO
# ==========================================

@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...)
):

    destination = os.path.join(
        INPUT_DIR,
        "video.mp4"
    )

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    layers = process_video()

    return {
        "success": True,
        "layers": layers
    }

# ==========================================
# RENDER VIDEO
# ==========================================

@app.post("/render")
async def render_video(
    data: dict = Body(...)
):

    selection_file = os.path.join(
        BASE_DIR,
        "user_selection.json"
    )

    with open(selection_file, "w") as f:
        json.dump(data, f)

    subprocess.run(
        [
            "python",
            os.path.join(BASE_DIR, "audio_mixer.py")
        ],
        check=True
    )

    subprocess.run(
        [
            "python",
            os.path.join(BASE_DIR, "final_render.py")
        ],
        check=True
    )

    return {
        "success": True,
        "download_url": "/download"
    }

# ==========================================
# DOWNLOAD VIDEO
# ==========================================

@app.get("/download")
def download_video():

    video_path = os.path.join(
        OUTPUT_DIR,
        "final_video.mp4"
    )

    if not os.path.exists(video_path):
        return {
            "success": False,
            "message": "Video not found"
        }

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename="cleaned_video.mp4"
    )