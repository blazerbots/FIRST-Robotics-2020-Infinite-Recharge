import wpilib as wpi
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID
import ctre
from rev.color import ColorSensorV3

import ports


class Drive():
    def __init__(self):
        
        self.leftMotor = wpi.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("leftChassisMotor")))
        self.rightMotor = wpi.SpeedControllerGroup(ctre.WPI_TalonSRX(ports.talonPorts.get("rightChassisMotor")))
        self.drive = wpi.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        #self.colorSensor = ColorSensorV3(wpi.I2C.Port.kOnboard)


    def basicDrive(self, x, y):
        #if drive is None:
        #drive = wpi.drive.DifferentialDrive(self.leftMotor, self.rightMotor)
        #drive.setSafetyEnabled(False)
        #self.controllerXValue = x
        #self.controllerYValue = y
        #self.drive.arcadeDrive(self.controllerYValue, self.controllerXValue)
        self.drive.arcadeDrive(y, x)


class Shooter():
    def __init__(self):
    
        # #Intake Components and Variables
        # self.intakeMotor = ctre.WPI_TalonSRX(ports.talonPorts.get("intakeMotor"))
        # self.bToggle = False
        # self.aToggle = False
        # self.timer = wpi.Timer()
        # self.cToggle = False #Conveyor Toggle
        # self.iToggle = False #Intake Toggle
        # self.sToggle = False #Shooter Toggle
        # self.cRun = False #True means conveyor is running
        # self.iRun = False # ^ ^ ^
        # self.sRun = False # ^ ^ ^
        # self.bRun = False # True means backup is running, iRun and sRun MUST be off if this is on
        # self.eRun = False # True means empty is running
        # self.bHold = False

        # #Shooting Components and Variables
        # self.shootingMotorF = ctre.WPI_TalonSRX(ports.talonPorts.get("shootingMotorF"))
        # self.shootingMotorB = ctre.WPI_TalonSRX(ports.talonPorts.get("shootingMotorB"))

        # #Conveyor Components and Variables
        # self.conveyorMotor = ctre.WPI_TalonSRX(ports.talonPorts.get("conveyorMotor"))
        # self.conveying = 0
        # self.conveyorMotor.set(0)

        #self.timer = wpi.Timer()
        self.shooterTimer = wpi.Timer()
        self.shooterToggle = False

        #Intake Components and Variables
        self.intakeMotor = ctre.WPI_TalonSRX(ports.talonPorts.get('intakeMotor'))
        
        #Shooting Components and Variables
        self.shootingMotorF = ctre.WPI_VictorSPX(ports.talonPorts.get('shootingMotorF'))
        self.shootingMotorB = ctre.WPI_VictorSPX(ports.talonPorts.get('shootingMotorB'))

        #Conveyor Components and Variables
        self.conveyorMotor = ctre.WPI_TalonSRX(ports.talonPorts.get('conveyorMotor'))

        self.intakeMotorSpeed = -.35 #.45
        self.conveyorMotorSpeed = .45 #.45
        self.shooterSpeed = .475
        self.shooterRatio = .75


    '''
    def intake(self, bPress, aPress):
        if(bPress):
            self.bToggle = not self.bToggle
            self.aToggle = False

        if(aPress):
            self.aToggle = not self.aToggle
            self.bToggle = False

        if(self.aToggle):
            self.intakeMotor.set(.1)
            if(self.conveying == 1):
                self.conveyorMotor.set(.35)
                self.conveying = 1
        else:
            self.intakeMotor.stopMotor()

        if(self.bToggle):
            self.intakeMotor.set(-.1)
            if(self.conveyorMotor):
                self.conveyorMotor.set(.35)
                self.conveying = 1
        else:
            self.intakeMotor.stopMotor()
        '''

    '''
    def shooting(self, triggerPress):
        if(triggerPress == 1):
            self.shootingMotorF.set(.375)
            self.shootingMotorB.set(-.485)
            if(not self.conveying):
                self.conveyorMotor.set(.35)
                self.conveying = 1
        else:
            self.shootingMotorF.stopMotor()
            self.shootingMotorB.stopMotor()
    '''
    '''
    def backup(self, buttonPress):
        if (buttonPress):
            self.conveyorMotor.set(-.45)
            self.intakeMotor.set(.25)
            self.shootingMotorF.set(-.25)
            self.shootingMotorB.set(.25)
        else:
            self.conveyorMotor.set(0)
            self.intakeMotor.set(0)
            self.shootingMotorF.set(0)
            self.shootingMotorB.set(0)

    def intake(self, buttonPress):
        if(buttonPress):
            self.iToggle = not self.iToggle
            self.cToggle = not self.cToggle

        if(self.iToggle):
            self.sToggle = False

        if(self.iToggle):
            self.conveyorMotor.set(.45)
            self.intakeMotor.set(-.25)
        else:
            self.intakeMotor.set(0)

        
        if(not self.cToggle):
            self.conveyorMotor.set(0)
        
    

    def shooter(self, buttonPress):
        if(buttonPress):
            self.sToggle = not self.sToggle
            self.cToggle = not self.cToggle

        if(self.sToggle):
            self.iToggle = False

        if(self.sToggle):
            self.conveyorMotor.set(.45)
            self.shootingMotorF.set(.3725)
            self.shootingMotorB.set(-.4825)
        else:
            self.shootingMotorF.set(0)
            self.shootingMotorB.set(0)
            

        
        if(not self.cToggle):
            self.conveyorMotor.set(0)
        

    def shooting2(self, buttonPress): #tm = timer
        #self.shootingMotorF.set(.375)
        #self.shootingMotorB.set(-.485)
        if(buttonPress):
            #self.timer.reset() NO
            #self.timer.start() NO
            
            self.shootingMotorF.set(.375)
            self.shootingMotorB.set(-.485)
            self.conveyorMotor.set(.45)
            self.intakeMotor.set(-.25)
            ''' '''
            ----------IMPORTANT----------
            A timer delay was used to allow the shooter to turn on and gain speed before
            the conveyor turns on (prevents weak shots). Using a timer for a delay in an
            if statement causes the code to treat the statement as a loop. This breaks it
            and gives various errors like: 'Watchdog not fed within ####s', 'RobotDrive... Output not
            updated often enough', something to do with DifferentialDrive, robotsafety, etc.
            ''' '''
            #if(self.timer.hasPeriodPassed(2)): DON'T USE
                #self.timer.stop()
                #self.conveyorMotor.set(.45)
'''

    def intake(self):
        self.shooterToggle = False

        self.shootingMotorB.stopMotor()
        self.shootingMotorF.stopMotor()
        self.conveyorMotor.set(self.conveyorMotorSpeed)
        self.intakeMotor.set(self.intakeMotorSpeed)
 

    def empty(self): #Empties the robot of all balls
        self.shooterToggle = False

        self.shootingMotorB.set(self.shooterSpeed * self.shooterRatio)
        self.shootingMotorF.set(-self.shooterSpeed)
        self.conveyorMotor.set(-self.conveyorMotorSpeed)
        self.intakeMotor.set(-self.intakeMotorSpeed)

    def backup(self):
        self.shooterToggle = False

        self.shootingMotorB.set(self.shooterSpeed * self.shooterRatio)
        self.shootingMotorF.set(-self.shooterSpeed)
        self.conveyorMotor.set(-self.conveyorMotorSpeed)
        self.intakeMotor.set(-self.intakeMotorSpeed)

    def shooting(self):
        
        self.intakeMotor.stopMotor()
        
        if (not self.shooterToggle):
            self.shooterToggle = True

            if self.shooterTimer is None:
                self.shooterTimer = wpi.Timer()

            self.shooterTimer.reset()
            self.shooterTimer.start()

            #self.conveyorMotor.set(-self.conveyorMotorSpeed*.5)
            self.conveyorMotor.stopMotor()
            self.shootingMotorB.set(-self.shooterSpeed)
            self.shootingMotorF.set(self.shooterSpeed)
        
        if self.shooterToggle and self.shooterTimer.get() > 3:
            self.conveyorMotor.set(self.conveyorMotorSpeed * 1.25)
            self.shootingMotorB.set(-self.shooterSpeed * self.shooterRatio * 1.25)
            self.shootingMotorF.set(self.shooterSpeed)


    def idle(self):
        self.shooterToggle = False
        self.shootingMotorB.stopMotor()
        self.shootingMotorF.stopMotor()
        self.conveyorMotor.stopMotor()
        self.intakeMotor.stopMotor()
            
class Controller():
    def __init__(self):
        self.colorSensor = ColorSensorV3(wpi.I2C.Port.kOnboard)
        self.liftMotor = ctre.WPI_VictorSPX(ports.talonPorts.get("liftMotor"))
        self.wheelMotor = ctre.WPI_VictorSPX(ports.talonPorts.get("controllerMotor"))

        self.bottomHallEffect = wpi.AnalogInput(ports.talonPorts.get("liftBottom"))
        self.topHallEffect = wpi.AnalogInput(ports.talonPorts.get("liftTop"))
        self.sensorThreshold = 500

        self.lToggle = False
        self.rToggle = False
        self.color = 1
        
        self.colorCount = 0 #Varipy pyable to count how many times the color has changed, may also be used to count how many times the wheel has been spun
        self.controllerCheck = False #False: # of spins or on certian color reqs not met, keep going True: conditions met, stop
        
        self.lifting = False
        self.lowering = False
        self.liftSpeed = .55
        self.wheelSpeed = .5


    def checkColorSensor(self):
        self.currentColor = self.colorSensor.getColor() #Variable to determine what the current color sensed by the sensor is
        self.ir = self.colorSensor.getIR()
        self.colorProximity = self.colorSensor.getProximity()
        
        wpi.SmartDashboard.putNumber("Red", self.currentColor.red)
        wpi.SmartDashboard.putNumber("Green", self.currentColor.green)
        wpi.SmartDashboard.putNumber("Blue", self.currentColor.blue)
        wpi.SmartDashboard.putNumber("IR", self.ir)
        wpi.SmartDashboard.putNumber("Proximity", self.colorProximity)   

        return self.currentColor
        
    def checkBottomSensor(self):
        self.bottomHall = self.bottomHallEffect.getValue()
        return self.bottomHall

    def checkTopSensor(self):
        self.topHall = self.topHallEffect.getValue()
        return self.topHall

    def boolFromVal(self, value):
        if value < self.sensorThreshold:
            return True
        else:
            return False    
     
    def lift(self):
        self.wheelMotor.stopMotor()

        self.bottomHall = self.boolFromVal(self.bottomHallEffect.getValue())
        self.topHall = self.boolFromVal(self.topHallEffect.getValue())

        if self.bottomHall and not self.lifting:
            self.lifting = True

        if self.lifting and self.topHall:
            self.liftMotor.set(0.2)
            self.lifting = False
        elif self.lifting:
            self.liftMotor.set(self.liftSpeed)
        else:
            self.liftMotor.set(0.2)

    def lower(self):
        self.wheelMotor.stopMotor()
        
        self.bottomHall = self.boolFromVal(self.bottomHallEffect.getValue())
        self.topHall = self.boolFromVal(self.topHallEffect.getValue())

        if self.bottomHall:
            self.idle()
            pass

        if not self.lowering: #and self.topHall
            self.lowering = True

        if self.lowering and self.bottomHall:
            self.liftMotor.stopMotor()
            self.lowering = False
        elif self.lowering:
            self.liftMotor.set(self.liftSpeed * -.25)
        else:
            self.liftMotor.stopMotor()
        

    def colorSpin(self):
        #pass
        self.checkColorSensor()
        self.wheelMotor.set(self.wheelSpeed)
        '''
        if self.lifted and not (self.cSpin or self.nSpin):
            self.cSpin = True
            if(self.currentColor != self.setColor):
                self.wheelMotor.set(wheelSpeed)
            else:
                self.wheelMotor.set(0)

        OR

        if self.lifted and (self.cSpin)
        '''
    
    def numSpin(self):
        #pass
        self.checkColorSensor()
        self.wheelMotor.set(self.wheelSpeed)

    def idle(self):
        # something here to lower lift, can't implement yet
        self.liftMotor.stopMotor()
        self.wheelMotor.stopMotor()