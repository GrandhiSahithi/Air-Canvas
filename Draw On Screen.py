import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could'nt open webcam.")
    exit()

canvas = None
colors = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
}
color = colors['blue'] 
while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Error: Couldn't read frame.")
        break

    if canvas is None:
        canvas = np.zeros_like(img)

    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8:  
                    cv2.circle(img, (cx, cy), 10, color, cv2.FILLED)
                    cv2.circle(canvas, (cx, cy), 10, color, cv2.FILLED)

    img = cv2.addWeighted(img, 0.5, canvas, 0.5, 0)
    cv2.imshow('Air Canvas', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
