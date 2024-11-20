from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
import os
from colorama import Fore, Style
from database import db_connection
import time
from profile import user_profile
from datetime import datetime, timedelta, datetime

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def user_dashboard(user_id):
    from chat_client import display_friends
    from auth import set_user_online_status
    from feeds import feeds
    from maskbook import main
    from friend import find_friend
    from settings import display_prof
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    profile_picture = user_data.get("profile_picture")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")

    # Create the main layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=6),  # Profile section below the menu
        Layout(name="invite_section", size=5),  # Invite friends section below profile
        Layout(name="dashboard")  # Dashboard as the main content
    )

    # Menu Layout - separated at the top
    console.print("   ⬅️ MENU", style="bold", justify="left")
    console.print("\n")
    my_status = user_data.get("online_status")
    status = Text(f"    {my_status}", style="bold green")
    # Header Layout with Profile Info
    header_content = Text.assemble(
        (f"{profile_picture} {first_name} {last_name}", "bold"),     status
    )
    
    layout["header"].update(Panel(header_content, padding=(1, 2), title_align="center"))

    # Invite Friends Section
    invite_friends = Panel("👥 Invite friends", style="dim", border_style="dim", padding=(1, 2))
    layout["invite_section"].update(invite_friends)

    # Dashboard Layout - 3x4 grid as per the image
    layout["dashboard"].split_row(
        Layout(name="column1"),
        Layout(name="column2"),
        Layout(name="column3"),
        Layout(name="column4")
    )

    # Each column in the dashboard
    dashboard_items = [
        Panel("   💬 MSG", style="dim", padding=(1, 3), title_align="center"),
        Panel("   🔐 SET", style="dim", padding=(1, 3), title_align="center"),
        Panel(" ✅ verify", style="dim", padding=(1, 3), title_align="center"),
        Panel("\n 📰 Feeds", style="dim", padding=(1, 2), title_align="center"),
        Panel("   👤 PROF", style="dim", padding=(1, 3), title_align="center"),
        Panel("  🚫 BAN", style="dim", padding=(1, 3), title_align="center", border_style="dim"),
        Panel("  Logout", style="dim", padding=(1, 3), title_align="center", border_style="dim"),
        Panel("  🔍 SRCH", style="dim", padding=(1, 3), title_align="center", border_style="dim")
    ]

    # Distribute items into columns
    layout["column1"].split_column(*dashboard_items[:2])  # First two items
    layout["column2"].split_column(*dashboard_items[2:4])  # Next two items
    layout["column3"].split_column(*dashboard_items[4:6])  # Remaining two items
    layout["column4"].split_column(*dashboard_items[6:])  # Remaining two items


# Render the entire layout
    console.print(layout)
    console.print("\n")
    action=input(Style.DIM+"Whats on your mind  "+Style.RESET_ALL)
    if action == 'f':
        return feeds(user_id)
    elif action == 'b':
        return feeds(user_id)    
    elif action.lower() == 'prof':
        return user_profile(user_id)
    elif action == 'msg':
        return display_friends(user_id)
    elif action == 'ban':
        print(Fore.RED+"\nCannot report users at the moment")
        time.sleep(2)
        return user_dashboard(user_id)
    elif action.lower() == 'l':
        set_user_online_status(user_data, user_id, status="offline")
        return main()
    elif action == 'set':
        return display_prof(user_id)
    elif action.lower()=='srch':
        return find_friend(user_id)
    else:
        print(Fore.RED+"Invalid input...")
        time.sleep(2)
        return user_dashboard(user_id)