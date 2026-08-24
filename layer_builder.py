import json

with open("detected_sounds.json", "r") as f:
    sounds = json.load(f)

layers = {}

for sound in sounds:
    layers[sound["label"]] = {
        "enabled": True,
        "confidence": sound["confidence"],
        "file": None
    }

with open("layers.json", "w") as f:
    json.dump(layers, f, indent=4)

print("Layers created.")