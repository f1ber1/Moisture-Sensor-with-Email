import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel =4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)

def callback(channel):
	if GPIO.input(channel):
		print("Water Detected!")
	else:
		print("Water not Detected!")

GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime = 300)
GPIO.add_event_callback(channel,callback)

while True:
	time.sleep(0)
