from flask import Flask
from flask_cors import CORS

from controllers.midi_controller import midi_controller

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(midi_controller)

if __name__ == '__main__':
    app.run(debug=True, port=5000)