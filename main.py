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

start = timer()
init(autoreset=True)

# Configurations and stuff
enviorment_tables = {
    "version": 1.2,
    "user_color": Fore.GREEN,  # System default
    "logged_in_user": "",  # we switch to root once everything has been set-up
    "current_directory": "",
    "full_current_directory": "os_filesystem",
    "machine_name": "",  # all of this will be configured in user.py
    "debug_mode": True,
    "ppm_online_server": "http://127.0.0.1:8080",
    "ppm_allow_online": True,
    "load_modules": True,
}

if enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')

# create FS
if os.path.exists("os_filesystem"):
    logging.info("Filesystem already exists.")
else:
    logging.warning("Filesystem does not exist. Creating one now")
    os.mkdir("os_filesystem")
    os.mkdir("os_filesystem/system")
    print("FS setup completed. Please relaunch ProtonOS")
    exit()


logger = logging.getLogger("main")
logger.info("Loading the filesystem now!")
import filesystem

# load permissions
import permissions
# load FS

# load modules and stuff
logging.info("Loading user colors")
import user_color  # User Colors

logger.info("Loading user manager")
import users  # User Manager

logging.info("Loading commands")
import commands  # Basic Commands


def load(command):
    if command[0] == "load":
        if not len(command) >= 2:
            print("Not enough arguments provided for the command")
            return
        try:
            exec(f"import {command[2]}")
        except Exception as e:
            logger.error(f"error : {e}")

# System Commands
system_commands = [
    commands.terminalexit,  # change from sexit to terminalexit because idk it sounds weird
    commands.set_env_variable,
    commands.view,
    load,
    commands.neofetch,
    users.switch,
    users.changepassword,
    user_color.ChangeColor,
    filesystem.ls,
    filesystem.cd,
    users.AddUser,
    filesystem.cat,
    filesystem.rm,
    filesystem.rmdir
    # PPM will load ppm commands (bug fix: ppm modules cant access system_commands)
]

def Load_PPM_Modules():
    if not enviorment_tables["load_modules"]:
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

if enviorment_tables["debug_mode"]:
    logger.debug(f"Time took to configure the OS is {start - end} seconds")

# Ask the user to login

print(f"ProtonOS {enviorment_tables['version']}")
print("Made by Proton0")
if enviorment_tables["logged_in_user"] == "":
    user = input("Enter username (default is root) : ")
    if user == "":
        user = "root"
    password = input(f"Enter password for user {user} : ")
    users.switch(["switch", user, password])

    if enviorment_tables["logged_in_user"] == "":
        logger.error("An error while logging in. Most likely you have entered the wrong username or password")
        exit()
    else:
        # set up
        enviorment_tables["machine_name"] = "protonOS"
        enviorment_tables["current_directory"] = "/"
else:
    enviorment_tables["user_color"] = user_color.LoginGetUsername(enviorment_tables["logged_in_user"])

# Main Terminal
while True:
    user_input = input(
        f"{enviorment_tables['user_color']}{enviorment_tables['logged_in_user']}@{enviorment_tables['machine_name']}{Fore.RESET} {enviorment_tables["current_directory"]} > ").split(
        " ")
    if os.path.isfile(f"{enviorment_tables['full_current_directory']}/{user_input[0]}.proton"):
        if platform.system() == "Darwin" or platform.system() == "Linux":
            os.system(f"bash {enviorment_tables['full_current_directory']}/{user_input[0]}.proton")
        else:
            os.system(f"{enviorment_tables['full_current_directory']}/{user_input[0]}")
    else:
        for command in system_commands:
            try:
                command(user_input)
            except Exception as e:
                logger.error(f"Error while executing the command : {e}")
