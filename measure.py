#!/usr/bin/env python3

import sys
import time

import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep

# choose pins on rpi (BCM5 and BCM6)
hx = HX711(dout=5, pd_sck=6)
outfile="/dev/shm/scale"

# HOW TO CALCULATE THE REFFERENCE UNIT
#########################################
# To set the reference unit to 1.
# Call get_weight before and after putting 1000g weight on your sensor.
# Divide difference with grams (1000g) and use it as refference unit.

hx.setReferenceUnit(493)
offset=-155 # Instead of taring
jitter=15 # Don't update if new value is within this change
previous=-9999
one_cup=236

hx.reset()

if 1 < len(sys.argv) and 'tare' == sys.argv[1]:
    print("Taring")
    hx.tare()

while True:

    try:
        grams = int("{0: 4.0f}".format(hx.getWeight()+offset))
        cups = int("{0: 4.0f}".format(grams/one_cup))
        if 0 > cups:
            print("Please calibrate scale (%s)" % str(grams))

        print("%s g / %s cups" % (str(grams), str(cups)))
        if grams < previous+jitter and grams > previous-jitter:
            print("Within jitter, not updating")
            previous=grams
        else:
            previous=grams
            with open(outfile, 'w') as f:
                f.write(str(grams))
        sleep(1)

    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        sys.exit()
