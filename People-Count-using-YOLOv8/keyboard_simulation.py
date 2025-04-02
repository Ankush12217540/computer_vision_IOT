import cv2
import mediapipe as mp
import math
import pyautogui  # For simulating keyboard inputs

# Initialize MediaPipe Hands and drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the MediaPipe hands module
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize OpenCV window
cv2.namedWindow("Hands-Free Media Player", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Hands-Free Media Player", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Define variables for control states
is_playing = False
volume = 50  # Default volume level (0-100)
media_control_text = ""

# Function to calculate the distance between two points
def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Open webcam video feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Check if any hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the thumb and index finger tips
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate the distance between thumb and index finger tips
            distance = calculate_distance(thumb_tip, index_tip) * 100

            # Control play/pause based on thumb-index distance
            if distance < 30:  # Play/Pause gesture (close fingers)
                if not is_playing:
                    is_playing = True
                    media_control_text = "Playing"
                    pyautogui.press('space')  # Simulate pressing space to play/pause
                else:
                    is_playing = False
                    media_control_text = "Paused"
                    pyautogui.press('space')  # Simulate pressing space to play/pause

            # Adjust volume based on the distance (greater distance = higher volume)
            elif distance > 70:  # Volume control gesture (spread fingers)
                volume = min(100, volume + 2)
                media_control_text = f"Volume: {volume}%"
                pyautogui.press('up')  # Simulate pressing arrow up to increase volume

            # Decrease volume if fingers are close (volume down gesture)
            elif distance < 20:
                volume = max(0, volume - 2)
                media_control_text = f"Volume: {volume}%"
                pyautogui.press('down')  # Simulate pressing arrow down to decrease volume

            # Media control feedback on the screen
            cv2.putText(frame, f"Media Control: {media_control_text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the video frame
    cv2.imshow("Hands-Free Media Player", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
