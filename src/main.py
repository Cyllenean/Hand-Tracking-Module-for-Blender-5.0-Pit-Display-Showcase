import cv2
import mediapipe as mp
import numpy as np
from HandTrackingModule import HandDetector
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Initialize files
with open("scale.txt", "w") as file:
    file.write("1.0")  # Start with scale 1.0

with open("pan.txt", "w") as file:
    file.write("0 0")

with open("rotate.txt", "w") as file:
    file.write("0")

# Constants
scale_factor = 0
min_length = 18.439088914585774
max_length = 200.5356303021603
min_scale = 10143
max_scale = 71189
x_blend = 30
z_blend = 20
min_s_blend = 1     # Minimum scale
max_s_blend = 7.5   # Maximum scale
rd = 165  # Rotation sensitivity

# Auto-rotation settings
auto_rotate_active = True
last_gesture_time = time.time()
idle_timeout = 0.5
auto_rotate_speed = 0.3

# Variable to store the current scale value
current_scale = 1.0

# Open the webcam
cap = cv2.VideoCapture(0)

# Create a HandDetector instance
detector = HandDetector(maxHands=2, detectionCon=0.9)

with mp_hands.Hands(
    model_complexity=0, min_detection_confidence=0.9, min_tracking_confidence=0.9
) as hands:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True)
        
        gesture_active = False
        current_time = time.time()
        
        # If no hands detected, set default values
        if not hands:
            with open("scale.txt", "w") as file:
                file.write("1.0")
            with open("rotate.txt", "w") as file:
                file.write("0")
            cv2.imshow("Handtracker_cam", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue
        
        if hands:
            if len(hands) == 1:
                hand1 = hands[0]
                lmList1 = hand1["lmList"]
                bbox1 = hand1["bbox"]
                handType1 = hand1["type"]
                fingerup1 = detector.fingersUp(hand1)
                area = bbox1[2] * bbox1[3]
                center1 = hand1["center"]
                x, z = center1[0], center1[1]
                xc = lmList1[8][0]

                fingerup1 = detector.fingersUp(hand1)
                fist = detector.fist(hand1)

                if handType1 == "Left":
                    if fingerup1 == [1, 1, 0, 0, 0]:
                        gesture_active = True
                        last_gesture_time = current_time
                        length, _, frame = detector.findDistance(
                            lmList1[4][0:2], lmList1[8][0:2], frame
                        )
                        rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(rotate)))
                        # PRESERVE SCALE - don't reset it, keep current value
                        with open("scale.txt", "w") as file:
                            file.write(str(current_scale))

                        cv2.putText(
                            frame,
                            f"Rotate Factor: {float(rotate)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2,
                        )
                        cv2.putText(
                            frame,
                            f"Scale: {current_scale:.2f}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2,
                        )
                    elif fingerup1 != [1, 1, 0, 0, 0]:
                        gesture_active = True
                        last_gesture_time = current_time
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(0)))
                        scale_factor = np.interp(
                            area, [min_scale, max_scale], [min_s_blend, max_s_blend]
                        )
                        scale_factor = "{:.5f}".format(scale_factor)
                        current_scale = float(scale_factor)  # Store the current scale
                        with open("scale.txt", "w") as file:
                            file.write(str(float(scale_factor)))

                        cv2.putText(
                            frame,
                            f"Scale Factor: {float(scale_factor)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 0, 0),
                            2,
                        )
                else:
                    if fist and fingerup1 != [0, 1, 0, 0, 0]:
                        gesture_active = True
                        last_gesture_time = current_time
                        with open("rotate.txt", "w") as file:
                            file.write("0")
                        
                        # IMPROVED PANNING WITH HIGHER SENSITIVITY
                        x_pan = np.interp(x, [69, 527], [-x_blend, x_blend]) * 7
                        z_pan = np.interp(z, [69, 412], [z_blend, -z_blend]) * 7
                        x_pan = "{:.5f}".format(x_pan)
                        z_pan = "{:.5f}".format(z_pan)
                        with open("pan.txt", "w") as file:
                            file.write(str(float(x_pan)))
                            file.write(str(" "))
                            file.write(str(float(z_pan)))
                        # PRESERVE SCALE - keep current value during pan
                        with open("scale.txt", "w") as file:
                            file.write(str(current_scale))

                        cv2.putText(
                            frame,
                            f"Pan X: {float(x_pan)}, Z: {float(z_pan)}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2,
                        )
                        cv2.putText(
                            frame,
                            f"Scale: {current_scale:.2f}",
                            (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2,
                        )

                    elif fingerup1 == [0, 1, 0, 0, 0]:
                        gesture_active = True
                        last_gesture_time = current_time
                        with open("rotate.txt", "w") as file:
                            file.write("0")
                        with open("scale.txt", "w") as file:
                            file.write(str(current_scale))  # PRESERVE SCALE
                        cv2.putText(
                            frame,
                            "POP",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (180, 200, 70),
                            2,
                        )

                    elif fingerup1 == [0, 1, 1, 1, 1]:
                        gesture_active = True
                        last_gesture_time = current_time
                        rotate = np.interp(xc, [56, 537], [-rd, rd])
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(rotate)))
                        with open("scale.txt", "w") as file:
                            file.write(str(current_scale))  # PRESERVE SCALE

                        cv2.putText(
                            frame,
                            f"Rotate Factor: {float(rotate)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2,
                        )
                        cv2.putText(
                            frame,
                            f"Scale: {current_scale:.2f}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2,
                        )
            else:
                # Two hands detected - preserve scale
                with open("scale.txt", "w") as file:
                    file.write(str(current_scale))
                hand1 = hands[0]
                handType1 = hand1["type"]
                if handType1 == "Right":
                    i = 0
                    j = 1
                else:
                    i = 1
                    j = 0
                hand1 = hands[i]
                lmList1 = hand1["lmList"]
                handType1 = hand1["type"]
                center1 = hand1["center"]
                fingerup1 = detector.fingersUp(hand1)
                area = bbox1[2] * bbox1[3]
                fingerup1 = detector.fingersUp(hand1)

                hand2 = hands[j]
                fingerup2 = detector.fingersUp(hand2)
                lmList2 = hand2["lmList"]
                handType2 = hand2["type"]
                x, z = center1[0], center1[1]
                bbox1 = hand2["bbox"]
                fist = detector.fist(hand1)

                if handType1 == "Right" and fist:
                    gesture_active = True
                    last_gesture_time = current_time
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(0)))
                    
                    # IMPROVED PANNING FOR TWO HANDS
                    x_pan = np.interp(x, [63, 404], [-x_blend, x_blend]) * 5
                    z_pan = np.interp(z, [64, 434], [z_blend, -z_blend]) * 5
                    x_pan = "{:.5f}".format(x_pan)
                    z_pan = "{:.5f}".format(z_pan)

                    with open("pan.txt", "w") as file:
                        file.write(str(float(x_pan)))
                        file.write(str(" "))
                        file.write(str(float(z_pan)))

                    cv2.putText(
                        frame,
                        f"Pan X: {float(x_pan)}, Z: {float(z_pan)}",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2,
                    )

                if (
                    handType1 == "Right"
                    and fingerup1 == [1, 1, 0, 0, 0]
                    and fingerup2 != [1, 1, 0, 0, 0]
                ):
                    gesture_active = True
                    last_gesture_time = current_time
                    length, _, img = detector.findDistance(
                        lmList1[4][0:2], lmList1[8][0:2], frame
                    )
                    rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(rotate)))

                    cv2.putText(
                        frame,
                        f"Rotate Factor: {float(rotate)}",
                        (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

                if fingerup2 == [1, 1, 0, 0, 0]:
                    gesture_active = True
                    last_gesture_time = current_time
                    length, _, img = detector.findDistance(
                        lmList2[4][0:2], lmList2[8][0:2], frame
                    )
                    rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(rotate)))

                    cv2.putText(
                        frame,
                        f"Rotate Factor: {float(rotate)}",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

                else:
                    gesture_active = True
                    last_gesture_time = current_time
                    scale_factor = np.interp(
                        area, [min_scale, max_scale], [min_s_blend, max_s_blend]
                    )
                    current_scale = float(scale_factor)  # Store the current scale
                    with open("scale.txt", "w") as file:
                        file.write(str(float(scale_factor)))

                    cv2.putText(
                        frame,
                        f"Scale Factor: {float(scale_factor)}",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2,
                    )

        # Auto-rotation and scale reset
        if not gesture_active and (current_time - last_gesture_time) > idle_timeout:
            with open("rotate.txt", "w") as file:
                file.write(str(auto_rotate_speed))
            with open("scale.txt", "w") as file:
                file.write(str(current_scale))  # PRESERVE SCALE during auto-rotation
            
            cv2.putText(
                frame,
                f"Auto-Rotating: {auto_rotate_speed} degrees/frame",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )
        elif not gesture_active:
            with open("rotate.txt", "w") as file:
                file.write("0")
            with open("scale.txt", "w") as file:
                file.write(str(current_scale))  # PRESERVE SCALE when idle

        cv2.imshow("Handtracker_cam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()