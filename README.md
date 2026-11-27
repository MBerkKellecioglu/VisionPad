# 🖐️ VisionPad

**Turn your webcam into a touchless mouse.**

VisionPad tracks your hand in real time and lets you control your Mac without touching anything. Move your hand to move the cursor, pinch to click.

## ✨ Features

- **Move with your palm:** The cursor follows your hand, so your fingers are free for clicking.
- **Pinch to click:** Touch your thumb to your index finger to click. Your palm stays still while you pinch, so the cursor doesn't drift.
- **Double click:** Pinch twice quickly to double click, just like a real mouse.
- **Works at any distance:** Clicks are detected the same way whether your hand is close to the camera or far away.
- **Smooth cursor:** Hand jitter is filtered out for steady movement.
- **Live preview:** A camera window shows your hand being tracked in real time.

## 🎮 How to Use

| Gesture | Action |
|---|---|
| ✋ Move your hand | Move the cursor |
| 👌 Touch thumb to index finger | Click |
| 👌👌 Pinch twice quickly | Double click |
| ⌨️ Press `q` | Quit |

Keep your hand inside the purple frame in the camera window. That frame covers your whole screen.

## 🚀 Getting Started

```bash
git clone https://github.com/MBerkKellecioglu/VisionPad.git
cd VisionPad

python3.11 -m venv venv
source venv/bin/activate
pip install opencv-python mediapipe==0.10.14 numpy pyautogui pyobjc-framework-Quartz

python fingertracking.py
```

> **macOS:** Grant **Camera** and **Accessibility** permissions to your terminal or VS Code when prompted (*System Settings → Privacy & Security*). If you skip this, VisionPad can't control the mouse.

## 🛠️ Built With

- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide): hand tracking
- [OpenCV](https://opencv.org/): camera capture and preview
- [PyAutoGUI](https://pyautogui.readthedocs.io/): cursor movement
- [PyObjC (Quartz)](https://pyobjc.readthedocs.io/): native macOS clicks and double clicks
- [NumPy](https://numpy.org/): coordinate math
