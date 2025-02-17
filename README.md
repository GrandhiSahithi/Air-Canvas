# 🖌️ Air Canvas 🎨

## Introduction

**Air Canvas** is an innovative web application that transforms hand gestures into digital art, allowing users to draw in the air seamlessly. This project leverages computer vision and advanced hand-tracking techniques to create an interactive and immersive drawing experience. By using your hand as a virtual brush, you can create art in real-time, with the output displayed directly on the live video feed. Whether you're an artist, a tech enthusiast, or just someone looking for a fun way to express creativity, Air Canvas offers a unique and engaging platform.

The project initially utilized **MediaPipe** for hand tracking but later evolved to include a **custom hand-tracking algorithm** based on HSV thresholding and contour analysis. This provides greater flexibility and independence from external libraries. With features like dynamic color selection, adjustable brush sizes, opacity control, and an eraser tool, Air Canvas is designed to be both powerful and user-friendly.

---

## Features

### 🖐️ Hand Tracking
- **MediaPipe Integration:** Accurate and real-time tracking of hand landmarks.
- **Custom Hand Tracking:** A custom algorithm using HSV thresholding and contour analysis for enhanced control and independence.

### 🎨 Dynamic Drawing Tools
- **Color Palette:** Choose from a wide range of colors for your brush.
- **Brush Size:** Adjust the thickness of your brush strokes.
- **Opacity Control:** Modify the transparency of your strokes for creative effects.
- **Eraser Tool:** Correct mistakes by erasing specific sections of your drawing.
- **Clear Canvas:** Reset the canvas with a single click for a fresh start.

### 📹 Real-Time Video Integration
- Draw directly on the live video feed, creating an interactive and immersive experience.
- Visual feedback ensures precise control over your gestures.

### 📱 User-Friendly Interface
- Intuitive controls for color selection, brush size, opacity, and more.
- Responsive design that works seamlessly across devices.

### 📊 Performance Metrics
- Real-time accuracy feedback for hand tracking.
- Performance evaluation to ensure smooth and lag-free drawing.

---

## How It Works

1. **Hand Detection:** The system detects your hand using either MediaPipe or the custom hand-tracking algorithm.
2. **Gesture Recognition:** Specific gestures (e.g., pinching) are used to control drawing actions like starting/stopping strokes or selecting tools.
3. **Drawing on Screen:** As you move your hand, the system maps your gestures to the canvas, rendering strokes in real-time.
4. **UI Interaction:** Use the on-screen controls to adjust colors, brush size, opacity, and more.

---

## Prerequisites 

To run this project, you'll need the following:

- 🐍 **Python 3.x**
- 🌐 **Flask** (for the web application)
- 📷 **OpenCV** (for computer vision and video processing)
- ✋ **Mediapipe** (for hand tracking, optional if using the custom algorithm)
- 🔢 **Numpy** (for numerical operations)

---
## Project Structure

air_canvas/
├── app.py                  # Flask application and main logic
├── templates/              # HTML templates
│   └── index.html          # Main UI page
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css       # Styles for the UI
│   ├── Images/
│   │     └── Background.jpeg  # Background image
│   └── js/
│       └── script.js       # JavaScript for interactive UI
├── Color Selection UI.py   # Logic for color selection
├── Draw On Screen.py       # Logic for rendering strokes
└── Hand Tracking.py        # Hand tracking implementation


## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/GrandhiSahithi/air-canvas.git
   cd air-canvas
