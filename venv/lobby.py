import PySimpleGUI as sg

def create_lobby_window():
    # Layout for the Lobby page
    lobby_layout = [
        [sg.Text('Lobby For Analyst', font=('Helvetica', 16), justification='center', expand_x=True)],  # Title Label

        [sg.Push(), sg.Button('Data Chart 1', size=(20, 1)), sg.Push()],  # Data Chart 1 button
        [sg.Push(), sg.Button('Data Chart 2', size=(20, 1)), sg.Push()],  # Data Chart 2 button
        [sg.Push(), sg.Button('Data Chart 3', size=(20, 1)), sg.Push()],  # Data Chart 3 button

        [sg.Push(), sg.Button('Sign Out', size=(10, 1)), sg.Button('Exit Application', size=(15, 1)), sg.Push()]  # Sign Out and Exit buttons
    ]

    # Create the window for Lobby
    lobby_window = sg.Window('Lobby', lobby_layout, element_justification='center', finalize=True)
    return lobby_window
