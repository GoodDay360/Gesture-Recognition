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
                        lms_index = np.array([6,10,14,18])
                        if label == "Right":
                                for i in lms_index:
                                        if lms[i].y < lms[i+1].y:
                                                num_check+=1
                                        if num_check==4:
                                                if lms[4].x < lms[3].x and lms[4].y>lms[i].y:
                                                        result=True
                                                elif lms[4].x < lms[3].x and lms[4].y<lms[i].y:
                                                        result=True
                        if label == "Left":
                                for i in lms_index:
                                        if lms[i].y < lms[i+1].y:
                                                num_check+=1
                                        if num_check==4:
                                                if lms[4].x > lms[3].x and lms[4].y>lms[i].y:
                                                        result=True
                                                elif lms[4].x > lms[3].x and lms[4].y<lms[i].y:
                                                        result=True
                
                        if result == True:
                                cv2.rectangle(img,(25,25),(350,150),(0,255,0),-1)
                                cv2.putText(img,"Power",(50,120),
                                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
                                # cv2.putText(img,"Power",(ht.getCoord(lms[11]).x,ht.getCoord(lms[11]).y),
                                # cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,153),2,cv2.LINE_AA)    


        cv2.imshow("Image", img)
        cv2.waitKey(1)