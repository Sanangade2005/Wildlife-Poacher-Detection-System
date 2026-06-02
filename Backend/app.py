import os
import traceback
import shutil
from datetime import datetime


from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

from db import User, VideoDetection, PhotoDetection
from dependencies import get_db

from detector import find_first_poacher_frame, detect_poacher_in_image
from gemini_client import verify_with_gemini
from email_alert import send_poacher_alert
from gpt_client import ask_gpt

# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# -------------------------------------------------
# GLOBAL ERROR HANDLER
# -------------------------------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"DEBUG: Exception occurred: {e}")
    traceback.print_exc()
    return jsonify({
        "error": str(e),
        "trace": traceback.format_exc()
    }), 500

# -------------------------------------------------
# ROOT
# -------------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Poaching Detection Backend Running"})

# -------------------------------------------------
# REGISTER
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    db = get_db()

    try:
        # if data["password"] != data["repeat_password"]:
        #     return jsonify({"message": "Passwords do not match"}), 400

        if db.query(User).filter_by(
            email_or_phone=data["email_or_phone"]
        ).first():
            return jsonify({"message": "User already exists"}), 400

        user = User(
            ranger_id=data["ranger_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email_or_phone=data["email_or_phone"],
            password=generate_password_hash(data["password"])
        )

        db.add(user)
        db.commit()

        return jsonify({"message": "User registered successfully"}), 201

    finally:
        db.close()

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    db = get_db()

    try:
        user = db.query(User).filter_by(
            email_or_phone=data["email_or_phone"]
        ).first()

        if user and check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Login successful", "ranger_id": user.ranger_id,
        "first_name": user.first_name}), 200

        return jsonify({"message": "Invalid credentials"}), 401

    finally:
        db.close()

# -------------------------------------------------
# ASK AI
# -------------------------------------------------
@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    return jsonify({"answer": ask_gpt(question)})

# -------------------------------------------------
# VIDEO DETECTION
# -------------------------------------------------
@app.route("/video-detection", methods=["POST"])
def video_detection():
    if "video" not in request.files:
        return jsonify({"error": "video file is required"}), 400

    ranger_id = request.form.get("ranger_id")
    if not ranger_id:
        return jsonify({"error": "ranger_id is required"}), 400

    video_file = request.files["video"]

    upload_dir = os.path.join(BASE_DIR, "uploads", "videos")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(
        upload_dir, f"{ranger_id}_{timestamp}_{video_file.filename}"
    )
    video_file.save(video_path)

    # 🔹 YOUR DETECTION LOGIC (unchanged)
    # result = find_first_poacher_frame(video_path)
    # if not result:
    #     return jsonify({"yolo_detected": False})

    result = find_first_poacher_frame(video_path)
    if not result:
        db = get_db()
        try:
            record = VideoDetection(
                ranger_id=ranger_id,
                frame_path=video_path,
                yolo_detected=False,
                gemini_detected=False,
                gemini_confidence=0.0,
                gemini_reason="No threat detected"
            )
            db.add(record)
            db.commit()
        finally:
            db.close()

        return jsonify({
            "yolo_detected": False,
            "message": "No threat detected"
        })



    frame_path, frame_no = result

    frames_dir = os.path.join(BASE_DIR, "frames", "detected")
    os.makedirs(frames_dir, exist_ok=True)

    new_frame_path = os.path.join(
        frames_dir, f"{ranger_id}_{timestamp}_frame_{frame_no}.jpg"
    )
    shutil.move(frame_path, new_frame_path)

    gemini_result = verify_with_gemini(new_frame_path)

    db = get_db()
    try:
        record = VideoDetection(
            ranger_id=ranger_id,
            frame_path=new_frame_path,
            yolo_detected=True,
            gemini_detected=gemini_result["detected"],
            gemini_confidence=gemini_result["confidence"],
            gemini_reason=gemini_result["reason"]
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    if gemini_result["detected"]:
        send_poacher_alert(
            new_frame_path,
            ranger_id,
            timestamp,
            gemini_result["reason"]
        )

    return jsonify({
        "yolo_detected": True,
        "gemini_verification": gemini_result
    })

# -------------------------------------------------
# PHOTO DETECTION
# -------------------------------------------------
@app.route("/photo-detection", methods=["POST"])
def photo_detection():
    if "image" not in request.files:
        return jsonify({"error": "image file is required"}), 400

    ranger_id = request.form.get("ranger_id")
    if not ranger_id:
        return jsonify({"error": "ranger_id is required"}), 400

    image_file = request.files["image"]

    upload_dir = os.path.join(BASE_DIR, "uploads", "images")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(
        upload_dir, f"{ranger_id}_{timestamp}_{image_file.filename}"
    )
    image_file.save(image_path)

    # ----- YOUR EXISTING DETECTION LOGIC (UNCHANGED) -----
    # if not detect_poacher_in_image(image_path):
    #     return jsonify({"yolo_detected": False})

    if not detect_poacher_in_image(image_path):
        db = get_db()
        try:
            record = PhotoDetection(
                ranger_id=ranger_id,
                image_path=image_path,
                yolo_detected=False,
                gemini_detected=False,
                gemini_confidence=0.0,
                gemini_reason="No threat detected"
            )
            db.add(record)
            db.commit()
        finally:
            db.close()

        return jsonify({
            "yolo_detected": False,
            "message": "No threat detected"
        })

    frames_dir = os.path.join(BASE_DIR, "frames", "detected")
    os.makedirs(frames_dir, exist_ok=True)

    new_image_path = os.path.join(
        frames_dir, f"{ranger_id}_{timestamp}_photo.jpg"
    )
    shutil.copy(image_path, new_image_path)

    gemini_result = verify_with_gemini(new_image_path)

    db = get_db()
    try:
        record = PhotoDetection(
            ranger_id=ranger_id,
            image_path=new_image_path,
            yolo_detected=True,
            gemini_detected=gemini_result["detected"],
            gemini_confidence=gemini_result["confidence"],
            gemini_reason=gemini_result["reason"]
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    if gemini_result["detected"]:
        send_poacher_alert(
            new_image_path,
            ranger_id,
            timestamp,
            gemini_result["reason"]
        )

    return jsonify({
        "yolo_detected": True,
        "gemini_verification": gemini_result
    })

# -------------------------------------------------
# ALERT HISTORY (for frontend History page)
# -------------------------------------------------
@app.route("/test")
def test():
    return {"msg": "Flask is alive"}

@app.route("/alert-history", methods=["GET"])
def alert_history():
    db = get_db()
    try:
        photo_records = db.query(PhotoDetection).all()
        video_records = db.query(VideoDetection).all()

        history = []

        for p in photo_records:
            history.append({
                "datetime": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
                "date": p.created_at.strftime("%d-%m-%Y") if p.created_at else "N/A",
                "type": "Photo",
                "status": "Alert Sent" if p.gemini_detected else "No Threat"
            })

        for v in video_records:
            history.append({
                "datetime": v.created_at.strftime("%Y-%m-%d %H:%M:%S") if v.created_at else None,
                "date": v.created_at.strftime("%d-%m-%Y") if v.created_at else "N/A",
                "type": "Video",
                "status": "Alert Sent" if v.gemini_detected else "No Threat"
            })

        # Sort newest first
        # history = sorted(history, key=lambda x: x["date"], reverse=True)
        # history = sorted(history, key=lambda x: x["datetime"] or "", reverse=True)
        history.sort(
            key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )


        return jsonify({"history": history})

    except Exception as e:
        print("HISTORY ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()

# -------------------------------------------------
# OFFICER PROFILE
# -------------------------------------------------
@app.route("/officer-profile/<ranger_id>", methods=["GET"])
def get_officer_profile(ranger_id):
    db = get_db()
    try:
        user = db.query(User).filter_by(ranger_id=ranger_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_or_phone": user.email_or_phone,
            "ranger_id": user.ranger_id
        }), 200
    finally:
        db.close()

@app.route("/officer-profile/<ranger_id>", methods=["PUT"])
def update_officer_profile(ranger_id):
    data = request.get_json(force=True)
    db = get_db()
    try:
        user = db.query(User).filter_by(ranger_id=ranger_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "email_or_phone" in data:
            user.email_or_phone = data["email_or_phone"]
        if "password" in data and data["password"]:
            user.password = generate_password_hash(data["password"])

        db.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)