import io
import numpy as np
import librosa


def analyse_audio(file_stream) -> dict:
    audio_bytes = io.BytesIO(file_stream.read())

    y, sr = librosa.load(audio_bytes, sr=None, mono=False)

    if y.ndim == 1:
        channels = 1
        y_mono = y
    else:
        channels = y.shape[0]
        y_mono = librosa.to_mono(y)

    duration = float(librosa.get_duration(y=y_mono, sr=sr))

    num_points = 500
    frame_length = max(1, len(y_mono) // num_points)
    frames = [
        float(np.max(np.abs(y_mono[i * frame_length:(i + 1) * frame_length])))
        for i in range(num_points)
    ]

    stft = np.abs(librosa.stft(y_mono))
    spectrum = np.mean(stft, axis=1).tolist()
    freqs = librosa.fft_frequencies(sr=sr).tolist()

    return {
        "duration": duration,
        "sample_rate": int(sr),
        "channels": channels,
        "waveform": frames,
        "freqs": freqs,
        "spectrum": spectrum,
    }
