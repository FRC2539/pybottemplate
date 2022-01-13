#!/usr/bin/env python3

import sys, os, re
import robot


def generateSubsystem():
    if len(sys.argv) >= 3:
        subsystem = sys.argv[2]
    else:
        subsystem = input("Enter a name for your subsystem: ")

    subsystem = subsystem.strip()
    if not subsystem:
        error("Subsystem name must not be blank")

    if subsystem[0].isdigit():
        error("Subsystem name cannot start with a digit")

    if not subsystem.isalnum():
        error("Subsystem name must contain only letters and numbers")

    if subsystem.lower() == subsystem:
        error("Subsystem name should be ClassCased")

    module = subsystem.lower()

    if hasattr(robot, module):
        error("There is already a subsystem named %s" % module)

    with open("subsystems/%s.py" % module, "w") as f:
        f.write(
            """
from wpilib.command import Subsystem

import ports


class {subsystem}(Subsystem):
    \'\'\'Describe what this subsystem does.\'\'\'

    def __init__(self):
        super().__init__('{subsystem}')
""".lstrip().format(
                subsystem=subsystem
            )
        )

    with open("robot.py", "r") as f:
        init = f.read()

    imports = re.compile("(from\s+subsystems\.\w+\s+import\s+[A-Z]\w+\s+as\s+\w+\s*)+")
    match = imports.search(init)

    old = match[0].strip()
    new = "%s\nfrom subsystems.%s import %s as %s"
    init = init.replace(old, new % (old, module, subsystem, module))

    with open("robot.py", "w") as f:
        f.write(init)

    with open("ports.py", "r") as f:
        ports = f.read()

    if not module in ports:
        ports = """
%s
%s = PortsList()
""" % (
            ports,
            module,
        )

    with open("ports.py", "w") as f:
        f.write(ports)

    with open("commands/resetcommand.py") as f:
        resetcommand = f.read()

    requires = re.compile("(self\.requires\(robot.\w+\)\s*)+")
    match = requires.search(resetcommand)

    old = match[0].strip()
    new = "%s\n        self.requires(robot.%s)"
    resetcommand = resetcommand.replace(old, new % (old, module))

    with open("commands/resetcommand.py", "w") as f:
        f.write(resetcommand)

    print("Generated subsystem %s" % subsystem)


def generateCommand():
    if len(sys.argv) >= 3:
        command = sys.argv[2]
    else:
        command = input("Enter a name for your command: ")

    command = command.strip()
    if not command:
        error("Command name must not be blank")

    if command[0].isdigit():
        error("Command name cannot start with a digit")

    if not command.isalnum():
        error("Command name must contain only letters and numbers")

    if command.lower() == command:
        error("Command name should be ClassCased")

    inherits = None
    if command.endswith("CommandGroup"):
        inherits = "CommandGroup"
    elif not command.endswith("Command"):
        command += "Command"

    if command == "DefaultCommand":
        inherits = "Command"

    if inherits is None:
        bases = [
            "InstantCommand",
            "TimedCommand",
            "CommandGroup",
            "Command",
            "DefaultCommand",
        ]
        print("Select a base class:")
        for id, cmd in enumerate(bases):
            print("%d.) %s" % (id, cmd))

        inherits = input("")
        if inherits.isdigit():
            inherits = bases[int(inherits)]

        if not inherits in bases:
            error("Unknown base class %s" % inherits)

    if inherits == "CommandGroup":
        inherits = "fc.CommandFlow"
        if command.endswith("Command"):
            command += "Group"

    if inherits == "DefaultCommand":
        inherits = "Command"
        command = "DefaultCommand"

    # Put spaces before capital letters
    # https://stackoverflow.com/a/199215
    description = re.sub("Command(Group)?$", "", command)
    description = re.sub(r"\B([A-Z])", r" \1", description)

    if inherits == "TimedCommand":
        duration = input("Duration in seconds (leave blank if variable): ")
        duration = duration.strip()
        if duration != "":
            try:
                float(duration)
            except ValueError:
                error("Duration must be a number")

    subsystem = input("Which subsystem is %s for? " % command)
    requirements = subsystem.strip().lower().split()

    for subsystem in requirements:
        if not hasattr(robot, subsystem):
            error("Unknown subsystem %s" % subsystem)

    if command == "DefaultCommand":
        if len(requirements) == 0:
            error("Subsystem is required for DefaultCommand")

        with open("subsystems/%s.py" % requirements[0]) as f:
            content = f.read()

        if "initDefaultCommand" in content:
            error("There is already a default command for this subsystem")

        if ".setDefaultCommand" in content:
            error("There is already a default command for this subsystem")

        content += (
            """

    def initDefaultCommand(self):
        from commands.%s.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())
"""
            % requirements[0]
        )

        with open("subsystems/%s.py" % requirements[0], "w") as f:
            f.write(content)

        description = "Default for %s" % requirements[0]

    path = "commands"
    if len(requirements) > 0:
        if not os.path.isdir("commands/%s" % requirements[0]):
            os.makedirs("commands/%s" % requirements[0])

        path += "/%s" % requirements[0]

    if inherits == "fc.CommandFlow":
        content = "import commandbased.flowcontrol as fc"
    else:
        content = "from wpilib.command import %s" % inherits

        if len(requirements) > 0:
            content += "\n\nimport robot"

    content += "\n\n\nclass %s(%s):\n\n" % (command, inherits)

    if inherits == "TimedCommand" and duration == "":
        content += "    def __init__(self, timeout):\n"
    else:
        content += "    def __init__(self):\n"

    if inherits == "TimedCommand":
        if duration:
            content += "        super().__init__('%s', %s)"
            content = content % (description, duration)
        else:
            content += "        super().__init__('%s', timeout)" % description
    else:
        content += "        super().__init__('%s')" % description

    content += "\n\n"

    if inherits == "fc.CommandFlow":
        content += "        # Add commands here with self.addSequential() and "
        content += "self.addParallel()"

    else:
        if len(requirements) > 0:
            for subsystem in requirements:
                content += "        self.requires(robot.%s)\n" % subsystem

            content += "\n"

        content += "\n    def initialize(self):\n        pass\n\n\n"

        if inherits != "InstantCommand":
            content += "    def execute(self):\n        pass\n\n\n"
            content += "    def end(self):\n        pass\n"

    with open("%s/%s.py" % (path, command.lower()), "w") as f:
        f.write(content)

    print("Created command %s" % command)


def error(msg):
    print("\033[91m%s\033[0m" % msg)
    sys.exit()


def usage():
    usage = """
usage:
    {0} command [CommandName]
    {0} subsystem [SubsystemName]
"""
    print(usage.lstrip().format(sys.argv[0]))
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    if sys.argv[1] == "subsystem":
        generateSubsystem()

    elif sys.argv[1] == "command":
        generateCommand()

    else:
        usage()
