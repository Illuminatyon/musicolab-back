import io

import numpy as np
import pytest
import soundfile as sf

from app import app


@pytest.fixture
def client():
    """Client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def build_wav(duration=1.0, sr=22050, freq=440.0):
    """Construit un fichier WAV mono en mémoire."""
    t = np.arange(int(duration * sr)) / sr
    mono = 0.5 * np.sin(2 * np.pi * freq * t)

    buffer = io.BytesIO()
    sf.write(buffer, mono, sr, format="WAV")
    buffer.seek(0)
    return buffer


def test_analyse_sans_fichier(client):
    """Sans champ 'file', l'API renvoie 400."""
    response = client.post(
        '/analyse',
        data={},
        content_type='multipart/form-data',
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Aucun fichier fourni'


def test_analyse_fichier_valide(client):
    """Un POST avec un fichier audio valide renvoie l'analyse en JSON."""
    wav = build_wav()

    response = client.post(
        '/analyse',
        data={'file': (wav, 'son.wav')},
        content_type='multipart/form-data',
    )

    assert response.status_code == 200

    data = response.get_json()
    for cle in ("duration", "sample_rate", "channels", "waveform", "freqs", "spectrum"):
        assert cle in data
    assert data["channels"] == 1
    assert data["sample_rate"] == 22050
