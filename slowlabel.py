#!/usr/bin/env python
""" slowlabel labels connected components with the recursive method.
    Is slow for large images.
"""

import numpy as np
from v4 import vx

of=' '
vxif=' '
vargs = vx.vaparse( "if= of= -v  - ")
if '-' in vargs:
   print ("vtempy V4 python local max test program")
   print ("if= input file")
   print ("of= output file")
   print ("[-v] verbose mode")
   exit(0)

# check arguments 
optv = '-v' in vargs
if 'if' in vargs:
   inimage = vx.Vx(vargs['if'])
else:
   print ( 'vtempy  error: if= must be specified')
   exit()
im = inimage.i
if im.dtype != 'uint8' :
    print ('vtempy error: image not byte type', file=sys.stderr)
    exit(1)
# check for output file name
if 'of' not in vargs:
   print ( 'vtempy error: of= must be specified')
   exit()

# Compute max filter
tmimage = vx.Vx( inimage ) 
tmimage.embedim((1,1,1,1))
tm = tmimage.i

for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        im[y,x] = 0
label = 1

def setlabel (x, y, label):
    global im, tm
    im[y,x] = label
    if (tm[y,x+1] != 0 and im[y-1,x] == 0): setlabel(x,y-1,label)
    if (tm[y+1,x+2] != 0 and im[y,x+1] == 0): setlabel(x+1,y,label)
    if (tm[y+2,x+1] != 0 and im[y+1,x] == 0): setlabel(x,y+1,label)
    if (tm[y+1,x] != 0 and im[y,x-1] == 0): setlabel(x-1,y,label)
    
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        # Search for unlabeled objects.
        if (tm[y+1,x+1] != 0 and im[y,x] == 0): 
            setlabel(x,y,label)
            label = label + 1
if optv:
   print (im)

inimage.write(vargs['of'])