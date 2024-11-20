from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import os
import time
import sys
from datetime import datetime, timedelta, datetime
from colorama import Fore, Style, Back, init
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Initialize a Console object for rich output
console = Console()

def display_prof(user_id):
    from dashboard import user_dashboard
    from account import acc_set
    from security import display_profile
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    profile_picture= user_data.get("profile_picture")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    setting_table = Table.grid(expand=True)
    setting_table.add_row("👤 Accounts ")
    setting_table.add_row("\n")
    setting_table.add_row("🔐 Password & Security")
    set_panel= Panel(setting_table, title="Accounts settings", border_style="dim", padding=(1,2))
    maskbook_logo = title="🐍 Pyra"
    prof_set= title="Accounts Center"
    prof_top = "\nManage your account settings across Pyra technologies. "
    profile= (f"  {profile_picture}  {first_name} {last_name}")
    console.print(maskbook_logo, justify="center", style="dim")
    console.print("\n")
    console.print(prof_set, style="bold", justify="center")
    console.print(prof_top, style="dim", justify="center")
    console.print("\n")
    console.print(Panel(profile, title="Profiles", border_style="bold", style="dim"))
    console.print("\n", set_panel)
    action= input(Style.DIM+"\nWhats on your mind   "+Style.RESET_ALL)
    if action == 'a':
        return acc_set(user_id)
    elif action == 'ps':
        return display_profile(user_id)
    elif action == 'b':
        return user_dashboard(user_id)
    else:
        print(Fore.RED+"\n Invalid input")
        time.sleep(2)
        return display_prof(user_id)
