import cv2

# Define a virtual on-screen keyboard layout
keyboard_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['Space', 'Enter', 'Backspace']
]

# Initialize OpenCV window
cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Virtual Keyboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Draw the on-screen keyboard
    draw_keyboard(frame)

    # Display the frame with the on-screen keyboard
    cv2.imshow("Virtual Keyboard", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
