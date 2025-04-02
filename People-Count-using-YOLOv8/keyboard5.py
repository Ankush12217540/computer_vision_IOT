import cv2
import mediapipe as mp
from pynput.keyboard import Controller
import time

# Initialize webcam and mediapipe hands module
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Set up MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Initialize keyboard controller
keyboard = Controller()

# Define the layout for the virtual keyboard
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Store typed text
finalText = ""

# Define a Button class for the keys
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Create the virtual keyboard
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Function to draw the keyboard on the screen
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw each button
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image for hand tracking
    results = hands.process(img_rgb)

    # If hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates for index finger and thumb
            thumb_x, thumb_y = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x, landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            index_x, index_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # Convert normalized coordinates to pixel values
            h, w, _ = img.shape
            thumb_x, thumb_y = int(thumb_x * w), int(thumb_y * h)
            index_x, index_y = int(index_x * w), int(index_y * h)

            # Measure the distance between the index finger and thumb
            dist = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

            # Check for button press
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                # If the index finger is near a button and the thumb is close enough (dist < threshold)
                if x < index_x < x + w and y < index_y < y + h and dist < 50:
                    # Highlight the button and simulate key press
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)BB
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    # Simulate key press
                    keyboard.press(button.text)
                    finalText += button.text
                    time.sleep(0.15)

    # Draw the keyboard and final text on the screen
    img = drawAll(img, buttonList)
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Display the image with the virtual keyboard
    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
