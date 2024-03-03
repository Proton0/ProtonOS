#
# Proton OS | A simple Terminal based Operating system based in Python 3
# Made by Proton0
#


# Core Modules
from colorama import init, Fore
import sys
import threading
import json
from timeit import default_timer as timer
import logging

start = timer()
init(autoreset=True)

# Configurations and stuff
enviorment_tables = {
    "version": 1.0,
    "user_color": Fore.GREEN,  # System default
    "logged_in_user": "",  # we switch to root once everything has been set-up
    "current_directory": "",
    "full_current_directory": "os_filesystem",
    "machine_name": "",  # all of this will be configured in user.py
    "debug_mode": True,
    "ppm_online_server": "http://127.0.0.1:8080",
    "ppm_allow_online": True,
}

# configure if being debugged and the logger
if not enviorment_tables["debug_mode"]:
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        enviorment_tables["debug_mode"] = False
        logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
    elif gettrace():
        print("Debug mode enabled.")
        enviorment_tables["debug_mode"] = True
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
    else:
        enviorment_tables["debug_mode"] = False
        logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    print("Debug mode is enabled")
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("main")
# load FS
logger.info("Loading the filesystem now!")
import filesystem

# load modules and stuff
logging.info("Loading user colors")
import user_color  # User Colors

logger.info("Loading user manager")
import users  # User Manager

logging.info("Loading commands")
import commands  # Basic Commands

# System Commands
system_commands = [
    commands.terminalexit,  # change from sexit to terminalexit because idk it sounds weird
    commands.set_env_variable,
    commands.view,
    commands.load,
    commands.neofetch,
    users.switch,
    users.changepassword,
    user_color.ChangeColor,
    filesystem.ls,
    filesystem.cd,
    users.AddUser
    # PPM will load ppm commands (bug fix: ppm modules cant access system_commands)
]

# Proton Package Manager Watchdog
from watchdog import watchdog

# Proton Package Manager Loader
last_imported_module = None

def Load_PPM_Modules():
    global last_imported_module
    try:
        logging.info("reading ppm json")
        with open("os_filesystem/system/ppm.json", "r") as f:
            logging.info("parsing ppm")
            ppm_data = json.load(f)
            logging.info("importing packages")
            logging.info(ppm_data)
            for package_name, package_import in ppm_data.items():
                logger.info(f"Loading ppm package {package_name}")
                last_imported_module = package_name
                watchdog_thread = threading.Thread(target=watchdog, args=(package_name, last_imported_module))
                watchdog_thread.start()
                exec(f"import {package_import}")
                watchdog_thread.join()  # Wait for watchdog to finish before importing next module
    except Exception as e:
        logger.error(f"Failed to import ppm packages : {e}")


import ppm

logger.info("definied system commands succesfully")

end = timer()

if enviorment_tables["debug_mode"]:
    logger.debug(f"Time took to configure the OS is {end - start} seconds")

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
    for command in system_commands:
        try:
            command(user_input)
        except Exception as e:
            logger.error(f"Error while executing the command : {e}")
