""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Index:

# 1. Imports
# 2. Global Classes
# 3. Define GUI Variables
# 4. Create Window
# 5. Attempts to connect to Camera
# 6. Connect to arduino
# 7. Pygame Initializations
# 8. Joystick/Gamepad Variables & Setup
# 9. Global Variables for Main Loop
# 10. Write Servo's to Default
# 11. Main Loop
# 12. Quit
# 13. Known Issues

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
# Imports

import pygame                                               # Used in conjunction with USB Joystick (Could also be used to create a UI)                             
import pygame.camera                                        # Experimental 
from nanpy import (ArduinoApi, SerialManager, Servo, wire)  # Arduino Api & Libraries for slavery
from time import sleep                                      # Used for time.sleep() function
from ROVFunctions import changeInterval
import socket

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Setup UDP

UDP_IP = "CHANGE TO PI'S IP"
UDP_Port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # (IPv4 Internet, UDP)

sock.bind((UDP_IP, UDP_Port)

while 1:
    data, address = sock.recvfrom(1024) # buffer size is 1024 bytes

    print(data))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Attempts to connect to Camera
camConnected = True
try:
        cam = pygame.camera.Camera("/dev/video0", (720, 1080)) # PSEYE Default Dimesnsions: (640,480)
        cam.start()
        print("Camera Connected!")
except:
        print("Camera Failed to Connect")
        camConnected = False
        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Connect to arduino

# Attempts to connect to arduino
arduinoConnected = False
try:
        connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected arduino (Connected to bottom left USB Port) and sets baudrate to 115200
        arduino = ArduinoApi(connection = connection)
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

                clawUDServo     = Servo(clawUDServoPin)
                clawGraspServo  = Servo(clawGraspServoPin)
                camUDServo      = Servo(camUDServoPin)
                armLRServo      = Servo(armLRServoPin)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Pygame Initializations

pygame.init()                                # Initialize pygame
pygame.camera.init()                         # Initialize the Camera library

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global Variables for Main Loop

running = True   # Breaks loop if False.

# Define Motor Values at default (in mS).
MLeftValue = 1500
MRightValue = 1500
MVerticalValue = 1500
MHorizontalValue = 1500

# Write Servo's to Default
clawUDPosition = 90
clawGraspPosition = 0   # May need to reverse
camUDPosition = 90
armLRPosition = 90

clawUDServo.write(clawUDPosition)
clawGraspServo.write(clawGraspPosition)
camUDServo.write(camUDPosition)
armLRServo.wrote(armLRPosition)
sleep(5)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

while running:

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Update GUI        

        # Sets throttle text's color to Red if at 0.
        if throttle == 0:
                valMotorsText.changeColor(RED)

        valMotorsText.Print(screen, "Throttle: " + str(int(throttle*100)) + "%")
        valMotorsText.newLine()

        # Display Value of all motors
        if joystickConnected and arduinoConnected:
                valMotorsText.Print(screen, "Motor 1: " + str(MLeftValue))
                valMotorsText.newLine()

                valMotorsText.Print(screen, "Motor 2: " + str(MRightValue))
                valMotorsText.newLine()
                
                valMotorsText.Print(screen, "Motor 3: " + str(MVerticalValue))
                valMotorsText.newLine()

                valMotorsText.Print(screen, "Motor 4: " + str(MHorizontalValue))
                valMotorsText.newLine()
        else:
                if not arduinoConnected:
                        valMotorsText.changeColor(RED)
                        valMotorsText.Print(screen, "arduino is DISCONNECTED")
                        valMotorsText.newLine()
                        valMotorsText.changeColor(BLACK)
                if not joystickConnected:
                        valMotorsText.changeColor(RED)
                        valMotorsText.Print(screen, "Joystick is DISCONNECTED")
                        valMotorsText.newLine()
                        valMotorsText.changeColor(BLACK)
        if gamepadConnected:
                # Update Screen with arm values
                pass
        else:
                valArmText.changeColor(RED)
                valArmText.Print(screen, "Gamepad is DISCONNECTED")
                        
        pygame.display.update()
        clock.tick(60) # Sets FPS to 60

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Write to motors

        # Limits Motor speed 
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
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

# Reset arm Servos to default
clawUDPosition = 90
clawGraspPosition = 0  # May need to reverse
armLRPosition = 90

clawUDServo.write(clawUDPosition)
clawGraspServo.write(clawGraspPosition)
armLRServo.write(armLRPosition)

# Reset Camera Servo to Default
camUDPosition= 90
camUDServo.write(camUDPosition)

# Quit
pygame.quit()
quit()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Known Issues

"""

- Once Connected, joystick, camera, & arduino can not be reconnected.
- Motors algorithms suck. Fix them.
-Power must be turned on before arduino.

"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
