#!/usr/bin/env python
""" boundpy
"""

import numpy as np
import cv2

def boundpy(im : np.ndarray, of):
    # Make 1 pixel bounding box around entire image array. [tm] is transformed matrix with 
    # 1 pixel bounding box: mapping T(x,y) such that x -> x+1, y -> y+1.
    tm = embedim(im, (1,1,1,1))

    # Maps pixels in image [im] to either background, boundary, or interior pixel values.
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if (tm[y+1,x+1] != 0):
                # Check if boundary:
                if (min(tm[y+1,x], tm[y,x], tm[y,x+1], tm[y,x+2], tm[y+1,x+2], tm[y+2,x+2], tm[y+2,x+1], tm[y+2,x]) == 0):
                    im[y,x] = 255
                else:
                    im[y,x] = 128
        
    dispmvx(im)
    cv2.imwrite(of, im)
