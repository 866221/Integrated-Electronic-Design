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
        continue_reading = False;
        GPIO.cleanup()

condensed = str(uid[0]) + str(uid[1])  + str(uid[2]) + str(uid[3])

def isAuthentic():
    curs.execute("SELECT * FROM scan WHERE tunique="+condensed)
    if str(curs.fetchone()) != "None":
        return True
    else:
        return False

if isAuthentic():
    print("This card is already in the database")

else:
    first = raw_input('First name: ')
    last = str(raw_input("Last name: "))
    student_id = raw_input("Student ID: ")
    gend = raw_input("Gender (M or F): ")
    #try:
    #print("INSERT INTO scan values(CURRENT_DATE(), NOW(), " + condensed + ", " + student_id + ", " + last_name + ", " + first_name + ", " + gender + ")")
    #curs.execute("INSERT INTO scan values(CURRENT_DATE(), NOW(), " + condensed + ", " + student_id + ", " + last_name + ", " + first_name + ", " + gender + ")")
    get_date = "CURRENT_DATE()"
    get_now = "NOW()"
    curs.execute("INSERT INTO scan values(CURRENT_DATE , NOW(), %s, %s, %s, %s, %s)" , (condensed, student_id, last, first, gend))

    db.commit()
    print("Data committed")


    #except:
        #print("Error: the database is being rolled back")
        #db.rollback()


