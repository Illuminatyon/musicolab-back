import mido
import io


def process_transposition(file_stream, interval: int) -> io.BytesIO:
    """
    Prend un flux de fichier MIDI et un intervalle,
    manipule les données, et retourne un nouveau flux binaire.
    """
    # Charger le fichier MIDI depuis le flux
    mid = mido.MidiFile(file=file_stream)

    # Parcourir et transposer les notes
    for track in mid.tracks:
        for msg in track:
            if msg.type in ['note_on', 'note_off']:
                new_note = msg.note + interval
                msg.note = max(0, min(127, new_note))  # Limites MIDI

    # Sauvegarder le résultat en mémoire
    out_buffer = io.BytesIO()
    mid.save(file=out_buffer)
    out_buffer.seek(0)

    return out_buffer