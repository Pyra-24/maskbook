from database import db_connection
from psycopg2 import sql
from rich.console import Console
from rich.panel import Panel
import time
from datetime import datetime, timedelta, datetime

# Initialize Rich Console
console = Console()

def get_friend_details(friend_username):
    """
    Fetch friend details by username from the database.
    """
    conn = db_connection()
    cursor = None
    
    try:
        cursor = conn.cursor()
        # Query to check if the friend's username exists
        query = sql.SQL("SELECT * FROM users WHERE username = %s")
        cursor.execute(query, (friend_username,))
        friend_data = cursor.fetchone()
        
        if friend_data:
            # Map the data to meaningful variables
            friend_data = {
                "id": friend_data[0],
                "username": friend_data[1],
                "email": friend_data[2],
                "password": friend_data[3],
                "first_name": friend_data[4],
                "last_name": friend_data[5],
                "profile_picture": friend_data[6],
                "created_at": friend_data[7],
                "updated_at": friend_data[8],
                "bio": friend_data[9],
                "essence": friend_data[10],
                "mood": friend_data[11],
                "hidden_talents": friend_data[12],
                "followers_count": friend_data[13],
                "following_count": friend_data[14],
                "posts_count": friend_data[15]
            }
            return friend_data
        else:
            return None
    
    except Exception as e:
        console.print(f"[red]Database error: {e}[/red]")
        return None
    
    finally:
        if cursor:
            cursor.close()
        conn.close()
