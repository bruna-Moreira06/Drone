# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:00:27 2023
@author: Bruna
"""
import cv2
import numpy as np
from djitellopy import Tello

from findface import findFace

tello = Tello()
tello.connect()

tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity,tello.yaw_velocity=[0,0,0,0]
tello.send_rc_control(tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity, 
                tello.yaw_velocity)

tello.streamoff()
tello.takeoff()
tello.streamon()
epsilonX2 = 0
epsilonY2 = 0

print(tello.get_battery())

while True:
    # recup de l'image du drone
    img = tello.get_frame_read()
    image=img.frame
    # redimensionnement de l'image capturée 
    image = cv2.resize(image,(360,240))
    image,[[posX,posY],area]=findFace(image)
    cv2.putText(image,f"x:{posX} y:{posY}",[80,80], cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),2)
    cv2.putText(image,f"Largeur:{area}",[150,150], cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),2)
    # afficher l'image        
    cv2.imshow('face',image)
    k=cv2.waitKey(30)
    if k==27:
        tello.land()

    centerX = 180
    epsilonX = posX-centerX
    P_yaw = 0.5
    D_yaw = 0.5
    controller_yaw = (P_yaw * epsilonX) + (D_yaw * (epsilonX - epsilonX2))
    epsilonX2 = epsilonX
    
    tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity=[0,0,0]

    centerY = 120
    epsilonY = posY-centerY
    P_up_down = 0.2
    D_up_down = 0.2
    controller_up_down = (P_up_down * epsilonY) + (D_up_down * (epsilonY - epsilonY2))
    epsilonY2 = epsilonY
    
    if posX!=0:
        yaw_velocity = int(np.clip(controller_yaw,-100,100))
        up_down_velocity = -int(np.clip(controller_up_down, -100, 100))
    else:
        up_down_velocity = 0
        epsilonY=0
        epsilonY2=0
        yaw_velocity=0
        epsilonX=0
        epsilonX2=0
        
    tello.yaw_velocity=yaw_velocity
    tello.up_down_velocity = up_down_velocity
    tello.send_rc_control(tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity, tello.yaw_velocity)
        
    
    P_forback = 0.2
    D_forback = 0.2
    controller_forback = (P_forback * epsilonZ) + (D_forback * (epsilonZ - epsilonZ2))
    epsilonZ2 = epsilonZ

    if area != 0:
        for_back_velocity = int(np.clip(controller_forback, -100, 100))
    else:
        for_back_velocity = 0

    tello.for_back_velocity = for_back_velocity
