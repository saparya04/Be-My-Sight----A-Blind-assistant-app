from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS to allow fetch from JS

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/run-object-detection", methods=["POST"])
def run_object_detection():
    try:
        print("Trigger received for object detection...")

        # Determine Python command based on OS
        python_cmd = "python3" if sys.platform != "win32" else "python"

        # Run object detection script in a subprocess
        process = subprocess.Popen([python_cmd, "object.py"])
        print(f"Object detection started with PID: {process.pid}")

        return jsonify({"status": "success", "message": "Object detection started!"})

    except Exception as e:
        print("Error starting object detection:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/welcome")
def welcome():
    return jsonify({"message": "Welcome message from Flask backend!"})

if __name__ == "__main__":
    app.run(debug=True)
