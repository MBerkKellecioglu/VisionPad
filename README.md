# 🖐️ VisionPad

**Turn your webcam into a touchless mouse.**

VisionPad tracks your hand in real time and lets you control your computer without touching anything. You point with your finger to move the cursor and pinch to click.

## ✨ Features

- **Point to move:** The cursor follows your index finger.
- **Pinch to click:** Touch your thumb to your middle finger to click. Your pointing finger stays still, so the cursor doesn't drift while you click.
- **Works at any distance:** Clicks are detected the same way whether your hand is close to the camera or far away.
- **Smooth cursor:** Hand jitter is filtered out for steady movement.
- **Live preview:** A camera window shows your hand being tracked in real time.

## 🎮 How to Use

| Gesture | Action |
|---|---|
| ☝️ Move your index finger | Move the cursor |
| 🤌 Touch thumb to middle finger | Click |
| ⌨️ Press `q` | Quit |

Keep your hand inside the purple frame in the camera window. That frame covers your whole screen.

## 🚀 Getting Started

```bash
git clone https://github.com/MBerkKellecioglu/VisionPad.git
cd VisionPad

python3.11 -m venv venv
source venv/bin/activate
pip install opencv-python mediapipe==0.10.14 numpy pyautogui

python fingertracking.py
```

> **macOS:** Grant **Camera** and **Accessibility** permissions to your terminal or VS Code when prompted (*System Settings → Privacy & Security*). If you skip this, VisionPad can't control the mouse.

## 🛠️ Built With

- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide): hand tracking
- [OpenCV](https://opencv.org/): camera capture and preview
- [PyAutoGUI](https://pyautogui.readthedocs.io/): mouse control
- [NumPy](https://numpy.org/): coordinate math
