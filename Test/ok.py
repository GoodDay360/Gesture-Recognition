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
            
            result=None
            num_check = 0
            lms_index = np.array([12,16,20])

            if label == "Right":   
                for i in lms_index:
                    if lms[i].y < lms[i-1].y and lms[i-1].y < lms[i-2].y and lms[i-2].y <lms[i-3].y:
                        num_check+=1
                if num_check==3:
                    if lms[4].x > lms[5].x and lms[8].x >lms[5].x:
                        if lms[4].y <  lms[2].y and lms[8].y > lms[6].y:
                            dis = (lms[8].y*100)/lms[4].y
                        else :
                            dis = 0
                        if dis >=90:
                            result = True


            if label == "Left":
                for i in lms_index:
                    if lms[i].y < lms[i-1].y and lms[i-1].y < lms[i-2].y and lms[i-2].y <lms[i-3].y:
                        num_check+=1
                if num_check==3:
                    if lms[4].x < lms[5].x and lms[8].x < lms[5].x:
                        if lms[4].y <  lms[2].y and lms[8].y > lms[6].y:
                            dis = (lms[8].y*100)/lms[4].y
                        else :
                            dis = 0
                        if dis >=90:
                            result = True

            if result == True:
                cv2.rectangle(img,(25,25),(200,150),(0,255,0),-1)
                cv2.putText(img,"OK",(50,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
                # cv2.putText(img,"OKAY",(ht.getCoord(lms[4]).x,ht.getCoord(lms[4]).y),
                #                 cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)    
    cv2.imshow("Image", img)
    cv2.waitKey(1)