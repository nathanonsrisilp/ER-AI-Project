import os
from datetime import datetime

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ftm_rssi_log")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "ftm_rssi_col")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

current_state = "idle"


def serialize_report(doc):
    return {
        "id": str(doc["_id"]),
        "incident_type": doc.get("incident_type"),
        "injured": doc.get("injured"),
        "location": doc.get("location"),
        "severity": doc.get("severity"),
        "confidence": doc.get("confidence"),
        "transcript": doc.get("transcript"),
        "gps_lat": doc.get("gps_lat"),
        "gps_lon": doc.get("gps_lon"),
        "status": doc.get("status"),
        "source": doc.get("source"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


@app.route("/api/reports", methods=["POST"])
def create_report():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    now = datetime.utcnow().isoformat()

    report = {
        "incident_type": data.get("incident_type", "unknown"),
        "injured": data.get("injured", "unknown"),
        "location": data.get("location", "unknown"),
        "severity": data.get("severity", "unknown"),
        "confidence": data.get("confidence", "unknown"),
        "transcript": data.get("transcript", ""),
        "gps_lat": data.get("gps_lat"),
        "gps_lon": data.get("gps_lon"),
        "status": data.get("status", "pending"),
        "source": data.get("source", "unknown"),
        "created_at": now,
        "updated_at": now,
    }

    result = collection.insert_one(report)
    report["_id"] = result.inserted_id

    return jsonify({
        "message": "Report saved",
        "report": serialize_report(report)
    }), 201


@app.route("/api/reports", methods=["GET"])
def get_reports():
    status = request.args.get("status")
    query = {}

    if status:
        query["status"] = status

    docs = collection.find(query).sort("created_at", -1)
    return jsonify([serialize_report(doc) for doc in docs])


@app.route("/api/reports/<report_id>", methods=["GET"])
def get_report(report_id):
    try:
        doc = collection.find_one({"_id": ObjectId(report_id)})
    except Exception:
        return jsonify({"error": "Invalid report ID"}), 400

    if not doc:
        return jsonify({"error": "Report not found"}), 404

    return jsonify(serialize_report(doc))


@app.route("/api/reports/<report_id>", methods=["PUT"])
def update_report(report_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    update_fields = {
        "updated_at": datetime.utcnow().isoformat()
    }

    allowed_fields = [
        "incident_type",
        "injured",
        "location",
        "severity",
        "confidence",
        "transcript",
        "gps_lat",
        "gps_lon",
        "status",
        "source",
    ]

    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    try:
        result = collection.update_one(
            {"_id": ObjectId(report_id)},
            {"$set": update_fields}
        )
    except Exception:
        return jsonify({"error": "Invalid report ID"}), 400

    if result.matched_count == 0:
        return jsonify({"error": "Report not found"}), 404

    updated = collection.find_one({"_id": ObjectId(report_id)})

    return jsonify({
        "message": "Report updated",
        "report": serialize_report(updated)
    })


@app.route("/api/set-status", methods=["GET"])
def set_status_route():
    global current_state
    current_state = request.args.get("state", "idle")
    return jsonify({"ok": True, "state": current_state})


@app.route("/api/alert-status", methods=["GET"])
def alert_status():
    return jsonify({"state": current_state})


@app.route("/")
def home():
    return jsonify({"message": "ER-Helper backend is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)