import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##############################
wCam, hCam = 640, 480
##############################

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=int(1))

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 200


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPostion(img, draw=False)
    if len(lmList) != 0:
        # print(lmList [4], lmList[8])

        x1, y1 = lmList[4][1], lmList [4][2]
        x2, y2 = lmList[8][1], lmList [8][2]
        cx,cy = (x1+x2) // 2, (y1+y2)//2

        cv.circle(img, (x1,y1), 10, (255,0,255), cv.FILLED)
        cv.circle(img, (x2,y2), 10, (255,0,255), -1)
        cv.line(img, (x1,y1), (x2,y2), (255,0,0), 2)
        cv.circle(img, (cx,cy), 10, (255,0,255), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range min 50, max 300
        # Volume Range min -65, max 0

        vol = np.interp(length, [35,200], [minVol, maxVol])
        volBar = np.interp(length, [35,200], [300, 150])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length <50:
            cv.circle(img, (cx,cy), 10, (0,255,0), cv.FILLED)
    cv.rectangle(img, (50,150), (86,300), (0,255,0), 2)
    cv.rectangle(img, (50,int(volBar)), (86,300), (0,255,0), -1)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime =  cTime

    cv.putText(img, f"FPS: {int(fps)}", (40,70), cv.FONT_HERSHEY_COMPLEX, 1, (200,255,0), 2)

    cv.imshow("Img", img)
    cv.waitKey(10)