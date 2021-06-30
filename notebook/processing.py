import numpy as np
import cv2
from PIL import Image

def resize(img):
    img = np.array(img)
    if img.shape[0] != 72 :
        resized_img = cv2.resize(img,(72,72))
        return (resized_img)  
    else: return img


def rev(img):
    img = np.array(img)
    img_cropped = img[:, 20:140, :]
    img = cv2.resize(img_cropped,(72,72))
    cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return cv2_im

