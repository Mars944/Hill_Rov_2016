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
clawUDPosition      = 90
clawGraspPosition   = 0   # May need to reverse
camUDPosition       = 90
armLRPosition  = 90

clawUDServo.write(clawUDPosition)
clawGraspServo.write(clawGraspPosition)
camUDServo.write(camUDPosition)
armLRServo.wrote(armLRPosition)
sleep(5)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

while running:
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Checks to see if the User has quit
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                       
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Reset Display

        # Reset Value TextBox's
        valMotorsText.reset()
        valArmText.reset()

        screen.fill(GRAY) # Reset Screen to gray

        # Attemp to Display Video Feed
        if camConnected:
                screen.blit(pygame.transform.scale(cam.get_image(), (524,393)), (0,0))
        else:
                camDisconnectedText.Print(screen, "CAMERA DISCONNECTED.")

        # Displays screenshots
        pygame.draw.rect(screen, ORANGE,(535, 399, 673, 250)) # 535 399 673 250
        if screenshotLeft != None:
                screen.blit(pygame.transform.scale(screenshotLeft, (320,240)), (548, 409))
        if screenshotRight != None:
                screen.blit(pygame.transform.scale(screenshotRight, (320,240)), (876,409))
        
        # Display Titles
        motorTitleText.Print(screen, "Motor Values:")
        sensTitleText.Print(screen, "Sensor Values:")
        gamepadReminderText.Print(screen, "Mash <Playstation Button> after Reconnect!")

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Read from Gamepad if gamepad is connected

        """ Presume Up & Right to be +1. May need to reverse on a case by case basis. """

        if gamepadConnected:
                for b in [4, 5, 6, 7, 8, 9, 10, 11]:
        
                        # Up on D-pad
                        if b == 4: # Extend Arm
                                if gamepad.get_button(b) == 1:
                                        if clawUDPosition > 0:
                                                clawUDPosition -= 1
                                                clawUDServo.write(clawUDPosition)

                        # Down on D-pad
                        elif b == 6: # Withdraw Arm
                                if gamepad.get_button(b) == 1:
                                        if clawUDPosition < 180:
                                                clawUDPosition += 1
                                                clawUDServo.write(clawUDPosition)

                        # Left on D-pad
                        elif b == 7:
                                if gamepad.get_button(b) == 1:
                                        if armLRPosition > 0:
                                                armLRPosition -= 1
                                                armLRServo.write(armLRPosition)

                        # Right on D-pad
                        elif b == 5:
                                if gamepad.get_button(b) == 1:
                                        if armLRPosition < 180:
                                                armLRPosition += 1
                                                armLRServo.write(armLRPosition)

                        # Right Trigger (Future Dylan: Their Triggers are your Bumpers. Love Past Dylan)
                        elif b == 9: # Close Claw
                                if gamepad.get_button(b) == 1:
                                        if clawGraspPosition < 180:
                                                print("Right")
                                                clawGraspPosition+=1
                                                clawGraspServo.write(clawGraspPosition)

                        # Left Trigger
                        elif b == 8: # Open Claw
                                if gamepad.get_button(b) == 1:
                                        if clawGraspPosition > 0:
                                                print("Left")
                                                clawGraspPosition-=1
                                                clawGraspServo.write(clawGraspPosition)


                # Camera Related Buttons. Tracked separately from arm servos
                for b in [1, 2]:
                        # Left Joystick
                        if b == 1:                  # Flip through saved Left Screenshots
                                if ssWaitL == 0:
                                        if gamepad.get_button(b) == 1:
                                                if not screenshotsLeft:
                                                        pass
                                                else:
                                                        ssDisplayedIndexL+=1
                                                        if ssDisplayedIndexL >= len(screenshotsLeft):
                                                                ssDisplayedIndexL = 0
                                                        screenshotLeft = screenshotsLeft[ssDisplayedIndexL]
                                                        ssWaitL+=1
                                else:
                                        ssWaitL+=1
                                        if ssWaitL >= 10:
                                                ssWaitL = 0

                        # Right Joystick
                        if b == 2:                  # Flip through saved Right Screenshots
                                if ssWaitR == 0:
                                        if gamepad.get_button(b) == 1:
                                                if not screenshotsRight:
                                                        pass
                                                else:
                                                        ssDisplayedIndexR+=1
                                                        if ssDisplayedIndexR >= len(screenshotsRight):
                                                                ssDisplayedIndexR = 0
                                                        screenshotRight = screenshotsRight[ssDisplayedIndexR]
                                                        ssWaitR+=1
                                else:
                                        ssWaitR+=1
                                        if ssWaitR >= 10:
                                                ssWaitR = 0
                                
                for b in [12, 13, 14, 15]:
                        # Triangle Button
                        if b == 12:                 # Move Camera Servo Up
                                if gamepad.get_button(b) == 1:
                                                if camUDPosition < 180:        
                                                        camUDPosition+=1
                                                        camUDServo.write(camUDPosition) 

                        # Circle Button
                        elif b == 13:               # Save Screenshot to RightArray            
                                if circleWait == 0:
                                        if camConnected:
                                                if gamepad.get_button(b) == 1:
                                                        screenshotsRight.append(cam.get_image())
                                                        ssDisplayedIndexR = len(screenshotsRight)-1
                                                        screenshotRight = screenshotsRight[len(screenshotsRight)-1]
                                                        circleWait+=1
                                else:
                                        circleWait+=1
                                        if circleWait >= 10:
                                                circleWait = 0

                        # X Button
                        elif b == 14:               # Move Camera Servo Down
                                if gamepad.get_button(b) == 1:
                                                if camUDPosition > 0:
                                                        camUDPosition-=1
                                                        camUDServo.write(camUDPosition)
                        # Square Button
                        elif b == 15:               # Save Screenshot to LeftArray            
                                if squareWait == 0:
                                        if camConnected:
                                                if gamepad.get_button(b) == 1:
                                                        screenshotsLeft.append(cam.get_image())
                                                        ssDisplayedIndexL = len(screenshotsLeft)-1
                                                        screenshotLeft = screenshotsLeft[len(screenshotsLeft)-1]
                                                        squareWait+=1
                                else:
                                        squareWait+=1
                                        if squareWait >= 10:
                                                squareWait = 0   

                # Check motion tracker to see if gamepad is disconnected.
                OGa23 = a23
                OGa24 = a24
                OGa25 = a25
                
                a23 = gamepad.get_axis(23)
                a24 = gamepad.get_axis(24)
                a25 = gamepad.get_axis(25)
                
                if OGa23==a23 and OGa24==a24 and OGa25==a25:
                        checkCount += 1
                        if checkCount == 100:
                                gamepadConnected = False
                                checkCount = 0
                else:
                        checkCount = 0
                        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Reads Joystick input if Joystick and Ardunio are both connected.

        if joystickConnected and arduinoConnected:

                numAxes = joystick.get_numaxes() # Gets number of axis on Joystick


                # Up/Down
                if joystick.get_hat(0) == (-1, 1) or joystick.get_hat(0) == (0, 1) or joystick.get_hat(0) == (1, 1):
                        MVerticalValue = 1500+(400*throttle)
                elif joystick.get_hat(0) == (-1, -1) or joystick.get_hat(0) == (0, -1) or joystick.get_hat(0) == (1, -1):
                        MVerticalValue = 1500-(400*throttle)
                else:
                        MVerticalValue = 1500
                        MHorizontalValue = 1500

                # Loops through each axis
                for a in range( numAxes-1 ):
                            
                        # throttle receives a percentage out of 100%
                        throttle = changeInterval(-joystick.get_axis(3), -1, 1, 0, 100)/100

                        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        #Band-Aid. Throttle will default at 0% instead of 50%.

                        if notMoved:
                                if throttle != .5:
                                        notMoved = False
                                else:
                                        throttle = 0
                                        
                        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        # Update Motor Values
                        
                        # Crab
                        if a == 0:
                                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500 - (400 * throttle), 1500 + (400 * throttle))
                                MHorizontalValue = valAxis

                        #Forward-Backward
                        elif a == 1: 
                                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500-(400*throttle), 1500+(400*throttle))
                                MLeftValue = valAxis
                                MRightValue = valAxis

                        # Yaw
                        elif a == 2:
                                yawChange = joystick.get_axis(a) # [-1 to 1]
                                yaw = yawChange * 200 * throttle # 200 can equal up to 400

                                # If MRightValue is Increasing
                                if yawChange < 0:
                                        if MRightValue+yaw > 1900:   # Checks to see if new MRightValue > 1900. If so, Offputs change to MLeftValue
                                                MRightValue = 1900
                                                MLeftValue = MLeftValue - yaw - (MRightValue+yaw) + 1900
                                        elif MRightValue-yaw < 1100: # Checks to see if new MLeftValue < 1100. If so, Offputs change to MRightValue
                                                MLeftValue = 1100
                                                MRightValue = MRightValue + yaw + (MLeftValue-yaw) - 1100
                                        else:
                                                MLeftValue = MLeftValue + yaw
                                                MRightValue = MRightValue - yaw
                                
                                # If MLeftValue is Increasing.
                                elif yawChange > 0:
                                        if MLeftValue+yaw > 1900:   # Checks to see if new MLeftValue > 1900. If so, Offputs change to MRightValue
                                                MLeftValue = 1900
                                                MRightValue = MRightValue - yaw - (MLeftValue+yaw) + 1900
                                        elif MRightValue-yaw < 1100: # Checks to see if new MRightValue < 1100. If so, Offputs change to MLeftValue
                                                MRightValue = 1100
                                                MLeftValue = MVerticalValue + yaw + (MRightValue-yaw) - 1100
                                        else:
                                                MLeftValue = MLeftValue + yaw
                                                MRightValue = MRightValue - yaw

                                  
        # If arduino is disconnected, try to reconnect
        else:
                if not arduinoConnected:
                        try:
                                connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected arduino (Connected to bottom left USB Port) and sets baudrate to 115200
                                arduino = ArduinoApi(connection = connection)
                                arduinoConnected = True
                                print("arduino Connected!")

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
                        except:
                                print("arduino Failed to Connect")
                              


        # If Camera is not connected, try to reconnect
        if not camConnected:
                try:
                        cam = pygame.camera.Camera("/dev/video0", ((640, 480))) # PSEYE Default Dimensions: (640,480)
                        cam.start()
                        print("Camera Connected!")
                        camConnected = True
                except:
                        pass

        # If no joysticks are detected, try to reconnect
        if not gamepadConnected and not joystickConnected:
                # Rescans connected joysticks
                pygame.joystick.quit()
                pygame.joystick.init()
                joystick_count = pygame.joystick.get_count()

                gamepadConnected = False
                joystickConnected = False
                for i in range(joystick_count):
                        if pygame.joystick.Joystick(i).get_name() == gamepadName:
                                gamepad = pygame.joystick.Joystick(i)
                                gamepad.init()
                                gamepadConnected = True
                                print("Gamepad Connected!")
                        elif pygame.joystick.Joystick(i).get_name() == joystickName:
                                joystick = pygame.joystick.Joystick(i)
                                joystick.init()
                                joystickConnected = True
                                print("Joystick Connected!")
                        else:
                                print("Unsupported Harware Ignored.")  
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""                
        # Round M_Values to Integers before processing.
        
        MLeftValue = int(MLeftValue)
        MRightValue = int(MRightValue)
        MVerticalValue = int(MVerticalValue)
        MHorizontalValue = int(MHorizontalValue)

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
clawUDPosition       = 90
clawGraspPosition    = 0  # May need to reverse
armLRPosition       = 90

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
