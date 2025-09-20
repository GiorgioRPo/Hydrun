from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

CSV_FILE = "locations.csv"

# Read CSV
def read_locations():
    locations = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    lat = float(row["Lat"])
                    lng = float(row["Long"])
                    name = row.get("Name", "")
                    folder = row.get("Folder", "")
                    level = row.get("Level", "")
                    temp = row.get("Temp", "")
                    operator = row.get("Operator", "")
                    locations.append({
                        "lat": lat,
                        "lng": lng,
                        "name": name,
                        "folder": folder,
                        "level": level,
                        "temp": temp,
                        "operator": operator
                    })
                except ValueError:
                    continue  # skip invalid rows
    return locations

# Append to CSV
def append_location(data):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["index", "Folder", "Name", "Level", "Temp", "Operator", "Lat", "Long"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        # Generate a new index
        new_index = sum(1 for _ in open(CSV_FILE)) if file_exists else 1
        row = {
            "index": new_index,
            "Folder": data.get("folder", ""),
            "Name": data.get("name", ""),
            "Level": data.get("level", ""),
            "Temp": data.get("temp", ""),
            "Operator": data.get("operator", ""),
            "Lat": data.get("lat"),
            "Long": data.get("lng")
        }
        writer.writerow(row)

# GET all markers
@app.route("/api/locations", methods=["GET"])
def get_locations():
    return jsonify(read_locations())

# POST a new marker
@app.route("/api/locations", methods=["POST"])
def add_location():
    data = request.get_json()
    if not data or "lat" not in data or "lng" not in data:
        return jsonify({"error": "lat and lng required"}), 400
    append_location(data)
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

