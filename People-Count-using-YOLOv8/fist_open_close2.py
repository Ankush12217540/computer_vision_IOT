import cv2
import mediapipe as mp
import serial
import time

# Initialize Serial Communication (adjust the COM port as needed)
ser = serial.Serial('COM16', 9600)  # Replace 'COM3' with your Arduino port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
time.sleep(2)  # Wait for the serial connection to establish

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Start capturing from webcam
cap = cv2.VideoCapture(0)

# Set the window to fullscreen
cv2.namedWindow("Fist Detection", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Fist Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def is_fist_closed(hand_landmarks):
    # Check if the fist is closed using landmarks
    distances = []
    
    # Calculate distances between thumb (4) and other fingers (tips)
    distances.append(abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[8].x))
    distances.append(abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[12].x))
    distances.append(abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[16].x))
    distances.append(abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[20].x))
    
    # If the distances are very small, we assume fist is closed
    if all(distance < 0.05 for distance in distances):
        return True
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and get hand landmarks
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        # Track only the first hand (index 0)
        hand_landmarks = results.multi_hand_landmarks[0]  # Only consider the first hand
        
        # Draw landmarks on the hand
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Check if the fist is closed
        if is_fist_closed(hand_landmarks):
            # Send signal to Arduino to turn the fan OFF
            ser.write(b'M')
            
            # Display "Fan OFF" and instructions
            cv2.putText(frame, "fan off", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            fan_off_text = "open your fist to turn the fan on"
            recommendation_color = (0, 255, 0)  # Green for the fan off
        else:
            # Send signal to Arduino to turn the fan ON
            ser.write(b'm')
            
            # Display "Fan ON" and instructions
            cv2.putText(frame, "fan on", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            fan_off_text = "close your fist to turn the fan off"
            recommendation_color = (0, 0, 255)  # Red for the fan on
        
        # Get the size of the text to be added (for centering)
        text_size = cv2.getTextSize(fan_off_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_width, text_height = text_size
        
        # Calculate the position to center the text horizontally at the bottom
        x_pos = (frame.shape[1] - text_width) // 2
        y_pos = frame.shape[0] - 30  # 30 pixels above the bottom of the frame
        
        # Add the recommendation text in the center of the bottom
        cv2.putText(frame, fan_off_text, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, recommendation_color, 2)
    
    # Display the frame
    cv2.imshow("Fist Detection", frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
