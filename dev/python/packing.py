#!/usr/bin/python

import termios, sys, os

from struct import *

StartFlag = 0xFC
EndFlag = 0xFD

command = 0x0800

payload = b'\xFF\xFF\xFF\xFF'

packetNum = 1 #TODO: determine packetNum dynamically

#packet = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00') #dummy packet of certain length

headerFormat = Struct('<BBH')
footerFormat = Struct('<HB')
payloadSize = len(payload)

packetSize = headerFormat.size + payloadSize + footerFormat.size

packet = bytearray(packetSize) #create the null packet

headerFormat.pack_into(packet,0,StartFlag,packetNum,command)

print 'packet='+repr(packet)+' of size '+ str(len(packet))

#TODO: pack the request properly with variable payload
packet[headerFormat.size:headerFormat.size+payloadSize] = payload

print 'packet='+repr(packet)

checksum = 0xAAAA
footerFormat.pack_into(packet,headerFormat.size + payloadSize,checksum,EndFlag)
print 'packet='+repr(packet)+' of size '+ str(len(packet))

blah = 0x800
blee = blah - 0x200
print 'blah='+repr(blah)
print 'blee='+repr(blee)
