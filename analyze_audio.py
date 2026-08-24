import librosa

audio_file = "temp/audio.wav"

y, sr = librosa.load(audio_file)

duration = librosa.get_duration(y=y, sr=sr)

print(f"Duration: {duration:.2f} seconds")
print(f"Sample Rate: {sr}")
print(f"Samples: {len(y)}")