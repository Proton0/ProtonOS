import __main__
import logging
from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel

# Setup logging
if __main__.environment_table["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("Login UI")

# Create the CustomTkinter window and widgets
root = CTk()
root.geometry("300x150")  # Set a reasonable window size

username_label = CTkLabel(root, text="Username", width=15)
username_entry = CTkEntry(root)
password_label = CTkLabel(root, text="Password", width=15)
password_entry = CTkEntry(root, show="*")  # Hide password characters

info_label = CTkLabel(root, text="The default password for 'root' is 'root'")
submit_button = CTkButton(root, text="Submit")

# Arrange the widgets using grid layout
username_label.grid(row=0, column=0)
username_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
info_label.grid(row=2, columnspan=2)
submit_button.grid(row=3, columnspan=2)  # Span across both columns


def LoginUI():
    logger.info("creating the window")
    submit_button.bind("<Button-1>", handle_button_click)
    root.mainloop()  # Start the Tkinter main event loop


def handle_button_click(event):
    username = username_entry.get()
    password = password_entry.get()
    __main__.LoginAPI(username, password)

    if __main__.environment_table["logged_in_user"] == username:
        root.quit()
        root.destroy()
        # Close the window on successful login
        return
    else:
        # Display error message (you can use a custom dialog library for a better experience)
        print("Incorrect username or password")
