import psycopg2
from decouple import config
from urllib.parse import urlparse
import re
import sys
import shutil
import threading
import time
import os
import time
from datetime import datetime, timedelta, datetime
from colorama import Fore, Style, Back, init
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered        

def db_connection():
    """Establishes a connection to the database with SSL and keepalives."""
    # Parse DATABASE_URL
    url = urlparse(config("DATABASE_URL"))
    
    # Extract connection details from the DATABASE_URL
    host = url.hostname
    port = url.port
    user = url.username
    password = url.password
    database = url.path[1:]

    try:
        # Connect using individual parameters
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=database,
            sslmode="require",               # Use SSL
            keepalives=1,                    # Enable keepalives
            keepalives_idle=300,             # Set idle time before keepalives (in seconds)
            keepalives_interval=60,          # Interval for keepalives (in seconds)
            keepalives_count=5               # Number of keepalive retries before disconnecting
        )
        
        return conn
    except psycopg2.OperationalError as db_error:
        error_message = str(db_error)  # Fixed variable name
        if "SSL connection has been closed unexpectedly" in error_message:
            print("\n❌ Poor Connection")
            return poor_connection_page()
        else:
            return poor_connection_page()
    except Exception as e:
        print(f"Poor connection ")
        return poor_connection_page()  # Added parentheses to call the function
        
def poor_connection_page():
    from main import main
    width = shutil.get_terminal_size().columns  # Get the width of the terminal

    frames = [
        f"{Fore.RED}🪫 Poor Connection 🪫{Style.RESET_ALL}",
        f"{Fore.YELLOW}🪫 Poor Connection 🪫{Style.RESET_ALL}",
        f"{Fore.LIGHTRED_EX}🪫 Poor Connection 🪫{Style.RESET_ALL}",
    ]

    # Animation loop
    for _ in range(10):  # Repeat for 10 cycles
        for frame in frames:
            clear_screen()
            print("\n\n\n")  # Create space at the top for centering vertically
            print(center_text(frame))
            print(Style.DIM + "-" * width)
            print(Fore.RED + "\n" + center_text("We're having trouble connecting. Please check your network and try again."))
            print("\n")
            print("                     _______ ")
            print("                   /       /| ")
            print("                  /_______/ | ")
            print("                 |       |  | ")
            print("                 |       |  | ")
            print("                 |_______| / ")
            print("                 |_______|/ ")
            print("\n")
            print(Fore.YELLOW + center_text("Attempting to reconnect..."))
            print(Style.DIM + "-" * width)
            time.sleep(0.3)  # Shorten sleep time for smoother animation
    
    # After animation completes, try returning to the main function
    return main()    
    
    