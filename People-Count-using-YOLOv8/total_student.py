from ultralytics import YOLO
import cv2
import serial

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Replace with the path to your YOLOv8 model file

# Initialize serial communication
serial_port = 'COM16'  # Replace with your serial port (e.g., 'COM16' on Windows, '/dev/ttyUSB0' on Linux)
baud_rate = 9600  # Match the baud rate of your Arduino
ser = serial.Serial(serial_port, baud_rate)

# Open the video stream (webcam or video file)
cap = cv2.VideoCapture(0)  # Use 0 for webcam; replace with a video file path if needed

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Create a named window for the display
cv2.namedWindow("Live Feed", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Live Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Run YOLO model prediction
    results = model.predict(source=frame, conf=0.5, save=False, stream=True)

    # Initialize student count
    student_count = 0

    # Count the number of detected "person" objects
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])  # Class ID
            if cls_id == 0:  # Class ID 0 corresponds to "person" in the COCO dataset
                student_count += 1

    # Display the count on the frame
    count_text = f"Students Present: {student_count}"
    cv2.putText(frame, count_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Send data to the serial port based on the count
    if student_count >= 2:
        ser.write(b'6')  # Send '6' if students are 4 or more
    else:
        ser.write(b'7')  # Send '7' if students are fewer than 4

    # Show the live frame
    cv2.imshow("Live Feed", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
