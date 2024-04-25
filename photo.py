from __future__ import print_function
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
import os

def splitfn(fn):
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    return path, name, ext

img_names_undistort = glob.glob("coeffs/*.png")
new_path = "tmp/"

camera_matrix = np.array([[413.69109211, 0.00000000e+00,  323.78181004],
                          [0.00000000e+00,  421.39338767, 217.91319701],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]);
dist_coefs = np.array([-5.69076469e-01,  3.26036238e-01, 6.83031393e-03, 9.35904926e-05,  -8.47810552e-02]);

i = 0

#for img_found in img_names_undistort:
while i < len(img_names_undistort):
    img = cv2.imread(img_names_undistort[i])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))

    dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)

    # crop and save the image
    x, y, w, h = roi
    dst = dst[y:y+h-50, x+70:x+w-20]

    name = img_names_undistort[i].split("/")
    print(name)
    name = name[1].split(".")
    name = name[0]
    full_name = new_path + name + '.jpg'

    #outfile = img_names_undistort + '_undistorte.png'
    print('Undistorted image written to: %s' % full_name)
    cv2.imwrite(full_name, dst)
    i = i + 1