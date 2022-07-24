import cv2
from cv2 import VideoCapture
from cv2 import CHAIN_APPROX_SIMPLE
from cv2 import circle
import numpy as np
import screeninfo


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 45)
def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect=[]
counter=0
face_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_frontalface_alt2.xml')

while True:
    ret, frame=cap.read()
    cv2.line(frame,(0,200),(650,200),(255,255,190),1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces1 = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces2 = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(20,255,0),1)
    
        center=center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame,center,4,(0,0,255),-1)

        for(x,y) in detect:
            if((y<200+3) and (y>200-3)):
                counter=counter+1

        detect.remove((x,y))
        print("People Counted",str(counter))
        cv2.putText(faces,"People's Count: "+str(counter),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    cv2.putText(frame,"People's Count: "+str(counter),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    cv2.namedWindow("WindowName",cv2.WINDOW_FULLSCREEN)
    window_name = 'People Counting System CVF Project'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name,frame)
    if(cv2.waitKey(1)==13):
        break

cv2.destroyAllWindows()
cap.release()
