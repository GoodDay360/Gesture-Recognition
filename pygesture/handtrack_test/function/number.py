def check(cv2,np,hands,img,hand):
    result = True
    not_draw = True
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        number = 0
        if label not in hand:
            index = np.array([8,12,16,20])
            if len(hands)>1:
                lms_1 = hands[0]["lms"]
                lms_2 = hands[1]["lms"]
                if lms_1[17].y < lms_1[1].y and lms_2[17].y < lms_2[1].y:
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
                if lms[17].y < lms[1].y:
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
            result = True
            cv2.rectangle(img,(25,25),(200,150),(0,255,0),-1)
            cv2.putText(img,str(number),(50,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)
            hand.append(label)
        elif number > 0:
            if len(hand) != 0 and not_draw:
                if label == "Right" and "Right" not in hand:
                    result = True
                    cv2.rectangle(img,(25,25),(150,150),(0,255,0),-1)
                    cv2.putText(img,str(number),(60,120),
                                        cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)
                    hand.append(label)
                elif label == "Left" and "Left" not in hand:
                    result = True
                    cv2.rectangle(img,(1125,25),(1250,150),(0,255,0),-1)
                    cv2.putText(img,str(number),(1160,120),
                                        cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
                    hand.append(label)
            else:
                result = True
                cv2.rectangle(img,(25,25),(150,150),(0,255,0),-1)
                cv2.putText(img,str(number),(60,120),
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)
                hand.append(label)
                not_draw = False
    if result:
        return True, img, hand
        
