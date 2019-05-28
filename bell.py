import cv2
import numpy as np
import pygame
import time
from pygame import *

cap = cv2.VideoCapture(0)
mixer.init()
m_o = ("bell.mp3")
mixer.music.load(m_o)

while(1):
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    kernel = np.ones((3,3),np.uint8)
    roi = frame[100:300, 100:300]
    blurred_frame = cv2.GaussianBlur(roi, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    cv2.rectangle(frame,(300,100),(100,300),(0,255,0),1)
    lower_skin = np.array([0,20,70], dtype=np.uint8)
    upper_skin = np.array([20,255,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.dilate(mask,kernel,iterations = 4)
    mask = cv2.GaussianBlur(mask,(5,5),100)

    def bell(area):
        if area > 500:
            print('ok')
            mixer.music.play()

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, contour, -2, (0, 255, 0), 3)
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        bell(area)
        break
   
    cv2.imshow('frame',frame)
    cv2.imshow('frame2',mask)
    
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


    
cv2.destroyAllWindows()
cap.release()    
