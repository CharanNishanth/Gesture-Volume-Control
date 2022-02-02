import cv2
import time
import numpy as np
import HandTrackingModuke as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480  #width and height of the cam

cap=cv2.VideoCapture(0)
cap.set(3,wCam) #id of width is 3
cap.set(4,hCam) #id of height is 4
pTime=0

detector=htm.handDetector(detectionCon=0.7) #creating object for handtracking module


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer=0


while True:
    sucess,img=cap.read()
    img = detector.findHands(img) #detecting hands ands and drawing on it
    lmlist=detector.findPosition(img,draw=False) #getting positions of landmarks
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])

        x1,y1=lmlist[4][1],lmlist[4][2] #getting x and y values of landmark 4
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2 #finding centre between two points


        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED) #drawing circle on landmark 4
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED) #drawing circle on landmark 8
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3) #drawing line between two points
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)  #drawing circle for the centre

        length=math.hypot(x2-x1,y2-y1) #finding length between the two points
        print(length)

        #Hand range 50 - 300
        #volume  Range -65 - 0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED) #changing the color of centre circle if the length is 50

    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)



    cTime=time.time() #fps
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'Fps:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3) #image,string,position,font,scale,color,thickness)

    cv2.imshow("Img",img)
    if cv2.waitKey(1) == 27:
        break
