#!/usr/bin/env python

import array
from scapy.all import sendp,Dot11,LLC,SNAP
import sys

HEADERSIZE=12

def sendPackets(iface,   # expect: string meaning athX
                channel, # expect: int meaning channel number (not Hz)
                power,   # expect: int meaning dBm
                angle,   # expect: int meaning degrees
                length, 
                numPkts):

    # Extract iface number
    ifaceNum = int(iface[-1])

    # Convert length into packet contents
    rawdata = array.array('B',
                          [1 for x in range(0,length-HEADERSIZE)]).tostring()
    
    # numPkts manipulation to account for scapy bug
    assert(numPkts > 0)
    numPkts = -numPkts # scapy bug(?) requiring negative number

    sendp(Dot11(type="Data",FCfield="to-DS",
                addr1="ff:ff:ff:ff:ff:ff",
                addr2="06:0b:6b:c0:ff:ee",
                addr3="c0:ff:ee:%02x:%02x:%02x" % (ifaceNum, power, angle))/
          LLC(ctrl=3)/SNAP()/rawdata,
          iface=iface,
          loop=numPkts)    

def main():
    if len(sys.argv) != 6:
        print "%s channel power angle length numpkts" % sys.argv[0]
        sys.exit(1)
        
    channel = int(sys.argv[1])
    power   = int(sys.argv[2])
    angle   = int(sys.argv[3])
    length  = int(sys.argv[4])
    numPkts = int(sys.argv[5])

    sendPackets('ath0',channel,power,angle,length,numPkts)

    sendPackets('ath1',channel,power,angle,length,numPkts)

if __name__=="__main__":
    main()

#EOF
