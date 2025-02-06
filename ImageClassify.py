import cv2
import mediapipe as mp
import numpy as np
from gestureStabilizer import get_stable_gesture
from NearestNeighbourModel import CustomKNN
import pandas as pd
import serial

# Initialize Bluetooth connection
bt_port = "COM7" 
baud_rate = 9600
bluetooth = serial.Serial(bt_port, baud_rate, timeout=1)

# Load gesture dataset and model
data = pd.read_csv('./dataset.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
knn = CustomKNN(k=3)
knn.fit(X, y)

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Gesture to command mapping
gesture_to_command = {
    "forward": "F",
    "backward": "B",
    "left": "L",
    "right": "R",
    "stop": "S"
}

# Initialize last command
last_command = None

def send_command(command):
    global last_command
    if command != last_command:
        bluetooth.write(command.encode('utf-8'))
        print(f"Sent command: {command}")
        last_command = command

def get_angles(hand_landmarks, frame_center):
   # Extract necessary landmarks for checking positions
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    wrist_pos = np.array([wrist.x, wrist.y])
    index_finger_pos = np.array([index_finger.x, index_finger.y])
    thumb_tip_pos = np.array([thumb_tip.x, thumb_tip.y])
    middle_finger_pos = np.array([middle_finger.x, middle_finger.y])
    ring_finger_pos = np.array([ring_finger.x, ring_finger.y])
    pinky_finger_pos = np.array([pinky_finger.x, pinky_finger.y])

    def calculate_angle(tip_pos):
        delta_tip = tip_pos - wrist_pos
        delta_center = frame_center - wrist_pos
        angle = np.degrees(np.arctan2(delta_tip[1], delta_tip[0]) - np.arctan2(delta_center[1], delta_center[0])) % 360
        return angle

    finger_angles = [
        calculate_angle(index_finger_pos),
        calculate_angle(thumb_tip_pos),
        calculate_angle(middle_finger_pos),
        calculate_angle(ring_finger_pos),
        calculate_angle(pinky_finger_pos),
    ]
    return finger_angles

cap = cv2.VideoCapture(0)
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        frame_height, frame_width, _ = frame.shape
        frame_center = (frame_width / 2, frame_height / 2)
        
        results = hands.process(rgb_frame)
        current_command = "S"  # Default to stop

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                angles = get_angles(hand_landmarks, frame_center)
                gesture = knn.predict(angles)[0]
                gesture = get_stable_gesture(gesture)

                # Map gesture to command
                current_command = gesture_to_command.get(gesture, "S")
                break

        send_command(current_command)
        cv2.imshow('Hand Gesture', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
bluetooth.close()