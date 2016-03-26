""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Index:

# 1. Imports
# 2. Global Classes
# 3. Define GUI Variables
# 4. Create Window
# 5. Connect to arduino
# 6. Pygame Initializations
# 7. Joystick/Gamepad Variables & Setup
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

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
# Global Classes

class TextBox:  # Creates an object to work similarly to a text box.
        
        def __init__(self, size, x, y):
                self.color = BLACK
                self.x = x
                self.originalX = x
                self.y = y
                self.originalY = y
                
                self.size = size
                self.line_height = self.size*3/4
                self.font = pygame.font.Font(None, self.size)

        def Print(self, screen, textString):
                textBitmap = self.font.render(textString, True, self.color)
                screen.blit(textBitmap, [self.x, self.y])

        def newLine(self):
                self.y += self.line_height

        def changeColor(self, color):
                self.color = color
        
        def reset(self):
                self.x = self.originalX
                self.y = self.originalY
                self.line_height = self.size*3/4
                self.color = BLACK
        
        def indent(self, multiplier):
                self.x += (10*multiplier)

        def unindent(self,multiplier):
                self.x -= (10*multiplier)        

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define GUI Variables

# Define Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY  = (211, 211, 211)
RED   = (255, 0, 0)
ORANGE = (255, 165, 0)

# Used to set window dimensions
display_width  = 1208 # 1208 (Home) 1825 (Hill) (Diff 640)
display_length = 649  # 649  (Home) 953  (Hill) (Diff 360)

# Create Clock object
clock = pygame.time.Clock() # Will be used for FPS

# Window's Icon
icon = pygame.image.load('resources/Hill_Logo.png')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Create Window

pygame.display.set_icon(icon)                                     # Sets Window's Icon
screen = pygame.display.set_mode((display_width, display_length)) # Creates Window/screen
pygame.display.set_caption("The Hill ROV Companion App")          # Sets Window's Title

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
armExtensionServoPin = 2
clawUDServoPin       = 4
clawOCServoPin       = 7
camUDServoPin        = 8

# Connects to ESC's & Servos if arduino is connected
if arduinoConnected:
                motor1 = Servo(motorPin1)
                motor1.writeMicroseconds(1500)
                sleep(1)
                print("ESC1 Connected!")

                motor2 = Servo(motorPin2)
                motor2.writeMicroseconds(1500)
                sleep(1)
                print("ESC2 Connected!")

                motor3 = Servo(motorPin3)
                motor3.writeMicroseconds(1500)
                sleep(1)
                print("ESC3 Connected!")

                motor4 = Servo(motorPin4)
                motor4.writeMicroseconds(1500)
                sleep(1)
                print("ESC4 Connected!")

                armExtensionServo = Servo(armExtensionServoPin)
                clawUDServo       = Servo(clawUDServoPin)
                clawOCServo       = Servo(clawOCServoPin)
                camUDServo        = Servo(camUDServoPin)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Pygame Initializations

pygame.init()                                # Initialize pygame
pygame.joystick.init()                       # Initialize the Joystick library
pygame.camera.init()                         # Initialize the Camera library

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Joystick/Gamepad Variables & Setup

# Define name of required hardware
gamepadName = "Sony PLAYSTATION(R)3 Controller"
joystickName = "Logitech Logitech Extreme 3D"

# Number of connected joysticks (Note: gamepads are considered joysticks)
joystick_count = pygame.joystick.get_count()  # (should = 2) 

# Find what joysticks are connected
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
        print("Unsupported Harware.")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global Variables for Main Loop

""""""
# TextBox Objects
motorTitleText      =TextBox(40, 700, 50)  # Title: "Motor Values"
sensTitleText       =TextBox(40, 10, 481)  # Title: "Sensor Values"
gamepadReminderText =TextBox(20, 1, 395)   # Reminder: Reminds user to mash playstation button after reconnect
valArmText          =TextBox(40, 170, 400) # Data: Arm Values
valMotorsText       =TextBox(30, 700, 90)  # Data: Motor Values
camDisconnectedText =TextBox(40, 10, 10)   # Disconnect: Warns that Camera is Disconnected

# Changes Color of certain TextBoxs
gamepadReminderText.changeColor(RED)
camDisconnectedText.changeColor(RED)

""""""

running = True   # Checks to see if the program is still running. Set False by quiting.

""""""
# Band-Aid for throttle. 
notMoved = True  # Checks to see if throttle has been moved from 0.
throttle = 0     # Define throttle to start at 0.

""""""
# Gamepad Variables

# Used to check if gamepad has been disconnected.
if gamepadConnected:
        a23 = gamepad.get_axis(23)
        a24 = gamepad.get_axis(24)
        a25 = gamepad.get_axis(25)
else:
        a23 = 0
        a24 = 0
        a25 = 0


checkCount = 0 # Counts to 50 to see if ps3 axes 23-25 are equal all 50 times.

# Arm variables
extendingCount = 0   # Counts to 50 to allow the arm enough time to withdraw/extend
extensionWait = 450  # UNTESTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
armExtended = False  # The program starts with the arm withdrawn

""""""
# Screenshot Variables

screenshotsLeft   = []   # Both used to store screenshots
screenshotsRight  = []   # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

screenshotLeft    = None # Holds the screenshot to be displayed on the Left
screenshotRight   = None # Holds the screenshot to be displayed on the Right

ssWaitL           = 0    # Waits for X counts before next screenshot
ssWaitR           = 0    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

squareWait        = 0  # Waits for X counts before next button use
circleWait        = 0  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


ssDisplayedIndexL = 0    # Stores index of screenshotsLeft being displayed
ssDisplayedIndexR = 0    # Stores index of screenshotsRight being displayed

""""""
# Define Motor Values at default (in mS).

M1Value = 1500
M2Value = 1500
M3Value = 1500
M4Value = 1500

""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Write Servo's to Default
"""Note: Values may be REVERSED!!!"""

clawUDPosition     = 90
clawOCPosition     = 0   # May need to reverse
camUDPosition      = 90

armExtensionServo.write(180) # May need to Reverse
clawUDServo.write(clawUDPosition)
clawOCServo.write(clawOCPosition) 
camUDServo.write(camUDPosition)

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

        # Reset TextBox's
        valMotorsText.reset()
        valArmText.reset()

        screen.fill(GRAY) # Reset Screen to grey

        # Attemp to Display Video Feed
        if camConnected:
                screen.blit(pygame.transform.scale(cam.get_image(), (524,393)), (0,0))
        else:
                camDisconnectedText.Print(screen, "CAMERA DISCONNECTED.")

        # Displays screenshots
        pygame.draw.rect(screen, ORANGE,(535, 399, 673, 250))
        if screenshotLeft != None:
                screen.blit(pygame.transform.scale(screenshotLeft, (320,240)), (548, 409)) # 523
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
                for b in range(0, 12):
                        # Select Button
                        if b == 0: # Withdraw Arm
                                pressed = gamepad.get_button(b)
                                if extendingCount != 0:
                                       pressed = 1 
                                if pressed == 1: 
                                        if extendingCount != 0:
                                                armExtended = False

                                                # Reset arm servos to default
                                                clawUDPosition     = 90
                                                clawOCPosition     = 0   # May need to reverse
                                                clawUDServo.write(clawUDPosition)
                                                clawOCServo.write(clawOCPosition) # May need to reverse

                                                armExtensionServo.write(180) # May need to Reverse Value

                                        # Attempt to wait for arm withdraw(WAIT TIME UNTESTED!!!)
                                        if extendingCount < extensionWait:
                                                extendingCount += 1
                                                break
                                        else:
                                                extendingCount = 0

                        # Start Button
                        elif b == 3: # Extend Arm
                                pressed = gamepad.get_button(b) == 1
                                if extendingCount != 0:
                                        pressed = 1
                                if pressed == 1:
                                        if extendingCount != 0:
                                                armExtended = True
                                                armExtensionServo.write(0) # May need to Reverse value

                                        if extendingCount < extensionWait:
                                                extendingCount += 1
                                                break
                                        else:
                                                extendingCount = 0
                                
                        # Up on D-pad
                        elif b == 4 and armExtended: # Tilt Claw Up
                                if gamepad.get_button(b) == 1:
                                                if clawUDPosition < 180:
                                                        clawUDPosition+=1
                                                        clawUDServo.write(clawUDPosition) 

                        # Down on D-pad
                        elif b == 6 and armExtended:  # Tilt Claw Down
                                if gamepad.get_button(b) == 1:
                                                if clawUDPosition > 0:        
                                                        clawUDPosition-=1
                                                        clawUDServo.write(clawUDPosition) 

                        # Left Bumper
                        elif b == 8 and armExtended:  # Open Claw
                                if gamepad.get_button(b) == 1:
                                                if clawOCPosition > 0:
                                                        clawOCPosition-=1
                                                        clawOCServo.write(clawOCPosition) 

                        # Right Bumper
                        elif b == 9 and armExtended:  # Close Claw
                                if gamepad.get_button(b) == 1:
                                        if clawOCPosition < 180:
                                                        clawOCPosition+=1
                                                        clawOCServo.write(clawOCPosition)

                # Camera Related Buttons. Tracked seperately from arm servos
                for b in range(1, 3):
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
                                
                for b in range(12, 16):
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

                # Check motion tracker to see if controller is disconnected.
                OGa23 = a23
                OGa24 = a24
                OGa25 = a25
                
                a23 = gamepad.get_axis(23)
                a24 = gamepad.get_axis(24)
                a25 = gamepad.get_axis(25)
                
                if OGa23==a23 and OGa24==a24 and OGa25==a25:
                        checkCount += 1
                else:
                        checkCount = 0
                if OGa23==a23 and OGa24==a24 and OGa25==a25 and checkCount == 100:
                        gamepadConnected=False
                        checkCount = 0
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Reads Joystick input if Joystick and Ardunio are both connected.

        if joystickConnected and arduinoConnected:

                numAxes = joystick.get_numaxes() # Gets number of axis on Joystick

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
                        
                        # Left-Right
                        if a == 0:
                              pass # Not Yet Written  

                        #Forward-Backward
                        elif a == 1: 
                                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500-(400*throttle), 1500+(400*throttle))
                                M1Value = valAxis
                                M2Value = valAxis

                        # Yaw
                        elif a == 2:
                                yawChange = changeInterval(joystick.get_axis(a), -1, 1, -50, 50)/100 # Remaps Yaw's interval from [-1, 1] to [-50, 50]%

                                # Backwards Yaw BROKEN! 
                                if yawChange != 25: #Not Neccessary, but it saves the program from running the following code.
                                        if yawChange > 0: 
                                                if M1Value < 1500:   # If in Reverse (Broken)
                                                        M1Value = M1Value - (400*throttle*yawChange)
                                                elif M1Value > 1500: # If Forward
                                                        M1Value = M1Value + (400*throttle*yawChange)
                                                else:                # If not moving forward/Backward
                                                        M1Value = 1500+200*throttle/100
                                                        M2Value = 1500-200*throttle/100
                                        elif yawChange < 0:          
                                                if M2Value < 1500:   # If in Reverse (Broken)
                                                        M2Value = M2Value + (400*throttle*yawChange)
                                                elif M2Value > 1500: # If Forward
                                                        M2Value = M2Value - (400*throttle*yawChange)
                                                else:                # If not moving forward/Backward
                                                         M1Value = 1500-200*throttle
                                                         M2Value = 1500+200*throttle

                # Up/Down
                if joystick.get_hat(0) == (0, 1):
                        M3Value = 1500+(400*throttle)
                        M4Value = 1500+(400*throttle)
                elif joystick.get_hat(0) == (0, -1):
                        M3Value = 1500-(400*throttle)
                        M4Value = 1500-(400*throttle)

                                  
        # If arduino is disconnected, try to reconnect
        else:
                if not arduinoConnected:
                        try:
                                connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected arduino (Connected to bottom left USB Port) and sets baudrate to 115200
                                arduino = ArduinoApi(connection = connection)
                                arduinoConnected = True
                                print("arduino Connected!")

                                motor1 = Servo(motorPin1)
                                motor1.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC1 Connected!")

                                motor2 = Servo(motorPin2)
                                motor2.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC2 Connected!")

                                motor3 = Servo(motorPin3)
                                motor3.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC3 Connected!")

                                motor4 = Servo(motorPin4)
                                motor4.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC4 Connected!")

                                armExtensionServo = Servo(armExtensionServoPin)
                                clawUDServo       = Servo(clawUDServoPin)
                                clawOCServo       = Servo(clawOCServoPin)
                                camUDServo        = Servo(camUDServoPin)
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
        # Update GUI        

        # Sets throttle text's color to Red if at 0.
        if throttle == 0:
                valMotorsText.changeColor(RED)

        valMotorsText.Print(screen, "Throttle: " + str(throttle))
        valMotorsText.newLine()

        # Display Value of all motors
        if joystickConnected and arduinoConnected:
                valMotorsText.Print(screen, "Motor 1: " + str(M1Value))
                valMotorsText.newLine()

                valMotorsText.Print(screen, "Motor 2: " + str(M2Value))
                valMotorsText.newLine()
                
                valMotorsText.Print(screen, "Motor 3: " + str(M3Value))
                valMotorsText.newLine()

                valMotorsText.Print(screen, "Motor 4: " + str(M4Value))
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

        # Limits to motorMax & MotorMin
        if arduinoConnected:
                if M1Value > 1500:
                        motor1.writeMicroseconds(min(M1Value, motorMax))
                elif M1Value < 1500:
                        motor1.writeMicroseconds(max(M1Value, motorMin))
                                
                if M2Value > 1500:
                        motor2.writeMicroseconds(min(M2Value, motorMax))
                elif M2Value < 1500:
                        motor2.writeMicroseconds(max(M2Value, motorMin))

                if M3Value > 1500:
                        motor3.writeMicroseconds(min(M3Value, motorMax))
                elif M3Value < 1500:
                        motor3.writeMicroseconds(max(M3Value, motorMin))

                if M4Value > 1500:
                        motor4.writeMicroseconds(min(M4Value, motorMax))
                elif M4Value < 1500:
                        motor4.writeMicroseconds(max(M4Value, motorMin)) 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

# Reset arm Servos to default
clawUDPosition     = 90
clawOCPosition     = 0            # May need to reverse
clawUDServo.write(clawUDPosition)
clawOCServo.write(clawOCPosition) # May need to reverse
armExtensionServo.write(180) # May need to Reverse Value

# Reset Camera Servo to Default
camUDPosition= 90
camUDServo.write(camUDPosition)

pygame.quit()
quit()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Known Issues

"""

- Once Connected, joystick, camera, & arduino can not be reconnected.
- Motors algorithms suck. Fix them.

"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
