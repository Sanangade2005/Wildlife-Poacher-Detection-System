from ultralytics import YOLO
import cv2
import os
from config import CONF_THRESHOLD

# Load model once
model = YOLO("models/poacher.pt")

# Process only 1 out of every N frames (speed boost)
FRAME_SKIP = 10

def detect_poacher_in_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    frame = cv2.imread(image_path)
    if frame is None:
        raise RuntimeError("Could not read image")

    results = model(frame, conf=CONF_THRESHOLD)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label.lower() == "poacher":
                return True  # YOLO detected poacher

    return False

def find_first_poacher_frame(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Could not open video file")

    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames for speed
        if frame_id % FRAME_SKIP != 0:
            frame_id += 1
            continue

        # Run YOLO
        results = model(frame, conf=CONF_THRESHOLD)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                if label.lower() == "poacher":
                    os.makedirs("frames/detected", exist_ok=True)

                    # TEMP save (will be renamed in app.py)
                    save_path = f"frames/detected/temp_frame_{frame_id}.jpg"
                    cv2.imwrite(save_path, frame)

                    cap.release()

                    # 🔥 RETURN BOTH PATH + FRAME NUMBER
                    return save_path, frame_id

        frame_id += 1

    cap.release()
    return None
