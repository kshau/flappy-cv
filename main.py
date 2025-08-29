from ultralytics import YOLO
import cv2

model = YOLO("yolo11n-pose.pt")

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 30)

bird_img = cv2.imread("./assets/bird.png", cv2.IMREAD_UNCHANGED)
    

while True:

    ret, frame = cap.read()
    if not ret:
        break

    result = model.track(frame, conf=0.5, verbose=False)[0]
    keypoints = result.keypoints.xy.cpu().numpy()

    if (len(keypoints) > 0):
        person = keypoints[0]

        left_eye_x, left_eye_y = map(int, person[1])
        right_eye_x, right_eye_y = map(int, person[2])

        cv2.circle(frame, center=(left_eye_x, left_eye_y), radius=5, color=(0, 255, 0), thickness=2)
        cv2.circle(frame, center=(right_eye_x, right_eye_y), radius=5, color=(0, 255, 0), thickness=2)

        bird_y = left_eye_y
        bird_x = 50

        bird_h, bird_w = bird_img.shape[:2]

        cv2.addWeighted(frame[bird_y:bird_y+bird_h, bird_x:bird_x+bird_h], 0, bird_img, 1, 0)


    cv2.imshow("Flappy", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break