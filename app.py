from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

markers = []  # temporarily in memory, or connect to database

@app.route('/api/markers', methods=['GET', 'POST'])
def handle_markers():
    global markers
    if request.method == 'POST':
        data = request.get_json()
        markers.append(data)  # data = {lat:..., lng:...}
        return jsonify({"status": "ok"})
    return jsonify(markers)

if __name__ == '__main__':
    app.run(debug=True)
