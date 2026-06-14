from flask import Flask, jsonify, render_template
from flask_cors import CORS
import threading

from sniffer import start_sniffing, ip_traffic

app = Flask(__name__)
CORS(app)

# Start traffic generator
threading.Thread(target=start_sniffing, daemon=True).start()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/live')
def live():

    if not ip_traffic:
        return jsonify({
            "attack_type": "Normal",
            "ip": "Waiting...",
            "lat": 20,
            "lon": 78,
            "country": "India"
        })

    # Most active IP
    ip = max(ip_traffic, key=lambda x: len(ip_traffic[x]))
    count = len(ip_traffic[ip])

    # Simple detection logic
    if count > 20:
        attack = "DDoS Attack"
    elif count > 10:
        attack = "Botnet Attack"
    else:
        attack = "Normal"

    return jsonify({
        "attack_type": attack,
        "ip": ip,
        "lat": 20.5937,
        "lon": 78.9629,
        "country": "India"
    })


if __name__ == "__main__":
    app.run(debug=True)