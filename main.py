import secrets
import os
from cryptography.fernet import Fernet
import csv
import pandas as pd

# check if there is a directory for the pwd manager files
if os.path.exists("C:/Users/Zone/Documents/pwd-manager") == False:
    os.mkdir("C:/Users/Zone/Documents/pwd-manager")

key = b''
# check that the encryption key has not already been created and saved.
if os.path.exists("C:/Users/Zone/Documents/pwd-manager/encryption-key.key") == False:
    # generate an encryption key
    key = Fernet.generate_key()
    # save encryption key in a key file
    with open("C:/Users/Zone/Documents/pwd-manager/encryption-key.key", "wb") as key_file:
        key_file.write(key)
    # else key file does exist
else:
    # retrieve encryption key
    with open("C:/Users/Zone/Documents/pwd-manager/encryption-key.key", "rb") as key_file:
        key = key_file.read()


def process_option():
    user_option = input(
        "Welcome!\n\nWhat would you like to do:\n1) Create a login:\n2) Retrieve a login:\n3) Delete a login\n4) Exit\n")

    match user_option:
        case "1":
            create_login()
        case "2":
            _ = retrieve_login()
        case "3":
            _ = delete_login()
        case "4":
            return
        case _:
            print("---------\nInvalid option selected, please try again\n-----------")


def create_login():
    platform = input("Enter platform name:\t")
    username = input("Enter username/Email:\t")

    while True:
        pass_option = input(
            "Would you like to:\n1) Enter a password\n2) Generate a randomized password\n")
        if pass_option == "1":
            password = input("Enter your password:\t")
            break
        elif pass_option == "2":
            password = generate_pass()
            break
        else:
            print("\nInvalid input entered! please try again.\n")

    encrypted_pass = encrypt_pass(password)

    login = [platform, username, encrypted_pass]

    append_login(login)


def encrypt_pass(password):
    password_in_bytes = str.encode(password)
    encrypted_pass = Fernet(key).encrypt(password_in_bytes)
    encrypted_pass = encrypted_pass.decode("utf-8")
    return encrypted_pass


def append_login(login):

    if os.path.exists("C:/Users/Zone/Documents/pwd-manager/logins.csv") == False:
        with open("C:/Users/Zone/Documents/pwd-manager/logins.csv", "w") as pass_file:
            csvwriter = csv.writer(pass_file)
            csvwriter.writerow(['Platform', 'Username', 'Password'])

    with open("C:/Users/Zone/Documents/pwd-manager/logins.csv", "a") as pass_file:
        csvwriter = csv.writer(pass_file)
        csvwriter.writerow(login)


def generate_pass():
    password_length = 16

    length_change = input(
        "The default password length is 16 characters\nWould you like to change the passowrd length (y/n):\t").lower()

    while True:
        if length_change == 'y':
            password_length = int(
                input("Enter your desired password length:\t"))
            break
        elif length_change == 'n':
            break
        else:
            length_change = input(
                "You entered an invalid input, please answer only using the letters 'y' or 'n'\nWould you like to change the password length (y/n):\t").lower()

    password = secrets.token_hex(int(password_length/2) + 1)[:password_length]

    print(f"Your password is:\t{password}")

    return password


def retrieve_login():
    platform = input(
        "Which platform's login would you like to retrieve?\t").lower()
    logins = []

    with open("C:/Users/Zone/Documents/pwd-manager/logins.csv", "r") as logins_file:
        csvreader = csv.reader(logins_file)
        for row in csvreader:
            logins.append(row)

    for login in logins:
        platform_name = login[0].lower()
        if platform == platform_name:

            with open("C:/Users/Zone/Documents/pwd-manager/encryption-key.key", "rb") as key_file:
                key = key_file.read()

            username = login[1]
            password = Fernet(key).decrypt(login[2]).decode("utf-8")

            print(f"Username:\t{username}\nPassword:\t{password}")
            return 0

    print("Platform data not found")


def delete_login():
    platform = input(
        "Which platform's login would you like to delete?\t").lower()

    df = pd.read_csv("C:/Users/Zone/Documents/pwd-manager/logins.csv")

    if df.loc[df.Platform == platform].shape[0] == 0:
        print(f"No login credentials for {platform} found!")
        return

    df.drop(df[df.Platform == platform].index, inplace=True)
    df.to_csv("C:/Users/Zone/Documents/pwd-manager/logins.csv")
    print(f"Login credentials for {platform} deleted successfully!")


process_option()
