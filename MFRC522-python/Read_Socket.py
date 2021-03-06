#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

continue_reading = True
pin = 11

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    #print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def start():
	pin = 11

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)

	continue_reading = True
	GPIO.output(pin,1)
	time.sleep(0.5)
	GPIO.output(pin,0)

	signal.signal(signal.SIGINT, end_read)

# Capture SIGINT for cleanup when the script is aborted
#def end_read(signal,frame):
#    global continue_reading
#   #print "Ctrl+C captured, ending read."
#   continue_reading = False
#    GPIO.cleanup()

# Hook the SIGINT
#signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
def Read():
	while continue_reading:
    
    		# Scan for cards    
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    		# If a card is found
    		if status == MIFAREReader.MI_OK:
        		#print "Card detected"
            		GPIO.output(pin,1)
    		elif status != MIFAREReader.MI_OK:
            		GPIO.output(pin,0)
    
   
    		# Get the UID of the card
    		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    		# If we have the UID, continue
    		if status == MIFAREReader.MI_OK:

        		# Print UID
        		result = (str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    
        		# This is the default key for authentication
        		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
       			# Select the scanned tag
        		MIFAREReader.MFRC522_SelectTag(uid)

        		# Authenticate
        		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        		# Check if authenticated
        		if status == MIFAREReader.MI_OK:
            			MIFAREReader.MFRC522_Read(8)
            			MIFAREReader.MFRC522_StopCrypto1()
        		else:
            			result = ("Authentication error")

        		time.sleep(5)
			continue_reading = False;
			return result



