#!/usr/bin/env python

from PIL import Image, ImageEnhance
import os
import subprocess
import glob

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


DPOSITION = { '1' : [950, 570],
              '2' : [510, 450],
              '3' : [210, 210],
              '4' : [1170,-10],
              '5' : [850, 475],
              }

positionFiles = [f.strip() for f in subprocess.Popen("ls | grep Position", shell=True, stdout=subprocess.PIPE).stdout.readlines()]
print positionFiles

livenodes = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 20, 21, 24]

print livenodes
for n in livenodes:
    im = Image.open("wrapnodes.png")
    for f in positionFiles:
        pngs = glob.glob(f+"/rotating-directionals/*RSSI.wrap"+str(n)+".png")
        for p in pngs:
            psplit   = p.split('/')
            position = psplit[0].split()[2]
            posAdj   = DPOSITION.get(position)
            rssi     = Image.open(p)
            rs       = rssi.size
            newrs    = [x / 2 for x in rssi.size]
            box      = (posAdj[0],posAdj[1],posAdj[0]+newrs[0],posAdj[1]+newrs[1])
            im       = watermark(im, rssi.rotate(180).resize(newrs), box, 0.6)

    im.save("seventh-floor-wrap"+str(n)+".png","PNG")
    print "Saved wrap"+str(n)
