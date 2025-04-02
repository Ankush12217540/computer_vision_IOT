import cv2
import mediapipe as mp
import numpy as np
from math import sqrt
import serial

# Initialize Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Calculate Euclidean Distance
def euclidean_distance(pt1, pt2):
    return sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

# Set up the serial connection to the Arduino
ser = serial.Serial('COM16', 9600, timeout=1)  # Adjust the COM port as needed

# Video Capture
cap = cv2.VideoCapture(0)

# Get screen width and height
screen_width = 1920  # You can replace this with dynamic screen width detection
screen_height = 1080  # You can replace this with dynamic screen height detection

# Calculate 90% of screen size
window_width = int(screen_width * 0.9)
window_height = int(screen_height * 0.9)

# Create a named window with the specified size
cv2.namedWindow("Hand Distance Measurement", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Distance Measurement", window_width, window_height)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to access the camera.")
        break

    # Flip the frame horizontally for a natural feel and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    results = hands.process(rgb_frame)
    h, w, _ = frame.shape  # Get the frame dimensions

    # Lists to store left and right hand landmarks
    left_hand_center = None
    right_hand_center = None

    # Extract hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_class in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Determine if the hand is left or right
            hand_label = hand_class.classification[0].label  # 'Left' or 'Right'
            cx, cy = 0, 0

            for i, lm in enumerate(hand_landmarks.landmark):
                cx += lm.x * w
                cy += lm.y * h

            # Calculate the center of the palm
            cx = int(cx / 21)
            cy = int(cy / 21)

            # Store the palm center for the respective hand
            if hand_label == "Left":
                left_hand_center = (cx, cy)
            elif hand_label == "Right":
                right_hand_center = (cx, cy)

            # Draw hand landmarks and connections
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
            )

    # Calculate the distance between palms if both are detected
    if left_hand_center and right_hand_center:
        # Draw circles on palm centers
        cv2.circle(frame, left_hand_center, 10, (0, 255, 0), -1)
        cv2.circle(frame, right_hand_center, 10, (255, 0, 0), -1)

        # Draw a line connecting the palm centers
        cv2.line(frame, left_hand_center, right_hand_center, (0, 255, 255), 2)

        # Calculate and display the distance between the palms
        distance_between_palms = euclidean_distance(left_hand_center, right_hand_center)
        mid_point = ((left_hand_center[0] + right_hand_center[0]) // 2,
                     (left_hand_center[1] + right_hand_center[1]) // 2)

        cv2.putText(frame, f"{int(distance_between_palms)} px", mid_point,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the labels for the hands
        cv2.putText(frame, "Left Hand", (left_hand_center[0] - 50, left_hand_center[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Right Hand", (right_hand_center[0] + 20, right_hand_center[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Control motor speed based on palm distance
        if distance_between_palms < 60:
            motor_speed = 0  # Very Close: 0% speed
            ser.write(b'4')  # Send 0 to Arduino
        elif distance_between_palms < 130:
            motor_speed = 64  # Close: 25% speed
            ser.write(b'0')  # Send 1 to Arduino
        elif distance_between_palms < 200:
            motor_speed = 64  # Close: 25% speed
            ser.write(b'1')  # Send 1 to Arduino
        elif distance_between_palms < 300:
            motor_speed = 128  # Medium: 50% speed
            ser.write(b'2')  # Send 2 to Arduino
        elif distance_between_palms > 300:
            motor_speed = 255  # Far: 100% speed
            ser.write(b'3')  # Send 3 to Arduino

    # Display the frame
    cv2.imshow("Hand Distance Measurement", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
