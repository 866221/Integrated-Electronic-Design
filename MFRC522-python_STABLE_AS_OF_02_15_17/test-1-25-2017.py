import RPi.GPIO as GPIO
import MFRC522
import signal
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.OUT)

while true:
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        GPIO.output(17, 1)
    else:
        GPIO.output(17, 0)


        
