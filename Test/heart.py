import handtrack as ht
import cv2,os
from PIL import Image
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ht = ht.handDetector()
currentDir = os.path.dirname(os.path.realpath(__file__))

heartImg = Image.open(os.path.join(currentDir,"assets","heart.png")).convert("RGBA")
heartImg = heartImg.resize((200, 200), Image.Resampling.LANCZOS)

heartLeftImg = Image.open(os.path.join(currentDir,"assets","heart_left.png")).convert("RGBA")
heartLeftImg = heartLeftImg.resize((250, 250), Image.Resampling.LANCZOS)

heartRightImg = Image.open(os.path.join(currentDir,"assets","heart_right.png")).convert("RGBA")
heartRightImg = heartRightImg.resize((250, 250), Image.Resampling.LANCZOS)




while True:
    CurrentDir = os.path.dirname(os.path.realpath(__file__))
    success, img = cap.read()
    # img = Image.open(os.path.join(CurrentDir,"2hand.jpg"))
    # img = img.convert("RGB")
    # img = np.asarray(img)
    img, hands = ht.findHands(img)
    if hands:
        heart = half_heart_left = half_heart_right = False
        for i in hands:
            label = i["label"]
            lms = i["lms"]
            num_check = 0
            lms_index = np.array([8,12,16,20])
            if label == "Right":
                for i in lms_index:
                    if lms[i].x > lms[i-2].x:
                        num_check+=1
                if num_check==4:
                    if lms[i].y >lms[i-2].y and lms[i].y < lms[4].y and lms[i-2].y < lms[4].y:
                        if lms[i].y > lms[4].y:
                            dis = (lms[4].y*100)/lms[i].y
                        elif lms[i].y < lms[4].y:
                            dis = (lms[i].y*100)/lms[4].y   
                        if dis <= 86:
                            half_heart_right = True
            elif label == "Left":
                for i in lms_index:
                    if lms[i].x < lms[i-2].x:
                        num_check += 1
                if num_check==4:
                    if lms[i].y >lms[i-2].y and lms[i].y < lms[4].y and lms[i-2].y < lms[4].y:
                        if lms[i].y > lms[4].y:
                            dis = (lms[4].y*100)/lms[i].y
                        elif lms[i].y < lms[4].y:
                            dis = (lms[i].y*100)/lms[4].y
                        if dis <= 86:
                            half_heart_left = True
        if half_heart_right and half_heart_left:
            lms_index = np.array([4,8,12,16,20])
            lms1 = hands[0]["lms"]
            lms2 = hands[1]["lms"]
            result = 0
            for i in lms_index:
                if lms1[i].x > lms2[i].x:
                    dis_x = (lms2[i].x*100)/lms1[i].x
                elif lms1[i].x < lms2[i].x:
                    dis_x = (lms1[i].x*100)/lms2[i].x
                if lms1[i].y > lms2[i].y:
                    dis_y = (lms2[i].y*100)/lms2[i].y
                elif lms1[i].y < lms2[i].y:
                    dis_y = (lms1[i].y*100)/lms2[i].y
                if dis_x >= 90 and dis_y >= 90:
                    result += 1
                    
            if result == 5:
                heart = True
            else:
                heart = False
        else:
            heart = False
                
        if heart:
            heart = True
            lms1 = hands[0]["lms"][0]
            lms2 = hands[1]["lms"][0]
            lms_x = int((ht.getCoord(lms1).x+ht.getCoord(lms2).x)/2)
            lms_y = int((ht.getCoord(lms1).y+ht.getCoord(lms2).y)/2)
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img = img.copy()
            img.paste(heartImg,(lms_x-100,lms_y-175),mask=heartImg)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        elif half_heart_right or half_heart_left:
            heart = True
            for i in hands:
                label = i["label"]
                lms = i["lms"]
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                img = img.copy()
                if label == "Left":
                    if half_heart_left:
                        img.paste(heartLeftImg,(ht.getCoord(lms[4]).x-75,ht.getCoord(lms[4]).y-200),mask=heartLeftImg)
                elif label == "Right":
                    if half_heart_right:
                        img.paste(heartRightImg,(ht.getCoord(lms[4]).x-225,ht.getCoord(lms[4]).y-200),mask=heartRightImg)
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


    cv2.imshow("Image", img)
    cv2.waitKey(1)