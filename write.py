import __main__
import os
import logging
import permissions

if __main__.environment_table["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("write")


def write(command):
    if command[0] == "write":

        if len(command) >= 2:
            file = __main__.environment_table["full_current_directory"] + "/" + command[1]
            if os.path.exists(file):
                print("File already exists")
                return
            if not permissions.FSOperationAllowed(__main__.environment_table["logged_in_user"], file):
                print("You cannot access this file")
                return
            print("Type !!write_exit to exit the program")
            lines = []
            while True:
                user_input = input("")
                if user_input == "!!write_exit":
                    break
                lines.append(user_input)
            print("Saving")
            f = open(file, "w")
            for line in lines:
                f.write(line + "\n")
