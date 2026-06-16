from flask import Blueprint, request, send_file, jsonify
import services.midi_service as midi_service

midi_controller = Blueprint('midi', __name__, url_prefix='/api/midi')


@midi_controller.route('/transpose', methods=['POST'])
def transpose_midi():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Fichier vide'}), 400

    try:
        interval = int(request.form.get('interval', 0))
    except ValueError:
        return jsonify({'error': 'Intervalle invalide'}), 400

    try:
        out_buffer = midi_service.process_transposition(file, interval)

        return send_file(
            out_buffer,
            mimetype='audio/midi',
            as_attachment=True,
            download_name=f"transposed_{file.filename}"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500