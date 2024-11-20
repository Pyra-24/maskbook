from database import db_connection
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich.layout import Layout
from rich.table import Table
from colorama import Fore, Style
from dashboard import user_dashboard
import time
from notification import display_notifications
from datetime import datetime, timedelta, date
import os
import sys
import psycopg2.extras  # Required for DictCursor
def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered 
    
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
width = os.get_terminal_size().columns

def toggle_like(post_id, user_id, cursor, conn):
    # Check if the user has already liked the post
    cursor.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    like_exists = cursor.fetchone()
    
    if like_exists:
        # User has already liked the post, so we will unlike it
        cursor.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
        cursor.execute("UPDATE posts SET like_count = like_count - 1 WHERE id = %s", (post_id,))
    else:
        # User has not liked the post yet, so we will like it
        cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (post_id, user_id))
        cursor.execute("UPDATE posts SET like_count = like_count + 1 WHERE id = %s", (post_id,))
    
    conn.commit()
    
def format_count(number):
    """Formats numbers into readable counts, e.g., 1000 -> 1k."""
    if number >= 1_000_000:
        return f"{number // 1_000_000}M"
    elif number >= 1_000:
        return f"{number // 1_000}k"
    return str(number)

def feeds(user_id):
    from chat_client import display_recent_chats, display_friends
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    conn = db_connection()
    clear_screen()  # Clear the console screen at the start
    # Header and menu
    head = "Maskbook"
    header = Text(head, style="bold blue")
    content = Text("👥          💬          🔔", style="bold")
    menu_bar = Panel(content, border_style="dim", width=30)
    console.print(header, justify="center")
    console.print("\n")
    console.print(menu_bar, justify="center")
    console.print("—" * width, style="bold")
    console.print("\n")
    
    # Establish database connection
    if conn is None:
        print("\n❌ Could not connect to the database.")
        return poor_connection_page()
        
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Fetch posts and user details in random order
        cursor.execute("""
            SELECT 
                posts.id, 
                posts.user_id, 
                posts.content, 
                posts.like_count, 
                posts.comment_count,
                posts.tag,
                users.first_name,
                users.last_name,
                users.username, 
                users.profile_picture
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY RANDOM()
        """)
        results = cursor.fetchall()

        if results:
            displayed = set()  # Track displayed posts to ensure no repeats
            while len(displayed) < len(results):
                n = len(displayed)
                post = results[n]

                # Display the post details
                format_like = format_count(post['like_count'])
                format_comment = format_count(post['comment_count'])
                like_comment_text = Text.assemble(
                    ("♥️  " + str(format_like), "bold red"),
                    (" " * (width - 30)),
                    (str(format_comment) + " 💬", "bold green")
                )
                jack = Panel(like_comment_text, expand=False)
                
                post_content = Panel(
                    Text(post['content'], style="italic"),
                    title=f"{post['profile_picture']} {post['first_name']} {post['last_name']}  @{post['username']}",
                    subtitle=Text(post['tag'], style="italic magenta"),
                    expand=True,
                    padding=(1, 2),
                    border_style="blue"
                )

                post_bar = Panel(
                    post_content,
                    title="📸 Feeds",
                    expand=True,
                    padding=(1, 2)
                )
                
                console.print("\n")
                console.print(post_bar)
                console.print(jack, justify="center")
                console.print("\n")
                console.print("—" * width)
                
                # Add post to displayed
                displayed.add(n)

                action = input(Style.DIM + "\nWhat's on your mind?:  " + Style.RESET_ALL).strip().lower()
                
                if action == 'n':
                    if len(displayed) < len(results):
                        clear_screen()
                        console.print(header, justify="center")
                        console.print("\n")
                        console.print(menu_bar, justify="center")
                        console.print("—" * width, style="bold")
                        console.print("\n")
                    else:
                        print(Fore.RED + "\nNo more posts to display.")
                        time.sleep(1)
                        return feeds(user_id)
                elif action == 'l':
                    toggle_like(post['id'], user_id, cursor, conn)

                    # Re-fetch the post to update likes_count
                    cursor.execute("""
                        SELECT like_count 
                        FROM posts 
                        WHERE id = %s
                    """, (post['id'],))
                    updated_post = cursor.fetchone()
                    post['like_count'] = updated_post['like_count']
                    return feeds(user_id)  # Refresh feed to update like count
                elif action == 'c':
                    comment_content = input("\nEnter your comment: ").strip()
                    if comment_content:
                        try:
                            cursor.execute("""
                                INSERT INTO comments (post_id, user_id, content)
                                VALUES (%s, %s, %s)
                            """, (post['id'], user_id, comment_content))
                            conn.commit()
                            cursor.execute("""
                                UPDATE posts 
                                SET comment_count = comment_count + 1 
                                WHERE id = %s
                            """, (post['id'],))
                            conn.commit()
                            post['comment_count'] += 1
                            print(Fore.GREEN + "\n ✅ Comment added successfully")
                            time.sleep(2)
                            return feeds(user_id)
                        except Exception as e:
                            print(Fore.RED + f"An error occurred: {e}")
                            time.sleep(4)
                elif action == 'vc':
                    # View comments
                    clear_screen()  # Clear screen before displaying comments
                    console.print("⬅️ b")
                    console.print("\n")
                    console.print(header, justify="center")
                    console.print("\nViewing comments for the selected post", style="bold")
                    console.print("\n")

                    # Fetch comments for the post
                    cursor.execute("""
                        SELECT comments.content, users.username, users.profile_picture 
                        FROM comments
                        JOIN users ON comments.user_id = users.id
                        WHERE comments.post_id = %s
                        ORDER BY comments.id
                    """, (post['id'],))
                    comments = cursor.fetchall()
                    
                    if comments:
                        for comment in comments:
                            comment_panel = Panel(
                                Text(comment['content'], style="italic"),
                                title=f"{comment['profile_picture']} {comment['username']}",
                                expand=False,
                                padding=(0, 2),
                                border_style="green"
                            )
                            console.print(comment_panel)
                    else:
                        console.print("\nNo comments available for this post.", style="bold red")
                    
                    loop=input(Style.DIM+"\ninput b to return.   ")
                    if loop == 'b':
                        return feeds(user_id)
                elif action == 'm':
                    return user_dashboard(user_id)
                elif action.lower() == 'msg':
                    return display_friends(user_id)    
                elif action == 'ns':
                    display_notifications(user_id)
                elif action == 'mf':
                    return display_friends(user_id)    
                elif action == 'cp':
                    post_update(user_id, cursor, conn)
                else:
                    print(Fore.RED + "Invalid input...")
                    time.sleep(1)
                    return feeds(user_id)
        else:
            posts(user_id)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        time.sleep(4)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
def posts(user_id):
    from chat_client import display_recent_chats, display_friends
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    conn = db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # No posts found; prompt user to create a new post
            no_content = Text("No posts available.", style="bold red", justify="center")
            no_post_bar = Panel(
                no_content,
                title="📸 Feeds",
                expand=True,
                padding=(1, 2)
            )
            console.print("\n")
            console.print(no_post_bar)

            # Prompt user to create a new post or view existing ones
            console.print("\n")
            action = input(Style.DIM + "\nWhat's on your mind: " + Style.RESET_ALL).strip().lower()

            if action == 'cp':
                post_update(user_id, cursor, conn)
            elif action == 'm':
                # Navigate to main_dashboard
                return user_dashboard(user_id)
            elif action == 'msg':
                    return display_friends(user_id)     
            elif action == 'mf':
                return display_friends(user_id)
            elif action == 'ns':
                    display_notifications(user_id)    
            elif action in ['n', 'p']:
                print(Fore.RED + "\nNo post available")
                time.sleep(2)
                return feeds(user_id)
            else:
                print(Fore.RED + "Invalid input.")
                time.sleep(1)
                return feeds(user_id)

        finally:
            if cursor:
                cursor.close()
            conn.close()

def post_update(user_id, cursor, conn):
    from auth import fetch_user_data
    user_data = fetch_user_data(user_id)
    # Gather post content from user
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    clear_screen()
    
    print("\n" + Style.DIM + "⬅️ b" + Style.RESET_ALL + Style.DIM + " create a post".rjust(-5))
    print("\n" + Style.DIM + center_text(f"{first_name} {last_name}"))
    print("\n")
    
    while True:
        content = input("What's on your mind? (500 char)  " + Style.DIM)
        if content == 'b':
            return feeds(user_id)

        if not content:
            print(Fore.RED + "\nPost cannot be empty")
            time.sleep(2)
            return post_update(user_id, cursor, conn)
    
        if len(content) > 500:  # Limit post content to 500 characters
            print(Fore.RED + "\nPost content is too long. Please keep it under 500 characters.")
            time.sleep(2)
            return post_update(user_id, cursor, conn)

        tag = input("\nAdd a tag for your post: ")
        if tag == 'b':
            return post_update(user_id, cursor, conn)
    
        if not tag.startswith('#'):
            print(Fore.RED + "\nTag must start with #")
            time.sleep(2)
            return post_update(user_id, cursor, conn)

        if len(tag) > 50:  # Limit tag length to 50 characters
            print(Fore.RED + "\nTag is too long. Please keep it under 50 characters.")
            time.sleep(2)
            return post_update(user_id, cursor, conn)
    
    # Proceed to save post and tag if valid
        save_post(user_id, content, tag)
        print(Fore.GREEN + "\nYour post has been successfully uploaded!")
        return post_update(user_id, cursor, conn)

        # Insert the new post into the Posts table and update posts_count
        try:
            # Insert the post
            cursor.execute("""
                INSERT INTO posts (user_id, content, like_count, comment_count, tag)
                VALUES (%s, %s, 0, 0, %s)
            """, (user_id, content, tag))
            
            # Increment posts_count in the users table
            cursor.execute("""
                UPDATE users
                SET posts_count = posts_count + 1
                WHERE id = %s
            """, (user_id,))
            
            conn.commit()
            print("\n✅ Post created successfully!")
            time.sleep(2)
            return post_update(user_id, cursor, conn)

        except Exception as e:
            print(Fore.RED + f"An error occurred while saving your post: {e}")
            time.sleep(4)
            return post_update(user_id, cursor, conn)