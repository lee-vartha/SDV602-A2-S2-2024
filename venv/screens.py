import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image
from data_service import DataService
from register import login_register_window
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
    # creating the function for the first chart popup (for the first DES page)
def create_chart_des1(data):
    if data.empty:
        return None
    
    # figure means the entire plot, axis is the actual plot
    figure, axis = plt.subplots()
    # the sources are just dummy data - in part 2, the actual data would be conducted
    source = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    usage = [23, 22, 16, 11, 9, 9, 5]

    # designing the bar chart - including the source, usage and creating colours for it
    axis.bar(source, usage, color=['green', 'red', 'blue', 'orange', 'gray', 'yellow', 'purple'])
    # setting the title and the label for the chart
    axis.set_title('Music Consumption Source (%)', fontsize=10)
    axis.set_ylabel('Percentage', fontsize=8)

    # saving the plot as PNG - this is necessary since PySimpleGUI only accepts PNG images
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(figure)
    buf.seek(0)
    return buf

# creating the function for the second chart (for the second DES page)
def create_chart_des2(data):
    if data.empty:
        return None

    figure, axis = plt.subplots()
    # the services and usage are dummy data
    services = ['a', 'b', 'c', 'd', 'e']
    usage = [1, 2, 3, 4, 5]

    # creating a PIE chart - autopct is percentage, which shows up on the pie chart 
    axis.pie(usage, labels=services, autopct='%1.1f%%')
    # setting the title
    axis.set_title('Music Pie Chart (%), fontsize=10')

    # saving the plot as PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(figure)
    buf.seek(0)
    return buf

# creating the function for the third chart (for the third DES page)
# this is linked from https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html#sphx-glr-gallery-lines-bars-and-markers-simple-plot-py
# ^^ for inspiration for the meantime
def create_chart_des3(data):
    if data.empty:
        return None

        # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    figure, axis = plt.subplots()
    axis.plot(t, s)

    axis.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    axis.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(figure)
    buf.seek(0)
    return buf

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
    chart_image = chart_function(data_service.data)
    if chart_image:
        window['-IMAGE-'].update(data=chart_image.read()) # ensuring the chart always loads up
    else:
        sg.popup_error('No data available to create chart')
    return window

# navigating through each DES page
def navigate_des(des_index, data_service):

    if des_index == 1:
        return create_window('A Statistical Analysis of Music Consumption - Chart 1', create_chart_des1, data_service) # the title for the first DES
    elif des_index == 2: 
        return create_window('A Statistical Analysis of Music Consumption - Chart 2', create_chart_des2, data_service)  # the title for the second DES
    elif des_index == 3:
        return create_window('A Statistical Analysis of Music Consumption - Chart 3', create_chart_des3, data_service)  # the title for the third DES
    
# # mapping the des index to the window
# data_service = DataService(file_path = 'data.csv')
# if login_register_window():
#     des_index = 1
#     window = navigate_des(des_index, data_service)

def navigate_and_handle_des(des_index, data_service):
    window = navigate_des(des_index, data_service)
    while True:
        event, values = window.read()


        if event == sg.WIN_CLOSED or event == '-BACK_LOBBY-':
            break

            # if the user clicks on 'next', the index will be incremented by 1 and the window will be closed and the next DES will be opened
        if event == '-NEXT-':
            des_index += 1 if des_index == 3 else des_index + 1
            window.close()
            window = navigate_des(des_index, data_service)

            # if the user clicks on 'prev', the index will be decremented by 1 and the window will be closed and the previous DES will be opened
        if event == '-PREV-':
            des_index = 3 if des_index == 1 else des_index - 1
            window.close()
            window = navigate_des(des_index, data_service)

        # if the user uploads an image (part 2 of milestone 3) then the image will be uploaded (should only be either png or jpg)
        if event == '-UPLOAD_DATA':
            file_path = select_file()
            if file_path:
                new_data = upload_data(file_path) 
                if new_data is not None:
                    data_service.merge_data(new_data)
                    sg.popup("Data is uploaded")

        # if the user clicks 'set image', then it will create the chart for the respective DES page the user is on (updates it)
        if event == '-SET_CHART-':
            chart_image = (create_chart_des1(data_service.data) if des_index == 1 else 
            create_chart_des2(data_service.data) if des_index == 2 else
            create_chart_des3(data_service.data))

            if chart_image:
                window['-IMAGE-'].update(data=chart_image.read())
            else:
                sg.popup_error('No data available to create chart')


        # if the user clicks 'send' for the chatbox, then it will update the chatbox with the message the user has sent
        if event == '-SEND_MSG-':
            message = values['-CHAT_INPUT-']
            if message:
                current_chat = window['-CHATBOX-'].get()
                window['-CHATBOX-'].update(f'{current_chat}\nYou: {message}')
                window['-CHAT_INPUT-'].update('')

    window.close()