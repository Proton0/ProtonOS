# VERY lightweight version of ProtonOS
from colorama import init, Fore
init(autoreset=True)
import __main__
def startVM(command):
    if command[0] == "start_vm":
        while True:
            user_input = input(f"{Fore.GREEN}root@virtual-machine{Fore.RESET} ~ > ")
            if user_input == "exit":
                return
            print(user_input)

__main__.system_commands.append(startVM)