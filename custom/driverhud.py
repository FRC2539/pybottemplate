'''
The DriveHUD displays useful information on the driver dashboard, and can read
information from the dashboard and provide it to the program.
'''

from wpilib.sendablechooser import SendableChooser
from wpilib.smartdashboard import SmartDashboard
from wpilib.command import Scheduler
from wpilib.driverstation import DriverStation
from networktables import NetworkTables

autonChooser = None

from wpilib.robotbase import RobotBase

def init():
    '''
    This function must be called from robotInit, but not before the subsystems
    have been created. Do not call it more than once.
    '''

    global autonChooser

    if autonChooser is not None and not RobotBase.isSimulation():
        raise RuntimeError('Driver HUD has already been initialized')

    # Import here to avoid circular import
    from commands.autonomouscommandgroup import AutonomousCommandGroup
    from commands.drivetrain.resettiltcommand import ResetTiltCommand
    from commands.tools.configurepidcommandgroup import ConfigurePIDCommandGroup


    '''
    Add commands to the autonChooser to make them available for selection by the
    driver. It is best to choose a command that will not break anything if run
    at the wrong time as the default command.
    '''
    autonChooser = SendableChooser()
    autonChooser.addDefault('Autonomous', AutonomousCommandGroup())

    SmartDashboard.putData('Autonomous Program', autonChooser)

    '''Display all currently running commands.'''
    SmartDashboard.putData('Active Commands', Scheduler.getInstance())

    showCommand(ResetTiltCommand())
    showCommand(ConfigurePIDCommandGroup())


def getAutonomousProgram():
    '''
    Return the autonomous program as selected on the dashboard. It is up to the
    calling scope to start and cancel the command as needed.
    '''

    global autonChooser

    if autonChooser is None:
        raise RuntimeError('Cannot select auton before HUD initializiation')

    return autonChooser.getSelected()


def showCommand(cmd):
    '''Display the given command on the dashboard.'''

    name = str(cmd)
    name.replace('/', '_')
    SmartDashboard.putData('Commands/%s' % name, cmd)


def showAlert(msg, type='Alerts'):
    '''Display a text notification on the dashboard.'''

    messages = SmartDashboard.getStringArray(type, [])
    messages = [x for x in messages if x]
    messages.append(msg)
    SmartDashboard.putStringArray(
        type,
        messages
    )


def showInfo(msg):
    showAlert(msg, 'Info')


def showField():
    field = NetworkTables.getTable('Field');
    ds = DriverStation.getInstance()

    color = ds.getAlliance()

    if color == ds.Alliance.Red:
        field.putValue('color', 'red')
    elif color == ds.Alliance.Blue:
        field.putValue('color', 'blue')

    layout = ds.getGameSpecificMessage()
    if layout:
        field.putValue('layout', layout)
