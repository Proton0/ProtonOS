import __main__
import os
import hashlib
import logging
import json

import user_color
import permissions

if __main__.environment_table["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("User Manager")
logger.info("User module loaded")

default_users = {
    "john": "63a9f0ea7bb98050796b649e85481845",  # MD5 hash of the password "root"
    "root": "63a9f0ea7bb98050796b649e85481845"  # MD5 hash of the password "root"
}

if os.path.exists("os_filesystem/system/users.json"):  # Check if it already exists. If not then we just create it
    logger.info("Users.json file already exist.")
else:
    logger.warning("Users.json file does not exist. Creating one now")  # create and put default_users
    fs = open("os_filesystem/system/users.json", "w+")
    fs.write(json.dumps(default_users))
    fs.close()
    logger.info("Succesfully created users.json")


def switch_v2(command):
    if command[0] == "switch":  # Check if arugments is enough
        if command[0][1] == "":
            print("Please enter a valid username")
            return
        if command[0][2] == "":
            print("Please enter a valid password")
        if not len(command) >= 2:
            print("Not enough arguments provided for the command")
            return
        if command[1] == __main__.environment_table["logged_in_user"]:  # preventing switching to the same account
            print("You are already logged in as the user!")
            return
        logger.info("Reading user data file")
        f = open("os_filesystem/system/users.json", "r")  # Read the hashes of accounts
        data = json.load(f)
        for key, value in data.items():
            if key == command[1]:
                try:
                    md5 = hashlib.md5(command[2].encode()).hexdigest()
                    if md5 == value:
                        print("Logged in succesfully")

                        # setup the user account
                        __main__.environment_table["logged_in_user"] = command[1]
                        permissions.LoginCheck(command[1])
                        __main__.environment_table["user_color"] = user_color.LoginGetUsername(command[1])
                        __main__.environment_table["full_current_directory"] = "os_filesystem"
                        __main__.environment_table["full_current_directory"] = "os_filesystem"
                        return True
                    else:
                        print("Incorrect password")
                        return False
                except Exception as e:
                    logger.error(f"Error while logging in : {e}")
                    return False

def switch(command):
    logger.warning("users.switch() is deprecated. Use switch_v2 instead")

    if command[0] == "switch":  # Check if arugments is enough
        if command[0][1] == "":
            print("Please enter a valid username")
            return
        if command[0][2] == "":
            print("Please enter a valid password")
        if not len(command) >= 2:
            print("Not enough arguments provided for the command")
            return
        if command[1] == __main__.environment_table["logged_in_user"]:  # preventing switching to the same account
            print("You are already logged in as the user!")
            return

        logger.info("Reading user data file")
        f = open("os_filesystem/system/users.json", "r")  # Read the hashes of accounts
        data = json.load(f)
        for key, value in data.items():
            logger.debug(f"{key} {value}")
            if key == command[1]:
                # hash command[2] and compare
                md5 = hashlib.md5(
                    command[2].encode()).hexdigest()  # Hash the password
                if md5 == value:
                    logger.info("hash matched")

                    # Update logged_in_user after successful password check
                    __main__.environment_table["logged_in_user"] = command[1]
                    __main__.environment_table["user_color"] = user_color.LoginGetUsername(command[1])
                    permissions.LoginCheck(command[1])  # Permissions and stuff ykyk
                    __main__.environment_table["current_directory"] = "/"
                    __main__.environment_table["full_current_directory"] = "os_filesystem"
                else:
                    print("Password does not match")
                    logger.info(f"expected : {value} but got : {md5}")


def AddUser(command):
    if command[0] == "add_user":
        if not len(command) == 3:
            print("Usage: add_user <username> <password>")
            return
        logging.info("hashing password")
        pw_hash = hashlib.md5(command[3].encode()).hexdigest()
        f = open("os_filesystem/system/users.json", "r+")
        user_data = json.load(f)  # Load JSON
        user_data[command[1]] = pw_hash  # Set username to hash
        f.seek(0)
        f.write(json.dumps(user_data))  # write
        f.truncate()
        f.close()  # close
        print("User created.")


def changepassword(command):
    if command[0] == "changepassword":
        print("Command n")
        if not len(command) >= 3:  # changepassword <username> <password>
            print("Not enough arguments provided for the command")
            return
        print(f"Changing account {command[1]}'s password to {command[2]}")
        logging.info(f"Hash of new password is {hashlib.md5(command[2].encode()).hexdigest()}")
        f = open("os_filesystem/system/users.json", "r+")  # open
        user_data = json.load(f)  # load json
        user_data[command[1]] = hashlib.md5(command[2].encode()).hexdigest()  # set user's password to hashed password
        f.seek(0)
        f.write(json.dumps(user_data))  # write
        f.truncate()
        f.close()  # close
