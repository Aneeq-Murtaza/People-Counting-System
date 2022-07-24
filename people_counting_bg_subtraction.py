import cv2
from cv2 import VideoCapture
from cv2 import CHAIN_APPROX_SIMPLE
from cv2 import circle
from cv2 import dilate
from cv2 import CHAIN_APPROX_NONE
import numpy as np
import screeninfo
import time

from sqlalchemy import true

cap = cv2.VideoCapture("people_walking_videos/video1.mp4")
cap.set(cv2.CAP_PROP_FPS, 10)
algo=cv2.createBackgroundSubtractorMOG2(history = 200, varThreshold =600)

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect=[]
counter=0
while True:
    ret, frame=cap.read()
    if(ret==True):

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray,(3,3),5)
        img_sub=algo.apply(blur)
        
        dilat=cv2.dilate(img_sub,np.ones((5,5)))
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dilate_addon=cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
        dilate_addon=cv2.morphologyEx(dilate_addon,cv2.MORPH_CLOSE,kernel)
        counter_shape,h=cv2.findContours(dilate_addon,cv2.RETR_TREE,CHAIN_APPROX_SIMPLE)
        cv2.line(frame,(0,250),(1150,250),(255,255,190),4)

        for (i,c) in enumerate(counter_shape):
            (x,y,w,h)=cv2.boundingRect(c)
            validate_counter=(w>=110 and h>=110)
            if not validate_counter:
                continue

            cv2.rectangle(frame,(x,y),(x+w,y+h),(20,255,0),2)

            center=center_handle(x,y,w,h)
            detect.append(center)
            cv2.circle(frame,center,4,(0,0,255),-1)

            for(x,y) in detect:
                if((y<250+6) and (y>250-6)):
                    counter=counter+1
            detect.remove((x,y))
            print("People's Counted",str(counter))
        cv2.putText(frame,"People's Count: "+str(counter),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
        cv2.namedWindow("WindowName",cv2.WINDOW_FULLSCREEN)
        window_name = 'People Counting System CVF Project'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)
        if(cv2.waitKey(1)==13):
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()
