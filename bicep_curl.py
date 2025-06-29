import cv2
import mediapipe as mp
import numpy as np
import math
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle between joints
def calculate_angle(a, b, c):
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Elbow
    c = np.array(c)  # Wrist

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Initialize video capture
cap = cv2.VideoCapture(0)

counter_right = 0
stage_right = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Set default values
        right_color = (255, 255, 255)
        posture_status = "No Detection"

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angle
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Determine posture correctness
            if abs(right_shoulder[0] - right_elbow[0]) < 0.1:
                right_color = (0, 255, 0)
                posture_status = "Correct Posture"
            else:
                right_color = (0, 0, 255)
                posture_status = "Incorrect Posture"

            # Rep counting
            if right_angle > 160:
                stage_right = "down"
            if right_angle < 30 and stage_right == "down":
                stage_right = "up"
                counter_right += 1

            # Draw arm lines
            cv2.line(image, tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                     tuple(np.multiply(right_elbow, [640, 480]).astype(int)), right_color, 2)
            cv2.line(image, tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                     tuple(np.multiply(right_wrist, [640, 480]).astype(int)), right_color, 2)

        except Exception as e:
            cv2.putText(image, "No Landmarks Detected", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display data on screen
        cv2.putText(image, 'Bicep Curl', (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(image, 'Reps: ' + str(counter_right), (250, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(image, posture_status, (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, right_color, 2)

        # Show frame
        cv2.imshow('Arm Exercise Tracker', image)

        # Press 'q' to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Save reps to file
os.makedirs("data", exist_ok=True)
with open("data/reps_bicep_curl.txt", "w") as f:
    f.write(str(counter_right))

# Release and close
cap.release()
cv2.destroyAllWindows()
