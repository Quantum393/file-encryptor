import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    STRIKE = '\u0336'


def generate_key():
    return Fernet.generate_key()


def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)


def load_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()


def encrypt_file(filename, key):
    fernet = Fernet(key)
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()

        encrypted_data = fernet.encrypt(file_data)

        encrypted_filename = os.path.basename(filename)  # Get the base filename

        name = encrypted_filename.split('.')

        if len(name) < 2:
            print(
                f"\n{bcolors.BOLD}{bcolors.FAIL}[ERROR 02]: Unable to construct encrypted file path for '{filename}'{bcolors.ENDC}")
            raise LookupError

        encrypted_file_path = os.path.join(os.path.dirname(filename), encrypted_filename)
        file_path = os.path.join(os.path.dirname(filename), f"{name[0]}.{name[1]}.encrypted")

        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        os.rename(encrypted_file_path, f"{file_path}")  # Rename the original file
        show_encrypted_popup(encrypted_filename)  # Pass only the base filename

    except PermissionError:
        print(
            f"\n{bcolors.BOLD}{bcolors.FAIL}[ERROR 01]: Unable to get permission to encrypt file: '{filename}'{bcolors.ENDC}")
        pass
    except LookupError:
        pass


def show_encrypted_popup(filename):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
def encrypt_all_files(directory, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.startswith('ENCRYPTED-'):
                file_path = os.path.join(root, filename)
                encrypt_file(file_path, key)
                print(f"Encrypted: {file_path} -> {os.path.basename(file_path)}.encrypted")


def decrypt_all_files(directory, key):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".encrypted"):
                file_path = os.path.join(root, filename)
                decrypt_file(file_path, key)
                print(f"Decrypted: {file_path} -> {os.path.basename(file_path).strip('.encrypted')}")


def decrypt_file(filename, key):
    fernet = Fernet(key)
    with open(f'{filename}', 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    encrypted_filename = os.path.basename(filename)  # Get the base filename

    encrypted_file_path = os.path.join(os.path.dirname(filename), encrypted_filename)

    with open(f'{filename}', 'wb') as dec_file:
        dec_file.write(decrypted)
    new_name = filename[:-10]
    file_path = os.path.join(os.path.dirname(filename), f"{new_name}")
    os.rename(encrypted_file_path, f"{file_path}")  # Rename the original file


def window():
    window = tk.Tk()
    window.configure(background='red')

    window.attributes('-fullscreen', True, '-topmost', True)
    # window.attributes('-fullscreen', True)
    window.title("title")
    label = tk.Label(window, text="text")
    text = Text(window, height=25,
                width=25,
                bg="black")
    text.insert(END, "")
    label.pack()
    text.pack()

    window.mainloop()


def on_closing():
    pass


def main():
    key_filename = 'encryption_key.key'

    if not os.path.exists(key_filename):
        key = generate_key()
        save_key(key, key_filename)
        print(f"{key_filename} -> {os.path.basename(key)}")
    else:
        key = load_key(key_filename)

    while True:
        print(f'''\n{bcolors.HEADER}{bcolors.BOLD}  __         ______     ______     __  __        ______     ______     __  __    
 /\ \       /\  __ \   /\  ___\   /\ \/ /       /\  == \   /\  __ \   /\_\_\_\   
 \ \ \____  \ \ \/\ \  \ \ \____  \ \  _"-.     \ \  __<   \ \ \/\ \  \/_/\_\/_  
 \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\     \ \_____\  \ \_____\   /\_\/\_\ 
 \/_____/   \/_____/   \/_____/   \/_/\/_/      \/_____/   \/_____/   \/_/\/_/ 
              {bcolors.ENDC}''')
        print(f"\n{bcolors.BOLD}{bcolors.UNDERLINE}Secure Data Management Tool{bcolors.ENDC}")
        print(f"\n{bcolors.OKCYAN}[1.] Encrypt a file{bcolors.ENDC}")
        print(f"\n{bcolors.FAIL}[2.] DANGEROUS -> Encrypt an entire directory{bcolors.ENDC}")
        print(f"\n{bcolors.OKGREEN}[3.] Decrypt a directory{bcolors.ENDC}")
        print(f"\n{bcolors.OKBLUE}[4.] Exit{bcolors.ENDC}")

        choice = input("\nSelect an option: ")

        if choice == '1':
            filename = input("Enter the filename to encrypt: ")
            encrypt_file(filename, key)
            print("File encrypted successfully.")
        elif choice == '2':
            count = 0
            print(
                f"\n \n{bcolors.WARNING}{bcolors.BOLD}Would you like to proceed, this may cause irreversible damage: y/n {bcolors.ENDC}")
            confirm = input("\n \n")
            if confirm == 'n':
                break
            elif confirm == 'y':
                # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                # downloads = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
                # pictures = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Pictures')
                print("\nEnter a directory to encrypt: ")
                directory = input("\n")
                list_of_directories = [directory]

                # list_of_directories = [desktop, downloads, pictures]

                for directory in list_of_directories:
                    encrypt_all_files(directory, key)
                    count += 1

                print(
                    f"\n \n{bcolors.OKGREEN}{bcolors.BOLD}{count} files in the directory have been encrypted successfully.{bcolors.ENDC}")
                messagebox.showwarning("LockBox", "All files have been encrypted", icon="info")

        elif choice == '3':
            filename = input(f"\n{bcolors.OKCYAN}Enter the directory to decrypt: {bcolors.ENDC} ")

            key = input(f"\n\n{bcolors.OKCYAN}Enter your decryption key: {bcolors.ENDC} ")

            decrypt_all_files(filename, key)
            print(f"\n\n{bcolors.OKGREEN}{bcolors.BOLD}Files decrypted successfully. {bcolors.ENDC} ")
            messagebox.showwarning("LockBox", "Files decrypted successfully", icon="info")

        elif choice == '4':
            print("\n")
            break
        else:
            print(f"{bcolors.FAIL}\nInvalid choice. Please select a valid option.{bcolors.ENDC}")


if __name__ == '__main__':
    main()
