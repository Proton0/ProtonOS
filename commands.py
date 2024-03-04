import platform
import __main__  # in order to access enviorment tables

import psutil
import sys


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
        cpu = "Unknown CPU"
        if platform.system() == "Darwin":
            try:
                cpu = psutil.cpu_times().physical_id
            except Exception as e:
                print("Failed to get CPU")
                if platform.processor() == "arm":
                    cpu = "Unknown Apple Silicon CPU"
        else:
            cpu = platform.processor()
        print(f"Hostname : {__main__.enviorment_tables['machine_name']}")
        print(f"Operating System : protonOS {__main__.enviorment_tables['version']}")
        print(f"CPU : {cpu} ({psutil.cpu_percent(interval=1)}% usage)")
        print(f"RAM : {psutil.virtual_memory().total / (1024 * 1024 * 1024)}GB")
