from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import bcrypt
import os
import time
import sys
from update import update_user_profile
from datetime import datetime, timedelta, datetime
from colorama import Fore, Style, Back, init
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Initialize a Console object for rich output
console = Console()

def display_profile(user_id):
    from settings import display_prof
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    my_password = user_data.get("password")
    my_email = user_data.get("email")
    my_first_name = user_data.get("first_name")
    my_last_name = user_data.get("last_name")
    my_username = user_data.get("username")
    
    sett=Table.grid(expand=True)
    sett.add_row("Change password", style="bold")
    sett.add_row("\n")
    sett.add_row("Change Name", style="bold")
    sett.add_row("\n")
    sett.add_row("Change Email", style="bold")
    sett.add_row("\n")
    sett.add_row("Change username", style="bold")
    sett_panel = Panel(sett, title="Login & Recovery", border_style="dim", padding=(1,2))
    title="Password and security "
    mas = "Manage your password, and recovery methods."
    console.print(f"{title}", style="bold", justify="center")
    console.print("\n")
    console.print(mas, style="dim", justify="center")
    console.print("\n", sett_panel)
    action = input(Style.DIM+"\n Whats on your mind:   "+Style.RESET_ALL)
    if action.lower() == 'cp':
        new_password=input(Style.DIM+"\nWhats your new password:   "+Style.RESET_ALL)
        if new_password.lower()== 'b':
            return display_profile(user_id)
        if bcrypt.checkpw(new_password.encode('utf-8'), my_password.encode('utf-8')):
            print(Fore.RED+"\nyour new password cannot be same as old password")
            time.sleep(2)
            return display_profile(user_id)
        hash_new_password= bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')   
        old_password = input(Style.DIM+"enter your old password?  "+Style.RESET_ALL)
        if bcrypt.checkpw(old_password.encode('utf-8'), my_password.encode('utf-8')):
            update_user_profile(user_id, password= hash_new_password)
            return display_profile(user_id)
        else:
            print(Fore.RED+"\n Incorrect old password")
            time.sleep(2)
            return display_profile(user_id)
            
    elif action.lower()== 'b':
        return display_prof(user_id)
            
    elif action.lower() == 'ce':
        new_email = input(Style.DIM+"\nEnter your new email:   "+Style.RESET_ALL)
        if new_email.lower()== 'b':
            return display_profile(user_id)
        if new_email != my_email:
            password=input(Style.DIM+"\nenter your password:  "+Style.RESET_ALL)
            if bcrypt.checkpw(password.encode('utf-8'), my_password.encode('utf-8')):
                update_user_profile(user_id, email= new_email)
                return display_profile(user_id)
            else:
                print(Fore.RED+"\n Incorrect password  ")
                time.sleep(2)
                return display_profile(user_id)
        else:
            print(Fore.RED+"\nNew email cannot be same as old email")
            time.sleep(2)
            return display_profile(user_id)
    elif action == 'cn':
        fn = input(Style.DIM+"\nenter your new first name:   ")
        if fn.lower()=='b':
            return display_profile(user_id)
        ln = input(Style.DIM+"\nenter your new last name")
        if ln.lower()=='b':
            return display_profile(user_id)
        if fn == my_first_name and ln == my_last_name:
            print(Fore.RED+"\nYour new name cannot be same as old name")
            time.sleep(2)
            return display_profile(user_id)
        else:
            update_user_profile(user_id, first_name= fn, last_name= ln)
            return display_profile(user_id)
    elif action == 'cu':
        new_username=input(Style.DIM+"\n enter your new username:   ")
        if new_username != my_username:
            update_user_profile(user_id, username= new_username)
            return display_profile(user_id)
        if new_username.lower()=='b':
            return display_profile(user_id)
        elif new_username == my_username:
            print(Fore.RED+"\n new username cannot be same as old one")
            time.sleep(2)
            return display_profile(user_id)
    else:
        print(Fore.RED+"\nInvalid input")
        time.sleep(2)
        return display_profile(user_id)
            
        
