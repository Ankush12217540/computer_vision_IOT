import cv2
import mediapipe as mp
import math
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Start webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam.")
    exit()

# Get screen resolution for full screen
screen_width = 1920  # Change this to your screen width
screen_height = 1080  # Change this to your screen height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Define colors
BACKGROUND_COLOR = (28, 28, 28)  # Dark background for the sidebar
TEXT_COLOR = (255, 255, 255)     # White color for text
HIGHLIGHT_COLOR = (0, 255, 0)    # Green for highlighting text

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    # Flip the frame for mirror view
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find hands
    results = hands.process(rgb_frame)

    # Create a sidebar to display the motor control distance
    sidebar_width = 350
    sidebar = frame[:, :sidebar_width]  # Left sidebar
    sidebar[:] = BACKGROUND_COLOR  # Black background for sidebar

    # Draw header text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(sidebar, "Gesture Control", (20, 50), font, 1.5, HIGHLIGHT_COLOR, 3, cv2.LINE_AA)
    cv2.putText(sidebar, "Distance:", (20, 100), font, 1.0, TEXT_COLOR, 2, cv2.LINE_AA)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the thumb and index finger
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert normalized coordinates to pixel values
            height, width, _ = frame.shape
            thumb_coordinates = (int(thumb_tip.x * width), int(thumb_tip.y * height))
            index_coordinates = (int(index_tip.x * width), int(index_tip.y * height))

            # Calculate the distance between the thumb and index finger
            distance = calculate_distance(thumb_coordinates, index_coordinates)

            # Show the distance with dynamic effect on the sidebar
            distance_text = f"{distance:.2f} px"
            cv2.putText(sidebar, distance_text, (20, 150), font, 1.5, HIGHLIGHT_COLOR, 3, cv2.LINE_AA)

            # Draw a dynamic circle around the fingers
            cv2.circle(frame, thumb_coordinates, 15, (255, 0, 0), 3)
            cv2.circle(frame, index_coordinates, 15, (255, 0, 0), 3)

            # Add a line connecting the thumb and index finger for better visibility
            cv2.line(frame, thumb_coordinates, index_coordinates, (0, 255, 255), 3)

    # Merge the sidebar with the main frame
    frame_with_sidebar = cv2.hconcat([sidebar, frame[:, sidebar_width:]])

    # Show the frame with sidebar in full screen
    cv2.imshow("Hand Gesture Control - Distance Measured", frame_with_sidebar)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
