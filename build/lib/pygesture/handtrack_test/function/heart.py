def check(ht,cv2,np,Image,hands,img,hand,heartImg,heartLeftImg,heartRightImg):
    heart = half_heart_left = half_heart_right = False
    for i in hands:
        label = i["label"]
        lms = i["lms"]
        num_check = 0
        lms_index = np.array([8,12,16,20])
        if label == "Right" and "Right" not in hand:
            for i in lms_index:
                if lms[i].x > lms[i-2].x:
                    num_check+=1
            if num_check==4:
                if lms[i].y >lms[i-2].y and lms[i].y < lms[4].y and lms[i-2].y < lms[4].y:
                    if lms[i].y > lms[4].y:
                        dis = (lms[4].y*100)/lms[i].y
                    elif lms[i].y < lms[4].y:
                        dis = (lms[i].y*100)/lms[4].y   
                    if dis <= 86:
                        half_heart_right = True
        elif label == "Left" and "Left" not in hand:
            for i in lms_index:
                if lms[i].x < lms[i-2].x:
                    num_check += 1
            if num_check==4:
                if lms[i].y >lms[i-2].y and lms[i].y < lms[4].y and lms[i-2].y < lms[4].y:
                    if lms[i].y > lms[4].y:
                        dis = (lms[4].y*100)/lms[i].y
                    elif lms[i].y < lms[4].y:
                        dis = (lms[i].y*100)/lms[4].y
                    if dis <= 86:
                        half_heart_left = True
    if half_heart_right and half_heart_left:
        lms_index = np.array([4,8,12,16,20])
        lms1 = hands[0]["lms"]
        lms2 = hands[1]["lms"]
        result = 0
        for i in lms_index:
            if lms1[i].x > lms2[i].x:
                dis_x = (lms2[i].x*100)/lms1[i].x
            elif lms1[i].x < lms2[i].x:
                dis_x = (lms1[i].x*100)/lms2[i].x
            if lms1[i].y > lms2[i].y:
                dis_y = (lms2[i].y*100)/lms2[i].y
            elif lms1[i].y < lms2[i].y:
                dis_y = (lms1[i].y*100)/lms2[i].y
            if dis_x >= 90 and dis_y >= 90:
                result += 1
                
        if result == 5:
            heart = True
            
    if heart:
        heart = True
        lms1 = hands[0]["lms"][0]
        lms2 = hands[1]["lms"][0]
        lms_x = int((ht.getCoord(lms1).x+ht.getCoord(lms2).x)/2)
        lms_y = int((ht.getCoord(lms1).y+ht.getCoord(lms2).y)/2)
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = img.copy()
        img.paste(heartImg,(lms_x-100,lms_y-175),mask=heartImg)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        hand.append("Right")
        hand.append("Left")
        return True,img,hand

    elif half_heart_right or half_heart_left:
        heart = True
        for i in hands:
            label = i["label"]
            lms = i["lms"]
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img = img.copy()
            if label == "Left" and "Left" not in hand:
                if half_heart_left:
                    hand.append(label)
                    img.paste(heartLeftImg,(ht.getCoord(lms[4]).x-75,ht.getCoord(lms[4]).y-200),mask=heartLeftImg)
            elif label == "Right" and "Right" not in hand:
                if half_heart_right:
                    hand.append(label)
                    img.paste(heartRightImg,(ht.getCoord(lms[4]).x-225,ht.getCoord(lms[4]).y-200),mask=heartRightImg)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return True,img,hand