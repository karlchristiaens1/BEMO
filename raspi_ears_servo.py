import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time
import threading

def eyes_blink(t):                    #calling time to provide delays in program
    #IO.cleanup
    IO.setwarnings(False)           # do not show any warnings
    IO.setmode (IO.BCM)             # we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(19,IO.OUT)             # initialize GPIO19 as an output.
    IO.setup(20, IO.OUT)            # initialize GPIO20 as an output.
    f = 100                         # Set up PWM frequency
    p1 = IO.PWM(19,f)               # GPIO19 as PWM output, with 100Hz frequency
    p1.start(0)                     # Generate PWM signal with 0% duty cycle
    
    p2 = IO.PWM(20,f)               # GPIO20 as PWM output, with 100Hz frequency
    p2.start(0)                     # Generate PWM signal with 0% duty cycle
    #IO.cleanup()
    
    time_end = time.time() + t
    while time.time()<time_end:                 # execute loop until time reaches the end
        for x in range (50):                    # execute loop for 50 times, x being incremented from 0 to 49.
            p1.ChangeDutyCycle(x)               # change duty cycle for varying the brightness of LED for GPIO19
            p2.ChangeDutyCycle(x)               # change duty cycle for varying the brightness of LED for GPIO20
            time.sleep(1/f)                     # sleep


        for x in range (50):                    # execute loop for 50 times, x being decreased from 49 to 0.
            p1.ChangeDutyCycle(50-x)            # change duty cycle for changing the brightness of LED for GPIO19.
            p2.ChangeDutyCycle(50-x)            # change duty cycle for changing the brightness of LED for GPIO20.
            time.sleep(1/f)                     # sleep
    
    #Turning off LEDs afterwards
    left_eyes_low()
    right_eyes_low()       

def right_eyes_low():       #GPIO19 LOW
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         
    IO.setup(19,IO.OUT)     
    IO.output(19, 0)    
    

def right_eyes_high():      #GPIO19 HIGH then LOW after 3 seconds
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         
    IO.setup(19,IO.OUT)     
    IO.output(19, 1)    
    time.sleep(3)
    right_eyes_low()

def left_eyes_low():        #GPIO20 LOW
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         
    IO.setup(20,IO.OUT)      
    IO.output(20, 0)   

def left_eyes_high():       #GPIO20 HIGH then LOW after 3 seconds
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         
    IO.setup(20,IO.OUT)     
    IO.output(20, 1)    
    time.sleep(3)
    left_eyes_low()

#CONTROLLING EARS MOVEMENT:
#75-10 : is the range from 0 to 180 degrees

def ears_up():              
    IO.setwarnings(False)   # do not show any warnings
    IO.setmode (IO.BCM)     
    IO.setup(13,IO.OUT)     # initialize GPIO13 as an output.
    IO.setup(12, IO.OUT)    # initialize GPIO12 as an output.
    f = 300
    p1 = IO.PWM(13,f)       # GPIO13 as PWM output, with 300Hz frequency
    p2 = IO.PWM(12,f)       # GPIO12 as PWM output, with 300Hz frequency
    p1.start(75)            # generate PWM signal with 75% duty cycle GPIO13
    p2.start(75)            # generate PWM signal with 75% duty cycle GPIO12
    time.sleep(2)
    #IO.cleanup()
    
def ears_down():                          
    IO.setwarnings(False)    # do not show any warnings
    IO.setmode (IO.BCM)         
    IO.setup(13,IO.OUT)      # initialize GPIO13 as an output.
    IO.setup(12, IO.OUT)     # initialize GPIO12 as an output.
    f = 300
    p1 = IO.PWM(13,f)        # GPIO13 as PWM output, with 300Hz frequency
    p2 = IO.PWM(12,f)        # GPIO12 as PWM output, with 300Hz frequency
    p1.start(42.5)           # generate PWM signal with 42.5% duty cycle GPIO13
    p2.start(42.5)           # generate PWM signal with 42.5% duty cycle GPIO12
    time.sleep(2)
    #IO.cleanup()        

#DEFINING THREADS
def thread_eyes_blink():
    blinking_eyes = threading.Thread(target = eyes_blink, args = (7,))
    blinking_eyes.start()

def thread_happy():
    left_eye = threading.Thread(target = left_eyes_high)
    left_eye.start()

def thread_sad():
    right_eye = threading.Thread(target = right_eyes_high)
    right_eye.start()
    
def thread_ears_up():
    raising_ears = threading.Thread(target = ears_up)
    raising_ears.start()

def thread_ears_down():
    lowering_ears = threading.Thread(target = ears_down)
    lowering_ears.start()

#DEFINING INTERRUPTS
def read_flex_sensor():
    IO.setmode (IO.BCM)
    channel = 6
    IO.setup(channel, IO.IN, pull_up_down = IO.PUD_DOWN)
    IO.add_event_detect(channel, IO.FALLING, callback = callback_one, bouncetime = 200)
    #if IO.event_detected(channel):
     #   print('Eevent was detected')

def read_button_right_sensor():
    IO.setmode (IO.BCM)
    channel = 5
    IO.setup(channel, IO.IN, pull_up_down = IO.PUD_DOWN)
    IO.add_event_detect(channel, IO.FALLING, callback = callback_two, bouncetime = 1000)

def read_button_left_sensor():
    IO.setmode (IO.BCM)
    channel = 21
    IO.setup(channel, IO.IN, pull_up_down = IO.PUD_DOWN)
    IO.add_event_detect(channel, IO.FALLING, callback = callback_three, bouncetime = 1000)

#DEFINING CALLBACKS FOR INTERRUPTS
def callback_one(channel):
    eyes_blink(8)

def callback_two(channel):
    print('Calling HMS.py')
    import HMS
    HMS.main()
    

def callback_three(channel):
    print('Calling Command.py')
    import Command 
    Command.main()
 
# FOR TESTING PURPOSES
#eyes_low()
#eyes_blink(100)
#ears_up()
#ears_down()

#thread_ears_up()
#thread_ears_down()

#while True:
    #sweep(45)
    #sweep(90)
#read_flex_sensor()
#read_button_right_sensor()
    
#START THREADING & INTERRUPTS
x = threading.Thread(target = read_flex_sensor)
y = threading.Thread(target = read_button_right_sensor)
z = threading.Thread(target = read_button_left_sensor)

x.start()
y.start()
z.start()

# ~ thread_eyes_blink()
# ~ thread_ears_up()
# ~ i = 1
# ~ while 1:
    # ~ i = i +1
    # ~ print('Does code here, ', i)
    # ~ time.sleep(1)
    # ~ thread_ears_down()
