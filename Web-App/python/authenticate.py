#!/usr/bin/env python

import MySQLdb
import RPi.GPIO as GPIO
import MFRC522
import signal
import time

pin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

db = MySQLdb.connect("localhost", "ied", "IEDpassword", "ids")
curs = db.cursor()
uid = []

while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        # print "Card detected"
        GPIO.output(pin, 1)
    elif status != MIFAREReader.MI_OK:
        GPIO.output(pin, 0)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
        continue_reading = False
        GPIO.cleanup()



def isAuthentic():
    result = str(uid[0])  + str(uid[1])  + str(uid[2]) + str(uid[3])
    curs.execute("SELECT * FROM scan WHERE tunique="+result)
    if len(curs.fetchall()) > 0:
        return True
    else:
        return False

if isAuthentic:
    GPIO.output(pin, 1)
else:
    GPIO.output(pin, 0)


