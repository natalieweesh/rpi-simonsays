import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button, LED, RGBLED
from signal import pause
from functools import partial, update_wrapper
import time, random

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

sound_pins = {
    2: Sound("sounds/drum_tom_mid_hard.wav"),
    3: Sound("sounds/drum_cymbal_open.wav")
}
led_pins = {
    0: LED(8, initial_value=False),
    1: LED(7, initial_value=False)
}
rgb = RGBLED(5, 6, 13)
rgb.color = (0, 0, 0)
left_button = Button(2)
right_button = Button(3)

simon = [0]
listening = False
user_input = []

def left():
    sound_pins[2].play()
    led_pins[0].on()
    time.sleep(0.5)
    led_pins[0].off()
    time.sleep(0.5)

def right():
    sound_pins[3].play()
    led_pins[1].on()
    time.sleep(0.5)
    led_pins[1].off()
    time.sleep(0.5)

def simon_says():
    global simon
    rgb.color = (1, 1, 1)
    print("SIMON SAYS...")
    for i in simon:
        if i == 0:
            left()
        else:
            right()
    print("YOUR TURN!")
    return listen()

def press(which):
    global listening
    if not listening:
        return
    if which == "left":
        sound_pins[2].play()
        led_pins[0].on()
        user_pressed("left")
    else:
        sound_pins[3].play()
        led_pins[1].on()
        user_pressed("right")

def user_pressed(which):
    global user_input
    global simon
    if len(user_input) < len(simon):
        if which == "left":
            user_input.append(0)
        else:
            user_input.append(1)
    if len(user_input) == len(simon):
        check_answer()

def check_answer():
    global user_input
    global simon
    global listening
    listening = False
    if user_input == simon:
        print("CORRECT!")
        correct_answer()
        next_turn()
    else:
        rgb.color = (1, 0, 0)
        print("YOU LOSE :(")
        print("you got up to ", len(simon), " turns")

def correct_answer():
    rgb.color = (0, 1, 0)
    time.sleep(1)
    led_pins[0].off()
    led_pins[1].off()

def next_turn():
    global user_input
    time.sleep(0.5)
    time.sleep(2)
    user_input = []
    simon.append(round(random.random()))
    simon_says()

def listen():
    global listening
    rgb.color = (1, 0.5, 0)
    listening = True
    user_input = []
    left_button.when_pressed = wrapped_partial(press, which="left")
    right_button.when_pressed = wrapped_partial(press, which="right")
    left_button.when_released = led_pins[0].off
    right_button.when_released = led_pins[1].off    

def main():
    time.sleep(1)

    simon_says()
    


if __name__ == "__main__":
    main()
