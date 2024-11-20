from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
import time
import os
import sys
from datetime import datetime, timedelta, datetime
from colorama import Fore, Style, Back, init
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Initialize the console
console = Console()

def user_profile(user_id):
    from dashboard import user_dashboard
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    # Define user profile data
    profile_emoji = user_data.get("profile_picture")  # Masked emoji
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    username = user_data.get("username")
    following = user_data.get("following_count")
    followers = user_data.get("followers_count")
    posts = user_data.get("posts_count")
    bio = user_data.get("bio")
    essence = user_data.get("essence")
    mood = user_data.get("mood")
    hidden_talents = user_data.get("hidden_talents")
    # Profile Header
    profile_header = Table.grid(expand=True)
    profile_header.add_column(justify="center")
    profile_header.add_row("\n")
    profile_header.add_row(f"[bold]{profile_emoji}  {first_name} {last_name}[/bold]")
    profile_header.add_row("")
    profile_header.add_row(f"[dim]@ {username}[/dim]")
    profile_header.add_row("\n")
    profile_header.add_row(f"[bold]Followers:[/bold] {followers}  |  [bold]Following:[/bold] {following}  |  [bold]Posts:[/bold] {posts}")

    # Bio Panel
    bio_panel = Panel(Text(bio, style="italic"), title="Bio", border_style="blue")

    # Additional Info Panels
    essence_panel = Panel(Text(essence, style="italic magenta"), title="Essence", border_style="magenta")
    mood_panel = Panel(Text(mood, style="bold cyan"), title="Current Mood", border_style="cyan")
    talents_panel = Panel(Text(hidden_talents, style="dim green"), title="Hidden Talents", border_style="green")

    # Display Profile
    console.print(Rule(style="grey35"))
    console.print(Align.center(profile_header))
    console.print(Rule(style="grey35"))

    console.print(Align.center(bio_panel))
    console.print(Rule(style="grey35"))

    # Display Essence, Mood, Hidden Talents
    console.print(Columns([essence_panel, mood_panel, talents_panel], align="center", padding=(1, 4)))
    console.print("")
    console.print(Rule(style="grey35"))
    action= input(Style.DIM+"\nWhats on your mind (b to return):   ")
    if action == 'b':
        return user_dashboard(user_id)
    else:
        print(Fore.RED+"\n Invalid input")
        time.sleep(2)
        return user_profile(user_id)
