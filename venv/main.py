import PySimpleGUI as sg
from lobby import create_lobby_window  # Import lobby window creation
from screens import navigate_des  # Import chart navigator for charts

# Start with the lobby window first
current_window = create_lobby_window()

while True:
    event, values = current_window.read()

    # If the window is closed or exit is clicked
    if event == sg.WIN_CLOSED or event == 'Exit Application':
        break


    # Handle transitions to charts based on buttons in the lobby
    if event == 'Data Chart 1':
        current_window.close()  # Close the current lobby window
        current_window = navigate_des(1)  # Navigate to chart 1

    elif event == 'Data Chart 2':
        current_window.close()  # Close the current lobby window
        current_window = navigate_des(2)  # Navigate to chart 2

    elif event == 'Data Chart 3':
        current_window.close()  # Close the current lobby window
        current_window = navigate_des(3)  # Navigate to chart 3

    # Handle sign-out functionality
    if event == 'Sign Out':
        sg.popup('Signing Out...')
        # Here you can add functionality to sign out the user
        # For example, close all windows and maybe redirect to a login screen

    # Add functionality to return to the lobby from charts
    if event == '-BACK_LOBBY-':
        current_window.close()  # Close the chart window
        current_window = create_lobby_window()  # Reopen the lobby window



# Close the window when done
current_window.close()
