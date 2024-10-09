import PySimpleGUI as sg
import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image

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
    
def create_chart_des1():
    figure, axis = plt.subplots()
    source = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    usage = [23, 22, 16, 11, 9, 9, 5]

    axis.bar(source, usage, color=['green', 'red', 'blue', 'orange', 'gray', 'yellow', 'purple'])
    axis.set_title('Music Consumption Source (%)', fontsize=10)
    axis.set_ylabel('Percentage', fontsize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(figure)
    buf.seek(0)
    return buf

def create_chart_des2():
    figure, axis = plt.subplots()
    services = ['a', 'b', 'c', 'd', 'e']
    usage = [1, 2, 3, 4, 5]

    axis.pie(usage, labels=services, autopct='%1.1f%%')
    axis.set_title('Music Pie Chart (%), fontsize=10')

    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    plt.close(figure)
    buf.seek(0)
    return buf

def create_chart_des3():
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


def create_window(title, chart_function):
    layout = [[sg.Text(title, font=('Bell MT', 15), size=(60,1))],
              [sg.Column([
                  [sg.Image(key='-IMAGE-', size=(600, 350))],
                [sg.Text('This will be a comprehensive and show a narrative-like explanation.',
                         key='-CHART_DESC-', size=(50, 2), font=('Bell MT', 15))]
              ]),
              sg.Column([
                  [sg.Button('Upload Image', key='-UPLOAD_IMAGE', font=('Bell MT', 15)),
                   sg.Button('Set Chart', key='-SET_CHART-', font=('Bell MT', 15))],
                   [sg.Multiline(size=(30, 16), key='-CHATBOX-', 
                                 disabled=True, autoscroll=True, font=('Bell MT', 15))],
                    [sg.Input(key='-CHAT_INPUT-', size=(25, 5), font=('Bell MT', 15)),
                     sg.Button('Send', key='-SEND_MSG-', font=('Bell MT', 15))]        
              ])],
                [sg.Button('Prev', key='-PREV-', font=('Bell MT', 12)),
                 sg.Button('Next', key='-NEXT-', font=('Bell MT', 12)),
                 sg.Button('Lobby', key='-BACK_LOBBY-', font=('Bell MT', 12)), sg.Push()]
              ]
    
    window = sg.Window('Data Explorer', layout, finalize=True, resizable=True)
    chart_image = chart_function()
    window['-IMAGE-'].update(data=chart_image.read())

    return window

def navigate_des(des_index):
    if des_index == 1:
        return create_window('A Statistical Analysis of Music Consumption - Chart 1', create_chart_des1)
    elif des_index == 2:
        return create_window('A Statistical Analysis of Music Consumption - Chart 2', create_chart_des2)
    elif des_index == 3:
        return create_window('A Statistical Analysis of Music Consumption - Chart 3', create_chart_des3)
    
des_index = 1
window = navigate_des(des_index)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '-BACK_LOBBY-':
        break

    if event == '-NEXT-':
        des_index += 1
        if des_index > 3:
            des_index = 1
        window.close()
        window = navigate_des(des_index)

    if event == '-PREV-':
        des_index -= 1
        if des_index < 1:
            des_index = 3
        window.close()
        window = navigate_des(des_index)

    if event == '-UPLOAD_IMAGE-':
        file_path = sg.popup_get_file('Choose an image', file_types=(('Image Files', '*.png;*.jpg'),))
        if file_path:
            image = upload_image(file_path)
            if image:
                window['-IMAGE-'].update(filename=file_path)

    if event == '-SET_IMAGE-':
        chart_image = create_chart_des1() if des_index == 1 else create_chart_des2() if des_index == 2 else create_chart_des3()
        window['-IMAGE-'].update(data=chart_image.read())

    if event == '-SEND_MSG-':
        message = values['-CHAT_INPUT-']
        if message:
            current_chat = window['-CHATBOX-'].get()
            window['-CHATBOX-'].update(f'{current_chat}\nYou: {message}')
            window['-CHAT_INPUT-'].update('')

window.close()
    
