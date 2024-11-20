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

def acc_set(user_id):
    clear_screen()
    from update import update_user_profile
    from settings import display_prof
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    my_bio = user_data.get("bio")
    my_profile_picture = user_data.get("profile_picture")
    my_mood = user_data.get("mood")
    my_hidden_talent = user_data.get("hidden_talents")
    my_essence = user_data.get("essence")
    
    sett=Table.grid(expand=True)
    sett.add_row("profile picture", style="bold")
    sett.add_row("\n")
    sett.add_row("Change Bio", style="bold")
    sett.add_row("\n")
    sett.add_row("Change essence", style="bold")
    sett.add_row("\n")
    sett.add_row("Change mood", style="bold")
    sett.add_row("\n")
    sett.add_row("Change hidden talent", style="bold")
    sett_panel = Panel(sett, title="Profile settings", border_style="dim", padding=(1,2))
    title="Account settings "
    mas = "Manage your profile details."
    console.print(f"{title}", style="bold", justify="center")
    console.print("\n")
    console.print(mas, style="dim", justify="center")
    console.print("\n", sett_panel)
    action = input(Style.DIM+"\n Whats on your mind:   "+Style.RESET_ALL)
    if action.lower() == 'pp':
        new_profile = input(Style.DIM + "\nEnter your new profile (emojis only):   ")
        if new_profile.lower()== 'b':
            return acc_set(user_id)

        # Check if the input contains only non-emoji characters (printable and alphabetic)
        if new_profile.isalpha() or new_profile.isprintable() and not any(ord(char) > 10000 for char in new_profile):
            print(Fore.RED + "\n Profile picture must be an emoji, not plain text!")
            return acc_set(user_id)  # Return to account settings if invalid
        else:
            comfirm = input(Style.DIM + f"\nDo you want to change your profile to {new_profile} (y/n):  " + Style.RESET_ALL)

            if comfirm.lower() == 'y':
                update_user_profile(user_id, profile_picture=new_profile)
            else:
                return acc_set(user_id)
    elif action.lower()== 'b':
        return display_prof(user_id)
                
    elif action.lower()== 'cb':
        new_bio=input(Style.DIM+"\nWhat is your bio:   "+Style.RESET_ALL)
        if new_bio.lower()== 'b':
            return acc_set(user_id)
        if new_bio != my_bio:
            update_user_profile(user_id, bio= new_bio)
        else:
            print(Fore.RED+"\nnew bio is same as old")
            time.sleep(1.5)
            return acc_set(user_id)
    elif action.lower()== 'ce':
        new_essence=input(Style.DIM+"\nWhat is your essence:  "+Style.RESET_ALL)
        if new_essence.lower()=='b':
            return acc_set(user_id)
        if new_essence != my_essence:
            update_user_profile(user_id, essence= new_essence)
        else:
            print(Fore.RED+"\nnew essence is same as old")
            time.sleep(1.5)
            return acc_set(user_id)
    elif action.lower()== 'cm':
        new_mood=input(Style.DIM+"\nWhat is your mood:  "+Style.RESET_ALL)
        if new_mood.lower()== 'b':
            return acc_set(user_id)
        if new_mood != my_mood:
            update_user_profile(user_id, mood= new_mood)
        else:
            print(Fore.RED+"\nnew mood is same as old")
            time.sleep(1.5)
            return acc_set(user_id)
    elif action.lower()== 'cht':
        new_hidden=input(Style.DIM+"\nWhat is your hidden talents:  "+Style.RESET_ALL)
        if new_hidden.lower()== 'b':
            return acc_set(user_id)
        if new_hidden != my_hidden_talent:
            update_user_profile(user_id, hidden_talents= new_hidden)
        else:
            print(Fore.RED+"\nnew hidden talent is same as old")
            time.sleep(1.5)
            return acc_set(user_id) 
            
    else:
        print(Fore.RED+"invalid input")
        time.sleep(1.5) 
        return acc_set(user_id)