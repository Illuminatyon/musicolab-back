import io

import mido
import pytest

import services.midi_service as midi_service


def build_midi(notes):
    """Construit un fichier MIDI en mémoire à partir d'une liste de hauteurs de notes.

    Pour chaque note, on génère un couple note_on / note_off.
    Retourne un flux binaire (BytesIO) prêt à être lu par process_transposition.
    """
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


def read_notes(buffer):
    """Extrait la liste des hauteurs de notes d'un flux MIDI."""
    buffer.seek(0)
    mid = mido.MidiFile(file=buffer)
    return [
        msg.note
        for track in mid.tracks
        for msg in track
        if msg.type in ('note_on', 'note_off')
    ]


def test_transposition_positive():
    """Un intervalle positif décale toutes les notes vers le haut."""
    source = build_midi([60, 62, 64])  # Do, Ré, Mi

    result = midi_service.process_transposition(source, 2)

    assert read_notes(result) == [62, 62, 64, 64, 66, 66]


def test_transposition_negative():
    """Un intervalle négatif décale toutes les notes vers le bas."""
    source = build_midi([60, 64, 67])

    result = midi_service.process_transposition(source, -5)

    assert read_notes(result) == [55, 55, 59, 59, 62, 62]


def test_transposition_interval_zero_inchange():
    """Un intervalle nul laisse les notes inchangées."""
    source = build_midi([10, 50, 90])

    result = midi_service.process_transposition(source, 0)

    assert read_notes(result) == [10, 10, 50, 50, 90, 90]


def test_transposition_borne_superieure():
    """Les notes ne peuvent pas dépasser 127 (limite MIDI)."""
    source = build_midi([120, 127])

    result = midi_service.process_transposition(source, 20)

    assert read_notes(result) == [127, 127, 127, 127]


def test_transposition_borne_inferieure():
    """Les notes ne peuvent pas descendre sous 0 (limite MIDI)."""
    source = build_midi([5, 0])

    result = midi_service.process_transposition(source, -20)

    assert read_notes(result) == [0, 0, 0, 0]


def test_retourne_bytesio_au_debut():
    """Le résultat est un BytesIO non vide, positionné au début."""
    source = build_midi([60])

    result = midi_service.process_transposition(source, 1)

    assert isinstance(result, io.BytesIO)
    assert result.tell() == 0
    assert len(result.getvalue()) > 0


def test_fichier_invalide_leve_exception():
    """Un flux qui n'est pas un fichier MIDI déclenche une exception."""
    invalide = io.BytesIO(b'ceci n est pas un fichier midi')

    with pytest.raises(Exception):
        midi_service.process_transposition(invalide, 2)
