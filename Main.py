""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Index:

# 1. Imports
# 2. Global Classes
# 3. Pygame Initializations
# 4. Define GUI Variables
# 5. Create Display Window
# 6. Connect to Hardware
# 7. Global Variables for Main Loop
# 8. Main Loop
# 9. Quit

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
# Pygame Initializations

pygame.init()                                # Initialize pygame
pygame.joystick.init()                       # Initialize the Joystick library
pygame.camera.init()                         # Initialize the Camera library
  
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define GUI Variables

# Define Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (211, 211, 211)
RED =  (255, 0, 0)

# Used to set window dimensions
display_width = 1000
display_length = 650

# Create Clock object
clock = pygame.time.Clock() # Will be used for FPS

# Window's Icon
icon = pygame.image.load('resources/Hill_Logo.png')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Create Display Window

pygame.display.set_icon(icon)                                     # Sets Window's Icon
screen = pygame.display.set_mode((display_width, display_length)) # Creates Window/screen
pygame.display.set_caption("The Hill ROV Companion App")          # Sets Window's Title

# Attempts to connect to Camera
camConnected = True
try:
        cam = pygame.camera.Camera("/dev/video0", ((640, 480))) # PSEYE Default Dimesnsions: (640,480)
        cam.start()
        print("Camera Connected!")
except:
        print("Camera Failed to Connect")
        camConnected = False
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Connect to Hardware

# Attempts to connect to Arduino
arduinoConnected = False
try:
        connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected Arduino (Connected to bottom left USB Port) and sets baudrate to 115200
        arduino = ArduinoApi(connection = connection)
        arduinoConnected = True
        print("Arduino Connected!")
except:
        print("Arduino Failed to Connect")

# Defines Hardware Pins
servoPin1 = 6
servoPin2 = 9
servoPin3 = 10
servoPin4 = 11

# Attempts to connect to ESC's if Arduino is connected
if arduinoConnected:
                motor1 = Servo(servoPin1)
                motor1.writeMicroseconds(1500)
                sleep(1)
                print("ESC1 Connected!")

                motor2 = Servo(servoPin2)
                motor2.writeMicroseconds(1500)
                sleep(1)
                print("ESC2 Connected!")

                motor3 = Servo(servoPin3)
                motor3.writeMicroseconds(1500)
                sleep(1)
                print("ESC3 Connected!")

                motor4 = Servo(servoPin4)
                motor4.writeMicroseconds(1500)
                sleep(1)
                print("ESC4 Connected!")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global Variables for Main Loop

# TextBox Objects
motorTitleText = TextBox(40, 700, 50)     # Title: "Motor Values"
sensTitleText = TextBox(40, 10, 481)      # Title: "Sensor Values"
valMotorsText = TextBox(30, 700, 90)       # Data: Motor Values
camDisconnectedText = TextBox(40, 10, 10) # Warning: Warns that Camera is Disconnected
camDisconnectedText.changeColor(RED)

running = True   # Checks to see if the program has been quit
notMoved = True  # Band-Aid for throttle. Used to see if the throttle has been moved from 0

# Count Variables (Will probably be removed on final version)
joystick_count = pygame.joystick.get_count()  # Number of connected joysticks (should = 2) 

# Define throttle to start at 0
throttle = 0

# Define Motor Values (in mS). Defaults at stopped position.
M1Value = 1500
M2Value = 1500
M3Value = 1500
M4Value = 1500

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

while running:
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Checks to see if the User has quit
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                       
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Reset Display to Default (gray background, Titles, and Camera Feed)

        valMotorsText.reset() # Resets valMotorText
        screen.fill(GRAY)   # Resets Screen to gray

        # Attemp to Display Video Feed
        if camConnected:
                screen.blit(cam.get_image(), (0,0))
        else:
                camDisconnectedText.Print(screen, "CAMERA DISCONNECTED.")

        # Display Titles
        motorTitleText.Print(screen, "Motor Values:")
        sensTitleText.Print(screen, "Sensor Values:")

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # For every attatched Joystick:
        if joystick_count != 0 and arduinoConnected:
                for i in range(joystick_count):
                        joystick = pygame.joystick.Joystick(i)
                        joystick.init()
                        """"""""""""""""""""""""
                        
                        numAxes = joystick.get_numaxes() # Gets number of axis

                        # Converts axis values to proper interval and sends them to Motors.
                        for a in range( numAxes-1 ):
                                    
                                # Finds throttle and assigns valAxis its value.
                                throttle = changeInterval(-joystick.get_axis(3), -1, 1, 0, 100)/100 # Remaps Throttle's interval from [-1, 1] to [0, 100]%

                                """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                #Band-Aid to fix Throttle Defaulting at 50.

                                if notMoved:
                                        if throttle != .5:
                                                notMoved = False
                                        else:
                                                throttle = 0
                                                
                                """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                # Updating Motor Values
                                
                                # Left-Right
                                if a == 0:
                                      pass #temp  

                                #Forward-Backward
                                elif a == 1:
                                        # Write valAxis (in mS), to the Motor Servos
                                        valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500-(400*throttle), 1500+(400*throttle))  # Maps Axis from [-1,1] to [1100, 1900] (Given Full Throttle)

                                        M1Value = valAxis
                                        M2Value = valAxis

                                # Yaw (now treated as a modifier)
                                elif a == 2:
                                        yawChange = changeInterval(joystick.get_axis(a), -1, 1, -50, 50)/100 # Remaps Yaw's interval from [-1, 1] to [-50, 50]%

                                        # Backwards yaw is all fucked up! 
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
                        """# Hat Button                        
                        for i in range(hat_count):
                                hat = joystick.gethat(i)

                                # Up/Down
                                if hat == (0, 1):
                                        M3Value = 1500+(400*throttle)
                                        M4Value = 1500+(400*throttle)
                                elif hat == (0, -1):
                                        M3Value = 1500-(400*throttle)
                                        M4Value = 1500-(400*throttle)"""
                                                
# Tries to connect to unconnected hardware
        else:
                # If Arduino is not connected, tries to connect (and connects to ESC's).
                if not arduinoConnected:
                        try:
                                connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected Arduino (Connected to bottom left USB Port) and sets baudrate to 115200
                                arduino = ArduinoApi(connection = connection)
                                arduinoConnected = True
                                print("Arduino Connected!")

                                motor1 = Servo(servoPin1)
                                motor1.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC1 Connected!")

                                motor2 = Servo(servoPin2)
                                motor2.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC2 Connected!")

                                motor3 = Servo(servoPin3)
                                motor3.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC3 Connected!")

                                motor4 = Servo(servoPin4)
                                motor4.writeMicroseconds(1500)
                                sleep(1)
                                print("ESC4 Connected!")
                        except:
                                print("Arduino Failed to Connect")
                              
                # If no Joysticks are connected, tries to connect.
                if joystick_count == 0:
                        joystick_count = pygame.joystick.get_count() # Number of connected joysticks (should = 1)
                        if joystick_count != 0:
                                hat__count = joystick.get_numhats()  # Number of hats found (should = 1)

        # Attempt to Connect to Camera
        if not camConnected:
                try:
                        cam = pygame.camera.Camera("/dev/video0", ((640, 480))) # PSEYE Default Dimensions: (640,480)
                        cam.start()
                        print("Camera Connected!")
                        camConnected = True
                except:
                        pass
                        
                        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Update GUI        

        # Sets throttle text's color to Red if at 0.
        if throttle == 0:
                valMotorsText.changeColor(RED)

        valMotorsText.Print(screen, "Throttle: " + str(throttle))
        valMotorsText.newLine()

        # Display Value of all motors
        if joystick_count != 0 and arduinoConnected:
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
                        valMotorsText.Print(screen, "Arduino is DISCONNECTED")
                        valMotorsText.newLine()
                        valMotorsText.changeColor(BLACK)
                if joystick_count == 0:
                        valMotorsText.changeColor(RED)
                        valMotorsText.Print(screen, "Joystick is DISCONNECTED")
                        valMotorsText.newLine()
                        valMotorsText.changeColor(BLACK)
                        

        pygame.display.update()
        clock.tick(60) # Sets FPS = 60

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # Write to motors

        # Motor's set Max & Min values 
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

pygame.quit()
quit()
