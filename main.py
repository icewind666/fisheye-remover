from __future__ import print_function
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
import os

#ffmpeg -copyts -ss 0 -i videoin.mp4 -t 15 -map 0 -c copy output.mp4

def splitfn(fn):
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    return path, name, ext

FILENAME_IN = "output.mp4"
FILENAME_OUT = "videoout.mp4"
CODEC = 'mp4v' 

'''
RMS: 1.0232805493307346
camera matrix:
 [[411.23452732   0.         323.07708657]
 [  0.         418.3698091  218.38142494]
 [  0.           0.           1.        ]]
distortion coefficients:  [-5.62910773e-01  3.19492518e-01  6.51250721e-03  1.80968153e-05
 -8.27330403e-02]
'''
camera_matrix = np.array([[413.69109211, 0.00000000e+00,  323.78181004],
                          [0.00000000e+00,  421.39338767, 217.91319701],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]);
dist_coefs = np.array([-5.69076469e-01,  3.26036238e-01, 6.83031393e-03, 9.35904926e-05,  -8.47810552e-02]);

print ("OpenCV version : {0}".format(cv2.__version__))
print((cv2.__version__).split('.'))
# Load video
video = cv2.VideoCapture(FILENAME_IN)

fourcc = cv2.VideoWriter_fourcc(*list(CODEC))

fps = video.get(cv2.CAP_PROP_FPS)
print(fps)

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
sizew = (640, 480)
print(size)
writer = cv2.VideoWriter(FILENAME_OUT, fourcc, 30, sizew)

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (size[0], size[1]), 1, (size[0], size[1]))
x, y, w, h = roi
M = cv2.getRotationMatrix2D((size[0]/2,size[1]/2),5,1)

while video.grab() is True:
    print("On frame %i of %i."%(video.get(cv2.CAP_PROP_POS_FRAMES), frame_count))

    frame = video.retrieve()[1]
    #print(frame)
    frame = cv2.undistort(frame, camera_matrix, dist_coefs, None, newcameramtx)
    #frame = frame[y:y+h-50, x+70:x+w-20]
    #print(frame)
    writer.write(frame)
video.release()
writer.release()