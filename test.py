from pygesture import handtrack
import cv2

# [int] maxHand: The maximum amount hand that allowed to be track.
# [bool] drawLandmark: Draw on landmark and connect them together.
# You can also put nothing in there it will also work.
# Ex: handtrack.handDetector()
# There are more options available, you can check the source code if want to learn more.
ht = handtrack.handDetector(maxHand=2, drawLandmark=True)
cap = cv2.VideoCapture(0)

# This is a config for camera resolution.
# But the quality still limit by your camera.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    success, img = cap.read()
    
    # The value will return everything you need.
    # img: is the image result.
    # hand: is the value of left or right hand and value of each landmarks on each hand.
    img, hand = ht.findHands(img)
    
    # Print it out to see what going on.
    print(hand)
    
    # "Hand Track" you can name it whatever you want. But other options may required.
    cv2.namedWindow("Hand Track", cv2.WND_PROP_FULLSCREEN)
    
    # [Optional] You can use this if you want full screen.
    cv2.setWindowProperty("Hand Track",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    # Display output image.
    cv2.imshow("Hand Track", img)
    
    # Wait in milliseconds before capture next frame.
    cv2.waitKey(1)
