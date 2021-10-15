import string
import random
import cv2
import numpy as np

def gen_name(N=7):
    return str(''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N))) + ".png"

def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def invert_grayscale(grayed):
    return cv2.bitwise_not(grayed)

def blur_img(img):
    return cv2.GaussianBlur(img, (19, 19), sigmaX=0, sigmaY=0)

def highlight_edges(img):
    lineSize=7
    blurValue=7
    gray=convert_to_grayscale(img)
    grayBlur=cv2.medianBlur(gray,blurValue)
    edges=cv2.adaptiveThreshold(grayBlur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,lineSize,blurValue)
    return edges

def invert_colors(img):
    colors=9
    data=np.float32(img).reshape((-1,3))
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)
    ret,label,center=cv2.kmeans(data,colors,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center=np.uint8(center)
    result=center[label.flatten()]
    result=result.reshape(img.shape)
    return result