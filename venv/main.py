# importing libraries that would be used for this project
import PySimpleGUI as sg
from lobby import create_lobby_window 
from screens import navigate_des

# ensuring the current window is always the lobby page
current_window = create_lobby_window()

# while that is happening (so that the window is kept open)
while True:
    event, values = current_window.read()

    # if the user chooses to close the application, the window is then closed
    if event == sg.WIN_CLOSED or event == 'Exit Application':
        break

        # if in the lobby, if the user clicks on any of the buttons, the window is closed and the user is taken to the corresponding page
    if event == 'Data Chart 1':
        current_window.close()
        current_window = navigate_des(1)

    elif event == 'Data Chart 2':
        current_window.close()
        current_window = navigate_des(2)

    elif event == 'Data Chart 3':
        current_window.close() 
        current_window = navigate_des(3) 

    # if the user clicks to sign out, they will be 'signed out' (although the functionality isnt in place yet)
    if event == 'Sign Out':
        sg.popup('Signing Out...')

    # if the user clicks to go back to the lobby, the current window (chart page) is closed and the lobby page opens up
    if event == '-BACK_LOBBY-':
        current_window.close()  
        current_window = create_lobby_window() 


# making sure the window is closed when its exited out
current_window.close() 
