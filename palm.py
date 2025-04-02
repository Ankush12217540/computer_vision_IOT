import cv2
import mediapipe as mp
import math

# Initialize the MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Start capturing from the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    # Flip the frame horizontally for a mirror view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find hands
    results = hands.process(rgb_frame)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the wrist and the middle finger tip (for palm positioning)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Convert normalized coordinates to pixel values
            height, width, _ = frame.shape
            wrist_coordinates = (int(wrist.x * width), int(wrist.y * height))
            middle_finger_tip_coordinates = (int(middle_finger_tip.x * width), int(middle_finger_tip.y * height))

            # Calculate the distance between the wrist and middle finger tip (representing the palm width)
            distance = calculate_distance(wrist_coordinates, middle_finger_tip_coordinates)

            # Display the distance on the frame
            cv2.putText(frame, f"Distance: {distance:.2f} px", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Check if hands are moving closer or farther apart
            if 'previous_distance' in locals():
                if distance > previous_distance:
                    cv2.putText(frame, "Move: Farther Apart", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif distance < previous_distance:
                    cv2.putText(frame, "Move: Closer", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            previous_distance = distance

    # Display the frame
    cv2.imshow("Palm Distance Measurement", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
