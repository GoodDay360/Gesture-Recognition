def check(ht,cv2,np,Image,hands,img,hand,stopSign):
    middle = False
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        cv2.putText(img,str(label),(ht.getCoord(lms[0]).x,ht.getCoord(lms[0]).y),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        lms_index = np.array([8,12,16,20])
        result = 0
        for i in lms_index:
            if lms[i].y > lms[i-2].y:
                result += 1
        if result != 4:
            lms_index = np.array([8,16,20])
            result = 0
            for i in lms_index:
                if lms[i].y > lms[i-2].y:
                    result+=1
            if result == 3:
                if lms[12].y < lms[10].y:
                    result+=1
                    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    img = img.copy()
                    if label == "Left" and "Left" not in hand:
                        middle = True
                        hand.append(label)
                        img.paste(stopSign,(ht.getCoord(lms[11]).x-85,ht.getCoord(lms[11]).y),mask=stopSign)
                    elif label == "Right" and "Right" not in hand:
                        middle = True
                        hand.append(label)
                        img.paste(stopSign,(ht.getCoord(lms[11]).x-105,ht.getCoord(lms[11]).y),mask=stopSign)
                    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    if middle:
        return True, img, hand
    else:
        result = False
        if result != 4:
            for i in hands:
                label = i["label"]
                lms = i["lms"]
                num_check=0
                if lms[17].x < lms[5].x and lms[4].x > lms[3].x:
                    if lms[16].y > lms[14].y and lms[12].y > lms[9].y:
                        if lms[8].y < lms[6].y:
                            num_check+=1
                        if lms[4].x > lms[1].x:
                            num_check+=1
                        if lms[20].y < lms[17].y:
                            num_check+=1
                if lms[17].x > lms[5].x and lms[4].x < lms[3].x:
                    if lms[16].y > lms[14].y and lms[12].y > lms[9].y:
                        if lms[8].y < lms[6].y:
                            num_check+=1
                        if lms[4].x < lms[1].x:
                            num_check+=1
                        if lms[20].y < lms[17].y:
                            num_check+=1
                if num_check == 3:
                    result = True
                    if label == "Right" and "Right" not in hand:
                        hand.append(label)
                        cv2.rectangle(img,(25,25),(575,150),(0,255,0),-1)
                        cv2.putText(img,"I Love You",(50,120),
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),10,cv2.LINE_AA) 
                    elif label == "Left" and "Left" not in hand:
                        hand.append(label)
                        cv2.rectangle(img,(650,25),(1200,150),(0,255,0),-1)
                        cv2.putText(img,"I Love You",(675,120),
                                    cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),10,cv2.LINE_AA) 
            if result:
                return True, img, hand
