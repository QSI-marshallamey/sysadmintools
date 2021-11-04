#!/usr/bin/env python3
# Plant Watering Program
import RPi.GPIO as GPIO
import datetime
from time import sleep

# Set variables
RUNNING = True
OFF     = 1
ON      = 0

# Setup outlets
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT, initial=OFF)
GPIO.setup(3, GPIO.OUT, initial=OFF)
GPIO.setup(4, GPIO.OUT, initial=OFF)
GPIO.setup(5, GPIO.OUT, initial=OFF)
GPIO.setup(6, GPIO.OUT, initial=OFF)
GPIO.setup(7, GPIO.OUT, initial=OFF)
GPIO.setup(8, GPIO.OUT, initial=OFF)
GPIO.setup(9, GPIO.OUT, initial=OFF)

# Start loop
while RUNNING:
    
    # Check the current time
    sleep(1)
    CURRENT_TIME = datetime.datetime.now()
    print("The current time is", CURRENT_TIME)
    
#    #Plant 1: Bryce
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 10:
#        GPIO.output(2, ON)
#        sleep(90)
#        GPIO.output(2, OFF)
#        
#    #Plant 2: India
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 12:
#        GPIO.output(3, ON)
#        sleep(90)
#        GPIO.output(3, OFF)
#        
#    #Plant 3: Maurice
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 14:
#        GPIO.output(4, ON)
#        sleep(90)
#        GPIO.output(4, OFF)
#        
#    #Plant 4: Indoor Kids
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 16:
#        GPIO.output(5, ON)
#        sleep(240)
#        GPIO.output(5, OFF)
#
#    #Plant 5: Bonsai
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 21:
#        GPIO.output(6, ON)
#        sleep(90)
#        GPIO.output(6, OFF)
#        
#    #Plant 6: Vagina Jenkins
#    if CURRENT_TIME.hour == 16 and CURRENT_TIME.minute == 23:
#        GPIO.output(7, ON)
#        sleep(240)
#        GPIO.output(7, OFF)
#        
#    #Plant 7: Herb Garden
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 28:
#        GPIO.output(8, ON)
#        sleep(240)
#        GPIO.output(8, OFF)
#        
#    #Plant 8: Nasturtium
#    if CURRENT_TIME.hour == 7 and CURRENT_TIME.minute == 33:
#        GPIO.output(9, ON)
#        sleep(240)
#        GPIO.output(9, OFF)
#        
    for i in range(2,10):
        GPIO.output(i, ON)
        print(i-1, 'is ON')
        sleep(3)
#        input()
        GPIO.output(i, OFF)
        print(i-1, 'is OFF')
#        input()
        sleep(1)
    