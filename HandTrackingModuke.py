import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                        self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converts bgr image to rgb
        self.results = self.hands.process(imgRGB)  # process frame for rgb image

        if self.results.multi_hand_landmarks:  # checks that it detects multiple hands
             for handLms in self.results.multi_hand_landmarks:   # to acess single hand
                  if draw:
                      self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)  # to draw connections for the hands on frame

        return img
    def findPosition(self,img,handNo=0,draw=True):

        lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):  # for id and x y z coordinates of landmarks
             # print(id,lm)
             h, w, c = img.shape  # height,width channels of image
             cx, cy = int(lm.x * w), int(lm.y * h)  # to get pixel values
             #print(id, cx, cy)
             lmlist.append([id,cx,cy])
             if draw:
                 cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmlist





def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        sucess, img = cap.read()
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        cTime = time.time()  # current time
        fps = 1 / (cTime - pTime)  # frame rate
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)  # (image,frame rate,dimensions,font,scale,purple color,thickness)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ =="__main__":
    main()