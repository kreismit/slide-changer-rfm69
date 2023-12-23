#!/bin/python3
import RPi.GPIO as gpio
import time

time.sleep(5) # Try to wait until the GPIO and SPI are ready

from RFM69 import Radio, FREQ_915MHZ
'''
	Settings for this RFM69HCW:
	Node ID 2
	Recipient ID is 1 here; will change in different programs
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
me = 2		# for sanity when we send and receive messages
other = 1
countRec=0  # count received messages
countTotal=0 # and all messages
while True:
    ## Set up GPIO ports
    # (runs within the loop so that cleanup() can be called at the end)
    gpio.setmode(gpio.BOARD)
    input1=8
    input2=10
    gpio.setup(input1, gpio.IN)
    gpio.setup(input2, gpio.IN)
    gpio.setwarnings(False)
    # Attempt to access the radio. If SPI isn't found, try again.
    try:
    #    with Radio(FREQ_915MHZ, me, 254, isHighPower=True) as radio:	# Initialize
        with Radio(FREQ_915MHZ, me, 254) as radio:	# Initialize
            print("Initialized RFM69.")
            while True:
                countTotal += 1
                # Syntax is weird here: radio.send is getting called, and the data is
                # two bits: one for the status of input 10 and one for the status of
                # input 38.
                # This function is inside an if statement so that we can track if it
                # was received.
                data1 = not gpio.input(input1)
                data2 = not gpio.input(input2)
                if radio.send(other, [data1,data2]):
                    countRec += 1
                    print("Message {}/{} acknowledged".format(countRec,countTotal))
                else:
                    print("Message was not received.")
                time.sleep(0.1) # and repeat this cycle every 1/10 sec
    except KeyboardInterrupt:
        gpio.cleanup()
        print("\nStopped")
        break
    except FileNotFoundError:
        gpio.cleanup()
        print("\nSPI bus not ready. Restarting.")
        time.sleep(1)
