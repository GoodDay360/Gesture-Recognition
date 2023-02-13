import cv2, os
import mediapipe as mp
from collections import namedtuple

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplex=1, detectionCon=0.5, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(mode, maxHands, modelComplex, detectionCon, trackCon)
    
    def getCoord(self,lm):
        h, w, c = self.img.shape
        coord = namedtuple('coord', ['x', 'y'])
        coord = coord(int(lm.x*w), int(lm.y*h))
        return coord
    
    def findHands(self,img):
        self.img = img
        imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        hand_li = None
        if self.results.multi_hand_landmarks:
            hand_li = []
            for hand_index, handLms in enumerate(self.results.multi_hand_landmarks):
                label = self.results.multi_handedness[hand_index].classification[0].label
                if label == "Left":
                    label = "Right"
                    color = (0,0,255) #Red
                else:
                    label = "Left"
                    color = (255,0,0) #Blue
                self.mpDraw.draw_landmarks(self.img, handLms, self.mpHands.HAND_CONNECTIONS, 
                                        # Joint Land Mark Color
                                        self.mpDraw.DrawingSpec(color=color, thickness=2, circle_radius=2),
                                        # Land Mark Line Connector Color
                                        self.mpDraw.DrawingSpec(color=color, thickness=2, circle_radius=2))
                hand = {
                    "label": label,
                    "lms": handLms.landmark
                }
                hand_li.append(hand)
        return self.img, hand_li
    
def track():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ht = handDetector()
    while True:
        CurrentDir = os.path.dirname(os.path.realpath(__file__))
        success, img = cap.read()
        #img = Image.open(os.path.join(CurrentDir,"1hand.jpg"))
        #img = Image.open(os.path.join(CurrentDir,"1handleft.jpg"))
        #img = Image.open(os.path.join(CurrentDir,"1handright.jpg"))
        #img = Image.open(os.path.join(CurrentDir,"2hand.jpg"))
        #img = img.convert("RGB")
        #img = np.asarray(img)
        img, hands = ht.findHands(img)
        print(hands)
        if hands:
            for i in hands:
                label = i["label"]
                lms = i["lms"]
                cv2.putText(img,str(label),(ht.getCoord(lms[0]).x,ht.getCoord(lms[0]).y),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)

        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    track()