from scapy.all import *
import logging  
import logging.handlers
from tkinter import *                       

root=Tk()
ap_list = []

def PacketHandler(packet) :
    print(packet.show())

sniff(iface="Wireless Network Connection", prn = PacketHandler, count=100, timeout=10)
    #==============================INITIALIATION==================================
if __name__ == '__main__':
    root.mainloop()
