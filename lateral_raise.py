import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Second point (vertex)
    c = np.array(c)  # Third point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Start capturing video
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Exercise state
counter_side = 0
stage_side = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detections
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for shoulder movement
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            # Calculate shoulder angle
            shoulder_angle = calculate_angle(hip, shoulder, elbow)

            # Determine stage and count reps
            if shoulder_angle > 150:
                stage_side = "start"
            if shoulder_angle < 70 and stage_side == "start":
                stage_side = "end"
                counter_side += 1

            # Draw lines for shoulder movement
            color = (0, 255, 0) if 30 < shoulder_angle < 150 else (0, 0, 255)

            cv2.line(image, tuple(np.multiply(hip, [640, 480]).astype(int)),
                     tuple(np.multiply(shoulder, [640, 480]).astype(int)), color, 2)
            cv2.line(image, tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                     tuple(np.multiply(elbow, [640, 480]).astype(int)), color, 2)

            # Display shoulder angle
            shoulder_coords = tuple(np.multiply(shoulder, [640, 480]).astype(int))
            cv2.putText(image, str(int(shoulder_angle)), shoulder_coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        except:
            cv2.putText(image, "No Landmarks Detected", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display headings and counter with spacing
        cv2.putText(image, 'Lateral Raise', (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Reps: ' + str(counter_side), (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        # Display the image
        cv2.imshow('Arm Exercise Tracker', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
