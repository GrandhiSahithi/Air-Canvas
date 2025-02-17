from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


canvas = None
color = (0, 255, 0)  
line_size = 10  
drawing = False
is_eraser = False  
opacity = 0.5  

def process_frame(frame):
    global canvas, drawing, is_eraser

    img = cv2.flip(frame, 1)  
    if canvas is None:
        canvas = np.zeros_like(img)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            
            drawing = is_finger_open(landmarks, 8) and not is_fist_closed(landmarks)

            if drawing:
                h, w, _ = img.shape
                cx, cy = int(landmarks[8].x * w), int(landmarks[8].y * h)
                
                if is_eraser:
                    cv2.circle(canvas, (cx, cy), line_size, (0, 0, 0), cv2.FILLED)
                else:
                    cv2.circle(canvas, (cx, cy), line_size, color, cv2.FILLED)
    else:
        drawing = False
    combined_img = cv2.addWeighted(img, 1 - opacity, canvas, opacity, 0)
    _, jpeg = cv2.imencode('.jpg', combined_img)
    return jpeg.tobytes()

def is_finger_open(landmarks, idx):
    return landmarks[idx].y < landmarks[idx - 2].y

def is_fist_closed(landmarks):
    return all(landmarks[i].y > landmarks[i - 2].y for i in range(8, 21, 4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/change_color', methods=['POST'])
def change_color():
    global color, is_eraser
    data = request.get_json()
    hex_color = data['color'].lstrip('#')
    color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
    is_eraser = False  
    return jsonify(success=True)

@app.route('/toggle_eraser', methods=['POST'])
def toggle_eraser():
    global is_eraser
    data = request.get_json()
    is_eraser = data['eraser']
    return jsonify(success=True)

@app.route('/change_size', methods=['POST'])
def change_size():
    global line_size
    data = request.get_json()
    line_size = data['size']
    return jsonify(success=True)

@app.route('/change_opacity', methods=['POST'])
def change_opacity():
    global opacity
    data = request.get_json()
    opacity = data['opacity']
    return jsonify(success=True)

@app.route('/clear_canvas', methods=['POST'])
def clear_canvas():
    global canvas
    canvas = None
    return jsonify(success=True)

def generate():
    cap = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame = process_frame(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    finally:
        cap.release()

if __name__ == '__main__':
    app.run(debug=True)
