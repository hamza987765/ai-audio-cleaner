import json
import shutil
import os

os.makedirs("layers", exist_ok=True)

MAPPING = {
    "Speech": "separated/htdemucs/audio/vocals.wav",
    "Music": "separated/htdemucs/audio/other.wav"
}

layers = {}

for name, source in MAPPING.items():

    if os.path.exists(source):

        destination = f"layers/{name}.wav"

        shutil.copy(source, destination)

        layers[name] = {
            "enabled": True,
            "file": destination
        }

with open("layers.json", "w") as f:
    json.dump(layers, f, indent=4)

print("Layers exported.")