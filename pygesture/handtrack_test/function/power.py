def check(cv2,np,hands,img,hand):
    result = False
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        
        result=None
        num_check = 0
        lms_index = np.array([6,10,14,18])
        if label == "Right":
            for i in lms_index:
                if lms[i].y < lms[i+1].y:
                    num_check+=1
                if num_check==4:
                    if lms[4].x < lms[3].x and lms[4].y>lms[i].y:
                            result=True
                    elif lms[4].x < lms[3].x and lms[4].y<lms[i].y:
                            result=True
        if label == "Left":
            for i in lms_index:
                if lms[i].y < lms[i+1].y:
                    num_check+=1
                if num_check==4:
                    if lms[4].x > lms[3].x and lms[4].y>lms[i].y:
                        result=True
                    elif lms[4].x > lms[3].x and lms[4].y<lms[i].y:
                        result=True

        if result == True:
            if label == "Right" and "Right" not in hand:
                cv2.rectangle(img,(25,25),(350,150),(0,255,0),-1)
                cv2.putText(img,"Power",(50,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA) 
                hand.append(label)

            elif label == "Left" and "Left" not in hand:
                cv2.rectangle(img,(925,25),(1250,150),(0,255,0),-1)
                cv2.putText(img,"Power",(950,120),
                            cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 
                hand.append(label)
    if result:            
        return True,img,hand