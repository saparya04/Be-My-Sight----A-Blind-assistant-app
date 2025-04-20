from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import subprocess
import sys
import os
import smtplib
from email.message import EmailMessage


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

@app.route("/run-currency-detection", methods=["POST"])
def run_currency_detection():
    try:
        print("Trigger received for currency detection...")

        python_cmd = "python3" if sys.platform != "win32" else "python"

        process = subprocess.Popen([python_cmd, "detection.py"])
        print(f"Currency detection started with PID: {process.pid}")

        return jsonify({"status": "success", "message": "Currency detection started!"})

    except Exception as e:
        print("Error starting currency detection:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

    
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    to_email = data.get("to")
    message_body = data.get("message")

    try:
        # Setup email
        msg = EmailMessage()
        msg["Subject"] = "Message from Be My Sight Assistant"
        msg["From"] = "saparyadey2019@gmail.com"  # Replace with your email
        msg["To"] = to_email
        msg.set_content(message_body)

        # Send the email (example with Gmail SMTP)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("saparyadey2019@gmail.com", "ospk rkdz fceh voym")  # Use App Password if using Gmail
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": "Email sent"})

    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"status": "error", "message": str(e)})

@app.route("/welcome")
def welcome():
    return jsonify({"message": "Welcome message from Flask backend!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(debug=True, host="0.0.0.0", port=port)