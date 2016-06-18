import pygame
import socket
from time import sleep

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define Functions
 
def changeInterval(x, in_min, in_max, out_min, out_max):     # Identical to Arduino map() function
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
sensTitleText       =TextBox(int(display_hyp*(40/1371)), int(display_width*(10/1208)),  int(display_length*(481/649))) # Title: "Sensor Values"
gamepadReminderText =TextBox(int(display_hyp*(20/1371)), int(display_width*(1/1208)),   int(display_length*(395/649))) # Reminder: Reminds user to mash playstation button after reconnect
valArmText          =TextBox(int(display_hyp*(40/1371)), int(display_width*(170/1208)), int(display_length*(400/649))) # Data: Arm Values
valMotorsText       =TextBox(int(display_hyp*(30/1371)), int(display_width*(700/1208)), int(display_length*(90/649)))  # Data: Motor Values
camDisconnectedText =TextBox(int(display_hyp*(40/1371)), int(display_width*(10/1208)),  int(display_length*(10/649)))  # Disconnect: Warns that Camera is Disconnected

# Changes Color of certain TextBoxes
gamepadReminderText.changeColor(RED)
camDisconnectedText.changeColor(RED)

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
        print("Unsupported Hardware")

""""""
# Band-Aid for Joystick's throttle defaulting at 50.

notMoved = True  # Checks to see if throttle has been moved from 0.
throttle = 0     # Define throttle to start at 0.

""""""
# Used to check if gamepad has been disconnected.

disconnectingCount = 0  # Counts to 50 to see if ps3 axes 23-25 are equal all 50 times.

if gamepadConnected:
    a23 = gamepad.get_axis(23)
    a24 = gamepad.get_axis(24)
    a25 = gamepad.get_axis(25)
else:
    a23 = 0
    a24 = 0
    a25 = 0

running = True   # Main loop ends when this = False.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Data to be sent to ROV

# Define Motor Values at default (in mS).
MLeftValue = 410
MRightValue = 410
MVerticalValue = 410
MHorizontalValue = 410

# Configure default servo pulse lengths
wrist_mid   = 430  
wrist_plus  = 580
wrist_minus = 280

claw_mid  = 335
claw_plus = 420
claw_minus = 250

arm_mid   = 410
arm_plus  = 550
arm_minus = 270

cam_max   = 430  # +-128 (Real cam mid, but treated like max)
cam_min   = 300
cam_mid   = 365

# Write Servo's to Default
clawUDPosition    = wrist_mid
clawGraspPosition = claw_mid
camUDPosition     = cam_mid
armLRPosition     = arm_mid

universal_thruster_mid = 410

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Data for Temperature ROV

sensorRequested = "0"

# Define Sensor Data at default
temperatureVal = 0.0
depthVal = 0.0

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
    
    screen.fill(GRAY)  # Resets background to Gray

    # Display Titles
    motorTitleText.Print(screen, "Motor Values:")
    sensTitleText.Print(screen, "Sensor Values:")
    gamepadReminderText.Print(screen, "Mash <Playstation Button> after Reconnect!")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Presume Up & Right to be +1. May need to reverse on a case by case basis. """

    if gamepadConnected:
        for b in [3, 4, 5, 6, 7, 8, 9, 12, 14]:  # Checks for all arm related servo value changes

            # Start Button
            if b == 3:
                if gamepad.get_button(b) == 3:
                    sensorRequested = "1"


            # Down on D-pad
            if b == 6:   # Move Wrist Up
                if gamepad.get_button(b) == 1:
                    if clawUDPosition >= wrist_minus:
                        clawUDPosition -= 1

            # Up on D-pad
            elif b == 4:  # Move Wrist Down
                if gamepad.get_button(b) == 1:
                    if clawUDPosition <= wrist_plus:
                        clawUDPosition += 1

            # Left on D-pad
            elif b == 7:  # Move Arm Left
                if gamepad.get_button(b) == 1:
                    if armLRPosition >= arm_minus:
                        armLRPosition -= 1

            # Right on D-pad
            elif b == 5:  # Move Arm Right
                if gamepad.get_button(b) == 1:
                    if armLRPosition <= arm_plus:
                        armLRPosition += 1

            # Left Trigger
            elif b == 8:  # Close Claw
                if gamepad.get_button(b) == 1:
                    if clawGraspPosition <= claw_plus:
                        clawGraspPosition += 1

            # Right Trigger
            elif b == 9:  # Open Claw
                if gamepad.get_button(b) == 1:
                    if clawGraspPosition >= claw_minus:
                        clawGraspPosition -= 1

            # Triangle Button
            if b == 12:  # Move Camera Servo Up
                if gamepad.get_button(b) == 1:
                    if camUDPosition <= cam_max:
                        camUDPosition += 1

            # X Button
            elif b == 14:  # Move Camera Servo Down
                if gamepad.get_button(b) == 1:
                    if camUDPosition >= cam_min:
                        camUDPosition -= 1

        # Check motion tracker to see if gamepad is disconnected.
        OGa23 = a23
        OGa24 = a24
        OGa25 = a25

        a23 = gamepad.get_axis(23)
        a24 = gamepad.get_axis(24)
        a25 = gamepad.get_axis(25)
        if OGa23 == a23 and OGa24 == a24 and OGa25 == a25:
            disconnectingCount += 1
            if disconnectingCount == 100:
                gamepadConnected = False
                disconnectingCount = 0
        else:
            disconnectingCount = 0

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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

            # Up/Down
            if joystick.get_hat(0) == (-1, 1) or joystick.get_hat(0) == (0, 1) or joystick.get_hat(0) == (1, 1):
                MVerticalValue = universal_thruster_mid + (256 * throttle)
            elif joystick.get_hat(0) == (-1, -1) or joystick.get_hat(0) == (0, -1) or joystick.get_hat(0) == (1, -1):
                MVerticalValue = universal_thruster_mid - (256 * throttle)
            else:
                MVerticalValue = universal_thruster_mid

            # Forward-Backward
            if a == 1:
                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, universal_thruster_mid - (256 * throttle), universal_thruster_mid + (256 * throttle))
                MLeftValue = valAxis
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

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
                print("Unsupported Hardware Ignored.")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Prepare & send data to be sent to ROV
    
    # Cast Servos as strings
    strClawUDPosition    = str(int(clawUDPosition))
    strArmLRPosition     = str(int(armLRPosition))
    strClawGraspPosition = str(int(clawGraspPosition))
    strCamUDServo        = str(int(camUDPosition))
        
    # Data to be sent to ROV (28 bytes)
    sData = str(int(MLeftValue)) + str(int(MRightValue)) + str(int(MVerticalValue)) + str(int(MHorizontalValue)) + strClawUDPosition + strArmLRPosition + strClawGraspPosition + strCamUDServo + sensorRequested
    sData = sData.encode('utf-8')
    
    sock.sendto(sData, server)  # Send the data to the ROV
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive sensor data from the ROV
    
    rData, addr = sock.recvfrom(1024)
    rData = rData.decode('utf-8')
    
    # INCOMPLETE, NEED TO RECEIVE DATA 1st, THEN TRANSLATE AND SET
    # Translate data received & Set Sensor Values
    temperatureVal = 0.0 
    depthVal = 0.0
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Update GUI

    # Sets throttle text's color to Red if at 0.
    if throttle == 0:
        valMotorsText.changeColor(RED)

    valMotorsText.Print(screen, "Throttle: " + str(int(throttle * 100)) + "%")
    valMotorsText.newLine()

    # Display Value of all motors
    if joystickConnected:

        # Display Left Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MLeftValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100

            valMotorsText.Print(screen, "Left Motor: " + str(tempStringNumVal) +"%")
            valMotorsText.newLine()
        except:
            valMotorsText.Print(screen, "Left Motor: 0%")
            valMotorsText.newLine()

        # Display Right Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MRightValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100

            valMotorsText.Print(screen, "Right Motor: " + str(tempStringNumVal) +"%")
            valMotorsText.newLine()
        except:
            valMotorsText.Print(screen, "Right Motor: 0%")
            valMotorsText.newLine()

        # Display Vertical Motor Vector Speed
        try:
            tempStringNumVal = changeInterval(MVerticalValue, (universal_thruster_mid - (256 * throttle)), (universal_thruster_mid + (256 * throttle)), -100, 100)
            if tempStringNumVal > 100:
                tempStringNumVal = 100
            elif tempStringNumVal < -100:
                tempStringNumVal = -100


            valMotorsText.Print(screen, "Vertical Motor: " + str(tempStringNumVal) +"%")
            valMotorsText.newLine()
        except:
            valMotorsText.Print(screen, "Vertical Motor: 0%")
            valMotorsText.newLine()

        # Display Arm Values
        if gamepadConnected:
            valMotorsText.changeColor(BLACK)

            # Display Arm
            valMotorsText.Print(screen, "Arm: "+ strArmLRPosition)
            valMotorsText.newLine()

            # Display Wrist
            valMotorsText.Print(screen, "Wrist: "+ strClawUDPosition)
            valMotorsText.newLine()

            # Display Claw
            valMotorsText.Print(screen, "Claw: "+ strClawGraspPosition)
            valMotorsText.newLine()
            
    else:
        if not joystickConnected:
            valMotorsText.changeColor(RED)
            valMotorsText.Print(screen, "Joystick is DISCONNECTED")
            valMotorsText.newLine()
            valMotorsText.changeColor(BLACK)

    


    pygame.display.update()
    clock.tick(60)  # Sets FPS to 60

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

pygame.quit()
quit()
