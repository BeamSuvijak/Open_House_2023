import cv2
import mediapipe as mp
import math
import threading as Thread
import socket
import sys
import time
import json
def detect_hand_gesture():
    cap = cv2.VideoCapture(0)
    No = 1
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    claping = True
    global DATA
    DATA = {}
    clap_cou = 0
    while True:
        wrist0 = (0, 0)
        wrist1 = (0, 0)

        _, frame = cap.read()

        frame_height, frame_width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        x0, x1, y0, y1 = 0, 0, 0, 0
        Power = 0
        distance_threshold = 100
        angle = 0


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

                                    #print(f'Hand0 -> x = {x0} , y = {y0}')
                            elif index_value == 1 and hand_idx == 1:
                                if id == 0:
                                    x1 = int(landmark.x * frame_width)
                                    y1 = int(landmark.y * frame_height)
                                    #print(f'Hand1 -> x = {x1} , y = {y1}')


                        for A_hand in the_hand:
                            index_value = A_hand.classification[0].index
                            if y0 < y1:
                                if index_value == 1 and hand_idx == 1:
                                    if id == 0:
                                        thumbx = int(landmark.x * frame_width)
                                        thumby = int(landmark.y * frame_height)
                                    if id == 12:
                                        indexx = int(landmark.x * frame_width)
                                        indexy = int(landmark.y * frame_height)
                            else:
                                if index_value == 0 and hand_idx == 0:
                                    if id == 0:
                                        thumbx = int(landmark.x * frame_width)
                                        thumby = int(landmark.y * frame_height)
                                    if id == 12:
                                        indexx = int(landmark.x * frame_width)
                                        indexy = int(landmark.y * frame_height)
                clap = ((thumbx - indexx) ** 2 + (thumby - indexy) ** 2) ** 0.5
                if clap > distance_threshold:
                    clap_cou += 1
                    if clap_cou >= 15:
                        clap_cou = 0
                        claping = False
                        print('shoot')
                # Calculate the distance
                x_pow = math.pow(x0 - x1, 2)
                y_pow = math.pow(y0 - y1, 2)
                distance = math.sqrt(x_pow + y_pow)
                #print(f'distance = {distance}')
                max_distance = frame_width * 0.8
                if distance > max_distance:
                    distance = max_distance
                #print(f'distance = {distance}')
                Power = (distance / max_distance) * 100
                Power = int(Power)
                #print(f'power = {Power}%')

                # Check if the lower hand is raised above the upper hand


                # Calculate the angle
                if No == 2:
                    angle = math.degrees(math.atan2(x1 - x0, y1 - y0))
                else:
                    angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
                if angle < 0:
                    angle += 360
                #print(f'angle = {(angle)%90}')
        angle = int(angle % 90)
        DATA = {
            "Player" : No,
            "Power" : Power,
            "Angle" : angle,
            "Clap" : claping
        }
        claping = True
        #print(sys.getsizeof(DATA))
        cv2.imshow('Check', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)

def Run_Client():
    global DATA
    encode_DATA = json.dumps(DATA).encode(FORMAT)
    client.send(encode_DATA)
    print(DATA)


if __name__ == "__main__":

    HEADER = 64
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    #SERVER = str(input("Server IP : "))

    SERVER = "172.20.10.3"
    print(SERVER)
    FORMAT = 'utf-8'
    disconnect_msg = "Disconnect"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER,PORT))
    connect = True

    hand_detect = Thread.Thread(target=detect_hand_gesture)
    hand_detect.start()
    DATA = {}
    while connect:
        Client_Job = Thread.Thread(target=Run_Client)
        Client_Job.start()
        time.sleep(0.1)
