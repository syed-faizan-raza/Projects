import RPi.GPIO as GPIO # for RPi's GPIO interaction
import time # for sleep function
import LCD1602 as lcd # for lcd functions
import keypadfunc as keypad # for keypad functions
import serial # for LCD and ADC
import DHT11 # for temperature and humidity sensor
import PCF8591 as ADC # for ADC chip readings/writings
import requests # for making requests to thingspeak api
import signal # for catching keyboard interrupts
import sys # for exiting program
import webbrowser # for opening flask server on startup
from flask import Flask # for flask server
from flask import send_file # to send image/video to user
from flask import render_template # to render the index page
from datetime import datetime # for time in iso format
from picamera import PiCamera # for camera module
from threading import Thread # for running tasks on different threads
''' Constants '''
PASSWORD = '$9' # password for the keypad and flask open
RFID_VALID = '5300C82FB3' # square card for valid entry
SERIAL_PORT = '/dev/ttyS0' # for UART
API_KEY = 'DR68KU7GU95C7WLO' # write api key for thing speak
CHANNEL_ID = '2212739' # thing speak channel id
OUTSIDE_LIGHT = 12 # blue LED for welcome light
DOOR = 16 # yellow LED which acts like a door
SHIFT_KEY = 6 # the button that can be used as a shift key for
password entering
BELL = 27 # the buzzer that acts as a bell
TRIG = 5 # Ultra sonic trigger
ECHO = 4 # ultra sonic echo
PIR = 18 # motion sensor
DHT_SENSOR = 17 # temperature and humidity sensor
RFID_EN = 14 # RFID enable pin
AFTER_MOTION_TIME = 30 # number of seconds to run peripheral after motion
is detected
MAX_ALLOWED_DISTANCE = 30 # maximum distance in cm that is allowed to be
detected by the ultra sonic sensor
PHOTO_PATH = '/home/pi/Desktop/outside_image.jpeg' # path to save image of
preview
VIDEO_PATH = '/home/pi/Desktop/outside_video.h264' # path to save video of
preview
''' Global Variables '''
door_open = False # to store whether door is open or
closed
door_last_open = None # to store the last time the door was opened
house_entered = False # to know if house is entered to close buzzer checks,
keypad and rfid
''' Initial Setup '''
GPIO.setwarnings(False) # remove warnings
GPIO.setmode(GPIO.BCM) # use BCM mode
GPIO.setup(SHIFT_KEY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # make GPIO 4
switch button input
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_UP) # make motion
sensor input
GPIO.setup(ECHO, GPIO.IN) # make ultra sonic echo input
GPIO.setup(BELL, GPIO.OUT) # make bell GPIO output
GPIO.setup(TRIG, GPIO.OUT) # make ultra sonic sensor trigger output
GPIO.setup(OUTSIDE_LIGHT, GPIO.OUT) # make outside light output
GPIO.setup(RFID_EN, GPIO.OUT) # make RFID enable pin output
GPIO.output(RFID_EN, GPIO.HIGH) # disable RFID
GPIO.setup(DOOR, GPIO.OUT) # make door output
GPIO.output(DOOR, GPIO.LOW) # ensure door is closed
bell_buzzer = GPIO.PWM(BELL, 500) # setup buzzer pwm with frequency 500
bell_buzzer.start(0) # default to 0% duty cycle so no sound is
made
lcd.init(0x27, 1) # initailize lcd with bus address 0x27 and turn on back
light
ADC.setup(0x48) # the ADC bus address
home_server = Flask(__name__) # Create a flask object called home server
camera = PiCamera() # create camera object
camera.resolution=(1280,720) # set resolution to 720p
# setup uart for RFID
ser = serial.Serial(baudrate = 2400,\
bytesize = serial.EIGHTBITS,\
parity = serial.PARITY_NONE,\
port = SERIAL_PORT,\
stopbits = serial.STOPBITS_ONE,\
timeout = 1) # 1 second time out
''' Handle closing the system'''
# function to close all peripherals
def close_nicely(signum, frame):
print("Closing system") # print closing message
bell_buzzer.stop() # Turn off bell
GPIO.remove_event_detect(PIR) # Turn off motion sensor
GPIO.output(RFID_EN, GPIO.HIGH) # shut off RFID
GPIO.output(OUTSIDE_LIGHT, GPIO.LOW) # shut off outside light
GPIO.output(DOOR, GPIO.LOW) # shut off door light
lcd.init(0x27, 0) # turn off LCD backlight
lcd.clear() # clear lcd text
camera.close() # close camera
sys.exit(1) # close the program
signal.signal(signal.SIGINT, close_nicely) # on press of ctrl + c
signal.signal(signal.SIGTERM, close_nicely) # on terminate of program
'''Reading/Writing to GPIOs and peripherals'''
# function to ring the bell
def ring_bell():
print("Ringing bell") # print to console
bell_buzzer.ChangeDutyCycle(50) # set duty cycle to 50% to start the noise
time.sleep(2) # ring bell for 2 seconds
bell_buzzer.ChangeDutyCycle(0) # set duty cycle to 0% to stop the noise
# change the status of the door based on the boolean new_door_status
def change_door_status(new_door_status):
global door_open, door_last_open # get access to global variables
if new_door_status == door_open: # no need to change status is its alredy
the correct state
return
GPIO.output(DOOR, GPIO.HIGH if new_door_status else GPIO.LOW) # change
status of LED to mock open/close door
door_open = new_door_status # st status in global variable for future use
if new_door_status: # if door is opened, save the last time it was
opened for flask route
door_last_open = time.ctime()
# function to open the door temporarily for for 5 seconds
def open_door_temp():
global house_entered # get access to global variable
house_entered = True # set house entered to true to close
buzzer checks, keypad and rfid
print('Access granted') # print to console
change_door_status(True) # open door
time.sleep(5) # keep door open for 5 seconds
change_door_status(False) # close door
GPIO.output(OUTSIDE_LIGHT, GPIO.LOW) # turn off outside light
# function to read bus speed from AIN1 of ADC chip
def read_light_intensity():
intensity_units = ADC.read(1) # read ADC channel 1
intensity_percentage = intensity_units/256 * 100 # convert the intensity
to a percentage
return (intensity_units, intensity_percentage) # return values to
caller
# function to read temperature and humidity from dht11
def read_dht():
dht_result = False # set dht result to show its
unknown
while not dht_result: # keep trying until dht is
read
dht_result = DHT11.readDht11(DHT_SENSOR) # read dht sensor
time.sleep(0.25) # to prevent overloading the
sensor
return dht_result # return the dht reading to
the caller
# function to read distance from ultra sonic sensor
def distance():
GPIO.output(TRIG, GPIO.LOW) # starting the process
time.sleep(0.000002) # from specifications
GPIO.output(TRIG, 1) # turn it on for 10 us
time.sleep(0.00001)
GPIO.output(TRIG, 0) # stop trigger
while GPIO.input(ECHO) == 0:# wait for echo to become high
pass
time1 = time.time() # get T1
while GPIO.input(ECHO) == 1:# wait for echo to return (become low again)
pass
time2 = time.time() # get T2
duration = time2 - time1 # get duration
return duration*1000000/58 # calculate distance by sound speed (340 m/s)
in cm
# validate if the rfid is valid
def validate_rfid(code):
s = code.decode("ascii") # convert it to ascii
# check if the code is valid by checking its length and start and stop
bits
if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
return s[1:-1] # remove start and stop bit and return the code
else:
return False # return false if code is invalid
# function to read rfid and open door if its valid
def rfid_read():
start_time = time.time() # get the start time to know when to stop
GPIO.output(RFID_EN, GPIO.LOW) # enable RFID
print("Accepting RFID") # print to console
# loop until time is up or house is entered
while time.time() - start_time < AFTER_MOTION_TIME and not house_entered:
ser.flushInput()GPIO.output(RFID_EN, GPIO.HIGH)GPIO.output(RFID_EN,
GPIO.HIGH) # clear input
ser.flushOutput() # clear output
data = ser.read(12) # read 12 bits from uart
code = validate_rfid(data) # check if its valid code
if code == RFID_VALID: # if code is valid
print("Correct RFID") # print to console that its valid
open_door_temp() # open door temporarily
else:
if code != False: # if read is valid rfid tag but not
correct
print("Incorrect RFID") # print to console that its invalid
time.sleep(1) # wait for 1 second to prevent
overloading the uart
GPIO.output(RFID_EN,GPIO.output(RFID_EN, GPIO.HIGH) GPIO.HIGH) # shut
off RFID
# function to read keypad and open door if correct password is entered
def keypad_read():
start_time = time.time() # get the start time to know when to stop
# loop until time is up or house is entered
while time.time() - start_time < AFTER_MOTION_TIME and not
house_entered:
lcd.write(0, 0, 'Input Password: ') # prompt password
password = keypad.get_password(SHIFT_KEY) # get 2 digit password from
user
if password != PASSWORD: # if wrong password
print("Incorrect password. Try again") # print to console that its
wrong
lcd.write(0, 0, 'Incorrect!! ') # show incorrect on LCD
time.sleep(0.5) # show incorrect for 500 ms
else:
print("Correct password.") # print to console that its
correct
lcd.write(0, 0, 'Success!! ') # show success
lcd.write(0, 1, ' ') # remove password
open_door_temp() # open door temporarily
# function to run the outside peripherals when motion is detected
def motion_detector():
global house_entered # get access to global variable
print('starting motion') # print to console that motion is detected
lcd.init(0x27, 1) # turn on LCD
house_entered = False # set house entered to false which is used for
buzzer checks, keypad and rfid
time_waited = 0 # create a variable to keep track of time
waited so its always consistent
# local function to wait for a certain amount of time
def wait(wait_time):
nonlocal time_waited # get access to time_waited variable of the
parent function
time.sleep(wait_time) # wait for wait_time seconds
time_waited += wait_time # add wait_time seconds to time waited
GPIO.output(OUTSIDE_LIGHT, GPIO.HIGH) # turn on outside light
Thread(target=rfid_read).start() # start rfid thread for rfid reads
Thread(target=keypad_read).start() # start keypad thread for keypad
reads
# loop until time is up
while time_waited <= AFTER_MOTION_TIME:
wait(5) # wait for 5 seconds
if house_entered: # quit loop if house is entered
break
dist = distance() # get distance from ultra sonic sensor. This shows
how far the person is from the door
allowed_distance = (ADC.read(0) / 256) * MAX_ALLOWED_DISTANCE #
calculate the allowed distance based on the ADC potentiometer
print("Distance is {} cm".format(dist)) # print distance to console
if dist <= allowed_distance: # if distance is less than
allowed distance
print("Ringing bell") # print to console that bell is
ringing
Thread(target=ring_bell).start() # start bell thread to ring the
bell
print("Capturing preview") # print to console that preview
is being captured
camera.capture(PHOTO_PATH) # take a photo
camera.start_recording(VIDEO_PATH) # start recording video
wait(5) # record for 5 seconds
camera.stop_recording() # stop recording video
break # break out of loop
# wait for the rest of the time if breaked out of above loop early
while time_waited <= AFTER_MOTION_TIME:
wait(5)
GPIO.output(OUTSIDE_LIGHT, GPIO.LOW) # turn off outside light
lcd.init(0x27, 0) # turn off LCD
lcd.clear() # turn off LCD
'''Thing speak functions'''
# function to send get data from thing speak. The field_id is the field number
on thing speak channe;
def get_values_from_cloud(field_id):
# get the last 10 values from the field as json
result =
requests.get("https://api.thingspeak.com/channels/{}/fields/{}.json?results=10
".format(CHANNEL_ID, field_id))
old_values = [] # create a list to store
the values
for feed in result.json()['feeds']: # get the array of json
objects which hold the values
old_value = feed['field{}'.format(field_id)] # get the value from the
field
if old_value != None: # if the value is not
null
old_values.append(int(old_value)) # add the value to the
list
return old_values # return the list of
values
''' flask server '''
# function for default route
@home_server.route('/')
def index():
return render_template('index.html')
# function for static door status route
@home_server.route('/door_status')
def door_status():
# if door has never been opened don't show last open time
if door_last_open == None:
return "Door is closed"
# if door is open show when it was opened
if door_open:
return "Door was opened at {}".format(door_last_open)
# if door is closed show when it was last opened
else:
return "Door is closed. It was last opened at
{}".format(door_last_open)
# function for static light intensity route
@home_server.route('/light_intensity')
def light_intensity():
intensity_units, intensity = read_light_intensity() # get light intensity
from ADC
print("Light intensity is: {}%".format(intensity)) # print to console
return "Light intensity is: {}%".format(intensity) # return light
intensity to show on webpage
# function for previewing the last photo or video. The route is dynamic and
can be either I for image or V for video
@home_server.route('/preview/<output_type>')
def preview(output_type):
if output_type.upper() == "I": # if image is requested
return send_file(PHOTO_PATH, mimetype="image/jpeg") # show the photo
on the webpage
elif output_type.upper() == "V": # if video is requested
return send_file(VIDEO_PATH, mimetype="video/h264",
as_attachment=True, attachment_filename="preview.h264") # download the video
with the name preview.h264
else:
return "Invalid Link!" # if invalid link dynamic route is
requested
# function for opening or closing the door. The route is dynamic and can be
either OPEN or CLOSE. Password is required to prevent unauthorized access
@home_server.route('/door/<password>/<status>')
def door(password, status):
if password != PASSWORD: # check if password is incorrect
return "Incorrect password" # return incorrect password message and
don't change door status
if status.upper() == "OPEN": # if open is requested
change_door_status(True) # open the door
return "Door was sucessfully opened at {}".format(time.ctime()) #
return success message with time
elif status.upper() == "CLOSE": # if close is requested
change_door_status(False) # close the door
return "Door was sucessfully closed at {}".format(time.ctime()) #
return success message with time
else:
return "Invalid Link!" # if invalid link dynamic route is
requested
'''Starting the program'''
humidity, temp = read_dht() # read humidity and
temperature from DHT sensor
lcd.write(0,0,"humidity: {}%".format(humidity)) # show humidity on LCD line 1
lcd.write(0,1,"Temperature: {}C".format(temp)) # show temperature on LCD line
2
print("Current humidity: {}%, temperature: {}°C".format(humidity, temp)) #
print humidity and temperature to console
requests.get("https://api.thingspeak.com/update?api_key={}&field2={}&field3={}
".format(API_KEY, humidity, temp))
time.sleep(2) # show message on LCD for 2
seconds
lcd.init(0x27, 0) # turn off LCD
lcd.clear() # turn off LCD
old_humidity_values = get_values_from_cloud(2) # get old humidity values from
thing speak
old_temp_values = get_values_from_cloud(3) # get old temperature values
from thing speak
avg_humidity =
int(sum(old_humidity_values)/len(old_humidity_values)) # calculate
average humidity from old values
avg_temp =
int(sum(old_temp_values)/len(old_temp_values)) #
calculate average temperature from old values
print("Average humidity: {}%, tempreature {}°C".format(avg_humidity,
avg_temp)) # print average humidity and temperature to console
_ ,previous_light_intensity_percent = read_light_intensity() # get initial
value of light intensity from ADC
# start flask server in a new thread on port 5000
Thread(target=home_server.run).start()
webbrowser.open("http://0.0.0.0:5000")
# start motion detector
GPIO.add_event_detect(PIR,
GPIO.FALLING,
callback=lambda self:
Thread(target=motion_detector).start(),
bouncetime=AFTER_MOTION_TIME*2*1000)
# inifinite loop
while True:
intensity, intensity_percent = read_light_intensity() #
get light intensity from ADC
# if there is a more than 2% difference between the current and previous
light intensity update the light intensity
# this is done to prevent light being changed on ADC reading errors
if abs(float(previous_light_intensity_percent) - float(intensity_percent))
> 2:
previous_light_intensity_percent = intensity_percent #
update previous light intensity for next time
print("Light intensity changed to: {}%".format(intensity_percent)) #
print light intensity to console
ADC.write(intensity) #
change light intensity of inside lights
requests.get("https://api.thingspeak.com/update?api_key={}&field1={}".
format(API_KEY, intensity_percent)) # update light intensity on cloud
time.sleep(3) #
wait 3 seconds before checking again to prevent overloading the ADC