import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

class Vx():
    def read_csv(ifile, whitespace=False):
        ''' read a csv file or file with whitespace separators
            and return vx ubyte image file
            only 2D images supported
        '''
        if whitespace:
            df = pd.read_csv(ifile, header=None, sep='\s+')
        else:
            df = pd.read_csv(ifile, header=None, )
        return df.to_numpy(dtype='uint8', copy=True)

    def read_img(ifile, flag=cv2.IMREAD_GRAYSCALE):
        return cv2.imread(ifile, flag)