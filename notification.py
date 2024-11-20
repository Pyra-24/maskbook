from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from database import db_connection
from datetime import datetime
import time
from colorama import Fore, Style, init
import os
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def notify_user(receiver_id, message):
    """
    Notify a user by inserting a message into their notifications.
    """
    conn = db_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO notifications (user_id, actor_id, notification_type, created_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (receiver_id, None, message, datetime.now()))
        conn.commit()
    except Exception as e:
        console.print(f"[bold red]An error occurred while sending a notification: {e}[/bold red]")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def handle_follow_request(user_id, actor_id, actor_name):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    """
    Handle a follow request: accept or decline.
    """
    # First, check if the users are already friends
    conn = db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        # Query to check if they are already friends
        cursor.execute("""
            SELECT status FROM friends
            WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
        """, (user_id, actor_id, actor_id, user_id))
        result = cursor.fetchone()

        if result and result[0] == 'accepted':
            console.print(f"[bold yellow]You both are already friends![/bold yellow]")
            time.sleep(2)
            return display_notifications(user_id)

        # If they are not friends, proceed with the request
        console.print(f"[bold]Do you want to accept the follow request from {actor_name}? (y/n):[/bold]")
        decision = input("> ").strip().lower()
        if decision == "y":
            conn = None
            cursor = None
            try:
                conn = db_connection()
                cursor = conn.cursor()

                # Update the status in the friends table
                update_status_query = """
                UPDATE friends
                SET status = 'accepted', updated_at = %s
                WHERE user_id = %s AND friend_id = %s AND status = 'pending'
                """
                cursor.execute(update_status_query, (datetime.now(), actor_id, user_id))

                # Increment follower and following counts
                increment_followers_query = """
                UPDATE users
                SET followers_count = followers_count + 1
                WHERE id = %s
                """
                increment_following_query = """
                UPDATE users
                SET following_count = following_count + 1
                WHERE id = %s
                """
                cursor.execute(increment_followers_query, (actor_id,))
                cursor.execute(increment_following_query, (user_id,))

                # Notify the actor
                notify_user_query = """
                INSERT INTO notifications (user_id, actor_id, notification_type, created_at)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(notify_user_query, (
                    actor_id,
                    user_id,
                    f"Your follow request has been accepted by {user_data['username']}.",
                    datetime.now(),
                ))

                conn.commit()

                console.print(f"[bold green]You have accepted the follow request from {actor_name}.[/bold green]")
                time.sleep(2)
                return display_notifications(user_id)

            except Exception as e:
                console.print(f"[bold red]An error occurred: {e}[/bold red]")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            console.print(f"[bold yellow]You declined the follow request from {actor_name}.[/bold yellow]")
            time.sleep(2)
            return display_notifications(user_id)

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def display_notifications(user_id):
    from feeds import feeds
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()

    conn = db_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        # Fetch notifications for the user
        cursor.execute("""
            SELECT notifications.id, notifications.actor_id, notifications.notification_type,
                   users.first_name, users.last_name
            FROM notifications
            JOIN users ON notifications.actor_id = users.id
            WHERE notifications.user_id = %s
            ORDER BY notifications.created_at DESC
        """, (user_id,))
        notifications = cursor.fetchall()

        if notifications:
            # Display each notification with a number
            console.print("\n[bold cyan]Your Notifications:[/bold cyan]\n")
            for idx, notification in enumerate(notifications, 1):
                actor_id = notification[1]
                notification_type = notification[2]
                actor_name = f"{notification[3]} {notification[4]}"

                if notification_type == "follow request":
                    message = f"{idx}. Follow request from {actor_name}."
                elif notification_type == "message":
                    message = f"{idx}. New message from {actor_name}."
                else:
                    message = f"{idx}. {notification_type.capitalize()} from {actor_name}."

                console.print(Panel(message, border_style="green"))

            # Prompt the user to select a notification
            console.print("\n[bold]Select a notification number to respond, or press Enter to exit:[/bold]")
            choice = input("> ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(notifications):
                    selected_notification = notifications[choice - 1]
                    actor_id = selected_notification[1]
                    notification_type = selected_notification[2]
                    actor_name = f"{selected_notification[3]} {selected_notification[4]}"

                    if notification_type == "follow request":
                        handle_follow_request(user_id, actor_id, actor_name)
                    elif notification_type == "message":
                        console.print(f"[bold]Opening chat with {actor_name}...[/bold]")
                        # Assuming `display_chat` exists to handle chat
                        display_chat(user_id, actor_id)
                    else:
                        console.print(f"[bold yellow]This notification cannot be interacted with.[/bold yellow]")
                else:
                    console.print(f"[bold red]Invalid choice.[/bold red]")
            else:
                console.print(f"[bold yellow]Exited notifications.[/bold yellow]")
                return feeds(user_id)

        else:
            # No notifications
            console.print(Panel("[bold red]No notifications available.[/bold red]", border_style="red", padding=(1, 2)))
            gg = input("\nWhat's on your mind:  ")
            if gg == 'b':
                return feeds(user_id)
            else:
                print(Fore.RED + "\nInvalid input")
                time.sleep(2)
                return display_notifications(user_id)

    except Exception as e:
        console.print(f"[bold red]An error occurred while fetching notifications: {e}[/bold red]")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def display_notifications(user_id):
    from feeds import feeds
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    clear_screen()
    """
    Fetch and display notifications for the given user.
    """
    conn = db_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        # Fetch notifications for the user
        cursor.execute("""
            SELECT notifications.id, notifications.actor_id, notifications.notification_type,
                   users.first_name, users.last_name
            FROM notifications
            JOIN users ON notifications.actor_id = users.id
            WHERE notifications.user_id = %s
            ORDER BY notifications.created_at DESC
        """, (user_id,))
        notifications = cursor.fetchall()

        if notifications:
            # Display each notification with a number
            console.print("\n[bold cyan]Your Notifications:[/bold cyan]\n")
            for idx, notification in enumerate(notifications, 1):
                actor_id = notification[1]
                notification_type = notification[2]
                actor_name = f"{notification[3]} {notification[4]}"

                if notification_type == "follow request":
                    message = f"{idx}. Follow request from {actor_name}."
                elif notification_type == "message":
                    message = f"{idx}. New message from {actor_name}."
                else:
                    message = f"{idx}. {notification_type.capitalize()} from {actor_name}."

                console.print(Panel(message, border_style="green"))

            # Prompt the user to select a notification
            console.print("\n[bold]Select a notification number to respond, or press Enter to exit:[/bold]")
            choice = input("> ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(notifications):
                    selected_notification = notifications[choice - 1]
                    actor_id = selected_notification[1]
                    notification_type = selected_notification[2]
                    actor_name = f"{selected_notification[3]} {selected_notification[4]}"

                    if notification_type == "follow request":
                        handle_follow_request(user_id, actor_id, actor_name)
                    elif notification_type == "message":
                        console.print(f"[bold]Opening chat with {actor_name}...[/bold]")
                        # Assuming `display_chat` exists to handle chat
                        display_chat(user_id, actor_id)
                    else:
                        console.print(f"[bold yellow]This notification cannot be interacted with.[/bold yellow]")
                else:
                    console.print(f"[bold red]Invalid choice.[/bold red]")
            else:
                console.print(f"[bold yellow]Exited notifications.[/bold yellow]")
                return feeds(user_id)

        else:
            # No notifications
            console.print(Panel("[bold red]No notifications available.[/bold red]", border_style="red", padding=(1, 2)))
            gg=input("\nWhats on your mind:  ")
            if gg == 'b':
                return feeds(user_id)
            else:
                print(Fore.RED+"\nInvalid input")
                time.sleep(2)
                return display_notifications(user_id)

    except Exception as e:
        console.print(f"[bold red]An error occurred while fetching notifications: {e}[/bold red]")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()