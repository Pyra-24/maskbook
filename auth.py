import os
import sys
import time
from datetime import datetime, timedelta, date
import random
from database import db_connection
import bcrypt
from feeds import feeds
from colorama import Fore, Style, Back, init
init(autoreset=True)

def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered 
    
def register_user(first_name, last_name, email, password, username):
    from login import login_users
    """Registers a new user."""
    
    # Random choices for additional user profile fields
    profile_picture = random.choice(['😊', '😎', '🤠', '🦁', '🐯', '🐶', '🦊', '🦝', '👑', '🌹', '🤩', '🤡', '😈', '🌟', '🤑', '🥸'])
    bios = [
        "Exploring the unseen paths. Sharing my masked journey.",
        "Living life one code at a time.",
        "Dreaming beyond the stars. Masked for mystery.",
        "An adventurer in a world of shadows.",
        "Observing the world with a hidden smile.",
        "Lost in thought, found in creativity."
    ]
    essences = [
        "Night Owl | Observer | Dreamer",
        "Thinker | Creator | Visionary",
        "Masked Hero | Hidden Talent | Seeker of Light",
        "Wanderer | Explorer | Friend",
        "Caffeine Enthusiast | Bookworm | Stargazer"
    ]
    moods = [
        "Currently inspired by the stars ✨",
        "Feeling mysterious and creative 🎭",
        "Full of energy and curiosity 🌟",
        "In a reflective and peaceful mood 🌙",
        "Vibing with the rhythm of life 🎶"
    ]
    hidden_talents = [
        "Whispering secrets to the wind, weaving shadows, decoding dreams.",
        "Telling stories in silence, capturing moments unseen.",
        "Dancing with words, painting with emotions.",
        "Building bridges where none exist.",
        "Creating magic out of the mundane."
    ]

    # Select random bio, essence, mood, and hidden talent
    bio = random.choice(bios)
    essence = random.choice(essences)
    mood = random.choice(moods)
    talent = random.choice(hidden_talents)

    conn = db_connection()
    cursor = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                print(Fore.RED + "\n  Email already registered!")
                time.sleep(2.9)
                return login_users()
            
            # Hash password and decode
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user data into the database
            cursor.execute(
                """
                INSERT INTO users (username, email, password, first_name, last_name, profile_picture, bio, essence, mood, hidden_talents)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (username, email, password_hash, first_name, last_name, profile_picture, bio, essence, mood, talent),
            )
            conn.commit()
            print("\n" + Fore.GREEN + center_text("🥳 Registration successful!"))
            time.sleep(2)
            return login_users()
        except Exception as e:
            print(f"Error during registration: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

def login_user(email, password):
    from login import login_users
    """Logs in an existing user and fetches the latest user data dynamically."""

    conn = db_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Fetch the user data by email
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                print(Fore.RED + "\n  Email not registered!")
                time.sleep(2.9)
                return login_users()

            # Check if the password is correct
            if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                print(Fore.GREEN + "\n" + center_text("Login successful!"))

                # Fetch the latest user data dynamically
                user_id = user[0]
                user_data = fetch_user_data(user_id)  # Ensure fetching the latest data here

                if user_data:  # Ensure the data exists
                    # Mark the user as online
                    set_user_online_status(user_data, user_id, status="online")

                    # Pass the latest data to the feeds function
                    feeds(user_id)
                else:
                    print(Fore.RED + "Failed to fetch latest user data.")
                    return login_users()

            else:
                print(Fore.RED + "\nInvalid credentials 🙊")
                time.sleep(2)
                return login_users()

        except Exception as e:
            print(f"Error during login: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            conn.close()


def fetch_user_data(user_id):
    """
    Fetch the latest user data from the database.
    Returns a dictionary with the user's current details.
    """
    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Query to get the latest data
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "password": user[3],
                "first_name": user[4],
                "last_name": user[5],
                "profile_picture": user[6],
                "created_at": user[7],
                "updated_at": user[8],
                "bio": user[9],
                "essence": user[10],
                "mood": user[11],
                "hidden_talents": user[12],
                "followers_count": user[13],
                "following_count": user[14],
                "posts_count": user[15],
                "online_status": user[16]
            }
        else:
            print("User data not found.")
            return None

    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()
            
def set_user_online_status(user_data, user_id, status=None):
    from database import poor_connection_page
    """Set the user's online status to either 'online' or 'offline'."""
    username = user_data.get("username")
    try:
        # Connect to the database
        conn = db_connection()
        if conn is None:
            poor_connection_page()

        cursor = conn.cursor()

        # Execute the query to update the user's status
        query = "UPDATE users SET online_status = %s WHERE id = %s"
        cursor.execute(query, (status, user_id))

        # Commit the changes to the database
        conn.commit()
        
    except Exception as e:
        print(f"Error updating online status for user {username}: {e}")
        time.sleep(2)
        return
    finally:
        if conn:
            cursor.close()
            conn.close()                