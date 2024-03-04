import __main__
import logging
import json
import os

if __main__.enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("User Permissions")

# Permissions will be implemented once User adding / removing


# Level 1 = Full access of the OS
# Level 2 = Cannot access system but can access PPM
# Level 3 = Cannot access both system and PPM

default_permissions = {
    "root": 1,
    "john": 3
}

if os.path.exists("os_filesystem/system/permissions.json"):
    logger.info("Permissions.json already exists")
else:
    logger.info("Creating permissions")
    f = open("os_filesystem/system/permissions.json", "w+")
    f.write(json.dumps(default_permissions))
    f.close()
    exit()


def LoginCheck(user):
    f = open("os_filesystem/system/permissions.json", "r+")
    permission_data = json.load(f)
    for userd, permission in permission_data.items():
        if userd == user:
            return
    logger.info(f"User {user} has no permissions. Creating permissions for user now")
    permission_data[user] = 3
    f.seek(0)
    f.write(json.dumps(permission_data))
    f.truncate()
    f.close()


def ChangeUserPermissions(command):
    if command[0] == "change_permission":
        if not len(command) == 2:
            print("usage: change_permission <username>")
            return
        if __main__.enviorment_tables["logged_in_user"] != "root":
            print("You are not allowed to access this command.")
            return
        if command[1] == "root":
            print("You cannot change root permissions.")
            return
        f = open("os_filesystem/system/permissions.json", "r")
        permission_data = json.load(f)
        logger.info("loaded permission data")
        for user, permission_level in permission_data.items():
            if user == command[1]:
                print(f"Select permission for account {command[1]}")
                print("[1] Full access of the OS")
                print("[2] Cannot access system folder but can install PPM packages")
                print("[3] Cannot access both system and PPM")
                k = input("Select permission : ")
                f = open("os_filesystem/system/permissions.json", "r+")
                permission_data = json.load(f)
                permission_data[command[1]] = int(k)
                f.seek(0)
                f.write(json.dumps(permission_data))
                f.truncate()
                f.close()


def FSOperationAllowed(username, attempted_access):
    if username == "root":
        logger.info(f"Allowed user root to access {attempted_access}")
        return True

    f = open("os_filesystem/system/permissions.json", "r")
    permission_data = json.load(f)

    for user, permission in permission_data.items():
        if username == user:
            logger.info(f"Got permission level for user")

            if attempted_access == "view_enviorment_vars":
                return True

            if attempted_access == "set_enviorment_vars":
                if permission == 1:
                    logger.info("Allowed user to set environment vars")
                    return True
                else:
                    logger.info("User attempted to change environment table")
                    return False

            if "os_filesystem/system" in attempted_access:
                if permission == 1:
                    logger.info("Allowed user to access system")
                    return True
                else:
                    logger.info("User attempted to access system")
                    return False

            if "os_filesystem/ppm" in attempted_access:
                if permission in (1, 2):
                    logger.info("Allowed user to access ppm fs")
                    return True
                else:
                    logger.info("User attempted to access ppm fs")
                    return False

            if attempted_access == "ppm":
                if permission in (1, 2):
                    logger.info("Allowed user to access ppm")
                    return True
    return False
