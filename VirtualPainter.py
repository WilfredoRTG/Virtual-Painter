import time
import numpy as np
import os
import cv2
import HandTrackingModule as htm

folderPath = "Headers"
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[3]
drawColor = (255,255,255)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1080)

detector = htm.handDetector(detectionCon=0.8)
xp, yp = 0, 0
imgCanvas = np.zeros((720,1280,3), np.uint8)
#show_image= True
while True:

    #Import the image
    success, img = cap.read()
    #img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)

    #Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:


        #tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[16][1:]
        x4, y4 = lmList[20][1:]
        x5, y5 = lmList[4][1:]
        


        #Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        #If selection mode - two finger up
        #print(fingers)
                
        if fingers[0] == True and fingers[1] ==True and fingers[2]==True and fingers[3]==True and fingers[4]== True:
            xp, xy = 0,0
            xp, xy = x1, y1
            
        if fingers[0] == False and fingers[1] ==True and fingers[2]==True and fingers[3]==False and fingers[4]== False:
            xp, yp = 0, 0
            #print("Selection mode activated")
            if y1 < 100:
                if 100<x1<350:
                    header = overlayList[3]
                    drawColor = (255,255,255)
                elif 400<x1<650:
                    header = overlayList[1]
                    drawColor = (255, 202, 51)
                elif 780<x1<950:
                    header = overlayList[2]
                    drawColor = (0, 128, 0)
                elif 1050<x1<1200:
                    header = overlayList[0]
                    drawColor = (0,0,0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            

        #if drawing mode - index finger is up
        if fingers[0] == False and fingers[1] ==True and fingers[2]==False and fingers[3]==False and fingers[4]== False:
            brushThickness = 15
            eraserThickness = 100
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                #print("Drawing mode activated")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp),(x1,y1),drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp),(x1,y1),drawColor, brushThickness)

            xp, yp = x1, y1
        


        #Huge drawing mode (3 fingers up)
        if fingers[0] == False and fingers[1] ==False and fingers[2]==True and fingers[3]==True and fingers[4]== True:
            xp, yp = 0, 0
            #print("The bigger one")
#            print(fingers)
            eraserThickness = 400
            brushThickness  = 60
            cv2.circle(img, (x3, y3), 15, drawColor, cv2.FILLED)
            #print("Drawing mode activated")
            if xp == 0 and yp == 0:
                xp, yp = x3, y3

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x3, y3), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x3, y3), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp),(x3,y3),drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp),(x3,y3),drawColor, brushThickness)

            xp, yp = x3, y3
        
        #Four fingers up
        if fingers[0] == False and fingers[1] ==True and fingers[2]==True and fingers[3]==True and fingers[4]== True:
            xp, yp = 0, 0
            eraserThickness = 500
            brushThickness  = 75
            midx = (x3+x2)//2
            midy = (y3+y2)//2
            cv2.circle(img, (midx, midy), 15, drawColor, cv2.FILLED)
            #print("Drawing mode activated")
            if xp == 0 and yp == 0:
                xp, yp = midx, (y3+y2//2)

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (midx, midy), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (midx, midy), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp),(midx,midy),drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp),(midx,midy),drawColor, brushThickness)

            xp, yp = midx, midy
            
        #Clear screan
        if fingers[0] == True and fingers[1] ==False and fingers[2]==False and fingers[3]==False and fingers[4]== False:
            xp, yp = 0, 0
            if xp == 0 and yp == 0:
                xp, yp = x4, y4
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp),(x4,y4),drawColor, 9999)
                cv2.line(imgCanvas, (xp, yp),(x4,y4),drawColor, 9999)
            xp, xy = x4, y4
        
        #Draw all the screan
        if fingers[0] == True and fingers[1] ==False and fingers[2]==False and fingers[3]==False and fingers[4]== True:
            xp, yp = 0, 0
            if xp == 0 and yp == 0:
                xp, yp = x4, y4
            if drawColor==(0,0,0):
                pass
            else:
                cv2.line(img, (xp, yp),(x4,y4),drawColor, 9999)
                cv2.line(imgCanvas, (xp, yp),(x4,y4),drawColor, 9999)
            xp, xy = x4, y4

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    #Seting the header image
    img[0:100, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5,0)
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
