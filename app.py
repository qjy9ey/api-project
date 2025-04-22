from flask import Flask, jsonify, request
from datetime import datetime
import pytz

app = Flask(__name__)

# Secret token for authentication
API_TOKEN = "supersecrettoken123"

# Sample database of capital cities and their timezones
CAPITALS = {
    "London": "Europe/London",
    "New York": "America/New_York",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Berlin": "Europe/Berlin"
}

# Token check decorator
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

# Route to get the current time of a capital city
@app.route('/api/time/<city>', methods=['GET'])
@token_required
def get_time(city):
    if city in CAPITALS:
        timezone = pytz.timezone(CAPITALS[city])
        local_time = datetime.now(timezone)
        utc_offset = local_time.utcoffset().total_seconds() / 3600  # UTC Offset in hours
        response = {
            "city": city,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": utc_offset
        }
        return jsonify(response)
    else:
        return jsonify({"error": f"City '{city}' not found in the database."}), 404

# Test route (you already know this one from your class)
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
