import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

"""
*** Complete the following code to make the led blink. ***
"""


def blink_led():
    pin = 7     # *** Make sure this is the pin your led is connected to! ***
    GPIO.setup(pin, GPIO.OUT)
    
    # *** Replace HOW_MANY_TIMES_TO_BLINK ***
    for blink in range(HOW_MANY_TIMES_TO_BLINK):    
        print("LED on")
        GPIO.output(pin, GPIO.HIGH)
        # *** Replace HOW_LONG_TO_STAY_ON (This value is in seconds) ***
        time.sleep(HOW_LONG_TO_STAY_ON)         
        print("LED off")
        GPIO.output(pin, GPIO.LOW)
        # *** Replace HOW_LONG_TO_STAY_OFF (This value is in seconds) ***
        time.sleep(HOW_LONG_TO_STAY_OFF)

    # Clean up the GPIO pins.
    GPIO.cleanup()        


def led_on_switch():
    switch_pin = 11 # *** Make sure this is the pin your switch is connected to! ***
    led_pin = 7     # *** Make sure this is the pin your led is connected to! ***
    on = False

    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # *** Replace CONDITION with either True or False ***
    while CONDITION:
        state = GPIO.input(switch_pin) == 0
        if state == CONDITION:
            GPIO.output(led_pin, GPIO.HIGH)
            on = True

        else:
            #turn led off
            if on:
                GPIO.output(led_pin, GPIO.LOW)
                on = False

    # Clean up the GPIO pins.
    GPIO.cleanup() 
        

def simon():
    '''
    leds and switches are both dictionaries, mapping the reference number 
    (i.e 1 2 3 4) of a led or switch to it's pin number.  You must ensure that
    the pin your led/switch is connected to is the same as the number after the 
    colon ( : ). 
    '''    
    leds = {1: 7,
            2: 11,
            3: 12,
            4: 13}

    switches = {1: 37,
                2: 36,
                3: 33,
                4: 31}


    # Set up all nessesary pins.
    for led in leds:
        GPIO.setup(leds[led], GPIO.OUT)
    for switch in switches:
        GPIO.setup(switches[switch], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    n = 4   # Number of lights per combination.
    t = 0.8 # How long each light is lit up for.

    # Start looping over our game logic untill the user quits.
    while True:
        # Get a random sequence of length n.
        seq = []
        for s in range(n):
            seq.append(random.randrange(1,5))

        # Display our sequence.
        for led_pin in seq:
            GPIO.output(leds[led_pin], GPIO.HIGH)
            time.sleep(t)
            GPIO.output(leds[led_pin], GPIO.LOW)
            time.sleep(t/2)

        print("seq =", seq)
        # Start looking for pressed switches untill at least n switches are pressed.
        switches_activated = []
        order = []
        while True:
            # Iterate through each switch, checking its state. Switch is only 
            # added to order after it is released.
            for switch in switches:

                activated = GPIO.input(switches[switch]) == 0

                if  activated and switch not in switches_activated:
                    switches_activated.append(switch)
                    GPIO.output(leds[switch], GPIO.HIGH)
                    
                if not activated and switch in switches_activated:
                    switches_activated.remove(switch)
                    order.append(switch)
                    print(switch, "pressed")
                    GPIO.output(leds[switch], GPIO.LOW)

            if len(order) >= len(seq):
                break

        loss = False
        
        # Check if there is the same number of switches pressed as is in our sequence.
        if len(seq) != len(order):
            loss = True

        # Check if the switches were pressed in the same order as our sequence.
        for s in range(len(seq)):
            if seq[s] != order[s]:
                loss = True
                break

        # Perform appropriate action based on weather the user won or lost.
        if loss == True:
            # If this code executes the user lost.
            display_loss(leds)
            # Reset variables.
            t = 0.8
            n = 4

        else:   
            # If this code executes user must have won!
            # Update t and n to make it harder!
            t -= 0.1
            n += 1      

            print("order=", order)
            print("correct!")

        # Ask the user if they want to play again.
        nput = input("Would you like to play again? ").lower()
        if nput != 'y' and nput != 'yes':
            # We are abput to exit! Clean up the GPIO pins.
            GPIO.cleanup() 
            return
        print("-" * 80)
        

def display_loss(leds):
    print("incorrect")
    # Blink leds 4 times.
    for x in range(4):
        for led in leds:
            GPIO.output(leds[led], GPIO.HIGH)

        time.sleep(0.5)

        for led in leds:
            GPIO.output(leds[led], GPIO.LOW)

        time.sleep(0.5)


# *** Uncomment one of the following to make that function run! ***

#blink_led()
#led_on_switch()
#simon()
GPIO.cleanup()
