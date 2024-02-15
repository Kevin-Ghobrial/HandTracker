import cv2
import mediapipe as mp
import subprocess
import os
import platform

count = 0
count2 = 0
count3 = 0
def change_volume(direction):
    # Adjust volume using osascript (macOS specific)
    if platform.system() == 'Darwin':
        if direction == 'up':
            osascript_command = 'osascript -e "set volume output volume ((output volume of (get volume settings)) + 10)"'
        else:
            osascript_command = 'osascript -e "set volume output volume ((output volume of (get volume settings)) - 10)"'
        subprocess.run(osascript_command, shell=True)
    else:
        print("Volume adjustment is only supported on macOS.")

print("Current working directory:", os.getcwd())

# Initialize hand tracking module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open camera
cap = cv2.VideoCapture(0)

# Adjust these parameters based on your preferences and environment
max_distance = 200  # Adjust sensitivity
frame_rate = 15  # Adjust frame rate

hand_detected = False  # Variable to track hand detection

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get hand landmarks
    results = hands.process(rgb_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        if hand_detected:
            if count == 0:
                print("Hand entered the screen!")
                count = 1
                count2 = 0

        hand_detected = True  # Hand is detected

        for hand_landmarks in results.multi_hand_landmarks:
            # Extract landmarks for fingertips
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Get the y-coordinates of thumb and index fingertips
            thumb_y = int(thumb_tip.y * frame.shape[0])
            index_y = int(index_tip.y * frame.shape[0])
            pinky_y = int(pinky_tip.y * frame.shape[0])
            wrist_y = int(wrist.y * frame.shape[0])

            # Adjust volume based on finger openness
            if wrist_y < index_y:
                count3 = 1;
                print("Gesture complete.")
                
            if count3 == 1:
                if thumb_y < index_y:  # Thumb is above the index finger (hand open)
                    change_volume('up')
                else:
                    change_volume('down')
            else:
                if count2 == 0:
                    print("Please do the hand gesture to turn on hand tracker :)")
                    count2 = 1

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        if hand_detected:
            print("Hand left the screen!")
            count = 0
            count3 = 0

        hand_detected = False  # Hand is not detected

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Adjust frame rate
    if cv2.waitKey(int(1000 / frame_rate)) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
