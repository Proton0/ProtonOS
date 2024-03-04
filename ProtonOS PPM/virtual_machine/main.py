# VERY lightweight version of ProtonOS
from colorama import init, Fore
init(autoreset=True)
import __main__
def startVM(command):
    if command[0] == "start_vm":
        user = "root"
        while True:
            user_input = input(f"{Fore.GREEN}{user}@virtual-machine{Fore.RESET} ~ > ").split(" ")
            if user_input[0] == "exit":
                return
            elif user_input[0] == "switch":
                user = user_input[1]
            elif user_input[0] == "vm":
                print("ProtonOS Virtual Machine version 1.1")
            else:
                print(user_input)

__main__.system_commands.append(startVM)