import PySimpleGUI as sg
import json
import os
from user_manager import UserManager

user_manager = UserManager()

USER_DATA_FILE = "users.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def register_user(username, password):
    users = load_user_data()
    if username in users:
        return False, "This username already exists!"
    users[username] = password
    save_user_data(users)
    return True, "Registration is successful!"

def login_user(username, password):
    users = load_user_data()
    if username in users and users[username] == password:
        return True, "Login successful!"
    return False, "Invalid username or password!"


def login_register_window():
    sg.theme("LightGreen")

    layout = [
        [sg.Text("Login/Register", size=(30, 1), font=("Bell MT", 18), justification="center")],
        [sg.Text("Username:", size=(11, 1)), sg.Input(key="-USERNAME-")],
        [sg.Text("Password:", size=(11, 1)), sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("Login"), sg.Button("Register"), sg.Button("Exit")],
        [sg.Text("", size=(40, 1), key="-MESSAGE-", text_color="pink", justification="center")],
    ]

    window = sg.Window("Login/Register", layout, finalize=True)


    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        username = values["-USERNAME-"]
        password = values["-PASSWORD-"]

        if event == "Login":
            if not username or not password:
                window["-MESSAGE-"].update("You gotta have both username and password!")
                continue
            login_status = user_manager.login(username, password)
            if login_status == "Login Success":
                sg.popup("Welcome!", f"You are logged in as: {username}!")
                break
            else:
                window["-MESSAGE-"].update(login_status)

        elif event == "Register":
            if not username or not password:
                window["-MESSAGE-"].update("You gotta have both username and password!")
                continue
            register_status = user_manager.register(username, password)
            if register_status == "Registration Success":
                sg.popup("Success!", "You can now log in!")
            else:
                window["-MESSAGE-"].update(register_status)

    window.close()

# Run the program
if __name__ == "__main__":
    login_register_window()
