#!/usr/bin/env python
import os
import subprocess
import re

class Packet():
    def __init__(self):
        self.RSSI    = -1
        self.iface   = None
        self.txpower = None
        self.angle   = None

    def process(self, string):
        matches = re.search("antenna 1 (\d+)dB signal.*DA:c0:ff:ee:(\d+):(\d+):(\d+)",string)
        if matches:
            RSSI, iface, txpower, angle = matches.groups()
            self.RSSI    = int(RSSI)
            self.iface   = "ath"+str(int(iface))
            self.txpower = int(txpower, 16)
            self.angle   = int(angle, 16)
        
def nodeFromFilename(dumpfile):
    return dumpfile.rstrip(".dump")

def computeAvgRssi(angle, txpower):
    global NATtoRSSI
    # For every node calculate the average RSSI and store (note this is related to the angle of the transmitter)
    dumpfiles = [logfile for logfile in os.listdir('.') if ".dump" in logfile]
    for dumpfile in dumpfiles:
        p = subprocess.Popen("tcpdump -r %(dumpfile)s -nevvv 2>/dev/null" % locals(),
                             shell=True,
                             stdout=subprocess.PIPE)
        ath0RSSIs = [] 
        ath1RSSIs = []
        for l in p.stdout.readlines():
            pkt = Packet()
            pkt.process(l)
            if "ath0" == pkt.iface:
                ath0RSSIs.append(pkt.RSSI)
            elif "ath1" == pkt.iface:
                ath1RSSIs.append(pkt.RSSI)

        # print "%s\t%.1f\t%.1f" % (nodeFromFilename(dumpfile), 
        #                           sum(ath0RSSIs)/float(len(ath0RSSIs)) if ath0RSSIs else 0,
        #                           sum(ath1RSSIs)/float(len(ath1RSSIs)) if ath1RSSIs else 0)

        NATtoRSSI[(nodeFromFilename(dumpfile), angle, txpower)] = sum(ath0RSSIs)/float(len(ath0RSSIs)) if ath0RSSIs else 0
        NATtoRSSI[(nodeFromFilename(dumpfile), angle+180, txpower)] = sum(ath1RSSIs)/float(len(ath1RSSIs)) if ath1RSSIs else 0
        
def main():
    # parameters
    channel = 11
    length  = 1400
    numpkts = 500

    # dictionary of relevant info
    global NATtoRSSI
    NATtoRSSI = dict()

    for angle in xrange(0,180,10):
        for txpower in [0, 7, 9, 17, 19]: #11, 13, 15 seem to be broken
            destination_directory = "angle=%(angle)d,txpower=%(txpower)d,numpkts=%(numpkts)d" % locals()
            print destination_directory
            oldpwd = os.getcwd()
            os.chdir(destination_directory)
            computeAvgRssi(angle, txpower)
            os.chdir(oldpwd)

    # myd = [(i[1], d.get(i)) for i in d if (('wrap9' == i[0]) and (9 == i[2]))]

    import pickle
    with open("nat2rssi.pkl","w") as fh:
        pickle.dump(NATtoRSSI,fh)
            
if __name__=="__main__":
    main()


def foo():
    import NorthPolarAxes
    import matplotlib
    import numpy as np
    from matplotlib.pyplot import figure, show, rc, grid

    # radar green, solid grid lines
    rc('grid', color='#316931', linewidth=1, linestyle='-')
    rc('xtick', labelsize=15)
    rc('ytick', labelsize=15)

    # force square figure and square axes looks better for polar, IMO
    width, height = matplotlib.rcParams['figure.figsize']
    size = min(width, height)
    # make a square figure
    fig = figure(figsize=(size, size))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, axisbg='#d5de9c')
    myd = [(0, 22.67157894736842),
           (10, 23.756578947368421),
           (20, 23.092039800995025),
           (30, 24.081081081081081),
           (40, 20.427450980392155),
           (50, 17.668831168831169),
           (60, 18.326599326599325),
           (70, 17.487864077669904),
           (80, 11.759776536312849),
           (90, 15.906474820143885),
           (100, 10.76),
           (180, 22.90295358649789),
           (190, 15.840220385674931),
           (200, 23.93734939759036),
           (210, 22.654794520547945),
           (220, 19.866220735785951),
           (230, 22.635730858468676),
           (240, 12.791428571428572),
           (250, 22.978401727861772),
           (260, 24.961290322580645),
           (270, 25.101052631578948),
           (280, 20.38372093023256)]
    # import collections
    # mydeq = collections.deque(myd)
    # mydeq.rotate(-9)
    # myd = list(mydeq)
    
    import math
    theta = [2*math.pi*i[0]/360. for i in myd]
    r     = [i[1] for i in myd]
    
    ax.subplot(1,1,1,projection='northpolar')
    ax.plot(theta, r, color='#ee8d18', lw=3)
    ax.set_rmax(30)
    grid(True)

    #ax.set_title("And there was much rejoicing!", fontsize=20)
    show()
