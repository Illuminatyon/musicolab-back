from flask import Flask
from flask_cors import CORS

from controllers.midi_controller import midi_controller
from controllers.audio_controller import audio_controller

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/analyse": {"origins": "*"}})

app.register_blueprint(midi_controller)
app.register_blueprint(audio_controller)

if __name__ == '__main__':
    app.run(debug=True, port=5000)