import platform
import __main__  # in order to access enviorment tables


def terminalexit(command):
    if command[0] == "exit":
        exit()


def set_env_variable(command):
    if command[0] == "set":
        if len(command) >= 3:  # Checking if there are enough elements in the command
            if command[1] == "logged_in_user":
                print("Operation not permitted.")
                return
            key = command[1]
            value = command[2]
            __main__.enviorment_tables[key] = value
        else:
            print("Insufficient arguments provided for the set command.")


def view(command):
    if command[0] == "view":
        for key, value in __main__.enviorment_tables.items():
            print(f"{key} : {value}")


def neofetch(command):
    if command[0] == "neofetch":
        print(f"System : {platform.system()}")
        print(f"Version : {platform.version()}")
        print(f"Release : {platform.release()}")
        print(f"CPU : {platform.processor()}")
        print(f"Architecture : {platform.architecture()}")
        print(f"Console : ProtonOS Emulated Console")
