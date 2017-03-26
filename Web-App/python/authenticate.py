#!/usr/bin/env python

import MySQLdb
import RPi.GPIO as GPIO
import MFRC522
import signal
import time

pin = 11
on = 1
off = 0

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

def isAuthentic():
    result = str(uid[0])  + str(uid[1])  + str(uid[2]) + str(uid[3])
    curs.execute("SELECT * FROM scan WHERE tunique="+result)
    current_user = str(curs.fetchone())

    if current_user != "None":
        curs.execute("SELECT * FROM scan WHERE tunique=" + result)
        for row in curs.fetchall():
            get_date = "CURRENT_DATE()"
            get_now = "NOW()"
            condensed = str(row[2])
            student_id = str(row[3])
            last = str(row[4])
            first = str(row[5])
            gend = str(row[6])
            print(str(row[2]) + "     " + str(row[3]) + "     " + str(row[4]) + "     " + str(row[5]) + "     " + str(row[6]))
            curs.execute("INSERT INTO history values(CURRENT_DATE , NOW(), %s, %s, %s, %s, %s)" , (condensed, student_id, last, first, gend))
            db.commit()
            print("Data committed")
        return True
    else:
        curs.execute("INSERT INTO history values(CURRENT_DATE , NOW(), %s, %s, %s, %s, %s)", (result, -1, "null", "null", "null"))
        db.commit()
        print("Data committed")
        return False

while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    #if status == MIFAREReader.MI_OK:
        # print "Card detected"
    #    GPIO.output(pin, 1)
    #elif status != MIFAREReader.MI_OK:
    #    GPIO.output(pin, 0)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
        if isAuthentic():
            GPIO.output(pin, on)
            print("The door is unlocked")
            time.sleep(5)
            GPIO.output(pin, off)
            print("The door is locked")

        else:
            GPIO.output(pin, off)
            print("Unauthentic, door locked")
            time.sleep(5)











