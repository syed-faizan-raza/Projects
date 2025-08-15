import RPi.GPIO as GPIO # for interfacing with RPi
import time # for time.sleep
import LCD1602 as lcd # for interfacing with LCD
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# set up rows as inputs
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# set up cols as outputs
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
def get_key():
'''
get a keypad press from the user
Returns: A tuple of
'''
while(True):
# check col 1
GPIO.output(26, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)
GPIO.output(24, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
if (GPIO.input(22)==0):
return (1, '!')
if (GPIO.input(21)==0):
return (4, '$')
if (GPIO.input(20)==0):
return (7, '&')
if (GPIO.input(19)==0): # * key
return (0xE, None)
# check col 2
GPIO.output(26, GPIO.HIGH)
GPIO.output(25, GPIO.LOW)
GPIO.output(24, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)
if (GPIO.input(22)==0):
return (2, '@')
if (GPIO.input(21)==0):
return (5, '%')
if (GPIO.input(20)==0):
return (8, '*')
if (GPIO.input(19)==0):
return (0, ')')
# check col 3
GPIO.output(26, GPIO.HIGH)
GPIO.output(25, GPIO.HIGH)
GPIO.output(24, GPIO.LOW)
GPIO.output(23, GPIO.HIGH)
if (GPIO.input(22)==0):
return (3, '#')
if (GPIO.input(21)==0):
return (6, '^')
if (GPIO.input(20)==0):
return (9, '(')
if (GPIO.input(19)==0): # # key
return (0xF, None)
# check col 4
GPIO.output(26, GPIO.HIGH)
GPIO.output(25, GPIO.HIGH)
GPIO.output(24, GPIO.HIGH)
GPIO.output(23, GPIO.LOW)
if (GPIO.input(22)==0): # A key
return (0xA, None)
if (GPIO.input(21)==0): # B key
return (0xB, None)
if (GPIO.input(20)==0): # C key
return (0xC, None)
if (GPIO.input(19)==0): # D key
return (0xD, None)
def get_password(shift_key_gpio):
'''
get 2 digit input from user
Parameters: shift_key_gpio: the GPIO number of the shift key
Returns: the 2 keys concatenated as a string
'''
# get key from user and save normal key or shift key depending on if shift
key gpio is pressed
normal_key1, shift_key1 = get_key()
key1 = str(normal_key1 if GPIO.input(shift_key_gpio) == GPIO.LOW else
shift_key1)
lcd.write(0, 1, key1) # show what was typed
time.sleep(0.5) # prevent one press causing 2 presses
# get key from user and save normal key or shift key depending on if shift
key gpio is pressed
normal_key2, shift_key2 = get_key()
key2 = str(normal_key2 if GPIO.input(shift_key_gpio) == GPIO.LOW else
shift_key2)
lcd.write(0, 1, key1 + key2) # show what was typed
time.sleep(0.5) # prevent one press causing 2 presses
return key1 + key2 # return the concatinated string