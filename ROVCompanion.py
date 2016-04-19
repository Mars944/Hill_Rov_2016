import pygame
import pygame.camera
import socket
from time import sleep

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up UDP (Treated as Client)

UDP_IP = "192.168.1.10"  # Static IP of Surface Pi
UDP_PORT = 5001          # Port of Surface Pi

server = ('192.168.1.11', 5000)  # IP & Port of Sub Pi

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Socket connection(IPv4, UDP)
sock.bind((UDP_IP, UDP_PORT))                            # Bind socket to IP & Port of the Surface Pi

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
display_width = 1920                       # 1208 (Home) 1825 (Hill) (Diff 640)
display_length = 1080                        # 649  (Home) 953  (Hill) (Diff 360)
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
screen = pygame.display.set_mode((display_width, display_length))  # Creates Window/screen
pygame.display.set_caption("The Hill ROV Companion App")           # Sets Window's Title

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Pygame Initializations


pygame.init()                                # Initialize pygame
pygame.joystick.init()                       # Initialize the Joystick library

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

""""""
# Screenshot Variables

screenshotsLeft = []    # Both used to store screenshots
screenshotsRight = []   # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

screenshotLeft = None   # Holds the selected screenshot to be displayed on the Left
screenshotRight = None  # Holds the selected screenshot to be displayed on the Right

ssWaitL = 0    # Waits for X counts before allowing next screenshot
ssWaitR = 0    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

squareWait = 0    # Waits for X counts before allowing next button use
circleWait = 0    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ssDisplayedIndexL = 0    # Stores index of screenshotsLeft being displayed
ssDisplayedIndexR = 0    # Stores index of screenshotsRight being displayed

""""""
camConnected = 0
image = ""
running = True   # Main loop ends when this = False.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Data to be sent to ROV

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

    # Attempt to Display Video Feed
    if camConnected:
        screen.blit(pygame.transform.scale(image, (524, 393)), (0, 0))  # Will be replaced with value from ROV
    else:
        camDisconnectedText.Print(screen, "CAMERA DISCONNECTED.")

    # Displays screenshots
    pygame.draw.rect(screen, ORANGE, (535, 399, 673, 250))  # 535 399 673 250
    if screenshotLeft is not None:   # Might change to != None
        screen.blit(pygame.transform.scale(screenshotLeft, (320, 240)), (548, 409))
    if screenshotRight is not None:  # Might change to != None
        screen.blit(pygame.transform.scale(screenshotRight, (320, 240)), (876, 409))

    # Display Titles
    motorTitleText.Print(screen, "Motor Values:")
    sensTitleText.Print(screen, "Sensor Values:")
    gamepadReminderText.Print(screen, "Mash <Playstation Button> after Reconnect!")

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Presume Up & Right to be +1. May need to reverse on a case by case basis. """

    if gamepadConnected:
        for b in [4, 5, 6, 7, 8, 9]:  # Checks for all arm related servo value changes

            # Up on D-pad
            if b == 4:  # Extend Arm
                if gamepad.get_button(b) == 1:
                    if clawUDPosition > 0:
                        clawUDPosition -= 1

            # Down on D-pad
            elif b == 6:  # Withdraw Arm
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

            # Right Trigger
            elif b == 9:  # Close Claw
                if gamepad.get_button(b) == 1:
                    if clawGraspPosition < 180:
                        print("Right")
                        clawGraspPosition += 1
                        clawGraspServo.write(clawGraspPosition)

            # Left Trigger
            elif b == 8:  # Open Claw
                if gamepad.get_button(b) == 1:
                    if clawGraspPosition > 0:
                        print("Left")
                        clawGraspPosition -= 1
                        clawGraspServo.write(clawGraspPosition)

        for b in [1, 2, 12, 13, 14, 15]:  # Checks for changes to screenshot and camera variables

            # Left Joystick
            if b == 1:  # Flip through saved Left Screenshots
                if ssWaitL == 0:
                    if gamepad.get_button(b) == 1:
                        if not screenshotsLeft:
                            pass
                        else:
                            ssDisplayedIndexL += 1
                            if ssDisplayedIndexL >= len(screenshotsLeft):
                                ssDisplayedIndexL = 0
                            screenshotLeft = screenshotsLeft[ssDisplayedIndexL]
                            ssWaitL += 1
                else:
                    ssWaitL += 1
                    if ssWaitL >= 10:
                        ssWaitL = 0

            # Right Joystick
            if b == 2:  # Flip through saved Right Screenshots
                if ssWaitR == 0:
                    if gamepad.get_button(b) == 1:
                        if not screenshotsRight:
                            pass
                        else:
                            ssDisplayedIndexR += 1
                            if ssDisplayedIndexR >= len(screenshotsRight):
                                ssDisplayedIndexR = 0
                            screenshotRight = screenshotsRight[ssDisplayedIndexR]
                            ssWaitR += 1
                else:
                    ssWaitR += 1
                    if ssWaitR >= 10:
                        ssWaitR = 0

            # Triangle Button
            if b == 12:  # Move Camera Servo Up
                if gamepad.get_button(b) == 1:
                    if camUDPosition < 180:
                        camUDPosition += 1
                        camUDServo.write(camUDPosition)

            # Circle Button
            elif b == 13:  # Save Screenshot to RightArray
                if circleWait == 0:
                    if camConnected:
                        if gamepad.get_button(b) == 1:
                            screenshotsRight.append(cam.get_image())
                            ssDisplayedIndexR = len(screenshotsRight) - 1
                            screenshotRight = screenshotsRight[len(screenshotsRight) - 1]
                            circleWait += 1
                else:
                    circleWait += 1
                    if circleWait >= 10:
                        circleWait = 0

            # X Button
            elif b == 14:  # Move Camera Servo Down
                if gamepad.get_button(b) == 1:
                    if camUDPosition > 0:
                        camUDPosition -= 1
                        camUDServo.write(camUDPosition)

            # Square Button
            elif b == 15:  # Save Screenshot to LeftArray
                if squareWait == 0:
                    if camConnected:
                        if gamepad.get_button(b) == 1:
                            screenshotsLeft.append(cam.get_image())
                            ssDisplayedIndexL = len(screenshotsLeft) - 1
                            screenshotLeft = screenshotsLeft[len(screenshotsLeft) - 1]
                            squareWait += 1
                else:
                    squareWait += 1
                    if squareWait >= 10:
                        squareWait = 0

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
                MVerticalValue = 1500 + (400 * throttle)
            elif joystick.get_hat(0) == (-1, -1) or joystick.get_hat(0) == (0, -1) or joystick.get_hat(0) == (1, -1):
                MVerticalValue = 1500 - (400 * throttle)
            else:
                MVerticalValue = 1500
                MHorizontalValue = 1500

            # Crab
            if a == 0:
                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500 - (400 * throttle), 1500 + (400 * throttle))
                MHorizontalValue = valAxis

            # Forward-Backward
            elif a == 1:
                valAxis = changeInterval(-joystick.get_axis(a), -1, 1, 1500 - (400 * throttle), 1500 + (400 * throttle))
                MLeftValue = valAxis
                MRightValue = valAxis

            # Yaw
            elif a == 2:
                yawChange = joystick.get_axis(a)  # [-1 to 1]
                yaw = yawChange * 200 * throttle  # 200 can equal up to 400

                # If MRightValue is Increasing
                if yawChange < 0:
                    if MRightValue + yaw > 1900:  # Checks to see if new MRightValue > 1900. If so, Offputs change to MLeftValue
                        MRightValue = 1900
                        MLeftValue = MLeftValue - yaw - (MRightValue + yaw) + 1900
                    elif MRightValue - yaw < 1100:  # Checks to see if new MLeftValue < 1100. If so, Offputs change to MRightValue
                        MLeftValue = 1100
                        MRightValue = MRightValue + yaw + (MLeftValue - yaw) - 1100
                    else:
                        MLeftValue += yaw
                        MRightValue -= yaw

                # If MLeftValue is Increasing.
                elif yawChange > 0:
                    if MLeftValue + yaw > 1900:  # Checks to see if new MLeftValue > 1900. If so, Offputs change to MRightValue
                        MLeftValue = 1900
                        MRightValue = MRightValue - yaw - (MLeftValue + yaw) + 1900
                    elif MRightValue - yaw < 1100:  # Checks to see if new MRightValue < 1100. If so, Offputs change to MLeftValue
                        MRightValue = 1100
                        MLeftValue = MVerticalValue + yaw + (MRightValue - yaw) - 1100
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

    # Cast Servos as encoded strings
    strClawUDPosition = str(clawUDPosition)
    strArmLRPosition = str(armLRPosition)
    strClawGraspPosition = str(clawGraspPosition)
    strCamUDServo = str(camUDPosition)

    # Add leading 0's to servo values if a 1 or 2 digit number.
    for s in [strClawUDPosition, strArmLRPosition, strClawGraspPosition, strCamUDServo]:
        if len(s) == 1:
            s = "00" + s
        elif len(s) == 2:
            s = "0" + s

    # Data to be sent to ROV (28 bytes)
    sData = str(int(MLeftValue)) + str(int(MRightValue)) + str(int(MVerticalValue)) + str(int(MHorizontalValue)) + strClawUDPosition + strArmLRPosition + strClawGraspPosition + strCamUDServo
    sData.encode('utf-8')

    sock.sendto(sData, server)  # Send the data to the ROV
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive data from the ROV
    
    rData = sock.recvfrom(1024)
    rData = rData.decode('utf-8')

    camConnected = int(rData[:1])
    image = pygame.image.fromstring(rData[1:])

    # Translate data received
    # Set Sensor Values
    # Set camera value
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Update GUI

    # Sets throttle text's color to Red if at 0.
    if throttle == 0:
        valMotorsText.changeColor(RED)

    valMotorsText.Print(screen, "Throttle: " + str(int(throttle * 100)) + "%")
    valMotorsText.newLine()

    # Display Value of all motors
    if joystickConnected:
        valMotorsText.Print(screen, "Motor 1: " + str(MLeftValue))
        valMotorsText.newLine()

        valMotorsText.Print(screen, "Motor 2: " + str(MRightValue))
        valMotorsText.newLine()

        valMotorsText.Print(screen, "Motor 3: " + str(MVerticalValue))
        valMotorsText.newLine()

        valMotorsText.Print(screen, "Motor 4: " + str(MHorizontalValue))
        valMotorsText.newLine()
    else:
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
    clock.tick(60)  # Sets FPS to 60

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

pygame.quit()
quit()
