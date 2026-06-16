import io

import mido
import pytest

from app import app


@pytest.fixture
def client():
    """Client de test Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def build_midi_bytes(notes):
    """Construit un fichier MIDI en mémoire à partir d'une liste de hauteurs."""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        track.append(mido.Message('note_on', note=note, velocity=64, time=0))
        track.append(mido.Message('note_off', note=note, velocity=64, time=480))

    buffer = io.BytesIO()
    mid.save(file=buffer)
    buffer.seek(0)
    return buffer


def read_notes(data):
    """Extrait la liste des hauteurs de notes d'un contenu MIDI binaire."""
    mid = mido.MidiFile(file=io.BytesIO(data))
    return [
        msg.note
        for track in mid.tracks
        for msg in track
        if msg.type in ('note_on', 'note_off')
    ]


def test_transpose_succes():
    """Un POST valide retourne le fichier MIDI transposé."""
    client_app = app.test_client()
    midi = build_midi_bytes([60, 62])

    response = client_app.post(
        '/api/midi/transpose',
        data={'file': (midi, 'morceau.mid'), 'interval': '2'},
        content_type='multipart/form-data',
    )

    assert response.status_code == 200
    assert response.mimetype == 'audio/midi'
    assert 'transposed_morceau.mid' in response.headers['Content-Disposition']
    assert read_notes(response.data) == [62, 62, 64, 64]


def test_transpose_sans_fichier(client):
    """Sans champ 'file', l'API renvoie 400."""
    response = client.post(
        '/api/midi/transpose',
        data={'interval': '2'},
        content_type='multipart/form-data',
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Aucun fichier fourni'


def test_transpose_fichier_vide(client):
    """Un fichier sans nom (vide) renvoie 400."""
    response = client.post(
        '/api/midi/transpose',
        data={'file': (io.BytesIO(b''), ''), 'interval': '2'},
        content_type='multipart/form-data',
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Fichier vide'


def test_transpose_intervalle_invalide(client):
    """Un intervalle non numérique renvoie 400."""
    midi = build_midi_bytes([60])

    response = client.post(
        '/api/midi/transpose',
        data={'file': (midi, 'morceau.mid'), 'interval': 'abc'},
        content_type='multipart/form-data',
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Intervalle invalide'


def test_transpose_intervalle_par_defaut(client):
    """Sans intervalle fourni, la valeur par défaut (0) est utilisée."""
    midi = build_midi_bytes([60, 64])

    response = client.post(
        '/api/midi/transpose',
        data={'file': (midi, 'morceau.mid')},
        content_type='multipart/form-data',
    )

    assert response.status_code == 200
    assert read_notes(response.data) == [60, 60, 64, 64]


def test_transpose_fichier_corrompu(client):
    """Un fichier qui n'est pas du MIDI valide renvoie 500."""
    faux = io.BytesIO(b'pas du tout un fichier midi')

    response = client.post(
        '/api/midi/transpose',
        data={'file': (faux, 'corrompu.mid'), 'interval': '2'},
        content_type='multipart/form-data',
    )

    assert response.status_code == 500
    assert 'error' in response.get_json()
