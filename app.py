"""
Main CLI app.

Usage:
- python app.py
"""
import sqlite3
from db import init_db, get_team_by_name, list_team_names
from auth import create_user, verify_user, user_exists
import getpass
import difflib
import sys

def prompt_register(conn):
    print("\n== Register ==")
    username = input("Choose a username: ").strip()
    if user_exists(conn, username):
        print("Username already exists.")
        return
    password = getpass.getpass("Choose a password: ")
    password2 = getpass.getpass("Confirm password: ")
    if password != password2:
        print("Passwords do not match.")
        return
    created = create_user(conn, username, password)
    if created:
        print("User created. Please login.")
    else:
        print("Failed to create user.")

def prompt_login(conn):
    print("\n== Login ==")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    if verify_user(conn, username, password):
        print(f"Login successful. Welcome, {username}!")
        return username
    else:
        print("Invalid username or password.")
        return None

def lookup_team(conn):
    name = input("\nEnter an MLB team name: ").strip()
    if not name:
        print("No team entered.")
        return
    result = get_team_by_name(conn, name)
    if result is None:
        # try fuzzy match
        names = list_team_names(conn)
        matches = difflib.get_close_matches(name, names, n=5, cutoff=0.5)
        if matches:
            print("Team not found exactly. Did you mean:")
            for m in matches:
                print(" -", m)
        else:
            print("Team not found. Try a different name.")
    elif isinstance(result, list):
        print("Multiple teams matched:")
        for row in result:
            print(f" - {row['name']} ({row['division']}): Rivals: {row['rivals']}")
    else:
        print(f"\nTeam: {result['name']}")
        print(f"Division: {result['division']}")
        print(f"Biggest rivals: {result['rivals']}")

def main():
    conn = init_db()
    print("Simple MLB lookup with login")
    while True:
        print("\nOptions:")
        print(" 1) Register")
        print(" 2) Login")
        print(" 3) Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            prompt_register(conn)
        elif choice == "2":
            user = prompt_login(conn)
            if user:
                # after login, do team lookup once, then exit or allow repeated queries
                while True:
                    lookup_team(conn)
                    cont = input("\nLookup another team? (y/N): ").strip().lower()
                    if cont != "y":
                        print("Logging out.")
                        break
        elif choice == "3":
            print("Goodbye.")
            conn.close()
            sys.exit(0)
        else:
            print("Unknown option. Choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
