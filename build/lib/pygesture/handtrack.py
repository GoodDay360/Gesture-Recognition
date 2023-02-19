import cv2
import mediapipe as mp
from collections import namedtuple

class handDetector():
    def __init__(self, mode=False, maxHand=2, modelComplex=1, detectionCon=0.5, trackCon=0.5, drawLandmark=True):
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(mode, maxHand, modelComplex, detectionCon, trackCon)
        self.drawLandmark = drawLandmark
    
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
                if self.drawLandmark:
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
    

