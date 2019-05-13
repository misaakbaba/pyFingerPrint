import RPi.GPIO as GPIO

# here you would put all your code for setting up GPIO,
# we'll cover that tomorrow
# initial values of variables etc...

#gpio relay pin
pin=11

#rpi gpio init
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(pin, GPIO.OUT)

def openDoor(pin):
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    return

try:
    # here you put your main loop or block of code
    openDoor(pin)

except KeyboardInterrupt:
    # here you put any code you want to run before the program 
    # exits when you press CTRL+C
except:
    # this catches ALL other exceptions including errors.
    # You won't get any error messages for debugging
    # so only use it once your code is working
    print "Other error or exception occurred!"

finally:
    GPIO.cleanup() # this ensures a clean exit

