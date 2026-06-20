import io

import numpy as np
import pytest
import soundfile as sf

import services.audio_service as audio_service


def build_wav(duration=1.0, sr=22050, freq=440.0, stereo=False):
    """Construit un fichier WAV en mémoire (sinusoïde) prêt à être analysé.

    Retourne un flux binaire (BytesIO) positionné au début, équivalent au
    flux fourni par Flask via request.files["file"].
    """
    t = np.arange(int(duration * sr)) / sr
    mono = 0.5 * np.sin(2 * np.pi * freq * t)

    data = np.column_stack([mono, mono]) if stereo else mono

    buffer = io.BytesIO()
    sf.write(buffer, data, sr, format="WAV")
    buffer.seek(0)
    return buffer


def test_analyse_signal_mono():
    """Un signal mono est détecté comme ayant 1 canal."""
    wav = build_wav(stereo=False)

    result = audio_service.analyse_audio(wav)

    assert result["channels"] == 1


def test_analyse_signal_stereo():
    """Un signal stéréo est détecté comme ayant 2 canaux."""
    wav = build_wav(stereo=True)

    result = audio_service.analyse_audio(wav)

    assert result["channels"] == 2


def test_analyse_duree_et_sample_rate():
    """La durée et la fréquence d'échantillonnage sont correctement extraites."""
    wav = build_wav(duration=1.0, sr=22050)

    result = audio_service.analyse_audio(wav)

    assert result["sample_rate"] == 22050
    assert result["duration"] == pytest.approx(1.0, rel=0.01)


def test_analyse_waveform_500_points():
    """La forme d'onde est toujours sous-échantillonnée à 500 points."""
    wav = build_wav()

    result = audio_service.analyse_audio(wav)

    assert len(result["waveform"]) == 500


def test_analyse_contient_toutes_les_cles():
    """Le résultat expose l'ensemble des champs attendus par le front."""
    wav = build_wav()

    result = audio_service.analyse_audio(wav)

    for cle in ("duration", "sample_rate", "channels", "waveform", "freqs", "spectrum"):
        assert cle in result
