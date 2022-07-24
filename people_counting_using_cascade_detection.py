# importing opencv module cv2
import cv2

# importing openncv video capture function
from cv2 import VideoCapture

# capturing web cam 0 (First Web cam)
cap = cv2.VideoCapture(0)

# controlling frames per second
cap.set(cv2.CAP_PROP_FPS, 45)

# calculating center of rectangle
def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect=[]

# counter to count detected people's
counter=0

# Haar Cascade file which contains dataset of face
face_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_frontalface_alt2.xml')

# While condition to run web cam continuously
while True:

    # ret stores boolean value True or False for frame
    # frame stores image from cap.read()
    ret, frame=cap.read()

    # Line which help us to count detected people
    cv2.line(frame,(0,200),(650,200),(255,255,190),1)

    # Converting bgr image to gray image (Because rgba takes 24 bits and gray scale takes 8 bits)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # .detectMultiScale() function gives a rectangle with contains face coordinates 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop to draw rectangles for more than one faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(20,255,0),1)

        # Getting cx and cy values with the help of x,y,w,h of a rectangle i.e rectangle center point
        center=center_handle(x,y,w,h)

        # appending center to detect list (cx and cy)
        detect.append(center)


        # Drawing a circle in the center of each rectangle
        cv2.circle(frame,center,4,(0,0,255),-1)

        # taking x and y of detect and comparing it with y of line
        for(x,y) in detect:
            if((y<200+3) and (y>200-3)):
                
                # if detected face is in the coordinates of y we will count +1 
                counter=counter+1
        # Also we will remove (x,y) from list
        detect.remove((x,y))
        print("People Counted",str(counter))
        cv2.putText(faces,"People's Count: "+str(counter),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    
    # Total People count
    cv2.putText(frame,"People's Count: "+str(counter),(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    
    # windows full screen view

    # this method creates a new window with name and size
    window_name = 'People Counting System CVF Project'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_FULLSCREEN)

    # Showing frames inside a window
    cv2.imshow(window_name,frame)

    #This cv2.waitkey(1) checks for pressed key in this case if we press ENTER (13) our program will break
    if(cv2.waitKey(1)==13):
        break

# Destroying all windows
cv2.destroyAllWindows()

# Releasing all frames in memory 
cap.release()
