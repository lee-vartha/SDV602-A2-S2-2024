# importing the necessary library
import PySimpleGUI as sg

# creating the lobby window
def create_lobby_window():
    layout = [
        [sg.Text('Lobby For Analyst', font=('Helvetica', 16), justification='center', expand_x=True)],  # title for the page

        # the necessary buttons (for each data chart page)
        [sg.Push(), sg.Button('Data Chart 1', size=(20, 1)), sg.Push()], 
        [sg.Push(), sg.Button('Data Chart 2', size=(20, 1)), sg.Push()], 
        [sg.Push(), sg.Button('Data Chart 3', size=(20, 1)), sg.Push()],  

        # the button to log out
        [sg.Push(), sg.Button('Sign Out', size=(10, 1)), sg.Button('Exit Application', size=(15, 1)), sg.Push()]  
    ]

    # creating the window
    lobby_window = sg.Window('Lobby', layout, element_justification='center', finalize=True)
    return lobby_window
