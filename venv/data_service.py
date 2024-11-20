import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np


class DataService:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = pd.DataFrame()
        if file_path:
            self.load_data(file_path)


    def load_data(self, file_path):
        try:
              self.data = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    

    def read_data(self):
        if os.path.exists(self.file_path):
                return pd.read_csv(self.file_path)
        else:
            return pd.DataFrame()
        
    def merge_data(self, new_data):
        self.data = pd.concat([self.data, new_data], ignore_index = True)

    
    def save_data(self):
        self.data.to_csv(self.file_path, index = False)


    # creating the function for the first chart popup (for the first DES page)
def create_chart_des1(self):
    if self.data.empty:
            return None

    # figure means the entire plot, axis is the actual plot
    figure, axis = plt.subplots()
    source = self.data['source'].value_counts().index.tolist()[:7]
    usage = self.data['source'].value_counts().tolist()[:7]

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
def create_chart_des2(self):
    if self.data.empty:
        return None
    services = self.data['services'].value_counts().index.tolist()[:7]
    usage = self.data['services'].value_counts().tolist()[:7]

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
def create_chart_des3(self):
    if self.data.empty:
        return None

        # Data for plotting
    t = self.data['t'].value_counts().index.tolist()[:7]
    s = self.data['t'].value_counts().tolist()[:7]

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