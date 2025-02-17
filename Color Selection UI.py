import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

canvas = None

colors = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'purple': (255, 0, 255),
    'cyan': (255, 255, 0),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}
color = colors['green']  # default color
color_names = list(colors.keys())
selected_color_name = 'green'

def draw_color_palette(frame):
    for i, (name, col) in enumerate(colors.items()):
        cv2.rectangle(frame, (10, 10 + i * 40), (30, 30 + i * 40), col, -1)
        cv2.putText(frame, name, (35, 25 + i * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def select_color(x, y):
    global color, selected_color_name
    for i, (name, col) in enumerate(colors.items()):
        if 10 <= x <= 30 and 10 + i * 40 <= y <= 30 + i * 40:
            color = col
            selected_color_name = name
            print(f"Selected color: {name}")

def is_finger_open(landmarks, idx):
    return landmarks[idx].y < landmarks[idx - 2].y

def is_fist_closed(landmarks):
    return all(landmarks[i].y > landmarks[i - 2].y for i in range(8, 21, 4))

drawing = False

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    img = cv2.flip(img, 1)

    if canvas is None:
        canvas = np.zeros_like(img)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            if is_fist_closed(landmarks):
                drawing = False
            else:
                drawing = is_finger_open(landmarks, 8)

            if drawing:
                h, w, _ = img.shape
                cx, cy = int(landmarks[8].x * w), int(landmarks[8].y * h)
                cv2.circle(img, (cx, cy), 10, color, cv2.FILLED)
                cv2.circle(canvas, (cx, cy), 10, color, cv2.FILLED)
    else:
        drawing = False

    combined_img = cv2.addWeighted(img, 0.5, canvas, 0.5, 0)

    draw_color_palette(combined_img)
    cv2.putText(combined_img, f"Selected color: {selected_color_name}", (10, combined_img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Air Canvas', combined_img)

    def mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            select_color(x, y)

    cv2.setMouseCallback('Air Canvas', mouse_click)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
