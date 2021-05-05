import wpilib as wpi #I don't know how to describe WPI, I can just safely say that making an FRC robot in ANY LANGUAGE is impossible without it.
import wpilib.drive #The methods within wpilib specifically related to drive and movement.
from wpilib.interfaces import GenericHID #I honestly don't know specifically what GenericHID is or what is stands for, I just know that it's necessary for the controllers and their inputs
import ctre #All libraries and methods related to the "Cross The Road Electronics"(ctre) motors.
from rev.color import ColorSensorV3 #All libraries and methods related to the color sensor.
from networktables import NetworkTables #I know what networktables ARE, but I have no idea how to describe them

import MethodsRobot #Allows the main file robot.py to access all of the methods within the MethodsRobot.py file
import ports #Allows the main file robot.py to access all of the ID's within the ports.py file

'''
The one, the only... MyRobot!!! Literally just the main class and a robot can't run without one of these. 
Just imagine a java program without a main(String[] args) class..

The parameter wpi.TimedRobot just tells the program that this robot runs using a timed system. 
Another alternative is IterativeRobot. But that's more advanced and as such requires more effort, I'm much too lazy for that.
If you really wanna know more about it, just look on the robotpy documentation.
'''
class MyRobot(wpi.TimedRobot):  

    #Self-Explanatory
    def resetStates(self):
        self.state = 0 #Int to check which mode/stage/state the shooter is currently in, and what tasks it is and is not currently doing
        self.cState = 0 #Int to check which mode/stage/state the spinner/lift mechanisms are currently in, and what tasks they are and are not currently doing
        self.colorCheck = False #Boolean to check whether the specific color on the wheel is currently under the FRC sensor
        self.spinCheck = False #Boolean to check if the numbers of wheel spins has been reached

        self.liftToggle = False #Checks whether or not 

    #The method that is first ran when the program starts. Initializes many of the variables and methods needed for the rest of the code
    def robotInit(self):

        self.driveMethods = MethodsRobot.Drive() #parent variable allowing access to all child methods of the Drive() class
        self.shooterMethods = MethodsRobot.Shooter() #parent variable allowing access to all child methods of the Shooter() class
        self.controllerMethods = MethodsRobot.Controller() #parent variable allowing access to all child methods of the Controller() class

        self.controllerMotor = ctre.WPI_TalonSRX(ports.talonPorts.get("controllerMotor")) #parent variable for the motor related to the controller(the spinner)

        self.timer = wpi.Timer() #No
        
        self.resetStates() #creates and sets the variables within resetStates() to 0

        self.driverController = wpi.XboxController(ports.controllerPorts.get("driverController")) #parent variable for the primary controller, the xbox controller
        self.codriverController = wpi.XboxController(ports.controllerPorts.get("codriverController")) #parent variable for the secondary controller, the logitech or whatever controller

        ##wpi.CameraServer.launch() 
        #wpi.CameraServer.

        
        self.printTimer = wpi.Timer()
        self.printTimer.reset()
        self.printTimer.start()

        '''
        self.table = NetworkTables.getTable("limelight")
        self.tx = self.table.getNumber('tx',None)
        self.ty = self.table.getNumber('ty',None)
        self.ta = self.table.getNumber('ta',None)
        self.ts = self.table.getNumber('ts',None)
        '''
        
    def teleopPeriodic(self):
        #self.driveMethods.basicDrive(self.driverController.getX(GenericHID.Hand.kLeftHand)*3/4, self.driverController.getY(GenericHID.Hand.kLeftHand)*3/4)
        #self.shooterMethods.intake(self.driverController.getBButtonPressed(), self.driverController.getAButtonPressed())
        #self.shooterMethods.shooting(self.driverController.getTriggerAxis(GenericHID.Hand.kRightHand))
        #self.shooterMethods.backup(self.driverController.getBumperPressed(GenericHID.Hand.kRightHand))
        #self.shooterMethods.backup(self.driverController.getTriggerAxis(GenericHID.kRightHand))
        #self.shooterMethods.shooter(self.driverController.getBumperPressed(GenericHID.Hand.kRightHand))
        #self.shooterMethods.intake(self.driverController.getBumperPressed(GenericHID.Hand.kLeftHand))

        intakeButton = self.driverController.getBumperPressed(GenericHID.Hand.kLeftHand)
        shooterButton = self.driverController.getBumperPressed(GenericHID.Hand.kRightHand)
        backButton = self.driverController.getYButtonPressed()
        emptyButton = self.driverController.getBButtonPressed()

        if emptyButton and self.state != 4:
            # State 4 completely empties the robot of any stored balls
            self.state = 4
        elif backButton and self.state != 3:
            # State 3 backs up the balls a little bit to avoid a jam
            self.state = 3
        elif intakeButton and self.state != 2:
            # state 2 intakes balls and stores them
            self.state = 2
        elif shooterButton and self.state != 1:
            # State 1 shoots balls
            self.state = 1
        elif intakeButton or shooterButton or backButton:
            # Hitting any button again turns all off
            self.state = 0

        # ----------| Spinner State Machine |---------- #
        
        colorButton = self.driverController.getAButtonPressed() #Spins the controller until a certain color
        spinButton = self.driverController.getXButtonPressed() #Spins the controller a certain number of times
        liftButton = self.driverController.getStartButtonPressed() #Toggles the 'lift' that raises and lowers the controller motor
        lowerButton = self.driverController.getBackButtonPressed()

        
        if self.printTimer.hasPeriodPassed(0.5):
            #self.logger.info(self.controllerMethods.checkTopSensor())
            #self.logger.info(self.controllerMethods.checkBottomSensor())
            self.logger.info(self.controllerMethods.checkColorSensor())

        if liftButton and self.cState == 0: #Toggles the status of the lift
            self.cState = 1
        elif lowerButton and self.cState == 1:
            self.cState = 0
        elif spinButton and self.cState == 1: #If colorButton, lift is raised, and state is not already 1, make state 1
            self.cState = 2
        elif colorButton and self.cState == 1: #If spinButton, lift is raised, and state is not already 2, make state 2
            self.cState = 3
        elif self.cState != 0 and (spinButton or colorButton):
            self.cState = 1
        
        #elif self.cState != 
        
        '''
        elif cState ==r or spinButton: #If spin or color is on, and one of the corresponding buttons is pressed again, turn all off & make the controller go idle
            self.cState = 0
        '''

        # ----------| Controller State Machine |---------- #

        # ----------/ Drive Methods \---------- #
        self.driveMethods.basicDrive(self.driverController.getX(GenericHID.Hand.kLeftHand)*3/4, -self.driverController.getY(GenericHID.Hand.kLeftHand))
        # ----------\ Drive Methods /---------- #

        # ----------/ Shooter Methods \---------- #
        if self.state == 4:
            self.shooterMethods.empty()
        elif self.state == 3:
            self.shooterMethods.backup()
        elif self.state == 2:
            self.shooterMethods.intake()
        elif self.state == 1:
            self.shooterMethods.shooting()
        else:
            self.shooterMethods.idle()
        # ----------\ Shooter Methods /---------- #

        # ----------/ Controller Methods \---------- #
        
        if self.cState == 1:
            self.controllerMethods.lift()
        elif self.cState == 2:
            self.controllerMethods.numSpin()
        elif self.cState == 3:
            self.controllerMethods.colorSpin()
        else:
            self.controllerMethods.lower()
        
        # ----------\ Controller Methods /---------- #

        #print(self.controllerMethods.currentColor)
        #self.controllerMethods.dial(self.driverController.getBumperPressed(GenericHID.Hand.kLeftHand), self.driverController.getBumperPressed(GenericHID.Hand.kRightHand))
        #self.shooterMethods.shooting2(self.driverController.getBumperPressed(GenericHID.Hand.kRightHand))

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        #self.teleopPeriodic()
        '''
        if self.timer.get() < 2.0:
            self.driveMethods.basicDrive(0, -0.5)
        else:
            self.driveMethods.basicDrive(0, 0)
        '''

    def disabledInit(self):
        self.resetStates()



if __name__ == "__main__":
    wpi.run(MyRobot)