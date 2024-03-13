#
# Proton OS | A simple Terminal based Operating system based in Python 3
# Made by Proton0
#


# Core Modules
from colorama import init, Fore
import os
import json
import platform
from timeit import default_timer as timer
import logging

time_since_boot = timer()

start = timer()
init(autoreset=True)

# Configurations and stuff
environment_table = {
    "version": 1.6,
    "user_color": Fore.GREEN,  # System default
    "logged_in_user": "",  # we switch to root once everything has been set-up
    "current_directory": "",
    "full_current_directory": "os_filesystem",
    "machine_name": "",  # all of this will be configured in user.py
    "debug_mode": False,
    "ppm_online_server": "http://127.0.0.1:8080",
    "ppm_allow_online": False,
    "load_modules": True,
    "run_command_as_sudo": False
}
if environment_table["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')

# Create fs folders
if os.path.exists("os_filesystem"):
    logging.info("Filesystem already exists.")
else:
    logging.warning("Filesystem does not exist. Creating one now")
    os.mkdir("os_filesystem")
    os.mkdir("os_filesystem/system")

logger = logging.getLogger("main")

logging.info("Loading modules")
import filesystem
import permissions
import user_color  # User Colors
import users  # User Manager
import write  # Write command
import commands  # Basic Commands


def LoginAPI(username, password):
    users.switch_v2(["switch", username, password])


running_on_mobile_prompt = input("Are you running on mobile (y/n) : ")
if running_on_mobile_prompt == "y" or running_on_mobile_prompt == "yes" or running_on_mobile_prompt == "Y" or running_on_mobile_prompt == "YES":
    running_on_mobile = True
    import mobile.login_ui as login_ui
else:
    print("Not running on mobile")
    import login_ui  # Requirement of LoginAPI

    running_on_mobile = False

def load(command):
    if command[0] == "load":
        if not len(command) >= 2:
            print("Not enough arguments provided for the command")
            return
        try:
            exec(f"import {command[1]}")
        except Exception as e:
            logger.error(f"error : {e}")


# System Commands
system_commands = [
    commands.terminalexit,  # change from sexit to terminalexit because idk it sounds weird
    commands.set_env_variable,
    commands.view,
    load,
    commands.neofetch,
    users.switch_v2,  # replaced switch with the version 2.0
    users.changepassword,
    user_color.ChangeColor,
    filesystem.ls,
    filesystem.cd,
    users.AddUser,
    filesystem.cat,
    filesystem.rm,
    filesystem.rmdir,
    commands.help,
    permissions.ChangeUserPermissions,
    filesystem.pwd,
    filesystem.mkdir,
    commands.echo,
    commands.ps,
    write.write,
    commands.time_took,
    # PPM will load ppm commands (bug fix: ppm modules cant access system_commands)
]

start_ppm = 0
end_ppm = 0
def Load_PPM_Modules():
    global start_ppm, end_ppm
    if not environment_table["load_modules"]:
        return
    start_ppm = timer()
    try:
        logging.info("reading ppm json")
        with open("os_filesystem/system/ppm.json", "r") as f:
            logger.info("parsing ppm")
            ppm_data = json.load(f)
            logger.info("importing packages")
            logger.info(ppm_data)
            for package_name, package_import in ppm_data.items():
                logger.info(f"Loading ppm package {package_name}")
                exec(f"import {package_import}")
    except Exception as e:
        logger.error(f"Failed to import ppm packages : {e}")
    end_ppm = timer()
    logger.info(f"PPM packages took {start_ppm - end_ppm}s to load")


import ppm

logger.info("definied system commands succesfully")

end = timer()

if environment_table["debug_mode"]:
    logger.debug(f"Time took to configure the OS is {start - end} seconds")

# Ask the user to login
print("""
██████╗ ██████╗  ██████╗ ████████╗ ██████╗ ███╗   ██╗     ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗████╗  ██║    ██╔═══██╗██╔════╝
██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██╔██╗ ██║    ██║   ██║███████╗
██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║╚██╗██║    ██║   ██║╚════██║
██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚████║    ╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚══════╝
                                                                          """)
print(f"ProtonOS {environment_table['version']}")
print("Made by Proton0")
if environment_table["logged_in_user"] == "":
    login_ui.LoginUI()
    if environment_table["logged_in_user"] == "":
        print("Unknown error while logging in.")
        exit()
    else:
        # set up
        environment_table["machine_name"] = "protonOS"
        environment_table["current_directory"] = "/"
else:
    environment_table["user_color"] = user_color.LoginGetUsername(environment_table["logged_in_user"])

# Main Terminal
while True:
    user_input = input(
        f"{environment_table['user_color']}{environment_table['logged_in_user']}@{environment_table['machine_name']}{Fore.RESET} {environment_table["current_directory"]} > ").split(
        " ")
    if os.path.isfile(f"{environment_table['full_current_directory']}/{user_input[0]}.proton"):
        if platform.system() == "Darwin" or platform.system() == "Linux":
            os.system(f"bash {environment_table['full_current_directory']}/{user_input[0]}.proton")
        else:
            os.system(f"{environment_table['full_current_directory']}/{user_input[0]}")
    else:
        for command in system_commands:
            try:
                if user_input[0] == "sudo":
                    environment_table["run_command_as_sudo"] = True
                    user_input.remove("sudo")
                    command(user_input)
                else:
                    command(user_input)
            except Exception as e:
                logger.error(f"Error while executing the command : {e}")
