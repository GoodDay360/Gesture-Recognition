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
            lms_index = np.array([8,12,16,20])

            lms2_x = lms[2].x
            lms6_x = lms[6].x
            lms4_y=lms[4].y
            lms2_y=lms[2].y
            if label == "Right":   
                for i in lms_index:
                    if lms[i].x < lms[i-2].x:
                        num_check+=1
                if num_check==4:
                    if lms[2].x < lms[6].x:
                        if lms2_y >  lms4_y:
                            if lms[5].y<lms[17].y and lms[4].x<lms[5].x:
                                result = True
                            
                        if lms2_y <  lms4_y:
                            if lms[5].y>lms[17].y:
                                result = False

            if label == "Left":
                for i in lms_index:
                    if lms[i].x > lms[i-2].x:
                        num_check+=1
                if num_check==4:
                    if lms[2].x > lms[6].x:
                        if lms2_y >  lms4_y:
                            if lms[5].y<lms[17].y:
                                result = True
                        if lms2_y <  lms4_y:
                            if lms[5].y>lms[17].y and lms[4].x<lms[5].x:
                                result = False
            # print(result)
            if result == True:
                cv2.putText(img,"Good Job!",(ht.getCoord(lms[4]).x,ht.getCoord(lms[4]).y),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)    
            elif result == False :
                cv2.putText(img,"Dislike",(ht.getCoord(lms[4]).x,ht.getCoord(lms[4]).y),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)              
            

    cv2.imshow("Image", img)
    cv2.waitKey(1)