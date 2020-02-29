# Sending data to esp8266

import socket
import pygame
import time
import math

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init() 
numaxes = joystick.get_numaxes()

time.sleep(2)
arr = []

def digit_counter(Number):
    Count = 0
    while(Number > 0):
        Number = Number // 10
        Count = Count + 1
    return Count

def getAxis_fb(number):
    if(joystick.get_axis(number) < -0.1 or joystick.get_axis(number) > 0.1):
        sign = joystick.get_axis(number)/abs(joystick.get_axis(number))
        nos = sign*math.log(9*abs(joystick.get_axis(number)) + 1)/2.303
        nos = int(nos*-1*1024)
        if nos > 0:
            forward = abs(nos)
            backward = 0
        elif(nos < 0):
            forward = 0
            backward = abs(nos)
        else:
            forward = 0
            backward = 0

        return forward,backward

def getAxis_lr(number):
    if(joystick.get_axis(number) < -0.1 or joystick.get_axis(number) > 0.1):
        sign = joystick.get_axis(number)/abs(joystick.get_axis(number))
        nos = sign*math.log(9*abs(joystick.get_axis(number)) + 1)/2.303
        nos = int(nos*1024)
        if nos > 0:
            left = abs(nos)
            right = 0
        elif(nos < 0):
            left = 0
            right = abs(nos)
        else:
            left = 0
            right = 0

        return left,right

def main():
    port = 1111
    host = '192.168.43.139'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        pygame.event.pump()
        result_fb = getAxis_fb(1)
        result_lr = getAxis_lr(4)

        forward = 0
        backward = 0
        left = 0
        right = 0

        if result_fb != None:
            forward = result_fb[0]
            backward = result_fb[1]
        if result_lr != None:
            left = result_lr[0]
            right = result_lr[1]

        # print("Forward :",forward)
        # print("Backward :",backward)
        # print("Left :",left)
        # print("Right :",right)

        array = [forward , backward , right , left]
        final_array = []
        for i in array:
            digits = digit_counter(i)
            if digits == 0:
                str_value = "0000"
            elif digits == 1:
                str_value = str(i)
                str_value = "000"+str_value
            elif digits == 2:
                str_value = str(i)
                str_value = "00"+str_value
            elif digits == 3:
                str_value = str(i)
                str_value = "0"+str_value
            else:
                str_value = str(i)
            final_array.append(str_value)

        string =  final_array[0] + final_array[1]  + final_array[2] + final_array[3]
        s.sendto(string, (host, port))
        time.sleep(0.15)


if __name__ == "__main__":
    main()
