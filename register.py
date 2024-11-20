import random
import string
import os
import re
import time
from datetime import datetime, timedelta, date
import sys
from auth import register_user
from login import login_users
from colorama import Fore, Style, Back, init
init(autoreset=True)

width = os.get_terminal_size().columns

def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered 

def center_emoji(emoji):
    """Center the given emoji based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = emoji.center(width)
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

def create_acc():
    clear_screen()
    from maskbook import main
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n")
    print("Join Maskbook")
    print("\n")
    print(center_emoji("♥️  📸 😎"))
    print(center_emoji("🫂 👥 👤"))
    print(Style.DIM + center_text("Create an account to connect with friends, family, and communities of people who share your interests."))
    print(Style.DIM + "—" * width)
    print("\n" + center_text("[5]. " + Back.BLUE + Fore.WHITE + " Get Started " + Style.RESET_ALL))
    print("\n" + center_text("     " + "[6]. " + Back.WHITE + Fore.BLACK + " I already have an account " + Style.RESET_ALL))
    print("\n")
    choice = input(Style.DIM + "\n  What's on your mind  ")

    if choice == '5':
        user = names()  # Start registration and get a User object
        if user:
            dashboard_menu(user)  # Pass User object directly to dashboard_menu

    elif choice == '6':
        user = login_users()  # Login and get a User object
        if user:
            dashboard_menu(user)

    elif choice == 'b':
        time.sleep(2.9)
        return main()

    else:
        print("Invalid option!")
        time.sleep(2.7)
        return create_acc() 
        
def names():
    clear_screen()
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n")
    print(Style.BRIGHT + Fore.WHITE + "  What's your name?")
    print(" ")
    print(Style.DIM + "  Enter the name you use in real life.")
    print("\n")
    first_name = input(Style.DIM + "   Your first name:  "+Style.RESET_ALL)
    if first_name == 'b':
        return create_acc()
    if not first_name:
        print(Fore.RED + "\n" + "Name cannot be empty")
        time.sleep(1)
        return names()
    last_name = input(Style.DIM+"\n   Your Last name:   "+ Style.RESET_ALL)
    if not last_name:
        print(Fore.RED+"\n last name cannot be empty")
        time.sleep(1)
        return names()
    if last_name == "b":
        return names()
    return emails(first_name, last_name)

def emails(first_name, last_name):
    clear_screen()
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n")
    print(Style.BRIGHT + Fore.WHITE + "  What's your email address?")
    print(" ")
    print(Style.DIM + "Enter the email address on which you can be contacted. No one will see this on your profile")
    print("\n")
    email = input(Style.DIM + "What's your email:  ")
    if email == 'b':
        return names()  # Corrected function name
    if not email:
        print(Fore.RED + "\n" + "  Email cannot be empty")
        time.sleep(1)
        return emails(names)
    if not validate_email(email):
        print(Fore.RED + "\n" + "  Invalid email type")
        time.sleep(1)
        return emails(firstname, last_name)
    return passwords(first_name, last_name, email)

def passwords(first_name, last_name, email):
    clear_screen()
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n")
    print(Style.BRIGHT + Fore.WHITE + "  Create a strong password")
    print(" ")
    print(Style.DIM + "Create a very strong password to avoid being hacked. No one will see this on your profile")
    print("\n")
    password = input(Style.DIM + "Create a password:  " + Style.RESET_ALL)
    print("\n")
    confirm_password = input(Style.DIM + "Confirm your password:  " + Style.RESET_ALL)
    if password == 'b':
        return emails(first_name, last_name)
    if not password:
        print(Fore.RED + "\n" + "  Password cannot be empty")
        time.sleep(1)
        return passwords(first_name, last_name, email)
    if password != confirm_password:
        print(Fore.RED + "\n" + "  Passwords do not match")
        time.sleep(1)
        return passwords(first_name, last_name, email)
    return usernames(first_name, last_name, email, password)
        
def usernames(first_name, last_name, email, password):
    clear_screen()
    print(Style.DIM + "  ⬅️" + " .[b]")
    print("\n")
    print(Style.BRIGHT + Fore.WHITE + "  Create a username")
    print(" ")
    print(Style.DIM + "Create a unique username this would be use by friends to find you")
    print("\n")
    username = input("Enter your username: ").strip().lower()  # Convert to lowercase
    if username == "b":
        return passwords(first_name, last_name, email)
    if username.split():
        # Check if the username contains spaces
        # Generate a random string of numbers or letters to append
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        username = ''.join(username.split()) + random_suffix.lower()  # Remove spaces and append random suffix
    register_user(first_name, last_name, email, password, username)        