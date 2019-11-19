# * This is a little code to get a image from a ip camera at TEC.
import numpy as np
from cv2 import cv2
cap = cv2.VideoCapture('http://compu:ICSCcomputec@172.24.15.126/mjpg/video.mjpg')
ret, frame = cap.read()
cv2.imwrite('img.jpg', frame)
