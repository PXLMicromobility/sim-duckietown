#!/usr/bin/env python3

"""
    This script is a rewritten version of joystick_control
    It allows for more control than the original script
"""
from duckietown import Duckietown

import pyglet
import cv2 as cv
import numpy as np
import math
from time import time

# Get all the arguments we will need
import argparse

parser = argparse.ArgumentParser(description='This script allows you to control a robot through a joystick in a gym environement')
# parser.add_argument('--map-name', default='udem1', help='the name of the map')
# parser.add_argument('--map-name', default='4way', help='the name of the map')
# parser.add_argument('--map-name', default='loop_dyn_duckiebots', help='the name of the map')
# parser.add_argument('--map-name', default='regress_4way_adam', help='the name of the map')
parser.add_argument('--map-name', default='zigzag_dists', help='the name of the map')

# The store_true option automatically creates a default value of False.
parser.add_argument('--distortion', action='store_true', help='enable fish-eye effect on camera (bool)')
parser.add_argument('--draw-curve', action='store_true', help='draw the lane following curve')
parser.add_argument('--logging-location', default='recording.log', help='the name of a log file (recording of actions)')
args = parser.parse_args()

# Create the duckietown environment
env = Duckietown(
    map_name = args.map_name,
    distortion = args.distortion,
    draw_curve = args.draw_curve
)

env.reset()
env.render()

# Used for computer vision
image = env.render('rgb_array')

def read_joystick():
    global joystick

    # left-right on a joystick
    x = round(joystick.x, 2)
    # up-down on a joystick
    y = -round(joystick.y, 2)

    # A truth table for every button (bool)
    # This is for a Dualshock 4 controller (PS4)
    keys = {
        "cross": joystick.buttons[0],
        "circle": joystick.buttons[1],
        "triangle": joystick.buttons[2],
        "square": joystick.buttons[3],

        "L1": joystick.buttons[4],
        "R1": joystick.buttons[5],
        "L2": joystick.buttons[6],
        "R2": joystick.buttons[7],

        "share": joystick.buttons[8],
        "options": joystick.buttons[9],
        "power": joystick.buttons[10],

        # These are actual presses on the joysticks, not all controllers have this
        # "joy_left": joystick.buttons[11],
        # "joy_right": joystick.buttons[12]
    }

    # Make sure that we only use inputs that are actually usefull
    x, y = x if abs(x) > 0.01 else 0, y if abs(y) > 0.01 else 0

    # How fast can each wheel move (0.35 gives you a maximum forward speed of about 0.4m/s)
    # This also serves as the maximum speed of the wheels
    base_velocity = 0.5

    # Which direction are we trying to go (-1 is back, 1 is forward)
    direction = -1 if y <= 0 else 1

    # How fast does the user want to move (the second term stands for how far out we are pushing the joystick)
    velocity = base_velocity * math.sqrt(y**2 + x**2) * direction

    if velocity == 0:
        # We are not trying to move, make sure we don't
        vel_left, vel_right = 0, 0
    else:
        # Adjust the velocities of both wheels given our adjustment
        # We always want the wheels to move at the speed given by the user unless we are turning
        vel_left = (1 - x**2) * velocity if x < 0 else velocity
        vel_right = (1 - x**2) * velocity if x > 0 else velocity

        # We did them in the wrong order if we're going backwards
        if direction == -1:
            vel_left, vel_right = vel_right, vel_left

        # Cap the speed at the base_velocity, we don't want the bot to go flying off
        if direction > 0:
            # We are going forward
            vel_left, vel_right = min(base_velocity, vel_left), min(base_velocity, vel_right)
            vel_left, vel_right = max(0, vel_left), max(0, vel_right)
        else:
            # We are going backward
            vel_left, vel_right = max(-base_velocity, vel_left), max(-base_velocity, vel_right)
            vel_left, vel_right = min(0, vel_left), min(0, vel_right)

    return vel_left, vel_right

# Not sure what dt stands for lol
def update(dt):
    """
        This method is called every frame to update the screen.
        This method handles the movement of the duckiebot.
    """
    vel_left, vel_right = read_joystick()

    image = env.move([vel_left, vel_right])

    env.render()

def main():
    global joystick

    pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

    # Registers joysticks and recording controls
    joysticks = pyglet.input.get_joysticks()

    # We don't have a joystick connected, y u no have joystick man
    assert joysticks, 'No joystick device is connected'

    # We assume you only want to use one joystick because reasons
    joystick = joysticks[0]

    joystick.open()

    cam_angle = env.unwrapped.cam_angle
    cam_angle[0] -= 5

    # Enter main event loop
    pyglet.app.run()

    env.close()

if __name__ == '__main__':
    main()