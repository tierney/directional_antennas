#!/usr/bin/env python

import os

def main():
    channel = 11
    length  = 1400
    numpkts = 500
    # for every angle, for every transmit power
    for angle in xrange(0,180,10):
        for txpower in [0, 7, 9, 11, 13, 15, 17, 19]:
            # set the angle on the rotating node (wire92)
            os.system("ssh root@wire92.cs.nyu.edu pololu/mmaestro.py %(angle)d" 
                      % locals())

            # set the transmit power on the tranmitters ifaces (wrap23)
            os.system("ssh root@wrap23.cs.nyu.edu \"iwconfig ath0 txpower %(txpower)d "\
                          "&& iwconfig ath1 txpower %(txpower)d\"" % locals())

            # start start the collectors (./startexp)
            os.system("./startExperiment.py")

            # transmit packets (wrap23)
            os.system("ssh root@wrap23.cs.nyu.edu ./tx.py "\
                          "%(channel)d %(txpower)d %(angle)d %(length)d %(numpkts)d" % locals())

            # stop collectors (./stopexp)
            os.system("./stopExperiment.py")
    
            # collect the traces (./fetch) --> Assuming the traces are named wrapNN.dump
            os.system("./fetchResultsExperiment.py")

            # move traces into appropriately labeled directory
            destination_directory = "angle=%(angle)d,txpower=%(txpower)d,numpkts=%(numpkts)d" % locals()
            os.mkdir(destination_directory)
            os.system("mv *.dump %(destination_directory)s" % locals())

if __name__=="__main__":
    main()


