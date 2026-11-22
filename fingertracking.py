import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from videostream import VideoStream
from collections import deque

"""
    One line optimisation, every time when using moveTo function, by default, function sleeps for 0.1 ms
    and moveTo function gets called 30 times (30 FPS) a second so it causes bottleneck in event queue

    We set that pause time to 0 ms to optimise that bottleneck
"""
pyautogui.PAUSE = 0.0

pyautogui.FAILSAFE = False

cap = VideoStream(src=0).start()

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity = 0,
    max_num_hands = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7
)

mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

# Limit working space
frame_r = 50

# Starting coordinates and smoothing for tracking
prev_x, prev_y = 0,0
curr_x, curr_y = 0,0
smoothening = 5

is_clicked = False

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: No Stream")
        break

    frame = cv2.flip(frame,1)

    # Screen height and width
    h,w,c = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks, world_landmarks in zip(result.multi_hand_landmarks, result.multi_hand_world_landmarks):
            index_finger_tip = hand_landmarks.landmark[8]
            
            # Real index finger coordinates scaled to camera resolution
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)

            # 3D coordinates (Origin is at the center of the palm) for thumb and middle fingers
            w_thumb = world_landmarks.landmark[4]
            w_middle = world_landmarks.landmark[12]

            # We dont need to scale anything we only need distance between those two fingers for "pinching"
            # Mind you our index finger coordinates and middle and thumb finger coordinates are NOT in the same coordinate system
            pinch_dist = np.linalg.norm([
                w_thumb.x - w_middle.x,
                w_thumb.y - w_middle.y,
                w_thumb.z - w_middle.z,
            ])

            cv2.rectangle(
                frame,
                (frame_r, frame_r),
                (w - frame_r, h - frame_r),
                (255, 0, 255),
                2,
            )

            # Camera pixel coordinates scaled to monitor resolution using interpolation
            screen_x = np.interp(x, (frame_r, w - frame_r), (0, screen_w))
            screen_y = np.interp(y, (frame_r, h - frame_r), (0, screen_h))

            # We apply smoothing to monitor coordinates in order to block jittering
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            if pinch_dist < 0.030 and not is_clicked:
                pyautogui.click()
                is_clicked = True
            elif pinch_dist > 0.040:
                is_clicked = False      

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


    cv2.imshow("Real Time Camera Stream", frame)

    # Quit when pressed q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting Program")
        break

cv2.destroyAllWindows()