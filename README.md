Krypton Cougars Robotics
=====
We are the [Krypton Cougars](http://www.team2539.com), [FIRST Robotics Competition](https://www.firstinspires.org/robotics/frc) team 2539 from Palmyra, PA.

This repository holds the control program for our robot. It is written in python and runs on the roboRIO. Additional vision processing is done via a co-processor. That project can also be found in our GitHub account.

Setting up your environment:
--
If you want more in-depth step-by-step instructions for installing this project on various operating systems, check out our [wiki](https://github.com/FRC2539/pybot/wiki/Prepare-Your-Computer).

**Prerequisites**

You must have [python 3](https://www.python.org/downloads/) and [pip 3](https://pip.pypa.io/en/stable/installing/) installed on your system to use this project. Consult your system's documentation for the proper way to install them.

**The simple way**

You must use a Unix-like shell, such as the Linux terminal, the Mac OS X terminal, or the Linux Subsystem on Windows to setup your environment using this method. This will not work in Windows Command Prompt or Powershell. See [the wiki](https://github.com/FRC2539/pybot/wiki/Windows-Setup) for Windows installation instructions.

_The direnv setup script relies on the presence of common utilies like `which` and `curl`, in addition to `python3` and `pip3`_

 1. Install [direnv](https://direnv.net/).
 2. Setup direnv for your shell as described in its documentation. If you don't know which shell you are using, run the following and restart your shell:

    `echo -e '\neval "$(direnv hook bash)"' >> ~/.bashrc`

 3. Clone this project into a local directory

    `git clone https://github.com/FRC2539/pybot.git`

 4. cd into the project

    `cd pybot`

 5. Enable direnv for the repository

    `direnv allow`

 6. Enjoy your completely set-up development environment

Using the program
--
All of the functionality of the project can be run through the robot.py file. There are three modes:

 1. **Test** `./robot.py test` - This mode runs a few sanity checks on the program. It can tell you if there is a syntax error or if it encounters a serious bug. It does not indicate that the program runs correctly, but only that it runs at all.
 2. **Deploy** `./robot.py deploy` - This mode copies the code from your repository to the roboRIO. For that reason, you must be connected to the robot's network before running this command. If you are not connected the command will fail.
 3. **Simulator** `./robot.py sim` - This mode runs the program on a simulated robot, showing you information about the sensors and actuators, and allowing you to view a model of your robot on a top-down projection of the field.

> On Windows, you will need to use `py -3 robot.py` instead of `./robot.py`

Troubleshooting
--
When deploying the program to the robot, you may receive a message telling you that the version of WPILib on the robot does not match your local version. To correct this, you must download updated modules and copy them to the robot:

 1. Connect to the internet
 2. Download the needed code with the [robotpy-installer](http://robotpy.readthedocs.io/en/stable/install/packages.html). Usually this will be only robotpy, but there are other packages that can be downloaded and installed.

    `robotpy-installer download-robotpy`

 3. Connect to the robot's network
 4. Copy the downloaded files to the roboRIO:

    `robotpy-installer install-robotpy`
