import pygame                                         # Used in conjunction with USB Joystick (Could also be used to create a UI)                             
import pygame.camera                                  # Experimental 
from nanpy import (ArduinoApi, SerialManager, Servo, wire)  # Arduino Api & Libraries for slavery
from time import sleep                                # Used for time.sleep() function
from ROVFunctions import changeInterval
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global FUNCTIONS


""" COMMENTED OUT TO TEST ROVFunctions Module
def changeInterval(x, in_min, in_max, out_min, out_max):     # Identical to Arduino map() function
        return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )
"""


def detectArduino():
        # Create TextBox object to display connection status
        connectingText = TextBox(40, display_width/2, display_length/2)
        connectingText.changeColor(WHITE)

        connected = False
        failed = 0
        
        while not connected:
                # Checks to see if the User has quit
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                                       
                try:
                        connection = SerialManager(device='/dev/ttyACM0', baudrate=115200)  # Finds the connected Arduino (Connected to bottom left USB Port) and sets baudrate to 9600
                        arduino = ArduinoApi(connection = connection)
                        connected = True
                        screen.fill(BLACK)
                        connectingText.print(screen, "Arduino Connected!")
                        pygame.display.update()
                except:
                        if failed == 0:
                                connectingText.print(screen, "Failed to connect to Arduino")
                                pygame.display.update()
                                sleep(1)
                                screen.fill(BLACK)
                                failed += 1
                        else:
                                screen.fill(BLACK)
                                connectingText.print(screen, "Attempting to Connect to Arduino.")
                                pygame.display.update()
                                sleep(.5)
                                        
                                screen.fill(BLACK)
                                connectingText.print(screen, "Attempting to Connect to Arduino..")
                                pygame.display.update()
                                sleep(.5)

                                screen.fill(BLACK)
                                connectingText.print(screen, "Attempting to Connect to Arduino...")
                                pygame.display.update()
                                sleep(.5)

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

        def print(self, screen, textString):
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
icon = pygame.image.load('resources\Hill_Logo.png')

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Create Display Window

pygame.display.set_icon(icon)                                     # Sets Window's Icon
screen = pygame.display.set_mode((display_width, display_length)) # Creates Window/screen
pygame.display.set_caption("The Hill ROV Companion App")          # Sets Window's Title

# Finds and activates Camera
cam = pygame.camera.Camera("/dev/video0", ((640, 480))) # PSEYE Default Dimesnsions: (640,480)
cam.start()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Connect to Hardware

# Hardware Pins
servoPin1 = 10
servoPin2 = 9

# Connect to Arduino
detectArduino()

# Connect to ESC 1
motor1 = Servo(servoPin1)
motor1.writeMicroseconds(1500)
arduino.delay(1000)

# Connect to ESC 2
motor2 = Servo(servoPin2)                
motor2.writeMicroseconds(1500)
arduino.delay(1000)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Global Variables for Main Loop

# TextBox Objects
motorTitleText = TextBox(40, 700, 50) # Title: "Joystick"
sensTitleText = TextBox(40, 0, 481) # Title: "Sensor"
valAxesText = TextBox(30, 700, 90)  # Data: Motor Values

running = True   # Checks to see if the program has been quit
notMoved = True  # Band-Aid for throttle. Used to see if the throttle has been moved from 0

# Count Variables (Will probably be removed on final version)
joystick_count = pygame.joystick.get_count() # Number of connected joysticks (should = 1)
hat__count = joystick.get_numhats()          # Number of hats found (should = 1)

# Motor's set Max & Min values 
motorMax = 1700
motorMin = 1300

# Motor Values (in mS). Default at stopped position.
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

        valAxesText.reset() # Resets valAxesText
        screen.fill(GRAY)   # Resets Screen to gray

        # Display Video Feed
        camFeed = cam.get_image() 
        screen.blit(camFeed, (0,0))

        # Display Titles
        motorTitleText.print(screen, "Motor Values:")
        sensTitleText.print(screen, "Sensor Values:")

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # For every attatched Joystick:
        
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
                # Hat Button                        
                for i in range(hat_count):
                        hat = joystick.gethat(i)

                        # Up/Down
                        if hat == (0, 1):
                                M3Value = 1500+(400*throttle)
                                M4Value = 1500+(400*throttle)
                        elif hat == (0, -1):
                                M3Value = 1500-(400*throttle)
                                M4Value = 1500-(400*throttle)
                
                """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                # Update GUI        

                if throttle == 0:
                        valAxesText.changeColor(RED)

                valAxesText.print(screen, "Throttle: " + str(throttle))
                valAxesText.newLine()

                valAxesText.print(screen, "Motor 1: " + str(M1Value))
                valAxesText.newLine()

                valAxesText.print(screen, "Motor 2: " + str(M2Value))
                valAxesText.newLine()

                valAxesText.print(screen, "Motor 3: " + str(M3Value))
                valAxesText.newLine()

                valAxesText.print(screen, "Motor 4: " + str(M4Value))
                valAxesText.newLine()

                pygame.display.update()
                clock.tick(60) # May Change, set FPS = 60

                #motor1.setValue(M1Value)
                #motor2.setValue(M2Value)
                if M1Value > 1500:
                        motor1.writeMicroseconds(min(M1Value, motorMax))
                else:
                        motor2.writeMicroseconds(max(M2Value, motorMin))

                      
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
pygame.quit()
quit()
