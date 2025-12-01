import json

active_program = True
print("Welcome to the Tiny Password Manager")
print("What would you like to do?")

while active_program:
    user_choice = input("1. Add a new password\n2. Search saved Passwords\n3. Quit\n")

    try:
        user_number = int(user_choice)
    except:
        print("That is not a number, please try again")
        continue

    try:
        with open("Password Manager.json", "r") as f:
            all_entries = json.load(f)
        if isinstance(all_entries, dict):
            all_entries = [all_entries]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        all_entries = []
    if user_number == 1:
        website = input("What is the website?")
        username = input("What is the username")
        password = input("What is the password?")
        entry = {
            "Website": website.lower(),
            "Username": username,
            "Password": password
        }
        all_entries.append(entry)
        with open("Password Manager.json", 'w') as f:
            json.dump(all_entries, f, indent=4)
    elif user_number == 2:
        found = False
        search = input("Enter the website to search for")
        for entry in all_entries:
            if search.lower() in entry['Website']:
                print(entry['Website'])
                print(entry['Username'])
                print(entry['Password'])
                found = True
        if not found:
            print("No entries found for that website")

        '''for entry in all_entries:
            print(f"Website: {entry['Website']}")
            print(f"Username: {entry['Username']}")
            print(f"Password: {entry['Password']}")
            print()'''
    elif user_number == 3:
        break

