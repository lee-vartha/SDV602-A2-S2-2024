# importing libraries that would be used for this project
import PySimpleGUI as sg
from data_service import DataService
from lobby import create_lobby_window 
from register import login_register_window
from user_manager import UserManager
from screens import navigate_and_handle_des, select_file, upload_data

def main():
    user_manager = UserManager()

    data_service = DataService(file_path='data.csv')
    print(data_service.data)
    login_register_window()

    if user_manager.current_status == "Logged In":
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
                current_window = navigate_and_handle_des(1, data_service)

            elif event == 'Data Chart 2':
                current_window.close()
                current_window = navigate_and_handle_des(2, data_service)

            elif event == 'Data Chart 3':
                current_window.close() 
                current_window = navigate_and_handle_des(3, data_service) 

            # if the user clicks to sign out, they will be 'signed out' (although the functionality isnt in place yet)
            if event == 'Sign Out':
                sg.popup('Signing Out...')

            # if the user clicks to go back to the lobby, the current window (chart page) is closed and the lobby page opens up
            if event == '-BACK_LOBBY-':
                current_window.close()  
                current_window = create_lobby_window() 

            if event == "-UPLOAD_DATA-":
                file_path = select_file()
                if file_path:
                    new_data = upload_data(file_path)
                    if new_data is not None:
                        data_service.merge_data(new_data)
                        sg.popup("Data is uploaded")


        # making sure the window is closed when its exited out
        current_window.close() 



if __name__ == "__main__":
    main()