import io
import serial
import time

import cv2
import mediapipe as mp
import numpy as np
import math
from angle_report import get_angles

def tupleize(lands,pos):
    global lr
    lr = 0
    exec("global lr\na = lands[mp_pose.PoseLandmark.%s.value]\nlr = (a.x,a.y)" % (pos),globals(),{"lands":lands})
    return lr


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

arduino = serial.Serial(port='COM7', baudrate=2000000, timeout=10)



mode = 0
min_angle = 360
max_angle = 0
CALIBRATION_STEP = 7

print('start-up')
time.sleep(2)
print('calibrating - press x to stop, press anything else to step up')

cali_in = input()

while cali_in != "x":
    arduino.write(bytes(str(1)+'\n','utf-8'))
    print('stepped up')
    cali_in = input()
    
arduino.write(bytes(str(100)+'\n','utf-8'))
print('done calibrating, turn off the ems until visuals are calibrated, press anything when ready')
input()
print('starting')

cap = cv2.VideoCapture(0)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5,enable_segmentation=True) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            wrist = tupleize(landmarks,"LEFT_WRIST")
            elbow = tupleize(landmarks,"LEFT_ELBOW")
            shoulder = tupleize(landmarks,"LEFT_SHOULDER")
            elbow_angle = get_angles(wrist,elbow,shoulder)
            
            if elbow_angle < min_angle: min_angle = elbow_angle
            if elbow_angle > max_angle: max_angle = elbow_angle
            percent = int((elbow_angle-min_angle)/(max_angle-min_angle)*100)
            if percent < 15: percent = 1
            arduino.write(bytes(str(percent)+'\n','utf-8'))
        except Exception as e:
            print('error:',e)
            pass

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
