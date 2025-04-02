import cv2
import mediapipe as mp
import math
import pyautogui

# Initialize MediaPipe Hands and drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the MediaPipe hands module
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize OpenCV window
cv2.namedWindow("Hands-Free Typing", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Hands-Free Typing", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Define a virtual on-screen keyboard layout (This can be expanded or customized)
keyboard_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['Space', 'Enter', 'Backspace']
]

# Calculate key positions and sizes
key_width = 100
key_height = 100
keyboard_x = 50  # X position of the keyboard (start from left)
keyboard_y = 500  # Y position of the keyboard (start from top)

# Adjust size of the keys if needed to fit the screen
screen_width = 1920  # Assuming a standard screen width
screen_height = 1080  # Assuming a standard screen height
total_width = len(keyboard_layout[0]) * key_width
total_height = len(keyboard_layout) * key_height

# Adjust keyboard layout for screen size
if total_width > screen_width:
    key_width = screen_width // len(keyboard_layout[0])

if total_height > screen_height:
    key_height = screen_height // len(keyboard_layout)

def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Function to detect if the index finger is close to a key
def is_finger_near_key(finger_tip, key_x, key_y):
    # Define a tolerance distance
    distance = math.sqrt((finger_tip.x - key_x) ** 2 + (finger_tip.y - key_y) ** 2)
    return distance < 0.05  # Threshold for finger proximity (adjust as needed)

# Function to draw the on-screen keyboard
def draw_keyboard(frame):
    for row_idx, row in enumerate(keyboard_layout):
        for col_idx, key in enumerate(row):
            x1 = keyboard_x + col_idx * key_width
            y1 = keyboard_y + row_idx * key_height
            x2 = x1 + key_width
            y2 = y1 + key_height
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)  # Draw key boundaries

            # Add text for the key in the center
            text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = int(x1 + (key_width - text_size[0]) / 2)
            text_y = int(y1 + (key_height + text_size[1]) / 2)
            cv2.putText(frame, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

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

            # Get the coordinates of the index finger tip
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Draw the index finger position on the screen
            index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)  # Green dot for index tip

            # Check if the index finger is hovering over any key
            for row_idx, row in enumerate(keyboard_layout):
                for col_idx, key in enumerate(row):
                    key_x = keyboard_x + col_idx * key_width + key_width / 2
                    key_y = keyboard_y + row_idx * key_height + key_height / 2
                    if is_finger_near_key(index_tip, key_x, key_y):
                        # Simulate typing the corresponding key
                        if key == 'Space':
                            pyautogui.press('space')
                        elif key == 'Enter':
                            pyautogui.press('enter')
                        elif key == 'Backspace':
                            pyautogui.press('backspace')
                        else:
                            pyautogui.write(key)  # Type the character

            # Draw the on-screen keyboard
            draw_keyboard(frame)

    # Display the frame with the on-screen keyboard
    cv2.imshow("Hands-Free Typing", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
