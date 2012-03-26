#!/usr/bin/env python

import os
import sys
import threading
import time
from Constants import *

class Pingable(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while NODENUMBERS:
            nodeNumber = NODENUMBERS.pop()
            os.system("scp wrap%d.cs.nyu.edu:wrap%d.dump ." % (nodeNumber, nodeNumber))
            os.system("ssh wrap%d.cs.nyu.edu rm -f wrap%d.dump" % (nodeNumber, nodeNumber))
            OKAYNODES.append(nodeNumber)
def main():
    for i in range(0,NUMTHREADS):
        t = Pingable()
        t.start()
    print "Processing",
    while len(OKAYNODES) < len(NODENUMBERS):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    print "\nDone."

if __name__=="__main__":
    main()

