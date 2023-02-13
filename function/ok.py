def check(cv2,np,hands,img,hand):
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        result=None
        num_check = 0
        lms_index = np.array([12,16,20])
        if label == "Right" and "Right" not in hand:   
            for i in lms_index:
                if lms[i].y < lms[i-1].y and lms[i-1].y < lms[i-2].y and lms[i-2].y <lms[i-3].y:
                    num_check+=1
            if num_check==3:
                if lms[4].x > lms[5].x and lms[8].x >lms[5].x:
                    if lms[4].y <  lms[2].y and lms[8].y > lms[6].y:
                        dis = (lms[8].y*100)/lms[4].y
                    else :
                        dis = 0
                    if dis >=90:
                        result = True

        if label == "Left" and "Left" not in hand:
            for i in lms_index:
                if lms[i].y < lms[i-1].y and lms[i-1].y < lms[i-2].y and lms[i-2].y <lms[i-3].y:
                    num_check+=1
            if num_check==3:
                if lms[4].x < lms[5].x and lms[8].x < lms[5].x:
                    if lms[4].y <  lms[2].y and lms[8].y > lms[6].y:
                        dis = (lms[8].y*100)/lms[4].y
                    else :
                        dis = 0
                    if dis >=90:
                        result = True

        if result == True:
            if label == "Right":
                cv2.rectangle(img,(25,25),(200,150),(0,255,0),-1)
                cv2.putText(img,"OK",(50,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA)
                hand.append(label)
            elif label == "Left":
                cv2.rectangle(img,(1075,25),(1250,150),(0,255,0),-1)
                cv2.putText(img,"OK",(1100,120),
                                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA)
                hand.append(label)
                
    if result:
        return True,img,hand