
import face_recognition
import cv2
import os
import gspread
import datetime



 
 
# Step 1: Encode known faces
def encode_faces(dataset_dir='face_recognition/dataset'):
    known_encodings = []
    known_names = []

    for student_name in os.listdir(dataset_dir):
        student_folder = os.path.join(dataset_dir, student_name)
        if not os.path.isdir(student_folder):
            continue

        for image_name in os.listdir(student_folder):
            image_path = os.path.join(student_folder, image_name)

            # Load and encode the image
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:  # Check if a face was found
                known_encodings.append(encodings[0])
                known_names.append(student_name)

    return {"encodings": known_encodings, "names": known_names}

# Step 2: Recognize faces in real-time
def recognize_faces(data):
    video_capture = cv2.VideoCapture(0)  # Open webcam

    # Set the video feed to full-screen mode
    cv2.namedWindow("Face Recognition", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    print("Starting face recognition... Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces and encodings
        boxes = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, boxes)

        # Match faces
        for (top, right, bottom, left), encoding in zip(boxes, encodings):
            matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                matched_idx = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for idx in matched_idx:
                    student_name = data["names"][idx]
                    counts[student_name] = counts.get(student_name, 0) + 1

                # Assign the most recognized name
                name = max(counts, key=counts.get)

            # Draw a box around the face and label it
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Display the video feed
        cv2.imshow("Face Recognition", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Encode faces
    print("Encoding known faces...")
    data = encode_faces()

    # Recognize faces in real-time
    recognize_faces(data)
