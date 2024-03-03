import os
import __main__

def Nano(command):
    if command[0] == "nano":
        if not len(command) == 2:
            print("usage: nano <filename>")
            print("Note: this will launch your system's nano cuz too lazy to recreate it lolol")
            print("Note: This approach is specific to MacOS and might not be portable to other systems.")
            return

        # Construct the command string, including the full path to nano
        nano_command = f"open -a Terminal.app /usr/bin/nano {os.getcwd()}/{__main__.enviorment_tables['full_current_directory']}"
        os.system(nano_command)
__main__.system_commands.append(Nano)