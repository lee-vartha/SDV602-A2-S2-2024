# importing the important libraries
import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image
from data_service import DataService
from data_service import create_chart_des1, create_chart_des2, create_chart_des3

def select_file():
    file_path = sg.popup_get_file(
        "Select a file", 
        file_types=(("CSV Files", "*.csv"), ("JSON Files", "*.json")),
        initial_folder="data"

        )
    return file_path


def upload_data(file_path):
    try:
        new_data = pd.read_csv(file_path)
        return new_data
    except Exception as e:
        sg.popup_error(f"Error loading data: {str(e)}")
        return None
    



# creating the function to be able to upload an image (for part 2)
def upload_image(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img = Image.open(img_file)
            img.verify()
            img.seek(0)
            return img
    except Exception as e:
        sg.popup_error(f"Theres an error loading the image: {str(e)}")
        return None
    
#where the charts can go

# creating the window for the charts
def create_window(title, chart_function, data_service):
    layout = [[sg.Text(title, font=('Bell MT', 15), size=(60,1))], # the title for the window
              [sg.Column([
                  [sg.Image(key='-IMAGE-', size=(600, 350))], # the image placeholder spot for the chart/s
                [sg.Text('This will be a comprehensive and show a narrative-like explanation.', # description for the chart (dummy data - will be actual details)
                         key='-CHART_DESC-', size=(50, 2), font=('Bell MT', 15))] 
              ]),
              sg.Column([
                  [sg.Button('Upload Data', key='-UPLOAD_DATA', font=('Bell MT', 15)), # the button to upload the image
                   sg.Button('Set Chart', key='-SET_CHART-', font=('Bell MT', 15))], # the button to set the chart
                   [sg.Multiline(size=(30, 16), key='-CHATBOX-', # the placeholder for the chatbox
                                 disabled=True, autoscroll=True, font=('Bell MT', 15))],
                    [sg.Input(key='-CHAT_INPUT-', size=(25, 5), font=('Bell MT', 15)), # the textbox for the chat
                     sg.Button('Send', key='-SEND_MSG-', font=('Bell MT', 15))] # the 'send' button for the chatbox

              ])],
                [sg.Button('Prev', key='-PREV-', font=('Bell MT', 12)), # the previous button for navigating through each DES
                 sg.Button('Next', key='-NEXT-', font=('Bell MT', 12)), # the next button for navigating through each DES
                 sg.Button('Lobby', key='-BACK_LOBBY-', font=('Bell MT', 12)), sg.Push()] # the button to go back to the lobby
              ]
    
    # creating the window
    window = sg.Window('Data Explorer', layout, finalize=True, resizable=True)
    chart_image = chart_function(data_service)
    window['-IMAGE-'].update(data=chart_image.read()) # ensuring the chart always loads up

    return window

# navigating through each DES page
def navigate_des(des_index, data_service):
    if des_index == 1:
        return create_window('A Statistical Analysis of Music Consumption - Chart 1', create_chart_des1, data_service) # the title for the first DES
    elif des_index == 2: 
        return create_window('A Statistical Analysis of Music Consumption - Chart 2', create_chart_des2, data_service)  # the title for the second DES
    elif des_index == 3:
        return create_window('A Statistical Analysis of Music Consumption - Chart 3', create_chart_des3, data_service)  # the title for the third DES
    
# mapping the des index to the window
data_service = DataService(file_path = 'data.csv')
des_index = 1
window = navigate_des(des_index, data_service)


while True:
    event, values = window.read()


    if event == sg.WIN_CLOSED or event == '-BACK_LOBBY-':
        break

        # if the user clicks on 'next', the index will be incremented by 1 and the window will be closed and the next DES will be opened
    if event == '-NEXT-':
        des_index += 1
        if des_index > 3:
            des_index = 1
        window.close()
        window = navigate_des(des_index, data_service)

        # if the user clicks on 'prev', the index will be decremented by 1 and the window will be closed and the previous DES will be opened
    if event == '-PREV-':
        des_index -= 1
        if des_index < 1:
            des_index = 3
        window.close()
        window = navigate_des(des_index, data_service)

    # if the user uploads an image (part 2 of milestone 3) then the image will be uploaded (should only be either png or jpg)
    if event == '-UPLOAD_DATA':
        file_path = sg.popup_get_file('Get file', file_types=(('CSV Files', '*.csv'),))
        if file_path:
            new_data = pd.read_sdv(file_path) 
            data_service.merge_data(new_data)
            chart_image = data_service.create_chart_des1() if des_index == 1 else data_service.create_chart_des2() if des_index == 2 else data_service.create_chart_des3()
            window['-IMAGE-'].update(data=chart_image.read())

    # if the user clicks 'set image', then it will create the chart for the respective DES page the user is on (updates it)
    if event == '-SET_IMAGE-':
        chart_image = create_chart_des1() if des_index == 1 else create_chart_des2() if des_index == 2 else create_chart_des3()
        window['-IMAGE-'].update(data=chart_image.read())

    # if the user clicks 'send' for the chatbox, then it will update the chatbox with the message the user has sent
    if event == '-SEND_MSG-':
        message = values['-CHAT_INPUT-']
        if message:
            current_chat = window['-CHATBOX-'].get()
            window['-CHATBOX-'].update(f'{current_chat}\nYou: {message}')
            window['-CHAT_INPUT-'].update('')

window.close()
    
