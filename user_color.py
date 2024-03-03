import __main__
from colorama import Fore, init
init(autoreset=True)
import json
import logging
import os

if __main__.enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("User Colors")
logger.info("User Colors loaded")

default_colors = {
    "root": Fore.RED,
    "john": Fore.BLUE,
    "system": Fore.GREEN # system will be used when no colors are set for the account
}

if os.path.exists("os_filesystem/system/user_colors.json"):
    logger.info("User Colors json already exists")
else:
    f = open("os_filesystem/system/user_colors.json", "w")
    f.write(json.dumps(default_colors))
    f.close()
    if not f.closed:
        f.close()
    logger.info("User Colors config created")

def LoginGetUsername(username):
    logger.info("Getting color for username : {}".format(username))
    try:
        f = open("os_filesystem/system/user_colors.json", "r")
        k = json.load(f)
        for key, value in k.items():
            if username == key:
                return value
    except Exception as e:
        logger.error(f"Error while getting the color for {username} : {e}")
        return Fore.GREEN
    logger.warning(f"The user {username} does not have a system color set.")

def ChangeColor(command):
    if command[0] == "changecolor":
        f = open("os_filesystem/system/user_colors.json", "r+")
        k = json.load(f)
        user = __main__.enviorment_tables["logged_in_user"]
        print("Please select any color you want")
        print(f"[1] {Fore.RED} RED")
        print(f"[2] {Fore.BLUE} BLUE")
        print(f"[3] {Fore.GREEN} GREEN")
        print(f"[4] {Fore.YELLOW} YELLOW")
        print(f"[5] {Fore.CYAN} CYAN")
        print(f"[6] {Fore.WHITE} WHITE")
        print(f"[7] {Fore.BLACK} BLACK")
        print(f"[8] {Fore.MAGENTA} MAGENTA")
        z = input("Select a number : ")
        if z == "1":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.RED
        elif z == "2":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.BLUE
        elif z == "3":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.GREEN
        elif z == "4":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.YELLOW
        elif z == "5":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.CYAN
        elif z == "6":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.WHITE
        elif z == "7":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.BLACK
        elif z == "8":
            k[__main__.enviorment_tables["logged_in_user"]] = Fore.MAGENTA
        print("Saving color...")
        f.seek(0)
        f.write(json.dumps(k))
        __main__.enviorment_tables["user_color"] = k[__main__.enviorment_tables["logged_in_user"]]
        f.truncate()
        f.close()