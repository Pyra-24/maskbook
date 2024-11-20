from database import db_connection
from psycopg2 import sql
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
from datetime import datetime
from colorama import Fore, Style, init
import os
import time
from search import get_friend_details

init(autoreset=True)

# Initialize a Console object for Rich output
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Database Functions
def get_follow_status(user_id, friend_id):
    """Get the follow status between the current user and a friend."""
    conn = db_connection()
    cursor = conn.cursor()
    try:
        query = sql.SQL(
            """
            SELECT status FROM friends 
            WHERE 
                (user_id = %s AND friend_id = %s) 
                OR 
                (user_id = %s AND friend_id = %s)
            """
        )
        cursor.execute(query, (user_id, friend_id, friend_id, user_id))
        result = cursor.fetchone()
        if result:
            return result[0]  # 'pending', 'accepted', etc.
        return "not following"
    except Exception as e:
        print(f"Error checking follow status: {e}")
        return "not following"
    finally:
        cursor.close()
        conn.close()

def create_follow_request(user_id, friend_id):
    """Create a follow request and update following/follower counts."""
    conn = db_connection()
    cursor = conn.cursor()
    try:
        # Insert the follow request
        query = sql.SQL("INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, 'pending')")
        cursor.execute(query, (user_id, friend_id))
        
        # Increment following_count for the user
        cursor.execute("UPDATE users SET following_count = following_count + 1 WHERE id = %s", (user_id,))
        
        # Increment followers_count for the friend
        cursor.execute("UPDATE users SET followers_count = followers_count + 1 WHERE id = %s", (friend_id,))
        
        conn.commit()
    except Exception as e:
        print(f"Error creating follow request: {e}")
    finally:
        cursor.close()
        conn.close()

def unfollow_user(user_id, friend_id):
    """Unfollow a user and update following/follower counts."""
    conn = db_connection()
    cursor = conn.cursor()
    try:
        # Delete the follow record
        query = sql.SQL("DELETE FROM friends WHERE user_id = %s AND friend_id = %s")
        cursor.execute(query, (user_id, friend_id))
        
        # Decrement following_count for the user
        cursor.execute("UPDATE users SET following_count = following_count - 1 WHERE id = %s", (user_id,))
        
        # Decrement followers_count for the friend
        cursor.execute("UPDATE users SET followers_count = followers_count - 1 WHERE id = %s", (friend_id,))
        
        conn.commit()
    except Exception as e:
        print(f"Error unfollowing user: {e}")
    finally:
        cursor.close()
        conn.close()

def send_follow_notification(user_id, friend_id):
    """
    Insert a notification for a follow request.
    """
    conn = db_connection()
    cursor = conn.cursor()
    try:
        query = sql.SQL(
            "INSERT INTO notifications (user_id, actor_id, notification_type, status) VALUES (%s, %s, 'follow request', 'pending')"
        )
        cursor.execute(query, (friend_id, user_id))  # `friend_id` is the receiver, `user_id` is the actor
        conn.commit()
    except Exception as e:
        print(f"Error sending follow notification: {e}")
    finally:
        cursor.close()
        conn.close()

# Application Logic
def find_friend(user_id):
    from dashboard import user_dashboard
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    """Search and display a friend's profile."""
    clear_screen()
    my_username = user_data.get("username")
    friend = input("What is your friend's username: ").strip()
    
    if friend == my_username:
        print(Fore.RED + "This is your username. Please enter a different username.")
        time.sleep(2)
        return find_friend(user_id)
    elif friend == 'b':
        return user_dashboard(user_id)

    if not friend:
        print(Fore.RED + "\nUsername cannot be empty. Please try again.")
        return find_friend(user_id)

    friend_data = get_friend_details(friend)
    if friend_data:
        friend_profile(user_id, friend_data)
    else:
        print(Fore.RED + f"\nFriend with username '{friend}' not found. Please try again.")
        time.sleep(2)
        return find_friend(user_id)

def friend_profile(user_id, friend_data):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    """Display friend's profile with follow/unfollow functionality."""
    clear_screen()
    friend_profile_emoji = friend_data.get("profile_picture")
    friend_fname = friend_data.get("first_name")
    friend_lname = friend_data.get("last_name")
    friend_username = friend_data.get("username")
    followers = friend_data.get("followers_count")
    following = friend_data.get("following_count")
    posts = friend_data.get("posts_count")
    hidden_talent = friend_data.get("hidden_talents")
    bio = friend_data.get("bio")
    mood = friend_data.get("mood")
    essence = friend_data.get("essence")
    
    # Check follow status
    # Get follow status
    follow_status = get_follow_status(user_id, friend_data["id"])
    follow_button_text = "Follow" if follow_status == "not following" or follow_status == "pending" else "Unfollow"

    # Profile Header
    friend_header = Table.grid(expand=True)
    friend_header.add_column(justify="center")
    friend_header.add_row("\n")
    friend_header.add_row(f"[bold]{friend_profile_emoji}  {friend_fname} {friend_lname}[/bold]")
    friend_header.add_row("\n")
    friend_header.add_row(f"[bold]Username:[/bold] [dim]{friend_username}[/dim]")
    friend_header.add_row(f"[bold]Followers:[/bold] [dim]{followers}[/dim] | [bold]Following:[/bold] [dim]{following}[/dim] | [bold]Posts:[/bold] [dim]{posts}[/dim]")
    friend_header.add_row("\n")

    # Buttons
    buttons_row = Columns(
        [
            Panel(f"[bold]{follow_button_text}[/bold]", border_style="bold green", padding=(0, 3), expand=False),
            Panel("[bold]Message[/bold]", border_style="bold blue", padding=(0, 3), expand=False),
        ],
        align="center",
        equal=True,
    )
    friend_header.add_row(Align.center(buttons_row))

    # Panels for Bio, Activities, Mood, and Essence
    bio_panel = Panel(Text(bio, style="#5F5F5F italic"), title="Bio Snippet", border_style="#DE165A")
    activity_panel = Panel(Text(hidden_talent, style="#5F5F5F"), title="Hidden Talents", border_style="yellow")
    mood_panel = Panel(Text(mood, style="#5F5F5F italic"), title="Mood", border_style="purple")
    essence_panel = Panel(Text(essence, style="#5F5F5F"), title="Essence", border_style="#00D0BD")

    # Display Profile
    console.print("\n")
    console.print(Align.center(friend_header))
    console.print("\n")
    console.print(Rule(style="grey35"))
    console.print("\n", Columns([bio_panel, activity_panel, mood_panel, essence_panel], align="center", padding=(1, 4)))
    console.print(Rule(style="grey35"))

    # Handle Follow/Unfollow action
    action = input("\nEnter 'f' to follow/unfollow, or 'b' to go back: ").strip().lower()
    if action == 'f':
        if follow_status == "not following":
            create_follow_request(user_id, friend_data["id"])
            send_follow_notification(user_id, friend_data["id"])
            print(Fore.GREEN + f"You have sent a follow request to {friend_fname}.")
        else:  # Unfollow case
            unfollow_user(user_id, friend_data["id"])
            print(Fore.RED + f"You have unfollowed {friend_fname}.")
        time.sleep(2)
        return find_friend(user_id)
    elif action == 'b':
        return find_friend(user_id)
    else:
        print(Fore.RED + "Invalid input. Please try again.")
        time.sleep(2)
        return friend_profile(user_id, friend_data)