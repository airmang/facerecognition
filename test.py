from utils1 import *
import cv2


w, h= 360, 240
pid = [0.7, 0.5, 0]
pError = 0
startCounter = 0

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
myDrone = initializeTello()

while True:

    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    img = telloGetFrame(myDrone, w, h)

    img, info = findFace(img)

    pError = trackFace(myDrone, info, w, pid, pError)
    #print(info[0][0])
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break