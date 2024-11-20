import os
import time
import sys
from datetime import datetime, timedelta, datetime
from database import db_connection
from colorama import Fore, Style, Back, init
init(autoreset=True)

def update_user_profile(user_id, username=None, email=None, password=None, first_name=None, last_name=None, 
                        profile_picture=None, bio=None, essence=None, mood=None, hidden_talents=None):
    """
    Updates the profile of the user based on the provided user_id.
    Only updates fields that are provided with a value.
    """
    conn = db_connection()
    cursor = None
    if conn:
        try:
            cursor = conn.cursor()

            # Collect fields to update
            update_fields = {}
            if username:
                update_fields["username"] = username
            if email:
                update_fields["email"] = email
            if password:
                # Hash the password before storing it
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_fields["password"] = password_hash
            if first_name:
                update_fields["first_name"] = first_name
            if last_name:
                update_fields["last_name"] = last_name
            if profile_picture:
                update_fields["profile_picture"] = profile_picture
            if bio:
                update_fields["bio"] = bio
            if essence:
                update_fields["essence"] = essence
            if mood:
                update_fields["mood"] = mood
            if hidden_talents:
                update_fields["hidden_talents"] = hidden_talents

            # Ensure there are fields to update
            if not update_fields:
                print("No fields to update.")
                return

            # Dynamically build the SQL query
            set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
            values = list(update_fields.values()) + [user_id]

            query = f"UPDATE users SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()

            print(Fore.GREEN+"\nProfile updated successfully.")
            time.sleep(2)
            input("\npress enter to return:   ")
        except Exception as e:
            print(f"Error updating profile: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()