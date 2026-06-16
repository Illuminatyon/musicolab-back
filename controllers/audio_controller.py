from flask import Blueprint, request, jsonify
import services.audio_service as audio_service

audio_controller = Blueprint('audio', __name__)


@audio_controller.route('/analyse', methods=['POST'])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier fourni"}), 400

    file = request.files["file"]

    result = audio_service.analyse_audio(file)

    return jsonify(result)
