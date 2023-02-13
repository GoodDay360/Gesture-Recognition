import handtrack as ht
import cv2,os,sys
from PIL import Image
import numpy as np

currentDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(currentDir,"function"))
import number,heart,thumb,power,peace,ok,loveu

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

ht = ht.handDetector()

stopSign = Image.open(os.path.join(currentDir,"assets","stop.png"))
stopSign = stopSign.resize((200, 200), Image.Resampling.LANCZOS)

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
        hand = []
        
        check_loveu = loveu.check(ht,cv2,np,Image,hands,img,hand,stopSign)
        if isinstance(check_loveu,tuple):
            check_loveu, img, hand = check_loveu
            
            
        if len(hand) <= 1:
            check_heart = heart.check(ht,cv2,np,Image,hands,img,hand,heartImg,heartLeftImg,heartRightImg)
            if isinstance(check_heart,tuple):
                check_heart, img, hand = check_heart
                
        if len(hand) <= 1:
            check_thumb = thumb.check(ht,cv2,np,hands,img,hand)
            if isinstance(check_thumb,tuple):
                check_thumb, img, hand = check_thumb
                
        if len(hand) <= 1:
            check_power = power.check(cv2,np,hands,img,hand)
            if isinstance(check_power,tuple):
                check_power, img, hand = check_power

        if len(hand) <= 1:
            check_peace = peace.check(cv2,np,hands,img,hand)
            if isinstance(check_peace,tuple):
                check_peace, img, hand = check_peace
                
        if len(hand) <= 1:
            check_ok = ok.check(cv2,np,hands,img,hand)
            if isinstance(check_ok,tuple):
                check_ok, img, hand = check_ok
        
        if len(hand) <= 1:
            check_number = number.check(cv2,np,hands,img,hand)
            if isinstance(check_number,tuple):
                check_number, img, hand = check_number
        # print(hand)
    cv2.namedWindow("Gesture Recognition", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Gesture Recognition",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Gesture Recognition", img)
    cv2.waitKey(1)