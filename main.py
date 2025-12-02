import json
from cryptography.fernet import Fernet
from pathlib import Path

key_file_path = Path("key.key")
if not key_file_path.exists():
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
else:
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)


def save_entries(file):
    with open("Password Manager.json", 'w') as f:
        json.dump(file, f, indent=4)


def add_entry(file):
    website = input("What is the website?")
    while website == "":
        website = input("Please try again. What is the website?")
    username = input("What is the username: ")
    while username == "":
        username = input("Please try again. What is the username: ")
    password = input("What is the password?")
    while password == "":
        password = input("Please try again. What is the password?")

    encrypted_password = fernet.encrypt(password.encode()).decode()
    entry = {
        "Website": website.lower(),
        "Username": username,
        "Password": encrypted_password
    }
    file.append(entry)
    save_entries(file)


def search_entries(file):
    found = False
    search = input("Enter the website to search for")
    for entry in file:
        if search.lower() in entry['Website']:
            decrypted_password = fernet.decrypt(entry['Password'].encode()).decode()
            print(f"Website: {entry['Website']}")
            print(f"Username: {entry['Username']}")
            print(f"Password: {decrypted_password}")
            found = True
    if not found:
        print("No entries found for that website")


def load_entries():
    try:
        with open("Password Manager.json", "r") as f:
            all_entries = json.load(f)
        if isinstance(all_entries, dict):
            all_entries = [all_entries]
        return all_entries
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []


def update_entry(file):
    updated = input("What website would you like to update?")
    for entry in file:
        if updated.lower() in entry['Website']:
            username = input("What is the username")
            while username == "":
                username = input("Please try again. What is the username?")
            password = input("What is the password?")
            while password == "":
                password = input("Please try again. What is the password?")
            confirm = input(f"Are you sure you want to update {entry['Website']}? (y/n): ")
            if confirm.lower() == 'y':
                entry['Username'] = username
                entry['Password'] = fernet.encrypt(password.encode()).decode()
                save_entries(file)
                print("Entry updated.")
            else:
                print("Update cancelled.")
            return
    print("No entries found for that website.")


def delete_entry(file):
    found = False
    deleted = input("What website would you like to delete?")
    for entry in file:
        if deleted.lower() in entry['Website']:
            found = True
            confirm = input(f"Are you sure that you want to delete {entry['Website']}? (y/n): ")
            if confirm.lower() == 'y':
                file.remove(entry)
                save_entries(file)
                print("Entry deleted")
                return
    if not found:
        print("No entries found for that website")


def main():
    active_program = True
    print("Welcome to the Tiny Password Manager")
    print("What would you like to do?")
    while active_program:
        user_choice = input("1. Add a new password\n2. Update Password\n3. Search saved Passwords\n4. Delete Password\n"
                            "9. Quit\n")

        try:
            user_number = int(user_choice)
        except ValueError:
            print("That is not a number, please try again")
            continue

        entries = load_entries()
        if user_number == 1:
            add_entry(entries)
        elif user_number == 2:
            update_entry(entries)
        elif user_number == 3:
            search_entries(entries)
        elif user_number == 4:
            delete_entry(entries)
        elif user_number == 9:
            break


if __name__ == "__main__":
    main()
