import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIN_DATA  = 22
PIN_LATCH = 27
PIN_CLOCK = 17
GPIO.setup(PIN_DATA,  GPIO.OUT)
GPIO.setup(PIN_LATCH, GPIO.OUT)
GPIO.setup(PIN_CLOCK, GPIO.OUT)

GPIO.output(PIN_LATCH, GPIO.LOW)
GPIO.output(PIN_CLOCK, GPIO.LOW)

def turnOnPump(byte):
  for bit in range(8): 
    GPIO.output(PIN_DATA, byte & 0x80)
    pulseClock()
    byte = byte << 0x01
  pulseLatch()

def turnOffPumps():
  for bit in range(8): 
    GPIO.output(PIN_DATA, 0)
    pulseClock()
  pulseLatch()

def pulseClock():
  # Pulse the clock pin to register bit
  GPIO.output(PIN_CLOCK, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(PIN_CLOCK, GPIO.LOW)

def pulseLatch():
  # Pulse the latch pin to set byte
  GPIO.output(PIN_LATCH, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(PIN_LATCH, GPIO.LOW)

def destroy(): 
  turnOffPumps()

while True:
  try:
    byte = 1
    for bit in range(4):
      turnOnPump(byte)
      byte = byte << 1
      time.sleep(.5)
    turnOffPumps()
    time.sleep(3)
  except KeyboardInterrupt:
    destroy()