#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import RPi.GPIO as GPIO
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

#gpio relay pin
relayPin=16
#gpio sharp pin
sharpPin=18

#rpi gpio init
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(relayPin, GPIO.OUT)
GPIO.setup(sharpPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#functions
def openDoor(pin):
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    return

## Search for a finger
##
## Tries to initialize the sensor
def initFinger():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            openDoor(relayPin) 
            print('The accuracy score is: ' + str(accuracyScore))

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

    finally:
            GPIO.cleanup() # this ensures a clean exit

GPIO.cleanup() # this ensures a clean exit


#main code starts here
try:
    while True:
        enable=GPIO.input(sharpPin)
        if enable==0:
            initFinger()

except:
    print("exception occured")

finally:
    GPIO.cleanup()