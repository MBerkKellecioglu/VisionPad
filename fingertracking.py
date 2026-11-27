import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from videostream import VideoStream
from collections import deque
import time
import Quartz

"""
    One line optimisation, every time when using moveTo function, by default, function sleeps for 0.1 ms
    and moveTo function gets called 30 times (30 FPS) a second so it causes bottleneck in event queue

    We set that pause time to 0 ms to optimise that bottleneck
"""
pyautogui.PAUSE = 0.0

def mac_click(x, y, click_count=1):
    """Using MacOS library for inputting double click"""
    for event_type in (Quartz.kCGEventLeftMouseDown, Quartz.kCGEventLeftMouseUp):
        event = Quartz.CGEventCreateMouseEvent(
            None, event_type, (x, y), Quartz.kCGMouseButtonLeft
        )
        Quartz.CGEventSetIntegerValueField(
            event, Quartz.kCGMouseEventClickState, click_count
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

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
frame_left, frame_right = 160, 480
frame_top, frame_bottom = 120, 300

# Starting coordinates and smoothing for tracking
prev_x, prev_y = 0,0
curr_x, curr_y = 0,0
smoothening = 8

# Pinch tresholds
PRESS_DIST = 0.03
RELEASE_DIST = 0.032
RELEASE_HOLD = 0.06       # Fingers must stay open this long before a new click

# Double click
DOUBLE_CLICK_TIME = 0.9    # A second pinch within this time is a double click
DOUBLE_CLICK_RADIUS = 100  # If the cursor moved further than this it's a new single click

click_count = 0
last_click_time = 0.0
last_click_pos = (0, 0)
release_start = None

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
            
            # 3D coordinates (Origin is at the center of the palm) for thumb and index fingers
            w_thumb = world_landmarks.landmark[4]
            w_index = world_landmarks.landmark[8]

            # We dont need to scale anything we only need distance between those two fingers for "pinching"
            # Mind you our index finger coordinates and index and thumb finger coordinates are NOT in the same coordinate system
            pinch_dist = np.linalg.norm([
                w_thumb.x - w_index.x,
                w_thumb.y - w_index.y,
                w_thumb.z - w_index.z,
            ])

            cv2.rectangle(
                frame,
                (frame_left,frame_top),
                (frame_right,frame_bottom),
                (255,0,255),
                2
            )

            mcp_ids = (5,9,13,17)

            # Get the average coordinates of base of the fingers to find the middle point
            anchor_x = (sum(hand_landmarks.landmark[i].x for i in mcp_ids) / len(mcp_ids)) * w
            anchor_y = (sum(hand_landmarks.landmark[i].y for i in mcp_ids) / len(mcp_ids)) * h

            # Map those coordinates to screen resolution
            screen_x = np.interp(anchor_x, (frame_left, frame_right), (0,screen_w))
            screen_y = np.interp(anchor_y, (frame_top, frame_bottom), (0,screen_h))

            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            now = time.monotonic()

            # Fingers must stay open for RELEASE_HOLD seconds
            # So jitter while the fingers are touching can't trigger a new click
            if pinch_dist > RELEASE_DIST:
                if release_start is None:
                    release_start = now
                if is_clicked and now - release_start >= RELEASE_HOLD:
                    is_clicked = False
            else:
                release_start = None

            # Press
            if pinch_dist < PRESS_DIST and not is_clicked:
                gap = now - last_click_time
                near_last = np.hypot(curr_x - last_click_pos[0], curr_y - last_click_pos[1]) < DOUBLE_CLICK_RADIUS

                if gap < DOUBLE_CLICK_TIME and near_last:
                    click_count += 1          # double/triple click, same spot as the first click
                else:
                    click_count = 1           # single click
                    last_click_pos = (curr_x, curr_y)

                mac_click(*last_click_pos, click_count)
                last_click_time = now
                is_clicked = True

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Pinch distance on screen: green when pressed, red when not
            color = (0, 255, 0) if is_clicked else (0, 0, 255)
            cv2.putText(frame, f"{pinch_dist * 100:.1f} cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)


    cv2.imshow("Real Time Camera Stream", frame)

    # Quit when pressed q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting Program")
        break

cv2.destroyAllWindows()