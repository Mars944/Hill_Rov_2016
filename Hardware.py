from time import sleep
from nanpy import Servo
import pygame

class Arduino():
    def __init__(self, display_width, display_length):
        # Create TextBox object to display connection status
        self.connectingText = TextBox(40, display_width/3, display_length/2)
        self.connectingText.changeColor(WHITE)

    def connect(self):
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
                self.connectingText.print(screen, "Arduino Connected!")
                pygame.display.update()
            except:
                if failed == 0:
                    self.connectingText.print(screen, "Failed to connect to Arduino")
                    pygame.display.update()
                    sleep(1)
                    screen.fill(BLACK)
                    failed += 1
                else:
                    screen.fill(BLACK)
                    self.connectingText.print(screen, "Attempting to Connect to Arduino.")
                    pygame.display.update()
                    sleep(.5)                                        
                    screen.fill(BLACK)
                    self.connectingText.print(screen, "Attempting to Connect to Arduino..")
                    pygame.display.update()
                    sleep(.5)

                    screen.fill(BLACK)
                    self.connectingText.print(screen, "Attempting to Connect to Arduino...")
                    pygame.display.update()
                    sleep(.5)

class Motor:

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.value = 1500
       
        try:
            self.servo = Servo(self.pin)
            self.servo.writeMicroseconds(1500)
            sleep(1)
            connected = True
            print("Success.")
        except:
            print("Failed.")

                
    def setValue(self, value):
        self.servo.writeMicroseconds(value)
