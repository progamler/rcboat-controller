#!/usr/bin/env python2
#
# 
# NOTE: This script requires the following Python modules:
#  pygame   - http://www.pygame.org/
# Win32 users may also need:
#  pywin32  - http://sourceforge.net/projects/pywin32/
#

import pygame
import socket
# allow multiple joysticks
joy = []

HOST = '10.0.0.255'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

value = 150
# handle joystick event
def handleJoyEvent(e):
    value=150
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"

        if (e.dict['axis'] == 1):
            axis = "Y"

        if (e.dict['axis'] == 2):
            axis = "Throttle"

        if (e.dict['axis'] == 3):
            axis = "Z"

        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # uncomment to debug
            #output(str, e.dict['joy'])

            ## Send Servo Value to boat
            if (axis == "X"):
                print(str)
                ## convert joystick position to servo increment
                x = (225*e.dict['value'])+375
                s.sendall('0;' + repr(x))
                print(x)
            elif (axis == "Throttle"):
                print(str)
                ## convert joystick position to servo increment
                x = (225*e.dict['value'])+375
                s.sendall('1;' + repr(x))
                print(x)

		

    elif e.type == pygame.JOYBUTTONDOWN:
        str = "Button: %d" % (e.dict['button'])
        # uncomment to debug
        #output(str, e.dict['joy'])
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 0):
            print "Bye!n"
            s.close()
            quit()
    else:
        pass

# print the joystick position
def output(line, stick):
    print "Joystick: %d; %s" % (stick, line)

# wait for joystick input
def joystickControl():
    while True:
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):
            handleJoyEvent(e)

# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "nPlease connect a joystick and run again.n"
        quit()
    print "n%d joystick(s) detected." % pygame.joystick.get_count()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print "Joystick %d: " % (i) + joy[i].get_name()
    print "Depress trigger (button 0) to quit.n"

    # run joystick listener loop
    joystickControl()

# allow use as a module or standalone script
if __name__ == "__main__":
    main()
