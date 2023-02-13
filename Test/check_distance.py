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
            cv2.putText(img,str(label),(ht.getCoord(lms[0]).x,ht.getCoord(lms[0]).y),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
            result = None
            if lms[8].x > lms[4].x:
                result = (lms[4].x*100)/lms[8].x
            elif lms[8].x < lms[4].x:
                result = (lms[8].x*100)/lms[4].x
            print(result)
    cv2.imshow("Image", img)
    cv2.waitKey(1)