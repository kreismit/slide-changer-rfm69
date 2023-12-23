# slide-changer-rfm69
Two-part embedded device which emulates a USB keyboard and remotely presses the right and left arrow keys to change slides. Uses the RFM69 915MHz radio.

Since it emulates a USB device, it works on any operating system.



## Hardware

This has currently been tested only with Raspberry Pi OS Lite (32-bit) on [Raspberry Pi Zero (v1)](https://www.raspberrypi.com/products/raspberry-pi-zero/) boards.
It relies on the [rpi-rfm69 Python library](https://rpi-rfm69.readthedocs.io/en/latest/index.html), which is only compatible with Raspberry Pi boards as of this writing.

It uses two RFM69HCW radios from Adafruit Industries, and they are connected exactly like [this diagram shows](https://rpi-rfm69.readthedocs.io/en/latest/hookup.html#wiring).

Connect two push buttons or keys to the transmitting Pi to [GPIO ports 14 and 15 (pin numbers 8 and 10).](https://pinout.xyz/)
Make sure you use pulldown resistors, or else the pins will tend to change by themselves and you will experience unexpected keypresses!
The button connected to GPIO 14/board pin 8 is the left key, and the button connected to GPIO 15/board pin 10 is the right key. You may want to label or place these accordingly.

## Installation

Load two Raspberry Pis with Raspbian/RasPiOS ([download link](https://www.raspberrypi.com/software/operating-systems/)).
(This code currently does not work with DietPi, and it has not been tested on other operating systems.)

On the transmitting SBC, copy the executables from `rpi0-tx` into the `/usr/local/bin/` directory and make sure they are executable (for example, using `sudo chmod +x /usr/local/bin/*` from the Pi.)

Add the following lines to `/etc/rc.local` or otherwise make them execute at boot:
```
/usr/local/bin/wireless-tx.py
```

On the receiving SBC, copy the executables from `rpi0-rx` into the `/usr/local/bin/` directory and make sure they are executable (for example, using `sudo chmod +x /usr/local/bin/*` from the Pi.)
```
/usr/local/bin/kreismit-usb
/usr/local/bin/wireless-rx.py
```

## Usage

Give power to the sending SBC and it will boot and run everything by itself.

Plug the receiving SBC into a host computer's USB port _through its USB data port_, not the USB power port. If you are using the Raspberry Pi Zero v1, most computers will supply enough power to run the Pi without undervoltage issues. If you are using another board, or if you have performance settings tweaked, your mileage may vary.

After both SBCs have completed their boot process, pressing the buttons connected to the sending SBC will press the left and right keys on the host computer.
The button connected to GPIO 14/board pin 8 is the left key, and the button connected to GPIO 15/board pin 10 is the right key.

## Debugging

The USB serial interface is enabled on the receiving SBC, and it defaults to baud rate 115200 on the Raspberry Pi. If you have issues with the radio, you can kill the program (for example, run `pkill wireless-rx` on the Pi) and then run the command and see its debugging output. The program will print its status and let you know whether it is able to communicate with the other Pi.
