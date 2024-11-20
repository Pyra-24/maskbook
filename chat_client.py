import psycopg2
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from datetime import datetime
import time
from colorama import Fore, Style, init
import os
from rich import print as rprint
from database import db_connection  # Assuming db_connection function is imported from utils

# Initialize the console
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to format the timestamp to relative time
def time_ago(timestamp):
    now = datetime.now()
    delta = now - timestamp
    if delta.total_seconds() < 60:
        return f"{int(delta.total_seconds())} second{'s' if delta.total_seconds() > 1 else ''} ago"
    elif delta.total_seconds() < 3600:
        return f"{int(delta.total_seconds() // 60)} minute{'s' if delta.total_seconds() // 60 > 1 else ''} ago"
    elif delta.total_seconds() < 86400:
        return f"{int(delta.total_seconds() // 3600)} hour{'s' if delta.total_seconds() // 3600 > 1 else ''} ago"
    elif delta.total_seconds() < 2592000:
        return f"{int(delta.total_seconds() // 86400)} day{'s' if delta.total_seconds() // 86400 > 1 else ''} ago"
    elif delta.total_seconds() < 31536000:
        return f"{int(delta.total_seconds() // 2592000)} month{'s' if delta.total_seconds() // 2592000 > 1 else ''} ago"
    else:
        return f"{int(delta.total_seconds() // 31536000)} year{'s' if delta.total_seconds() // 31536000 > 1 else ''} ago"

def display_friends(user_id):
    from feeds import feeds
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    try:
        conn = db_connection()
        cursor = conn.cursor()
        # Fetch approved friends
        query = """
        SELECT u.id, u.username
        FROM friends f
        JOIN users u ON 
            (f.user_id = u.id AND f.friend_id = %s) 
            OR (f.friend_id = u.id AND f.user_id = %s)
        WHERE f.status = 'accepted'
        """
        cursor.execute(query, (user_id, user_id))
        friends = cursor.fetchall()

        if not friends:
            console.print("\n[bold red]You have no friends.[/bold red]")
            hk = input("\nWhats on your mind:  ")
            if hk == 'b':
                return feeds(user_id)
            else:
                print(Fore.RED+"Invalid input")
                time.sleep(2)
                return display_friends(user_id)

        
        # Construct the content for the panel
        content = "\n".join([f"{idx}. {username}" for idx, (friend_id, username) in enumerate(friends, start=1)])

# Create and print the panel
        friends_panel = Panel(content, title="My Friends", border_style="blue")
        console.print("\n")
        console.print(friends_panel)


        choice = input(Style.DIM+"\nPick a friend by number (or 'b' to go back):   ").strip()
        if choice.lower() == 'b':
            return feeds(user_id) # Exit to main menu or previous screen
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(friends):
                friend_id, username = friends[choice_idx]
                display_chat(user_id, friend_id)  # Open chat with selected friend
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
                time.sleep(2)
                return display_friends(user_id)
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")
            time.sleep(2)
            return display_friends(user_id)
    except Exception as e:
        print(f"Error displaying friends: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def display_recent_chats(user_id):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    try:
        conn = db_connection()
        cursor = conn.cursor()
        # Fetch friends sorted by most recent conversation
        query = """
        SELECT DISTINCT ON (m.sender_id, m.receiver_id)
               u.id, u.username, MAX(m.timestamp) AS last_message_time
        FROM messages m
        JOIN users u ON (u.id = m.sender_id AND m.receiver_id = %s)
                     OR (u.id = m.receiver_id AND m.sender_id = %s)
        GROUP BY u.id, u.username
        ORDER BY last_message_time DESC
        """
        cursor.execute(query, (user_id, user_id))
        recent_chats = cursor.fetchall()

        if not recent_chats:
            console.print("[bold red]No recent chats found.[/bold red]")
            return

        console.print("[bold green]Recent Chats:[/bold green]")
        for idx, (friend_id, username, last_message_time) in enumerate(recent_chats, start=1):
            time_display = time_ago(last_message_time)
            console.print(f"{idx}. [bold cyan]{username}[/bold cyan] - Last message: {time_display}")

        choice = input("Pick a chat by number (or 'b' to go back): ").strip()
        if choice.lower() == 'b':
            return  # Exit to main menu or previous screen
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(recent_chats):
                friend_id, username, _ = recent_chats[choice_idx]
                display_chat(user_id, friend_id)  # Open chat with selected friend
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]")
    except Exception as e:
        print(f"Error displaying recent chats: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Function to retrieve chat messages
def get_chat_messages(user_id, receiver_id):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        SELECT sender_id, receiver_id, message, timestamp, seen
        FROM messages
        WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
        """
        cursor.execute(query, (user_id, receiver_id, receiver_id, user_id))
        messages = cursor.fetchall()

        # Check if no messages were found
        if not messages:
            return [{"message": "No messages yet. Start the conversation!"}]
        
        # Format messages with the relative time and seen status
        formatted_messages = []
        for msg in messages:
            sender, receiver, message, timestamp, seen = msg
            time_display = time_ago(timestamp)
            seen_status = "☑︎" if seen else "☐"
            formatted_messages.append({
                "sender": sender,
                "message": message,
                "time": time_display,
                "seen": seen_status,
            })

        return formatted_messages
    except Exception as e:
        print(f"Error fetching chat messages: {e}")
        return [{"message": "Error retrieving messages."}]
    finally:
        if conn:
            cursor.close()
            conn.close()
            
# Function to save a message
def save_message(user_id, receiver_id, message):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    try:
        conn = db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now()
        query = """
        INSERT INTO messages (sender_id, receiver_id, message, timestamp, seen)
        VALUES (%s, %s, %s, %s, FALSE)
        """
        cursor.execute(query, (user_id, receiver_id, message, timestamp))
        conn.commit()
    except Exception as e:
        print(f"Error saving message: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
           
def mark_as_seen(sender_id, receiver_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE messages
        SET seen = TRUE
        WHERE sender_id = %s AND receiver_id = %s AND seen = FALSE
        """
        cursor.execute(query, (sender_id, receiver_id))
        conn.commit()
    except Exception as e:
        print(f"Error marking messages as seen: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()           
            
# Function to display the chat
def display_chat(user_id, receiver_id):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    chat_messages = get_chat_messages(user_id, receiver_id)
    receiver_username = user_data.get("username", f"User {receiver_id}")
    console.print(Align(Panel(f"👤 Chat with {receiver_username}", style="bold blue"), align="center"))
    console.print("\n")
    console.print(Rule(style="grey35"))
    # If there are no messages, display the placeholder message
    if len(chat_messages) == 1 and "message" in chat_messages[0]:
        console.print(Panel(chat_messages[0]["message"], style="dim"))
    else:
        # Display all the fetched messages
        for msg in chat_messages:
            alignment = "left" if msg["sender"] == receiver_id else "right"
            color = "yellow" if msg["sender"] == receiver_id else "cyan"
            seen_status = msg.get("seen", "☐")
            msg_panel = Panel(
                Text(f"{msg['message']} - {msg['time']} {seen_status}", style=color),
                border_style=color,)
            console.print("\n")
            console.print(Align(msg_panel, align=alignment))
    console.print("\n")
    console.print(Rule(style="grey35"))
    console.print("\n[bold cyan]Type your message below or (b to exit):[/bold cyan]")
    while True:
        message = input("Your message: ")

        if message.lower() == 'b':
        # Display friends when user inputs 'b'
            return display_friends(user_id)

        elif message.lower() == 'ref':
        # Refresh chat when user inputs 'ref'
            return display_chat(user_id, receiver_id)

        elif message.strip():  # Check if message is not empty (ignoring spaces)
        # Save the message and mark as seen
            save_message(user_id, receiver_id, message)
            mark_as_seen(receiver_id, user_id)
            return display_chat(user_id, receiver_id)

        else:
            # If the message is empty
            print(Fore.RED + "Message cannot be empty. Please type something.")
            time.sleep(2)