import platform
import __main__  # in order to access enviorment tables
from timeit import default_timer as timer
import psutil
from prettytable import PrettyTable

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
            except:
                print("Failed to get CPU")
                if platform.processor() == "arm":
                    cpu = "Unknown Apple Silicon CPU"
        else:
            cpu = platform.processor()
        print(f"Hostname : {__main__.enviorment_tables['machine_name']}")
        print(f"Operating System : protonOS {__main__.enviorment_tables['version']}")
        print(f"CPU : {cpu} ({psutil.cpu_percent(interval=1)}% usage)")
        print(f"RAM : {psutil.virtual_memory().total / (1024 * 1024 * 1024)}GB")


def help(command):
    if command[0] == "help":
        print("Basic Commands")
        print("exit             | Exits the program")
        print("install_package  | Installs any package you want using PPM")
        print("uninstall_package| Uninstalls any installed packages")
        print("load             | Load any .py file")
        print("changecolor      | Changes the user's color")
        print("set              | Set environment variables")
        print("view             | View environment variables")
        print("add_user         | Adds a user to the OS")
        print("switch           | Switch users")
        print("change_password  | Changes a user's password")


def ps(command):
    if command[0] == "ps":
        x = PrettyTable()
        time = timer() - __main__.time_since_boot
        x.field_names = ["PID", "TTY", "TIME", "CMD"]
        x.add_row(["0", "?", time, "kernel"])
        x.add_row(["1", "?", time, "filesystem"])
        x.add_row(["2", "?", time, "user_manager"])
        x.add_row(["3", "?", time, "terminal"])
        x.add_row(["4", "?", "?", "ps"])
        print(x)


def time_took(command):
    if command[0] == "time_took":
        x = PrettyTable()
        time = timer() - __main__.time_since_boot
        x.field_names = ["Name", "Time"]

        a = timer() - __main__.time_since_boot
        b = __main__.end_ppm - __main__.start_ppm
        c = __main__.end - __main__.start

        x.add_row(["Time since boot", a])
        x.add_row(["Time took to load PPM Modules", b])
        x.add_row(["Time took to configure OS", c])

        print(x)


def echo(command):
    if command[0] == "echo":
        if len(command) == 2:
            print(command[1])
