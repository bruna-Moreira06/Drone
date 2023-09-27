import time
import cv2

def findFace(img):

 faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 faces = faceCascade.detectMultiScale(imgGray,1.2,4)
 myFaceListC = []
 myFaceListArea = []
 for(x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    cx = x+w//2
    cy = y+h//2
    area = w
    myFaceListArea.append(area)
    myFaceListC.append([cx,cy])
 if len(myFaceListArea) !=0:
    i = myFaceListArea.index(max(myFaceListArea))
    return img,[myFaceListC[i],myFaceListArea[i]]
 else:
    return img, [[0,0],0]


def webcam():
    cap = cv2.VideoCapture(0)

    while True:
        success,img=cap.read()
        img,_=findFace(img)
        cv2.imshow('face',img)
        k=cv2.waitKey(30)
        if k==27:
            tello.land()
    
