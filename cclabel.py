#!/usr/bin/env python
""" cclabel labels connected components with the sequential method.
    Runs faster than [slowlabel.py]
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

# Create a 1 pixel bounding box around image array [im].
tmimage = vx.Vx( inimage ) 
tmimage.embedim((1,1,1,1))
tm = tmimage.i

# Set all pixels in [im] to 0.
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        im[y,x] = 0

label = 0
equiv_map = {} # [equiv_map] represents the equivalent table that shows equivalency relation between different labels.

# First pass over the image array: for all object pixels, first checks if adjacent above (Pu) and left (Pl) pixels are labeled, and if they are, let im[y,x] = Pu or Pl. If neither Pu, Pl are labeled, assume im[y,x] is a new object, and give it a new label = label + 1.
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        # Search for unlabeled objects. If pixel unlabeled, check if Pl, Pu have labels. If not, create new label, else label pixel Pl or Pu.
        if (tm[y+1,x+1] != 0 and im[y,x] == 0): 
            # Give im[y,x] label Pu.
            if (im[y-1,x] != 0): 
                im[y,x] = im[y-1,x]
            # Give im[y,x] label Pl.
            elif (im[y, x-1] != 0): im[y,x] = im[y,x-1]
            # If Pl, Pu do not have label, increment label.
            else:
                label = label + 1
                im[y,x] = label

            # If im[y,x] is an object, Pu and Pl have different labels, make labels Pu, Pl equivalent.
            if (im[y, x-1] != im[y-1, x] and min(im[y, x-1], im[y-1, x]) != 0): 
                if (im[y, x-1] in equiv_map): 
                    equiv_map[im[y-1,x]] = equiv_map.get(im[y, x-1])
                elif (im[y-1, x] in equiv_map): 
                    equiv_map[im[y,x-1]] = equiv_map.get(im[y-1, x])
                else:
                    equiv_map[im[y, x-1]] = min(im[y, x-1], im[y-1, x])
                    equiv_map[im[y-1,x]] = min(im[y, x-1], im[y-1, x])

# Second pass over the labeled image array: merge all objects together with equivalent labels.
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        if (im[y,x] in equiv_map): 
            # Give im[y,x] label Pu.
            im[y,x] = equiv_map.get(im[y,x])
            
if optv:
   print (im)

inimage.write(vargs['of'])