import handtrack as ht
import cv2,os
from PIL import Image
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ht = ht.handDetector()
currentDir = os.path.dirname(os.path.realpath(__file__))

stopSign = Image.open(os.path.join(currentDir,"assets","stop.png"))
stopSign = stopSign.resize((200, 200), Image.Resampling.LANCZOS)


while True:
    success, img = cap.read()
    # img = Image.open(os.path.join(currentDir,"2hand.jpg"))
    # img = img.convert("RGB")
    # img = np.asarray(img)
    img, hands = ht.findHands(img)
    
    # img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # img = img_pil.copy()
    # stopSign = stopSign.resize((100, 100), Image.ANTIALIAS)
    # img.paste(stopSign,(100, 50),mask=stopSign)
    # img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    
    if hands:
        for i in hands:
            label = i["label"]
            lms = i["lms"]
            cv2.putText(img,str(label),(ht.getCoord(lms[0]).x,ht.getCoord(lms[0]).y),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            lms_index = np.array([8,12,16,20])
            result = 0
            for i in lms_index:
                if lms[i].y > lms[i-2].y:
                    result += 1
            if result != 4:
                lms_index = np.array([8,16,20])
                result = 0
                for i in lms_index:
                    if lms[i].y > lms[i-2].y:
                        result+=1
                if result == 3:
                    if lms[12].y < lms[10].y:
                        result+=1
                        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                        img = img.copy()
                        if label == "Left":
                            img.paste(stopSign,(ht.getCoord(lms[11]).x-85,ht.getCoord(lms[11]).y),mask=stopSign)
                        elif label == "Right":
                            img.paste(stopSign,(ht.getCoord(lms[11]).x-105,ht.getCoord(lms[11]).y),mask=stopSign)
                        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
        if result != 4:
            number = 0
            index = np.array([8,12,16,20])
            if len(hands)>1:
                lms_1 = hands[0]["lms"]
                lms_2 = hands[1]["lms"]
                for i in np.arange(4):
                    if lms_1[index[i]].y < lms_1[index[i]-1].y:
                        number += 1
                    if lms_2[index[i]].y < lms_2[index[i]-1].y:
                        number += 1
                for i in hands:
                    lms = i["lms"]
                    if lms[17].x > lms[5].x:
                        if (lms[4].x < lms[3].x and lms[4].x < lms[2].x):
                            number += 1
                    elif lms[17].x < lms[5].x:
                        if (lms[4].x > lms[3].x and lms[4].x > lms[2].x):
                            number += 1
            else:
                lms = hands[0]["lms"]
                for i in np.arange(4):
                    if lms[index[i]].y < lms[index[i]-1].y:
                        number += 1
                if lms[17].x > lms[5].x:
                    if (lms[4].x < lms[3].x and lms[4].x < lms[2].x):
                        number += 1
                elif lms[17].x < lms[5].x:
                    if (lms[4].x > lms[3].x and lms[4].x > lms[2].x):
                        number += 1
            if number == 10:
                cv2.rectangle(img,(25,25),(200,150),(0,255,0),-1)
                cv2.putText(img,str(number),(50,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
            elif number > 0:
                cv2.rectangle(img,(25,25),(150,150),(0,255,0),-1)
                cv2.putText(img,str(number),(60,120),
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
            print(number)

    cv2.imshow("HandTrack", img)
    cv2.waitKey(1)