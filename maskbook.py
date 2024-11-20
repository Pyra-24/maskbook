import os
import sys
import time
from datetime import datetime, timedelta, date
from login import login_users
from register import create_acc
from colorama import Fore, Style, Back, init
init(autoreset=True)

width = os.get_terminal_size().columns

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def center_text(text):
    """Center the given text based on the terminal width."""
    width = os.get_terminal_size().columns
    centered = text.center(width)
    return centered   
    
def attention():
    clear_screen()
    print("")
    print(Fore.RED+center_text("🚨 ATTENTION 🚨"))
    print(Style.DIM+center_text("\nHow to use"))
    print("")
    print(Fore.RED+"To call a function with 1 name: "+Style.RESET_ALL+"Use the first and last letters of a function name"+Style.RESET_ALL+Fore.RED+" Example. "+Style.RESET_ALL+"Groups, you call it this way gs Implement it this way to other function with 1 name")
    print("")
    print(Fore.RED+"To call a function with 2 name: "+Style.RESET_ALL+"Use the first and first letters of the function name"+Style.RESET_ALL+Fore.RED+" Example. "+Style.RESET_ALL+"My Profile, you call it this way mp Implement it this way to other function with 2 names")
    print("")
    print(center_text("EXAMPLE"))
    print(Fore.BLUE+"\n to create a post = "+Style.RESET_ALL+"(cp)")
    print("")
    print(Fore.BLUE+" to go to main dashboard ="+Style.RESET_ALL+" (m)")
    print("")
    print(Fore.BLUE+" to go to message = "+Style.RESET_ALL+"(msg)")
    print("")
    print(Fore.BLUE+" to view notifications = "+Style.RESET_ALL+"(ns)")
    print("")
    print(Fore.BLUE+" to go to friend list = "+Style.RESET_ALL+"(mf)")
    print("")
    print(Fore.BLUE+" to refresh = "+Style.RESET_ALL+"(ref)")
    print("")
    print(Fore.BLUE+" to go to profile = "+Style.RESET_ALL+"(pro)")
    print("")
    print(Fore.BLUE+" to go to feeds = "+Style.RESET_ALL+"(f)")
    print("")
    print(Fore.BLUE+" to logout = "+Style.RESET_ALL+"(l)")
    print("")
    print(Fore.BLUE+" to go to settings = "+Style.RESET_ALL+"(set)")
    print("")
    print(Fore.BLUE+" to go to search = "+Style.RESET_ALL+"(srch)")
    print("")
    print(Fore.BLUE+" to comment on a post = "+Style.RESET_ALL+"(c)")
    print("")
    print(Fore.BLUE+" to view comment on a post = "+Style.RESET_ALL+"(vc)")
    print("")
    print(Fore.BLUE+" to like a post = "+Style.RESET_ALL+"(l)")
    print("")
    print(Fore.BLUE+" to view next post = "+Style.RESET_ALL+"(n)")
    print("")
    print(Fore.BLUE+" to return back to any function = "+Style.RESET_ALL+"(b)")
    bm = input(Style.DIM+"\n Input c to continue:  "+Style.RESET_ALL)
    if bm.lower() == 'c':
        huge()
    else:
        print(Fore.RED+"Invalid Input")
        time.sleep(0.9)
        return attention()    
def huge():
    clear_screen()
    print(Fore.BLUE+Style.BRIGHT+"\n"+center_text("Maskbook"))
    print("\n")
    print(Style.DIM+"—"*width)
    print(Style.DIM+"By proceeding, you agree to Terms which includes letting Maskbook to keep your data encrypted.")
    print(Style.DIM+"—"*width)
    print("\n"+Style.RESET_ALL+center_text(" "+"[1]. "+Back.BLUE+" Login "+Style.RESET_ALL+Style.DIM+" | "+Style.RESET_ALL+"[2]. "+Back.WHITE+Fore.BLUE+ " Create new account "+Style.RESET_ALL))
    print("_"*width)
    print("\n"+center_text("[3]. "+Style.DIM+"Forgot password?"))
    print(Style.DIM+"_"*width)
    print("\n")
    choice = input("\n"+Style.DIM+" What's on your mind?   "+Style.RESET_ALL).strip()
    if choice == '1':
        login_users()
    elif choice == '2':
        create_acc()
    elif choice == '3':
        print(Fore.RED+center_text("\nSorry this is'nt available yet..."))
        time.sleep(2)
        return main()
    else:
        print(Fore.RED+"\nInvalid input")
        time.sleep(2)
        return huge()
    
def main():
    clear_screen()
    attention()
if __name__ == "__main__":
    main()                     