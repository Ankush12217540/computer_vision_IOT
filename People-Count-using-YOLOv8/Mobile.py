from ultralytics import YOLO
import cv2
import serial
import time

# Set up the serial connection to the Arduino
# Make sure to replace 'COM3' with your Arduino's port and '9600' with the correct baud rate
ser = serial.Serial('COM16', 9600, timeout=1)  # Adjust the COM port as needed

# Load the YOLOv8 model (ensure it supports mobile phone detection)
model = YOLO('yolov8n.pt')  # Replace with your model file path

# Open the video stream
cap = cv2.VideoCapture(0)  # Use the webcam as the video source
if not cap.isOpened():
    print("Error: Cannot access webcam.")
    exit()

cv2.namedWindow("Mobile Phone Detection", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Mobile Phone Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    # Run YOLO model prediction on the frame
    results = model.predict(source=frame, conf=0.4, save=False, stream=True)

    phone_detected = False  # Flag to check if phone is detected

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])  # Class ID
            if cls_id == 67:  # Class ID for "mobile phone" (COCO dataset class ID for mobile phone is 67)
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Draw the bounding box around the detected mobile phone
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # Add label to the bounding box
                cv2.putText(frame, "Mobile Phone", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                phone_detected = True  # Phone detected flag is set to True

    # Send command to Arduino based on detection
    if phone_detected:
 
        ser.write(b'B')  # Send 'B' to Arduino (turn on buzzer)
    else:
        ser.write(b'b')  # Send 'b' to Arduino (turn off buzzer)

    # Show the frame in the window
    cv2.imshow("Mobile Phone Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
