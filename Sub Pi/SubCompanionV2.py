""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Imports

from time import sleep
import socket            # Used to create UDP connection between Pis
import smbus             # Required for I2C with MS5837_30BA01 Sensor
import Adafruit_PCA9685  # PWM Hat Library

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up UDP (Treated as Server)

UDP_IP = "192.168.1.11"  # Static IP of Sub Pi
UDP_PORT = 5001          # Port of Sub Pi 

client = ('192.168.1.10', 5000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Socket connection(IPv4, UDP)

# Attempts to bind socket until success.
binding = 1
while binding:
    try:
        sock.bind((UDP_IP, UDP_PORT))  # Bind socket to IP & Port of the Surface Pi
        binding = 0
    except:
        pass

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up MS5837_30BA01

# Get I2C bus
bus = smbus.SMBus(1)
time.sleep(.5)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set up PWM Hat

# Initialize the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure defualt servo pulse lengths
wrist_mid   = 430
wrist_plus  = 580
wrist_minus = 280

claw_mid    = 335
claw_plus   = 420
claw_minus  = 250

arm_mid     = 410
arm_plus    = 550
arm_minus   = 270

cam_mid   = 430

thruster_max = 410+(410*.75)
thruster_mid = 410
thruster_min = 410-(410*.75)



# Set frequency to 60hz, good for servos. (May need to change for motors?)
pwm.set_pwm_freq(60)
 
clawUDChannel = 1
clawGraspChannel = 0
armLRChannel = 2
camUDChannel = 3

LeftMotorChannel = 13
RightMotorChannel = 14
VerticalMotorChannel = 15

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Global Variables for Main Loop

# Define Motor Values at default (in mS).
MLeftValue = thruster_mid
MRightValue = thruster_mid
MVerticalValue = thruster_mid
MHorizontalValue = thruster_mid

# Write Servo's to Default
clawUDPosition    = wrist_mid
clawGraspPosition = claw_mid
camUDPosition     = cam_mid
armLRPosition     = arm_mid

OGClawUDPosition    = wrist_mid
OGClawGraspPosition = claw_mid
OGCamUDPosition     = cam_mid
OGArmLRPosition     = arm_mid

# Should already be in this position
pwm.set_pwm(LeftMotorChannel,     0, MLeftValue)
pwm.set_pwm(RightMotorChannel,    0, MRightValue)
pwm.set_pwm(VerticalMotorChannel, 0, MVerticalValue)

pwm.set_pwm(clawUDChannel,    0, clawUDPosition)
pwm.set_pwm(clawGraspChannel, 0, clawGraspPosition)
pwm.set_pwm(armLRChannel,     0, armLRPosition)
pwm.set_pwm(camUDChannel,     0, camUDPosition)
sleep(1)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Main Loop

running = True   # Breaks out of main loop if equal to False.
while running:
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive values from Sensors
    # I NEED TO DO THIS! DONT FORGET! DO IT TONIGHT!
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Receive & Translate Motor & Servo values from Surface

    rData, addr = sock.recvfrom(1024)
    rData = rData.decode('utf-8')

    MLeftValue = int(rData[:3])
    MRightValue = int(rData[3:6])
    MVerticalValue = int(rData[6:9])
    MHorizontalValue = int(rData[9:12])

    clawUDPosition = int(rData[12:15])
    armLRPosition = int(rData[15:18])
    clawGraspPosition = int(rData[18:21])
    camUDPosition = int(rData[21:24])

    print(str(armLRPosition))

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Prepare and send Sensor data to Surface

    #DO THIS SHIT TONIGHT!!!

    sData = "5char" # 5characters for temp. ? for pressure
    sData = sData.encode('utf-8')

    sock.sendto(sData, addr)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Write to motors & servos

    # Limits Motor speed from the original interval [410+256, 410-256]
    motorMax = thruster_max
    motorMin = thruster_min

    # Limits & writes M_Values to ESC's!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if MLeftValue > thruster_mid:
            pwm.set_pwm(LeftMotorChannel, 0, min(int(MLeftValue), int(motorMax)))
    elif MLeftValue < thruster_mid:
        
            pwm.set_pwm(LeftMotorChannel, 0, max(int(MLeftValue), int(motorMax)))
    else:
            pwm.set_pwm(LeftMotorChannel, 0, int(MLeftValue))

    if MRightValue > thruster_mid:
            pwm.set_pwm(RightMotorChannel, 0, min(int(MRightValue), int(motorMax)))
    elif MRightValue < thruster_mid:
            pwm.set_pwm(RightMotorChannel, 0, max(int(MRightValue), int(motorMax)))
    else:
            pwm.set_pwm(RightMotorChannel, 0, int(MRightValue))

    if MVerticalValue > thruster_mid:
            pwm.set_pwm(VerticalMotorChannel, 0, min(int(MVerticalValue), int(motorMax)))
    elif MVerticalValue < thruster_mid:
            pwm.set_pwm(VerticalMotorChannel, 0, max(int(MVerticalValue), int(motorMax)))
    else:
            pwm.set_pwm(VerticalMotorChannel, 0, int(MVerticalValue))

    # Write to Servos if new value is requested
    if clawUDPosition != OGClawUDPosition:
        pwm.set_pwm(clawUDChannel, 0, clawUDPosition)
        OGClawUDPosition = clawUDPosition

    if clawGraspPosition != OGClawGraspPosition:
        pwm.set_pwm(clawGraspChannel, 0, clawGraspPosition)
        OGClawGraspPosition = clawGraspPosition

    if camUDPosition != OGCamUDPosition:
        pwm.set_pwm(camUDChannel, 0, camUDPosition)
        OGCamUDPosition = camUDPosition

    if armLRPosition != OGArmLRPosition:
        pwm.set_pwm(armLRChannel, 0, armLRPosition)
        OGArmLRPosition = armLRPosition

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Prepare to Quit

# Write Servo's to Default
clawUDPosition    = wrist_mid
clawGraspPosition = claw_mid
camUDPosition     = cam_mid
armLRPosition     = arm_mid

# Should already be in this position
pwm.set_pwm(clawUDChannel,    0, clawUDPosition)
pwm.set_pwm(clawGraspChannel, 0, clawGraspPosition)
pwm.set_pwm(armLRChannel,     0, armLRPosition)
pwm.set_pwm(camUDChannel,     0, camUDPosition)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Quit

quit()
