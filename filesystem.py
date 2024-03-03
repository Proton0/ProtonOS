import __main__
import shutil
import os
import logging

if __main__.enviorment_tables["debug_mode"]:
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
        print("Filesystem re-created succesfully. ProtonOS will close you will need to re-launch it for the filesystem to be fully recreated")
        exit()
    else:
        exit(44)

def cd(command):
    if command[0] == "cd":
        if not len(command) > 2:
            print("not enough args")
            return
        if command[1] == "..":
            # go back a directory
            if __main__.enviorment_tables["full_current_directory"] == "os_filesystem":
                __main__.enviorment_tables["current_directory"] == "/"
            return
        __main__.enviorment_tables["current_directory"] = command[1]
        __main__.enviorment_tables["full_current_directory"] = __main__.enviorment_tables["full_current_directory"] + "/" + command[1]

def ls(command):
    if command[0] == "ls":
        if len(command) > 2:
            k = os.listdir("os_filesystem/" + command[1])
            for f in k:
                print(f)
            return
        if __main__.enviorment_tables["current_directory"] == "/":
            k = os.listdir("os_filesystem")
            for f in k:
                print(f)
            return
        else:
            k = os.listdir(__main__.enviorment_tables["full_current_directory"])
            for f in k:
                print(f)
            return