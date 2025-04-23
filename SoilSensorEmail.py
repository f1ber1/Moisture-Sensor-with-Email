import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT= 456
EMAIL_USER='3413542199@qq.com'
EMAIL_PASSWORD = 'lurtbvjlpgzgdacb'
RECIPENT_EMAIL = '976559217@qq.com'
DAILY_CHECK_TIMES = ["07:00", "9:00", "11:00", "13:00"]
channel = 4
last_check_time = None

def send_email(status):
	msg = EmailMessage()
	email_content = f"PLANT STATUS UPDATE:- Condition: {status}- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
	msg['Subject']= 'Plant message'
	msg['From']= EMAIL_USER
	msg['To'] =RECIPENT_EMAIL
	msg.set_content(email_content)
	try:
		server = smtplib.SMTP('smtp.qq.com',587)
		server.starttls()
		server.login(EMAIL_USER,EMAIL_PASSWORD)
		server.send_message(msg)
		print('send successful')
	except Exception as e:
		print(f'send erorr:{e}')

def check_moisture():
	if GPIO.input(channel):
		return "Soil is DRY - Water NEEDED"
	return "Soil is WET - No water needed"

def should_check_now():
	current_time = datetime.now().strftime("%H:%M")
	return current_time in DAILY_CHECK_TIMES

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
GPIO.add_event_detect(channel,GPIO.BOTH,bouncetime = 300)

try:
	print('program is running')
	while True:
		current_time = datetime.now().strftime("%H:%M")
		if should_check_now() and current_time != last_check_time:
			status = check_moisture()
			send_email(status)
			last_check_time = current_time
		
		
		time.sleep(30)
except KeyboardInterrupt:
	GPIO.cleanup()
