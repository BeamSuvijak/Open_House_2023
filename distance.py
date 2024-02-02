import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    wrist0 = (0, 0)
    wrist1 = (0, 0)

    _, frame = cap.read()

    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    x0, x1, y0, y1 = 0, 0, 0, 0
    if hands:
        max_landmarks = -1
        best_hand = None

        the_hand = output.multi_handedness

        if len(the_hand) == 2:
            for hand_idx, hand in enumerate(hands):
                landmarks = hand.landmark
                num_landmarks = len(landmarks)
                if num_landmarks > max_landmarks:
                    max_landmarks = num_landmarks
                    best_hand = hand
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark

                for id, landmark in enumerate(landmarks):
                    mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)

                    for A_hand in the_hand:
                        index_value = A_hand.classification[0].index

                        if index_value == 0 and hand_idx == 0:
                            if id == 0:
                                x0 = int(landmark.x * frame_width)
                                y0 = int(landmark.y * frame_height)

                                print(f'Hand0 -> x = {x0} , y = {y0}')
                        elif index_value == 1 and hand_idx == 1:
                            if id == 0:
                                x1 = int(landmark.x * frame_width)
                                y1 = int(landmark.y * frame_height)
                                print(f'Hand1 -> x = {x1} , y = {y1}')

            # Calculate the distance
            x_pow = math.pow(x0 - x1, 2)
            y_pow = math.pow(y0 - y1, 2)
            distance = math.sqrt(x_pow + y_pow)
            print(f'distance = {distance}')

            # Calculate the angle
            angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
            if angle < 0:
                angle += 360
            print(f'angle = {angle}')

    cv2.imshow('Check', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit(0)
