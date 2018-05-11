#!/usr/bin/env python3

import sys, os, re
import robot


def generateSubsystem():
    if len(sys.argv) >= 3:
        subsystem = sys.argv[2]
    else:
        subsystem = input('Enter a name for your subsystem: ')

    subsystem = subsystem.strip()
    if not subsystem:
        print("Subsystem name must not be blank")
        sys.exit()

    if subsystem[0].isdigit():
        print('Subsystem name cannot start with a digit')
        sys.exit()

    if not subsystem.isalnum():
        print('Subsystem name must contain only letters and numbers')
        sys.exit()

    if subsystem.lower() == subsystem:
        print('Subsystem name should be ClassCased')
        sys.exit()

    module = subsystem.lower()

    if hasattr(robot, module):
        print('There is already a subsystem for %s' % module)
        sys.exit()

    with open('subsystems/%s.py' % module, 'w') as f:
        f.write('''
from .debuggablesubsystem import DebuggableSubsystem

import ports


class {subsystem}(DebuggableSubsystem):
    \'\'\'Describe what this subsystem does.\'\'\'

    def __init__(self):
        super().__init__('{subsystem}')
'''.lstrip().format(subsystem=subsystem))


    with open('robot.py', 'r') as f:
        init = f.read()

    imports = re.compile(
        '(from\s+subsystems\.\w+\s+import\s+[A-Z]\w+\s+as\s+\w+\s*)+'
    )
    match = imports.search(init)

    old = match[0].strip()
    new = '%s\nfrom subsystems.%s import %s as %s'
    init = init.replace(old, new % (old, module, subsystem, module))

    with open('robot.py', 'w') as f:
        f.write(init)


    with open('ports.py', 'r') as f:
        ports = f.read()

    if not module in ports:
        ports = '''
%s
%s = PortsList()
''' % (ports, module)

    with open('ports.py', 'w') as f:
        f.write(ports)

    print('Generated subsystem %s' % subsystem)


def generateCommand():
    if len(sys.argv) >= 3:
        command = sys.argv[2]
    else:
        command = input('Enter a name for your command: ')

    command = command.strip()
    if not command:
        print("Command name must not be blank")
        sys.exit()

    if command[0].isdigit():
        print('Command name cannot start with a digit')
        sys.exit()

    if not command.isalnum():
        print('Command name must contain only letters and numbers')
        sys.exit()

    if command.lower() == command:
        print('Command name should be ClassCased')

    inherits = None
    if command.endswith('CommandGroup'):
        inherits = 'CommandGroup'
    elif not command.endswith('Command'):
        command += 'Command'

    if command == 'DefaultCommand':
        inherits = 'Command'

    if inherits is None:
        bases = [
            'InstantCommand',
            'TimedCommand',
            'CommandGroup',
            'Command',
            'DefaultCommand'
        ]
        print('Select a base class:')
        for id, cmd in enumerate(bases):
            print('%d.) %s' % (id, cmd))

        inherits = input('')
        if inherits.isdigit():
            inherits = bases[int(inherits)]

        if not inherits in bases:
            print('Unknown base class %s' % inherits)
            sys.exit()

    if inherits == 'CommandGroup':
        if command.endswith('Command'):
            command += 'Group'

    if inherits == 'DefaultCommand':
        inherits = 'Command'
        command = 'DefaultCommand'

    # Put spaces before capital letters
    # https://stackoverflow.com/a/199215
    description = re.sub('Command(Group)?$', '', command)
    description = re.sub(r'\B([A-Z])', r' \1', description)

    if inherits == 'TimedCommand':
        duration = input('Duration in seconds (leave blank if variable): ')
        duration = duration.strip()
        if duration != '':
            try:
                float(duration)
            except ValueError:
                print('Duration must be a number')
                sys.exit()

    subsystem = input('Which subsystem is %s for? ' % command)
    requirements = subsystem.strip().lower().split()

    for subsystem in requirements:
        if not hasattr(robot, subsystem):
            print('Unknown subsystem %s' % subsystem)
            sys.exit()

    if command == 'DefaultCommand':
        if len(requirements) == 0:
            print('Subsystem is required for DefaultCommand')
            sys.exit()

        with open('subsystems/%s.py' % requirements[0]) as f:
            content = f.read()

        if 'initDefaultCommand' in content:
            print('There is already a default command for this subsystem')
            sys.exit()

        if '.setDefaultCommand' in content:
            print('There is already a default command for this subsystem')
            sys.exit()

        content += '''

    def initDefaultCommand(self):
        from commands.%s.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
''' % requirements[0]

        with open('subsystems/%s.py' % requirements[0], 'w') as f:
            f.write(content)

        description = 'Default for %s' % requirements[0]

    path = 'commands'
    if len(requirements) > 0:
        if not os.path.isdir('commands/%s' % requirements[0]):
            os.makedirs('commands/%s' % requirements[0])

        path += '/%s' % requirements[0]

    content = 'from wpilib.command.%s import %s' % (inherits.lower(), inherits)
    content += '\n'

    if inherits == 'CommandGroup':
        content += 'import commandbased.flowcontrol as fc'

    elif len(requirements) > 0:
        content += '\nimport robot'

    content += '\n\nclass %s(%s):\n\n' % (command, inherits)

    if inherits == 'TimedCommand' and duration == '':
        content += '    def __init__(self, timeout):\n'
    else:
        content += '    def __init__(self):\n'

    if inherits == 'TimedCommand':
        if duration:
            content += "        super().__init__('%s', %s)"
            content = content % (description, duration)
        else:
            content += "        super().__init__('%s', timeout)" % description
    else:
        content += "        super().__init__('%s')" % description

    content += '\n\n'

    if inherits == 'CommandGroup':
        content += '        # Add commands here with self.addSequential() and '
        content += 'self.addParallel()'

    else:
        if len(requirements) > 0:
            for subsystem in requirements:
                content += '        self.requires(robot.%s)\n' % subsystem

            content += '\n'

        content += '\n    def initialize(self):\n        pass\n\n\n'

        if inherits != 'InstantCommand':
            content += '    def execute(self):\n        pass\n\n\n'
            content += '    def end(self):\n        pass\n'

    with open('%s/%s.py' % (path, command.lower()), 'w') as f:
        f.write(content)

    print('Created command %s' % command)


def usage():
    print('usage: %s subject [args...]' % sys.argv[0])
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    if sys.argv[1] == 'subsystem':
        generateSubsystem()

    elif sys.argv[1] == 'command':
        generateCommand()

    else:
        usage()
