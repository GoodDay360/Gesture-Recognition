def check(cv2,np,hands,img,hand):
    check_peace = False
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        result=0
        num_check = 0
        
        lms_index = np.array([16,20])
        for i in lms_index:
            if lms[i].y > lms[i-2].y:
                num_check+=1
        if num_check==2:
            if label == "Left" and "Left" not in hand:
                if lms[17].x > lms[5].x:
                    if lms[4].x > lms[5].x:
                        result += 1
                    if lms[8].y < lms[6].y:
                        result+=1
                    if lms[12].y < lms[10].y:
                        result+=1
            if label == "Right" and "Right" not in hand:
                if lms[17].x < lms[5].x:
                    if lms[4].x < lms[5].x:
                        result += 1
                    if lms[8].y < lms[6].y:
                        result+=1
                    if lms[12].y < lms[10].y:
                        result+=1
        if result == 3:
            check_peace = True
            if label == "Right":
                cv2.rectangle(img,(25,25),(350,150),(0,255,0),-1)
                cv2.putText(img,"Peace",(50,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA) 
                hand.append(label)
            elif label == "Left":
                cv2.rectangle(img,(925,25),(1250,150),(0,255,0),-1)
                cv2.putText(img,"Peace",(950,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 
                hand.append(label)
    if check_peace:
        return True,img,hand

