import tensorflow as tf
import tensorflow_hub as hub
import librosa
import numpy as np

print("Loading YAMNet model...")

model = hub.load("https://tfhub.dev/google/yamnet/1")

print("Loading audio...")

audio_path = "temp/audio.wav"

waveform, sr = librosa.load(
    audio_path,
    sr=16000,
    mono=True
)

waveform = waveform.astype(np.float32)

print("Running classification...")

scores, embeddings, spectrogram = model(waveform)

scores_np = scores.numpy()

mean_scores = scores_np.mean(axis=0)

class_map_path = model.class_map_path().numpy().decode("utf-8")

class_names = []

with tf.io.gfile.GFile(class_map_path) as f:
    next(f)

    for line in f:
        class_names.append(
            line.strip().split(",")[2]
        )

top_indices = np.argsort(mean_scores)[::-1][:10]

print("\nTop Detected Sounds:\n")

for i in top_indices:
    print(
        f"{class_names[i]}: "
        f"{mean_scores[i]:.4f}"
    )