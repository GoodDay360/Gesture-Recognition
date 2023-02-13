import handtrack as ht
import cv2,os
from PIL import Image
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ht = ht.handDetector()
while True:
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    success, img = cap.read()
    # img = Image.open(os.path.join(CurrentDir,"2hand.jpg"))
    # img = img.convert("RGB")
    # img = np.asarray(img)
    img, hands = ht.findHands(img)
    if hands:
        for i in hands:
            label = i["label"]
            lms = i["lms"]
            result=0
            if lms[17].x < lms[5].x and lms[4].x > lms[3].x:
                if lms[16].y > lms[14].y and lms[12].y > lms[9].y:
                    if lms[8].y < lms[6].y:
                        result+=1
                    if lms[4].x > lms[1].x:
                        result+=1
                    if lms[20].y < lms[17].y:
                        result+=1
            if lms[17].x > lms[5].x and lms[4].x < lms[3].x:
                if lms[16].y > lms[14].y and lms[12].y > lms[9].y:
                    if lms[8].y < lms[6].y:
                        result+=1
                    if lms[4].x < lms[1].x:
                        result+=1
                    if lms[20].y < lms[17].y:
                        result+=1
            if result == 3:
                cv2.rectangle(img,(25,25),(575,150),(0,255,0),-1)
                cv2.putText(img,"I Love You",(50,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 

    cv2.imshow("Image", img)
    cv2.waitKey(1)