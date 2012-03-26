#!/usr/bin/env python

from PIL import Image, ImageEnhance
import os
import subprocess
import glob
import pickle
import math
from Constants import * # Get list of nodes as NODENUMBERS list
from NorthPolarAxes import *

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

locations = {'wrap1': (34.0, 6.0),
             'wrap10': (19.0, 18.5),
             'wrap11': (24.5, 18.0),
             'wrap12': (40.5, 22.25),
             'wrap13': (32.5, 23.5),
             'wrap14': (40.5, 28),
             'wrap15': (19.0, 4.5),
             'wrap16': (17.5, 14.0),
             'wrap17': (13.5, 29.5),
             'wrap18': (39.5, 29.0),
             'wrap19': (27.5, 8.0),
             'wrap2': (23.5, 12.0),
             'wrap20': (19.5, 29.5),
             'wrap21': (19.0, 23.5),
             'wrap22': (34.0, 13.0),
             'wrap24': (12.0, 14.0),
             'wrap3': (41.5, 8.0),
             'wrap4': (28.5, 24.5),
             'wrap5': (28.0, 30.0),
             'wrap6': (46.0, 27.75),
             'wrap7': (14.0, 24.5),
             'wrap8': (37.0, 15.5),
             'wrap9': (36.5, 23.5)}

def main():
    with open("nat2rssi.pkl") as fh:
        NATtoRSSI = pickle.load(fh)

    d = NATtoRSSI
    # for every node, for every power level, present the angles
    for node in ["wrap"+str(i) for i in NODENUMBERS]:
        for txpower in [0, 7, 9, 17, 19]:
            myd = [(i[1], d.get(i)) for i in d if ((node == i[0]) and 
                                                   (txpower == i[2]))]
            myd.sort(lambda x,y: cmp(x[0],y[0]))

            theta = [2*math.pi*i[0]/360. for i in myd]
            r     = [i[1] for i in myd]

            P.clf()
            sub = P.subplot(1,1,1,projection='northpolar')
            P.fill(theta,r,'b',alpha=0.4)
            sub.set_rmax(60)
            sub.set_title("%(node)s receiving with txpower %(txpower)d dBm" % locals())
            #P.show()
            P.savefig(node+",txpower=%(txpower)d.png" % locals())

im = Image.open("seventh-floor-cs-floorplan.png")
for node in ["wrap"+str(i) for i in NODENUMBERS]:
    imwm = Image.open(node+".png")
    size = imwm.size
    newx, newy = [d for d in size]

    oldx, oldy = locations.get(node)
    y = oldy*11.25
    x = oldx*12.5
    y = im.size[1] - y
    box = (x, y, x+newx, y+newy)
    im = watermark(im, imwm.resize([newx,newy]), box)

im.show()
# if __name__=="__main__":
#     main()
