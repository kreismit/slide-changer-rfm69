#!/bin/python3

# Program to send keypresses in response to wireless events.
NULL_CHAR = chr(0)

def write_keypress(report):
    with open('/dev/hidg0', 'rb+') as fd:
        # First, encode and write the first argument:
        fd.write(report.encode())
        # Then, write 8 null characters to clear all keypresses:
        report=NULL_CHAR*8
        fd.write(report.encode())

from RFM69 import Radio, FREQ_915MHZ
from time import sleep
#import RPi.GPIO as gpio

'''
        Settings for this RFM69HCW:
        Node ID 1
        Recipient ID is 2 here; will change in different programs
        Network ID = 254
        Syntax: Radio(freq, node, network)

        Keyword args (must explicitly assign):
        isHighPower (bool)
        power (int)
        verbose (bool)
        encryptionKey (str)
        promiscuousMode (bool)
        spiBus (int)
        spiDevice (int)
        interruptPin (int)
        resetPin (int)
'''
me = 1      # for sanity when we send and receive messages
other = 2

right_keypress=False # keep track of when keys have already been pressed, so
left_keypress=False  # that a single button-push isn't looped

while True:
    try:
        with Radio(FREQ_915MHZ, me, 254, autoAcknowledge=True) as radio:
            print("Initialized RFM69.")
            while True:
                # Listen for incoming packets
                #print("Listening...")
                # Loop through every received packet
                for packet in radio.get_packets():
                    # note that right keypress overrides left keypress
                    if packet.data[0] and not right_keypress:
                        # Send RightArrow
                        write_keypress(NULL_CHAR*2+chr(0x4f)+NULL_CHAR*5)
                        right_keypress=True
                        left_keypress=False
                        # if right_keypress is already set, do nothing
                    elif packet.data[1] and not left_keypress:
                        # Send LeftArrow
                        write_keypress(NULL_CHAR*2+chr(0x50)+NULL_CHAR*5)
                        right_keypress=False
                        left_keypress=True
                        # if left_keypress is already set, do nothing
                    elif not packet.data[0] and not packet.data[1]:
                        # if nothing is pressed, clear the Boolean vars
                        right_keypress=False
                        left_keypress=False
                    print("{} and {}".format(packet.data[0],packet.data[1]))
    except KeyboardInterrupt:
        print("\nStopped")
        break
    except FileNotFoundError:
        print("\nSPI bus not ready. Restarting.")
        sleep(1)
