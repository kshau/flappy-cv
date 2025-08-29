from dotenv import load_dotenv
load_dotenv()

from ultralytics import YOLO
import cv2
import os

from game import run_game

FPS = int(os.environ["FPS"])
OPENCV_VIDEO_CAPTURE_SRC = int(os.environ["OPENCV_VIDEO_CAPTURE_SRC"])

model = YOLO("yolo11n-pose.pt")

cap = cv2.VideoCapture(OPENCV_VIDEO_CAPTURE_SRC)
cap.set(cv2.CAP_PROP_FPS, FPS)

running = True

left_eye_y = None
old_left_eye_y = None

while running:

    ret, frame = cap.read()
    if not ret:
        break

    result = model.track(frame, conf=0.5, verbose=False)[0]
    keypoints = result.keypoints.xy.cpu().numpy()

    if len(keypoints) > 0:
        person = keypoints[0]
        if len(person) > 0:

            old_left_eye_y = left_eye_y
            left_eye_x, left_eye_y = map(int, person[1])

            cv2.circle(frame, (left_eye_x, left_eye_y), 5, (0, 255, 0), 2)

    delta_left_eye_y = 0

    if left_eye_y and old_left_eye_y:
        delta_left_eye_y = left_eye_y - old_left_eye_y

    running = run_game(delta_left_eye_y)
    cv2.imshow("Controller", frame)