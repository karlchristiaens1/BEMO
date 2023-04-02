import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time
import threading
def eyes_blink(t):                          #calling time to provide delays in program
    #IO.cleanup
    IO.setwarnings(False)           #do not show any warnings
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(19,IO.OUT)      # initialize GPIO19 as an output.
    IO.setup(20, IO.OUT)
    f = 100
    p1 = IO.PWM(19,f)          #GPIO19 as PWM output, with 100Hz frequency
    p1.start(0)                              #generate PWM signal with 0% duty cycle
    
    p2 = IO.PWM(20,f)          #GPIO19 as PWM output, with 100Hz frequency
    p2.start(0)                              #generate PWM signal with 0% duty cycle
    
    #IO.cleanup()
    
    time_end = time.time() + t
    while time.time()<time_end:                               #execute loop forever
        for x in range (50):                          #execute loop for 50 times, x being incremented from 0 to 49.
            p1.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
            p2.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
            time.sleep(1/f)                           #sleep for 100m seconds


        for x in range (50):                         #execute loop for 50 times, x being incremented from 0 to 49.
            p1.ChangeDutyCycle(50-x)        #change duty cycle for changing the brightness of LED.
            p2.ChangeDutyCycle(50-x)        #change duty cycle for changing the brightness of LED.
            time.sleep(1/f)                          #sleep for 100m secon
    left_eyes_low()
    right_eyes_low()       

def right_eyes_low():
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(19,IO.OUT)      # initialize GPIO19 as an output.
    IO.output(19, 0)    # initialize GPIO19 as an output.

def right_eyes_high():
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(19,IO.OUT)      # initialize GPIO19 as an output.
    IO.output(19, 1)    # initialize GPIO19 as an output.

def left_eyes_low():
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(20,IO.OUT)      # initialize GPIO19 as an output.
    IO.output(20, 0)    # initialize GPIO19 as an output.

def left_eyes_high():
    #code to turn LED off!
    #IO.cleanup
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(20,IO.OUT)      # initialize GPIO19 as an output.
    IO.output(20, 1)    # initialize GPIO19 as an output.
    
def ears_up():                          #calling time to provide delays in program
    IO.setwarnings(False)           #do not show any warnings
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(13,IO.OUT)      # initialize GPIO19 as an output.
    IO.setup(12, IO.OUT)
    f = 300
    p1 = IO.PWM(13,f)          #GPIO19 as PWM output, with 100Hz frequency
    p2 = IO.PWM(12,f)
    p1.start(75)                              #generate PWM signal with 0% duty cycle
    p2.start(75)
    time.sleep(2)
    #IO.cleanup()
#75-10 : is the range from 0 to 180 degrees
def ears_down():                          #calling time to provide delays in program
    IO.setwarnings(False)           #do not show any warnings
    IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
    IO.setup(13,IO.OUT)      # initialize GPIO19 as an output.
    IO.setup(12, IO.OUT)
    f = 300
    p1 = IO.PWM(13,f)          #GPIO19 as PWM output, with 100Hz frequency
    p2 = IO.PWM(12,f)
    p1.start(42.5)                              #generate PWM signal with 0% duty cycle
    p2.start(42.5)
    time.sleep(2)
    #IO.cleanup()        

#DEFINING THREADS
def thread_eyes_blink():
    blinking_eyes = threading.Thread(target = eyes_blink, args = (7,))
    blinking_eyes.start()

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
