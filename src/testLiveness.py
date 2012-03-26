#!/usr/bin/env python

import os
import threading

NUMTHREADS = 10
NODENUMBERS = range(1,25)
NODESTOEXCLUDE = [13, 17, 22]
# # Remove any disconnectednodes
for node in NODESTOEXCLUDE:
    NODENUMBERS.remove(node)

OKAYNODES = []

class Pingable(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while NODENUMBERS:
            nodeNumber = NODENUMBERS.pop()
            # ret = os.system("ping -c 1 wrap%d.cs.nyu.edu 2>&1 > /dev/null" % nodeNumber)
            # if 0 != ret:
            #     print "Check wrap%d" % nodeNumber
            ret = os.system("ssh wrap%d.cs.nyu.edu echo hi" % nodeNumber)
            print "wrap%d --> %d" % (nodeNumber, ret)

def main():
    for i in range(0,NUMTHREADS):
        t = Pingable()
        t.start()
    print "Done"

if __name__=="__main__":
    main()
