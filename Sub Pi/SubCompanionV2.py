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

sensorRequested = 0  # If 1, then data from the Sensor will be recorded
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
    sensorRequested = int(rData[24:25])

    print(str(armLRPosition))

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Read and Prepare Sensor data (Code from https://www.controleverything.com/content/Pressure?sku=MS5837-30BA01_I2CS#tabs-0-product_tabset-2)

    while True:
        # Read 12 bytes of calibration data
        # Read pressure sensitivity
        data = bus.read_i2c_block_data(0x76, 0xA2, 2)
        C1 = data[0] * 256 + data[1]

        # Read pressure offset
        data = bus.read_i2c_block_data(0x76, 0xA4, 2)
        C2 = data[0] * 256 + data[1]

        # Read temperature coefficient of pressure sensitivity
        data = bus.read_i2c_block_data(0x76, 0xA6, 2)
        C3 = data[0] * 256 + data[1]

        # Read temperature coefficient of pressure offset
        data = bus.read_i2c_block_data(0x76, 0xA8, 2)
        C4 = data[0] * 256 + data[1]

        # Read reference temperature
        data = bus.read_i2c_block_data(0x76, 0xAA, 2)
        C5 = data[0] * 256 + data[1]

        # Read temperature coefficient of the temperature
        data = bus.read_i2c_block_data(0x76, 0xAC, 2)
        C6 = data[0] * 256 + data[1]

        # MS5837_30BA01 address, 0x76(118)
        #		0x40(64)	Pressure conversion(OSR = 256) command
        bus.write_byte(0x76, 0x40)

        time.sleep(0.5)

        # Read digital pressure value
        # Read data back from 0x00(0), 3 bytes
        # D1 MSB2, D1 MSB1, D1 LSB
        value = bus.read_i2c_block_data(0x76, 0x00, 3)
        D1 = value[0] * 65536 + value[1] * 256 + value[2]

        # MS5837_30BA01 address, 0x76(118)
        #		0x50(64)	Temperature conversion(OSR = 256) command
        bus.write_byte(0x76, 0x50)

        time.sleep(0.5)

        # Read digital temperature value
        # Read data back from 0x00(0), 3 bytes
        # D2 MSB2, D2 MSB1, D2 LSB
        value = bus.read_i2c_block_data(0x76, 0x00, 3)
        D2 = value[0] * 65536 + value[1] * 256 + value[2]

        dT = D2 - C5 * 256
        TEMP = 2000 + dT * C6 / 8388608
        OFF = C2 * 65536 + (C4 * dT) / 128
        SENS = C1 * 32768 + (C3 * dT ) / 256
        T2 = 0
        OFF2 = 0
        SENS2 = 0

        if TEMP >= 2000 :
                T2 = 2 * (dT * dT) / 137438953472
                OFF2 = ((TEMP - 2000) * (TEMP - 2000)) / 16
                SENS2 = 0
        elif TEMP < 2000 :
                T2 = 3 *(dT * dT) / 8589934592
                OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 2
                SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
                if TEMP < -1500 :
                        OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
                        SENS2 = SENS2 + 4 * ((TEMP + 1500) * (TEMP + 1500))

        TEMP = TEMP - T2
        OFF2 = OFF - OFF2
        SENS2 = SENS - SENS2
        pressure = ((((D1 * SENS2) / 2097152) - OFF2) / 8192) / 10.0
        
        depth = pressure/(1000*9.8)
        cTemp = TEMP / 100.0

	
	""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Send Data to Surface if Requested

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
