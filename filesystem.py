import __main__
import shutil
import permissions
import os
import logging
from colorama import Fore, init

init(autoreset=True)

if __main__.environment_table["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("Filesystem")
logger.info("Filesystem module loaded.")

if os.path.exists("os_filesystem"):
    logger.info("Filesystem already exists.")
else:
    logger.warning("Filesystem does not exist. Creating one now")
    os.mkdir("os_filesystem")
    os.mkdir("os_filesystem/system")
    print("FS setup completed. Please relaunch ProtonOS")
    exit()

# Easter egg :D
if os.path.exists("os_filesystem/secrets/easter_egg"):
    print("secret :D")


def corrupted(reason):
    logging.error("Filesystem is corrupted. Launching FS Recovery!")
    print("ProtonOS Filesystem Recovery")
    print(f"There was an error with the filesystem ({reason})")
    print("Because of this. It is recommended that the filesystem gets wiped and recreated")
    print("If the filesystem gets recreated then ALL DATA ON THE FILESYSTEM WILL BE LOST (Including system settings)")
    k = input("Press Y to re-create the filesystem")
    if k == "Y" or k == "y":
        print("Please wait")
        logging.info("Re-creating the filesystem")
        shutil.rmtree("os_filesystem")
        logging.info("Deleted old filesystem. Recreating the filesystem now")
        os.mkdir("os_filesystem")
        os.mkdir("os_filesystem/system")
        print(
            "Filesystem re-created succesfully. ProtonOS will close you will need to re-launch it for the filesystem to be fully recreated")
        exit()
    else:
        exit(44)


def cd(command):
    if command[0] == "cd":
        if not len(command) == 2:
            print("not enough args")
            return
        if command[1] == "..":
            # Go back a directory
            if __main__.environment_table["full_current_directory"] == "os_filesystem":
                __main__.environment_table["current_directory"] = "/"
                __main__.environment_table["full_current_directory"] = "/"
            else:
                current_directory_parts = __main__.environment_table["full_current_directory"].split("/")
                parent_directory_parts = current_directory_parts[:-1]
                parent_directory = "/".join(parent_directory_parts)
                parent_directory_name = parent_directory_parts[-1]
                if parent_directory_name == "os_filesystem":
                    __main__.environment_table["current_directory"] = "/"
                else:
                    __main__.environment_table["current_directory"] = parent_directory_name
                if parent_directory == "/" or parent_directory == "":
                    __main__.environment_table["full_current_directory"] = "os_filesystem"
                else:
                    __main__.environment_table["full_current_directory"] = parent_directory
            return
        if not permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'],
                                              __main__.environment_table["full_current_directory"] + "/" + command[1]):
            print("permission error")
            return
        __main__.environment_table["current_directory"] = command[1]
        __main__.environment_table["full_current_directory"] = __main__.environment_table[
                                                                   "full_current_directory"] + "/" + command[1]


def ls(command):
    if command[0] == "ls":

        if len(command) == 2:
            if not permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'],
                                                  f"os_filesystem/{command[1]}"):
                print("permission error")
                return
            k = os.listdir("os_filesystem/" + command[1])
            for f in k:
                print(f)
            return
        if __main__.environment_table["current_directory"] == "/":
            k = os.listdir("os_filesystem")
            for f in k:
                if permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'], f"os_filesystem/{f}"):
                    print(f"{Fore.GREEN}{f}")
                else:
                    print(f"{Fore.RED}{f}")
            return
        else:
            k = os.listdir(__main__.environment_table["full_current_directory"])
            for f in k:
                print(f)
            return


def cat(command):
    if command[0] == "cat":
        if len(command) == 2:
            if not permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'],
                                                  __main__.environment_table["full_current_directory"]):
                print("permission error")
                return
            f = open(__main__.environment_table["full_current_directory"] + "/" + command[1], "r")
            for line in f.readlines():
                print(line)


def rm(command):
    if command[0] == "rm":
        if len(command) == 3:
            if command[1] == "-rf":
                if command[2] == "/":
                    k = input("Are you sure you want to delete the entire filesystem (y/n) : ")
                    if k.lower() == "y" or k.lower() == "yes":
                        print("Deleting filesystem")
                        if not permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'],
                                                              "os_filesystem/system"):
                            print("You arent allowed to do this")
                            return
                        shutil.rmtree("os_filesystem")
                        print("Critical error")
                        exit()
                    else:
                        print("Cancelled")
        if len(command) == 2:
            if not permissions.FSOperationAllowed(__main__.environment_table["logged_in_user"],
                                                  __main__.environment_table["full_current_directory"] + "/" + command[
                                                      1]):
                print("permission error")
                return
            if os.path.isfile(__main__.environment_table["full_current_directory"] + "/" + command[1]):
                os.remove(__main__.environment_table["full_current_directory"] + "/" + command[1])
            else:
                shutil.rmtree(__main__.environment_table["full_current_directory"] + "/" + command[1])


def rmdir(command):
    if command[0] == "rmdir":
        rm(["rm", command[1]])


def pwd(command):
    if command[0] == "pwd":
        print(__main__.environment_table['full_current_directory'])


def mkdir(command):
    if command[0] == "mkdir":
        if len(command) == 2:
            if not permissions.FSOperationAllowed(__main__.environment_table['logged_in_user'],
                                                  __main__.environment_table['full_current_directory'] + "/" + command[
                                                      1]):
                print("permission error")
                return
            else:
                os.mkdir(__main__.environment_table["full_current_directory"] + "/" + command[1])
