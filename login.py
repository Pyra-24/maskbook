import os
import sys
import re
import time
from datetime import datetime, timedelta, date
from getpass import getpass
from auth import login_user
from colorama import Fore, Style, Back, init
init(autoreset=True)

def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered 
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def validate_email(email):
    # Define the regex pattern for a valid email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Check if the input matches the email pattern
    if re.match(email_regex, email):
        return True
    else:
        return False       

def login_users():
    from maskbook import main
    clear_screen()
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n\n")
    print(Fore.BLUE + Style.BRIGHT + center_text("Maskbook"))
    print("\n\n")
    
    email = input(Style.DIM + "Email address:   " + Style.RESET_ALL).strip()
    if email == 'b':
        return main()
    if not validate_email(email):
        print(Style.DIM+Fore.RED+"\nInvalid email type")
        time.sleep(2)
        return login_users()
    
    password = getpass(Style.DIM + "\n" + "Enter password:  ")
    if password.lower() == 'b':
        return login_users()
    login_user(email, password)    