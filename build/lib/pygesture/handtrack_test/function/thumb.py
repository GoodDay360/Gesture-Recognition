def check(ht,cv2,np,hands,img,hand):
    check_thumb = False
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        result=None
        num_check = 0
        lms_index = np.array([8,12,16,20])
        if label == "Right" and "Right" not in hand:   
            for i in lms_index:
                if lms[i].x < lms[i-2].x:
                    num_check+=1
            if num_check==4:
                if lms[2].x < lms[6].x:
                    if lms[2].y >  lms[4].y:
                        if lms[5].y<lms[17].y and lms[4].x<lms[5].x:
                            result = True
                            hand.append(label)
                    if lms[2].y <  lms[4].y:
                        if lms[5].y>lms[17].y:
                            result = False
                            hand.append(label)

        if label == "Left" and "Left" not in hand:
            for i in lms_index:
                if lms[i].x > lms[i-2].x:
                    num_check+=1
            if num_check==4:
                if lms[2].x > lms[6].x:
                    if lms[2].y >  lms[4].y:
                        if lms[5].y<lms[17].y and lms[4].x > lms[5].x:
                            result = True
                            hand.append(label)
                    if lms[2].y <  lms[4].y:
                        if lms[5].y>lms[17].y:
                            result = False
                            hand.append(label)
        # print(result)
        if result == True:
            if label == "Right":
                cv2.rectangle(img,(25,25),(550,150),(0,255,0),-1)
                cv2.putText(img,"Good Job!",(50,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA) 
                hand.append(label)
            elif label == "Left":
                cv2.rectangle(img,(725,25),(1250,150),(0,255,0),-1)
                cv2.putText(img,"Good Job!",(750,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 
                hand.append(label)
            check_thumb = True
        elif result == False:
            if label == "Right":
                cv2.rectangle(img,(25,25),(375,150),(0,255,0),-1)
                cv2.putText(img,"Dislike",(50,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA) 
                hand.append(label)
            elif label == "Left":
                cv2.rectangle(img,(900,25),(1250,150),(0,255,0),-1)
                cv2.putText(img,"Dislike",(925,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 
                hand.append(label)
            check_thumb = True
    if check_thumb:
        return True, img, hand
