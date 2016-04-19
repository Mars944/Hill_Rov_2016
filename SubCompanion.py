""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Imports

import pygame                                               # Used in conjunction with USB Joystick (Could also be used to create a UI)                             
import pygame.camera                                        # Experimental 
from nanpy import (ArduinoApi, SerialManager, Servo, wire)  # Arduino Api & Libraries for slavery
from time import sleep                                      # Used for time.sleep() function
from ROVFunctions import changeInterval
import socket

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up UDP (Treated as Server)

UDP_IP = "192.168.1.11"  # Static IP of Surface Pi
UDP_PORT = 5000          # Port of Surface Pi

client = ('192.168.1.1', 5001)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Socket connection(IPv4, UDP)
sock.bind((UDP_IP, UDP_PORT))                            # Bind socket to IP & Port of the Surface Pi

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Attempts to connect to Camera
camConnected = 1
try:
        cam = pygame.camera.Camera("/dev/video0", (720, 1080))
        cam.start()
        print("Camera Connected!")
except:
        print("Camera Failed to Connect")
        camConnected = 0
        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Connect to arduino

# Attempts to connect to arduino
arduinoConnected = False
try:
        connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected arduino (Connected to bottom left USB Port) and sets baudrate to 115200
        arduino = ArduinoApi(connection=connection)
        arduinoConnected = True
        print("arduino Connected!")
except:
        print("arduino Failed to Connect")

# Define Motor Pins
motorPin1 = 6
motorPin2 = 9
motorPin3 = 10
motorPin4 = 11

# Define Servo Pins
clawUDServoPin     = 2
clawGraspServoPin  = 4
armLRServoPin      = 7
camUDServoPin      = 8

# Connects to ESC's & Servos if arduino is connected
if arduinoConnected:
                motorLeft = Servo(motorPin1)
                motorLeft.writeMicroseconds(1500)
                sleep(1)
                print("ESC1 Connected!")

                motorRight = Servo(motorPin2)
                motorRight.writeMicroseconds(1500)
                sleep(1)
                print("ESC2 Connected!")

                motorVertical = Servo(motorPin3)
                motorVertical.writeMicroseconds(1500)
                sleep(1)
                print("ESC3 Connected!")

                motorHorizontal = Servo(motorPin4)
                motorHorizontal.writeMicroseconds(1500)
                sleep(1)
                print("ESC4 Connected!")

                clawUDServo    = Servo(clawUDServoPin)
                clawGraspServo = Servo(clawGraspServoPin)
                camUDServo     = Servo(camUDServoPin)
                armLRServo     = Servo(armLRServoPin)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Pygame Initializations

pygame.init()                                # Initialize pygame
pygame.camera.init()                         # Initialize the Camera library

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global Variables for Main Loop

# Define Motor Values at default (in mS).
MLeftValue = 1500
MRightValue = 1500
MVerticalValue = 1500
MHorizontalValue = 1500

# Write Servo's to Default
clawUDPosition = 90
clawGraspPosition = 0  # May need to reverse
camUDPosition = 90
armLRPosition = 90

# Should already be in this position
clawUDServo.write(clawUDPosition)
clawGraspServo.write(clawGraspPosition)
camUDServo.write(camUDPosition)
armLRServo.wrote(armLRPosition)
sleep(5)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

running = True   # Breaks out of main loop if equal to False.
while running:
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive & Translate Motor & Servo values from Surface

    rData = sock.recvfrom(1024)
    rData = rData.decode('utf-8')

    MLeftValue = int(rData[:4])
    MRightValue = int(rData[4:8])
    MVerticalValue = int(rData[8:12])
    MHorizontalValue = int(rData[12:16])

    clawUDPosition = int(rData[16:19])
    armLRPosition = int(rData[19:22])
    clawGraspPosition = int(rData[22:25])
    camUDPosition = int(rData[25:28])

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Write to motors & servos

    # Limits Motor speed from the original interval [1100, 1900]
    motorMax = 1700
    motorMin = 1300

    # Limits & writes M_Values to ESC's
    if arduinoConnected:
            if MLeftValue > 1500:
                    motorLeft.writeMicroseconds(min(MLeftValue, motorMax))
            elif MLeftValue < 1500:
                    motorLeft.writeMicroseconds(max(MLeftValue, motorMin))
            else:
                    motorLeft.writeMicroseconds(MLeftValue)

            if MRightValue > 1500:
                    motorRight.writeMicroseconds(min(MRightValue, motorMax))
            elif MRightValue < 1500:
                    motorRight.writeMicroseconds(max(MRightValue, motorMin))
            else:
                    motorRight.writeMicroseconds(MRightValue)

            if MVerticalValue > 1500:
                    motorVertical.writeMicroseconds(min(MVerticalValue, motorMax))
            elif MVerticalValue < 1500:
                    motorVertical.writeMicroseconds(max(MVerticalValue, motorMin))
            else:
                    motorVertical.writeMicroseconds(MVerticalValue)

            if MHorizontalValue > 1500:
                    motorHorizontal.writeMicroseconds(min(MHorizontalValue, motorMax))
            elif MHorizontalValue < 1500:
                    motorHorizontal.writeMicroseconds(max(MHorizontalValue, motorMin))
            else:
                    motorHorizontal.writeMicroseconds(MHorizontalValue)

            # Write to Servos
            clawUDServo.write(clawUDPosition)
            clawGraspServo.write(clawGraspPosition)
            camUDServo.write(camUDPosition)
            armLRServo.wrote(armLRPosition)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive values from Camera and Sensors

    if camConnected:
        camString = cam.get_raw()  # Stores string of image
    else:
        try:
            cam = pygame.camera.Camera("/dev/video0", (720, 1080))
            cam.start()
            print("Camera Connected!")
            camConnected = 1
        except:
            print("Camera Failed to Connect")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Prepare and send data to Surface

    rData = str(camConnected) + camString  # Plus sensor values
    rData.encode('utf-8')

    sock.sendto(rData, client)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Prepare to Quit

# Reset all Servos to default
clawUDServo.write(90)
clawGraspServo.write(0)
armLRServo.write(90)
camUDServo.write(90)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

pygame.quit()
quit()
