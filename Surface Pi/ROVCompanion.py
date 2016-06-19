import pygame
import socket
from time import sleep

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define Functions
 
def changeInterval(x, in_min, in_max, out_min, out_max):     # Inspired by the Arduino map() function
        return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up UDP (Treated as Client)


UDP_IP = "192.168.1.10"  # Static IP of Surface Pi
UDP_PORT = 5000          # Port of Surface Pi

server = ('192.168.1.11', 5001)  # IP & Port of Sub Pi (192.168.1.11)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Socket connection(IPv4, UDP)

binding = 1
while binding:
    try:
        sock.bind((UDP_IP, UDP_PORT))                            # Bind socket to IP & Port of the Surface Pi
        binding = 0
    except:
        "Binding"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Pygame Initializations

pygame.init()           # Initialize pygame
pygame.joystick.init()  # Initialize the Joystick library

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Classes


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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Used to set window dimensions (Should be fullscreen eventually)
display_width = 1825                       # 1208 (Home) 1825 (Hill) (Diff 640)
display_length = 953                        # 649  (Home) 953  (Hill) (Diff 360)
display_hyp = int((display_length**2 + display_width**2)**.5)  # Only used to set dimensions dependent on length and width.

# Create Clock object
clock = pygame.time.Clock()  # Will be used for FPS
 
# Window's Icon
icon = pygame.image.load('resources/Hill_Logo.png')

# TextBox Objects
motorTitleText      =TextBox(int(display_hyp*(40/1371)), int(display_width*(700/1208)), int(display_length*(50/649)))  # Title: "Motor Values"
valArmText          =TextBox(int(display_hyp*(40/1371)), int(display_width*(170/1208)), int(display_length*(400/649))) # Data: Arm Values
valuesText          =TextBox(int(display_hyp*(30/1371)), int(display_width*(700/1208)), int(display_length*(90/649)))  # Data: Motor Values

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Create Window

pygame.display.set_icon(icon)                                      # Sets Window's Icon
pygame.display.set_caption("True Companion App")           # Sets Window's Title
screen = pygame.display.set_mode((display_width, display_length))  # Creates Window/screen
screen.fill(GRAY)
clock.tick(60)                                                     # Sets FPS to 60
pygame.display.update()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Joystick & Gamepad Variables/Setup

# Define name of required hardware
joystickName = "Logitech Logitech Extreme 3D"

# Number of connected joysticks (Note: gamepads are considered joysticks)
joystick_count = pygame.joystick.get_count()  # (should = 1) 

# Find what joysticks are connected
joystickConnected = False
for i in range(joystick_count):
    if pygame.joystick.Joystick(i).get_name() == joystickName:
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joystickConnected = True
        print("Joystick Connected!")
    else:
        print("Unsupported Hardware")

""""""
# Band-Aid for Joystick's throttle defaulting at 50.

notMoved = True  # Checks to see if throttle has been moved from 0.
throttle = 0     # Define throttle to start at 0.

""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Data to be sent to ROV

# Define Motor Values at default (in mS).

universal_thruster_mid = 410
thruster_max           = 600
thruster_min           = 220
MLeftValue             = universal_thruster_mid
MRightValue            = universal_thruster_mid
MVerticalValue         = universal_thruster_mid

# Configure default servo pulse lengths
wrist_mid = 430  
wrist_max = 580
wrist_min = 280

claw_mid  = 335
claw_max  = 490
claw_min  = 200

arm_mid   = 410
arm_max   = 550
arm_min   = 270

cam_mid   = 365
cam_max   = 460
cam_min   = 280

# Write Servo's to Default
clawUDPosition    = wrist_mid
clawGraspPosition = claw_mid
camUDPosition     = cam_mid
armLRPosition     = arm_mid

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Data for Temperature ROV

sensorRequested = "0"

# Define Sensor Data at default
cTemp    = "??.??"
mDepth   = "??.??"
pressure = "??.??"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

running = True   # Main loop ends when this = False.
while running:
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Checks to see if the User has quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Reset Display

    # Reset Value TextBox's
    valuesText.reset()
    valArmText.reset()
    
    screen.fill(GRAY)  # Resets background to Gray

    # Display Title
    motorTitleText.Print(screen, "Motor Values:")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Presume Up & Right to be +1. May need to reverse on a case by case basis. """

    # Reads Joystick input

    if joystickConnected:
        numAxes = joystick.get_numaxes()  # Gets number of axis on Joystick

        # Checks each axis on the Joystick
        for a in range(numAxes - 1):

            # throttle = int([0%, 100%])
            throttle = changeInterval(-joystick.get_axis(3), -1, 1, 0, 100) / 100

            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            # Band-Aid to fix Throttle defaulting at 50%.

            if notMoved:
                if throttle != .5:
                    notMoved = False
                else:
                    throttle = 0

            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            # Update local Motor Values

            # Cam Up/Down
            if joystick.get_hat(0) == (-1, 1) or joystick.get_hat(0) == (0, 1) or joystick.get_hat(0) == (1, 1):
                if camUDPosition < cam_max:
                        camUDPosition += 1
            elif joystick.get_hat(0) == (-1, -1) or joystick.get_hat(0) == (0, -1) or joystick.get_hat(0) == (1, -1):
                if camUDPosition > cam_min:
                        camUDPosition -= 1

            # Forward-Backward
            if a == 1:
                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, universal_thruster_mid - int(256 * throttle), universal_thruster_mid + int(256 * throttle))
                MLeftValue  = valAxis
                MRightValue = valAxis

            # Yaw
            elif a == 2:
                yawChange = joystick.get_axis(a)  # [-1 to 1]
                yaw = yawChange * 128 * throttle  # 128 can equal up to 256

                # If MRightValue is Increasing
                if yawChange < 0:
                    if MRightValue + yaw > universal_thruster_mid+256:  # Checks to see if new MRightValue > value cap. If so, Offputs change to MLeftValue
                        MRightValue = universal_thruster_mid+256
                        MLeftValue = MLeftValue - yaw - (MRightValue + yaw) + universal_thruster_mid+256
                    elif MRightValue - yaw < universal_thruster_mid-256:  # Checks to see if new MLeftValue < minimum value cap. If so, Offputs change to MRightValue
                        MLeftValue = universal_thruster_mid-256
                        MRightValue = MRightValue + yaw + (MLeftValue - yaw) - universal_thruster_mid-256
                    else:
                        MLeftValue += yaw
                        MRightValue -= yaw

                # If MLeftValue is Increasing.
                elif yawChange > 0:
                    if MLeftValue + yaw > universal_thruster_mid+256:  # Checks to see if new MLeftValue > 1900. If so, Offputs change to MRightValue
                        MLeftValue = universal_thruster_mid+256
                        MRightValue = MRightValue - yaw - (MLeftValue + yaw) + universal_thruster_mid+256
                    elif MRightValue - yaw < universal_thruster_mid-256:  # Checks to see if new MRightValue < 1100. If so, Offputs change to MLeftValue
                        MRightValue = universal_thruster_mid-256
                        MLeftValue = MVerticalValue + yaw + (MRightValue - yaw) - universal_thruster_mid-256
                    else:
                        MLeftValue += yaw
                        MRightValue -= yaw

        vertRunning = True  # Used to test if the Vertical Motor buttons are being pressed.
        # Checks Button Values
        for b in range(9):
            
            # Thumb (2) Button
            if b == 1:  # Close Claw
                if joystick.get_button(b) == 1:
                    if clawGraspPosition < claw_max:
                        clawGraspPosition += 1

            # Trigger Button
            elif b == 0:  # Open Claw
                if joystick.get_button(b) == 1:
                    if clawGraspPosition > claw_min:
                        clawGraspPosition -= 1

            # 3 Button
            elif b == 2:  # Move Arm Right
                if joystick.get_button(b) == 1:
                    if armLRPosition < arm_max:
                        armLRPosition += 1

            # 6 Button
            elif b == 5:  # Move Wrist Down
                if joystick.get_button(b) == 1:
                    if clawUDPosition < wrist_max:
                        clawUDPosition += 1

            # 5 Button
            elif b == 4:  # Move Arm Left
                if joystick.get_button(b) == 1:
                    if armLRPosition > arm_min:
                        armLRPosition -= 1

            # 4 Button
            elif b == 3:   # Move Wrist Up
                if joystick.get_button(b) == 1:
                    if clawUDPosition > wrist_min:
                        clawUDPosition -= 1

            # 7 Button
            elif b == 6:  # Toggle Vertical Motor Negative
                if joystick.get_button(b) == 1:
                    MVerticalValue = universal_thruster_mid-(256*throttle)
                else:
                    vertRunning = False	 

            # 8 Button
            elif b == 7:  # Toggle Vertical Motor Positive
                if joystick.get_button(b) == 1:
                    MVerticalValue = universal_thruster_mid+(256*throttle)
                else:
                    if not vertRunning:
                        MVerticalValue = universal_thruster_mid

            # 11 Button
            elif b == 8 and sensorRequested == "0":  # Request Sensor Data
                if joystick.get_button(b+2) == 1:
                    sensorRequested = "1"

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # If no joysticks are detected, try to reconnect

    if not joystickConnected:
        # Rescans connected joysticks
        pygame.joystick.quit()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        joystickConnected = False
        for i in range(joystick_count):
            if pygame.joystick.Joystick(i).get_name() == joystickName:
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                joystickConnected = True
                print("Joystick Connected!")
            else:
                print("Unsupported Hardware Ignored.")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Prepare & send data to be sent to ROV
    
    # Cast Servos as strings
    strClawUDPosition    = str(int(clawUDPosition))
    strArmLRPosition     = str(int(armLRPosition))
    strClawGraspPosition = str(int(clawGraspPosition))
    strCamUDServo        = str(int(camUDPosition))

    # Data to be sent to ROV (28 bytes)
    sData = str(int(MLeftValue)) + str(int(MRightValue)) + str(int(MVerticalValue)) + strClawUDPosition + strArmLRPosition + strClawGraspPosition + strCamUDServo + sensorRequested
    sData = sData.encode('utf-8')
    
    sock.sendto(sData, server)  # Send the data to the ROV
    if not sensorRequested:
        sleep(1.2)
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive sensor data from the ROV
    
    rData, addr = sock.recvfrom(1024)
    rData = rData.decode('utf-8')

    if rData != "00000000000":
	    cTemp    = rData[:rData.index("_")]
	    mDepth   = rData[rData.index("_")+1:rData.index("$")]
	    pressure = rData[rData.index("$")+1:]
	    sensorRequested = "0"

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Update GUI

    # Sets throttle text's color to Red if at 0.
    if throttle == 0:
        valuesText.changeColor(RED)

    valuesText.Print(screen, "Throttle: " + str(int(throttle * 100)) + "%")
    valuesText.newLine()

    # Display Value of all motors
    if joystickConnected:

        # Display Left Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MLeftValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100

            valuesText.Print(screen, "Left Motor: " + str(tempStringNumVal) +"%")
            valuesText.newLine()
        except:
            valuesText.Print(screen, "Left Motor: 0%")
            valuesText.newLine()

        # Display Right Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MRightValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100

            valuesText.Print(screen, "Right Motor: " + str(tempStringNumVal) +"%")
            valuesText.newLine()
        except:
            valuesText.Print(screen, "Right Motor: 0%")
            valuesText.newLine()

        # Display Vertical Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MVerticalValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100


            valuesText.Print(screen, "Vertical Motor: " + str(tempStringNumVal) +"%")
            valuesText.newLine()
        except:
            valuesText.Print(screen, "Vertical Motor: 0%")
            valuesText.newLine()

            # Display Arm Values
            valuesText.changeColor(BLACK)

            # Display Arm
            valuesText.Print(screen, "Arm: "+ strArmLRPosition)
            valuesText.newLine()

            # Display Wrist
            valuesText.Print(screen, "Wrist: "+ strClawUDPosition)
            valuesText.newLine()

            # Display Claw
            valuesText.Print(screen, "Claw: "+ strClawGraspPosition)
            valuesText.newLine()

        # Display Sensor Values
        valuesText.Print(screen, "Temperature: "+ str(cTemp) + "°C")
        valuesText.newLine()
        valuesText.Print(screen, "Depth: "+ str(mDepth) + " Meters")
        valuesText.newLine()
        valuesText.Print(screen, "Pressure: "+ str(pressure) + " mbar")
        valuesText.newLine()
            
    else:
        if not joystickConnected:
            valuesText.changeColor(ORANGE)
            valuesText.Print(screen, "Joystick is DISCONNECTED")
            valuesText.newLine()
            valuesText.changeColor(BLACK)


    pygame.display.update()
    clock.tick(60)  # Sets FPS to 60

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

pygame.quit()
quit()
